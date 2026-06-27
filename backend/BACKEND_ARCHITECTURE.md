# Backend Architecture — Social Farm AI OS

## Overview

The backend is built with **FastAPI** (Python 3.11) and follows a clean architecture pattern with clear separation of concerns.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/                  # API routes
│   │   ├── __init__.py      # Router aggregation
│   │   ├── ai/              # AI endpoints
│   │   ├── auth/            # Authentication endpoints
│   │   ├── organizations/   # Organization management
│   │   ├── research/        # Research module
│   │   ├── strategy/        # Strategy engine
│   │   └── workspaces/      # Workspace management
│   ├── core/                 # Core utilities
│   │   ├── config.py        # Application settings
│   │   ├── database.py      # Database configuration
│   │   └── security.py      # JWT & authentication
│   ├── db/                   # Database utilities
│   ├── models/               # SQLAlchemy models
│   │   ├── ai/              # AI agent models
│   │   ├── strategy/        # Strategy engine models
│   │   ├── brand.py
│   │   ├── rbac.py
│   │   ├── research.py
│   │   └── user.py
│   ├── schemas/              # Pydantic schemas
│   │   ├── base.py          # Base schemas
│   │   ├── user.py
│   │   ├── research.py
│   │   ├── rbac.py
│   │   └── brand.py
│   └── services/             # Business logic
│       ├── ai/              # AI services
│       │   ├── prompts/     # Prompt templates
│       │   ├── registry/    # Provider registry
│       │   ├── router/      # AI routing
│       │   ├── quality/     # Quality checks
│       │   └── workflow/    # Workflow management
│       └── strategy/        # Strategy engine
│           ├── audience_analyzer.py
│           ├── campaign_planner.py
│           ├── calendar_generator.py
│           ├── competitor_analyzer.py
│           ├── forecast_engine.py
│           ├── opportunity_engine.py
│           ├── recommendation_engine.py
│           └── strategy_engine.py
├── tests/                    # Test suite
│   └── strategy/            # Strategy tests
├── requirements.txt          # Python dependencies
├── runtime.txt              # Python version
└── Procfile                 # Render deployment
```

## Key Components

### 1. FastAPI Application (`main.py`)

- Initializes FastAPI with metadata
- Configures CORS middleware
- Mounts API routers
- Provides health endpoints
- Includes request logging middleware

### 2. Authentication (`core/security.py`)

- JWT token generation and validation
- Password hashing with Argon2
- HTTP Bearer authentication
- Token subject extraction

### 3. Database (`core/database.py`)

- SQLAlchemy async engine
- Session factory with context manager
- FastAPI dependency injection
- Connection pooling

### 4. Configuration (`core/config.py`)

- Pydantic Settings for type-safe config
- Environment variable loading
- Default values for development
- Cached settings instance

## API Endpoints

### Authentication (`/api/auth`)

- `POST /login` - User login
- `POST /register` - User registration
- `POST /refresh` - Refresh token
- `GET /me` - Get current user

### AI (`/api/ai`)

- `POST /chat` - AI chat completion
- `GET /providers` - List AI providers
- `POST /workflows` - Create AI workflow
- `GET /tasks` - List AI tasks

### Research (`/api/research`)

- `POST /analyze` - Analyze content
- `GET /trends` - Get trending topics
- `POST /competitors` - Competitor analysis

### Strategy (`/api/strategy`)

- `POST /plan` - Create strategy plan
- `GET /recommendations` - Get recommendations
- `POST /forecast` - Generate forecast

### Workspaces (`/api/workspaces`)

- `GET /` - List workspaces
- `POST /` - Create workspace
- `GET /:id` - Get workspace
- `PUT /:id` - Update workspace

### Organizations (`/api/organizations`)

- `GET /` - List organizations
- `POST /` - Create organization
- `GET /:id` - Get organization
- `PUT /:id` - Update organization

## Database Models

### User Model

```python
class User(Base):
    __tablename__ = "users"
    
    id: int
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
```

### Strategy Models

- `Strategy` - Marketing strategy
- `Campaign` - Marketing campaign
- `Audience` - Target audience
- `Competitor` - Competitor analysis
- `Forecast` - Performance forecast
- `Recommendation` - AI recommendations

### AI Models

- `AIAgent` - AI agent configuration
- `AITask` - AI task execution
- `AIWorkflow` - Workflow definitions
- `AIPrompt` - Prompt templates
- `AIProvider` - Provider configuration

## Services

### Strategy Engine

- `StrategyEngine` - Main strategy orchestrator
- `AudienceAnalyzer` - Audience analysis
- `CompetitorAnalyzer` - Competitor analysis
- `CampaignPlanner` - Campaign planning
- `ForecastEngine` - Performance forecasting
- `RecommendationEngine` - AI recommendations

### AI Services

- `AIRouter` - Multi-provider routing
- `AIRegistry` - Provider registry
- `AIQuality` - Quality checks
- `AIWorkflow` - Workflow management

## Development

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run with Docker
docker-compose up backend
```

### Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest -v --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/strategy/test_strategy_services.py -v
```

### Code Quality

```bash
# Linting
ruff check .

# Formatting
ruff format .

# Type checking
mypy app --ignore-missing-imports
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:password@localhost:5432/socialfarm` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `JWT_SECRET` | JWT signing secret | `change-me-in-production` |
| `DEBUG` | Enable debug mode | `false` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |

## Production Deployment

### Render

- Python 3.11 runtime
- Free tier available
- Auto-deploy from main branch
- Health check at `/health`

### Environment Setup

1. Set `DATABASE_URL` to production PostgreSQL
2. Set `REDIS_URL` to production Redis
3. Generate secure `JWT_SECRET`
4. Set `DEBUG=false`
5. Configure CORS origins for production domain