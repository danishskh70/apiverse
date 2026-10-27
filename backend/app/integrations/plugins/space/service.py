import os
from datetime import date as date_class

import httpx
from fastapi import HTTPException

NASA_APOD_URL = "https://science.nasa.gov/wp-json/wp/v2/apod-basic"
REQUEST_TIMEOUT = 30.0


async def get_apod(date: str | None = None) -> dict:
    params = {"api_key": os.getenv("NASA_API_KEY", "DEMO_KEY")}

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

        raise HTTPException(
            status_code=502,
            detail="NASA could not process the APOD request.",
        ) from exc

    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve astronomy data right now.",
        ) from exc

    # NASA's new endpoint returns a list of APOD entries.
    if isinstance(data, dict):
        entries = [data]
    elif isinstance(data, list):
        entries = data
    else:
        raise HTTPException(
            status_code=502,
            detail="NASA returned an invalid APOD response.",
        )

    requested_date = date or date_class.today().isoformat()

    entry = next(
        (
            item
            for item in entries
            if isinstance(item, dict) and item.get("date") == requested_date
        ),
        None,
    )

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=f"No APOD entry found for {requested_date}.",
        )

    title = entry.get("title")
    media_type = entry.get("media_type")
    image_url = entry.get("hdurl") or entry.get("url")

    if (
        not title
        or not image_url
        or not image_url.startswith("https://")
        or not media_type
    ):
        raise HTTPException(
            status_code=502,
            detail="NASA returned incomplete APOD data.",
        )

    # Preserve the response shape expected by the existing frontend.
    return {
        **entry,
        "date": entry.get("date", requested_date),
        "title": title,
        "url": entry.get("url") or image_url,
        "hdurl": entry.get("hdurl") or image_url,
        "media_type": media_type,
        "explanation": entry.get("explanation", ""),
    }
