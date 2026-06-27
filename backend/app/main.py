"""
Social Farm AI Backend — FastAPI Application Entry Point.

Initializes the FastAPI app, configures middleware,
mounts API routers, and provides health endpoints.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from datetime import datetime, timezone

from app.api import api_router

app = FastAPI(
    title="Social Farm AI OS",
    description="AI-powered social media content creation, research, trend intelligence, "
                "planning, publishing, analytics, and multi-agent orchestration platform.",
    version="0.3.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000"
    ).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Mount API router
# ---------------------------------------------------------------------------
app.include_router(api_router)

# ---------------------------------------------------------------------------
# Global health endpoint (outside /api prefix for load-balancer checks)
# ---------------------------------------------------------------------------


@app.get("/health")
async def root_health():
    return {
        "status": "healthy",
        "service": "social-farm-ai-backend",
        "version": "0.3.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Request logging middleware (optional, basic)
# ---------------------------------------------------------------------------


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = datetime.now(timezone.utc)
    response = await call_next(request)
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    # Only log in debug mode to avoid noise
    if os.getenv("DEBUG", "").lower() in ("1", "true", "yes"):
        print(
            f"[{datetime.now(timezone.utc).isoformat()}] "
            f"{request.method} {request.url.path} -> {response.status_code} "
            f"({elapsed:.3f}s)"
        )
    return response


# ---------------------------------------------------------------------------
# Global exception handler
# ---------------------------------------------------------------------------


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "path": str(request.url.path),
        },
    )


# ---------------------------------------------------------------------------
# Entry point for direct execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload_enabled = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload_enabled,
        log_level="info",
    )
