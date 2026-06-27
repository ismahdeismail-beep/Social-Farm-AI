# Frontend Specification: APPLICATION_STRUCTURE

## Philosophy
The `frontend/` directory follows a feature-based organization to ensure modularity and ease of maintenance as the application scales.

## Structure
```
frontend/
├── app/              # Next.js App Router (pages/layouts)
├── components/       # Shared UI components (shadcn/ui base)
├── features/         # Feature-specific modules (auth, trend, ai-studio)
├── hooks/            # Global/Shared React hooks
├── lib/              # Library configurations (tailwind, utils)
├── services/         # API clients, shared service logic
├── store/            # Zustand global state
├── types/            # Global TypeScript types
└── tests/            # E2E/Integration tests
```

## Dependency Rules
- Features *can* import from `components`, `hooks`, `lib`, `services`, `types`.
- Shared `components` *cannot* import from `features`.
- Modules *must* communicate via public interfaces exported from their index files.
