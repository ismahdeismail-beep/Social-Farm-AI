# API Architecture — Social Farm AI OS

## Overview

The API follows RESTful design principles with OpenAPI 3.0 specification. Built with FastAPI for automatic documentation and validation.

## Base URL

```
Production: https://api.socialfarm-ai.com
Staging: https://staging-api.socialfarm-ai.com
Development: http://localhost:8000
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Token Lifecycle

1. **Obtain Token:** `POST /api/auth/login`
2. **Use Token:** Include in request headers
3. **Refresh Token:** `POST /api/auth/refresh`
4. **Token Expiry:** 30 minutes (access), 7 days (refresh)

## API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Register new user | No |
| POST | `/login` | User login | No |
| POST | `/refresh` | Refresh access token | Yes |
| GET | `/me` | Get current user | Yes |
| PUT | `/me` | Update current user | Yes |
| POST | `/logout` | Logout user | Yes |

### AI (`/api/ai`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/chat` | AI chat completion | Yes |
| GET | `/providers` | List AI providers | Yes |
| GET | `/agents` | List AI agents | Yes |
| POST | `/agents` | Create AI agent | Yes |
| GET | `/tasks` | List AI tasks | Yes |
| POST | `/tasks` | Create AI task | Yes |
| GET | `/tasks/{id}` | Get task status | Yes |
| POST | `/workflows` | Create AI workflow | Yes |
| GET | `/workflows` | List AI workflows | Yes |

### Research (`/api/research`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/analyze` | Analyze content | Yes |
| GET | `/trends` | Get trending topics | Yes |
| POST | `/competitors` | Competitor analysis | Yes |
| GET | `/queries` | List research queries | Yes |
| POST | `/queries` | Create research query | Yes |
| GET | `/queries/{id}` | Get query results | Yes |

### Strategy (`/api/strategy`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/plan` | Create strategy plan | Yes |
| GET | `/plans` | List strategy plans | Yes |
| GET | `/plans/{id}` | Get strategy plan | Yes |
| PUT | `/plans/{id}` | Update strategy plan | Yes |
| DELETE | `/plans/{id}` | Delete strategy plan | Yes |
| GET | `/recommendations` | Get recommendations | Yes |
| POST | `/forecast` | Generate forecast | Yes |
| GET | `/campaigns` | List campaigns | Yes |
| POST | `/campaigns` | Create campaign | Yes |

### Workspaces (`/api/workspaces`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List workspaces | Yes |
| POST | `/` | Create workspace | Yes |
| GET | `/{id}` | Get workspace | Yes |
| PUT | `/{id}` | Update workspace | Yes |
| DELETE | `/{id}` | Delete workspace | Yes |
| POST | `/{id}/switch` | Switch active workspace | Yes |
| GET | `/{id}/members` | List workspace members | Yes |
| POST | `/{id}/members` | Add workspace member | Yes |
| DELETE | `/{id}/members/{user_id}` | Remove member | Yes |

### Organizations (`/api/organizations`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List organizations | Yes |
| POST | `/` | Create organization | Yes |
| GET | `/{id}` | Get organization | Yes |
| PUT | `/{id}` | Update organization | Yes |
| DELETE | `/{id}` | Delete organization | Yes |
| GET | `/{id}/members` | List org members | Yes |
| POST | `/{id}/members` | Add org member | Yes |
| DELETE | `/{id}/members/{user_id}` | Remove member | Yes |

## Request/Response Format

### Request Headers

```
Content-Type: application/json
Authorization: Bearer <token>
Accept: application/json
X-Request-ID: <unique-id> (optional)
```

### Success Response

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "id": "123",
    "name": "Example"
  }
}
```

### Error Response

```json
{
  "success": false,
  "message": "Validation error",
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ],
  "error_code": "VALIDATION_ERROR"
}
```

### Paginated Response

```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "pages": 5
  }
}
```

## HTTP Status Codes

| Code | Description | Usage |
|------|-------------|-------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

## Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| Global | 100 requests | 1 minute |
| Auth | 10 requests | 1 minute |
| AI | 10 requests | 1 minute |
| Read | 1000 requests | 1 minute |

Rate limit headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## Versioning

API versioning via URL path:

```
/api/v1/auth/login
/api/v2/auth/login
```

Current version: **v1**

## OpenAPI Specification

Access the OpenAPI documentation:

- **Swagger UI:** `https://api.socialfarm-ai.com/api/docs`
- **ReDoc:** `https://api.socialfarm-ai.com/api/redoc`
- **OpenAPI JSON:** `https://api.socialfarm-ai.com/api/openapi.json`

## Best Practices

### For Consumers

1. **Use appropriate HTTP methods**
2. **Handle pagination** for list endpoints
3. **Implement retry logic** with exponential backoff
4. **Cache responses** when possible
5. **Use request IDs** for debugging

### For Providers

1. **Validate all inputs** with Pydantic
2. **Return appropriate status codes**
3. **Include helpful error messages**
4. **Implement rate limiting**
5. **Log all requests** for debugging