from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from schemas.Restaurant import Restaurant, RestaurantDetail
from services.restaurantService import restaurantService, get_restaurant_service
from fastapi_core.limiter import limiter
from fastapi_core.config import RATE_LIMIT

router = APIRouter()

root = 'restaurants'





@router.get(f'/{root}/search/', response_model=list[Restaurant])
@limiter.limit(RATE_LIMIT)
async def search_restaurants(
    request: Request,
    query: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: restaurantService = Depends(get_restaurant_service),
):
    return await service.search_restaurants(query, limit, offset)



@router.get(f'/{root}/popular' )
async def get_popular_restaurants(request: Request, period : str ,tz :  str = Query('UTC') , service: restaurantService = Depends(get_restaurant_service)):
    result =  await service.get_popular_restaurants(period, tz)
    if not result:
        raise HTTPException(status_code=404, detail='No popular restaurants found for the given period and timezone')
    return result


@router.get(f'/{root}/', response_model=list[Restaurant])
@limiter.limit(RATE_LIMIT)
async def list_restaurants(
    request: Request,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    name: Optional[str] = None,
    address: Optional[str] = None,
    service: restaurantService = Depends(get_restaurant_service),
):
    return await service.list_restaurants(limit, offset, name, address)


@router.get(f'/{root}/{{restaurant_id}}', response_model=RestaurantDetail)
@limiter.limit(RATE_LIMIT)
async def get_restaurant_detail(
    request: Request,
    restaurant_id: UUID,
    service: restaurantService = Depends(get_restaurant_service),
):
    result = await service.get_restaurant_detail(restaurant_id)
    if not result:
        raise HTTPException(status_code=404, detail='restaurant not found')
    return result


