from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import Depends

from models.menu_item import MenuItem
from models.restaurant import Restaurant
from models.table_type import TableType
from repositories.restaurantRepository import get_restaurant_repository, restaurantRepository
from schemas.Restaurant import RestaurantDetail


from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional, Tuple
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException

class restaurantService:
    def __init__(self, repository: restaurantRepository):
        self.restaurantRepository = repository

    async def list_restaurants(self, limit: int, offset: int, name: Optional[str], address: Optional[str]):
        return await self.restaurantRepository.list_restaurants(limit, offset, name, address)

    async def search_restaurants(self, query_text: str, limit: int, offset: int):
        return await self.restaurantRepository.search_restaurants(query_text, limit, offset)

    async def get_restaurant_detail(self, restaurant_id: UUID) -> Optional[RestaurantDetail]:
        result = await self.restaurantRepository.get_restaurant_detail(restaurant_id)
        if not result:
            return None

        restaurant_model, table_types_models, menu_items_models = result
        
        data = restaurant_model.model_dump()
        data['table_types'] = [t.model_dump() for t in table_types_models]
        data['menu'] = [m.model_dump() for m in menu_items_models]
        
        return RestaurantDetail(**data)
    

    def _get_window(self, window: str, tz: str) -> tuple[date, date]:
        try:
            zone = ZoneInfo(tz)
        except Exception as exc:
            raise HTTPException(status_code=400, detail='invalid timezone') from exc

        today = datetime.now(zone).date()
        if window == '7d':
            return today, today + timedelta(days=7)
        if window == '30d':
            return today, today + timedelta(days=30)
        if window == '90d':
            return today, today + timedelta(days=90)
        raise HTTPException(status_code=400, detail='invalid window')

    
    async def get_popular_restaurants(self, period: str, timezone: str):
        
        start_date, end_date = self._get_window(period, timezone)

        restaurant_reservas=  await self.restaurantRepository.get_popular_restaurants(start_date, end_date, timezone)
        
        
        map_result = []
        for restaurant, reservas in restaurant_reservas:
            restaurant_data = restaurant.model_dump()
            restaurant_data['reservas_count'] = reservas
            map_result.append(restaurant_data)
        return map_result


def get_restaurant_service(
    repository: restaurantRepository = Depends(get_restaurant_repository),
) -> restaurantService:
    return restaurantService(repository)
