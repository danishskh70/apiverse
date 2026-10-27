from datetime import date

import httpx
import pytest
from fastapi import HTTPException

from app.integrations.plugins.history.service import get_historical_events
from app.integrations.plugins.space.service import get_apod
from app.integrations.plugins.word.service import get_word_definition


def mock_http_client(monkeypatch, response=None, error=None, capture=None):
    class MockClient:
        def __init__(self, *args, **kwargs):
            if capture is not None:
                capture["headers"] = kwargs.get("headers", {})
                capture["timeout"] = kwargs.get("timeout")

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def get(self, url, **kwargs):
            if capture is not None:
                capture["url"] = url
                capture["params"] = kwargs.get("params")
            if error:
                raise error
            return response

    monkeypatch.setattr(httpx, "AsyncClient", MockClient)


def response_with_json(data, status=200):
    request = httpx.Request("GET", "https://example.test")
    response = httpx.Response(status, json=data, request=request)
    return response


@pytest.mark.asyncio
async def test_apod_maps_nasa_list_response(monkeypatch):
    today = date.today().isoformat()
    payload = [
        {
            "date": today,
            "title": "A test image",
            "media_type": "image",
            "url": "https://example.test/image.jpg",
            "hdurl": "https://example.test/large.jpg",
            "explanation": "A test explanation",
        }
    ]
    capture = {}
    mock_http_client(
        monkeypatch,
        response=response_with_json(payload),
        capture=capture,
    )

    result = await get_apod()

    assert result["title"] == "A test image"
    assert result["hdurl"] == "https://example.test/large.jpg"
    assert capture["url"] == ("https://science.nasa.gov/wp-json/wp/v2/apod-basic")


@pytest.mark.asyncio
async def test_apod_passes_requested_date(monkeypatch):
    payload = [
        {
            "date": "2026-10-27",
            "title": "Dated image",
            "media_type": "image",
            "url": "https://example.test/image.jpg",
        }
    ]
    capture = {}
    mock_http_client(
        monkeypatch,
        response=response_with_json(payload),
        capture=capture,
    )

    result = await get_apod("2026-10-27")

    assert result["date"] == "2026-10-27"
    assert capture["params"]["date"] == "2026-10-27"


@pytest.mark.asyncio
async def test_apod_returns_404_when_date_is_missing(monkeypatch):
    mock_http_client(monkeypatch, response=response_with_json([]))

    with pytest.raises(HTTPException) as exc:
        await get_apod("2020-01-01")

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_apod_maps_upstream_http_error(monkeypatch):
    request = httpx.Request("GET", "https://example.test")
    response = httpx.Response(503, request=request)
    mock_http_client(monkeypatch, response=response)

    with pytest.raises(HTTPException) as exc:
        await get_apod()

    assert exc.value.status_code == 502


@pytest.mark.asyncio
async def test_word_maps_wiktionary_definition_and_attribution(monkeypatch):
    payload = {
        "word": "serendipity",
        "meanings": [
            {
                "partOfSpeech": "noun",
                "senses": [
                    {
                        "glosses": ["A fortunate discovery by chance."],
                        "examples": ["It was pure serendipity."],
                    }
                ],
            }
        ],
    }
    capture = {}
    mock_http_client(
        monkeypatch,
        response=response_with_json(payload),
        capture=capture,
    )

    result = await get_word_definition("serendipity")

    assert result["word"] == "serendipity"
    assert result["meanings"][0]["definitions"][0]["definition"] == (
        "A fortunate discovery by chance."
    )
    assert result["meanings"][0]["definitions"][0]["example"] == (
        "It was pure serendipity."
    )
    assert result["source"] == "Wiktionary (CC BY-SA 4.0)"
    assert capture["params"] == {"compact": "true"}


@pytest.mark.asyncio
async def test_word_rejects_malformed_upstream_data(monkeypatch):
    mock_http_client(
        monkeypatch,
        response=response_with_json({"word": "test", "meanings": "invalid"}),
    )

    with pytest.raises(HTTPException) as exc:
        await get_word_definition("test")

    assert exc.value.status_code == 502


@pytest.mark.asyncio
async def test_word_maps_upstream_http_error(monkeypatch):
    request = httpx.Request("GET", "https://example.test")
    mock_http_client(
        monkeypatch,
        response=httpx.Response(503, request=request),
    )

    with pytest.raises(HTTPException) as exc:
        await get_word_definition("test")

    assert exc.value.status_code == 502


@pytest.mark.asyncio
async def test_history_maps_events_and_article_links(monkeypatch):
    payload = {
        "events": [
            {
                "year": 2019,
                "text": "A historical event.",
                "pages": [
                    {
                        "title": "Test_page",
                        "titles": {"canonical": "Test_page"},
                    }
                ],
            }
        ]
    }
    capture = {}
    mock_http_client(
        monkeypatch,
        response=response_with_json(payload),
        capture=capture,
    )

    result = await get_historical_events(10, 27)

    assert result["date"] == "10-27"
    assert result["source"] == "Wikipedia"
    assert result["events"][0]["year"] == 2019
    assert result["events"][0]["pages"][0] == {
        "title": "Test page",
        "url": "https://en.wikipedia.org/wiki/Test_page",
    }
    assert capture["url"].endswith("/10/27")
    assert capture["headers"]["Api-User-Agent"].startswith("APIverse/")


@pytest.mark.asyncio
async def test_history_rejects_invalid_date():
    with pytest.raises(HTTPException) as exc:
        await get_historical_events(2, 30)

    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_history_maps_upstream_http_error(monkeypatch):
    request = httpx.Request("GET", "https://example.test")
    mock_http_client(
        monkeypatch,
        response=httpx.Response(403, request=request),
    )

    with pytest.raises(HTTPException) as exc:
        await get_historical_events(10, 27)

    assert exc.value.status_code == 502


@pytest.mark.asyncio
async def test_history_limits_results_to_twelve(monkeypatch):
    payload = {
        "events": [
            {"year": year, "text": f"Event {year}", "pages": []} for year in range(20)
        ]
    }
    mock_http_client(monkeypatch, response=response_with_json(payload))

    result = await get_historical_events(10, 27)

    assert len(result["events"]) == 12


@pytest.mark.asyncio
async def test_history_maps_connection_failure(monkeypatch):
    request = httpx.Request(
        "GET",
        "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/events/10/27",
    )
    mock_http_client(
        monkeypatch,
        error=httpx.ConnectError("Connection failed", request=request),
    )

    with pytest.raises(HTTPException) as exc:
        await get_historical_events(10, 27)

    assert exc.value.status_code == 502
    assert exc.value.detail == "Unable to connect to the history service right now."


@pytest.mark.asyncio
async def test_history_rejects_invalid_json(monkeypatch):
    request = httpx.Request("GET", "https://example.test")
    response = httpx.Response(
        200,
        content=b"{invalid json",
        headers={"Content-Type": "application/json"},
        request=request,
    )
    mock_http_client(monkeypatch, response=response)

    with pytest.raises(HTTPException) as exc:
        await get_historical_events(10, 27)

    assert exc.value.status_code == 502
    assert exc.value.detail == "The history service returned invalid data."


@pytest.mark.asyncio
@pytest.mark.parametrize("payload", [[], None, "unexpected", {"events": "invalid"}])
async def test_history_rejects_unexpected_response_structure(monkeypatch, payload):
    mock_http_client(monkeypatch, response=response_with_json(payload))

    with pytest.raises(HTTPException) as exc:
        await get_historical_events(10, 27)

    assert exc.value.status_code == 502
    assert exc.value.detail == "The history service returned invalid data."


@pytest.mark.asyncio
async def test_history_skips_malformed_events_and_pages(monkeypatch):
    payload = {
        "events": [
            None,
            {"year": 1900, "text": 123},
            {
                "year": 1901,
                "text": "A valid event",
                "pages": [
                    None,
                    "invalid page",
                    {},
                    {"title": ""},
                    {"title": "Valid_page"},
                ],
            },
            {
                "year": 1902,
                "text": "Event with invalid pages container",
                "pages": "invalid",
            },
        ]
    }
    mock_http_client(monkeypatch, response=response_with_json(payload))

    result = await get_historical_events(10, 27)

    assert len(result["events"]) == 2
    assert result["events"][0]["title"] == "A valid event"
    assert result["events"][0]["pages"] == [
        {
            "title": "Valid page",
            "url": "https://en.wikipedia.org/wiki/Valid_page",
        }
    ]
    assert result["events"][1]["pages"] == []


@pytest.mark.asyncio
async def test_history_encodes_canonical_article_title(monkeypatch):
    payload = {
        "events": [
            {
                "year": 2000,
                "text": "Encoded title event",
                "pages": [
                    {
                        "title": "A title",
                        "titles": {"canonical": "A title/with special characters"},
                    }
                ],
            }
        ]
    }
    mock_http_client(monkeypatch, response=response_with_json(payload))

    result = await get_historical_events(10, 27)

    assert result["events"][0]["pages"][0]["url"] == (
        "https://en.wikipedia.org/wiki/A_title%2Fwith_special_characters"
    )


@pytest.mark.asyncio
async def test_history_falls_back_when_canonical_title_is_invalid(monkeypatch):
    payload = {
        "events": [
            {
                "year": 2001,
                "text": "Fallback title event",
                "pages": [
                    {
                        "title": "Fallback_page",
                        "titles": {"canonical": ""},
                    }
                ],
            }
        ]
    }
    mock_http_client(monkeypatch, response=response_with_json(payload))

    result = await get_historical_events(10, 27)

    assert result["events"][0]["pages"][0]["url"] == (
        "https://en.wikipedia.org/wiki/Fallback_page"
    )


@pytest.mark.asyncio
async def test_word_maps_connection_failure(monkeypatch):
    mock_http_client(
        monkeypatch,
        error=httpx.ConnectError("connection failed"),
    )

    with pytest.raises(HTTPException) as exc:
        await get_word_definition("serendipity")

    assert exc.value.status_code == 502
    assert exc.value.detail == (
        "Unable to connect to the dictionary service right now."
    )


@pytest.mark.asyncio
async def test_word_maps_invalid_json(monkeypatch):
    response = httpx.Response(
        200,
        content=b"not json",
        request=httpx.Request(
            "GET",
            "https://api.suvankar.cc/dictionaryapi/v1/definitions/en/test",
        ),
    )
    mock_http_client(monkeypatch, response=response)

    with pytest.raises(HTTPException) as exc:
        await get_word_definition("test")

    assert exc.value.status_code == 502
    assert exc.value.detail == ("The dictionary service returned invalid data.")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        [],
        None,
        "unexpected",
        {},
        {"meanings": "invalid"},
    ],
)
async def test_word_rejects_invalid_payload_structure(monkeypatch, payload):
    mock_http_client(monkeypatch, response=response_with_json(payload))

    with pytest.raises(HTTPException) as exc:
        await get_word_definition("test")

    assert exc.value.status_code == 502
    assert exc.value.detail == ("The dictionary service returned invalid data.")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"word": "", "meanings": [{"senses": [{"glosses": ["meaning"]}]}]},
        {"word": None, "meanings": [{"senses": [{"glosses": ["meaning"]}]}]},
        {"word": "test", "meanings": []},
        {"word": "test", "meanings": [{"senses": [{"glosses": [" "]}]}]},
        {"word": "test", "meanings": [{"senses": []}]},
    ],
)
async def test_word_rejects_payload_without_usable_definitions(monkeypatch, payload):
    mock_http_client(monkeypatch, response=response_with_json(payload))

    with pytest.raises(HTTPException) as exc:
        await get_word_definition("test")

    assert exc.value.status_code == 502
    assert exc.value.detail == "No usable definitions were returned."


@pytest.mark.asyncio
async def test_word_skips_malformed_senses_glosses_and_examples(monkeypatch):
    payload = {
        "word": "test",
        "meanings": [
            None,
            {
                "partOfSpeech": "noun",
                "senses": [
                    None,
                    {"glosses": "not a list"},
                    {
                        "glosses": [None, "", "   ", "A valid definition"],
                        "examples": ["   ", 42],
                    },
                    {
                        "glosses": ["Another definition"],
                        "examples": ["A useful example"],
                    },
                ],
            },
            {"senses": [{"glosses": [""]}]},
        ],
    }
    mock_http_client(monkeypatch, response=response_with_json(payload))

    result = await get_word_definition("test")

    assert result["word"] == "test"
    assert result["meanings"] == [
        {
            "partOfSpeech": "noun",
            "definitions": [
                {"definition": "A valid definition"},
                {
                    "definition": "Another definition",
                    "example": "A useful example",
                },
            ],
        }
    ]


@pytest.mark.asyncio
async def test_word_uses_empty_part_of_speech_when_missing(monkeypatch):
    payload = {
        "word": "test",
        "meanings": [{"senses": [{"glosses": ["A definition"]}]}],
    }
    mock_http_client(monkeypatch, response=response_with_json(payload))

    result = await get_word_definition("test")

    assert result["meanings"][0]["partOfSpeech"] == ""
