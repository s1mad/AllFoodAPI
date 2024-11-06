from fastapi import FastAPI
from app.api.database.database import metadata, engine, database
from app.api.router.router import router

# Создаём таблицы при старте
metadata.create_all(engine)

# Инициализация FastAPI приложения
app = FastAPI(docs_url="/")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Включаем маршруты
app.include_router(router, prefix='/api/v1/auth', tags=['auth'])
