from fastapi import FastAPI

from app.api.database.database import database
from app.api.router.router import router

app = FastAPI(openapi_url="/api/v1/owner/openapi.json", docs_url="/api/v1/owner/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router, prefix='/api/v1/owner', tags=['owner'])
