from typing import Dict, Any


class DependencyContainer:
    """Dependency injection container"""
    
    def __init__(self):
        self._dependencies: Dict[str, Any] = {}
    
    def register(self, name: str, dependency: Any):
        """Register a dependency"""
        self._dependencies[name] = dependency
    
    def get(self, name: str) -> Any:
        """Get a dependency"""
        if name not in self._dependencies:
            raise KeyError(f"Dependency '{name}' not found")
        return self._dependencies[name]
    
    def has(self, name: str) -> bool:
        """Check if dependency exists"""
        return name in self._dependencies


# Global container instance
container = DependencyContainer()
