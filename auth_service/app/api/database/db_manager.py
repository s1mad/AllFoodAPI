from sqlalchemy import select
from passlib.context import CryptContext
from app.api.database.database import users, database
from app.api.model.user import UserCreate, UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Хэширование пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Создание пользователя
async def create_user(user: UserCreate):
    hashed_password = hash_password(user.password)
    query = users.insert().values(
        phone_number=user.phone_number,
        password=hashed_password,
        is_owner=user.is_owner
    )
    await database.execute(query)


# Получение пользователя по номеру телефона
async def get_user_by_phone(phone_number: str):
    query = select(users).where(users.c.phone_number == phone_number)
    result = await database.fetch_one(query)
    return result


# Получение пользователя по ID
async def get_user_by_id(user_id: int):
    query = select(users).where(users.c.id == user_id)
    result = await database.fetch_one(query)
    return result
