# SERVICE ARCHITECTURE

## Purpose
Defines the business logic boundary.

## Boundaries
- **Domain Services:** Specific logic for one domain (e.g., `BrandService`).
- **Shared Services:** Cross-cutting functionality (e.g., `EmailService`, `FileService`).

## Dependency Rules
- Services call Repositories.
- Services do not call other Services directly (use Events/Queues for cross-domain orchestration).
- Services cannot access the Database directly.
