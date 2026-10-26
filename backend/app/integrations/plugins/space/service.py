import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
REQUEST_TIMEOUT = 30.0


async def get_apod(date: str | None = None) -> dict:
    """Fetch NASA's Astronomy Picture of the Day."""
    api_key = os.getenv("NASA_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="NASA_API_KEY is not configured.",
        )

    params = {"api_key": api_key}
    if date:
        params["date"] = date

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(NASA_APOD_URL, params=params)
            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="NASA API rate limit reached. Try again later.",
            ) from exc

        if exc.response.status_code == 400:
            raise HTTPException(
                status_code=400,
                detail="NASA rejected the requested date or parameters.",
            ) from exc

        raise HTTPException(
            status_code=502,
            detail="NASA could not process the request.",
        ) from exc

    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve astronomy data right now.",
        ) from exc

    if not isinstance(data, dict) or not data.get("url") or not data.get("title"):
        raise HTTPException(
            status_code=502,
            detail="NASA returned an invalid APOD response.",
        )

    return data
