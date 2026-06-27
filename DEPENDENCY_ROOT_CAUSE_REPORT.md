# Dependency Root Cause Report — Render Build Failure

## Build Failure Summary

**Service:** `social-farm-ai-backend`
**Platform:** Render (free tier)
**Build Log Timestamp:** 2026-06-27T09:40:51Z
**Status:** Build failed at `pip install` step

---

## Render Build Log (Key Excerpt)

```
Collecting fastapi==0.100.0 (from -r requirements.txt (line 1))
Collecting pydantic==2.0.0 (from pydantic[email]==2.0.0->-r requirements.txt (line 5))
...
ERROR: Cannot install -r requirements.txt (line 1) and pydantic==2.0.0
because these package versions have conflicting dependencies.

The conflict is caused by:
    The user requested pydantic==2.0.0
    fastapi 0.100.0 depends on pydantic!=1.8, !=1.8.1, !=2.0.0, !=2.0.1, <3.0.0 and >=1.7.4
```

---

## Root Cause

**FastAPI 0.100.0 explicitly excludes `pydantic==2.0.0`** via a `!=2.0.0` constraint in its dependency specification.

The `backend/requirements.txt` pinned:
```
fastapi==0.100.0
pydantic[email]==2.0.0
```

This is an **irresolvable conflict**: pip cannot install both packages as specified because FastAPI 0.100.0 declares `pydantic!=2.0.0`.

### Why FastAPI 0.100.0 Excludes Pydantic 2.0.0

FastAPI 0.100.0 was the first release to add Pydantic v2 support. However, Pydantic 2.0.0 had critical bugs that caused failures in FastAPI's validation layer. The FastAPI team added `!=2.0.0, !=2.0.1` to force users to upgrade to Pydantic 2.0.2+ (which contained the fixes).

### Why This Was Not Caught Locally

- The dependency versions were set manually without running `pip install` to verify resolution
- No CI pipeline step validated dependency resolution before deployment
- Local development may have used cached/pre-installed packages

---

## Additional Issues Identified

### 1. Python Version Mismatch

**render.yaml** specified `PYTHON_VERSION: "3.11.0"` as an environment variable, but this is a **runtime-only** variable. Render uses the `runtime` field for build-time Python selection.

**Result:** Render used Python 3.14.3 (default) instead of 3.11.0.

### 2. Poetry Detection Interference

A `pyproject.toml` at the repository root (containing only Poetry metadata, no dependencies) triggered Render to detect the project as Poetry-based:

```
Using Poetry version 2.1.3 (default)
```

While the `buildCommand` used `pip install`, Poetry detection could interfere with dependency resolution or package installation.

### 3. Render Deployed from Stale Commit

Render checked out commit `e560f5a` — the commit **before** the dependency fix (`0f9a443`). This indicates the Render deploy was triggered before the fix was pushed.

---

## Fix Applied (Commit `c19fddf`)

### Dependency Fix (from commit `0f9a443`)

Updated to stable, compatible versions:

| Package | Before | After |
|---------|--------|-------|
| fastapi | 0.100.0 | 0.115.0 |
| pydantic[email] | 2.0.0 | 2.9.2 |
| pydantic-settings | 2.0.0 | 2.5.2 |
| uvicorn[standard] | 0.23.0 | 0.30.6 |
| sqlalchemy | 2.0.0 | 2.0.35 |
| alembic | 1.11.0 | 1.13.2 |

### Render Configuration Fix (commit `c19fddf`)

| Change | Before | After |
|--------|--------|-------|
| `runtime` | `python` | `python-3.11.0` |
| `pyproject.toml` | Present (triggers Poetry) | Deleted |
| `.python-version` | Missing | Created (`3.11.0`) |
| `buildCommand` | `pip install -r requirements.txt` | `pip install --upgrade pip && pip install -r requirements.txt` |
| `PYTHON_VERSION` envVar | Set to `3.11.0` (runtime-only) | Removed (handled by runtime + .python-version) |

---

## Files Inspected

| File | Purpose |
|------|---------|
| `backend/requirements.txt` | Backend dependencies (Render reads this) |
| `requirements.txt` | Root dependencies (Vercel/serverless) |
| `render.yaml` | Render deployment configuration |
| `pyproject.toml` | Poetry metadata (removed) |
| `Dockerfile.backend` | Docker build (not used by Render) |
| `backend/app/main.py` | FastAPI entry point |
| `backend/app/core/config.py` | pydantic-settings usage |
| `backend/app/schemas/base.py` | Pydantic v2 syntax |

## Files Modified

| File | Change |
|------|--------|
| `render.yaml` | Fixed runtime, buildCommand, removed PYTHON_VERSION envVar |
| `.python-version` | Created with `3.11.0` |
| `pyproject.toml` | Deleted |

## Files NOT Modified

| File | Reason |
|------|--------|
| `backend/requirements.txt` | Already correct from commit `0f9a443` |
| `requirements.txt` | Already correct from commit `0f9a443` |

---

## Conclusion

**Root cause identified:** FastAPI 0.100.0 excludes `pydantic==2.0.0` via `!=2.0.0` constraint. Pinned versions created an irresolvable conflict.

**Minimum fix applied:**
1. Dependency versions updated to compatible set (fastapi 0.115.0 + pydantic 2.9.2) — already in repo
2. Render build configuration fixed (Python version, Poetry detection) — commit `c19fddf`

**Status:** ✅ Root cause identified and fixed
