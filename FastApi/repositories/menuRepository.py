from datetime import date
from typing import List
from fastapi import Depends

from db.postgress import get_db_connection_pool
from db.redis import get_redis
from repositories.redis.redis import decorator_cache
from models.menu_item import MenuItem

class menuRepository:
    def __init__(self, conexion, redis):
        self.conexion = conexion
        self.redis = redis

    @decorator_cache('menu', 300)
    async def get_menu_items(self, target_date: date) -> List[MenuItem]:
        query = """
            SELECT id, restaurant_id, course, name, description, price, allergens,
                   is_available, available_from, available_until, created, modified
            FROM content.menu_item
            WHERE is_available = TRUE
              AND (available_from IS NULL OR available_from <= $1)
              AND (available_until IS NULL OR available_until >= $1)
            ORDER BY course, name;
        """
        async with self.conexion.acquire() as connection:

            rows = await connection.fetch(query, target_date)
            
            return [MenuItem(**dict(row)) for row in rows]


def get_menu_repository(
        conexion = Depends(get_db_connection_pool),
        redis = Depends(get_redis),
) -> menuRepository:
    return menuRepository(conexion, redis)