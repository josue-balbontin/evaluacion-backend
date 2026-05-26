from datetime import date

from fastapi import Depends

from repositories.menuRepository import get_menu_repository, menuRepository


class menuService:
    def __init__(self, repository: menuRepository):
        self.menuRepository = repository

    async def get_menu_items(self, date_value: date):
        return await self.menuRepository.get_menu_items(date_value)


def get_menu_service(
    repository: menuRepository = Depends(get_menu_repository)
) -> menuService:
    return menuService(repository)
