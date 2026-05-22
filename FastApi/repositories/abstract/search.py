from abc import ABC, abstractmethod
from typing import Any, List


class AbstractSearch(ABC):
    @abstractmethod
    async def search(self, query: str, limit: int, offset: int) -> List[Any]:
        pass
