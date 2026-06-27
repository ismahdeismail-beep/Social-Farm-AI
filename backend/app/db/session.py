import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./social_farm_ai.db"
)

_engine = None
_SessionLocal = None


def _get_engine():
    global _engine
    if _engine is None:
        connect_args = {}
        if DATABASE_URL.startswith("sqlite"):
            connect_args["check_same_thread"] = False
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
    return _engine


def _get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_get_engine())
    return _SessionLocal


class _LazySessionLocal:
    """Lazy proxy that creates the session factory only when first accessed."""
    def __getattr__(self, name):
        return getattr(_get_session_local(), name)

    def __call__(self, *args, **kwargs):
        return _get_session_local()(*args, **kwargs)


SessionLocal = _LazySessionLocal()
engine = None


def get_engine():
    """Get the SQLAlchemy engine (created lazily)."""
    return _get_engine()


def get_db():
    db = _get_session_local()()
    try:
        yield db
    finally:
        db.close()
