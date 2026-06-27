# Disaster Recovery

## Objectives
*   **RTO (Recovery Time Objective)**: < 1 hour.
*   **RPO (Recovery Point Objective)**: < 15 minutes.

## Procedures
1.  **Infrastructure Recovery**: Re-provision infrastructure via IaC.
2.  **Database Recovery**: Restore from latest backup.
3.  **Application Recovery**: Redeploy containers.

## Testing
Disaster recovery drills performed quarterly.
