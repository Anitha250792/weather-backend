from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .db.session import Base, engine
from .api.routes.weather import router as weather_router
from .api.routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def startup():
        import logging

        try:
            Base.metadata.create_all(bind=engine)
            logging.info("✅ Database connected and tables created")
        except Exception as e:
            logging.error("❌ Database connection failed: %s", e)

    app.include_router(health_router, prefix="/api")
    app.include_router(weather_router, prefix="/api")

    return app


app = create_app()
