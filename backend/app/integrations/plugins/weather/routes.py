import httpx
from fastapi import APIRouter, HTTPException, Query, status

from app.integrations.plugins.weather.service import get_current_weather

router = APIRouter(
    prefix="/api/v1/integrations/weather",
    tags=["Weather"],
)


@router.get("/current")
async def current_weather(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
) -> dict:
    try:
        return await get_current_weather(latitude, longitude)
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The weather provider is currently unavailable.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The weather provider returned invalid data.",
        ) from exc
