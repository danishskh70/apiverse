import logging

import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)

DICTIONARY_URL = "https://api.suvankar.cc/dictionaryapi/v1/definitions/en"
REQUEST_TIMEOUT = 10.0


async def get_word_definition(word: str) -> dict:
    """Fetch dictionary definitions and examples from Wiktionary."""
    url = f"{DICTIONARY_URL}/{word}"

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(url, params={"compact": "true"})

            if response.is_error:
                logger.warning(
                    "Dictionary upstream error: status=%s body=%s",
                    response.status_code,
                    response.text[:300],
                )

            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as exc:
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
        raise HTTPException(
            status_code=502,
            detail="The dictionary service returned invalid data.",
        ) from exc

    if not isinstance(data, dict) or not isinstance(data.get("meanings"), list):
        raise HTTPException(
            status_code=502,
            detail="The dictionary service returned invalid data.",
        )

    meanings = []

    for meaning in data["meanings"]:
        if not isinstance(meaning, dict):
            continue

        definitions = []

        for sense in meaning.get("senses", []):
            if not isinstance(sense, dict):
                continue

            glosses = sense.get("glosses", [])
            if not isinstance(glosses, list):
                continue

            for gloss in glosses:
                if not isinstance(gloss, str) or not gloss.strip():
                    continue

                definition = {"definition": gloss}

                examples = sense.get("examples", [])
                if isinstance(examples, list) and examples:
                    example = examples[0]
                    if isinstance(example, str) and example.strip():
                        definition["example"] = example

                definitions.append(definition)

        if definitions:
            meanings.append(
                {
                    "partOfSpeech": meaning.get("partOfSpeech", ""),
                    "definitions": definitions,
                }
            )

    result_word = data.get("word")
    if not isinstance(result_word, str) or not result_word or not meanings:
        raise HTTPException(
            status_code=502,
            detail="No usable definitions were returned.",
        )

    return {
        "word": result_word,
        "phonetic": "",
        "meanings": meanings,
        "source": "Wiktionary (CC BY-SA 4.0)",
    }
