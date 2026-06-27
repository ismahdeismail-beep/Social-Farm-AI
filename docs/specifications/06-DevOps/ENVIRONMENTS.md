# Environments

## 1. Environment Definitions

| Environment | Purpose | Access | Data Sensitivity |
| :--- | :--- | :--- | :--- |
| **Local** | Individual developer machines | Developers | Low |
| **Development** | Feature development and testing | Developers | Low |
| **Testing** | Automated integration and QA | CI/CD, QA | Low |
| **Staging** | Production-like validation | CI/CD, Stakeholders | Medium |
| **Production** | Live end-user environment | Automated CD | High |
| **Preview** | Ephemeral PR environments | CI/CD | Low |

## 2. Configuration Differences
Configurations are managed via hierarchical files, with environment-specific overrides (e.g., `config.prod.yaml` overrides `config.base.yaml`). This ensures that environment-specific settings (e.g., database URLs, API keys) are correctly applied.

## 3. Promotion Workflow
Code is promoted through environments:
`Development` -> `Testing` -> `Staging` -> `Production`

Promotion requires:
1.  Successful CI/CD pipeline execution.
2.  Successful smoke tests in the target environment.
3.  For Production, manual approval from authorized personnel.
