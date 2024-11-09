import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.database.database import database
from app.api.rabbit.config import config
from app.api.rabbit.rabbit import init_rabbit_producer, rabbit_producer
from app.api.router.router import router

# Настройка логирования
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    try:
        yield
    finally:
        await database.disconnect()


# Функция для запуска слушателя RabbitMQ
def run_rabbit_listener():
    init_rabbit_producer(
        host=config.RABBIT_HOST,
        order_queue=config.ORDER_QUEUE,
        username=config.RABBIT_USER,
        password=config.RABBIT_PASSWORD
    )
    rabbit_producer.start_listening()


# Инициализация FastAPI приложения
app = FastAPI(lifespan=lifespan, openapi_url="/api/v1/user/openapi.json", docs_url="/api/v1/user/docs")

# Включаем маршруты
app.include_router(router, prefix='/api/v1/user', tags=['user'])

if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor, run_rabbit_listener)
        uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
