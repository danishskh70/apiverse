
import logging
import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

logger = logging.getLogger(__name__)

load_dotenv()

NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
REQUEST_TIMEOUT = 30.0


async def get_apod(date: str | None = None) -> dict:
    """Fetch NASA's Astronomy Picture of the Day."""
    api_key = os.getenv("NASA_API_KEY")

    if not api_key:
        logger.error("NASA APOD unavailable: NASA_API_KEY is not configured.")
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

            if response.is_error:
                logger.warning(
                    "NASA APOD upstream error: status=%s body=%s",
                    response.status_code,
                    response.text[:300],
                )

            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as exc:
        upstream_status = exc.response.status_code

        if upstream_status == 429:
            raise HTTPException(
                status_code=429,
                detail="NASA API rate limit reached. Try again later.",
            ) from exc

        if upstream_status == 400:
            raise HTTPException(
                status_code=400,
                detail="NASA rejected the requested date or parameters.",
            ) from exc

        raise HTTPException(
            status_code=502,
            detail="NASA could not process the request.",
        ) from exc

    except httpx.RequestError as exc:
        logger.warning(
            "NASA APOD connection failure: error_type=%s",
            type(exc).__name__,
        )
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to NASA right now.",
        ) from exc

    except ValueError as exc:
        logger.warning(
            "NASA APOD returned invalid JSON: error_type=%s",
            type(exc).__name__,
        )
        raise HTTPException(
            status_code=502,
            detail="NASA returned an invalid response.",
        ) from exc

    if not isinstance(data, dict) or not data.get("url") or not data.get("title"):
        logger.warning("NASA APOD returned an unexpected response structure.")
        raise HTTPException(
            status_code=502,
            detail="NASA returned an invalid APOD response.",
        )

    return data
