# WEBHOOKS

## Purpose
The Webhook system enables real-time integration with external applications to receive event updates from the Publishing Engine.

## Event Types
| Event | Trigger | Payload |
| :--- | :--- | :--- |
| `post.published` | Successful publish | Post ID, Platform, Timestamp |
| `post.failed` | Permanent failure | Post ID, Error Type, Timestamp |
| `post.approved` | Approval status change | Post ID, Approver ID, Timestamp |

## Design
Webhooks are delivered via POST requests to user-configured endpoints. The system implements a delivery retry mechanism with exponential backoff for webhook failures.
