


from uuid import UUID
from pydantic import BaseModel


class Menu(BaseModel):
    id: UUID
    course: str
    name: str
    description: str
    price: float
    allergens: list[str]