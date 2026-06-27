# Performance Optimization — Social Farm AI OS

## Overview

This document covers performance optimization strategies for the backend, frontend, database, and infrastructure.

## Backend Optimization

### 1. Async/Await

Use async operations for I/O-bound tasks:

```python
# ❌ Synchronous
def get_users():
    return db.query(User).all()

# ✅ Asynchronous
async def get_users():
    result = await db.execute(select(User))
    return result.scalars().all()
```

### 2. Connection Pooling

Configure SQLAlchemy connection pooling:

```python
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,        # Number of persistent connections
    max_overflow=10,     # Extra connections when pool is full
    pool_timeout=30,     # Seconds to wait for a connection
    pool_recycle=1800,   # Recycle connections after 30 minutes
    pool_pre_ping=True,  # Verify connections before using
)
```

### 3. Caching

Implement Redis caching for frequently accessed data:

```python
from redis import asyncio as aioredis

redis = aioredis.from_url(REDIS_URL)

async def get_user(user_id: int):
    # Check cache first
    cached = await redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Fetch from database
    user = await db.get(User, user_id)
    
    # Cache for 5 minutes
    await redis.setex(
        f"user:{user_id}",
        300,
        json.dumps(user.__dict__)
    )
    
    return user
```

### 4. Background Tasks

Use Celery for long-running tasks:

```python
from celery import Celery

celery_app = Celery("tasks", broker=REDIS_URL)

@celery_app.task
def process_research_query(query_id: int):
    # Long-running processing
    pass

# In API endpoint
@router.post("/research")
async def create_research(background_tasks: BackgroundTasks):
    task = process_research_query.delay(query_id)
    return {"task_id": task.id}
```

### 5. Response Compression

Enable gzip compression:

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## Frontend Optimization

### 1. Code Splitting

Use dynamic imports for heavy components:

```typescript
// ❌ Static import
import AICommandCenter from './components/AICommandCenter';

// ✅ Dynamic import
const AICommandCenter = dynamic(
  () => import('./components/AICommandCenter'),
  { loading: () => <Skeleton /> }
);
```

### 2. Image Optimization

Use Next.js Image component:

```tsx
import Image from 'next/image';

<Image
  src="/hero.png"
  alt="Hero"
  width={1200}
  height={600}
  placeholder="blur"
  blurDataURL={blurDataURL}
/>
```

### 3. Server Components

Use React Server Components for static content:

```tsx
// app/page.tsx (Server Component)
export default async function HomePage() {
  const data = await fetchData(); // Server-side fetch
  
  return (
    <div>
      <h1>{data.title}</h1>
      <ClientComponent data={data} />
    </div>
  );
}
```

### 4. ISR (Incremental Static Regeneration)

Cache pages for dynamic content:

```tsx
// app/blog/[id]/page.tsx
export const revalidate = 60; // Revalidate every 60 seconds

export default async function BlogPost({ params }) {
  const post = await getPost(params.id);
  return <Article post={post} />;
}
```

### 5. Zustand Optimization

Use selectors to minimize re-renders:

```typescript
// ❌ subscribing to entire store
const { user, settings, notifications } = useStore();

// ✅ subscribing to specific slices
const user = useStore(state => state.user);
const settings = useStore(state => state.settings);
```

## Database Optimization

### 1. Indexing

Add indexes for frequently queried columns:

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)  # ✅ Indexed
    created_at = Column(DateTime, index=True)         # ✅ Indexed
```

### 2. Query Optimization

Use eager loading to avoid N+1 queries:

```python
# ❌ N+1 queries
users = await db.execute(select(User))
for user in users.scalars():
    posts = await db.execute(
        select(Post).where(Post.user_id == user.id)
    )

# ✅ Single query with join
users = await db.execute(
    select(User).options(joinedload(User.posts))
)
```

### 3. Connection Pooling

Configure PgBouncer for connection pooling:

```ini
[databases]
socialfarm = host=localhost port=5432 dbname=socialfarm

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

### 4. Query Analysis

Use pg_stat_statements to identify slow queries:

```sql
SELECT query, calls, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

## Infrastructure Optimization

### 1. CDN

Use a CDN for static assets:

```nginx
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 2. Load Balancing

Configure load balancing for multiple backend instances:

```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      replicas: 3
```

### 3. Auto-scaling

Configure auto-scaling based on metrics:

```yaml
# render.yaml
services:
  - type: web
    scaling:
      minInstances: 1
      maxInstances: 10
      metrics:
        - type: cpu
          target: 70
```

## Monitoring

### 1. Backend Metrics

Track request duration, error rates, and throughput:

```python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('http_requests_total', 'Total requests')
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Request duration')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    REQUEST_COUNT.inc()
    REQUEST_DURATION.observe(duration)
    
    return response
```

### 2. Frontend Metrics

Track Core Web Vitals:

```typescript
import { onCLS, onFID, onLCP } from 'web-vitals';

onCLS(console.log);
onFID(console.log);
onLCP(console.log);
```

### 3. Database Metrics

Monitor connection pool and query performance:

```sql
-- Connection pool stats
SELECT * FROM pg_stat_activity;

-- Slow queries
SELECT * FROM pg_stat_statements;
```

## Performance Benchmarks

| Metric | Target | Current |
|--------|--------|---------|
| API Response Time | < 200ms | TBD |
| Page Load Time | < 2s | TBD |
| Time to Interactive | < 3s | TBD |
| Lighthouse Score | > 90 | TBD |
| Database Query Time | < 50ms | TBD |

## Optimization Checklist

### Backend
- [ ] Async/await for I/O operations
- [ ] Connection pooling configured
- [ ] Redis caching implemented
- [ ] Background tasks for long operations
- [ ] Response compression enabled
- [ ] Rate limiting configured

### Frontend
- [ ] Code splitting implemented
- [ ] Images optimized
- [ ] Server Components used
- [ ] ISR configured for dynamic pages
- [ ] State management optimized

### Database
- [ ] Indexes added for frequent queries
- [ ] Eager loading implemented
- [ ] Connection pooling configured
- [ ] Query analysis performed

### Infrastructure
- [ ] CDN configured
- [ ] Load balancing setup
- [ ] Auto-scaling configured
- [ ] Monitoring in place