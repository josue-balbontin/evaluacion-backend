from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

root = 'tables'

class Table(BaseModel):
    id: str
    name: str
    steats: int
    description: str
    
@router.get(f'/{root}/types')
async def get_table_types():
    return {'table_types': []}
