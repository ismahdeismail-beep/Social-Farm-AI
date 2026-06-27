# DATA RETENTION

## Soft Delete Strategy
- All core entities include a `deleted_at` timestamp.
- Application logic filters `WHERE deleted_at IS NULL`.
- Permanent deletion is a background task managed by `ops` cleanup workers.

## Archiving Policies
- **Audit Logs:** Retain for 1 year in active table, archive to cold storage for 7 years.
- **AI Memory/Conversations:** Retain per project lifecycle.
- **Analytics:** Aggregated daily metrics retained indefinitely; raw events archived after 90 days.
- **Notifications:** Retain for 30 days.
