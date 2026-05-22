from datetime import datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Restaurant(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    timezone: Optional[str] = None
    is_active: Optional[bool] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
