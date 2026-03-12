"""Application configuration."""
import os
from pathlib import Path

# Default SQLite for local dev; use DATABASE_URL for PostgreSQL in production
_raw_url = os.getenv(
    "DATABASE_URL",
    f"sqlite+aiosqlite:///{Path(__file__).resolve().parent.parent / 'hrms.db'}",
)
# Render/Railway give postgresql://; SQLAlchemy async needs postgresql+asyncpg://
if _raw_url.startswith("postgresql://") and "+asyncpg" not in _raw_url:
    DATABASE_URL = _raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = _raw_url

# Comma-separated origins for CORS (e.g. https://your-app.vercel.app); default allows localhost
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").strip().split(",")
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS if o.strip()]
