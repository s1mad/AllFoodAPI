from pydantic import BaseModel
from typing import Optional


# Модель для создания нового блюда.
class DishIn(BaseModel):
    name: str
    price: float
    ingredients: str


# Модель для вывода информации о блюде.
class DishOut(DishIn):
    id: int


# Модель для обновления данных о блюде.
class DishUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    ingredients: Optional[str] = None
