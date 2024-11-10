from typing import List
from fastapi import APIRouter, HTTPException, status
from app.api.database import db_manager
from app.api.database.db_manager import get_dishes_by_restaurant, user_is_own_restaurant
from app.api.model.dish import DishOut, DishIn, DishUpdate
from app.api.utils.get_current_user import get_current_user

# Инициализация маршрутизатора для управления блюдами
dish_router = APIRouter()


@dish_router.get(
    path='/restaurant/{restaurant_id}/dish',
    response_model=List[DishOut],
    status_code=status.HTTP_200_OK)
async def get_restaurant_dishes(restaurant_id: int, token: str):
    """
    Получает список блюд для ресторана текущего пользователя.
    """
    current_user = await get_current_user(token)
    if current_user.get("is_owner") and await user_is_own_restaurant(current_user["id"], restaurant_id):
        return await get_dishes_by_restaurant(restaurant_id)
    raise HTTPException(status_code=403, detail="Доступ запрещен")


@dish_router.post(
    path='/restaurant/{restaurant_id}/dish',
    response_model=DishOut,
    status_code=status.HTTP_201_CREATED)
async def add_dish(restaurant_id: int, payload: DishIn, token: str):
    """
    Добавляет новое блюдо в ресторан текущего пользователя.
    """
    current_user = await get_current_user(token)
    if current_user.get("is_owner") and await user_is_own_restaurant(current_user["id"], restaurant_id):
        dish_id = await db_manager.add_dish(restaurant_id, payload)
        dish = await db_manager.get_dish(dish_id)
        return dish
    raise HTTPException(status_code=403, detail="Доступ запрещен")


@dish_router.put(
    path='/restaurant/{restaurant_id}/dish/{dish_id}',
    response_model=DishOut)
async def update_dish(restaurant_id: int, dish_id: int, token: str, payload: DishUpdate):
    """
    Обновляет информацию о блюде в ресторане текущего пользователя.
    """
    current_user = await get_current_user(token)
    if current_user.get("is_owner") and await user_is_own_restaurant(current_user["id"], restaurant_id):
        updated_dish = await db_manager.update_dish(dish_id, payload)
        return updated_dish
    raise HTTPException(status_code=403, detail="Доступ запрещен")


@dish_router.delete(
    path='/restaurant/{restaurant_id}/dish/{dish_id}',
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(restaurant_id: int, dish_id: int, token: str):
    """
    Удаляет блюдо из ресторана текущего пользователя.
    """
    current_user = await get_current_user(token)
    if current_user.get("is_owner") and await user_is_own_restaurant(current_user["id"], restaurant_id):
        await db_manager.delete_dish(dish_id)
        return
    raise HTTPException(status_code=403, detail="Доступ запрещен")
