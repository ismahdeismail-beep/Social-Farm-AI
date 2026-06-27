# Authorization Security

## 1. RBAC (Role-Based Access Control)
*   Roles: `SuperAdmin`, `Admin`, `Editor`, `Viewer`.
*   Permissions: Granular actions (e.g., `create_project`, `delete_media`).

## 2. Workspace Isolation
*   All resources are scoped to a `workspace_id`.
*   Middleware enforces `workspace_id` check on every request.

## 3. Privilege Escalation Prevention
*   Strict validation of user roles before performing administrative actions.
*   No user can assign a role higher than their own.
