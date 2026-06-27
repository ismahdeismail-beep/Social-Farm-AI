# REALTIME_ANALYTICS

## Purpose
Realtime Analytics provides immediate visibility into platform activity, crucial for monitoring live campaigns, publishing status, and system health.

## Key Capabilities
- **Live Publishing Feed:** Monitor publishing tasks as they are dispatched and processed.
- **System Health:** Live monitoring of pipeline throughput and error rates.
- **Campaign Activity:** Real-time engagement spikes for active campaigns.
- **AI Activity:** Live view of AI inference tasks and system load.

## Architecture
Realtime analytics utilizes a streaming architecture (WebSocket or Server-Sent Events) connected directly to the [DATA_PIPELINE](./DATA_PIPELINE.md) event bus, bypassing the warehouse storage delay.
