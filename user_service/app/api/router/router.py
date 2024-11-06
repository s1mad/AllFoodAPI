from fastapi import HTTPException, APIRouter
from typing import List

from app.api.database.db_manager import get_all_restaurants, get_dishes_by_restaurant, create_order
from app.api.model.dish import Dish
from app.api.model.order_request import OrderRequest
from app.api.model.restaurant import Restaurant

router = APIRouter()


@router.get('/restaurants', response_model=List[Restaurant])
async def read_restaurants():
    return await get_all_restaurants()


@router.get('/restaurants/{restaurant_id}/dishes', response_model=List[Dish])
async def read_dishes(restaurant_id: int):
    dishes = await get_dishes_by_restaurant(restaurant_id)
    if not dishes:
        raise HTTPException(status_code=404, detail="Dishes not found for this restaurant")
    return dishes


@router.post('/order', response_model=dict)
async def place_order(order: OrderRequest):
    return await create_order(order)
