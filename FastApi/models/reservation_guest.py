from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ReservationGuest(BaseModel):
    id: UUID
    reservation_id: UUID
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    dietary_notes: Optional[str] = None
    is_primary: Optional[bool] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
