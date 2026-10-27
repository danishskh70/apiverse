from fastapi import APIRouter, Query

from app.integrations.plugins.history.service import get_historical_events

router = APIRouter(
    prefix="/api/v1/integrations",
    tags=["This Day in History"],
)


@router.get("/history/today")
async def historical_events(
    month: int | None = Query(default=None, ge=1, le=12),
    day: int | None = Query(default=None, ge=1, le=31),
) -> dict:
    """Return historical events for today's date or a specified date."""
    if (month is None) != (day is None):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=422,
            detail="Provide both month and day, or neither.",
        )

    return await get_historical_events(month=month, day=day)
