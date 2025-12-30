from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

class Base(DeclarativeBase):
    pass

engine = None
SessionLocal = None


def get_engine():
    global engine, SessionLocal

    if engine is None:
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )

        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        )

    return engine


def get_db():
    if SessionLocal is None:
        get_engine()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
