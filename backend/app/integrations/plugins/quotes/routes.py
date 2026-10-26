from fastapi import APIRouter

from app.integrations.plugins.quotes.service import get_daily_quote

router = APIRouter(
    prefix="/api/v1/integrations",
    tags=["Daily Inspiration"],
)


@router.get("/quotes/daily")
async def daily_quote() -> dict[str, str]:
    """Return today's inspirational quote."""
    return await get_daily_quote()
