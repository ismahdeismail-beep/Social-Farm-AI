# Frontend Architecture — Social Farm AI OS

## Overview

The frontend is built with **Next.js 14** (App Router), **React 18**, **TypeScript 5**, and **Tailwind CSS 3**.

## Project Structure

```
frontend/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home page
│   ├── globals.css          # Global styles
│   ├── ai/                  # AI features
│   ├── api/                 # API routes (BFF)
│   ├── login/               # Auth pages
│   ├── register/            # Auth pages
│   ├── research/            # Research module
│   └── strategy/            # Strategy module
├── components/               # React components
│   └── ui/                  # UI components
│       ├── Button.tsx       # Button component
│       ├── Card.tsx         # Card component
│       └── Input.tsx        # Input component
├── stores/                   # Zustand stores
│   ├── strategy-store.ts    # Strategy state
│   └── research.ts          # Research state
├── types/                    # TypeScript types
│   └── index.ts             # Type definitions
├── tailwind.config.js       # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
├── next.config.mjs          # Next.js configuration
└── package.json             # Dependencies
```

## Key Features

### 1. App Router

- File-based routing
- Nested layouts
- Loading states
- Error boundaries
- Metadata API

### 2. React Server Components

- Server-side rendering
- Static generation
- Streaming SSR
- Reduced client-side JavaScript

### 3. State Management

- **Zustand** for global state
- **React Query** for server state
- Lightweight and performant

### 4. Styling

- **Tailwind CSS** for utility-first styling
- Custom color palette (brand colors)
- Dark mode support
- Responsive design

## Component Architecture

### UI Components

#### Button
```tsx
<Button variant="primary" size="md" isLoading={false}>
  Click me
</Button>
```

**Variants:** primary, secondary, outline, ghost, danger
**Sizes:** sm, md, lg

#### Card
```tsx
<Card variant="interactive">
  <CardHeader>Title</CardHeader>
  <CardContent>Content</CardContent>
  <CardFooter>Footer</CardFooter>
</Card>
```

**Variants:** default, interactive, bordered

#### Input
```tsx
<Input
  label="Email"
  type="email"
  placeholder="Enter your email"
  error="Invalid email"
/>
```

## Type System

### API Types

```typescript
interface ApiResponse<T> {
  success: boolean;
  message: string;
  data?: T;
  error?: string;
}

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
```

### Domain Types

- **User** - User accounts
- **AIAgent** - AI agent configuration
- **AITask** - AI task execution
- **Strategy** - Marketing strategy
- **Campaign** - Marketing campaign
- **ContentItem** - Content pieces

## State Management

### Zustand Stores

```typescript
// Example store
interface StrategyStore {
  strategies: Strategy[];
  currentStrategy: Strategy | null;
  loading: boolean;
  error: string | null;
  fetchStrategies: () => Promise<void>;
  setCurrentStrategy: (strategy: Strategy) => void;
}
```

### React Query

```typescript
// Example query
const { data, isLoading, error } = useQuery({
  queryKey: ['strategies'],
  queryFn: () => fetchStrategies(),
});
```

## Routing

### Page Structure

```
/                  # Home page
/login             # Login page
/register          # Register page
/ai                # AI Command Center
/research          # Research Engine
/strategy          # Content Strategy
/api/*             # API routes (BFF)
```

### Dynamic Routes

```typescript
// app/strategy/[id]/page.tsx
export default function StrategyPage({ params }: { params: { id: string } }) {
  return <StrategyDetail id={params.id} />;
}
```

## Styling

### Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          // ...
          900: '#0c4a6e',
        },
      },
    },
  },
};
```

### Global Styles

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 255, 255, 255;
  --background-rgb: 17, 24, 39;
}

body {
  color: rgb(var(--foreground-rgb));
  background: rgb(var(--background-rgb));
}
```

## Performance Optimization

### Code Splitting

- Dynamic imports for heavy components
- Route-based code splitting
- Lazy loading of non-critical components

### Image Optimization

- Next.js Image component
- Automatic WebP conversion
- Responsive images

### Caching

- React Query cache
- SWR for data fetching
- ISR for static pages

## Development

### Running Locally

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Code Quality

```bash
# Linting
npm run lint

# Type checking
npx tsc --noEmit

# Formatting
npx prettier --write .
```

### Testing

```bash
# Unit tests
npm test

# E2E tests
npx playwright test
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `NEXT_PUBLIC_APP_NAME` | Application name | `Social Farm AI OS` |

## Deployment

### Vercel

- Automatic deployment from GitHub
- Preview deployments for PRs
- Environment variables configured in dashboard
- Edge functions available

### Docker

```bash
# Build image
docker build -f Dockerfile.frontend -t social-farm-ai-frontend .

# Run container
docker run -p 3000:3000 social-farm-ai-frontend
```