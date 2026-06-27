# Deployment Summary — Social Farm AI OS

## Deployment URLs

| Resource | URL |
|----------|-----|
| Frontend | `https://social-farm-ai.vercel.app` |
| Backend | `https://social-farm-ai-backend.onrender.com` |
| API Documentation | `https://social-farm-ai-backend.onrender.com/api/docs` |
| Health Endpoint | `https://social-farm-ai-backend.onrender.com/health` |

## Components

- **Frontend:** Next.js 14 on Vercel
- **Backend:** FastAPI (Python 3.11) on Render
- **Database:** PostgreSQL 15 on Render
- **Cache:** Redis 7 on Render (optional)

## Environment Variables

### Frontend (Vercel)
- `NEXT_PUBLIC_API_URL=https://social-farm-ai-backend.onrender.com`

### Backend (Render)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string (optional)
- `JWT_SECRET` - Randomly generated secret
- `CORS_ORIGINS=https://social-farm-ai.vercel.app,http://localhost:3000`
- `DEBUG=false`

## CI/CD

- **Platform:** GitHub Actions
- **Trigger:** Push to `main` or `develop` branch
- **Auto-deploy:** Render (backend) + Vercel (frontend)

## Status

- ✅ Backend deployed to Render
- ✅ Frontend deployed to Vercel
- ✅ CI/CD pipeline configured
- ✅ Auto-deploy enabled