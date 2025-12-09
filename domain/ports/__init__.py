from abc import ABC, abstractmethod
from typing import Optional, List


class Repository(ABC):
    """Port for data persistence"""
    
    @abstractmethod
    async def save(self, entity: any) -> any:
        pass
    
    @abstractmethod
    async def find_by_id(self, entity_id: str) -> Optional[any]:
        pass
    
    @abstractmethod
    async def find_all(self) -> List[any]:
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        pass
