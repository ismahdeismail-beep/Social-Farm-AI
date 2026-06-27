# Frontend Specification: ROUTING

## Purpose
Define the navigation structure using Next.js App Router conventions.

## Conventions
- **Public Routes:** `/login`, `/register`, `/forgot-password`.
- **Protected Routes:** `/dashboard`, `/ai-studio`, `/media-factory`, etc.
- **Nested Layouts:** Used to maintain UI consistency for modules (e.g., `dashboard/layout.tsx` for main sidebar).
- **Dynamic Routes:** `/[workspaceId]/[brandId]/projects/[projectId]`.

## Error Handling
- Use `error.tsx` for component-level errors.
- Use `not-found.tsx` for 404 handling at module level.
