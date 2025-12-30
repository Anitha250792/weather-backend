from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather Forecast AI Backend"
    API_V1_PREFIX: str = "/api"

    SECRET_KEY: str = Field(default="dev-secret", env="SECRET_KEY")

    DATABASE_URL: str = Field(
        default="sqlite:///./weather_ai.db",
        env="DATABASE_URL"
    )

    # ✅ FIX IS HERE (typed field)
    CORS_ALLOW_ORIGINS: List[str] = [
        "http://localhost:5173",
        "https://weather-frontend-two-plum.vercel.app",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
