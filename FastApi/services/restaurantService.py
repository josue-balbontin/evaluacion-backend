from typing import Optional
from uuid import UUID

from fastapi import Depends

from repositories.restaurantRepository import get_restaurant_repository, restaurantRepository
from schemas.Restaurant import RestaurantDetail


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

        restaurant, table_types, menu_items = result
        data = restaurant.model_dump() if hasattr(restaurant, 'model_dump') else restaurant.dict()
        data['table_types'] = [
            item.model_dump() if hasattr(item, 'model_dump') else item.dict()
            for item in table_types
        ]
        data['menu'] = [
            item.model_dump() if hasattr(item, 'model_dump') else item.dict()
            for item in menu_items
        ]
        return RestaurantDetail(**data)


def get_restaurant_service(
    repository: restaurantRepository = Depends(get_restaurant_repository),
) -> restaurantService:
    return restaurantService(repository)
