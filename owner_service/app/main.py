import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.database.database import database
from app.api.rabbit.rabbitmq_order_consumer import start_rabbitmq_order_consumer
from app.api.routers.dish_router import dish_router
from app.api.routers.order_router import order_router
from app.api.routers.restaurant_router import restaurant_router

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
    openapi_url="/api/v1/owner/openapi.json",
    docs_url="/api/v1/owner/docs"
)

# Включаем маршруты
prefix = '/api/v1/owner'
app.include_router(restaurant_router, prefix=prefix, tags=['restaurant'])
app.include_router(dish_router, prefix=prefix, tags=['dish'])
app.include_router(order_router, prefix=prefix, tags=['order'])

# Запуск RabbitMQ потребителя для обработки входящих сообщений из очереди
start_rabbitmq_order_consumer()
