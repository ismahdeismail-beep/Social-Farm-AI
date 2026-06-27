# DEVELOPMENT_RULES
Status: TODO
This document will be completed during the specification phase.
# Social Farm AI OS

# DEVELOPMENT RULES

Version: 1.0

Status: Active

Classification: Core Specification

---

# Purpose

This document defines the mandatory engineering rules governing the development of Social Farm AI OS.

These rules apply to all contributors, AI coding agents, and automation systems. Their purpose is to ensure a maintainable, secure, scalable, and consistent codebase.

---

# General Principles

Development shall prioritize:

- Correctness over speed
- Simplicity over complexity
- Readability over cleverness
- Reusability over duplication
- Security by default
- Performance by design
- Documentation as part of development

---

# Architecture Rules

## Single Responsibility

Each module, service, and component shall have one clearly defined responsibility.

Avoid combining unrelated functionality into a single file or class.

---

## Modular Design

Modules should be independent.

Communication between modules must occur through defined interfaces.

Direct dependencies between unrelated modules are prohibited.

---

## Separation of Concerns

The application shall separate:

- Presentation
- Business Logic
- Data Access
- Infrastructure
- AI Integration

Business rules must never reside inside UI components.

---

# Code Reuse

Before creating new code:

1. Search for an existing implementation.
2. Extend existing functionality where appropriate.
3. Create reusable utilities instead of duplicating logic.

Duplicated code should be eliminated during refactoring.

---

# File Organization

Each file should have a clear purpose.

Avoid files exceeding approximately 500 lines unless justified by design.

Large features should be split into logical modules.

---

# Naming Standards

Names should be descriptive and unambiguous.

Examples:

Good

```text
CreateVideoJob
TrendAnalyzer
PublishContentService
UserRepository
```

Avoid

```text
Helper
Utils
Data
Manager
Temp
```

Names should describe intent, not implementation details.

---

# API Rules

Every API endpoint shall:

- Validate input
- Authenticate requests
- Authorize access
- Return consistent responses
- Handle errors gracefully
- Log important events

No endpoint should expose internal implementation details.

---

# Database Rules

Database access shall occur only through repositories or service layers.

Never execute raw SQL directly inside controllers or UI code unless explicitly documented and reviewed.

Every schema change must be versioned through migrations.

---

# AI Integration Rules

AI providers shall be accessed through the centralized AI Gateway.

Application modules must never call AI providers directly.

All prompts should be:

- Version controlled
- Reusable
- Documented
- Testable

Provider-specific logic should remain isolated.

---

# Error Handling

Errors should be:

- Anticipated
- Logged
- User-friendly
- Recoverable where possible

Avoid generic catch blocks that silently ignore failures.

Never expose stack traces or sensitive details to end users.

---

# Logging Rules

Log events that assist debugging and operations.

Log:

- Authentication events
- Publishing events
- AI requests
- Background jobs
- Errors
- Performance warnings

Do not log:

- Passwords
- API keys
- Tokens
- Personal secrets
- Sensitive content

---

# Configuration Management

Configuration must come from environment variables or approved configuration files.

Hardcoding credentials, secrets, URLs, or environment-specific values is prohibited.

---

# Dependency Rules

Before adding a dependency:

- Verify active maintenance
- Review licensing
- Assess security
- Confirm necessity

Unused dependencies should be removed regularly.

---

# Frontend Rules

Interfaces shall:

- Be responsive
- Be accessible
- Support keyboard navigation
- Display loading states
- Display meaningful error messages
- Support dark mode

UI logic should remain separate from business logic.

---

# Backend Rules

Controllers should remain thin.

Business logic belongs in services.

Database operations belong in repositories.

Validation should occur before business logic executes.

---

# Background Jobs

Long-running operations must execute asynchronously.

Examples:

- AI generation
- Video rendering
- Scheduled publishing
- Report generation

Jobs should support retries and failure reporting.

---

# Testing Rules

Every feature should include appropriate automated tests.

Minimum expectations:

- Unit tests
- Integration tests
- Critical workflow validation

Bugs should include regression tests where practical.

---

# Documentation Rules

Every major feature must include:

- Purpose
- Inputs
- Outputs
- Dependencies
- Usage Notes

Public APIs must be documented.

Architectural changes should update the relevant specifications.

---

# Git Rules

Development should use feature branches.

Example:

```text
feature/dashboard

feature/media-factory

feature/analytics
```

Commit messages should be descriptive.

Example:

```text
feat: add publishing scheduler

fix: resolve media rendering timeout

refactor: simplify AI routing service
```

Avoid large commits containing unrelated changes.

---

# Security Rules

Every implementation must:

- Validate input
- Escape output where appropriate
- Enforce authorization
- Protect secrets
- Use secure defaults
- Apply least-privilege principles

Security is not optional.

---

# Performance Rules

Developers should:

- Avoid unnecessary database queries
- Cache frequently accessed data
- Lazy load heavy resources
- Optimize rendering pipelines
- Minimize bundle sizes

Performance should be measured, not assumed.

---

# Review Checklist

Before marking work complete, verify:

- Requirements satisfied
- Tests passing
- Documentation updated
- No duplicated code
- Security considered
- Performance acceptable
- Naming consistent
- Architecture respected

---

# Prohibited Practices

The following are prohibited unless formally approved:

- Hardcoded secrets
- Copy-pasted business logic
- Circular dependencies
- Direct database access from UI
- Direct AI provider calls outside the AI Gateway
- Ignoring errors
- Skipping validation
- Disabling authentication for convenience
- Commenting out code instead of removing it

---

# Continuous Improvement

Development is iterative.

Refactoring is encouraged when it:

- Improves clarity
- Reduces duplication
- Increases maintainability
- Improves performance
- Simplifies architecture

Large refactors should be planned and documented.

---

# Compliance

All project contributors are expected to follow these rules.

Any intentional deviation should be documented with justification and approved during architectural review.

---

# Revision History

| Version | Date | Summary |
|----------|------|---------|
| 1.0 | Initial Release | Development standards and engineering rules |

---

# End of Document