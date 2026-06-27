# Role-Based Access Control (RBAC)

## 1. Role Definitions

| Role | Description | Permissions |
| :--- | :--- | :--- |
| **SuperAdmin** | Full system access | All |
| **Admin** | Workspace management | Manage users, brands, projects |
| **Editor** | Content creation | Create/Edit projects, media |
| **Viewer** | Read-only access | View projects, analytics |

## 2. Permission Inheritance
*   Permissions are additive.
*   `Admin` inherits all `Editor` permissions.
*   `Editor` inherits all `Viewer` permissions.

## 3. Implementation
*   Middleware checks user role against required permission for the endpoint.
