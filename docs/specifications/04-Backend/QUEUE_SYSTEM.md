# QUEUE SYSTEM

## Purpose
Reliable handling of long-running operations.

## Architecture
- **Broker:** Redis.
- **Worker:** Celery.
- **Design:** Priority queues for different tasks (e.g., `high` for rendering, `low` for analytics).
