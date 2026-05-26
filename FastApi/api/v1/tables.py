from fastapi import APIRouter, Depends
from services.tablesService import TableService, get_tables_service
from schemas.TableType import TableType



router = APIRouter()

root = 'tables'


    
@router.get(f'/{root}/types' , response_model=list[TableType])
async def get_table_types(service: TableService=Depends(get_tables_service)):

    results : list[TableType] = await service.get_tables_type()

    return results
