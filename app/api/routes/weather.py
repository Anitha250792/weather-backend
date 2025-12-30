from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...models.weather import WeatherRecord

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/latest")
def latest_weather(city: str, db: Session = Depends(get_db)):
    try:
        return (
            db.query(WeatherRecord)
            .filter(WeatherRecord.city.ilike(city))
            .order_by(WeatherRecord.timestamp.desc())
            .limit(10)
            .all()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
