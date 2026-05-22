from datetime import date, time
from typing import Dict, List, Optional, Tuple, Any
from uuid import UUID

from fastapi import Depends

from db.postgress import get_db_connection_pool
from repositories.abstract.repository import AbstractRepository

TIME_SLOTS = [time(18, 0), time(19, 30), time(21, 0)]


class reservationsRepository(AbstractRepository):

    def __init__(self, conexion):
        self.conexion = conexion

    async def get_by_id(self, id: Any) -> Any:
        pass
        
    async def list_all(self, limit: int, offset: int, **kwargs) -> List[Any]:
        return []

    async def get_availability(
        self,
        date_value: date,
        time_value: Optional[time],
        party: int,
        table_type: Optional[UUID],
    ) -> List[Dict]:
        slots = [time_value] if time_value else TIME_SLOTS

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

        reserved_map: Dict[Tuple[UUID, time], int] = {}
        for row in reservation_rows:
            reserved_map[(row['table_type_id'], row['reservation_time'])] = int(row['reserved'] or 0)

        results = []
        for row in table_rows:
            seats = int(row.get('seats') or 0)
            quantity = int(row.get('quantity') or 1)
            capacity = seats * quantity
            for slot in slots:
                reserved = reserved_map.get((row['id'], slot), 0)
                available = max(capacity - reserved, 0)
                if party > available:
                    available = 0
                results.append(
                    {
                        'time': slot.strftime('%H:%M'),
                        'table_type': row['id'],
                        'table_type_name': row.get('name') or 'Table',
                        'seats': capacity,
                        'available_seats': available,
                        'price_per_seat': row.get('price_per_seat'),
                    }
                )

        return results


def get_reservations_repository(
    conexion = Depends(get_db_connection_pool),
) -> AbstractRepository:
    return reservationsRepository(conexion)
