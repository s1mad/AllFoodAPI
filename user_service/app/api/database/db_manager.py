from sqlalchemy import select

from app.api.database.database import restaurants, database, dishes
from app.api.model.dish import Dish
from app.api.model.order_request import OrderRequest
from app.api.model.restaurant import Restaurant


# Получение списка всех ресторанов
async def get_all_restaurants():
    query = select(restaurants)
    result = await database.fetch_all(query)
    return [Restaurant(**row) for row in result]


# Получение списка блюд конкретного ресторана
async def get_dishes_by_restaurant(restaurant_id: int):
    query = select(dishes).where(dishes.c.restaurant_id == restaurant_id)
    result = await database.fetch_all(query)
    return [Dish(**row) for row in result]


# Обработка заказа
async def create_order(order: OrderRequest):
    # Здесь могла бы быть логика отправки заказа
    # Пока просто возвращаем сообщение об успехе
    return {"message": "Order successfully sent to restaurant"}
