from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.weather import WeatherRecord

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/latest")
def latest_weather(
    city: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
):
    return (
        db.query(WeatherRecord)
        .filter(WeatherRecord.city.ilike(city))
        .order_by(WeatherRecord.created_at.desc())
        .limit(10)
        .all()
    )
