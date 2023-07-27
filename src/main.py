from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.core.config import get_settings
from src.db.database import Base

from src.db.database import engine
import uvicorn

from src.api.v1 import base

app_settings = get_settings()

app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=app_settings.app_title,  # название приложение берём из настроек
    # Адрес документации в красивом интерфейсе
    docs_url='/api/openapi',
    # Адрес документации в формате OpenAPI
    openapi_url='/api/openapi.json',
    # Можно сразу сделать небольшую оптимизацию сервиса
    # и заменить стандартный JSON-сериализатор на более шуструю версию, написанную на Rust
    default_response_class=ORJSONResponse)

app.include_router(base.router, prefix='/api/v1')


@app.on_event("startup")
async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    pass


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
    )
