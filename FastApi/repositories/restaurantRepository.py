from typing import List, Optional
from uuid import UUID

from fastapi import Depends

from db.postgress import get_db_connection_pool
from db.redis import get_redis
from repositories.redis import decorator_cache
from models.menu_item import MenuItem
from models.restaurant import Restaurant
from models.table_type import TableType


class restaurantRepository:
    def __init__(self, conexion, redis):
        self.conexion = conexion
        self.redis = redis

    @decorator_cache('restaurants_list', 300)
    async def list_restaurants(
        self,
        limit: int,
        offset: int,
        name: Optional[str] = None,
        address: Optional[str] = None,
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

    async def search_restaurants(
        self,
        query_text: str,
        limit: int,
        offset: int,
    ) -> List[Restaurant]:
        search = f"%{query_text}%"
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
            rows = await connection.fetch(query, search, limit, offset)
            return [Restaurant(**dict(row)) for row in rows]

    @decorator_cache('restaurants_detail', 300)
    async def get_restaurant_detail(self, restaurant_id: UUID):
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


def get_restaurant_repository(
    conexion = Depends(get_db_connection_pool),
    redis = Depends(get_redis),
) -> restaurantRepository:
    return restaurantRepository(conexion, redis)
