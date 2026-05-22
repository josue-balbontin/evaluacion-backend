import asyncpg
from core import config

db_pool = None

async def get_db_pool() -> asyncpg.Pool:
    """
    Crea y devuelve un Pool de conexiones asíncronas a PostgreSQL.
    El pool evita tener que abrir y cerrar la conexión en cada consulta.
    """
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(config.POSTGRES_URL)
    return db_pool

async def close_db_pool():
    """
    Cierra el pool de conexiones limpiamente cuando la API se apaga.
    """
    global db_pool
    if db_pool is not None:
        await db_pool.close()