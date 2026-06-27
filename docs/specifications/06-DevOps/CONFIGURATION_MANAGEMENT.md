# Configuration Management

## 1. Configuration Hierarchy
To ensure consistency and flexibility, we use a hierarchical configuration approach:
1.  **Default Configuration (`config.base.yaml`)**: Contains base settings applicable to all environments.
2.  **Environment Overrides (`config.{env}.yaml`)**: Contains environment-specific settings (e.g., `config.prod.yaml`, `config.staging.yaml`).
3.  **Runtime Configuration**: Dynamic settings (e.g., feature flags) loaded at runtime from a centralized service.

## 2. Environment Isolation
Each environment is strictly isolated. Configuration files for one environment are never used in another. Environment variables are injected at runtime, ensuring that sensitive data is not hardcoded.

## 3. Feature Flags
Feature flags are managed via a centralized service. This allows for:
*   **Safe Rollouts**: Enabling features for a subset of users.
*   **Rapid Disabling**: Quickly disabling problematic features without a full redeployment.
*   **A/B Testing**: Testing different versions of a feature.

## 4. Configuration Validation
All configuration files are validated against JSON schemas during the CI process. This prevents runtime errors caused by malformed configuration.

## 5. Runtime Configuration
Sensitive runtime configurations (e.g., database credentials, API keys) are injected via secure secret management systems (e.g., HashiCorp Vault, AWS Secrets Manager) and are never stored in plain text or committed to version control.
