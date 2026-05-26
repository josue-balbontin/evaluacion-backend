from abc import ABC, abstractmethod
from typing import Any, List


class AbstractRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: Any) -> Any:
        pass

    @abstractmethod
    async def list_all(self, limit: int, offset: int, **kwargs) -> List[Any]:
        pass
