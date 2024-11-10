from typing import List

from fastapi import APIRouter, status

from app.api.database.db_manager import get_all_restaurants, get_dishes_by_restaurant
from app.api.model.dish import Dish
from app.api.model.restaurant import Restaurant

# Создаем роутер для маршрутов
view_router = APIRouter()


@view_router.get(
    path='/restaurants',
    response_model=List[Restaurant],
    status_code=status.HTTP_200_OK)
async def get_restaurants():
    """
    Получение списка всех ресторанов.
    """
    restaurants = await get_all_restaurants()
    return restaurants


@view_router.get(
    path='/restaurants/{restaurant_id}/dishes',
    response_model=List[Dish],
    status_code=status.HTTP_200_OK)
async def get_dishes_by_restaurant_id(restaurant_id: int):
    """
    Получение списка блюд для заданного ресторана по его ID.
    """
    dishes = await get_dishes_by_restaurant(restaurant_id)
    return dishes
