# Deployment Guide — Social Farm AI OS

## Overview

This guide covers deployment options for Social Farm AI OS:
- **Render** (Backend + PostgreSQL)
- **Vercel** (Frontend)
- **Docker** (Full stack)
- **Manual** (Self-hosted)

## Prerequisites

- Docker & Docker Compose
- Git
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for manual deployment)
- Redis 7+ (for manual deployment)

---

## 1. Render Deployment (Recommended)

### Backend

1. **Connect GitHub repository**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure service**
   - Name: `social-farm-ai-backend`
   - Runtime: Python
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Plan: Free (or Starter for production)

3. **Set environment variables**
   ```
   DATABASE_URL=postgresql://... (from Render PostgreSQL)
   REDIS_URL=redis://... (from Render Redis)
   JWT_SECRET=<generate-random-secret>
   CORS_ORIGINS=https://social-farm-ai.vercel.app
   DEBUG=false
   ```

4. **Create PostgreSQL database**
   - Click "New" → "PostgreSQL"
   - Name: `social-farm-db`
   - Copy the connection string to `DATABASE_URL`

5. **Create Redis instance**
   - Click "New" → "Redis"
   - Name: `social-farm-redis`
   - Copy the connection string to `REDIS_URL`

### Frontend

1. **Connect GitHub repository**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure project**
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Set environment variables**
   ```
   NEXT_PUBLIC_API_URL=https://social-farm-ai-backend.onrender.com
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel will automatically deploy on push to main

---

## 2. Docker Deployment

### Quick Start

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/Social-Farm-AI.git
cd Social-Farm-AI

# Copy environment file
cp .env.example .env

# Edit .env with your settings
# IMPORTANT: Set strong passwords for POSTGRES_PASSWORD, REDIS_PASSWORD, JWT_SECRET

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

### Environment Variables

Create `.env` file:

```bash
# Database
POSTGRES_DB=socialfarm
POSTGRES_USER=user
POSTGRES_PASSWORD=your-secure-password-here

# Redis
REDIS_PASSWORD=your-secure-redis-password-here

# Backend
JWT_SECRET=your-secure-jwt-secret-here
CORS_ORIGINS=https://your-domain.com

# Frontend
NEXT_PUBLIC_API_URL=http://backend:8000
```

### Commands

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Start with monitoring
docker-compose --profile monitoring -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop all services
docker-compose -f docker-compose.prod.yml down

# Restart a service
docker-compose -f docker-compose.prod.yml restart backend

# Scale backend (if needed)
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

---

## 3. Manual Deployment

### Backend

```bash
# Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv

# Clone and setup
git clone https://github.com/YOUR_USERNAME/Social-Farm-AI.git
cd Social-Farm-AI/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/socialfarm"
export REDIS_URL="redis://localhost:6379/0"
export JWT_SECRET="your-secret-key"

# Run migrations (if using Alembic)
alembic upgrade head

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend

```bash
# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Clone and setup
cd Social-Farm-AI/frontend

# Install dependencies
npm ci

# Set environment variables
export NEXT_PUBLIC_API_URL="http://localhost:8000"

# Build for production
npm run build

# Start server
npm start
```

### Database

```bash
# Install PostgreSQL 15
sudo apt install postgresql-15

# Create database and user
sudo -u postgres psql
CREATE DATABASE socialfarm;
CREATE USER user WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE socialfarm TO user;
\q
```

---

## 4. Nginx Configuration

### Basic Setup

```bash
# Install Nginx
sudo apt install nginx

# Copy configuration
sudo cp nginx/nginx.conf /etc/nginx/nginx.conf

# Restart Nginx
sudo systemctl restart nginx
```

### SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo systemctl status certbot.timer
```

---

## 5. Monitoring Setup

### Prometheus

```bash
# Start with monitoring profile
docker-compose --profile monitoring -f docker-compose.prod.yml up -d prometheus

# Access Prometheus
# http://localhost:9090
```

### Grafana

```bash
# Start with monitoring profile
docker-compose --profile monitoring -f docker-compose.prod.yml up -d grafana

# Access Grafana
# http://localhost:3001
# Default login: admin / admin
```

---

## 6. Troubleshooting

### Common Issues

#### Database Connection Failed

```bash
# Check PostgreSQL status
docker-compose -f docker-compose.prod.yml ps db

# View logs
docker-compose -f docker-compose.prod.yml logs db

# Test connection
docker-compose -f docker-compose.prod.yml exec db psql -U user -d socialfarm
```

#### Redis Connection Failed

```bash
# Check Redis status
docker-compose -f docker-compose.prod.yml ps redis

# View logs
docker-compose -f docker-compose.prod.yml logs redis

# Test connection
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
```

#### Backend Not Starting

```bash
# Check backend logs
docker-compose -f docker-compose.prod.yml logs backend

# Common issues:
# - Missing environment variables
# - Database connection refused
# - Port already in use
```

#### Frontend Build Failed

```bash
# Check frontend logs
docker-compose -f docker-compose.prod.yml logs frontend

# Common issues:
# - Missing NEXT_PUBLIC_API_URL
# - Node.js version mismatch
# - npm install failed
```

### Health Checks

```bash
# Check all services
docker-compose -f docker-compose.prod.yml ps

# Check backend health
curl http://localhost:8000/health

# Check frontend health
curl http://localhost:3000/
```

---

## 7. Security Checklist

- [ ] Strong passwords for all services
- [ ] JWT_SECRET is randomly generated
- [ ] CORS_ORIGINS is properly configured
- [ ] DEBUG is set to false in production
- [ ] SSL certificates are installed
- [ ] Firewall is properly configured
- [ ] Database is not exposed to public
- [ ] Redis is password protected
- [ ] Environment variables are not committed to git

---

## 8. Performance Tuning

### Backend

- Increase uvicorn workers: `--workers 4`
- Enable connection pooling
- Configure Redis caching
- Set up CDN for static assets

### Frontend

- Enable Next.js Image Optimization
- Configure ISR for static pages
- Enable gzip compression
- Set up CDN

### Database

- Add indexes for frequently queried columns
- Configure connection pooling
- Set up read replicas (if needed)
- Enable pg_stat_statements

---

## 9. Backup Strategy

### Database

```bash
# Backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U user socialfarm > backup.sql

# Restore
docker-compose -f docker-compose.prod.yml exec db psql -U user socialfarm < backup.sql
```

### Redis

```bash
# Backup
docker-compose -f docker-compose.prod.yml exec redis redis-cli BGSAVE

# Copy backup file
docker cp $(docker-compose -f docker-compose.prod.yml ps -q redis):/data/dump.rdb ./redis-backup.rdb
```

---

## 10. Support

For issues or questions:
- Check the [GitHub Issues](https://github.com/YOUR_USERNAME/Social-Farm-AI/issues)
- Review the [Documentation](./docs/)
- Contact the development team