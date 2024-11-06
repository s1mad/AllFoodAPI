from pydantic import BaseModel
from typing import Optional


# Модель для создания нового ресторана
class RestaurantIn(BaseModel):
    name: str
    address: str


# Модель для вывода информации о ресторане с ID
class RestaurantOut(RestaurantIn):
    id: int


# Модель для обновления информации о ресторане
class RestaurantUpdate(RestaurantIn):
    name: Optional[str] = None
    address: Optional[str] = None
