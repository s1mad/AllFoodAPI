from fastapi import APIRouter, HTTPException, status
import bcrypt
from typing import List

from app.api.database.db_manager import hash_password
from app.api.utils.jwt import create_access_token, verify_token
from app.api.database.database import users, database
from app.api.model.user import UserCreate, UserResponse
from sqlalchemy.future import select
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    id: str  # Используем строку для id
    phone_number: str  # Заменяем на phone_number
    is_owner: bool




# Регистрация нового пользователя
@router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate):
    query = select(users).where(users.c.phone_number == user.phone_number)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")

    hashed_password = hash_password(user.password)
    query = users.insert().values(
        phone_number=user.phone_number,
        password_hash=hashed_password,
        is_owner=False  # Setting is_owner to False by default
    )
    user_id = await database.execute(query)
    return UserResponse(id=user_id, phone_number=user.phone_number, is_owner=False)


# Авторизация пользователя и получение JWT токена
@router.post('/login')
async def login_user(user: UserCreate):
    query = select(users).where(users.c.phone_number == user.phone_number)
    db_user = await database.fetch_one(query)
    if db_user is None or not bcrypt.checkpw(user.password.encode('utf-8'), db_user['password_hash'].encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Создание JWT токена
    user_data = {
        "sub": db_user['phone_number'],  # Можно использовать поле phone_number как уникальный идентификатор
        "username": db_user['phone_number'],  # Можно заменить на db_user['username'], если оно есть
        "is_owner": db_user['is_owner']
    }

    access_token = create_access_token(data=user_data)
    return {"access_token": access_token, "token_type": "bearer"}


# Получение всех пользователей
@router.get('/users', response_model=List[UserResponse])
async def get_all_users():
    query = select(users)
    result = await database.fetch_all(query)
    return [UserResponse(**row) for row in result]


# Эндпоинт для получения пользователя по токену
@router.get("/user", response_model=User)
async def get_user(token: str):
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Получаем id и phone_number из токена
    user_id = user_data['sub']  # ID будет в sub, который теперь можно использовать как phone_number
    phone_number = user_data['sub']  # Если sub — это телефон, используем его как phone_number

    return User(id=user_id, phone_number=phone_number, is_owner=user_data['is_owner'])

