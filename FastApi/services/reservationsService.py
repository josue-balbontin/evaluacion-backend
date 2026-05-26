from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional, Tuple
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException

from repositories.reservationsRepository import get_reservations_repository, reservationsRepository

TIME_SLOTS = [time(18, 0), time(19, 30), time(21, 0)]


class reservationsService:
    def __init__(self, repository: reservationsRepository):
        self.repository = repository

    def _get_window(self, window: str, tz: str) -> tuple[date, date]:
        try:
            zone = ZoneInfo(tz)
        except Exception as exc:
            raise HTTPException(status_code=400, detail='invalid timezone') from exc

        today = datetime.now(zone).date()
        if window == 'next7days':
            return today, today + timedelta(days=7)
        if window == 'weekend':
            days_until = (5 - today.weekday()) % 7
            saturday = today + timedelta(days=days_until)
            sunday = saturday + timedelta(days=1)
            return saturday, sunday
        if window == 'today':
            return today, today
        raise HTTPException(status_code=400, detail='invalid window')

    async def get_availability(
        self,
        date_value: date,
        time_value: Optional[time],
        party: int,
        table_type: Optional[UUID],
        tz: str,
        window: str,
    ) -> List[dict]:
        
        start_date, end_date = self._get_window(window, tz)
        if date_value < start_date or date_value > end_date:
            return []
            
        slots = [time_value] if time_value else TIME_SLOTS
        
        table_rows, reservation_rows = await self.repository.get_availability_data(date_value, slots, table_type)
        
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
    
    


def get_reservations_service(
    repository: reservationsRepository = Depends(get_reservations_repository),
) -> reservationsService:
    return reservationsService(repository)
