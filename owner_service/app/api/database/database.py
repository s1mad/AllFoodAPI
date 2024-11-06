import os

from databases import Database
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

restaurants = Table(
    'restaurants',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(64)),
    Column('address', String(256)),
)

# Создаём асинхронное подключение
database = Database(DATABASE_URL)
