# Social Farm AI OS

An intelligent content operations platform that transforms ideas into high-quality multimedia content through coordinated AI agents, structured workflows, and human oversight.

## 🚀 Features

- **AI Command Center** - Orchestrate AI agents, manage models, and monitor system health
- **Research Engine** - Deep research, trend analysis, and knowledge management
- **Content Strategy** - Plan campaigns, manage calendars, and discover opportunities
- **Multi-Provider AI** - OpenAI, Anthropic, Gemini, Grok, DeepSeek integration
- **Real-time Analytics** - Track performance metrics and generate insights
- **Collaborative Workspaces** - Team management and permissions

## 📁 Project Structure

```
Social-Farm-AI/
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core utilities
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── app/                # App Router pages
│   ├── components/         # React components
│   ├── stores/             # Zustand stores
│   ├── types/              # TypeScript types
│   └── package.json        # Node.js dependencies
├── api/                    # API layer (BFF)
├── docs/                   # Documentation
├── scripts/                # Automation scripts
├── infrastructure/         # Infrastructure configs
├── docker/                 # Docker configurations
├── docker-compose.yml      # Development Docker Compose
├── docker-compose.prod.yml # Production Docker Compose
├── Dockerfile.backend      # Backend Docker image
├── Dockerfile.frontend     # Frontend Docker image
├── render.yaml             # Render deployment
├── vercel.json             # Vercel deployment
└── pyproject.toml          # Python project config
```

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11)
- **Database:** PostgreSQL 15 + SQLAlchemy 2.0
- **Cache:** Redis 7
- **Task Queue:** Celery
- **Authentication:** JWT + Argon2

### Frontend
- **Framework:** Next.js 14 (App Router)
- **UI Library:** React 18
- **Language:** TypeScript 5
- **Styling:** Tailwind CSS 3
- **State Management:** Zustand + React Query

### Infrastructure
- **Containers:** Docker + Docker Compose
- **Deployment:** Render (backend) + Vercel (frontend)
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Social-Farm-AI.git
   cd Social-Farm-AI
   ```

2. **Start with Docker**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentation

- [Architecture Overview](./docs/ARCHITECTURE_CONSOLIDATION_REPORT.md)
- [API Documentation](./API_ARCHITECTURE.md)
- [Backend Architecture](./backend/BACKEND_ARCHITECTURE.md)
- [Frontend Architecture](./frontend/FRONTEND_ARCHITECTURE.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Security Policy](./SECURITY.md)
- [Performance Optimization](./PERFORMANCE_OPTIMIZATION.md)
- [Accessibility Guide](./ACCESSIBILITY.md)

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

### End-to-End Tests
```bash
cd tests
npm run test:e2e
```

## 🚀 Deployment

### Render (Backend)
1. Connect GitHub repository to Render
2. Create PostgreSQL database
3. Create Redis instance
4. Configure environment variables
5. Deploy

### Vercel (Frontend)
1. Import repository to Vercel
2. Configure framework preset (Next.js)
3. Set environment variables
4. Deploy

### Docker (Full Stack)
```bash
# Production
docker-compose -f docker-compose.prod.yml up -d

# With monitoring
docker-compose --profile monitoring -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE.md) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)