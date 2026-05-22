import json
import logging
from typing import Any, Optional
from functools import wraps
from repositories.redis.cache import AbstractCache

logger = logging.getLogger(__name__)


def _custom_encoder(obj: Any):
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()
    if hasattr(obj, 'dict'):
        return obj.dict()
    return str(obj)


class RedisCache(AbstractCache):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def get(self, key: str) -> Optional[Any]:
        if self.redis_client is None:
            return None
        try:
            data = await self.redis_client.get(key)
            if not data:
                return None
            return json.loads(data)
        except Exception as exc:
            logger.warning(f"Redis no responde, pasando a Postgres: {exc}")
            return None

    async def set(self, key: str, value: Any, expire: int = 300) -> None:
        if self.redis_client is None or value is None:
            return
        try:
            json_data = json.dumps(value, default=_custom_encoder)
            await self.redis_client.set(key, json_data, ex=expire)
        except Exception as exc:
            logger.warning(f"Error guardando en Redis: {exc}")


def decorator_cache(prefix: str, expire: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            args_str = "_".join([str(arg) for arg in args])
            cache_key = f"{prefix}_{args_str}" if args_str else prefix
            
            if not hasattr(self, 'cache'):
                return await func(self, *args, **kwargs)

            cached_data = await self.cache.get(cache_key)
            if cached_data:
                return cached_data

            result = await func(self, *args, **kwargs)

            await self.cache.set(cache_key, result, expire)

            return result
        return wrapper
    return decorator
