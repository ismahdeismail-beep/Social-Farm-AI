# FILE_STRUCTURE
Status: TODO
This document will be completed during the specification phase.
# Social Farm AI OS

# FILE STRUCTURE

Version: 1.0

Status: Active

Classification: Core Specification

---

# Purpose

This document defines the official repository structure for Social Farm AI OS.

Every directory has a clearly defined responsibility.

Source code, documentation, assets, infrastructure, and automation must remain organized according to this specification.

No implementation should create arbitrary folders without architectural justification.

---

# Repository Overview

```
Social-Farm-AI/

│

├── docs/

├── frontend/

├── backend/

├── shared/

├── assets/

├── infrastructure/

├── docker/

├── scripts/

├── .github/

├── README.md

├── LICENSE

└── .gitignore
```

---

# Root Directory

The root directory contains project-wide resources.

Contents include:

- Repository configuration
- Documentation
- Source code
- Infrastructure
- Assets
- Automation

The root should remain clean and uncluttered.

---

# docs/

Purpose

Contains all project documentation.

Subdirectories

```
docs/

├── specifications/

├── prompts/

└── diagrams/
```

---

## specifications/

Purpose

The authoritative engineering specifications for the project.

Contains:

- Core Architecture
- UI Specifications
- Database Design
- AI Design
- Security
- DevOps
- API Specifications
- Implementation Guides

Specifications act as the source of truth.

---

## prompts/

Purpose

Stores structured prompts used by AI coding assistants.

Examples:

- Project initialization
- Build phases
- Code generation
- Refactoring
- Documentation generation

Prompts should be version controlled.

---

## diagrams/

Purpose

Stores architecture diagrams.

Examples:

- System diagrams
- ER diagrams
- Deployment diagrams
- Workflow diagrams
- Sequence diagrams

Preferred formats:

- Draw.io
- Mermaid
- SVG

---

# frontend/

Purpose

Contains the complete frontend application.

Example structure

```
frontend/

├── app/

├── components/

├── features/

├── hooks/

├── lib/

├── services/

├── store/

├── styles/

├── types/

├── utils/

└── tests/
```

---

## app/

Application routing.

Layouts.

Pages.

Navigation.

---

## components/

Reusable UI components.

Should not contain business logic.

---

## features/

Feature-oriented modules.

Example

```
trend-engine

media-factory

publishing

analytics
```

Each feature should own:

- Components
- Hooks
- Services
- Types

---

## hooks/

Reusable React hooks.

Examples

- useAuth
- useBrand
- useTheme
- usePublishing

---

## services/

Frontend API clients.

No UI rendering.

---

## store/

Global application state.

Responsibilities

- Authentication
- User Preferences
- Brand Context
- Theme
- Notifications

---

## styles/

Global styling.

Fonts.

Theme.

Variables.

---

## types/

Shared TypeScript types.

Interfaces.

Enums.

---

## utils/

Utility functions.

Pure functions only.

---

## tests/

Frontend tests.

Unit tests.

Integration tests.

---

# backend/

Purpose

Contains backend services.

Example

```
backend/

├── api/

├── services/

├── repositories/

├── models/

├── schemas/

├── workers/

├── ai/

├── media/

├── auth/

├── config/

├── utils/

└── tests/
```

---

## api/

REST endpoints.

Controllers.

Routers.

---

## services/

Business logic.

Workflow orchestration.

---

## repositories/

Database abstraction.

ORM access.

Transactions.

---

## models/

Database models.

ORM entities.

---

## schemas/

Validation models.

API contracts.

Request validation.

---

## workers/

Background jobs.

Examples

- Rendering
- AI generation
- Publishing
- Analytics

---

## ai/

AI orchestration.

Prompt routing.

Provider abstraction.

Memory.

---

## media/

Rendering.

Video.

Audio.

Subtitles.

Assets.

---

## auth/

Authentication.

Authorization.

Tokens.

Sessions.

---

## config/

Application configuration.

Environment loading.

Feature flags.

---

## utils/

Reusable backend utilities.

---

## tests/

Backend testing.

Unit.

Integration.

Performance.

---

# shared/

Purpose

Code shared between frontend and backend.

Examples

- Types
- Constants
- Validation
- API Contracts

Avoid duplicated logic.

---

# assets/

Purpose

Project assets.

Contains

```
assets/

images/

icons/

logos/

fonts/

templates/

sample-data/
```

Not intended for user uploads.

---

# infrastructure/

Purpose

Infrastructure configuration.

Examples

- Deployment
- Monitoring
- Provisioning
- Cloud Configuration

---

# docker/

Purpose

Dockerfiles.

Docker Compose.

Container configuration.

---

# scripts/

Purpose

Automation scripts.

Examples

- Setup
- Database
- Migration
- Deployment
- Maintenance

Scripts should be idempotent whenever possible.

---

# .github/

Purpose

GitHub configuration.

Contains

```
workflows/

ISSUE_TEMPLATE/

PULL_REQUEST_TEMPLATE/

CODEOWNERS/
```

---

# Naming Rules

Folders

Use kebab-case.

Files

Use kebab-case.

Avoid spaces.

Avoid special characters.

---

# Ownership

Every directory should have a clearly defined responsibility.

Files should not be duplicated across multiple locations.

Shared code belongs in `shared/`.

Platform-specific code belongs in the corresponding application.

---

# Dependency Rules

Allowed

```
Frontend

↓

Backend API

↓

Business Services

↓

Repositories

↓

Database
```

Not Allowed

```
Frontend

↓

Database
```

Nor:

```
UI Components

↓

Database
```

All communication must pass through approved layers.

---

# Future Expansion

Future directories may include:

```
mobile/

desktop/

plugins/

sdk/

cli/

marketplace/

examples/
```

These additions should not require restructuring existing folders.

---

# Repository Health

A healthy repository should exhibit:

- Clear organization
- Predictable structure
- Minimal duplication
- Consistent naming
- Strong separation of concerns

Repository organization should scale as the project grows.

---

# Relationship to Other Documents

This document defines **where** project resources belong.

It complements:

- SYSTEM_ARCHITECTURE.md
- DEVELOPMENT_RULES.md
- CODING_STANDARDS.md

Together they define how the project is organized, implemented, and maintained.

---

# Revision History

| Version | Date | Summary |
|----------|------|---------|
| 1.0 | Initial Release | Repository structure specification |

---

# End of Document