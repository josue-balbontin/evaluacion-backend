from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class MenuItem(BaseModel):
    id: UUID
    restaurant_id: UUID
    name: str
    description: Optional[str] = None
    course: Optional[str] = None
    price: float
    allergens: Optional[List[str]] = None
    is_available: Optional[bool] = None
    available_from: Optional[date] = None
    available_until: Optional[date] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
