# BACKUP AND RECOVERY

## Backup Policy
- **Daily Full Backups:** Automated snapshot of the entire database.
- **Incremental Backups:** Continuous WAL (Write-Ahead Logging) archiving to enable Point-in-Time Recovery (PITR).

## Recovery Procedures
- **Disaster Recovery:** Automated restoration of the latest full snapshot + replaying WAL logs.
- **Restore Testing:** Quarterly manual restoration of production backups to a staging environment to verify data integrity.
