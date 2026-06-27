# Database Specification: README

## Overview
This directory contains the authoritative specification for the Social Farm AI OS PostgreSQL database. 

## Implementation Order
1.  **Core Domain:** Initialize `organizations`, `workspaces`, `users`, `roles`, and `permissions` tables.
2.  **Brand Domain:** Initialize `brands`, `projects`, `campaigns`.
3.  **Content Domain:** Initialize `content`, `scripts`, `media`, `assets`, `tags`.
4.  **AI Domain:** Initialize `ai_agents`, `prompt_library`, `ai_memory`, `conversations`.
5.  **Operational Domain:** Initialize `publishing_queue`, `publishing_history`, `analytics`, `notifications`, `audit_logs`.
6.  **System/Access:** Initialize `api_keys`, `oauth_accounts`, `settings`.

## File Index
- `DATABASE_OVERVIEW.md`: Architectural philosophy and design principles.
- `ENTITY_RELATIONSHIPS.md`: High-level data modeling and relationship rules.
- `TABLE_SPECIFICATIONS.md`: Detailed schema definitions for all entities.
- `INDEXING_STRATEGY.md`: Indexing and performance optimization plan.
- `MIGRATION_STRATEGY.md`: Migration lifecycle and Alembic workflows.
- `DATA_RETENTION.md`: Archiving and soft-delete policies.
- `BACKUP_AND_RECOVERY.md`: DR and operational resilience plan.
- `SEED_DATA.md`: Initial system data, roles, and permissions.
- `DATABASE_SECURITY.md`: Security, encryption, and access control.
- `DATABASE_DICTIONARY.md`: Exhaustive definition of every entity and field.
