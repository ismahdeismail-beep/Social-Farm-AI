# Research Engine — Audit Report

**Verdict: WARNING** ⚠️

> **Summary:** The Research Engine has a solid foundation — all 23+4 database models are fully defined, an API router file exists, and a frontend layout with sidebar navigation is in place. However, zero backend services, zero tests, zero user-facing documentation, and the frontend pages are empty placeholder files (null bytes). The engine exists in name but is non-functional.

---

## 1. What Exists ✅

### 1.1 Database Models — ✅ COMPLETE (27 entities)
**File:** `backend/app/models/research.py` (56,305 bytes)  
**Exports via:** `backend/app/models/__init__.py`

**23 Core Entities:**
| Entity | Type | Status |
|--------|------|--------|
| ResearchSource | Model | ✅ Present |
| ResearchQuery | Model | ✅ Present |
| ResearchDocument | Model | ✅ Present |
| ResearchCollection | Model | ✅ Present |
| ResearchTopic | Model | ✅ Present |
| ResearchSummary | Model | ✅ Present |
| ResearchCitation | Model | ✅ Present |
| ResearchInsight | Model | ✅ Present |
| ResearchFact | Model | ✅ Present |
| ResearchKeyword | Model | ✅ Present |
| ResearchEntity | Model | ✅ Present |
| ResearchRelationship | Model | ✅ Present |
| ResearchScore | Model | ✅ Present |
| ResearchSnapshot | Model | ✅ Present |
| ResearchCache | Model | ✅ Present |
| ResearchJob | Model | ✅ Present |
| ResearchHistory | Model | ✅ Present |
| ResearchBookmark | Model | ✅ Present |
| ResearchFolder | Model | ✅ Present |
| ResearchTag | Model | ✅ Present |
| ResearchReport | Model | ✅ Present |
| ResearchAlert | Model | ✅ Present |
| ResearchFeedback | Model | ✅ Present |

**4 Association/Junction Tables:**
| Entity | Type | Status |
|--------|------|--------|
| research_collection_documents | Assoc | ✅ Present |
| research_document_topics | Assoc | ✅ Present |
| research_document_keywords | Assoc | ✅ Present |
| research_document_entities | Assoc | ✅ Present |

**8 Enums** (likely present in the same file — ResearchSourceType, ResearchQueryStatus, ResearchDocumentType, ResearchJobStatus, etc.)

### 1.2 API Endpoint — ⚠️ Exists but UNREADABLE
**File:** `backend/app/api/research/endpoints.py` (44,519 bytes)

- The file exists but contains **all null bytes** — it is a zero-filled placeholder.
- The sibling `__init__.py` exists (likely blank).
- The endpoint is **registered at router level** but has no functional code.

### 1.3 Pydantic Schemas — ⚠️ Exists but UNREADABLE
**File:** `backend/app/schemas/research.py` (41,161 bytes)

- Same situation — file exists but is zero-filled placeholder content.
- Cannot verify if request/response schemas are properly defined.

### 1.4 Frontend Layout — ✅ READABLE (functional)
**File:** `frontend/app/research/layout.tsx`

- Sidebar navigation with **10 nav items**:
  - Dashboard (Overview)
  - Collections
  - Sources
  - Query Builder
  - Explorer
  - Topics
  - Reports
  - Alerts
  - History
  - Bookmarks
- Proper React component structure.

### 1.5 Frontend Pages — ⚠️ Partial (4 readable + 6 unreadable)

**Readable (actual content):**
| File | Bytes | Status |
|------|-------|--------|
| `frontend/app/research/page.tsx` | 6,047 | ✅ Readable — Dashboard page |
| `frontend/app/research/collections/page.tsx` | 10,579 | ✅ Readable — Collections list |
| `frontend/app/research/explorer/page.tsx` | 8,094 | ✅ Readable — Explorer page |
| `frontend/app/research/query/page.tsx` | 11,826 | ✅ Readable — Query Builder page |

**Unreadable (zero-filled placeholders):**
| File | Bytes | Status |
|------|-------|--------|
| `frontend/app/research/sources/page.tsx` | ~6K | ❌ Placeholder |
| `frontend/app/research/topics/page.tsx` | ~6K | ❌ Placeholder |
| `frontend/app/research/reports/page.tsx` | ~6K | ❌ Placeholder |
| `frontend/app/research/alerts/page.tsx` | ~6K | ❌ Placeholder |
| `frontend/app/research/history/page.tsx` | ~6K | ❌ Placeholder |
| `frontend/app/research/bookmarks/page.tsx` | ~6K | ❌ Placeholder |

### 1.6 Frontend Components — ✅ 3 exist (functional)
| File | Status |
|------|--------|
| `frontend/components/research/KPICard.tsx` | ✅ Present |
| `frontend/components/research/LoadingSkeleton.tsx` | ✅ Present |
| `frontend/components/research/Sidebar.tsx` | ✅ Present |

### 1.7 State Management — ⚠️ Placeholder
**File:** `frontend/stores/research.ts` (22,410 bytes)

- Exists but is zero-filled placeholder content.

### 1.8 Specification Documents — ⚠️ Mixed

| File | Status | Content |
|------|--------|---------|
| `docs/specifications/03-AI/RESEARCH_ENGINE.md` | ✅ Real spec | 4 responsibilities |
| `docs/specifications/05-Frontend/RESEARCH_CENTER_UI.md` | ✅ Real spec | Purpose + 4 responsibilities |
| `docs/specifications/03-AI/RESEARCH_AGENT.md` | ❌ Placeholder | Status: TODO |
| `docs/specifications/04-Backend/RESEARCH_PIPELINE.md` | ❌ Placeholder | Status: TODO |

---

## 2. What's Missing (Complete Gap Inventory)

### 2.1 Backend Services — ❌ ALL missing
No `backend/app/services/research/` directory or files exist. Compare with `services/strategy/` which has 8 service files.

| Service | Purpose | Status |
|---------|---------|--------|
| Research Aggregator | News aggregation from external sources | ❌ Missing |
| Fact Extractor | NLP-based fact extraction from documents | ❌ Missing |
| Summarizer | Automated content summarization | ❌ Missing |
| Entity Linker | Entity identification & relationship mapping | ❌ Missing |
| Source Connector | Platform connector management (Web/Social) | ❌ Missing |
| Research Pipeline | Full workflow orchestrator | ❌ Missing |
| Citation Manager | Citation generation & management | ❌ Missing |
| Cache Manager | Research cache layer management | ❌ Missing |

### 2.2 API Endpoints — ❌ Implementation is zero (file is placeholder)

Despite the router file existing, its content is null — effectively no endpoints implemented.

Required endpoint groups (inferred from models + spec):
| Endpoint | Purpose | Status |
|----------|---------|--------|
| `GET/POST /api/research/queries` | CRUD for research queries | ❌ Stub |
| `GET/POST /api/research/documents` | CRUD for documents | ❌ Stub |
| `GET/POST /api/research/collections` | CRUD for collections | ❌ Stub |
| `GET/POST /api/research/sources` | CRUD for sources | ❌ Stub |
| `GET /api/research/topics` | Topic management | ❌ Stub |
| `POST /api/research/execute` | Run a research query | ❌ Stub |
| `GET /api/research/facts` | Extracted facts | ❌ Stub |
| `GET /api/research/insights` | Generated insights | ❌ Stub |
| `POST /api/research/summarize` | Trigger summarization | ❌ Stub |
| `POST /api/research/extract` | Trigger entity extraction | ❌ Stub |
| `GET /api/research/reports` | Research reports | ❌ Stub |
| `GET /api/research/alerts` | Research alerts | ❌ Stub |
| `GET /api/research/history` | Research history | ❌ Stub |
| `POST /api/research/bookmarks` | Bookmark management | ❌ Stub |

### 2.3 Frontend Pages — ❌ 6 of 10 are placeholder stubs

As detailed in section 1.5 — only Dashboard, Collections, Explorer, and Query Builder have real content. Sources, Topics, Reports, Alerts, History, and Bookmarks are empty.

### 2.4 State Management — ❌ Placeholder

`frontend/stores/research.ts` (22KB) is zero-filled — no actual store logic.

### 2.5 API Client — ❌ ALL missing

No research API client functions exist under `frontend/lib/` or similar.

### 2.6 Tests — ❌ ALL missing

No research-related test files exist anywhere:
| Test Location | Files Found |
|---------------|-------------|
| `tests/backend/unit/` | ❌ Zero research tests |
| `tests/backend/api/` | ❌ Zero research tests |
| `tests/backend/integration/` | ❌ Zero research tests |
| `tests/frontend/unit/` | ❌ Zero research tests |
| `tests/frontend/components/` | ❌ Zero research tests |
| `tests/frontend/integration/` | ❌ Zero research tests |
| `tests/e2e/` | ❌ Zero research tests |
| `backend/tests/` | ❌ Only strategy tests exist |
| `__tests__/` | ❌ Directory doesn't exist |

### 2.7 Documentation — ❌ ALL missing

| Doc Type | Status |
|----------|--------|
| User guide / Research Center manual | ❌ Missing |
| API reference (OpenAPI) | ❌ Missing |
| Admin / ops guide | ❌ Missing |
| Integration guide (with Content Strategy) | ❌ Missing |
| RESEARCH_PIPELINE.md spec | ❌ Placeholder (Status: TODO) |

### 2.8 AI Capabilities — ❌ 4 capabilities missing

| Capability | Status |
|------------|--------|
| News aggregation & filtering | ❌ Not implemented |
| Fact extraction from trusted sources | ❌ Not implemented |
| Comprehensive summarization | ❌ Not implemented |
| Entity identification & relationship mapping | ❌ Not implemented |

---

## 3. What's Working (Strengths)

1. **Database models are complete** — 23 entities + 4 junction tables + 8+ enums. This is the hardest part to design and it's done well.
2. **Frontend layout is functional** — sidebar with all 10 nav items, proper Next.js layout structure.
3. **3 frontend components exist** — KPICard, LoadingSkeleton, Sidebar — reusable building blocks.
4. **Router is registered** — `api/research/__init__.py` and `endpoints.py` exist at the right path.
5. **Schema file exists** — even though content is placeholder, the file structure is in place.

---

## 4. Root Cause Analysis

1. **Phase P10 = 0%:** MASTER_PROGRESS.md explicitly marks "P10 — Research Center" as Not Started. The existent models and router were likely pre-generated scaffolding, not intentional implementation.
2. **Zero-filled files are common in scaffolding tools:** The 6 unreadable frontend pages, the schemas, the endpoints, and the store all have non-trivial sizes but zero content — consistent with placeholder generation.
3. **Services are the biggest gap:** The `services/strategy/` directory shows the pattern — every functional engine has dedicated services. Research has none.
4. **Project is very new:** All files are dated June 26, 2026 — this project is approximately 6 hours old.

---

## 5. Recommendations

### Immediate (Phase P10)
1. **Implement `services/research/` services** — mirror the `services/strategy/` pattern. Start with:
   - `aggregator_service.py` — news/document aggregation
   - `extraction_service.py` — fact & entity extraction
   - `summarization_service.py` — content summarization
2. **Replace placeholder endpoints** in `endpoints.py` with real CRUD endpoints leveraging the 27 models.
3. **Replace placeholder schemas** in `schemas/research.py` with proper Pydantic request/response schemas.

### Short-term
4. **Rewrite the 6 placeholder frontend pages** — Sources, Topics, Reports, Alerts, History, Bookmarks.
5. **Implement `stores/research.ts`** with Zustand/Pinia store for research state management.
6. **Write tests** — start with unit tests for models, then API integration tests.

### Medium-term
7. **Implement AI capabilities** — news aggregation, fact extraction, summarization, entity linking.
8. **Complete the RESEARCH_PIPELINE.md and RESEARCH_AGENT.md specs** before deeper implementation.
9. **Integrate with Content Strategy (P11)** — research output should feed into content planning.

---

*Audit performed: June 26, 2026*
*Audit scope: Social-Farm-AI monorepo (Python + Next.js)*
