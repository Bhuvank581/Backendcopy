from typing import Optional, List, Dict, Any
from domain.ports import Repository


class InMemoryRepository(Repository):
    """In-memory implementation of Repository port"""
    
    def __init__(self):
        self._storage: Dict[str, Any] = {}
        self._counter = 0
    
    async def save(self, entity: Any) -> Any:
        if not entity.id:
            self._counter += 1
            entity.id = str(self._counter)
        
        self._storage[entity.id] = entity
        return entity
    
    async def find_by_id(self, entity_id: str) -> Optional[Any]:
        return self._storage.get(entity_id)
    
    async def find_all(self) -> List[Any]:
        return list(self._storage.values())
    
    async def delete(self, entity_id: str) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False
