
from typing import List

from fastapi import Depends

from db.postgress import get_db_connection_pool
from db.redis import get_redis
from repositories.redis import decorator_cache

from models.table_type import TableType


class tablesRespository:
    def __init__(self, conexion, redis):
        self.conexion = conexion
        self.redis = redis

    @decorator_cache("tables_type" ,  3600)
    async def get_tables_type(self) -> List[TableType]:
        query = """
            SELECT id, restaurant_id, name, seats, description
            FROM content.table_type
            WHERE is_active = TRUE;
        """
        async with self.conexion.acquire() as connection:
            rows= await connection.fetch(query)
            return [TableType(**dict(row)) for row in rows]

def get_tables_repository(
        conexion = Depends(get_db_connection_pool),
        redis = Depends(get_redis)
        ) -> tablesRespository:
    return tablesRespository(conexion, redis)