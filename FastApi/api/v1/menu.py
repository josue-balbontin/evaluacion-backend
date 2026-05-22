from datetime import date

from fastapi import APIRouter, Depends, Query

from schemas.Menu import Menu
from services.menuService import menuService, get_menu_service





router = APIRouter()

root = 'menu'


    
@router.get(f'/{root}' , response_model=list[Menu])
async def get_menu_items(date_value: date ,service: menuService = Depends(get_menu_service),):
    results: list[Menu] = await service.get_menu_items(date_value)
    return results
