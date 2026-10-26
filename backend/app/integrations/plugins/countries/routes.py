
from fastapi import APIRouter

from app.integrations.plugins.countries.service import get_countries

router = APIRouter(
    prefix="/api/v1/integrations",
    tags=["World Explorer"],
)


@router.get("/countries")
async def list_countries() -> list[dict]:
    return await get_countries()
