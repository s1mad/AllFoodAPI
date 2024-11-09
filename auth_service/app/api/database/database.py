import os

from databases import Database
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Table, MetaData, Boolean, create_engine

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

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

# Создаём асинхронное подключение
database = Database(DATABASE_URL)
metadata.create_all(engine)
