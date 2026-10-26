
from datetime import date

import httpx
from fastapi import HTTPException

WIKIPEDIA_URL = "https://en.wikipedia.org/api/rest_v1/feed/onthisday/events"
REQUEST_TIMEOUT = 10.0


async def get_historical_events(
    month: int | None = None,
    day: int | None = None,
) -> dict:
    """Fetch historical events for a given month and day."""
    today = date.today()
    month = month or today.month
    day = day or today.day

    try:
        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": "APIverse/1.0 (historical events explorer)"},
        ) as client:
            response = await client.get(f"{WIKIPEDIA_URL}/{month}/{day}")
            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="The history service returned an unsuccessful response.",
        ) from exc

    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve historical events right now.",
        ) from exc

    events = data.get("events") if isinstance(data, dict) else None

    if not isinstance(events, list):
        raise HTTPException(
            status_code=502,
            detail="The history service returned invalid data.",
        )

    results = []

    for event in events[:12]:
        if not isinstance(event, dict) or not event.get("text"):
            continue

        results.append(
            {
                "year": event.get("year"),
                "title": event["text"],
                "pages": [
                    {
                        "title": page.get("title"),
                        "url": page.get("content_urls", {})
                        .get("desktop", {})
                        .get("page"),
                    }
                    for page in event.get("pages", [])
                    if isinstance(page, dict) and page.get("title")
                ],
            }
        )

    return {
        "date": f"{month:02d}-{day:02d}",
        "events": results,
        "source": "Wikipedia",
    }