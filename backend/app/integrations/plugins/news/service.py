import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
NEWS_SEARCH_URL = "https://newsapi.org/v2/everything"

CATEGORY_QUERIES = {
    "general": "India",
    "business": "India AND (business OR economy OR markets)",
    "technology": "India AND (technology OR tech OR software)",
    "science": "India AND (science OR research)",
    "health": "India AND (health OR medical)",
    "sports": "India AND (sports OR cricket)",
    "entertainment": "India AND (entertainment OR films OR Bollywood)",
}


def _raise_provider_error(exc: httpx.HTTPStatusError) -> None:
    if exc.response.status_code == 429:
        raise HTTPException(
            status_code=429,
            detail="NewsAPI rate limit reached. Try again later.",
        ) from exc

    raise HTTPException(
        status_code=502,
        detail="The news provider rejected the request. Check API access and credentials.",
    ) from exc


async def _request_articles(
    client: httpx.AsyncClient,
    url: str,
    params: dict[str, str | int],
    headers: dict[str, str],
) -> dict:
    response = await client.get(url, params=params, headers=headers)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, dict) or payload.get("status") != "ok":
        raise HTTPException(
            status_code=502,
            detail="The news provider returned an error.",
        )

    articles = payload.get("articles", [])
    if not isinstance(articles, list):
        raise HTTPException(
            status_code=502,
            detail="The news provider returned an invalid article list.",
        )

    return {
        "totalResults": payload.get("totalResults", len(articles)),
        "articles": articles,
    }


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
    params: dict[str, str | int] = {
        "country": country.lower(),
        "category": category,
        "pageSize": page_size,
    }

    if q and q.strip():
        params["q"] = q.strip()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            result = await _request_articles(
                client,
                NEWS_API_URL,
                params,
                headers,
            )

            if result["articles"]:
                return {
                    "totalResults": result["totalResults"],
                    "articles": result["articles"][:page_size],
                }

            # Country-filtered headlines can be empty even when search
            # results exist. Fall back to relevant articles, not US headlines.
            search_query = CATEGORY_QUERIES.get(category, "India")

            if country.lower() == "in" and q and q.strip():
                search_query = f"({q.strip()}) AND ({search_query})"
            elif q and q.strip():
                search_query = q.strip()

            fallback_params: dict[str, str | int] = {
                "q": search_query,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": page_size,
            }

            fallback = await _request_articles(
                client,
                NEWS_SEARCH_URL,
                fallback_params,
                headers,
            )

            return {
                "totalResults": fallback["totalResults"],
                "articles": fallback["articles"][:page_size],
            }

    except httpx.HTTPStatusError as exc:
        _raise_provider_error(exc)
    except HTTPException:
        raise
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve news right now.",
        ) from exc
