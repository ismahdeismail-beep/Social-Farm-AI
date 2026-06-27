# CI/CD Documentation — Social Farm AI OS

## Overview

This document describes the CI/CD pipeline for Social Farm AI OS, including automated testing, security scanning, and deployment workflows.

## Pipeline Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Commit    │───▶│    Lint     │───▶│    Test     │───▶│   Build     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                              │                  │
                                              ▼                  ▼
                                       ┌─────────────┐    ┌─────────────┐
                                       │   Security  │    │  Deploy     │
                                       │   Scan      │    │  (Staging)  │
                                       └─────────────┘    └─────────────┘
                                                                  │
                                                                  ▼
                                                           ┌─────────────┐
                                                           │  Deploy     │
                                                           │  (Production)│
                                                           └─────────────┘
```

## Workflows

### 1. CI Pipeline (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main`

**Jobs:**

#### Backend
- **Runner:** Ubuntu latest
- **Services:** PostgreSQL 15, Redis 7
- **Steps:**
  1. Checkout code
  2. Setup Python 3.11
  3. Install dependencies
  4. Lint with Ruff
  5. Format check with Ruff
  6. Type check with mypy
  7. Run tests with pytest
  8. Upload coverage to Codecov

#### Frontend
- **Runner:** Ubuntu latest
- **Steps:**
  1. Checkout code
  2. Setup Node.js 20
  3. Install dependencies (npm ci)
  4. Lint with ESLint
  5. Type check with TypeScript
  6. Build Next.js app
  7. Run tests

#### Security
- **Runner:** Ubuntu latest
- **Steps:**
  1. Checkout code
  2. Run Trivy vulnerability scanner
  3. Fail on critical/high vulnerabilities

#### Docker
- **Runner:** Ubuntu latest
- **Needs:** Backend, Frontend
- **Condition:** Only on `main` branch
- **Steps:**
  1. Checkout code
  2. Setup Docker Buildx
  3. Build backend image
  4. Build frontend image

### 2. Deployment Pipeline

#### Staging
- **Trigger:** Push to `develop` branch
- **Needs:** Backend, Frontend, Security
- **Steps:**
  1. Deploy to Render (staging)
  2. Deploy to Vercel (staging)

#### Production
- **Trigger:** Push to `main` branch
- **Needs:** Backend, Frontend, Security, Docker
- **Environment:** Production
- **Steps:**
  1. Deploy to Render (production)
  2. Deploy to Vercel (production)

## Environment Variables

### CI/CD

| Variable | Description | Source |
|----------|-------------|--------|
| `DATABASE_URL` | PostgreSQL connection | GitHub Secrets |
| `REDIS_URL` | Redis connection | GitHub Secrets |
| `JWT_SECRET` | JWT signing secret | GitHub Secrets |
| `CODECOV_TOKEN` | Codecov upload token | GitHub Secrets |

### Deployment

| Variable | Description | Target |
|----------|-------------|--------|
| `DATABASE_URL` | PostgreSQL connection | Render |
| `REDIS_URL` | Redis connection | Render |
| `JWT_SECRET` | JWT signing secret | Render |
| `CORS_ORIGINS` | Allowed origins | Render |
| `NEXT_PUBLIC_API_URL` | Backend API URL | Vercel |

## Branch Strategy

### Main Branch
- Production-ready code
- Protected branch
- Requires PR approval
- All CI checks must pass

### Develop Branch
- Integration branch
- Staging deployments
- Feature branches merge here

### Feature Branches
- Named: `feat/`, `fix/`, `docs/`, `refactor/`
- Branch from `develop`
- Merge back to `develop`

## Pull Request Process

1. **Create PR** from feature branch to `develop`
2. **Automated checks:**
   - Linting passes
   - Tests pass
   - Security scan passes
   - Build succeeds
3. **Code review** by at least one maintainer
4. **Merge** after approval
5. **Automatic deployment** to staging

## Security Scanning

### Static Analysis
- **Python:** Bandit, Safety
- **JavaScript:** ESLint Security Plugin
- **Dependencies:** Dependabot, Snyk

### Dynamic Analysis
- **DAST:** OWASP ZAP (scheduled)
- **Container:** Trivy (in CI)
- **Infrastructure:** Checkov (in CI)

### Secret Scanning
- **TruffleHog:** Scans for secrets in code
- **GitGuardian:** Monitors for leaked credentials

## Monitoring & Alerting

### CI/CD Metrics
- Build success rate
- Test coverage
- Deployment frequency
- Lead time for changes

### Alerts
- Failed builds (Slack)
- Security vulnerabilities (Email)
- Deployment failures (Slack, Email)

## Rollback Procedures

### Backend (Render)
1. Go to Render Dashboard
2. Select service
3. Click "Manual Deploy"
4. Select previous successful deployment

### Frontend (Vercel)
1. Go to Vercel Dashboard
2. Select project
3. Go to "Deployments"
4. Click "Promote to Production" on previous deployment

### Docker
```bash
# Rollback to previous version
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

## Performance Optimization

### Build Optimization
- Parallel job execution
- Dependency caching
- Docker layer caching
- Incremental builds

### Test Optimization
- Test parallelization
- Test splitting
- Failed test retry
- Flaky test detection

## Troubleshooting

### Common Issues

#### Build Fails
- Check dependency versions
- Verify environment variables
- Review build logs

#### Tests Fail
- Check test database connection
- Verify mock configurations
- Review test environment

#### Deployment Fails
- Check service health
- Verify environment variables
- Review deployment logs

### Debug Commands

```bash
# Check CI status
gh run list

# Download logs
gh run view <run-id> --log

# Re-run failed jobs
gh run rerun <run-id> --failed
```

## Best Practices

1. **Keep CI fast** - Optimize build and test times
2. **Fail fast** - Run fastest checks first
3. **Parallelize** - Run independent jobs in parallel
4. **Cache aggressively** - Dependencies, build artifacts
5. **Monitor metrics** - Track build times, success rates
6. **Document changes** - Update this guide when modifying pipelines

## Contact

- **DevOps Team:** devops@socialfarm-ai.com
- **CI/CD Issues:** GitHub Issues
- **Emergencies:** [Emergency Contact]