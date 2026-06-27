# EVENT_TRACKING

## Purpose
The Event Tracking system provides a unified, structured language for recording user, system, and AI interactions across the platform.

## Event Categories
| Category | Examples |
| :--- | :--- |
| **Frontend** | Page views, clicks, form submissions, scroll depth |
| **Backend** | API requests, database updates, background jobs |
| **AI** | Prompt submission, model inference, memory retrieval |
| **Publishing** | Post creation, scheduling, publish success/failure |
| **Media** | Media upload, processing, generation |
| **System** | Auth, login/out, error logging, audit trails |

## Schema Design
Every event must follow this JSON schema:
```json
{
  "event_id": "UUID",
  "timestamp": "ISO8601",
  "user_id": "UUID",
  "workspace_id": "UUID",
  "event_name": "string",
  "source": "string",
  "metadata": "object"
}
```

## Implementation
Events are captured using SDKs (client-side) or Middleware (server-side) and streamed directly to the [DATA_PIPELINE](./DATA_PIPELINE.md).
