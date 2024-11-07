from fastapi import HTTPException
from sqlalchemy import select

from app.api.database.database import restaurants, database, dishes
from app.api.model.dish import DishOut, DishIn, DishUpdate
from app.api.model.restaurant import RestaurantIn, RestaurantOut, RestaurantUpdate


# Получаем все рестораны пользователя
async def get_restaurants_by_user(user_id: int):
    query = select(restaurants).where(user_id == restaurants.c.user_id)
    result = await database.fetch_all(query)
    return result


# Получаем ресторан по ID
async def get_restaurant(id: int):
    query = select(restaurants).where(id == restaurants.c.id)
    result = await database.fetch_one(query)
    if result: return RestaurantOut(**result)
    return None


# Добавляем новый ресторан
async def add_restaurant(user_id: int, payload: RestaurantIn):
    query = restaurants.insert().values(
        name=payload.name,
        address=payload.address,
        user_id=user_id
    )
    result = await database.execute(query)  # Выполняем вставку в базу данных
    return result  # Возвращаем ID добавленного ресторана


# Обновляем данные ресторана
async def update_restaurant(id: int, payload: RestaurantUpdate):
    # Получаем ресторан из базы данных
    existing_restaurant = await get_restaurant(id)
    if not existing_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant with given id not found")

    # Обновляем только те поля, которые указаны в payload
    update_data = payload.dict(exclude_unset=True)

    # Формируем запрос для обновления
    query = restaurants.update().where(restaurants.c.id == id).values(update_data)
    await database.execute(query)

    # Возвращаем обновленные данные ресторана
    updated_restaurant = await get_restaurant(id)
    return updated_restaurant


# Удаляем ресторан
async def delete_restaurant(id: int):
    query = restaurants.delete().where(restaurants.c.id == id)
    await database.execute(query)
    return {"message": "Restaurant deleted successfully"}


# Получаем все блюда ресторана
async def get_dishes_by_restaurant(restaurant_id: int):
    query = select(dishes).where(restaurant_id == dishes.c.restaurant_id)
    result = await database.fetch_all(query)
    return result


# Получаем блюдо по ID
async def get_dish(id: int):
    query = select(dishes).where(id == dishes.c.id)
    result = await database.fetch_one(query)
    if result: return DishOut(**result)
    return None


# Добавляем новое блюдо
async def add_dish(restaurant_id: int, payload: DishIn):
    query = dishes.insert().values(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        restaurant_id=restaurant_id
    )
    result = await database.execute(query)  # Выполняем вставку в базу данных
    return result  # Возвращаем ID добавленного блюда


# Обновляем данные блюда
async def update_dish(id: int, payload: DishUpdate):
    # Получаем блюдо из базы данных
    existing_dish = await get_dish(id)
    if not existing_dish: raise HTTPException(status_code=404, detail="Dish with given id not found")

    # Обновляем только те поля, которые указаны в payload
    update_data = payload.dict(exclude_unset=True)

    # Формируем запрос для обновления
    query = dishes.update().where(dishes.c.id == id).values(update_data)
    await database.execute(query)

    # Возвращаем обновленные данные блюда
    updated_dish = await get_dish(id)
    return updated_dish


# Удаляем блюдо
async def delete_dish(id: int):
    query = dishes.delete().where(dishes.c.id == id)
    await database.execute(query)
    return {"message": "Dish deleted successfully"}
