from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.tablesService import TableService, get_tables_service




router = APIRouter()

root = 'tables'

class Table(BaseModel):
    id: UUID
    name: str
    seats: int
    description: str
    
@router.get(f'/{root}/types' , response_model=list[Table])
async def get_table_types(service: TableService=Depends(get_tables_service)):

    results : list[Table] = await service.get_tables_type()

    return results
