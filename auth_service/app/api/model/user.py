from pydantic import BaseModel


# Модель для создания нового пользователя
class UserCreate(BaseModel):
    phone_number: str
    password: str


# Модель для вывода информации о пользователе
class UserResponse(BaseModel):
    id: int
    phone_number: str
    is_owner: bool

    class Config:
        from_attributes = True
