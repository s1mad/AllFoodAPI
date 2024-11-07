from pydantic import BaseModel
from typing import Optional


class DishIn(BaseModel):
    name: str
    description: str
    price: float


class DishOut(DishIn):
    id: int


class DishUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
