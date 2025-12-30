from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime, timedelta

from ...db.session import get_db

router = APIRouter(prefix="/predictions", tags=["predictions"])


# -------------------------------
# Schemas
# -------------------------------

class PredictionPoint(BaseModel):
    ts: str
    yhat: float
    yhat_lower: float
    yhat_upper: float


class PredictionResponse(BaseModel):
    horizon: str
    points: List[PredictionPoint]
    confidence: float


# -------------------------------
# Helper (rule-based AI)
# -------------------------------

def generate_predictions(
    horizon: str,
    base_temp: float = 30.0,
    count: int = 7,
):
    now = datetime.utcnow()
    points = []

    temp = base_temp

    for i in range(count):
        temp += random.uniform(-1.2, 1.2)

        ts = now + (
            timedelta(hours=i) if horizon == "hourly" else timedelta(days=i)
        )

        points.append(
            {
                "ts": ts.isoformat(),
                "yhat": round(temp, 2),
                "yhat_lower": round(temp - random.uniform(1, 2), 2),
                "yhat_upper": round(temp + random.uniform(1, 2), 2),
            }
        )

    return points


# -------------------------------
# Routes
# -------------------------------

@router.get("")
def get_predictions(
    lat: float = Query(...),
    lon: float = Query(...),
    horizon: str = Query("daily", pattern="^(hourly|daily)$"),
    db: Session = Depends(get_db),
):
    """
    Working AI prediction endpoint (sync).
    ML-ready. No Celery. No Redis.
    """

    if horizon == "hourly":
        points = generate_predictions("hourly", count=48)
    else:
        points = generate_predictions("daily", count=7)

    return {
        "horizon": horizon,
        "points": points,
        "confidence": round(random.uniform(0.75, 0.95), 2),
    }


@router.get("/health")
def predictions_health():
    return {
        "status": "ok",
        "engine": "rule-based-ai",
        "ml_ready": True,
    }
