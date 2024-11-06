from fastapi import HTTPException

from app.api.model.restaurant import RestaurantIn, RestaurantOut, RestaurantUpdate
from app.api.database.database import restaurants
from databases import Database
from sqlalchemy import select

DATABASE_URL = 'sqlite:///./all_food_db.sqlite'
database = Database(DATABASE_URL)


# Получаем все рестораны
async def get_all_restaurants():
    query = select(restaurants)
    result = await database.fetch_all(query)
    # Возвращаем данные в формате Pydantic, создавая объекты RestaurantOut
    return [RestaurantOut(**row) for row in result]


# Получаем ресторан по ID
async def get_restaurant(id: int):
    query = select(restaurants).where(restaurants.c.id == id)
    result = await database.fetch_one(query)
    if result:
        return RestaurantOut(**result)
    return None


# Добавляем новый ресторан
async def add_restaurant(payload: RestaurantIn):
    query = restaurants.insert().values(name=payload.name, address=payload.address)
    # Выполняем вставку в базу данных
    result = await database.execute(query)
    # Возвращаем ID добавленного ресторана
    return result


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
