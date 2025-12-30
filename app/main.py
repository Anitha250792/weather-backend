from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .api.routes.health import router as health_router
from .api.routes.auth import router as auth_router
from .api.routes.weather import router as weather_router
from .api.routes.recommendations import router as rec_router
from .api.routes.predictions import router as pred_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Aman Skies AI Backend",
        version="0.1.0",
    )

    # ---------------------------
    # CORS
    # ---------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---------------------------
    # Routers
    # ---------------------------
    app.include_router(health_router, prefix="/api")
    app.include_router(auth_router, prefix="/api")
    app.include_router(weather_router, prefix="/api")
    app.include_router(rec_router, prefix="/api")
    app.include_router(pred_router, prefix="/api")

    # ---------------------------
    # Root health check
    # ---------------------------
    @app.get("/")
    def root():
        return {"status": "ok"}

    return app


app = create_app()
