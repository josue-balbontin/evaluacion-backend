from typing import Optional
from elasticsearch import AsyncElasticsearch


es: Optional[AsyncElasticsearch] = None

# The function will be needed for dependency injection
async def get_elastic() -> AsyncElasticsearch:
    return es 