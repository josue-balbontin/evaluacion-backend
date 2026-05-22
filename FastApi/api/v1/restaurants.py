from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.Restaurant import Restaurant, RestaurantDetail
from services.restaurantService import restaurantService, get_restaurant_service

router = APIRouter()

root = 'restaurants'


@router.get(f'/{root}/search/', response_model=list[Restaurant])
async def search_restaurants(
    query: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: restaurantService = Depends(get_restaurant_service),
):
    return await service.search_restaurants(query, limit, offset)


@router.get(f'/{root}/', response_model=list[Restaurant])
async def list_restaurants(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    name: Optional[str] = None,
    address: Optional[str] = None,
    service: restaurantService = Depends(get_restaurant_service),
):
    return await service.list_restaurants(limit, offset, name, address)


@router.get(f'/{root}/{{restaurant_id}}', response_model=RestaurantDetail)
async def get_restaurant_detail(
    restaurant_id: UUID,
    service: restaurantService = Depends(get_restaurant_service),
):
    result = await service.get_restaurant_detail(restaurant_id)
    if not result:
        raise HTTPException(status_code=404, detail='restaurant not found')
    return result
