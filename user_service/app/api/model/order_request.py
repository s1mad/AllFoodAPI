from pydantic import BaseModel
from typing import List


# Модель для запроса на создание заказа
class OrderRequest(BaseModel):
    dishes: List[dict]  # [{"id": int, "quantity": int}]
    address: str
    phone_number: str
    restaurant_id: int
