# Hexagonal Architecture Backend

This backend follows the Hexagonal Architecture (Ports and Adapters) pattern.

## Architecture Layers

```
backend/
├── domain/              # Core business logic (innermost layer)
│   ├── entities/        # Business entities
│   └── ports/           # Interfaces/contracts
├── application/         # Use cases / Application services
│   └── use_cases/       # Business operations
├── infrastructure/      # External adapters (outermost layer)
│   ├── api/            # FastAPI HTTP adapter
│   ├── persistence/    # Database adapters
│   ├── config.py       # Configuration
│   └── container.py    # Dependency injection
└── main.py             # Application entry point
```

## Key Principles

1. **Domain Layer** - Pure business logic, no external dependencies
2. **Application Layer** - Orchestrates use cases
3. **Infrastructure Layer** - Implements ports with external technologies
4. **Dependency Rule** - Dependencies point inward (Infrastructure → Application → Domain)

## Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the server:

```bash
uvicorn main:app --reload
```

API available at `http://localhost:8000/api/v1`
