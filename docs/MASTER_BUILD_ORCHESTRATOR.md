# MASTER BUILD ORCHESTRATOR

This document is the permanent implementation guide for the Social Farm AI OS project. All development, regardless of phase, must strictly adhere to the policies defined herein.

## 1. Overall Development Strategy
We employ a **Vertical Slice Architecture**. We build complete, functional features end-to-end (Database → API → UI → Tests → Docs) rather than building horizontal technical layers. This ensures that every increment is a deployable, testable unit of value.

## 2. Architecture Freeze Policy
*   **Policy**: The core architecture is defined in `docs/specifications/`.
*   **Changes**: Architectural changes are prohibited without a formal Architecture Decision Record (ADR) and approval from the Principal Architect.
*   **Versioning**: All architectural changes must be versioned in the ADR log.

## 3. Incremental Development Rules
*   **Scope**: Maximum of 5 files per implementation cycle.
*   **Feature Size**: Features must be small enough to be implemented and tested in a single session.
*   **Context**: AI agents must load only the relevant specification and the immediate code context to avoid hallucinations.

## 4. Feature Build Order
| Phase | Title | Objectives |
| :--- | :--- | :--- |
| P1 | Repository Audit | Codebase health check & cleanup |
| P2 | Authentication | Auth operational; Dev env stable |
| P3 | Organizations | Multi-tenancy foundation |
| P4 | Users | User profile management |
| P5 | Roles & Permissions | RBAC implementation |
| P6 | Brand Manager | Brand entity management |
| P7 | Project Manager | Project structure & metadata |
| P8 | Dashboard | Base UI, Navigation |
| P9 | Trend War Room | Discovery, Alerts |
| P10 | Research Center | Source connections |
| P11 | AI Studio | Memory, Prompt Library |
| P12 | Script Studio | Scripting pipeline |
| P13 | Media Factory | Rendering, Encoding |
| P14 | Publishing Center | Queue, Scheduler |
| P15 | Analytics Center | Dashboards, Metrics |
| P16 | Growth Center | Insight generation |
| P17 | Admin Panel | Audit, Security, RBAC |
| P18 | Optimization | Scaling, Caching |

## 5. Quality Gates
Every phase must pass:
1.  **Formatting**: Prettier/Black.
2.  **Linting**: ESLint/Ruff.
3.  **Type Checking**: TypeScript/MyPy.
4.  **Security**: Snyk/Bandit.
5.  **Tests**: Unit & Integration.
6.  **Documentation**: Updated specs.
7.  **Manual QA**: Human verification.

## 6. Coding Standards
*   **Python**: FastAPI, SQLAlchemy, Ruff.
*   **TypeScript**: Next.js, React, Tailwind, Zod.
*   **Naming**: Consistent `camelCase` for JS/TS, `snake_case` for Python/SQL.

## 7. AI Coding Rules
*   Never overwrite unrelated files.
*   Never refactor without approval.
*   Always explain major decisions.
*   Always update tests and documentation.

## 8. Context Management
*   AI must load only the relevant `docs/specifications/` file.
*   If context exceeds 10,000 tokens, split the task.

## 9. Git Workflow
*   `feature/<phase-id>-<name>` branch.
*   PR required for merge to `develop`.
*   Commit message: `feat(phase-id): description`.

## 10. Testing Workflow
Unit → Integration → UI → Performance → Security → Regression → Approval.

## 11. Definition of Done
Documentation updated, Backend complete, Frontend complete, Tests passing, Lint passing, Security reviewed, Performance acceptable, Git committed.

## 12. Recovery Strategy
Rollback → Restore → Rebuild → Retest → Continue.

## 13. Progress Tracking
Tracked in `docs/MASTER_PROGRESS.md`.

## 14. Future Expansion
New modules require an ADR, specification update, and integration into the build order.
