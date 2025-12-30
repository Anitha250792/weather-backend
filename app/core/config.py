from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather Forecast AI Backend"

    DATABASE_URL: str
    OPENWEATHER_API_KEY: str

    CORS_ALLOW_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://weather-frontend-two-plum.vercel.app",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
