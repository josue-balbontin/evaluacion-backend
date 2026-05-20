from typing import Optional
from redis.asyncio import Redis


redis: Optional[Redis] = None


# The function will be needed for dependency injection
async def get_redis() -> Redis:
    return redis