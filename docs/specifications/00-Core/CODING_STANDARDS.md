# CODING_STANDARDS
Status: TODO
This document will be completed during the specification phase.
# Social Farm AI OS

# CODING STANDARDS

Version: 1.0

Status: Active

Classification: Core Specification

---

# Purpose

This document establishes the coding standards for Social Farm AI OS.

The objective is to ensure that all source code is:

- Consistent
- Readable
- Maintainable
- Testable
- Secure
- Production-ready

These standards apply to every contributor, AI coding agent, automation workflow, and generated code.

---

# Guiding Principles

Code should prioritize:

- Readability over cleverness
- Explicitness over ambiguity
- Simplicity over complexity
- Reusability over duplication
- Maintainability over shortcuts

Every line of code should make the project easier to understand.

---

# General Formatting

## Indentation

Use spaces only.

- TypeScript: 2 spaces
- Python: 4 spaces

Never mix tabs and spaces.

---

## Line Length

Maximum recommended line length:

120 characters.

Long expressions should be broken into multiple lines.

---

## File Length

Recommended maximum:

- Components: 300 lines
- Services: 500 lines
- Utilities: 200 lines

Split large files into logical modules.

---

# Naming Conventions

## Variables

Use descriptive camelCase names.

Good:

```ts
currentUser
trendScore
publishedContent
```

Avoid:

```ts
x
temp
obj
value
```

---

## Constants

Use UPPER_SNAKE_CASE.

Example:

```ts
MAX_UPLOAD_SIZE
DEFAULT_PAGE_SIZE
```

---

## Functions

Use verb-based names.

Good:

```ts
generateCaption()
publishContent()
analyzeTrend()
calculateScore()
```

Avoid:

```ts
handler()
process()
execute()
```

unless the context makes the purpose obvious.

---

## Classes

Use PascalCase.

Example:

```text
TrendAnalyzer

VideoRenderer

PublishingScheduler

MediaFactory
```

---

## Interfaces

Use PascalCase.

Example:

```text
User

Brand

TrendAnalysis

MediaAsset
```

Avoid interface prefixes like `IUser`.

---

## Enums

Use PascalCase.

Members should be UPPER_SNAKE_CASE.

Example

```text
PublishingStatus

PENDING

PUBLISHED

FAILED
```

---

# Folder Naming

Folders use kebab-case.

Example

```text
media-factory

script-studio

trend-engine
```

---

# File Naming

Use kebab-case.

Examples

```text
trend-service.ts

video-renderer.ts

publishing-engine.ts

dashboard-layout.tsx
```

Avoid:

```text
TrendService.ts

NewFile.ts

Test123.ts
```

---

# Component Standards

React components should:

- Have one responsibility
- Be reusable
- Accept typed props
- Avoid excessive nesting

Preferred structure

```text
Component

↓

Subcomponents

↓

Shared Components

↓

Primitive UI
```

---

# TypeScript Standards

Always enable strict mode.

Avoid:

```ts
any
```

Prefer:

```ts
unknown

specific interfaces

generics
```

Use readonly where applicable.

Prefer immutable data structures.

---

# Python Standards

Follow PEP 8.

Use:

- Type hints
- Docstrings
- Dataclasses where appropriate
- Async functions for I/O operations

Avoid global mutable state.

---

# Comments

Code should explain itself.

Comments should explain:

- Why something exists
- Architectural decisions
- Complex algorithms

Avoid comments that simply repeat the code.

Bad

```ts
// increment counter

counter++
```

Good

```ts
// Retry count is limited to prevent infinite publishing loops.
```

---

# Documentation

Public functions should include documentation.

Example

```text
Purpose

Parameters

Returns

Exceptions

Example Usage
```

Complex services should include module-level documentation.

---

# Error Handling

Always handle expected failures.

Example categories:

- Validation errors
- Authentication failures
- Network failures
- Storage failures
- AI provider failures

Do not swallow exceptions.

Every error should be logged appropriately.

---

# Logging

Logs should include:

- Severity
- Timestamp
- Module
- Correlation ID
- User ID (if available)

Never log:

- Passwords
- Tokens
- API Keys
- Secrets

---

# API Standards

REST endpoints should use nouns.

Good

```text
GET /projects

POST /projects

GET /projects/{id}

DELETE /projects/{id}
```

Avoid:

```text
/getProjects

/deleteProject
```

Use HTTP methods appropriately.

---

# Database Standards

Table names:

snake_case

Example

```text
users

media_assets

publishing_jobs
```

Primary key:

id

Foreign keys:

user_id

brand_id

project_id

Use timestamps:

created_at

updated_at

deleted_at (soft delete if applicable)

---

# Configuration

Never hardcode:

- URLs
- Secrets
- Passwords
- Tokens
- Keys

Use environment variables.

---

# Dependency Injection

Services should receive dependencies through constructors or framework-supported dependency injection.

Avoid creating service instances directly inside business logic.

---

# Testing Standards

Every feature should include tests.

Naming

```text
feature-name.test.ts

feature-name.spec.ts
```

Backend

```text
test_feature.py
```

Tests should be:

- Deterministic
- Isolated
- Fast
- Readable

---

# Git Commit Standard

Use Conventional Commits.

Examples

```text
feat: add AI trend analyzer

fix: resolve scheduler timezone bug

refactor: simplify publishing workflow

docs: update architecture specification

test: add media engine tests

chore: upgrade dependencies
```

---

# Pull Request Standards

Every pull request should include:

- Summary
- Scope
- Screenshots (UI changes)
- Testing performed
- Related issues
- Breaking changes

---

# Security Standards

Validate all input.

Escape output where appropriate.

Protect against:

- Injection
- XSS
- CSRF
- SSRF

Never trust client-side validation alone.

---

# Performance Standards

Prefer:

- Lazy loading
- Pagination
- Streaming large files
- Efficient queries
- Background processing

Avoid premature optimization, but measure performance regularly.

---

# Accessibility Standards

Interfaces should support:

- Keyboard navigation
- Screen readers
- Color contrast
- Focus indicators
- Responsive layouts

Accessibility is a core quality requirement.

---

# Code Review Checklist

Before merging:

- Code follows naming standards.
- Formatting passes.
- Tests pass.
- No duplicated logic.
- Documentation updated.
- Security reviewed.
- Performance acceptable.
- Architecture respected.

---

# Exceptions

Any exception to these standards must:

- Be documented.
- Include justification.
- Be approved during architectural review.

---

# Revision History

| Version | Date | Summary |
|----------|------|---------|
| 1.0 | Initial Release | Project-wide coding standards |

---

# End of Document