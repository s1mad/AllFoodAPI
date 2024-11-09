from typing import List

from fastapi import HTTPException, APIRouter

from app.api.database.db_manager import get_all_restaurants, get_dishes_by_restaurant
from app.api.model.dish import Dish
from app.api.model.order_request import OrderRequest
from app.api.model.restaurant import Restaurant

router = APIRouter()


@router.get('/restaurants', response_model=List[Restaurant])
async def get_restaurants():
    return await get_all_restaurants()


@router.get('/restaurants/{restaurant_id}/dishes', response_model=List[Dish])
async def get_dishes_by_restaurant_id(restaurant_id: int):
    return await get_dishes_by_restaurant(restaurant_id)


@router.post('/order', response_model=dict)
async def create_order(token: str, order: OrderRequest):
    # Здесь могла бы быть логика отправки заказа
    # Пока просто возвращаем сообщение об успехе
    return {"message": "Order successfully sent to restaurant"}
