from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.api.database import db_manager
from app.api.model.dish import DishOut, DishIn, DishUpdate
from app.api.model.restaurant import RestaurantOut, RestaurantIn, RestaurantUpdate
from app.api.model.user import TokenRequest, get_current_user

router = APIRouter()

@router.get('/restaurants', response_model=List[RestaurantOut])
async def index(token: str):
    current_user = await get_current_user(token)
    restaurants = await db_manager.get_restaurants_by_user(current_user.id)
    return restaurants


@router.post('/restaurants', status_code=201, response_model=RestaurantOut)
async def add_restaurant(payload: RestaurantIn, token_request: TokenRequest):
    current_user = await get_current_user(token_request.token)
    restaurant_id = await db_manager.add_restaurant(payload, owner_id=current_user.id)
    return {**payload.dict(), 'id': restaurant_id, 'owner_id': current_user.id}


@router.put('/restaurant/{id}', response_model=RestaurantOut)
async def update_restaurant(id: int, payload: RestaurantUpdate, token_request: TokenRequest):
    current_user = await get_current_user(token_request.token)
    restaurant = await db_manager.get_restaurant(id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant with given id not found")
    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this restaurant")
    updated_restaurant = await db_manager.update_restaurant(id, payload)
    return updated_restaurant


@router.delete('/restaurants/{id}', response_model=RestaurantOut)
async def delete_restaurant(id: int, token_request: TokenRequest):
    current_user = await get_current_user(token_request.token)
    restaurant = await db_manager.get_restaurant(id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant with given id not found")
    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this restaurant")
    await db_manager.delete_restaurant(id)
    return restaurant


@router.post('/restaurants/{restaurant_id}/dishes', response_model=DishOut)
async def add_dish(restaurant_id: int, payload: DishIn, token_request: TokenRequest):
    current_user = await get_current_user(token_request.token)
    restaurant = await db_manager.get_restaurant(restaurant_id)
    if not restaurant or restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add dish to this restaurant")
    dish_id = await db_manager.add_dish(payload, restaurant_id)
    return DishOut(**payload.dict(), id=dish_id, restaurant_id=restaurant_id)


@router.put('/dishes/{id}', response_model=DishOut)
async def update_dish(id: int, payload: DishUpdate, token_request: TokenRequest):
    current_user = await get_current_user(token_request.token)
    dish = await db_manager.get_dish(id)
    restaurant = await db_manager.get_restaurant(dish.restaurant_id)
    if not restaurant or restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this dish")
    return await db_manager.update_dish(id, payload)


@router.delete('/dishes/{id}', response_model=DishOut)
async def delete_dish(id: int, token_request: TokenRequest):
    current_user = await get_current_user(token_request.token)
    dish = await db_manager.get_dish(id)
    restaurant = await db_manager.get_restaurant(dish.restaurant_id)
    if not restaurant or restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this dish")
    await db_manager.delete_dish(id)
    return dish
