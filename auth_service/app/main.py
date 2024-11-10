import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.database.database import database
from app.api.routers.auth_router import auth_router

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.
    Выполняет подключение к базе данных при запуске приложения
    и разрывает соединение при его остановке.
    """
    await database.connect()
    try:
        yield
    finally:
        await database.disconnect()


# Инициализация FastAPI приложения с указанием кастомных URL для OpenAPI и документации Swagger
app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/v1/auth/openapi.json",
    docs_url="/api/v1/auth/docs"
)

# Включаем маршруты
app.include_router(auth_router, prefix='/api/v1/auth', tags=['auth'])
