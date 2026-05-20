from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 minutes

class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # get_by_id returns a film object. It is optional, since the film may be missing from 
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        # We try to get data from the cache, because it works faster
        film = await self._film_from_cache(film_id)
        if not film:
            # If the film is not in the cache, then we look for it in Elasticsearch
            film = await self._get_film_from_elastic(film_id)
            if not film:
                # If it's missing from Elasticsearch, then the film is not in the database 
                return None
            # Save the film to the cache
            await self._put_film_to_cache(film)
        return film
    

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])
    

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        # We try to get data about the film from the cache using the get command
        # https://redis.io/commands/get/
        data = await self.redis.get(film_id)
        if not data:
            return None
        # pydantic provides a convenient API for creating model objects from json
        film = Film.parse_raw(data)
        return film


    async def _put_film_to_cache(self, film: Film):
        # Save the film data using the set command
        # Set the cache lifetime to 5 minutes
        # https://redis.io/commands/set/
        # pydantic allows you to serialize the model to json
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)

@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)