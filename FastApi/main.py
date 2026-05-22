from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1 import menu, reservations, restaurants, tables
from db.postgress import close_db_connection_pool, get_db_connection_pool
from core import config
from redis.asyncio import Redis
from contextlib import asynccontextmanager

import uvicorn
import logging
from core.logger import LOGGING

from db import redis


from api.v1 import healthz


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto se ejecuta al ENCENDER la API
    print("Iniciando conexión a PostgreSQL...")
    await get_db_connection_pool()
    yield
    # Esto se ejecuta al APAGAR la API
    print("Cerrando conexión a PostgreSQL...")
    await close_db_connection_pool()

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

if __name__ == '__main__':
    # The application can be launched with the command
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # but in order not to lose the ability to use the debugger,
    # we'll run the uvicorn server through python
    uvicorn.run(
    'main:app',
            host='0.0.0.0',
            port=8000,
            log_config=LOGGING,
            log_level=logging.DEBUG,
    )



@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
                                           

@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()



app.include_router(healthz.router, prefix='/api/v1', tags=['healthz'])

app.include_router(tables.router, prefix='/api/v1', tags=['tables'])

app.include_router(menu.router, prefix='/api/v1', tags=['menu'])

app.include_router(restaurants.router, prefix='/api/v1', tags=['restaurants'])

app.include_router(reservations.router, prefix='/api/v1', tags=['reservations'])