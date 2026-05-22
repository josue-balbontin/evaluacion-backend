
from repositories.tablesRepository import get_tables_repository, tablesRespository
from fastapi import Depends

class TableService:
    def __init__(self, repository: tablesRespository):
        self.tablesRepository = repository


    async def get_tables_type(self):
        return await self.tablesRepository.get_tables_type()
    


def get_tables_service(
        repository: tablesRespository = Depends(get_tables_repository)
) -> TableService:
    return TableService(repository)