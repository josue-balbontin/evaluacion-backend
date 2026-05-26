from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TableType(BaseModel):
    id: UUID
    restaurant_id: UUID
    name: str
    description: Optional[str] = None
    seats: int
    quantity: Optional[int] = None
    price_per_seat: Optional[float] = None
    is_active: Optional[bool] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
