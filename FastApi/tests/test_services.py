import pytest
from datetime import date, time, timedelta
from uuid import uuid4
from fastapi import HTTPException
from zoneinfo import ZoneInfo

from services.reservationsService import reservationsService

class DummyReservationsRepo:
    async def get_availability(self, date_value, time_value, party, table_type):
        return [{"time": "18:00", "available_seats": 10}]
        
    async def get_by_id(self, id):
        pass

    async def list_all(self, limit, offset, **kwargs):
        pass


@pytest.fixture
def res_service():
    repo = DummyReservationsRepo()
    return reservationsService(repository=repo)


def test_get_window_next7days(res_service):
    start_date, end_date = res_service._get_window('next7days', 'UTC')
    assert (end_date - start_date).days == 7


def test_get_window_today(res_service):

    start_date, end_date = res_service._get_window('today', 'UTC')
    assert start_date == end_date


def test_get_window_invalid_tz(res_service):

    with pytest.raises(HTTPException) as exc:
        res_service._get_window('today', 'INVALID/TZ')
    assert exc.value.status_code == 400
    assert exc.value.detail == 'invalid timezone'


def test_get_window_invalid_window(res_service):

    with pytest.raises(HTTPException) as exc:
        res_service._get_window('invalid_window_string', 'UTC')
    assert exc.value.status_code == 400
    assert exc.value.detail == 'invalid window'


@pytest.mark.asyncio
async def test_get_availability_out_of_window(res_service):
 
    past_date = date(2000, 1, 1)
    results = await res_service.get_availability(
        date_value=past_date,
        time_value=None,
        party=2,
        table_type=None,
        tz='UTC',
        window='next7days'
    )
    assert results == []

@pytest.mark.asyncio
async def test_get_availability_in_window(res_service):

    # Assuming today is within 'next7days'
    today, _ = res_service._get_window('next7days', 'UTC')
    results = await res_service.get_availability(
        date_value=today,
        time_value=None,
        party=2,
        table_type=None,
        tz='UTC',
        window='next7days'
    )
    assert len(results) == 1
    assert results[0]['available_seats'] == 10
