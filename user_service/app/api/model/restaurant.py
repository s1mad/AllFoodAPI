from pydantic import BaseModel


# Модель для информации о ресторане
class Restaurant(BaseModel):
    id: int
    name: str
    address: str
