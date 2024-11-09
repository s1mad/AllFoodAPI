from typing import List

from fastapi import APIRouter, HTTPException

from app.api.database import db_manager
from app.api.database.db_manager import get_restaurants_by_user, get_restaurant, user_is_own_restaurant, \
    get_dishes_by_restaurant
from app.api.model.dish import DishOut, DishIn, DishUpdate
from app.api.model.restaurant import RestaurantIn, RestaurantUpdate, Restaurant
from app.api.util.get_current_user import get_current_user

router = APIRouter()


@router.get('/restaurants', response_model=List[Restaurant])
async def get_user_restaurants(token: str):
    current_user = await get_current_user(token)
    if current_user.get("is_owner") is True:
        return await get_restaurants_by_user(current_user["id"])

    raise HTTPException(status_code=403, detail="Not authorized to access this resource")


@router.post('/restaurant', status_code=201, response_model=Restaurant)
async def add_restaurant(payload: RestaurantIn, token: str):
    current_user = await get_current_user(token)
    if current_user.get("is_owner") is True:
        restaurant_id = await db_manager.add_restaurant(current_user["id"], payload)
        restaurant = await get_restaurant(restaurant_id)
        return restaurant

    raise HTTPException(status_code=403, detail="Not authorized to access this resource")


@router.put('/restaurant/{id}', response_model=Restaurant)
async def update_restaurant(id: int, payload: RestaurantUpdate, token: str):
    current_user = await get_current_user(token)

    if current_user.get("is_owner") is True:
        if await user_is_own_restaurant(current_user["id"], id):
            updated_restaurant = await db_manager.update_restaurant(id, payload)
            return updated_restaurant

    raise HTTPException(status_code=403, detail="Not authorized to access this resource")


@router.delete('/restaurant/{id}')
async def delete_restaurant(id: int, token: str):
    current_user = await get_current_user(token)

    if current_user.get("is_owner") is True:
        if await user_is_own_restaurant(current_user["id"], id):
            await db_manager.delete_restaurant(id)
            return {"detail": "Success delete"}

    raise HTTPException(status_code=403, detail="Not authorized to access this resource")


@router.get('/restaurant/{restaurant_id}/dish', response_model=List[DishOut])
async def get_restaurant_dishes(restaurant_id: int, token: str):
    current_user = await get_current_user(token)

    if current_user.get("is_owner") is True:
        if await user_is_own_restaurant(current_user["id"], restaurant_id):
            return await get_dishes_by_restaurant(restaurant_id)

    raise HTTPException(status_code=403, detail="Not authorized to access this resource")


@router.post('/restaurant/{restaurant_id}/dish', response_model=DishOut)
async def add_dish(restaurant_id: int, payload: DishIn, token: str):
    current_user = await get_current_user(token)

    if current_user.get("is_owner") is True:
        if await user_is_own_restaurant(current_user["id"], restaurant_id):
            dish_id = await db_manager.add_dish(restaurant_id, payload)
            dish = await db_manager.get_dish(dish_id)
            return dish

    raise HTTPException(status_code=403, detail="Not authorized to access this resource")


@router.put('/restaurant/{restaurant_id}/dish/{dish_id}', response_model=DishOut)
async def update_dish(restaurant_id: int, dish_id: int, token: str, payload: DishUpdate):
    current_user = await get_current_user(token)

    if current_user.get("is_owner") is True:
        if await user_is_own_restaurant(current_user["id"], restaurant_id):
            updated_restaurant = await db_manager.update_dish(dish_id, payload)
            return updated_restaurant

    raise HTTPException(status_code=403, detail="Not authorized to access this resource")


@router.delete('/restaurant/{restaurant_id}/dish/{dish_id}')
async def delete_dish(restaurant_id: int, dish_id: int, token: str):
    current_user = await get_current_user(token)

    if current_user.get("is_owner") is True:
        if await user_is_own_restaurant(current_user["id"], restaurant_id):
            await db_manager.delete_dish(dish_id)
            return {"detail": "Success delete"}

    raise HTTPException(status_code=403, detail="Not authorized to access this resource")
