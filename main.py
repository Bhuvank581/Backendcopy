from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.config import settings
from infrastructure.container import container
from infrastructure.api.routes import health
from infrastructure.persistence.in_memory_repository import InMemoryRepository


def create_app() -> FastAPI:
    """Application factory following hexagonal architecture"""
    
    app = FastAPI(
        title="Hexagonal API",
        description="FastAPI with Hexagonal Architecture",
        version="1.0.0",
        debug=settings.debug
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this based on your frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize dependencies (Dependency Injection)
    _setup_dependencies()
    
    # Register routes
    app.include_router(health.router, prefix=settings.api_prefix, tags=["health"])
    
    return app


def _setup_dependencies():
    """Setup dependency injection container"""
    # Register repositories
    container.register("repository", InMemoryRepository())


# Create application instance
app = create_app()
