

from typing import List

from fastapi import Depends

from db.postgress import get_db_connection_pool

from models.table_type import TableType


class tablesRespository:
    def __init__(self, conexion):
        self.conexion = conexion
    
    async def get_tables_type(self) -> List[TableType]:
        query = """
            SELECT id, restaurant_id, name, seats, description
            FROM content.table_type
            WHERE is_active = TRUE;
        """
        async with self.conexion.acquire() as connection:
            rows= await connection.fetch(query)
            return [TableType(**dict(row)) for row in rows]

def get_tables_repository(conexion = Depends(get_db_connection_pool)) -> tablesRespository:
    return tablesRespository(conexion)