from fastapi import APIRouter, Query

from app.integrations.plugins.word.service import get_word_definition

router = APIRouter(
    prefix="/api/v1/integrations",
    tags=["Word of the Day"],
)


@router.get("/word/definition")
async def word_definition(
    word: str = Query(min_length=1, max_length=80, pattern=r"^[a-zA-Z-]+$"),
) -> dict:
    """Return dictionary definitions for a word."""
    return await get_word_definition(word)