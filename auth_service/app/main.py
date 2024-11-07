from fastapi import FastAPI

from app.api.database.database import database
from app.api.router.router import router

# Инициализация FastAPI приложения
app = FastAPI(openapi_url="/api/v1/auth/openapi.json", docs_url="/api/v1/auth/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Включаем маршруты
app.include_router(router, prefix='/api/v1/auth', tags=['auth'])
