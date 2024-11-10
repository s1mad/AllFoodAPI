from typing import List
from fastapi import APIRouter, HTTPException, status
from app.api.rabbit.rabbitmq_order_consumer import orders, OrderRequest
from app.api.utils.get_current_user import get_current_user
from app.api.database.db_manager import user_is_own_restaurant

# Инициализация маршрутизатора для получения заказов
order_router = APIRouter()


@order_router.get(path='/orders/{restaurant_id}',
                  response_model=List[OrderRequest],
                  status_code=status.HTTP_200_OK)
async def get_orders(token: str, restaurant_id: int):
    """
    Получает список заказов для ресторана текущего пользователя.
    """
    current_user = await get_current_user(token)
    if current_user.get("is_owner") and await user_is_own_restaurant(current_user["id"], restaurant_id):
        filtered_orders = [
            OrderRequest(**order) for order in orders if order['restaurant_id'] == restaurant_id
        ]
        return filtered_orders
    raise HTTPException(status_code=403, detail="Доступ запрещен")
