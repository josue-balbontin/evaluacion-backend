from datetime import date, datetime
from typing import List, Optional, Any
from uuid import UUID

from fastapi import Depends

from db.postgress import get_db_connection_pool
from db.redis import get_redis
from repositories.redis.redis import decorator_cache, RedisCache
from repositories.abstract.repository import AbstractRepository
from repositories.abstract.search import AbstractSearch
from repositories.redis.cache import AbstractCache

from models.menu_item import MenuItem
from models.restaurant import Restaurant
from models.table_type import TableType


class restaurantRepository(AbstractRepository, AbstractSearch):
    def __init__(self, conexion, cache: AbstractCache):
        self.conexion = conexion
        self.cache = cache

    @decorator_cache('restaurants_list', 300)
    async def list_all(
        self,
        limit: int,
        offset: int,
        name: Optional[str] = None,
        address: Optional[str] = None,
        **kwargs
    ) -> List[Restaurant]:
        conditions = ["is_active = TRUE"]
        params = []

        if name:
            params.append(f"%{name}%")
            conditions.append(f"name ILIKE ${len(params)}")

        if address:
            params.append(f"%{address}%")
            conditions.append(f"address ILIKE ${len(params)}")

        params.append(limit)
        limit_idx = len(params)
        params.append(offset)
        offset_idx = len(params)

        where_sql = " AND ".join(conditions)
        query = f"""
            SELECT id, name, slug, description, address, phone,
                   opening_time, closing_time, timezone
            FROM content.restaurant
            WHERE {where_sql}
            ORDER BY name
            LIMIT ${limit_idx} OFFSET ${offset_idx};
        """

        async with self.conexion.acquire() as connection:
            rows = await connection.fetch(query, *params)
            return [Restaurant(**dict(row)) for row in rows]
            
    async def list_restaurants(self, limit: int, offset: int, name: Optional[str] = None, address: Optional[str] = None) -> List[Restaurant]:
        return await self.list_all(limit, offset, name=name, address=address)

    async def search(
        self,
        query_text: str,
        limit: int,
        offset: int,
    ) -> List[Restaurant]:
        search_param = f"%{query_text}%"
        query = """
            SELECT id, name, slug, description, address, phone,
                   opening_time, closing_time, timezone
            FROM content.restaurant
            WHERE is_active = TRUE
              AND (
                name ILIKE $1
                OR address ILIKE $1
                OR description ILIKE $1
                OR slug ILIKE $1
                OR phone ILIKE $1
              )
            ORDER BY name
            LIMIT $2 OFFSET $3;
        """

        async with self.conexion.acquire() as connection:
            rows = await connection.fetch(query, search_param, limit, offset)
            return [Restaurant(**dict(row)) for row in rows]
            
    async def search_restaurants(self, query_text: str, limit: int, offset: int) -> List[Restaurant]:
        return await self.search(query_text, limit, offset)

    @decorator_cache('restaurants_detail', 300)
    async def get_by_id(self, restaurant_id: Any) -> Optional[tuple]:
        restaurant_query = """
            SELECT id, name, slug, description, address, phone,
                   opening_time, closing_time, timezone
            FROM content.restaurant
            WHERE id = $1 AND is_active = TRUE;
        """

        async with self.conexion.acquire() as connection:
            restaurant_row = await connection.fetchrow(restaurant_query, restaurant_id)
            if not restaurant_row:
                return None

            table_query = """
                SELECT id, restaurant_id, name, description, seats,
                       quantity, price_per_seat, is_active, created, modified
                FROM content.table_type
                WHERE restaurant_id = $1 AND is_active = TRUE
                ORDER BY name;
            """
            menu_query = """
                SELECT id, restaurant_id, course, name, description, price, allergens,
                       is_available, available_from, available_until, created, modified
                FROM content.menu_item
                WHERE restaurant_id = $1 AND is_available = TRUE
                ORDER BY course, name;
            """

            table_rows = await connection.fetch(table_query, restaurant_id)
            menu_rows = await connection.fetch(menu_query, restaurant_id)

        restaurant = Restaurant(**dict(restaurant_row))
        table_types = [TableType(**dict(row)) for row in table_rows]
        menu_items = [MenuItem(**dict(row)) for row in menu_rows]

        return restaurant, table_types, menu_items
        
    async def get_restaurant_detail(self, restaurant_id: UUID):
        return await self.get_by_id(restaurant_id)
    
    @decorator_cache('popular_restaurants', 300)
    async def get_popular_restaurants(self, start_date : date , end_date : date , timezone: str):

        query = """
            SELECT r.id, r.name, r.slug, r.description, r.address, r.phone,
                   r.opening_time, r.closing_time, r.timezone,
                   COUNT(status.id) as reservas_count
            FROM content.restaurant as r
            LEFT JOIN content.reservation as res 
                   ON r.id = res.restaurant_id 
                  AND res.reservation_date >= $1 
                  AND res.reservation_date <= $2
            LEFT JOIN content.reservation_status as status 
                   ON res.status_id = status.id
                  AND (status.name ILIKE '%confirm%' OR status.name ILIKE '%Confirmada%')
            GROUP BY r.id
            ORDER BY reservas_count DESC
        """

        async with self.conexion.acquire() as connection:
            rows = await connection.fetch(query, start_date, end_date)
            return [(dict(row)) for row in rows]
        
        



def get_restaurant_repository(
    conexion = Depends(get_db_connection_pool),
    redis_client = Depends(get_redis),
) -> AbstractRepository:
    return restaurantRepository(conexion, RedisCache(redis_client))
