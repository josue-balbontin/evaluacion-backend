from uuid import UUID

from pydantic import BaseModel


class TableType(BaseModel):
    id: UUID
    name: str
    seats: int
    description: str