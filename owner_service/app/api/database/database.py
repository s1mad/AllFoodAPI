import os

from databases import Database
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, ForeignKey, Float, Boolean
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

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
    Column('description', String(256)),
    Column('price', Float),
    Column('restaurant_id', Integer, ForeignKey('restaurants.id'))  # Связываем с рестораном
)

# Создаём асинхронное подключение
database = Database(DATABASE_URL)
