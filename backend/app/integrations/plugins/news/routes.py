from typing import Literal

from fastapi import APIRouter, Query

from app.integrations.plugins.news.service import get_top_headlines

router = APIRouter(
    prefix="/api/v1/integrations",
    tags=["Newsroom"],
)

NewsCategory = Literal[
    "general",
    "business",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology",
]


@router.get("/news")
async def list_news(
    country: str = Query(
        default="in",
        min_length=2,
        max_length=2,
        pattern="^[a-zA-Z]{2}$",
    ),
    category: NewsCategory = "general",
    q: str | None = Query(default=None, min_length=1, max_length=100),
    page_size: int = Query(default=12, ge=1, le=100),
) -> dict:
    return await get_top_headlines(
        country=country.lower(),
        category=category,
        q=q,
        page_size=page_size,
    )
