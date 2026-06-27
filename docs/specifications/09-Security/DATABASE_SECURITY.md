# Database Security

## 1. Purpose
To secure the database against unauthorized access, data breaches, and corruption.

## 2. Architecture
Database is deployed in a private subnet, accessible only by authorized application services.

## 3. Responsibilities
*   **DBA/DevOps**: Manage database security configuration.
*   **Backend Team**: Implement secure query practices.

## 4. Threats
*   SQL injection.
*   Unauthorized data access.
*   Data loss.

## 5. Mitigations
*   Parameterized queries (ORM).
*   Least privilege database roles.
*   Encryption at rest and in transit.

## 6. Best Practices
*   Regular security patching.
*   Audit all database queries.

## 7. Security Controls
*   Database firewall.
*   Encryption.

## 8. Monitoring
*   Monitor database access logs.
*   Alert on suspicious query patterns.

## 9. Incident Handling
*   Isolate compromised database instances.

## 10. Future Enhancements
*   Database activity monitoring (DAM).

## 11. Cross References
*   `DATA_PROTECTION.md`
