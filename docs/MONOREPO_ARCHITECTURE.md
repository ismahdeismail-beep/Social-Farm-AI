# Monorepo Architecture — Social Farm AI OS

## Overview

This document describes the monorepo architecture for Social Farm AI OS, including workspace configuration, dependency management, and build optimization.

## Architecture Principles

### 1. Single Repository
- All code lives in one repository
- Shared versioning and releases
- Unified CI/CD pipeline

### 2. Workspace Isolation
- Clear separation between packages
- Independent deployment capability
- Shared types and utilities

### 3. Dependency Boundaries
- No circular dependencies
- Clear dependency hierarchy
- Shared dependencies at root

## Directory Structure

```
Social-Farm-AI/
├── packages/
│   ├── backend/           # FastAPI backend
│   ├── frontend/          # Next.js frontend
│   ├── shared/            # Shared types and utilities
│   └── api/               # API layer (BFF)
├── tools/
│   ├── scripts/           # Build and utility scripts
│   └── configs/           # Shared configurations
├── docs/                  # Documentation
├── tests/                 # End-to-end tests
├── package.json           # Root package.json
├── pnpm-workspace.yaml    # Workspace configuration
└── turbo.json             # Turborepo configuration
```

## Workspace Configuration

### pnpm-workspace.yaml

```yaml
packages:
  - 'packages/*'
  - 'tools/*'
```

### Root package.json

```json
{
  "name": "social-farm-ai",
  "private": true,
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "test": "turbo test",
    "lint": "turbo lint",
    "format": "prettier --write ."
  },
  "devDependencies": {
    "turbo": "^1.10.0",
    "prettier": "^3.0.0",
    "eslint": "^8.0.0"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}
```

### turbo.json

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env"],
  "globalEnv": ["NODE_ENV"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["build"]
    }
  }
}
```

## Package Dependencies

### Dependency Graph

```
                    ┌─────────────┐
                    │   shared    │
                    └─────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌───────────┐    ┌───────────┐    ┌───────────┐
    │  backend  │    │    api    │    │ frontend  │
    └───────────┘    └───────────┘    └───────────┘
```

### Package Responsibilities

#### shared
- TypeScript type definitions
- Shared utilities
- Constants and configurations
- No external dependencies

#### backend
- FastAPI application
- Database models
- Business logic
- API endpoints

#### api
- API Gateway (BFF)
- Request/Response transformation
- Authentication middleware
- Rate limiting

#### frontend
- Next.js application
- React components
- State management
- UI/UX implementation

## Build Optimization

### Caching Strategy

1. **Local Cache**
   - Turborepo local cache
   - Node modules cache
   - Build artifacts cache

2. **Remote Cache**
   - Turborepo remote cache
   - CI/CD cache sharing
   - Team-wide cache

### Build Pipeline

```bash
# Development
pnpm dev            # Start all packages in development mode

# Production
pnpm build          # Build all packages
pnpm test           # Run all tests
pnpm lint           # Lint all packages
```

### Parallel Execution

Turborepo automatically parallelizes builds based on the dependency graph:

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

## Dependency Management

### Version Strategy

- **Semantic Versioning** for all packages
- **Lock file** for deterministic builds
- **Regular updates** for security patches

### Shared Dependencies

Root-level shared dependencies:

```json
{
  "devDependencies": {
    "typescript": "^5.0.0",
    "prettier": "^3.0.0",
    "eslint": "^8.0.0"
  }
}
```

### Package-specific Dependencies

Each package manages its own dependencies:

```json
// packages/backend/package.json
{
  "dependencies": {
    "fastapi": "^0.100.0",
    "sqlalchemy": "^2.0.0"
  }
}
```

## Development Workflow

### Adding a New Package

1. Create package directory:
   ```bash
   mkdir packages/new-package
   cd packages/new-package
   ```

2. Initialize package:
   ```bash
   pnpm init
   ```

3. Add to workspace:
   ```yaml
   # pnpm-workspace.yaml
   packages:
     - 'packages/*'
   ```

4. Add dependencies:
   ```bash
   pnpm add <dependency>
   ```

### Cross-Package Development

1. **Linking packages**
   ```bash
   # In consuming package
   pnpm add @social-farm-ai/shared
   ```

2. **Using shared types**
   ```typescript
   import { User } from '@social-farm-ai/shared';
   ```

### Testing Strategy

1. **Unit Tests**
   - Each package has its own test suite
   - Run with package-specific commands

2. **Integration Tests**
   - Test package interactions
   - Located in `tests/` directory

3. **E2E Tests**
   - Full application testing
   - Playwright for browser testing

## CI/CD Integration

### Pipeline Structure

```yaml
# .github/workflows/ci.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Build
        run: pnpm build
      
      - name: Test
        run: pnpm test
      
      - name: Lint
        run: pnpm lint
```

### Caching in CI

```yaml
- name: Cache node_modules
  uses: actions/cache@v3
  with:
    path: |
      node_modules
      apps/*/node_modules
      packages/*/node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/pnpm-lock.yaml') }}
```

## Performance Considerations

### Build Times

- **Incremental builds** - Only rebuild changed packages
- **Parallel execution** - Build independent packages simultaneously
- **Caching** - Reuse previous build artifacts

### Development Experience

- **Hot reload** - Fast refresh for frontend
- **Watch mode** - Auto-rebuild on changes
- **Shared types** - Instant type checking

## Best Practices

### Do's

✅ **Use shared types** for cross-package communication
✅ **Keep packages focused** - Single responsibility
✅ **Document dependencies** - Clear dependency graph
✅ **Use workspace protocol** for local packages
✅ **Regular dependency updates** - Security patches

### Don'ts

❌ **Don't create circular dependencies**
❌ **Don't share implementation details**
❌ **Don't skip build caching**
❌ **Don't ignore TypeScript errors**
❌ **Don't commit lock file changes without reason**

## Troubleshooting

### Common Issues

#### Build Fails
```bash
# Clear cache and rebuild
pnpm clean
pnpm install
pnpm build
```

#### Type Errors
```bash
# Rebuild shared types
cd packages/shared
pnpm build
```

#### Dependency Issues
```bash
# Clean install
rm -rf node_modules
rm pnpm-lock.yaml
pnpm install
```

### Debug Commands

```bash
# Check dependency graph
pnpm why <package>

# List all packages
pnpm list --depth 0

# Check for circular dependencies
madge --circular packages/*
```

## Migration Guide

### From npm to pnpm

1. Install pnpm:
   ```bash
   npm install -g pnpm
   ```

2. Remove node_modules:
   ```bash
   rm -rf node_modules
   ```

3. Install dependencies:
   ```bash
   pnpm install
   ```

4. Update scripts:
   ```json
   {
     "scripts": {
       "dev": "pnpm dev",
       "build": "pnpm build"
     }
   }
```

## Resources

- [Turborepo Documentation](https://turbo.build/repo/docs)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Monorepo Best Practices](https://monorepo.tools/)