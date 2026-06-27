# Agent Mapping — Social Farm AI Project

## Project Overview

**Social Farm AI OS** is an intelligent content operations platform that transforms ideas into high-quality multimedia content through coordinated AI agents, structured workflows, and human oversight.

**Tech Stack:**
- **Backend:** Python 3.11, FastAPI, SQLAlchemy, PostgreSQL, Redis
- **Frontend:** Next.js 14, React 18, TypeScript 5, Tailwind CSS 3, Zustand, React Query
- **Infrastructure:** Docker, Render (backend), Vercel (frontend), PostgreSQL, Redis
- **AI:** Multi-provider routing (OpenAI, Anthropic, Gemini, Grok, DeepSeek)

---

## Agent 1: GitHub Repository Manager + Git Expert

**Primary Responsibilities:**
- Repository cloning and setup
- Branch management (create, switch, delete)
- Commit operations with conventional commits
- Push/pull operations
- Merge conflict resolution
- Pull request management
- Git history analysis
- Interactive rebasing
- Cherry-pick operations
- Commit squashing
- Branch recovery

**Key Files:**
- `.gitignore`
- `.github/` (GitHub Actions workflows)
- `CONTRIBUTING.md`
- `CHANGELOG.md`

**Commands to Master:**
```bash
git clone, git branch, git checkout, git commit, git push, git pull
git rebase, git cherry-pick, git squash, git merge
gh pr create, gh pr merge, gh pr review
```

---

## Agent 2: FastAPI Expert + Python Expert + SQLAlchemy Expert

**Primary Responsibilities:**
- FastAPI application architecture
- API routing and endpoint design
- Middleware configuration
- Dependency injection patterns
- Background task management
- Authentication/authorization
- OpenAPI documentation
- Python async programming
- Package management
- SQLAlchemy ORM models
- Database migrations (Alembic)
- Query optimization

**Key Files:**
- `backend/app/main.py` — FastAPI entry point
- `backend/app/api/` — API routers
- `backend/app/models/` — SQLAlchemy models
- `backend/app/schemas/` — Pydantic schemas
- `backend/app/services/` — Business logic
- `backend/app/core/` — Security, config
- `backend/requirements.txt`
- `pyproject.toml`

**Current Structure:**
```
backend/app/
├── main.py              # FastAPI app initialization
├── api/                 # API routers
├── core/                # Security, config
├── db/                  # Database setup
├── models/              # SQLAlchemy models
│   ├── ai/              # AI agent models
│   ├── strategy/        # Strategy engine models
│   ├── brand.py
│   ├── rbac.py
│   ├── research.py
│   └── user.py
├── schemas/             # Pydantic schemas
└── services/            # Business logic
    ├── ai/              # AI services
    └── strategy/        # Strategy engine
```

---

## Agent 3: Next.js 14 Expert + React Expert + TypeScript Expert + Tailwind CSS Expert

**Primary Responsibilities:**
- Next.js 14 App Router
- React Server Components
- Route Handlers
- Metadata API
- Server Actions
- Image optimization
- React hooks and performance
- State management (Zustand)
- Component optimization
- Suspense and lazy loading
- TypeScript strict typing
- Interface generation
- Responsive UI
- Dark mode implementation
- Layout optimization

**Key Files:**
- `frontend/app/` — Next.js App Router
- `frontend/app/layout.tsx` — Root layout
- `frontend/app/page.tsx` — Home page
- `frontend/stores/` — Zustand stores
- `frontend/tailwind.config.js`
- `frontend/tsconfig.json`
- `frontend/package.json`

**Current Structure:**
```
frontend/app/
├── layout.tsx           # Root layout
├── page.tsx             # Home page
├── globals.css          # Global styles
├── ai/                  # AI features
├── api/                 # API routes
├── login/               # Auth pages
├── register/            # Auth pages
├── research/            # Research module
└── strategy/            # Strategy module
```

---

## Agent 4: Docker Expert + Render Deployment Expert + Vercel Expert + DevOps Engineer

**Primary Responsibilities:**
- Dockerfile creation and optimization
- Multi-stage builds
- Docker Compose configuration
- Container networking
- Health checks
- Render deployment (backend)
- Vercel deployment (frontend)
- Environment variable management
- Custom domains
- Infrastructure monitoring
- Logging and scaling
- Production readiness

**Key Files:**
- `Dockerfile.backend` — Backend Docker image
- `Dockerfile.frontend` — Frontend Docker image
- `docker-compose.yml` — Local development
- `render.yaml` — Render deployment
- `vercel.json` — Vercel configuration
- `.dockerignore`
- `.vercelignore`
- `infrastructure/`

**Current Configuration:**
```yaml
# docker-compose.yml
services:
  db: postgres:15
  redis: redis:7
  backend: FastAPI (port 8000)
  frontend: Next.js (port 3000)

# render.yaml
- Backend: Python 3.11, free tier
- Health check: /health
- Auto-deploy: true

# vercel.json
- Frontend: Next.js 14
```

---

## Agent 5: CI/CD Engineer + Testing Engineer + Security Auditor

**Primary Responsibilities:**
- GitHub Actions workflows
- Build pipelines
- Test automation
- Release automation
- Deployment workflows
- Pytest (backend testing)
- Jest (frontend testing)
- Playwright (E2E testing)
- React Testing Library
- Coverage analysis
- Secret scanning
- JWT/OAuth security
- Dependency vulnerability scanning
- OWASP compliance
- Environment security

**Key Files:**
- `.github/workflows/` — CI/CD pipelines
- `backend/tests/` — Backend tests
- `tests/` — Shared tests
- `SECURITY.md`
- `.env.example`

**Current Test Structure:**
```
backend/tests/
└── strategy/
    ├── test_strategy_services.py
    └── test_strategy_api.py
```

---

## Agent 6: API Architect + Performance Optimizer + Accessibility Expert

**Primary Responsibilities:**
- REST API design
- API versioning
- Request validation
- Error handling
- OpenAPI compliance
- Backend profiling
- Frontend optimization
- Database tuning
- Bundle analysis
- Caching strategies
- WCAG compliance
- Keyboard navigation
- Screen reader support
- Semantic HTML

**Key Files:**
- `backend/app/api/` — API endpoints
- `backend/app/core/` — Security, config
- `api/app/api/` — Additional API layer
- `frontend/app/` — UI components
- `frontend/app/globals.css` — Styles

**API Endpoints:**
```
/api/auth/       — Authentication
/api/ai/         — AI services
/api/research/   — Research module
/api/strategy/   — Strategy engine
/api/workspaces/ — Workspace management
/api/organizations/ — Organization management
```

---

## Agent 7: Documentation Generator + Monorepo Architect

**Primary Responsibilities:**
- README generation
- API documentation
- Deployment guides
- Architecture documentation
- Changelog maintenance
- Repository organization
- Workspace configuration
- Dependency boundaries
- Build optimization

**Key Files:**
- `README.md`
- `docs/` — Documentation folder
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `SECURITY.md`
- `LICENSE.md`
- `BRAND_MANAGEMENT.md`
- `MONOREPO_AUDIT.md`
- `PROJECT_STRUCTURE_REPORT.md`

**Current Documentation:**
```
docs/
├── specifications/     # Detailed specs
│   ├── 03-AI/         # AI specifications
│   ├── 07-Publishing/ # Publishing specs
│   ├── 08-Analytics/  # Analytics specs
│   └── 09-Security/   # Security specs
└── *.md               # Various reports
```

---

## Agent 8: AI Gateway Engineer + Prompt Engineering Specialist (Future)

**Primary Responsibilities:**
- Multi-provider AI routing
- OpenAI integration
- Anthropic integration
- Gemini integration
- Grok integration
- DeepSeek integration
- Failover logic
- Prompt template design
- System prompt optimization
- AI workflow design
- Evaluation frameworks
- Prompt versioning

**Key Files:**
- `backend/app/services/ai/` — AI services
- `backend/app/models/ai/` — AI models
- `api/app/models/ai/` — AI API models
- `frontend/app/ai/` — AI frontend

**AI Model Structure:**
```
backend/app/models/ai/
├── agent.py       # AI agent models
├── execution.py   # Execution tracking
├── memory.py      # Memory management
├── metrics.py     # Performance metrics
├── prompt.py      # Prompt templates
├── provider.py    # Provider configuration
├── task.py        # Task management
└── workflow.py    # Workflow definitions
```

---

## Implementation Priority

Based on the priority installation order:

1. **GitHub Repository Manager + Git Expert** ✅ (AGENTS.md created)
2. **Git Expert** ✅ (Included in Agent 1)
3. **Python Expert** → Agent 2
4. **FastAPI Expert** → Agent 2
5. **Next.js 14 Expert** → Agent 3
6. **TypeScript Expert** → Agent 3
7. **React Expert** → Agent 3
8. **Docker Expert** → Agent 4
9. **Render Deployment Expert** → Agent 4
10. **Vercel Expert** → Agent 4
11. **CI/CD Engineer** → Agent 5
12. **PostgreSQL Expert** → Agent 2 (database)
13. **SQLAlchemy Expert** → Agent 2
14. **Testing Engineer** → Agent 5
15. **Security Auditor** → Agent 5
16. **Performance Optimizer** → Agent 6
17. **API Architect** → Agent 6
18. **Monorepo Architect** → Agent 7
19. **Documentation Generator** → Agent 7
20. **Accessibility Expert** → Agent 6
21. **AI Gateway Engineer** → Agent 8 (Future)
22. **Prompt Engineering Specialist** → Agent 8 (Future)
23. **Code Refactoring Expert** → Agent 6
24. **DevOps Engineer** → Agent 4
25. **Tailwind CSS Expert** → Agent 3

---

## Next Steps

1. **Configure OpenCode skills** for each agent
2. **Set up agent routing** in OpenCode configuration
3. **Test agent workflows** with sample tasks
4. **Document agent interactions** and collaboration patterns
5. **Monitor performance** and optimize as needed