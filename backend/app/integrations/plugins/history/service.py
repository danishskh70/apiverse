import logging
from datetime import date
from urllib.parse import quote

import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)

WIKIMEDIA_URL = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/events"
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
        date(2000, month, day)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid month or day.",
        ) from exc

    try:
        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": "APIverse/1.0 (historical events explorer)",
                "Api-User-Agent": "APIverse/1.0 (historical events explorer)",
                "Accept": "application/json",
            },
        ) as client:
            response = await client.get(f"{WIKIMEDIA_URL}/{month:02d}/{day:02d}")
            if response.is_error:
                logger.warning(
                    "Wikimedia history upstream error: status=%s body=%s",
                    response.status_code,
                    response.text[:300],
                )
            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="The history service returned an unsuccessful response.",
        ) from exc
    except httpx.RequestError as exc:
        logger.warning(
            "Wikimedia history connection failure: error_type=%s",
            type(exc).__name__,
        )
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to the history service right now.",
        ) from exc
    except ValueError as exc:
        logger.warning(
            "Wikimedia history returned invalid JSON: error_type=%s",
            type(exc).__name__,
        )
        raise HTTPException(
            status_code=502,
            detail="The history service returned invalid data.",
        ) from exc

    events = data.get("events") if isinstance(data, dict) else None
    if not isinstance(events, list):
        logger.warning("Wikimedia history returned an unexpected response structure.")
        raise HTTPException(
            status_code=502,
            detail="The history service returned invalid data.",
        )

    results = []

    for event in events:
        if not isinstance(event, dict) or not isinstance(event.get("text"), str):
            continue

        pages = []
        event_pages = event.get("pages", [])

        if isinstance(event_pages, list):
            for page in event_pages:
                if not isinstance(page, dict):
                    continue

                title = page.get("title")
                if not isinstance(title, str) or not title:
                    continue

                canonical = page.get("titles", {}).get("canonical", title)
                if not isinstance(canonical, str) or not canonical:
                    canonical = title

                pages.append(
                    {
                        "title": title.replace("_", " "),
                        "url": f"https://en.wikipedia.org/wiki/{quote(canonical.replace(' ', '_'), safe='()_')}",
                    }
                )

        results.append(
            {
                "year": event.get("year"),
                "title": event["text"],
                "pages": pages,
            }
        )

        if len(results) == 12:
            break

    return {
        "date": f"{month:02d}-{day:02d}",
        "events": results,
        "source": "Wikipedia",
    }
