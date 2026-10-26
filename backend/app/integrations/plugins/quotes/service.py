import httpx
from fastapi import HTTPException

ZENQUOTES_URL = "https://zenquotes.io/api/today"
REQUEST_TIMEOUT = 10.0


async def get_daily_quote() -> dict[str, str]:
    """Fetch the daily quote from ZenQuotes."""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(ZENQUOTES_URL)
            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="ZenQuotes returned an unsuccessful response.",
        ) from exc

    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve today's quote right now.",
        ) from exc

    if (
        not isinstance(data, list)
        or not data
        or not isinstance(data[0], dict)
        or not data[0].get("q")
        or not data[0].get("a")
    ):
        raise HTTPException(
            status_code=502,
            detail="ZenQuotes returned an invalid quote.",
        )

    return {
        "quote": data[0]["q"],
        "author": data[0]["a"],
        "source": "ZenQuotes",
    }
