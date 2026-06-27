# DATA_RETENTION

## Purpose
The Data Retention policy balances storage costs, performance requirements, and compliance obligations.

## Retention Policy
| Data Type | Retention Period | Action |
| :--- | :--- | :--- |
| Raw Events | 90 Days | Aggregated -> Archive |
| Aggregated Metrics | 3 Years | Long-term Storage |
| Audit Logs | 5 Years | Archived (Compliance) |

## Implementation
Data older than the retention period is automatically archived to low-cost storage (S3 Glacier) or deleted, as defined in the policy.
