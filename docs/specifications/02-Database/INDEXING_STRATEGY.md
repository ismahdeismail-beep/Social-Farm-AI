# INDEXING STRATEGY

## Primary Strategy
- **Primary Keys:** Clustered B-tree indexes automatically created on all PK columns.
- **Foreign Keys:** All FK columns must be indexed to ensure join performance.

## Specialized Indexing
- **GIN (Generalized Inverted Index):** Used for `JSONB` columns in `ai_memory`, `content` metadata, and `analytics` logs to allow efficient full-text and key-value searches.
- **Composite Indexes:** Created for common query patterns (e.g., `(project_id, created_at)` for content filtering).
- **Partial Indexes:** Used for soft-delete filtering (e.g., `WHERE deleted_at IS NULL`).

## Performance Strategy
- Regularly run `ANALYZE` to update query planner statistics.
- Avoid over-indexing columns with low cardinality.
- Monitor index usage using `pg_stat_user_indexes`.
