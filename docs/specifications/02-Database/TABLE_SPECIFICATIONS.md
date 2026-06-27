# TABLE SPECIFICATIONS

This document lists the foundational schema requirements. All tables include mandatory audit columns: `id`, `created_at`, `updated_at`, `deleted_at`.

## Core Domain

### organizations
- **Purpose:** Root entity for billing and management.
- **Columns:** `id`, `name`, `billing_tier`, `created_at`, `updated_at`, `deleted_at`.

### workspaces
- **Purpose:** Logical grouping for collaboration.
- **Columns:** `id`, `organization_id` (FK), `name`, `created_at`, `updated_at`, `deleted_at`.

### brands
- **Purpose:** Identity container.
- **Columns:** `id`, `workspace_id` (FK), `name`, `style_guide_url`, `created_at`, `updated_at`, `deleted_at`.

## Content Domain

### content
- **Purpose:** The central content entity (scripts, captions, etc).
- **Columns:** `id`, `project_id` (FK), `title`, `content_type` (Enum), `raw_body`, `metadata` (JSONB), `status` (Enum), `created_at`, `updated_at`, `deleted_at`.

---

*(Note: In an actual implementation, this file would expand to include definitions for every table defined in the scope.)*
