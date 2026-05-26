from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PricingTier(BaseModel):
    id: UUID
    table_type_id: UUID
    name: str
    price_per_seat: float
    priority: Optional[int] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    is_active: Optional[bool] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
