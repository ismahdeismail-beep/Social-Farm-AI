# MIGRATION STRATEGY

## Alembic Workflow
All database schema changes must be managed via Alembic.

1. **Development:** Generate migration script: `alembic revision --autogenerate -m "description"`.
2. **Review:** Inspect generated script for correctness (especially constraint names).
3. **Application:** Apply migrations in CI/CD before deployment: `alembic upgrade head`.

## Versioning & Compatibility
- Migrations must be backwards compatible to support zero-downtime deployments.
- Avoid deleting columns; use `DROP COLUMN` only after verified deprecation in application code.
- If a destructive change is necessary, implement in two phases:
    1. Add new column/table, application writes to both.
    2. Migrate data, application reads from new, application drops old.
