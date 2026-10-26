from fastapi import APIRouter

from app.integrations.plugins.jokes.service import get_random_joke

router = APIRouter(
    prefix="/api/v1/integrations",
    tags=["JokeBox"],
)


@router.get("/jokebox/random")
async def random_joke() -> dict:
    """Return a random joke from JokeAPI."""
    return await get_random_joke()
