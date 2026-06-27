# AUTHORIZATION

## Purpose
Enforce Role-Based Access Control (RBAC).

## Implementation
- **Roles:** Defined in the `roles` table.
- **Permissions:** Granular strings (e.g., `content:create`, `brand:delete`).
- **Policy Enforcement:** Middleware validates user roles/permissions against requested resource.

## Ownership
Resources linked to a `workspace_id` or `brand_id` check if the user is authenticated in that scope.
