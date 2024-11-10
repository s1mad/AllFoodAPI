import logging
from fastapi import HTTPException
from sqlalchemy import select

from app.api.database.database import restaurants, database, dishes
from app.api.model.dish import DishOut, DishIn, DishUpdate
from app.api.model.restaurant import RestaurantIn, RestaurantOut, RestaurantUpdate, Restaurant

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def get_restaurants_by_user(user_id: int):
    """
    Получает все рестораны, принадлежащие пользователю по его ID.

    :param user_id: ID пользователя
    :return: Список ресторанов пользователя
    """
    logging.info(f"Fetching restaurants for user with ID {user_id}.")
    query = select(restaurants).where(user_id == restaurants.c.user_id)
    result = await database.fetch_all(query)
    logging.info(f"Found {len(result)} restaurants for user {user_id}.")
    return [Restaurant(**row) for row in result]


async def get_restaurant(id: int):
    """
    Получает ресторан по его ID.

    :param id: ID ресторана
    :return: Ресторан с данным ID
    """
    logging.info(f"Fetching restaurant with ID {id}.")
    query = select(restaurants).where(id == restaurants.c.id)
    result = await database.fetch_one(query)
    if result:
        logging.info(f"Found restaurant with ID {id}.")
        return RestaurantOut(**result)
    logging.warning(f"Restaurant with ID {id} not found.")
    return None


async def user_is_own_restaurant(user_id: int, restaurant_id: int) -> bool:
    """
    Проверяет, является ли пользователь владельцем данного ресторана.

    :param user_id: ID пользователя
    :param restaurant_id: ID ресторана
    :return: True, если пользователь является владельцем ресторана, иначе False
    """
    logging.info(f"Checking ownership for user {user_id} and restaurant {restaurant_id}.")
    query = select(restaurants).where(
        (restaurant_id == restaurants.c.id) & (user_id == restaurants.c.user_id)
    )
    result = await database.fetch_one(query)
    if result:
        logging.info(f"User {user_id} is the owner of restaurant {restaurant_id}.")
        return True
    logging.warning(f"User {user_id} is not the owner of restaurant {restaurant_id}.")
    return False


async def add_restaurant(user_id: int, payload: RestaurantIn):
    """
    Добавляет новый ресторан в базу данных.

    :param user_id: ID владельца ресторана
    :param payload: Данные нового ресторана
    :return: ID нового ресторана
    """
    logging.info(f"Adding new restaurant for user {user_id} with name {payload.name}.")
    query = restaurants.insert().values(
        name=payload.name,
        address=payload.address,
        user_id=user_id
    )
    result = await database.execute(query)
    logging.info(f"Restaurant added successfully with ID {result}.")
    return result


async def update_restaurant(id: int, payload: RestaurantUpdate):
    """
    Обновляет данные ресторана.

    :param id: ID ресторана
    :param payload: Данные для обновления
    :return: Обновленные данные ресторана
    """
    logging.info(f"Updating restaurant with ID {id}.")
    # Получаем ресторан из базы данных
    existing_restaurant = await get_restaurant(id)
    if not existing_restaurant:
        logging.error(f"Restaurant with ID {id} not found.")
        raise HTTPException(status_code=404, detail="Restaurant with given id not found")

    # Обновляем только те поля, которые указаны в payload
    update_data = payload.dict(exclude_unset=True)
    query = restaurants.update().where(restaurants.c.id == id).values(update_data)
    await database.execute(query)

    updated_restaurant = await get_restaurant(id)
    logging.info(f"Restaurant with ID {id} updated successfully.")
    return updated_restaurant


async def delete_restaurant(id: int):
    """
    Удаляет ресторан по ID и все связанные с ним блюда.

    :param id: ID ресторана для удаления
    :return: Сообщение об успешном удалении
    """
    logging.info(f"Deleting restaurant with ID {id}.")
    # Сначала удаляем все блюда, связанные с рестораном
    delete_dishes_query = dishes.delete().where(dishes.c.restaurant_id == id)
    await database.execute(delete_dishes_query)

    # Удаляем сам ресторан
    query = restaurants.delete().where(restaurants.c.id == id)
    await database.execute(query)

    logging.info(f"Restaurant with ID {id} deleted successfully.")
    return {"message": "Restaurant deleted successfully"}


async def get_dishes_by_restaurant(restaurant_id: int):
    """
    Получает все блюда для ресторана по его ID.

    :param restaurant_id: ID ресторана
    :return: Список всех блюд ресторана
    """
    logging.info(f"Fetching dishes for restaurant with ID {restaurant_id}.")
    query = select(dishes).where(restaurant_id == dishes.c.restaurant_id)
    result = await database.fetch_all(query)
    logging.info(f"Found {len(result)} dishes for restaurant {restaurant_id}.")
    return result


async def get_dish(id: int):
    """
    Получает блюдо по его ID.

    :param id: ID блюда
    :return: Блюдо с данным ID
    """
    logging.info(f"Fetching dish with ID {id}.")
    query = select(dishes).where(id == dishes.c.id)
    result = await database.fetch_one(query)
    if result:
        logging.info(f"Found dish with ID {id}.")
        return DishOut(**result)
    logging.warning(f"Dish with ID {id} not found.")
    return None


async def add_dish(restaurant_id: int, payload: DishIn):
    """
    Добавляет новое блюдо в ресторан.

    :param restaurant_id: ID ресторана, к которому добавляется блюдо
    :param payload: Данные нового блюда
    :return: ID нового блюда
    """
    logging.info(f"Adding new dish to restaurant {restaurant_id} with name {payload.name}.")
    query = dishes.insert().values(
        name=payload.name,
        ingredients=payload.ingredients,
        price=payload.price,
        restaurant_id=restaurant_id
    )
    result = await database.execute(query)
    logging.info(f"Dish added successfully with ID {result}.")
    return result


async def update_dish(id: int, payload: DishUpdate):
    """
    Обновляет данные блюда.

    :param id: ID блюда
    :param payload: Данные для обновления
    :return: Обновленные данные блюда
    """
    logging.info(f"Updating dish with ID {id}.")
    # Получаем блюдо из базы данных
    existing_dish = await get_dish(id)
    if not existing_dish:
        logging.error(f"Dish with ID {id} not found.")
        raise HTTPException(status_code=404, detail="Dish with given id not found")

    # Обновляем только те поля, которые указаны в payload
    update_data = payload.dict(exclude_unset=True)
    query = dishes.update().where(dishes.c.id == id).values(update_data)
    await database.execute(query)

    updated_dish = await get_dish(id)
    logging.info(f"Dish with ID {id} updated successfully.")
    return updated_dish


async def delete_dish(id: int):
    """
    Удаляет блюдо по ID.

    :param id: ID блюда для удаления
    :return: Сообщение об успешном удалении
    """
    logging.info(f"Deleting dish with ID {id}.")
    query = dishes.delete().where(dishes.c.id == id)
    await database.execute(query)
    logging.info(f"Dish with ID {id} deleted successfully.")
    return {"message": "Dish deleted successfully"}
