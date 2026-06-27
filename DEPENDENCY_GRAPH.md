# DEPENDENCY GRAPH — Implementation Order

**Date:** June 26, 2026  
**Source:** Verified import analysis of `backend/` and `frontend/`  
**Rule:** No module implemented before its dependencies are satisfied.

---

## TIER 0 — Foundation (No Dependencies)

| # | Module | Files | Dependency | Implemented? |
|---|--------|-------|------------|--------------|
| 0.1 | `app.core.security` | `security.py` | None | ✅ Yes (21 lines) |
| 0.2 | `app.db.session` | `session.py` | None | ✅ Yes (19 lines) |
| 0.3 | `app.db.__init__` | `__init__.py` | None | ❌ **Zero bytes** |
| 0.4 | `app.models.base` | Base declarative class | None | ✅ (in `models/__init__.py`) |

---

## TIER 1 — Domain Models

Dependency: `models.base`

| # | Module | Files | Lines | Status |
|---|--------|-------|-------|--------|
| 1.1 | `models/ai/` | agent, execution, memory, metrics, prompt, provider, task, workflow | 1,695 | ✅ Done |
| 1.2 | `models/strategy/` | audience, campaign, competitor, forecast, metrics, opportunity, plan, platform, recommendation, risk, strategy, theme | 1,505 | ✅ Done |
| 1.3 | `models/brand.py` | Brand model | 616 | ✅ Done (1 stub at L101) |
| 1.4 | `models/rbac.py` | RBAC model | 215 | ✅ Done |
| 1.5 | `models/research.py` | 23 + 4 entities | 1,331 | ✅ Done |
| 1.6 | `models/user.py` | User model | 13 | ✅ Done |

---

## TIER 2 — Pydantic Schemas

Dependency: Corresponding models

| # | Module | Depends On | Status |
|---|--------|------------|--------|
| 2.1 | `schemas/brand.py` (715 lines) | models.brand | ✅ Done |
| 2.2 | `schemas/rbac.py` (230 lines) | models.rbac | ✅ Done |
| 2.3 | **`schemas/research.py`** (41KB null) | **models.research** | ❌ **Null-filled** |
| 2.4 | `schemas/user.py` (14 lines) | models.user | ✅ Done |

---

## TIER 3 — Core Services

Dependency: `models.base`, `models.*`

| # | Module | Lines | Depends On | Status |
|---|--------|-------|------------|--------|
| 3.1 | `services/rbac.py` | 641 | models.rbac, models | ⚠️ **2 pass stubs** |
| 3.2 | `services/ai/registry/` | 394 | models.ai | ⚠️ **return None (L308)** |
| 3.3 | `services/ai/router/` | 289 | models.ai | ⚠️ **TODO: load from DB** |
| 3.4 | `services/ai/prompts/` | 391 | models.ai | ⚠️ **return None (L257), TODO** |
| 3.5 | `services/ai/memory/` | 316 | models.ai | ⚠️ **return None (L255), TODO** |
| 3.6 | `services/ai/quality/` | 423 | models.ai | ✅ Done |

---

## TIER 4 — AI Gateway & Workflow

Dependency: Tier 3 services

| # | Module | Lines | Depends On | Status |
|---|--------|-------|------------|--------|
| 4.1 | `services/ai/gateway/` | 317 | router, registry | ⚠️ **TODO: implement provider calls** |
| 4.2 | `services/ai/workflow/` | 417 | models.ai.workflow | ⚠️ **5 TODO agent stubs** |
| 4.3 | `services/ai/orchestrator/` | 604 | gateway, memory, prompts, quality, registry, router, workflow | ⚠️ **Depends on stubs** |

---

## TIER 5 — API Layer

Dependency: Security + Schemas + Services

| # | Module | Lines | Status |
|---|--------|-------|--------|
| 5.1 | `api/auth/` (endpoints.py) | 26 | ✅ Done |
| 5.2 | `api/workspaces/` (endpoints.py) | 262 | ✅ Done |
| 5.3 | `api/organizations/` (endpoints.py) | 428 | ✅ Done |
| 5.4 | `api/ai/` (__init__.py) | 428 | ⚠️ **Depends on stub services** |
| 5.5 | `api/strategy/` (__init__.py) | 491 | ✅ Done |
| 5.6 | **`api/research/`** (2 files) | **1 + null** | ❌ **Null-filled** |

---

## TIER 6 — Domain Services (Engine Layer)

| # | Module | Depends On | Status |
|---|--------|------------|--------|
| 6.1 | `services/strategy/*` (8 files, 4,296 lines) | models.strategy + services.ai | ✅ Done |
| 6.2 | **`services/research/*`** | **models.research + services.ai** | ❌ **Missing entirely** |
| 6.3 | `services/trend/*` | models.trend + services.ai | ❌ **Missing entirely** |
| 6.4 | `services/publishing/*` | models.strategy + services.ai | ❌ **Missing** |
| 6.5 | `services/analytics/*` | models.strategy + services.ai | ❌ **Missing** |

---

## TIER 7 — Frontend Pages

Dependency: Backend API

| # | Module | Files | Status |
|---|--------|-------|--------|
| 7.1 | `frontend/app/login/` | 1 page | ✅ Done |
| 7.2 | `frontend/app/register/` | 1 page | ✅ Done |
| 7.3 | `frontend/app/ai/` | 4 pages (ai, agents, health, models) | ✅ Done |
| 7.4 | `frontend/app/strategy/` | 4 pages (strategy, calendar, campaigns, opportunities) | ✅ Done |
| 7.5 | **`frontend/app/research/`** | **10 pages planned, 4+3 null-filled, 6 empty** | ❌ **Broken** |
| 7.6 | `frontend/app/trends/` | — | ❌ **Does not exist** |

---

## IMPLEMENTATION ORDER

Based on the dependency graph, modules MUST be implemented in this exact sequence:

### Wave A — Fix Foundation Stubs (Tiers 0-3)
```
 1. app.db.__init__               # Zero-byte → session factory
 2. services.rbac                  # Fix 2 pass stubs
 3. services.ai.registry           # Fix return None (L308)
 4. services.ai.router             # Fix TODO (L68)
 5. services.ai.prompts            # Fix return None (L257), Fix TODO (L88)
 6. services.ai.memory             # Fix return None (L255), Fix TODO (L86, L184, L270)
```

### Wave B — Fix Gateway & Workflow (Tier 4)
```
 7. services.ai.gateway            # Implement real AI provider calls
 8. services.ai.workflow           # Wire 5 agent connections
```

### Wave C — Research Engine (Tiers 2, 5, 6, 7)
```
 9. services/research/*            # NEW: 8 service files (aggregator, extractor, etc.)
10. schemas/research.py            # Rewrite null-filled → 27 Pydantic schemas
11. api/research/__init__.py       # Fix router setup
12. api/research/endpoints.py      # Rewrite null-filled → full CRUD
13. frontend/stores/research.ts    # Rewrite null-filled
14. frontend/app/research/*        # Rewrite 7 null-filled files + create 6 missing pages
```

### Wave D — Trend Engine (Tiers 1, 6, 5, 7)
```
15. models/trend/*                 # NEW: 8+ model types
16. services/trend/*               # NEW: 7+ service files
17. api/trend/*                    # NEW: 9+ endpoint groups
18. frontend/trends/*              # NEW: 6+ pages
```

### Wave E — Remaining Engines
```
19. Brand Context Engine
20. Publishing Engine
21. Analytics Engine
22. Content Planner
```

### Wave F — Tests & Quality
```
23. Test files for all modules
24. Documentation for all modules
25. TODO-only spec files
```

---

## VERIFIED MODULE LINES COUNT

| Area | Lines of Code | Status |
|------|---------------|--------|
| Models | 4,859 | ✅ 98% complete |
| Schemas | 960 | ⚠️ 50% (research null) |
| Services | 5,646 | ⚠️ 60% (stubs + missing) |
| API | 1,636 | ⚠️ 50% (research null) |
| Frontend (TSX/TS) | 2,996 | ⚠️ 50% (research null) |
| Tests | 847 | ❌ 10% |
| **Total backend** | **13,101** | ⚠️ |
| **Total frontend** | **~3,000** | ⚠️ |

**Grand total: ~16,000 lines** across 97+ source files.
