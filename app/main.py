"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.database import engine, Base
from app.api.routes import employees, attendance


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup; optional teardown."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="HRMS Lite API",
    description="Lightweight HRMS – employees and attendance",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")


@app.get("/api/health")
async def health():
    """Health check for deployment."""
    return {"status": "ok"}
