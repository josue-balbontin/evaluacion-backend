from datetime import date, datetime, time, timedelta
from typing import List, Optional
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException

from repositories.reservationsRepository import get_reservations_repository, reservationsRepository


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
        return await self.repository.get_availability(date_value, time_value, party, table_type)


def get_reservations_service(
    repository: reservationsRepository = Depends(get_reservations_repository),
) -> reservationsService:
    return reservationsService(repository)
