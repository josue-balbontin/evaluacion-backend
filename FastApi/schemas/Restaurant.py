from datetime import time
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from schemas.Menu import Menu
from schemas.TableType import TableType


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


class RestaurantDetail(Restaurant):
    table_types: List[TableType] = []
    menu: List[Menu] = []
