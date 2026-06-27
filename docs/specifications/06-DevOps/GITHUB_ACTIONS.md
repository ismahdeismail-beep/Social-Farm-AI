# GitHub Actions

## Workflows

| Workflow | Trigger | Description |
| :--- | :--- | :--- |
| **CI/CD** | Push to main/develop | Full pipeline execution |
| **Dependency Updates** | Scheduled | Automated dependency updates |
| **Release Tagging** | Tag push | Release build and deployment |
| **Docs Validation** | PR | Validate documentation integrity |
| **Security Scanning** | Scheduled/PR | Vulnerability scanning |

All workflows are defined in `.github/workflows/` and utilize reusable actions for consistency.
