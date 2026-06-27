# STACK REPORT

**Generated:** 2026-06-26
**Repository:** Social-Farm-AI

---

## Frontend

| Property | Value |
|----------|-------|
| **Framework** | Next.js 14.0.0 |
| **Router** | App Router (`app/` directory) |
| **React** | ^18 (installed: 18.x) |
| **TypeScript** | ^5 (installed: 5.9.3) |
| **Tailwind CSS** | ^3 (installed: 3.4.19) |
| **State Management** | Zustand ^4 |
| **Data Fetching** | @tanstack/react-query ^5 |
| **Package Manager** | npm (lock: package-lock.json) |
| **Linting** | ESLint ^8 with `eslint-config-next` |
| **Formatting** | Prettier |
| **Utility Classes** | tailwind-merge, clsx |

### Frontend Structure
```
frontend/
├── app/                     # App Router pages
│   ├── ai/                  # AI Command Center
│   ├── login/               # Login page
│   ├── register/            # Registration page
│   ├── research/            # Research Engine (with nested routes)
│   └── strategy/            # Content Strategy (with nested routes)
├── stores/                  # Zustand state stores
│   ├── research.ts
│   └── strategy-store.ts
└── package.json
```

### Missing Configuration (to be created)
- `tsconfig.json`
- `next.config.mjs`
- `tailwind.config.js`
- `postcss.config.mjs`
- `app/layout.tsx` (root layout)
- `app/page.tsx` (root page)

---

## Backend

| Property | Value |
|----------|-------|
| **Framework** | FastAPI 0.100.0 |
| **Python** | 3.11+ (target) |
| **ASGI Server** | Uvicorn 0.23.0 |
| **ORM** | SQLAlchemy 2.0.0 |
| **Migrations** | Alembic 1.11.0 |
| **Validation** | Pydantic 2.0.0 |
| **Task Queue** | Celery 5.3.0 |
| **Message Broker** | Redis 5.0.0 (via redis-py) |
| **Auth** | JWT (python-jose) + Argon2 (passlib) |
| **Testing** | Pytest 7.4.0, httpx 0.24.0 |
| **Linting** | Ruff 0.0.280, Black 23.7.0 |
| **Type Checking** | Mypy 1.4.0 |

### Backend Structure
```
backend/
├── app/
│   ├── api/                 # API route handlers
│   │   ├── ai/
│   │   ├── auth/
│   │   ├── organizations/
│   │   ├── research/
│   │   ├── strategy/
│   │   └── workspaces/
│   ├── core/                # Core utilities (security)
│   ├── db/                  # Database session
│   ├── models/              # SQLAlchemy models
│   │   ├── ai/              # AI system models
│   │   └── strategy/        # Strategy engine models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
│       ├── ai/              # AI services
│       └── strategy/        # Strategy services
├── tests/
└── requirements.txt
```

---

## Infrastructure

| Component | Technology |
|-----------|-----------|
| **Database** | PostgreSQL 15 |
| **Cache/Queue** | Redis 7 |
| **Containerization** | Docker Compose |
| **CI/CD** | GitHub Actions |
| **AI Providers** | OpenAI, Anthropic, Google (via gateway) |

---

## DevOps Status

| Area | Status |
|------|--------|
| Dockerfiles | ❌ Missing (to be created) |
| Docker Compose | ✅ `docker-compose.yml` |
| GitHub Actions | ✅ Basic test workflow |
| Environment Config | ✅ `.env.example` |
| Deployment Config | ❌ Missing |
