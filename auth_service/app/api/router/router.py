from datetime import datetime, timedelta
from typing import List

import bcrypt
import jwt
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from app.api.database.database import users, database
from app.api.model.user import UserCreate, UserResponse

router = APIRouter()

# Секрет для JWT токенов
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Хэширование пароля
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# Создание JWT токена
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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
        is_owner=user.is_owner
    )
    await database.execute(query)
    return UserResponse(id=1, phone_number=user.phone_number, is_owner=user.is_owner)


# Авторизация пользователя и получение JWT токена
@router.post('/login')
async def login_user(user: UserCreate):
    query = select(users).where(users.c.phone_number == user.phone_number)
    db_user = await database.fetch_one(query)
    if db_user is None or not bcrypt.checkpw(user.password.encode('utf-8'), db_user['password_hash'].encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.phone_number})
    return {"access_token": access_token, "token_type": "bearer"}


# Получение всех пользователей
@router.get('/users', response_model=List[UserResponse])
async def get_all_users():
    query = select(users)
    result = await database.fetch_all(query)
    return [UserResponse(**row) for row in result]
