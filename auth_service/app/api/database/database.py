import os

from databases import Database
from sqlalchemy import Column, Integer, String, Table, MetaData, Boolean, create_engine, ForeignKey, Float

# Получаем строку подключения к базе данных из переменных окружения
DATABASE_URL = os.getenv('DATABASE_URL')

# Создаём движок для подключения к базе данных
# connect_args={"check_same_thread": False} используется для того, чтобы избежать ошибки с многопоточностью в SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

# Таблица пользователей
users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('phone_number', String(20), unique=True, nullable=False),
    Column('password_hash', String(128), nullable=False),
    Column('is_owner', Boolean, default=False),
)

# Таблица для ресторанов
restaurants = Table(
    'restaurants',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(64)),
    Column('address', String(256)),
    Column('user_id', Integer, ForeignKey('users.id'))  # Связываем с таблицей владельцев
)

# Таблица для блюд
dishes = Table(
    'dishes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(64)),
    Column('ingredients', String(256)),
    Column('price', Float),
    Column('restaurant_id', Integer, ForeignKey('restaurants.id'))  # Связываем с рестораном
)

# Создание асинхронного подключения к базе данных
database = Database(DATABASE_URL)

# Создание таблиц в базе данных (если они ещё не созданы)
metadata.create_all(engine)
