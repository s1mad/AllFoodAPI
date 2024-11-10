from typing import List
from fastapi import APIRouter, HTTPException, status

from app.api.database import db_manager
from app.api.database.db_manager import get_restaurants_by_user, get_restaurant, user_is_own_restaurant
from app.api.model.restaurant import RestaurantIn, RestaurantUpdate, Restaurant
from app.api.utils.get_current_user import get_current_user

# Инициализация маршрутизатора для управления ресторанами
restaurant_router = APIRouter()


@restaurant_router.get(
    path='/restaurants',
    response_model=List[Restaurant],
    status_code=status.HTTP_200_OK)
async def get_user_restaurants(token: str):
    """
    Получает список ресторанов, принадлежащих текущему пользователю.
    """
    current_user = await get_current_user(token)
    if current_user.get("is_owner"):
        return await get_restaurants_by_user(current_user["id"])
    raise HTTPException(status_code=403, detail="Доступ запрещен")


@restaurant_router.post(
    path='/restaurant',
    response_model=Restaurant,
    status_code=status.HTTP_201_CREATED)
async def add_restaurant(payload: RestaurantIn, token: str):
    """
    Добавляет новый ресторан, принадлежащий текущему пользователю.
    """
    current_user = await get_current_user(token)
    if current_user.get("is_owner"):
        restaurant_id = await db_manager.add_restaurant(current_user["id"], payload)
        restaurant = await get_restaurant(restaurant_id)
        return restaurant
    raise HTTPException(status_code=403, detail="Доступ запрещен")


@restaurant_router.put(
    path='/restaurant/{id}',
    response_model=Restaurant)
async def update_restaurant(id: int, payload: RestaurantUpdate, token: str):
    """
    Обновляет информацию о ресторане текущего пользователя.
    """
    current_user = await get_current_user(token)
    if current_user.get("is_owner") and await user_is_own_restaurant(current_user["id"], id):
        updated_restaurant = await db_manager.update_restaurant(id, payload)
        return updated_restaurant
    raise HTTPException(status_code=403, detail="Доступ запрещен")


@restaurant_router.delete(
    path='/restaurant/{id}',
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant(id: int, token: str):
    """
    Удаляет ресторан текущего пользователя.
    """
    current_user = await get_current_user(token)
    if current_user.get("is_owner") and await user_is_own_restaurant(current_user["id"], id):
        await db_manager.delete_restaurant(id)
        return
    raise HTTPException(status_code=403, detail="Доступ запрещен")
