# MONOREPO AUDIT REPORT

**Repository:** Social-Farm-AI  
**Audit Date:** 2026-06-27  
**Auditor:** Repository Auditor Agent  
**Repository Path:** `C:\Users\ADMIN\Downloads\Social-Farm-AI-main`  
**Status:** This is a zip-downloaded copy (no `.git` directory)

---

## 1. Repository Overview

| Attribute | Value |
|-----------|-------|
| **Project Name** | `social-farm-ai` |
| **Frontend** | Next.js 14 (React 18, TypeScript, Tailwind CSS) |
| **Backend** | FastAPI (Python 3.11, SQLAlchemy, Celery) |
| **Deployment Targets** | Vercel (frontend), Render (backend) |
| **Containerization** | Docker (multi-stage builds), Docker Compose |
| **CI/CD** | GitHub Actions (`.github/workflows/test.yml`) |
| **Total Root Entries** | 45 (files + directories) |
| **Version** | v0.3.0 (per FastAPI app) / v0.1.0 (per frontend package.json) |
| **License** | MIT (LICENSE.md present) |

---

## 2. Simplified Directory Tree

```
Social-Farm-AI-main/
├── api/                          # [DUPLICATE] Vercel serverless entry (duplicates backend/)
│   ├── index.py                  #   Vercel serverless handler
│   └── app/
│       ├── main.py               #   FastAPI app (duplicate of backend/app/main.py)
│       ├── api/                   #   Routers (duplicate)
│       ├── core/                  #   Config/Security (duplicate)
│       ├── models/                #   DB models (duplicate)
│       └── schemas/               #   Pydantic schemas (duplicate)
├── assets/                       # [PLACEHOLDER] — only .gitkeep
├── backend/                      # [PRIMARY] FastAPI backend
│   ├── app/
│   │   ├── main.py               #   FastAPI entry point
│   │   ├── api/                   #   API route handlers
│   │   ├── core/                  #   Security, config
│   │   ├── db/                    #   Database session
│   │   ├── models/                #   SQLAlchemy models
│   │   ├── schemas/               #   Pydantic schemas
│   │   └── services/              #   Business logic (AI, RBAC, Strategy)
│   ├── tests/                     #   Strategy tests (legacy location)
│   ├── Procfile                   #   Heroku/Render process definition
│   ├── requirements.txt           #   Python dependencies
│   └── runtime.txt                #   Python version (3.11.0)
├── docker/                       # [PLACEHOLDER] — only .gitkeep
├── docs/                         # Comprehensive documentation
│   ├── specifications/            #   Split into 10 spec areas (00-Core to 10-API)
│   ├── diagrams/                  #   Architecture diagrams (Draw.io markdown)
│   ├── prompts/                   #   Build prompts (Phase 01-08)
│   ├── archive/                   #   Archived specs
│   └── *.md                       #   Multiple audit/plan/spec reports
├── frontend/                     # Next.js frontend app
│   ├── app/                       #   App Router pages
│   │   ├── ai/                    #     AI agents/health/models pages
│   │   ├── api/                   #     API client routes
│   │   ├── login/                 #     Login page
│   │   ├── register/              #     Registration page
│   │   ├── research/              #     Research module pages
│   │   ├── strategy/              #     Strategy module pages
│   │   ├── layout.tsx             #     Root layout
│   │   ├── page.tsx               #     Home page
│   │   └── globals.css            #     Global styles
│   ├── stores/                    #   Zustand state management
│   ├── node_modules/              #   Installed dependencies
│   ├── .next/                     #   Next.js build output
│   ├── package.json               #   Node dependencies
│   └── vercel.json                #   Frontend Vercel config
├── infrastructure/               # [PLACEHOLDER] — only .gitkeep
├── scripts/                      # [PLACEHOLDER] — only .gitkeep
├── shared/                       # [PLACEHOLDER] — only .gitkeep
├── tests/                        # Centralized test directory
│   ├── backend/                   #   Backend tests
│   │   ├── ai/                    #     AI orchestrator tests
│   │   ├── conftest.py            #     (empty file)
│   │   └── pytest.ini             #     Pytest config
│   ├── frontend/                  #   Frontend tests
│   │   ├── vitest.config.ts       #     Vitest configuration
│   │   └── setup.ts               #     Test setup
│   └── README.md                  #   Testing documentation
├── .github/
│   └── workflows/
│       └── test.yml               #   GitHub Actions CI/CD
├── vercel.json                    # Root Vercel config (frontend deployment)
├── render.yaml                    # Render config (backend deployment)
├── docker-compose.yml             # Orchestrates db, redis, backend, frontend
├── Dockerfile.backend             # Multi-stage Python build
├── Dockerfile.frontend            # Multi-stage Node build
├── requirements.txt               # Root requirements (subset of backend/requirements.txt)
├── pyproject.toml                 # Poetry project config
├── ruff.toml                      # Python linter config
├── .editorconfig                  # Editor settings
├── .eslintrc.json                 # ESLint config (Next.js)
├── .prettierrc                    # Prettier config
├── .prettierignore                # Prettier ignore rules
├── .gitattributes                 # Git attribute rules
├── .gitignore                     # Git ignore rules
├── .dockerignore                  # Docker build ignore rules
├── .vercelignore                  # Vercel deployment ignore rules
├── .env.example                   # Environment variable template
├── README.md                      # Project readme
├── LICENSE.md                     # MIT License
├── CHANGELOG.md                   # Changelog
├── CONTRIBUTING.md                # Contribution guide
├── CODE_OF_CONDUCT.md             # Code of conduct
├── SECURITY.md                    # Security policy
└── Various *REPORT.md files       # 10+ audit/report markdown files
```

---

## 3. Configuration Audit

### 3.1 Root Configuration Files

| File | Status | Details |
|------|--------|---------|
| `.eslintrc.json` | PRESENT | Extends `next/core-web-vitals` - proper for Next.js |
| `.prettierrc` | PRESENT | semi: true, singleQuote: true, tabWidth: 2, trailingComma: "es5", printWidth: 120 |
| `.prettierignore` | PRESENT | Ignores node_modules, .next, out, dist, .env* |
| `.editorconfig` | PRESENT | indent_style: space, indent_size: 2, charset: utf-8, lf line endings |
| `.gitattributes` | PRESENT | Auto text detection, language-specific diff settings, binary handling |
| `.gitignore` | PRESENT | Comprehensive (Python, Node, IDE, OS, Docker, Testing, DB, Logs, Build) |
| `.dockerignore` | PRESENT | Comprehensive (git, Python, Node, IDE, Docker, Testing, DB, Logs) |
| `.vercelignore` | PRESENT | Excludes backend/, docker/, infrastructure/, scripts/, tests/, docs/, assets/, shared/, *.md |
| `.env.example` | PRESENT | Database, Redis, JWT, Backend, Frontend, AI provider placeholders |
| `ruff.toml` | PRESENT | line-length: 120, lint rules: E, F, I |
| `pyproject.toml` | PRESENT | Poetry config (name: social-farm-ai, version: 0.1.0) |

**All 11 root config files are present.** No missing critical configs.

### 3.2 Workspace Configuration

| Check | Status | Details |
|-------|--------|---------|
| Root `package.json` | **MISSING** | No root package.json exists. The repository does not use npm workspaces, yarn workspaces, or pnpm workspaces. |
| npm workspaces | NOT CONFIGURED | Only `frontend/package.json` exists, no workspace configuration. |
| pyproject.toml | PRESENT | Poetry config exists but appears unused; actual deps managed via requirements.txt |

### 3.3 Deployment Configuration

| File | Status | Details |
|------|--------|---------|
| `vercel.json` (root) | PRESENT | Build: `cd frontend && npm install && npm run build`, Output: `frontend/.next`, Framework: nextjs |
| `frontend/vercel.json` | PRESENT | Duplicate of root vercel.json (subset), framework: nextjs |
| `render.yaml` | PRESENT | Python web service, pip installs backend/requirements.txt, starts uvicorn |
| `Procfile` (backend/) | PRESENT | `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| `runtime.txt` (backend/) | PRESENT | `python-3.11.0` |

**Note:** Both root `vercel.json` and `frontend/vercel.json` exist with overlapping purpose. This is a potential source of confusion.

---

## 4. Directory Structure Verification

### 4.1 Frontend (`frontend/`)

| Expected | Present | Notes |
|----------|---------|-------|
| `package.json` | YES | Dependencies: next@14.0.0, react@18, zustand@4, @tanstack/react-query@5 |
| `tsconfig.json` | YES | Target es5, strict mode, bundler module resolution, path alias `@/*` |
| `next.config.mjs` | YES | Has API proxy rewrite for development |
| `tailwind.config.js` | YES | Custom brand color palette |
| `postcss.config.mjs` | YES | PostCSS config |
| `app/` (App Router) | YES | Pages: ai/, api/, login/, register/, research/, strategy/ |
| `stores/` | YES | Zustand stores: research.ts, strategy-store.ts |
| `node_modules/` | YES | Pre-installed (includes zustand, etc.) |
| `.next/` | YES | Build output present |
| `vercel.json` | YES | Frontend-specific Vercel config |

**Frontend structure is complete and properly configured.**

### 4.2 Backend (`backend/`)

| Expected | Present | Notes |
|----------|---------|-------|
| `requirements.txt` | YES | 20 packages (FastAPI, SQLAlchemy, Celery, Redis, JWT, testing tools) |
| `runtime.txt` | YES | Python 3.11.0 |
| `Procfile` | YES | Uvicorn start command |
| `app/main.py` | YES | FastAPI app with CORS, health endpoint, error handling |
| `app/api/` | YES | Routers: ai, auth, organizations, research, strategy, workspaces |
| `app/core/` | YES | Security module |
| `app/db/` | YES | Database session management |
| `app/models/` | YES | SQLAlchemy models (user, brand, rbac, research, ai/, strategy/) |
| `app/schemas/` | YES | Pydantic schemas (user, brand, rbac, research) |
| `app/services/` | YES | Business logic: ai/ (8 sub-modules), rbac.py, strategy/ (8 engines) |
| `tests/` | YES | Strategy tests (2 files) |

**Backend structure is complete and well-organized.**

### 4.3 Expected Monorepo Directories

| Directory | Status | Contents | Notes |
|-----------|--------|----------|-------|
| `frontend/` | **VERIFIED** | Full Next.js app | Propserly structured |
| `backend/` | **VERIFIED** | Full FastAPI app | Properly structured |
| `shared/` | **PLACEHOLDER** | `.gitkeep` only | Empty — no shared code |
| `api/` | **DUPLICATE** | Duplicates `backend/` | See Issue #2 below |
| `tests/` | **PARTIAL** | backend/ai, frontend/ | Missing e2e/, performance/, security/ (listed in README) |
| `docs/` | **VERIFIED** | Full specs, diagrams, prompts | Well-organized |
| `scripts/` | **PLACEHOLDER** | `.gitkeep` only | Empty |
| `infrastructure/` | **PLACEHOLDER** | `.gitkeep` only | Empty |
| `assets/` | **PLACEHOLDER** | `.gitkeep` only | Empty |
| `docker/` | **PLACEHOLDER** | `.gitkeep` only | Empty |
| `.github/` | **VERIFIED** | CI workflow (test.yml) | Proper |

---

## 5. Issues Found

### ISSUE 1 (HIGH): `api/` directory is a near-duplicate of `backend/`

- **Severity:** HIGH
- **Description:** The `api/` directory contains a complete copy of the FastAPI application structure (`app/main.py`, `app/api/`, `app/core/`, `app/models/`, `app/schemas/`), with nearly identical file contents (e.g., `app/api/__init__.py` is byte-for-byte identical).
- **Evidence:** Both `backend/app/__init__.py` and `api/app/__init__.py` exist; `api/app/main.py` is identical to `backend/app/main.py`; `api/app/models/ai/` has the same 9 files as `backend/app/models/ai/`.
- **Risk:** Code drift — updates to `backend/` must be manually mirrored to `api/`. This is a maintenance liability.
- **Recommendation:** Remove the `api/` directory and use `api/index.py` as a thin Vercel serverless wrapper that imports directly from `backend/app/main.py`.

### ISSUE 2 (MEDIUM): Duplicate `vercel.json` (root + frontend/)

- **Severity:** MEDIUM
- **Description:** Both the root `vercel.json` and `frontend/vercel.json` define Vercel deployment configuration. The root one is more comprehensive (includes build/install commands), while the frontend one is a subset.
- **Risk:** Confusion about which config Vercel uses during deployment. If the Vercel project root is the repo root, the root `vercel.json` takes precedence, making `frontend/vercel.json` dead config.
- **Recommendation:** Consolidate into a single `vercel.json` at root and remove `frontend/vercel.json` (or vice versa depending on Vercel project setup).

### ISSUE 3 (MEDIUM): Scattered test locations

- **Severity:** MEDIUM
- **Description:** Tests exist in two separate directory trees:
  - `backend/tests/` — strategy tests (legacy location)
  - `tests/backend/` — AI orchestrator tests (new location)
  - `tests/frontend/` — frontend test config
- **Risk:** Fragmented test discovery. Developers may not know where to add new tests. `tests/README.md` also references `e2e/`, `performance/`, and `security/` test directories that do not exist.
- **Recommendation:** Consolidate all backend tests under `tests/backend/` and remove `backend/tests/`. Create placeholder directories for e2e/, performance/, security/ if planned, or update the README.

### ISSUE 4 (LOW): Root `requirements.txt` vs `backend/requirements.txt`

- **Severity:** LOW
- **Description:** Root `requirements.txt` (14 packages, production-only) is a subset of `backend/requirements.txt` (20 packages, includes dev tools like pytest, black, ruff, mypy).
- **Risk:** Slight confusion — developers may install the wrong one. The root copy exists for Vercel serverless deployment.
- **Recommendation:** Add a comment header to root `requirements.txt` explicitly stating "Production-only subset for Vercel deployment" and consider using `backend/requirements-prod.txt` instead.

### ISSUE 5 (LOW): 5 placeholder directories with only `.gitkeep`

- **Severity:** LOW
- **Description:** `shared/`, `scripts/`, `infrastructure/`, `assets/`, and `docker/` contain only a `.gitkeep` file.
- **Risk:** None immediate, but the purpose of these directories is unclear without documentation.
- **Recommendation:** Either populate with content or add a `.md` file explaining the intended purpose of each.

### ISSUE 6 (LOW): `.git` not present (expected — zip download)

- **Severity:** INFO
- **Description:** No `.git` directory exists, confirming this is a downloaded ZIP archive, not a git clone.
- **Recommendation:** When ready to version-control, run `git init` and connect to the appropriate remote.

### ISSUE 7 (LOW): No root package.json / workspace config

- **Severity:** LOW
- **Description:** The monorepo has no root `package.json` with workspace configuration (`workspaces: ["frontend"]` or similar). Only `frontend/package.json` exists.
- **Recommendation:** If JavaScript monorepo tooling is desired, add a root `package.json` with npm/yarn/pnpm workspace configuration.

---

## 6. Recommendations Summary

| Priority | Issue | Action |
|----------|-------|--------|
| **HIGH** | `api/` duplicates `backend/` | Remove `api/` directory; use thin Vercel wrapper importing from `backend/` |
| **MEDIUM** | Duplicate `vercel.json` | Consolidate into a single config file |
| **MEDIUM** | Scattered tests | Move `backend/tests/` into `tests/backend/`; update test docs |
| **LOW** | Dual `requirements.txt` | Clarify root requirements.txt purpose; consider renaming |
| **LOW** | Placeholder directories | Document purpose or populate with content |
| **LOW** | No workspace config | Add root package.json if JS monorepo tooling needed |

---

## 7. Positive Findings

- **Comprehensive root configuration** — All expected config files are present and well-formed.
- **Docker support** — Multi-stage Dockerfiles for both frontend and backend, plus docker-compose.yml with Postgres and Redis.
- **CI/CD configured** — GitHub Actions workflow tests both frontend and backend.
- **Documentation rich** — Extensive docs/ directory with specifications, diagrams, build prompts, and audit reports.
- **State management** — Frontend uses Zustand stores properly with TypeScript.
- **API proxy** — Next.js rewrites configured for seamless development.
- **Security basics** — JWT auth, CORS configured, `.env.example` with secure defaults.
- **Deployment ready** — Vercel (frontend) and Render (backend) configs both present and functional.

---

## 8. Quick Stats

| Metric | Value |
|--------|-------|
| Total files (approx.) | 200+ |
| Root config files | 11/11 present |
| Expected monorepo dirs | 10/10 present (5 verified, 3 placeholder, 1 duplicate, 1 partial) |
| Placeholder dirs | 5 (shared, scripts, infrastructure, assets, docker) |
| Duplicate dirs | 1 (api/ mirrors backend/) |
| Test locations | 2 (backend/tests/, tests/) |
| Deployment configs | 3 (vercel.json x2, render.yaml) |
| CI workflows | 1 (test.yml) |
| Docker configs | 4 (2 Dockerfiles, docker-compose.yml, .dockerignore) |

---

*Audit completed by Repository Auditor Agent — 2026-06-27*
