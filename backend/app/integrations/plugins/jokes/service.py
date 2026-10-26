import httpx
from fastapi import HTTPException

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any"
REQUEST_TIMEOUT = 10.0


async def get_random_joke() -> dict:
    """Fetch a random joke from JokeAPI."""
    params = {
        "safe-mode": "",
        "blacklistFlags": "nsfw,religious,political,racist,sexist,explicit",
    }

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(JOKE_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="JokeAPI returned an unsuccessful response.",
        ) from exc

    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve a joke right now.",
        ) from exc

    if not isinstance(data, dict) or data.get("error"):
        raise HTTPException(
            status_code=502,
            detail="JokeAPI returned an invalid response.",
        )

    if data.get("type") == "single":
        if not data.get("joke"):
            raise HTTPException(
                status_code=502,
                detail="JokeAPI returned an incomplete joke.",
            )
    elif data.get("type") == "twopart":
        if not data.get("setup") or not data.get("delivery"):
            raise HTTPException(
                status_code=502,
                detail="JokeAPI returned an incomplete joke.",
            )
    else:
        raise HTTPException(
            status_code=502,
            detail="JokeAPI returned an unsupported joke format.",
        )

    return data
