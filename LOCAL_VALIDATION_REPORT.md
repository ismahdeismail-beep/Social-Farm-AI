# Local Validation Report — Social Farm AI OS

## Executive Summary

This report documents the local end-to-end validation phase for Social Farm AI OS, including setup instructions, validation checklist, and troubleshooting guide.

---

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 20+ | Frontend runtime |
| PostgreSQL | 15+ | Database |
| Redis | 7+ | Caching (optional) |
| Git | Latest | Version control |

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Social-Farm-AI.git
cd Social-Farm-AI
```

---

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="sqlite:///./social_farm_ai.db"
export JWT_SECRET="your-secret-key"
export DEBUG="true"

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in new terminal)
cd frontend

# Install dependencies
npm install

# Set environment variables
export NEXT_PUBLIC_API_URL="http://localhost:8000"

# Start frontend development server
npm run dev
```

---

### 4. Database Setup (Optional - for PostgreSQL)

```bash
# Create database
createdb socialfarm

# Set DATABASE_URL
export DATABASE_URL="postgresql://user:password@localhost:5432/socialfarm"

# Run migrations (if available)
alembic upgrade head
```

---

## Validation Checklist

### Backend Validation

| Endpoint | Method | Expected Response | Status |
|----------|--------|-------------------|--------|
| `/health` | GET | `{"status": "healthy", ...}` | ⬜ |
| `/api/docs` | GET | Swagger UI | ⬜ |
| `/api/redoc` | GET | ReDoc UI | ⬜ |
| `/api/openapi.json` | GET | OpenAPI JSON | ⬜ |
| `/api/auth/register` | POST | User registered | ⬜ |
| `/api/auth/login` | POST | JWT token | ⬜ |
| `/api/ai/health` | GET | `{"status": "healthy", ...}` | ⬜ |
| `/api/research/health` | GET | `{"status": "healthy", ...}` | ⬜ |

---

### Frontend Validation

| Page | URL | Expected Behavior | Status |
|------|-----|-------------------|--------|
| Home | `http://localhost:3000` | Dashboard with navigation | ⬜ |
| AI Command Center | `http://localhost:3000/ai` | Chat interface | ⬜ |
| Research Engine | `http://localhost:3000/research` | Research dashboard | ⬜ |
| Content Strategy | `http://localhost:3000/strategy` | Strategy dashboard | ⬜ |
| Login | `http://localhost:3000/login` | Login form | ⬜ |
| Register | `http://localhost:3000/register` | Register form | ⬜ |

---

### API Integration Validation

| Test Case | Description | Expected Result | Status |
|-----------|-------------|-----------------|--------|
| Login Flow | Login with valid credentials | JWT token returned | ⬜ |
| Register Flow | Register new user | User created | ⬜ |
| AI Chat | Send message to AI | Response received | ⬜ |
| Research Query | Create research query | Query created | ⬜ |
| Strategy Generation | Generate strategy | Strategy created | ⬜ |

---

### Database Validation

| Test Case | Description | Expected Result | Status |
|-----------|-------------|-----------------|--------|
| User Creation | Create new user | User saved to DB | ⬜ |
| Organization Creation | Create organization | Organization saved | ⬜ |
| Workspace Creation | Create workspace | Workspace saved | ⬜ |
| Research Query | Create research query | Query saved | ⬜ |

---

## Health Endpoint Testing

### Main Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "social-farm-ai-backend",
  "version": "0.3.0",
  "timestamp": "2026-06-27T00:00:00Z"
}
```

---

### AI Health Endpoint

```bash
curl http://localhost:8000/api/ai/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "components": {
    "orchestrator": "healthy",
    "registry": "healthy",
    "router": "healthy",
    "memory": "healthy",
    "quality": "healthy"
  },
  "timestamp": "2026-06-27T00:00:00Z"
}
```

---

### Research Health Endpoint

```bash
curl http://localhost:8000/api/research/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "research-engine",
  "timestamp": "2026-06-27T00:00:00Z"
}
```

---

## API Documentation Testing

### Swagger UI

1. Open browser to `http://localhost:8000/api/docs`
2. Verify all endpoints are listed
3. Test endpoints using Swagger UI

---

### ReDoc

1. Open browser to `http://localhost:8000/api/redoc`
2. Verify documentation is rendered
3. Check all endpoints are documented

---

### OpenAPI JSON

1. Open browser to `http://localhost:8000/api/openapi.json`
2. Verify JSON is valid
3. Check all endpoints are included

---

## Frontend-Backend Communication

### Test API Calls

1. Open browser developer tools
2. Navigate to AI Command Center
3. Send a test message
4. Verify API call is made to backend
5. Check network tab for successful response

---

### Test CORS

1. Open browser console
2. Check for CORS errors
3. Verify requests are not blocked

---

## Troubleshooting

### Common Issues

#### Backend Won't Start

**Symptoms:**
- Port already in use
- Import errors
- Database connection failed

**Solutions:**
```bash
# Check if port is in use
netstat -ano | findstr :8000

# Kill process using port
taskkill /PID <PID> /F

# Check Python version
python --version

# Verify dependencies
pip list
```

---

#### Frontend Won't Start

**Symptoms:**
- Port already in use
- Node.js version mismatch
- Missing dependencies

**Solutions:**
```bash
# Check Node.js version
node --version

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules
npm install
```

---

#### API Connection Failed

**Symptoms:**
- CORS errors in browser
- Network errors
- Timeout errors

**Solutions:**
1. Verify backend is running on port 8000
2. Check `NEXT_PUBLIC_API_URL` is set correctly
3. Verify CORS configuration in backend

---

#### Database Connection Failed

**Symptoms:**
- Connection refused
- Authentication failed
- Database not found

**Solutions:**
1. Verify database is running
2. Check `DATABASE_URL` environment variable
3. Verify database credentials

---

### Debug Commands

```bash
# Check backend logs
# (Logs are printed to console in debug mode)

# Check frontend logs
# (Check browser developer tools)

# Test backend directly
curl -v http://localhost:8000/health

# Test database connection
python -c "from sqlalchemy import create_engine; engine = create_engine('sqlite:///./social_farm_ai.db'); print('Connected')"
```

---

## Performance Testing

### Load Testing (Optional)

```bash
# Install Apache Bench
# Windows: Download from Apache website
# macOS: brew install ab

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health
```

---

### Response Time Testing

```bash
# Test response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# curl-format.txt content:
#     time_namelookup:  %{time_namelookup}\n
#        time_connect:  %{time_connect}\n
#     time_appconnect:  %{time_appconnect}\n
#    time_pretransfer:  %{time_pretransfer}\n
#       time_redirect:  %{time_redirect}\n
#  time_starttransfer:  %{time_starttransfer}\n
#                     ----------\n
#          time_total:  %{time_total}\n
```

---

## Security Testing

### Authentication Testing

1. Test unauthenticated access to protected endpoints
2. Test invalid token handling
3. Test token expiration

```bash
# Test unauthenticated access
curl http://localhost:8000/api/ai/agents

# Expected: 401 Unauthorized

# Test with invalid token
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/api/ai/agents

# Expected: 401 Unauthorized
```

---

## Browser Testing

### Supported Browsers

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | Latest | ⬜ |
| Firefox | Latest | ⬜ |
| Safari | Latest | ⬜ |
| Edge | Latest | ⬜ |

---

### Responsive Testing

| Device | Resolution | Status |
|--------|------------|--------|
| Desktop | 1920x1080 | ⬜ |
| Laptop | 1366x768 | ⬜ |
| Tablet | 768x1024 | ⬜ |
| Mobile | 375x667 | ⬜ |

---

## Validation Summary

### Backend

- [ ] Backend starts without errors
- [ ] Health endpoint returns 200
- [ ] API documentation loads correctly
- [ ] Authentication flow works
- [ ] Database operations work

---

### Frontend

- [ ] Frontend starts without errors
- [ ] All pages load correctly
- [ ] API calls succeed
- [ ] No console errors
- [ ] Responsive design works

---

### Integration

- [ ] Frontend communicates with backend
- [ ] Authentication works end-to-end
- [ ] AI chat works end-to-end
- [ ] Research queries work end-to-end
- [ ] Strategy generation works end-to-end

---

## Conclusion

The local validation phase provides a comprehensive checklist for testing the complete application locally. Follow the setup instructions and validation checklist to ensure all components are working correctly before proceeding to deployment.

**Status:** ✅ Local Validation Report Complete