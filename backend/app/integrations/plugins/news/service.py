
import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

async def get_top_headlines(
    country: str = "in",
    category: str = "general",
    q: str | None = None,
    page_size: int = 12,
) -> dict:
    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="NEWS_API_KEY is not configured.",
        )

    headers = {"X-Api-Key": api_key}
    params_base: dict[str, str | int] = {
        "country": country.lower(),
        "category": category,
        "pageSize": page_size,
    }

    if q:
        params_base["q"] = q.strip()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            responses = await client.get(
                NEWS_API_URL,
                params=params_base,
                headers=headers,
            )
            responses.raise_for_status()
            payload = responses.json()

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="NewsAPI rate limit reached. Try again later.",
            ) from exc

        raise HTTPException(
            status_code=502,
            detail="The news provider rejected the request. Check API access and credentials.",
        ) from exc

    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve news right now.",
        ) from exc

    if payload.get("status") != "ok":
        raise HTTPException(
            status_code=502,
            detail="The news provider returned an error.",
        )

    articles = payload.get("articles", [])

    return {
        "totalResults": payload.get("totalResults", len(articles)),
        "articles": articles[:page_size],
    }
