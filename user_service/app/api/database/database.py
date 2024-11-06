import os
from databases import Database
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, Float

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

# Таблица ресторанов
restaurants = Table(
    'restaurants',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(64)),
    Column('address', String(256)),
)

# Таблица блюд
dishes = Table(
    'dishes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(64)),
    Column('price', Float),
    Column('ingredients', String(256)),
    Column('category', String(64)),
    Column('restaurant_id', Integer),
)

# Создаём асинхронное подключение
database = Database(DATABASE_URL)
