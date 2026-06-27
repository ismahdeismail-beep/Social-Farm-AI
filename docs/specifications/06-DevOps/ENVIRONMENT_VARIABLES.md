# Environment Variables

## 1. Overview
All environment variables must be defined in the project's configuration management system. They are categorized by function and security level.

## 2. Variable Specification

| Category | Variable Name | Purpose | Required | Default | Security Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Frontend** | `NEXT_PUBLIC_API_URL` | API Endpoint | Yes | N/A | Public |
| **Backend** | `DATABASE_URL` | Database Connection | Yes | N/A | High |
| **Database** | `DB_PASSWORD` | Database Password | Yes | N/A | Critical |
| **Redis** | `REDIS_URL` | Redis Connection | Yes | N/A | High |
| **AI Providers** | `OPENAI_API_KEY` | AI Service Key | Yes | N/A | Critical |
| **Storage** | `S3_BUCKET_NAME` | Storage Bucket | Yes | N/A | Medium |
| **Auth** | `JWT_SECRET` | Auth Token Secret | Yes | N/A | Critical |
| **Analytics** | `ANALYTICS_ID` | Analytics Tracking | No | N/A | Public |
| **Publishing** | `PUBLISH_QUEUE_URL` | Queue Endpoint | Yes | N/A | Medium |
| **Security** | `ENCRYPTION_KEY` | Data Encryption | Yes | N/A | Critical |
| **Monitoring** | `DATADOG_API_KEY` | Monitoring Key | Yes | N/A | High |
| **Logging** | `LOG_LEVEL` | Logging Verbosity | No | INFO | Low |

## 3. Security Levels
*   **Public**: Safe to expose in client-side code.
*   **Low**: Non-sensitive configuration.
*   **Medium**: Sensitive but not critical.
*   **High**: Highly sensitive, requires encryption at rest and in transit.
*   **Critical**: Must be managed via a secure secrets manager, rotated regularly, and never logged.
