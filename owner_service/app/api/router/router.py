from fastapi import HTTPException, APIRouter
from typing import List

from app.api.database import db_manager
from app.api.model.restaurant import RestaurantIn, RestaurantOut, RestaurantUpdate

router = APIRouter()


@router.get('/', response_model=List[RestaurantOut])
async def index():
    # Получаем все рестораны из базы данных
    return await db_manager.get_all_restaurants()


@router.post('/', status_code=201, response_model=RestaurantOut)
async def add_restaurant(payload: RestaurantIn):
    # Добавляем новый ресторан в базу данных
    restaurant_id = await db_manager.add_restaurant(payload)
    return {**payload.dict(), 'id': restaurant_id}


@router.put('/{id}', response_model=RestaurantOut)
async def update_restaurant(id: int, payload: RestaurantUpdate):
    # Получаем ресторан из базы данных
    restaurant = await db_manager.get_restaurant(id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant with given id not found")

    # Обновляем ресторан, используя только измененные поля
    updated_restaurant = await db_manager.update_restaurant(id, payload)

    return updated_restaurant


@router.delete('/{id}', response_model=RestaurantOut)
async def delete_restaurant(id: int):
    # Получаем ресторан для удаления
    restaurant = await db_manager.get_restaurant(id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant with given id not found")

    # Удаляем ресторан из базы данных
    await db_manager.delete_restaurant(id)
    return restaurant
