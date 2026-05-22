from abc import ABC, abstractmethod
from typing import Any, Optional


class AbstractCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int = 300) -> None:
        pass
