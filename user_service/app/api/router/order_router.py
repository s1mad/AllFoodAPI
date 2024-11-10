from fastapi import HTTPException, APIRouter, status

from app.api.model.order_request import OrderRequest
from app.api.rabbit.rabbit import rabbit_producer

# Создаем роутер для маршрутов
order_router = APIRouter()


@order_router.post(
    path='/order',
    response_model=dict,
    status_code=status.HTTP_201_CREATED)
async def create_order(token: str, order: OrderRequest):
    """
     Создание заказа и отправка его в ресторан.
    """
    try:
        # Логика отправки заказа в очередь RabbitMQ
        message = order.dict()
        rabbit_producer.send_message(message)
        return {"message": "Order successfully sent to restaurant"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order data.")
