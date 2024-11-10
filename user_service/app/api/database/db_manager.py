import logging

from sqlalchemy import select

from app.api.database.database import restaurants, database, dishes
from app.api.model.dish import Dish
from app.api.model.restaurant import Restaurant


async def get_all_restaurants():
    """
    Получение списка всех ресторанов.
    Эта функция выполняет запрос к базе данных для получения всех ресторанов и возвращает их в виде списка объектов `Restaurant`.
    """
    query = select(restaurants)
    result = await database.fetch_all(query)
    logging.info("Successfully fetched all restaurants from the database.")
    return [Restaurant(**row) for row in result]


async def get_dishes_by_restaurant(restaurant_id: int):
    """
    Получение списка блюд конкретного ресторана по его ID.
    Эта функция выполняет запрос к базе данных для получения всех блюд, которые принадлежат ресторану с заданным ID.
    """
    query = select(dishes).where(restaurant_id == dishes.c.restaurant_id)
    result = await database.fetch_all(query)
    logging.info("Successfully fetched all restaurants from the database.")
    return [Dish(**row) for row in result]
