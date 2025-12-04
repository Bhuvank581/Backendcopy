from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


class UseCase(ABC, Generic[T]):
    """Base use case interface"""
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> T:
        pass
