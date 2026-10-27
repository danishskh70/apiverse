
import logging

import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)

DICTIONARY_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"
REQUEST_TIMEOUT = 10.0


async def get_word_definition(word: str) -> dict:
    """Fetch definitions and examples for a word."""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(f"{DICTIONARY_URL}/{word}")

            if response.is_error:
                logger.warning(
                    "Dictionary upstream error: status=%s body=%s",
                    response.status_code,
                    response.text[:300],
                )

            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="No dictionary entry was found for this word.",
            ) from exc

        raise HTTPException(
            status_code=502,
            detail="The dictionary service returned an unsuccessful response.",
        ) from exc

    except httpx.RequestError as exc:
        logger.warning(
            "Dictionary connection failure: error_type=%s",
            type(exc).__name__,
        )
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to the dictionary service right now.",
        ) from exc

    except ValueError as exc:
        logger.warning(
            "Dictionary returned invalid JSON: error_type=%s",
            type(exc).__name__,
        )
        raise HTTPException(
            status_code=502,
            detail="The dictionary service returned invalid data.",
        ) from exc

    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        logger.warning("Dictionary returned an unexpected response structure.")
        raise HTTPException(
            status_code=502,
            detail="The dictionary service returned invalid data.",
        )

    entry = data[0]
    meanings = []

    for meaning in entry.get("meanings", []):
        if not isinstance(meaning, dict):
            continue

        definitions = []

        for item in meaning.get("definitions", []):
            if not isinstance(item, dict) or not item.get("definition"):
                continue

            definition = {"definition": item["definition"]}

            if item.get("example"):
                definition["example"] = item["example"]

            definitions.append(definition)

        if definitions:
            meanings.append(
                {
                    "partOfSpeech": meaning.get("partOfSpeech", ""),
                    "definitions": definitions,
                }
            )

    if not entry.get("word") or not meanings:
        logger.warning("Dictionary response contained no usable definitions.")
        raise HTTPException(
            status_code=502,
            detail="No usable definitions were returned.",
        )

    phonetics = [
        item.get("text")
        for item in entry.get("phonetics", [])
        if isinstance(item, dict) and item.get("text")
    ]

    return {
        "word": entry["word"],
        "phonetic": phonetics[0] if phonetics else "",
        "meanings": meanings,
        "source": "Free Dictionary API",
    }
