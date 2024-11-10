from typing import List

from pydantic import BaseModel


# Класс модели для проверки формата OrderRequest
class OrderRequest(BaseModel):
    dishes: List[dict]
    address: str
    phone_number: str
    restaurant_id: int
