# TECH_STACK
# TECHNOLOGY STACK
Version: 1.0
Status: Active
Classification: Core Specification

---

# Purpose

This document defines the approved technology stack for Social Farm AI OS.

Every implementation must use the technologies defined here unless an architectural decision formally approves an alternative.

The goals of this technology stack are:

- Maintainability
- Performance
- Scalability
- Security
- Developer Experience
- AI Integration

---

# Technology Selection Principles

Technologies selected for this project should:

- Be actively maintained.
- Have strong documentation.
- Possess large developer communities.
- Support long-term scalability.
- Be production proven.
- Integrate well with the rest of the stack.
- Minimize vendor lock-in whenever practical.

---

# High-Level Stack

| Layer | Technology |
|---------|------------|
| Frontend | Next.js |
| Language | TypeScript |
| Backend | FastAPI |
| Backend Language | Python |
| Database | PostgreSQL |
| Cache | Redis |
| Queue | Redis / Celery |
| ORM | SQLAlchemy |
| Authentication | JWT + OAuth Ready |
| Storage | S3 Compatible Storage |
| AI Gateway | Multi-provider Routing |
| Media Processing | FFmpeg |
| Containerization | Docker |
| Reverse Proxy | Nginx |
| CI/CD | GitHub Actions |

---

# Frontend

## Framework

Next.js (App Router)

Reasons

- Server Components
- Performance
- SEO
- API Routes
- Production Ready

---

## Language

TypeScript

Reasons

- Type Safety
- Better Refactoring
- Improved Maintainability

---

## Styling

Tailwind CSS

Reasons

- Utility-first
- Fast Development
- Consistent Design

---

## Component Library

shadcn/ui

Reasons

- Accessible
- Modern
- Customizable
- Built on Radix UI

---

## Icons

Lucide Icons

Reasons

- Lightweight
- Consistent
- Open Source

---

## Forms

React Hook Form

Validation

Zod

---

## State Management

Zustand

Responsibilities

- User State
- Brand Context
- Application Settings
- UI State

---

## Server State

TanStack Query

Responsibilities

- API Requests
- Caching
- Synchronization
- Background Refresh

---

# Backend

## Framework

FastAPI

Reasons

- High Performance
- Async Support
- Automatic Documentation
- Type Validation

---

## Language

Python 3.12+

---

## API Documentation

OpenAPI

Swagger UI

ReDoc

---

## Validation

Pydantic

---

## ORM

SQLAlchemy

---

## Database Migration

Alembic

---

# Database

Primary Database

PostgreSQL

Reasons

- Reliable
- ACID Compliant
- Excellent Performance
- Mature Ecosystem

---

# Cache

Redis

Uses

- Sessions
- Caching
- Background Jobs
- Rate Limiting
- AI Context Cache

---

# Background Processing

Celery

Broker

Redis

Responsibilities

- AI Jobs
- Video Rendering
- Thumbnail Generation
- Scheduled Publishing
- Analytics Aggregation

---

# Authentication

Primary

JWT

Future Support

- Google OAuth
- GitHub OAuth
- Microsoft OAuth
- Apple Sign-In

---

# File Storage

Supported

- Local Storage (Development)
- Amazon S3
- Cloudflare R2
- MinIO
- Supabase Storage

Storage should be abstracted behind a common interface.

---

# AI Layer

The system shall support multiple AI providers.

Approved Providers

- OpenAI
- Anthropic Claude
- Google Gemini
- xAI Grok
- OpenRouter
- Ollama (Local Models)

Provider selection should be configurable.

---

# AI Framework

Preferred Libraries

- LangChain (Optional)
- LiteLLM (Recommended)
- Instructor
- Pydantic AI (Evaluate)

The architecture should not depend exclusively on any single AI framework.

---

# Image Generation

Supported Providers

- OpenAI Images
- Google Imagen (Future)
- Stable Diffusion
- Flux Models

---

# Voice Generation

Preferred Providers

- ElevenLabs
- OpenAI Audio
- Azure Speech
- Local TTS (Future)

---

# Video Processing

Primary Tool

FFmpeg

Responsibilities

- Rendering
- Compression
- Subtitle Burn-in
- Audio Mixing
- Format Conversion

---

# Web Scraping

Preferred Tools

- Playwright
- BeautifulSoup
- Requests

Use only where legally and technically appropriate.

---

# Search

Recommended

- Tavily API
- SerpAPI
- Brave Search API

Search providers should be interchangeable.

---

# Analytics

Future Support

- PostHog
- Plausible
- Google Analytics

Internal analytics should remain the primary source of operational metrics.

---

# Notifications

Supported

- Email
- In-App Notifications
- Webhooks

Future

- SMS
- Push Notifications
- Slack
- Discord

---

# Development Tools

IDE

- VS Code

AI Coding

- OpenCode
- Claude
- ChatGPT

Version Control

- Git

Repository

- GitHub

---

# Testing

Frontend

- Vitest
- Playwright

Backend

- Pytest

API

- HTTPX

Coverage Target

Minimum 80%

Target 90%+

---

# Code Quality

Formatting

Frontend

- Prettier

Backend

- Black

Linting

Frontend

- ESLint

Backend

- Ruff

Type Checking

Frontend

- TypeScript

Backend

- MyPy

---

# DevOps

Containerization

- Docker

Reverse Proxy

- Nginx

Continuous Integration

- GitHub Actions

Monitoring

- Prometheus
- Grafana

Logging

- Loki

---

# Security

Secrets

Environment Variables

Encryption

TLS

HTTPS Everywhere

Password Hashing

Argon2

Input Validation

Pydantic

Rate Limiting

Redis

Audit Logging

Enabled

---

# Documentation

Markdown

OpenAPI

Architecture Decision Records (ADR)

Draw.io

Mermaid Diagrams

---

# Browser Support

Latest versions of:

- Chrome
- Edge
- Firefox
- Safari

Responsive Support

- Desktop
- Tablet
- Mobile

---

# Future Technology Evaluation

The following technologies may be evaluated in future releases:

- Kubernetes
- Temporal
- Apache Kafka
- ClickHouse
- Vector Databases
- WebAssembly
- Electron
- React Native

Evaluation does not imply adoption.

---

# Technology Governance

Only technologies approved in this document should be introduced into the project.

New dependencies require:

- Architectural review.
- Security review.
- License verification.
- Compatibility assessment.
- Documentation update.

---

# Revision History

| Version | Date | Summary |
|----------|------|---------|
| 1.0 | Initial Release | Approved technology stack for Social Farm AI OS |

---

# End of Document