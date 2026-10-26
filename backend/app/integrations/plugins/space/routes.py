from datetime import date

from fastapi import APIRouter, Query

from app.integrations.plugins.space.service import get_apod

router = APIRouter(
    prefix="/api/v1/integrations",
    tags=["Space"],
)


@router.get("/space/apod")
async def astronomy_picture_of_the_day(
    apod_date: date | None = Query(default=None, alias="date"),
) -> dict:
    """Return NASA's Astronomy Picture of the Day."""
    return await get_apod(
        date=apod_date.isoformat() if apod_date else None,
    )
