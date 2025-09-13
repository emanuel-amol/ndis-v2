# app/main.py
from __future__ import annotations

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.api.v1.api import api_router


app = FastAPI(title="NDIS API", version="1.0.0")

# CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific domains in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Simple error logging middleware
@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.error("UNHANDLED ERROR: %s", e, exc_info=True)
        raise


@app.on_event("startup")
def create_tables() -> None:
    """
    Ensure all model modules are imported so SQLAlchemy can configure
    relationships (especially string-based ones) before create_all().
    """
    # Import submodules so mappers are registered
    # If you have a User model, import it too so back_populates resolves.
    try:
        from app.models import user  # noqa: F401
    except Exception:
        # It's fine if there's no user model
        pass

    from app.models import referral as _referral  # noqa: F401
    from app.models import email_log as _email_log  # noqa: F401

    Base.metadata.create_all(bind=engine)


# Mount API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/healthz")
def healthcheck():
    return {"status": "ok"}
