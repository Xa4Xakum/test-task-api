from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from loguru import logger

from database.engine import create_tables, engine
from utils.misc import setup_logger
from routes import building, organization, activity
from middlewares.auth import verify_api_key
from middlewares.exception_catch import exception_middleware
from config.init import conf


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    logger.info('Логгеры установлены')

    await create_tables(engine)
    logger.info('Движок бд создан')

    logger.info('API online')
    yield

    await engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    version='0.1.0',
    title='Тестовое задание',
    summary='Документация к API по тестовому заданию',
    description=(
        'Здесь представлен результат выполнения тестового задания на '
        '[вакансию python-разработчик](https://hh.ru/vacancy/126642474).\n\n'
        'Пишите в [телеграм](https://t.me/Xa4_Xakum), если вам нравится мой результат.\n\n'
        '## Аутентификация\n\n'
        f'Для использования API необходимо передавать статический API ключ в заголовке `X-Auth-Key`.\n\n'
        f'**Ваш API ключ:** `{conf.secret_key}`\n\n'
        'Пример заголовка:\n'
        '```\n'
        f'X-Auth-Key: {conf.secret_key}\n'
        '```'
    ),
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "tryItOutEnabled": True,
    },
)

app.middleware('http')(exception_middleware)

app.include_router(activity.r, prefix='/activity', tags=['activity'], dependencies=[Depends(verify_api_key)])
app.include_router(organization.r, prefix='/organization', tags=['organization'], dependencies=[Depends(verify_api_key)])
app.include_router(building.r, prefix='/building', tags=['building'], dependencies=[Depends(verify_api_key)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "API online", "status": "ok"}
