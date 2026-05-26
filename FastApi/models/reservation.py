from datetime import date, datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Reservation(BaseModel):
    id: UUID
    restaurant_id: UUID
    table_type_id: UUID
    status_id: UUID
    reservation_date: date
    reservation_time: time
    party_size: int
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    notes: Optional[str] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
