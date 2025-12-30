from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

from ..core.config import settings


class Base(DeclarativeBase):
    pass


DATABASE_URL = settings.DATABASE_URL

# ✅ Force SSL for Render Postgres
engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
    connect_args={
        "sslmode": "require"
    }
)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
