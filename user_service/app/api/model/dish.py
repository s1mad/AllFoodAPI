from pydantic import BaseModel


# Модель для информации о блюде
class Dish(BaseModel):
    id: int
    name: str
    price: float
    ingredients: str
