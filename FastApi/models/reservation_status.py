from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ReservationStatus(BaseModel):
    id: UUID
    name: str
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
