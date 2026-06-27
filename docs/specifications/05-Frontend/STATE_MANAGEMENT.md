# Frontend Specification: STATE_MANAGEMENT

## Global State (Zustand)
Used for transient UI state that must be shared globally (e.g., Theme, Command Palette visibility, Sidebar state, User Preferences).

## Server State (TanStack Query)
Used for all data fetching and server-side synchronization.
- Automatic caching.
- Background refetching.
- Optimistic updates.
- Loading/Error state management.

## Guidelines
- Avoid putting API responses directly into Zustand.
- Use TanStack Query for all server-side data synchronization.
