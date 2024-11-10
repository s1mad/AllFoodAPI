import logging
from sqlalchemy import select
from passlib.context import CryptContext
from app.api.database.database import users, database
from app.api.model.user import UserCreate

# Инициализация CryptContext для хэширования паролей с использованием алгоритма bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Логгер для записи сообщений о выполнении операций
logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    """
    Хэширует переданный пароль с использованием алгоритма bcrypt.
    """
    hashed_password = pwd_context.hash(password)
    logger.debug(
        f"Password hashed successfully: {password[:4]}...")  # Логирование успешного хэширования (первые 4 символа пароля)
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, совпадает ли переданный пароль с хэшированным значением.
    """
    result = pwd_context.verify(plain_password, hashed_password)
    if result:
        logger.debug("Password verification successful.")
    else:
        logger.warning("Password verification failed.")
    return result


async def create_user(user: UserCreate):
    """
    Создаёт нового пользователя в базе данных.
    """
    logger.info(f"Creating new user with phone number: {user.phone_number}")

    # Хэширование пароля
    hashed_password = hash_password(user.password)

    # Запрос для вставки нового пользователя в базу данных
    query = users.insert().values(
        phone_number=user.phone_number,
        password=hashed_password,
        is_owner=user.is_owner
    )

    # Выполнение запроса и добавление пользователя в базу
    await database.execute(query)
    logger.info(f"User with phone number {user.phone_number} created successfully.")


async def get_user_by_phone(phone_number: str):
    """
    Получает пользователя по номеру телефона.
    """
    logger.info(f"Fetching user with phone number: {phone_number}")

    # Запрос для поиска пользователя по номеру телефона
    query = select(users).where(phone_number == users.c.phone_number)
    result = await database.fetch_one(query)

    if result:
        logger.debug(f"User with phone number {phone_number} found.")
    else:
        logger.warning(f"User with phone number {phone_number} not found.")

    return result


async def get_user_by_id(user_id: int):
    """
    Получает пользователя по его ID.
    """
    logger.info(f"Fetching user with ID: {user_id}")

    # Запрос для поиска пользователя по ID
    query = select(users).where(user_id == users.c.id)
    result = await database.fetch_one(query)

    if result:
        logger.debug(f"User with ID {user_id} found.")
    else:
        logger.warning(f"User with ID {user_id} not found.")

    return result
