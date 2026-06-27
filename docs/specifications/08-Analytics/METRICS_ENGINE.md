# METRICS_ENGINE

## Purpose
The Metrics Engine is responsible for the standardized calculation, aggregation, and serving of business and operational metrics derived from the raw event data.

## Metrics Definition
All metrics are defined in a centralized repository (code as configuration) to ensure consistency across dashboards and reports.

| Metric | Type | Definition |
| :--- | :--- | :--- |
| **Active Users** | Count | Distinct users with active sessions in X period |
| **Publishing Success Rate** | Ratio | Successful posts / Total publishing attempts |
| **Avg. Engagement Rate** | Percentage | (Likes + Comments + Shares) / Impressions |
| **AI Inference Latency** | Duration | Time taken for AI agent to respond |

## Architecture
- **Aggregation Layer:** Computes metrics (daily/hourly) using SQL or Flink.
- **Metric Store:** Stores pre-aggregated metrics in a highly queryable format (Redis/PostgreSQL).
- **Metric API:** Provides a standardized API for dashboards to query these metrics.
