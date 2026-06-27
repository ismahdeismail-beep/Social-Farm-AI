"""
API router aggregation.

Mounts all sub-routers onto the main API gateway.
"""

from fastapi import APIRouter
from app.api.ai import router as ai_router
from app.api.auth.endpoints import router as auth_router
from app.api.organizations.endpoints import router as organizations_router
from app.api.workspaces.endpoints import router as workspaces_router
from app.api.research import router as research_router
from app.api.strategy import router as strategy_router

api_router = APIRouter(prefix="/api")

# Mount all sub-routers
api_router.include_router(ai_router)       # /api/ai/**
api_router.include_router(auth_router)      # /api/auth/**
api_router.include_router(organizations_router)  # /api/organizations/**
api_router.include_router(workspaces_router)     # /api/workspaces/**
api_router.include_router(research_router)       # /api/research/**
api_router.include_router(strategy_router)       # /api/strategy/**
