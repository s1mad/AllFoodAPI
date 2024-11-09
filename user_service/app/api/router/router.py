import logging
from typing import List

from fastapi import HTTPException, APIRouter

from app.api.database.db_manager import get_all_restaurants, get_dishes_by_restaurant
from app.api.model.dish import Dish
from app.api.model.order_request import OrderRequest
from app.api.model.restaurant import Restaurant
from app.api.rabbit.rabbit import rabbit_producer

router = APIRouter()
log = logging.getLogger(__name__)

@router.get('/restaurants', response_model=List[Restaurant])
async def get_restaurants():
    _restaurants = await get_all_restaurants()
    log.info("get_restaurants successfully.")
    return _restaurants


@router.get('/restaurants/{restaurant_id}/dishes', response_model=List[Dish])
async def get_dishes_by_restaurant_id(restaurant_id: int):
    dishes = await get_dishes_by_restaurant(restaurant_id)
    log.info("get_dishes_by_restaurant_id successfully.")
    return dishes


@router.post('/order', response_model=dict)
async def create_order(token: str, order: OrderRequest):
    try:
        # Логика отправки заказа в очередь RabbitMQ
        message = order.dict()
        rabbit_producer.send_message(message)
        log.info("Order successfully sent to RabbitMQ.")
        return {"message": "Order successfully sent to restaurant"}
    except Exception as e:
        log.error(f"Failed to send order to RabbitMQ: {e}")
        raise HTTPException(status_code=500, detail="Error sending order")