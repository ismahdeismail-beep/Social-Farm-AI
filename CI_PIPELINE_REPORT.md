# CI/CD Pipeline Audit Report

**Date:** 2026-06-27
**Repository:** Social-Farm-AI
**Auditor:** CI/CD Engineer

---

## 1. Current CI/CD Configuration

### Workflow Files

Only **one** workflow file exists:

| File | Path |
|------|------|
| `test.yml` | `.github/workflows/test.yml` |

No other workflow files (e.g., deploy.yml, release.yml, security-scan.yml) are present.

### Workflow Triggers

The workflow `CI — Lint, Type Check & Build` triggers on:

| Event | Branches |
|-------|----------|
| `push` | `main`, `develop` |
| `pull_request` | `main` |

### Defined Jobs

Two parallel jobs:

| Job | Runs On | Working Directory |
|-----|---------|-------------------|
| `backend` | `ubuntu-latest` | `backend/` |
| `frontend` | `ubuntu-latest` | `frontend/` |

---

## 2. Checks Performed

### Backend (`backend/`)

| Step | Tool / Action | Details |
|------|--------------|---------|
| Checkout | `actions/checkout@v4` | |
| Setup Python | `actions/setup-python@v5` | Python 3.11, pip caching enabled |
| Install deps | `pip install -r requirements.txt` | |
| Lint | `ruff check . --exit-zero` | Ruff linting (never fails due to `--exit-zero`) |
| Type check | `mypy app --ignore-missing-imports \|\| true` | Mypy type checking (failures suppressed) |
| Run tests | `pytest -v --cov=app --cov-report=term-missing \|\| true` | Pytest with coverage (failures suppressed) |

**Service containers:** PostgreSQL 15 with health check.
**No Redis service** is configured, despite `REDIS_URL` being set in the test environment.

### Frontend (`frontend/`)

| Step | Tool / Action | Details |
|------|--------------|---------|
| Checkout | `actions/checkout@v4` | |
| Setup Node | `actions/setup-node@v4` | Node.js 20, npm caching enabled |
| Install deps | `npm install` | |
| Lint | `npm run lint \|\| true` | ESLint via Next.js (failures suppressed) |
| Type check | `npx tsc --noEmit \|\| true` | TypeScript type checking (failures suppressed) |
| Build | `npm run build` | Next.js production build |

**No artifacts** are produced or uploaded from the build step.

---

## 3. Version Verification

### Python Version

| Source | Specified Version | Match? |
|--------|-------------------|--------|
| `.github/workflows/test.yml` | `"3.11"` | Yes |
| `backend/runtime.txt` | `python-3.11.0` | Yes |
| `Dockerfile.backend` | `python:3.11-slim` | Yes |
| `render.yaml` | `"3.11.0"` | Yes |

**Verdict:** Consistent across all files.

### Node.js Version

| Source | Specified Version | Match? |
|--------|-------------------|--------|
| `.github/workflows/test.yml` | `"20"` | Yes |
| `Dockerfile.frontend` | `node:20-alpine` | Yes |
| `frontend/package.json` | `@types/node: ^20` | Yes |

**Verdict:** Consistent across all files.

---

## 4. Path Verification

| Workflow Path | Actual Directory Exists? | Correct? |
|--------------|--------------------------|----------|
| `backend/` (working-directory) | Yes | Correct |
| `backend/requirements.txt` (cache-dependency-path) | Yes | Correct |
| `frontend/` (working-directory) | Yes | Correct |
| `frontend/package.json` (cache-dependency-path) | Yes | Correct |

**Verdict:** All paths referenced in the workflow match the actual repository structure.

---

## 5. Issues Found

### 🔴 Critical Issues

#### Issue 1: All quality checks can silently pass despite failures
**Severity:** HIGH

Every meaningful check in the pipeline uses `|| true` (or `--exit-zero`), which causes the step to **never fail**:

- Backend lint: `ruff check . --exit-zero` — always returns exit code 0
- Backend type check: `mypy app --ignore-missing-imports || true` — failures swallowed
- Backend tests: `pytest -v --cov=app --cov-report=term-missing || true` — failures swallowed
- Frontend lint: `npm run lint || true` — failures swallowed
- Frontend type check: `npx tsc --noEmit || true` — failures swallowed

This means the CI pipeline **provides no real quality gating**. Broken code, lint errors, type errors, and failing tests will all pass CI undetected.

#### Issue 2: Missing Redis service for backend tests
**Severity:** HIGH

The backend test environment sets `REDIS_URL: redis://localhost:6379/0`, but no Redis service container is defined in the workflow. Only PostgreSQL is configured as a service. If any backend tests attempt to connect to Redis, they will fail (or hang until timeout).

### 🟡 Medium Issues

#### Issue 3: No build artifacts are produced
**Severity:** MEDIUM

The frontend `npm run build` step runs successfully, but the produced `.next/` build output is not uploaded as an artifact. This means:
- The CI cannot be used for deployment directly
- No build artifacts are inspectable after the run
- No way to download and verify the built output

#### Issue 4: No deployment pipeline exists
**Severity:** MEDIUM

There is no deploy job or deployment workflow. The pipeline only performs CI checks (and poorly, due to Issue 1). There is no automated deployment to:
- Staging / preview environments
- Production (Render for backend, Vercel for frontend)

### 🟢 Low Issues

#### Issue 5: No matrix testing
**Severity:** LOW

The workflow only tests a single Python version (3.11) and a single Node.js version (20). A matrix strategy would provide confidence across multiple runtime versions.

#### Issue 6: Ruff configuration uses deprecated format
**Severity:** LOW

The `ruff.toml` uses `[tool.ruff]` as the table header. In newer versions of Ruff (>=0.2.0), this should be split into `[lint]`, `[format]`, etc. The current config is valid for the pinned version (`ruff==0.0.280`) but will break on upgrade.

#### Issue 7: No security scanning
**Severity:** LOW

The pipeline does not include any security-related checks such as:
- Dependency vulnerability scanning (e.g., `pip-audit`, `npm audit`, or GitHub Dependabot)
- SAST/static analysis security scanning
- Secret detection

#### Issue 8: No caching for pip packages across runs
**Severity:** LOW

While the workflow specifies `cache: "pip"`, the cache key is tied to `backend/requirements.txt`. If only development dependencies change (e.g., adding a linting tool), the cache is invalidated entirely. Consider splitting production and development requirements for more granular caching.

---

## 6. Recommendations

### Immediate (High Priority)

| # | Recommendation | Details |
|---|---------------|---------|
| 1 | **Remove `|| true` from all check steps** | Each of `ruff`, `mypy`, `pytest`, `npm run lint`, `npx tsc --noEmit` must be allowed to fail the pipeline when they detect real issues. |
| 2 | **Remove `--exit-zero` from ruff** | Replace with `ruff check .` so lint violations cause pipeline failures. |
| 3 | **Add Redis service container** | Add a `redis` service to the backend job identical to the PostgreSQL service setup. |

### Short-term (Medium Priority)

| # | Recommendation | Details |
|---|---------------|---------|
| 4 | **Upload frontend build as artifact** | Add `actions/upload-artifact@v4` step after `npm run build` to archive `.next/` and `public/` for inspection and deployment. |
| 5 | **Add deployment jobs** | Create separate deploy jobs (with `needs: [backend, frontend]`) that deploy to Render (backend) and Vercel (frontend), gated on the `main` branch. |
| 6 | **Add dependabot configuration** | Create `.github/dependabot.yml` to automate dependency updates for `pip` and `npm`. |

### Long-term (Low Priority)

| # | Recommendation | Details |
|---|---------------|---------|
| 7 | **Add matrix build strategy** | Test against Python 3.10, 3.11, 3.12 and Node.js 18, 20, 22. |
| 8 | **Add security scanning** | Integrate `pip-audit` / `npm audit` steps and consider GitHub CodeQL or Trivy scanning. |
| 9 | **Add PR preview deployments** | For pull requests, deploy preview environments (Vercel for frontend, ephemeral Render instances for backend). |
| 10 | **Add concurrency / cancel-in-progress** | Configure `concurrency` on the workflow to auto-cancel stale runs on the same branch/PR. |
| 11 | **Update ruff.toml to modern format** | Migrate to `[lint]` section format for compatibility with future ruff versions. |
| 12 | **Add notification step** | Notify Slack/Discord on pipeline failures so the team can respond quickly. |

---

## 7. Summary

| Metric | Status |
|--------|--------|
| Workflow files found | 1 (`test.yml`) |
| Trigger configuration | `push` (main, develop), `PR` (main) |
| Backend CI checks | Lint, type check, test (all suppressed) |
| Frontend CI checks | Lint, type check, build |
| Caching configured | Yes (pip + npm) |
| Artifacts produced | No |
| Deployment automated | No |
| Python version consistency | ✅ All reference 3.11 |
| Node.js version consistency | ✅ All reference 20 |
| Path correctness | ✅ All paths valid |

**Overall Assessment:** The CI pipeline skeleton is well-structured with separate backend and frontend jobs, correct working directories, and reasonable tool choices. However, the decision to suppress all check failures (`|| true`, `--exit-zero`) renders the pipeline **effectively a no-op for quality gating**. The missing Redis service will cause runtime test failures, and the lack of artifact production or deployment means the pipeline has no path to production.

The pipeline needs immediate fixes to become a meaningful quality gate, followed by deployment automation to complete the CI/CD lifecycle.
