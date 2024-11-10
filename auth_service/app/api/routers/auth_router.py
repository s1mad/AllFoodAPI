from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from app.api.database.database import users, database
from app.api.database.db_manager import hash_password, get_user_by_id, verify_password
from app.api.model.user import UserCreate, UserResponse
from app.api.utils.jwt import create_access_token, verify_token

# Инициализация маршрутизатора
auth_router = APIRouter()


@auth_router.post(
    path='/register',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    """
    Регистрирует нового пользователя.
    """
    # Проверка на существующего пользователя с данным номером телефона
    query = select(users).where(user.phone_number == users.c.phone_number)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Номер телефона уже зарегистрирован")

    hashed_password = hash_password(user.password)
    query = users.insert().values(
        phone_number=user.phone_number,
        password_hash=hashed_password,
        is_owner=False  # Устанавливаем роль по умолчанию как не владелец
    )
    # Сохраняем пользователя в базу данных и возвращаем его ID
    user_id = await database.execute(query)
    return UserResponse(id=user_id, phone_number=user.phone_number, is_owner=False)


@auth_router.post(
    path='/login',
    status_code=status.HTTP_200_OK)
async def login_user(user: UserCreate):
    """
    Авторизует пользователя и возвращает JWT токен.
    """
    # Поиск пользователя в базе данных по номеру телефона
    query = select(users).where(user.phone_number == users.c.phone_number)
    db_user = await database.fetch_one(query)
    # Проверка пароля
    if db_user is None or not verify_password(user.password, db_user['password_hash']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Формируем данные для JWT токена с данными пользователя
    user_data = {
        "id": db_user['id'],
        "phone_number": db_user['phone_number'],
        "is_owner": db_user['is_owner']
    }

    access_token = create_access_token(data=user_data)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get(
    path="/user",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK)
async def get_user(token: str):
    """
    Получает данные пользователя на основе переданного JWT токена.
    """

    # Проверка валидности токена
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Получение данных пользователя из базы данных по ID
    user_from_db = await get_user_by_id(user_data['id'])
    if not user_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Возвращаем информацию о пользователе
    return UserResponse(
        id=user_from_db['id'],
        phone_number=user_from_db['phone_number'],
        is_owner=user_from_db['is_owner']
    )
