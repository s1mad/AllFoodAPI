from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.database.database import database
from app.api.router.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    try:
        yield
    finally:
        await database.disconnect()


# Инициализация FastAPI приложения
app = FastAPI(lifespan=lifespan, openapi_url="/api/v1/owner/openapi.json", docs_url="/api/v1/owner/docs")

# Включаем маршруты
app.include_router(router, prefix='/api/v1/owner', tags=['owner'])

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
