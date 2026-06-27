# Environment Configuration Report

**Project:** Social Farm AI OS  
**Date:** 2026-06-27  
**Scope:** Audit of all environment variable configurations across the codebase  
**Engineer:** Environment Engineer (Multi-Agent System)

---

## Table of Contents

1. [Sources Analyzed](#1-sources-analyzed)
2. [Complete Environment Variable Inventory](#2-complete-environment-variable-inventory)
3. [Requirement vs Optional Classification](#3-requirement-vs-optional-classification)
4. [Secret vs Public Classification](#4-secret-vs-public-classification)
5. [Current Status (Set / Not Set)](#5-current-status-set--not-set)
6. [NEXT_PUBLIC_ Prefix Convention Compliance](#6-next_public_-prefix-convention-compliance)
7. [Deployment Configuration Analysis](#7-deployment-configuration-analysis)
   - 7.1 Render (render.yaml)
   - 7.2 Vercel (vercel.json)
   - 7.3 Docker Compose
   - 7.4 GitHub Actions CI
8. [Cross-Cutting Issues](#8-cross-cutting-issues)
9. [Deployment-Specific Recommendations](#9-deployment-specific-recommendations)
10. [Placeholder Generation](#10-placeholder-generation)

---

## 1. Sources Analyzed

| # | File | Path |
|---|------|------|
| 1 | `.env.example` | `/root/.env.example` |
| 2 | `render.yaml` | `/root/render.yaml` |
| 3 | `vercel.json` (root) | `/root/vercel.json` |
| 4 | `vercel.json` (frontend) | `/frontend/vercel.json` |
| 5 | `next.config.mjs` | `/frontend/next.config.mjs` |
| 6 | `backend/app/main.py` | `/backend/app/main.py` |
| 7 | `backend/app/db/session.py` | `/backend/app/db/session.py` |
| 8 | `backend/app/core/security.py` | `/backend/app/core/security.py` |
| 9 | `backend/app/services/ai/gateway/__init__.py` | `/backend/app/services/ai/gateway/__init__.py` |
| 10 | `api/app/main.py` | `/api/app/main.py` (duplicate) |
| 11 | `api/app/core/security.py` | `/api/app/core/security.py` (duplicate) |
| 12 | `docker-compose.yml` | `/root/docker-compose.yml` |
| 13 | `Dockerfile.backend` | `/root/Dockerfile.backend` |
| 14 | `Dockerfile.frontend` | `/root/Dockerfile.frontend` |
| 15 | `.github/workflows/test.yml` | `/root/.github/workflows/test.yml` |
| 16 | `.gitignore` | `/root/.gitignore` |

No `.env`, `.env.local`, `.env.production`, or `.env.development` files exist anywhere in the repository (frontend/ or backend/). They are properly excluded via `.gitignore`.

---

## 2. Complete Environment Variable Inventory

### 2.1 Backend — Core Required

| Variable | Source File(s) | Default Value | Purpose |
|----------|---------------|---------------|---------|
| `DATABASE_URL` | `db/session.py` | `postgresql://postgres:postgres@localhost:5432/social_farm_ai` | PostgreSQL connection string |
| `JWT_SECRET` | `core/security.py` | `change-me-in-production` | HMAC signing key for JWT tokens |
| `REDIS_URL` | (CI test.yml) | `redis://localhost:6379/0` | Redis connection string (used by Celery) |
| `CORS_ORIGINS` | `main.py` | `http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000` | CSV of allowed CORS origins |
| `HOST` | `main.py` | `0.0.0.0` | Server bind address |
| `PORT` | `main.py` | `8000` | Server listen port |
| `DEBUG` | `main.py` | (empty string) | Enables debug logging & hot-reload when `"1"`, `"true"`, or `"yes"` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `core/security.py` | `30` | JWT token expiry in minutes |

### 2.2 Backend — AI Provider Keys (Optional)

| Variable | Source File | Default Value | Purpose |
|----------|-------------|---------------|---------|
| `OPENAI_API_KEY` | `ai/gateway/__init__.py` | `""` (empty) | OpenAI API authentication |
| `OPENAI_BASE_URL` | `ai/gateway/__init__.py` | `https://api.openai.com/v1` | OpenAI API base URL (self-hosted compatible) |
| `ANTHROPIC_API_KEY` | `ai/gateway/__init__.py` | `""` (empty) | Anthropic API authentication |
| `ANTHROPIC_BASE_URL` | `ai/gateway/__init__.py` | `https://api.anthropic.com/v1` | Anthropic API base URL |
| `GOOGLE_API_KEY` | `ai/gateway/__init__.py` | `""` (empty) | Google Gemini API authentication |
| `GOOGLE_BASE_URL` | `ai/gateway/__init__.py` | `https://generativelanguage.googleapis.com/v1beta` | Google Gemini API base URL |

### 2.3 Frontend

| Variable | Source File | Default Value | Purpose |
|----------|-------------|---------------|---------|
| `NEXT_PUBLIC_API_URL` | `next.config.mjs` | `http://localhost:8000` | Backend API URL for Next.js rewrites |

### 2.4 Docker / CI — Internal-Use Variables

| Variable | Source File | Value | Purpose |
|----------|-------------|-------|---------|
| `POSTGRES_DB` | `docker-compose.yml`, CI | `socialfarm` | PostgreSQL database name (Docker container) |
| `POSTGRES_USER` | `docker-compose.yml`, CI | `user` | PostgreSQL user (Docker container) |
| `POSTGRES_PASSWORD` | `docker-compose.yml`, CI | `password` | PostgreSQL password (Docker container) |
| `PYTHON_VERSION` | `render.yaml` | `3.11.0` | Python runtime version for Render |
| `NODE_ENV` | `Dockerfile.frontend` | `production` | Node environment mode |

---

## 3. Requirement vs Optional Classification

### Required (app crashes without these)

| Variable | Reason |
|----------|--------|
| `DATABASE_URL` | SQLAlchemy engine will fail to connect; all data operations break |
| `JWT_SECRET` | `change-me-in-production` default is insecure; JWT signing/verification will still work but is unsafe |
| `REDIS_URL` | Required by Celery for background tasks; app may partially function without it |
| `CORS_ORIGINS` | Frontend requests from allowed origins will be blocked |
| `NEXT_PUBLIC_API_URL` | Next.js rewrites will fall back to `localhost:8000`; production builds will proxy to wrong URL |

### Optional (safe defaults exist, or feature-specific)

| Variable | Default | Impact if Missing |
|----------|---------|-------------------|
| `HOST` | `0.0.0.0` | Still binds correctly |
| `PORT` | `8000` | Still listens on correct port |
| `DEBUG` | (empty = false) | No debug logging; no hot-reload |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Tokens expire in 30 minutes (reasonable default) |
| `OPENAI_API_KEY` | `""` | OpenAI provider not available; other providers may still work |
| `ANTHROPIC_API_KEY` | `""` | Anthropic provider not available |
| `GOOGLE_API_KEY` | `""` | Google provider not available |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | Uses default OpenAI URL |
| `ANTHROPIC_BASE_URL` | `https://api.anthropic.com/v1` | Uses default Anthropic URL |
| `GOOGLE_BASE_URL` | `https://generativelanguage.googleapis.com/v1beta` | Uses default Google URL |

---

## 4. Secret vs Public Classification

### Secrets (must never be committed, use secret management)

| Variable | Classification | Why |
|----------|---------------|-----|
| `DATABASE_URL` | **CRITICAL SECRET** | Contains database credentials; full connection string |
| `JWT_SECRET` | **CRITICAL SECRET** | Used to sign JWT tokens; compromise allows forgery |
| `REDIS_URL` | **SECRET** | Connection string to Redis (no auth by default but should be protected) |
| `OPENAI_API_KEY` | **SECRET** | Paid API key; cost exposure if leaked |
| `ANTHROPIC_API_KEY` | **SECRET** | Paid API key; cost exposure if leaked |
| `GOOGLE_API_KEY` | **SECRET** | Paid API key; cost exposure if leaked |

### Public (safe to commit, or NEXT_PUBLIC_ prefixed)

| Variable | Classification | Why |
|----------|---------------|-----|
| `NEXT_PUBLIC_API_URL` | **PUBLIC** | Intentionally exposed to client-side JS (Next.js convention) |
| `CORS_ORIGINS` | **PUBLIC** | URL list; no sensitive data |
| `HOST` | **PUBLIC** | Bind address; no sensitive data |
| `PORT` | **PUBLIC** | Port number; no sensitive data |
| `DEBUG` | **PUBLIC** | Boolean flag; no sensitive data |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | **PUBLIC** | Integer; no sensitive data |
| `OPENAI_BASE_URL` | **PUBLIC** | Base URL; no authentication data |
| `ANTHROPIC_BASE_URL` | **PUBLIC** | Base URL; no authentication data |
| `GOOGLE_BASE_URL` | **PUBLIC** | Base URL; no authentication data |
| `PYTHON_VERSION` | **PUBLIC** | Runtime version string |

---

## 5. Current Status (Set / Not Set)

### 5.1 Local Development

| Variable | Status | Where Set |
|----------|--------|-----------|
| `DATABASE_URL` | **NOT SET** — no `.env` file exists | `.env.example` only |
| `JWT_SECRET` | **NOT SET** — no `.env` file exists | `.env.example` only |
| `REDIS_URL` | **NOT SET** — no `.env` file exists | `.env.example` only |
| `CORS_ORIGINS` | **NOT SET** — no `.env` file exists | `.env.example` only |
| `HOST` | **NOT SET** — no `.env` file exists | `.env.example` only |
| `PORT` | **NOT SET** — no `.env` file exists | `.env.example` only |
| `DEBUG` | **NOT SET** — no `.env` file exists | `.env.example` only |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | **NOT SET** — no `.env` file exists | `.env.example` only |
| `NEXT_PUBLIC_API_URL` | **NOT SET** — no `.env` file exists | `.env.example` only |
| AI API keys | **NOT SET** — no `.env` file exists | `.env.example` (commented out) |

> **Note:** All variables use sensible defaults in code, so the app will run without any `.env` file, but with potentially incorrect values for a production environment.

### 5.2 Docker Compose

| Variable | Status | Value |
|----------|--------|-------|
| `DATABASE_URL` | **SET** | `postgresql://user:password@db:5432/socialfarm` |
| `REDIS_URL` | **SET** | `redis://redis:6379/0` |
| `JWT_SECRET` | **SET** (with fallback) | `${JWT_SECRET:-change-me-in-production}` |
| `CORS_ORIGINS` | **SET** | `http://localhost:3000,http://frontend:3000` |
| `DEBUG` | **SET** | `"false"` |
| `NEXT_PUBLIC_API_URL` | **SET** | `http://localhost:8000` |
| `HOST` | **NOT SET** | Uses code default `0.0.0.0` |
| `PORT` | **NOT SET** | Uses code default `8000` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | **NOT SET** | Uses code default `30` |
| AI API keys | **NOT SET** | Not configured in compose |

### 5.3 Render (render.yaml)

| Variable | Status | Value / Mechanism |
|----------|--------|-------------------|
| `DATABASE_URL` | **REQUIRES USER INPUT** | `sync: false` — user must set manually in Render dashboard |
| `REDIS_URL` | **REQUIRES USER INPUT** | `sync: false` — user must set manually in Render dashboard |
| `JWT_SECRET` | **AUTO-GENERATED** | `generateValue: true` — Render creates on first deploy |
| `CORS_ORIGINS` | **SET** | `"https://social-farm-ai.vercel.app,http://localhost:3000"` |
| `DEBUG` | **SET** | `"false"` |
| `PYTHON_VERSION` | **SET** | `"3.11.0"` |
| `HOST` | **NOT SET** | Not in render.yaml; Render provides `$PORT` via start command |
| `PORT` | **SET (implicitly)** | Used as `$PORT` in start command but not as env var in config |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | **NOT SET** | Not in render.yaml |
| `NEXT_PUBLIC_API_URL` | **NOT SET** | Not needed — Render only hosts backend |
| AI API keys | **NOT SET** | Not configured |

### 5.4 Vercel (vercel.json)

| Variable | Status | Notes |
|----------|--------|-------|
| `NEXT_PUBLIC_API_URL` | **MUST BE SET IN DASHBOARD** | Not specified in `vercel.json`; must be configured via Vercel project settings |
| All other frontend vars | N/A | No other frontend-specific env vars exist |

### 5.5 CI (GitHub Actions)

| Variable | Status | Value |
|----------|--------|-------|
| `DATABASE_URL` | **SET** | `postgresql://user:password@localhost:5432/socialfarm` |
| `REDIS_URL` | **SET** | `redis://localhost:6379/0` |
| `JWT_SECRET` | **SET** | `ci-test-secret` |
| `NEXT_PUBLIC_API_URL` | **SET** | `http://localhost:8000` |

---

## 6. NEXT_PUBLIC_ Prefix Convention Compliance

**Status: COMPLIANT**

The frontend uses exactly one public environment variable: `NEXT_PUBLIC_API_URL`.

- [x] It is used in `frontend/next.config.mjs` via `process.env.NEXT_PUBLIC_API_URL`
- [x] It is properly prefixed with `NEXT_PUBLIC_` so Next.js inlines it at build time for client-side access
- [x] It has a fallback default of `http://localhost:8000`
- [x] No non-`NEXT_PUBLIC_` prefixed variables are accessed in frontend source code (excluding `node_modules`)

**No further frontend environment variables** are used in the source (no `process.env.X` calls in `frontend/app/`).

---

## 7. Deployment Configuration Analysis

### 7.1 Render (render.yaml)

**File:** `/render.yaml`

```yaml
services:
  - type: web
    name: social-farm-ai-backend
    runtime: python
    plan: free
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: REDIS_URL
        sync: false
      - key: JWT_SECRET
        generateValue: true
      - key: CORS_ORIGINS
        value: "https://social-farm-ai.vercel.app,http://localhost:3000"
      - key: DEBUG
        value: "false"
      - key: PYTHON_VERSION
        value: "3.11.0"
    healthCheckPath: /health
    autoDeploy: true
```

**Issues Found:**

1. **Missing variables:** `HOST`, `PORT`, and `ACCESS_TOKEN_EXPIRE_MINUTES` are not declared.
   - `HOST` has a safe default (`0.0.0.0`)
   - `PORT` is passed via the start command (`$PORT`), so it is effectively set
   - `ACCESS_TOKEN_EXPIRE_MINUTES` falls back to `30` — acceptable but should be documented

2. **DATABASE_URL and REDIS_URL require manual setup:** `sync: false` means the user must create a Render PostgreSQL and Render Redis instance and paste the connection strings manually. This is expected but should be documented in a runbook.

3. **No AI provider keys:** If AI features are needed, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and/or `GOOGLE_API_KEY` must be added manually.

4. **Free plan limitations:** The `free` plan spins down after inactivity, which will cause cold starts. Redis is not available on the free plan; a paid plan (Starter at $7/mo) is required for Redis and to prevent spin-down.

**Positive:**
- `JWT_SECRET` is auto-generated via `generateValue: true` (best practice)
- `CORS_ORIGINS` correctly references the Vercel frontend URL
- Health check path is configured at `/health`
- `PYTHON_VERSION` is pinned to `3.11.0`

### 7.2 Vercel (vercel.json)

**Root file:** `/vercel.json`  
**Frontend file:** `/frontend/vercel.json`

Both are identical in content:

```json
{
  "framework": "nextjs",
  "regions": ["iad1"],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" },
        { "key": "Access-Control-Allow-Methods", "value": "GET,POST,PUT,DELETE,OPTIONS" },
        { "key": "Access-Control-Allow-Headers", "value": "Content-Type, Authorization" }
      ]
    }
  ]
}
```

**Issues Found:**

1. **No environment variables declared.** `NEXT_PUBLIC_API_URL` must be set in the Vercel Project Settings dashboard under Environment Variables. It should be set for both Preview and Production environments.

2. **Duplicate vercel.json:** Having both `/vercel.json` and `/frontend/vercel.json` with identical content is redundant. Vercel automatically detects the frontend/ directory as the project root when the root vercel.json sets `outputDirectory: "frontend/.next"`. The frontend copy can be removed.

3. **CORS headers are set at the Vercel edge level** for `/api/(.*)` paths. These will only apply if the frontend is serving its own API routes (Next.js API routes), not when proxying to the backend via Next.js rewrites. The backend's CORS middleware (`CORS_ORIGINS`) handles actual cross-origin requests to the backend.

4. **Root vercel.json has extra fields not in frontend copy:**
   - `buildCommand: "cd frontend && npm install && npm run build"`
   - `outputDirectory: "frontend/.next"`
   - `installCommand: "cd frontend && npm install"`

   These are necessary for the monorepo setup. The frontend copy lacks these, which could cause build issues if deployed from the frontend/ directory directly.

### 7.3 Docker Compose

**File:** `/docker-compose.yml`

**Issues Found:**

1. **JWT_SECRET has a weak fallback:** `${JWT_SECRET:-change-me-in-production}` — if `JWT_SECRET` is not set in the host environment, the default `change-me-in-production` is used, which is insecure.

2. **Hardcoded credentials for PostgreSQL:** `user`/`password` are hardcoded in the compose file. This is acceptable for local development but should be overrideable via environment variables.

3. **Missing HOST/PORT:** Not set in compose; backend uses code defaults. The Dockerfile.backend CMD hardcodes `--host 0.0.0.0 --port 8000`, so these env vars are effectively ignored in Docker.

4. **No AI provider keys:** Not configured in compose.

5. **Frontend NEXT_PUBLIC_API_URL is hardcoded** to `http://localhost:8000`. This works for local Docker but would need to change for other environments.

6. **No volume for frontend:** Frontend has no volume mount, so code changes require a rebuild. This is acceptable for production but inconvenient for development.

### 7.4 GitHub Actions CI

**File:** `/github/workflows/test.yml`

**Status: GOOD**

- Backend tests set `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`
- Frontend build sets `NEXT_PUBLIC_API_URL`
- PostgreSQL service container is properly configured
- All CI environment variables use safe, throwaway values

---

## 8. Cross-Cutting Issues

### 8.1 Duplicate Codebase: `api/app/` vs `backend/app/`

The directory `/api/app/` contains an almost exact copy of `/backend/app/` with its own `main.py`, `core/security.py`, etc. Both reference the same environment variables. This creates a maintenance burden — any env var changes must be made in both locations.

**Risk:** If one copy is updated and the other is not, deployments from the outdated copy may break or behave differently.

### 8.2 Docker Backend Ignores HOST/PORT Env Vars

`Dockerfile.backend` ends with:
```
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

This hardcoded CMD bypasses the `HOST` and `PORT` environment variables read by `main.py`'s `if __name__ == "__main__"` block (lines 101-111). The `uvicorn.run()` call is never executed in Docker because the CMD invokes uvicorn directly.

**Impact:** Setting `HOST` or `PORT` env vars has no effect on Docker deployments.

### 8.3 No `.env` File in Repository

The `.gitignore` correctly excludes all `*.env` files, and no `.env` file exists in the repo. This is correct behavior — `.env` files should be local-only. However, there is no setup script to copy `.env.example` to `.env`.

### 8.4 Overlapping Gitignore Patterns

The `.gitignore` includes:
```
*.env
*.env.local
*.env.development
*.env.production
*.env.test
```

The first pattern `*.env` already matches all the others (e.g., `foo.env.local` matches `*.env`). The additional patterns are redundant.

### 8.5 `api/app/` Missing AI Gateway

The `/api/app/` directory does not contain the `services/ai/gateway/` module. If the `/api/` path is used as a deployment entry point, AI provider functionality will be unavailable.

### 8.6 No Environment Validation at Startup

Neither the backend nor frontend validates that required environment variables are set at startup. The app may start with invalid defaults and fail later with confusing errors.

---

## 9. Deployment-Specific Recommendations

### 9.1 Local Development

1. **Copy `.env.example` to `.env`:**
   ```bash
   cp .env.example .env
   ```
   (Consider adding a `setup.sh` or `npm run setup` script)

2. **Generate a real JWT secret:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Set up local PostgreSQL and Redis** (or use `docker-compose up db redis`)

### 9.2 Docker Compose

1. **Add `HOST` and `PORT` to compose** for clarity, even if Dockerfile ignores them.

2. **Fix Dockerfile.backend** to use environment variables:
   ```
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
   Change to use `$HOST` and `$PORT` or keep hardcoded and remove env var reads from `main.py`.

3. **Remove the weak JWT fallback** or add a startup check that warns if the value is the default.

### 9.3 Render (Production Backend)

1. **What to set in Render Dashboard** (after deployment):
   - Create a Render PostgreSQL instance → copy its `Internal Connection String` → set as `DATABASE_URL`
   - Create a Render Redis instance → copy its `Internal Connection String` → set as `REDIS_URL`
   - `JWT_SECRET` — already auto-generated by Render (`generateValue: true`)
   - (Optional) Set AI provider keys if using AI features

2. **Add to `render.yaml`** (nice-to-have):
   ```yaml
   - key: ACCESS_TOKEN_EXPIRE_MINUTES
     value: "60"
   ```

3. **Upgrade from Free plan:** The free plan does not include Redis and spins down after inactivity. For production:
   - **Starter plan** ($7/mo) — includes Redis, no spin-down, 512 MB RAM
   - **Professional plan** ($20/mo) — more RAM, better performance

4. **Consider adding a Render Cron Job** to keep the free instance warm (hit `/health` every 10 minutes).

### 9.4 Vercel (Production Frontend)

1. **Set `NEXT_PUBLIC_API_URL` in Vercel Dashboard:**
   - Project → Settings → Environment Variables
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://social-farm-ai-backend.onrender.com` (or your Render backend URL)
   - Apply to: Production, Preview, Development

2. **Remove `frontend/vercel.json`** — the root `vercel.json` is sufficient.

3. **Add `NEXT_PUBLIC_API_URL` to root `vercel.json`** (optional, for documentation):
   ```json
   {
     "env": {
       "NEXT_PUBLIC_API_URL": "https://social-farm-ai-backend.onrender.com"
     }
   }
   ```
   Note: This would make the URL visible in the config file; Vercel dashboard is more secure for production values.

### 9.5 GitHub Actions CI

The CI configuration is already correct. No changes needed.

---

## 10. Placeholder Generation

Below are ready-to-use placeholder values for local development and testing. **Never use these in production.**

### 10.1 Local `.env` File Content

Create a file named `.env` at the project root with the following content:

```bash
# =============================================================================
# Social Farm AI OS — Local Development Environment
# =============================================================================
# Generated by ENVIRONMENT_CONFIGURATION_REPORT.md
# WARNING: These values are for local development ONLY.
# =============================================================================

# ---------- Database ----------
DATABASE_URL=postgresql://user:password@localhost:5432/socialfarm

# ---------- Redis ----------
REDIS_URL=redis://localhost:6379/0

# ---------- JWT / Auth ----------
JWT_SECRET=dev-jwt-secret-do-not-use-in-production-change-me
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ---------- Backend ----------
HOST=0.0.0.0
PORT=8000
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001

# ---------- Frontend ----------
NEXT_PUBLIC_API_URL=http://localhost:8000

# ---------- AI Providers (optional — uncomment to enable) ----------
# OPENAI_API_KEY=sk-your-key-here
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# GOOGLE_API_KEY=your-google-key-here
```

### 10.2 CI Placeholder Values

For CI/CD pipeline configuration:

| Variable | Placeholder Value |
|----------|-------------------|
| `DATABASE_URL` | `postgresql://user:password@localhost:5432/socialfarm_test` |
| `REDIS_URL` | `redis://localhost:6379/1` |
| `JWT_SECRET` | `ci-test-secret-insecure` |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` |

### 10.3 Production Render Dashboard Values

For Render environment variables (set via Dashboard, not in yaml):

| Variable | Example Production Value |
|----------|--------------------------|
| `DATABASE_URL` | `postgresql://user:XXXX@social-farm-ai-db.internal:5432/socialfarm` |
| `REDIS_URL` | `rediss://:XXXX@social-farm-ai-redis.internal:6379` |
| `JWT_SECRET` | (auto-generated by Render) |
| `OPENAI_API_KEY` | `sk-proj-XXXX` (if using OpenAI) |

### 10.4 Production Vercel Dashboard Values

| Variable | Example Production Value |
|----------|--------------------------|
| `NEXT_PUBLIC_API_URL` | `https://social-farm-ai-backend.onrender.com` |

---

## Appendix A: Environment Variable Reference Table

| Variable | Backend | Frontend | Docker | Render | Vercel | CI | Required | Secret | Has Default |
|----------|---------|----------|--------|--------|--------|----|----------|--------|-------------|
| `DATABASE_URL` | YES | - | YES | sync:false | - | YES | YES | YES | YES |
| `JWT_SECRET` | YES | - | YES | auto-gen | - | YES | YES | YES | YES |
| `REDIS_URL` | (celery) | - | YES | sync:false | - | YES | YES | YES | YES |
| `CORS_ORIGINS` | YES | - | YES | SET | - | - | YES | NO | YES |
| `HOST` | YES | - | - | - | - | - | NO | NO | YES |
| `PORT` | YES | - | - | ($PORT) | - | - | NO | NO | YES |
| `DEBUG` | YES | - | YES | SET | - | - | NO | NO | YES |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | YES | - | - | - | - | - | NO | NO | YES |
| `NEXT_PUBLIC_API_URL` | - | YES | YES | - | DASHBOARD | YES | YES | NO | YES |
| `OPENAI_API_KEY` | YES | - | - | - | - | - | NO | YES | NO |
| `OPENAI_BASE_URL` | YES | - | - | - | - | - | NO | NO | YES |
| `ANTHROPIC_API_KEY` | YES | - | - | - | - | - | NO | YES | NO |
| `ANTHROPIC_BASE_URL` | YES | - | - | - | - | - | NO | NO | YES |
| `GOOGLE_API_KEY` | YES | - | - | - | - | - | NO | YES | NO |
| `GOOGLE_BASE_URL` | YES | - | - | - | - | - | NO | NO | YES |
| `PYTHON_VERSION` | - | - | - | SET | - | - | NO | NO | N/A |

**Key:** `YES` = referenced in code/config | `-` = not used | `SET` = hardcoded value | `sync:false` = requires manual entry | `auto-gen` = auto-generated | `DASHBOARD` = must be set in platform dashboard

---

## Appendix B: Files Referencing Each Environment Variable

| Variable | Files |
|----------|-------|
| `DATABASE_URL` | `backend/app/db/session.py`, `.github/workflows/test.yml`, `docker-compose.yml`, `render.yaml`, `.env.example` |
| `JWT_SECRET` | `backend/app/core/security.py`, `api/app/core/security.py`, `docker-compose.yml`, `render.yaml`, `.github/workflows/test.yml`, `.env.example` |
| `REDIS_URL` | `docker-compose.yml`, `render.yaml`, `.github/workflows/test.yml`, `.env.example` |
| `CORS_ORIGINS` | `backend/app/main.py`, `api/app/main.py`, `docker-compose.yml`, `render.yaml`, `.env.example` |
| `HOST` | `backend/app/main.py` (line 102), `api/app/main.py` (line 102), `.env.example` |
| `PORT` | `backend/app/main.py` (line 103), `api/app/main.py` (line 103), `.env.example` |
| `DEBUG` | `backend/app/main.py` (lines 72, 104), `api/app/main.py` (lines 72, 104), `docker-compose.yml`, `render.yaml`, `.env.example` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `backend/app/core/security.py` (line 14), `api/app/core/security.py` (line 14), `.env.example` |
| `NEXT_PUBLIC_API_URL` | `frontend/next.config.mjs` (lines 20-21), `docker-compose.yml`, `.github/workflows/test.yml`, `.env.example` |
| `OPENAI_API_KEY` | `backend/app/services/ai/gateway/__init__.py` (line 152), `.env.example` |
| `OPENAI_BASE_URL` | `backend/app/services/ai/gateway/__init__.py` (line 156) |
| `ANTHROPIC_API_KEY` | `backend/app/services/ai/gateway/__init__.py` (line 163), `.env.example` |
| `ANTHROPIC_BASE_URL` | `backend/app/services/ai/gateway/__init__.py` (line 167) |
| `GOOGLE_API_KEY` | `backend/app/services/ai/gateway/__init__.py` (line 174), `.env.example` |
| `GOOGLE_BASE_URL` | `backend/app/services/ai/gateway/__init__.py` (line 178) |

---

*Report generated by the Environment Engineer agent of the Social Farm AI Multi-Agent System.*
