from datetime import date, time
from typing import Dict, List, Optional, Tuple, Any
from uuid import UUID

from fastapi import Depends

from db.postgress import get_db_connection_pool
from repositories.abstract.repository import AbstractRepository


class reservationsRepository(AbstractRepository):

    def __init__(self, conexion):
        self.conexion = conexion

    async def get_by_id(self, id: Any) -> Any:
        pass
        
    async def list_all(self, limit: int, offset: int, **kwargs) -> List[Any]:
        return []

    async def get_availability_data(
        self,
        date_value: date,
        slots: List[time],
        table_type: Optional[UUID],
    ) -> Tuple[List[dict], List[dict]]:

        table_query = """
            SELECT id, name, seats, quantity, price_per_seat
            FROM content.table_type
            WHERE is_active = TRUE
        """
        params = []
        if table_type:
            params.append(table_type)
            table_query += f" AND id = ${len(params)}"
        table_query += " ORDER BY name;"

        reservation_query = """
            SELECT table_type_id, reservation_time, SUM(party_size) AS reserved
            FROM content.reservation
            WHERE reservation_date = $1
              AND reservation_time = ANY($2)
            GROUP BY table_type_id, reservation_time;
        """

        async with self.conexion.acquire() as connection:
            table_rows = await connection.fetch(table_query, *params)
            reservation_rows = await connection.fetch(reservation_query, date_value, slots)

        return [dict(row) for row in table_rows], [dict(row) for row in reservation_rows]


def get_reservations_repository(
    conexion = Depends(get_db_connection_pool),
) -> AbstractRepository:
    return reservationsRepository(conexion)
