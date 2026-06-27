# Data Protection

## 1. Sensitive Data Classification
*   **Public**: Non-sensitive data.
*   **Internal**: Business data, not for public consumption.
*   **Confidential**: PII, user data, brand secrets.
*   **Restricted**: Credentials, encryption keys.

## 2. PII Handling
*   PII is encrypted at rest.
*   PII is masked in logs and non-production environments.

## 3. Data Retention & Deletion
*   Automated data deletion policies based on data classification.
*   Support for "Right to be Forgotten" (GDPR).
