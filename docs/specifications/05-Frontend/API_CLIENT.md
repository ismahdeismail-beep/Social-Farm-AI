# Frontend Specification: API_CLIENT

## Purpose
Unified HTTP interface for communicating with the FastAPI backend.

## Design
- Built on `ky` or `axios` with interceptors.
- **Authentication:** Injects JWT from Auth Store/Cookies automatically.
- **Error Handling:** Centralized parsing of structured error responses.
- **Caching:** Handled by TanStack Query.
