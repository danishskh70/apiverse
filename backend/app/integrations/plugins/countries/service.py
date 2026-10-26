
import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

COUNTRIES_API_URL = "https://api.restcountries.com/countries/v5"


async def get_countries() -> list[dict]:
    api_key = os.getenv("REST_COUNTRIES_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="REST_COUNTRIES_API_KEY is not configured.",
        )

    headers = {"Authorization": f"Bearer {api_key}"}
    countries: list[dict] = []
    offset = 0
    limit = 100

    params = {
        "limit": limit,
        "response_fields": (
            "names.common,names.official,capitals,"
            "region,population,codes.alpha_3,"
            "flag.url_png,flag.description"
        ),
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            while True:
                response = await client.get(
                    COUNTRIES_API_URL,
                    headers=headers,
                    params={**params, "offset": offset},
                )
                response.raise_for_status()

                payload = response.json()
                data = payload.get("data", {})
                objects = data.get("objects", [])

                for item in objects:
                    names = item.get("names") or {}
                    capitals = item.get("capitals") or []
                    flag = item.get("flag") or {}
                    codes = item.get("codes") or {}

                    countries.append({
                        "name": {
                            "common": names.get("common", "Unknown"),
                            "official": names.get("official", "Unknown"),
                        },
                        "flags": {
                            "png": flag.get("url_png", ""),
                            "alt": flag.get("description", ""),
                        },
                        "capital": [
                            capital["name"]
                            for capital in capitals
                            if capital.get("name")
                        ],
                        "region": item.get("region") or "Unknown",
                        "population": item.get("population") or 0,
                        "cca3": codes.get("alpha_3", ""),
                    })

                meta = data.get("meta", {})

                if not objects or not meta.get("more", False):
                    break

                offset += len(objects)

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="Countries API rejected the request. Check your API key and API access.",
        ) from exc
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve country data.",
        ) from exc

    return countries
