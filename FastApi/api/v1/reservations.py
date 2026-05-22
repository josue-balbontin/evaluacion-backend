from datetime import date, time
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from schemas.Availability import Availability
from services.reservationsService import get_reservations_service, reservationsService
from fastapi_core.limiter import limiter
from fastapi_core.config import RATE_LIMIT

router = APIRouter()

root = 'reservations'


@router.get(f'/{root}/availability/', response_model=list[Availability])
@limiter.limit(RATE_LIMIT)
async def get_availability(
    request: Request,
    date_value: date = Query(..., alias='date'),
    time_value: Optional[time] = Query(None, alias='time'),
    party: int = Query(..., ge=1),
    table_type: Optional[UUID] = Query(None, alias='table_type'),
    tz: str = Query('UTC'),
    window: str = Query('next7days'),
    service: reservationsService = Depends(get_reservations_service),
):
    return await service.get_availability(
        date_value=date_value,
        time_value=time_value,
        party=party,
        table_type=table_type,
        tz=tz,
        window=window,
    )
