from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Availability(BaseModel):
    time: str
    table_type: UUID
    table_type_name: str
    seats: int
    available_seats: int
    price_per_seat: Optional[float] = None
