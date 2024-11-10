import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.database.database import database
from app.api.rabbit.rabbit import init_rabbit_producer
from app.api.router.order_router import order_router
from app.api.router.view_router import view_router

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    try:
        yield
    finally:
        await database.disconnect()


# Инициализация FastAPI приложения
app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/v1/user/openapi.json",
    docs_url="/api/v1/user/docs"
)

# Включаем маршруты
prefix = '/api/v1/user'
app.include_router(view_router, prefix=prefix, tags=['view'])
app.include_router(order_router, prefix=prefix, tags=['order'])

# Инициализация RabbitMQ producer для отправки сообщений в очереди
init_rabbit_producer()