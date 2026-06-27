# API ARCHITECTURE

## Purpose
Standardizes REST API communication.

## Standards
- **Version:** `/api/v1/...`
- **Methodology:** Use standard HTTP verbs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
- **Response Structure:** `{ "success": boolean, "data": {}, "error": {} }`
- **Pagination:** `?page=1&size=20` (Cursor-based for large sets).

## Security
- API-level JWT authentication.
- Scoped permissions enforced at the controller level.
- Rate limiting per API Key or User ID.
