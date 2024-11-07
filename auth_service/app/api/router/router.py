from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from app.api.database.database import users, database
from app.api.database.db_manager import hash_password, get_user_by_id, verify_password
from app.api.model.user import UserCreate, UserResponse
from app.api.utils.jwt import create_access_token, verify_token

router = APIRouter()


# Регистрация нового пользователя
@router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate):
    query = select(users).where(user.phone_number == users.c.phone_number)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")

    hashed_password = hash_password(user.password)
    query = users.insert().values(
        phone_number=user.phone_number,
        password_hash=hashed_password,
        is_owner=False
    )
    user_id = await database.execute(query)
    return UserResponse(id=user_id, phone_number=user.phone_number, is_owner=False)


# Авторизация пользователя и получение JWT токена
@router.post('/login')
async def login_user(user: UserCreate):
    query = select(users).where(user.phone_number == users.c.phone_number)
    db_user = await database.fetch_one(query)
    if db_user is None or not verify_password(user.password, db_user['password_hash']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Создание JWT токена с id пользователя
    user_data = {
        "id": db_user['id'],
        "phone_number": db_user['phone_number'],
        "is_owner": db_user['is_owner']
    }

    access_token = create_access_token(data=user_data)
    return {"access_token": access_token, "token_type": "bearer"}


# Эндпоинт для получения пользователя по токену
@router.get("/user", response_model=UserResponse)
async def get_user(token: str):
    # Проверка токена
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Получение данных пользователя по ID из базы данных
    user_from_db = await get_user_by_id(user_data['id'])
    if not user_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Возвращаем модель UserResponse с данными из базы
    return UserResponse(
        id=user_from_db['id'],
        phone_number=user_from_db['phone_number'],
        is_owner=user_from_db['is_owner']
    )
