import json
from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.integrations.plugins.countries.service import (
    COUNTRIES_API_URL,
    get_countries,
)
from app.integrations.plugins.jokes.service import get_random_joke
from app.integrations.plugins.quotes.service import get_daily_quote
from app.main import app

client = TestClient(app)


def make_response(data, status=200):
    request = httpx.Request("GET", "https://example.test")
    return httpx.Response(
        status,
        content=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        request=request,
    )


def mock_client(monkeypatch, responses, capture=None):
    class MockClient:
        def __init__(self, *args, **kwargs):
            if capture is not None:
                capture["timeout"] = kwargs.get("timeout")

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def get(self, url, **kwargs):
            if capture is not None:
                capture.setdefault("requests", []).append({"url": url, **kwargs})

            result = responses.pop(0)
            if isinstance(result, Exception):
                raise result
            return result

    monkeypatch.setattr(httpx, "AsyncClient", MockClient)


# ---------------------------------------------------------------------
# World Explorer / Countries
# ---------------------------------------------------------------------


@pytest.mark.asyncio
async def test_countries_maps_country_fields(monkeypatch):
    monkeypatch.setenv("REST_COUNTRIES_API_KEY", "test-key")
    capture = {}

    mock_client(
        monkeypatch,
        [
            make_response(
                {
                    "data": {
                        "objects": [
                            {
                                "names": {
                                    "common": "India",
                                    "official": "Republic of India",
                                },
                                "capitals": [{"name": "New Delhi"}],
                                "region": "Asia",
                                "population": 1000,
                                "codes": {"alpha_3": "IND"},
                                "flag": {
                                    "url_png": "https://example.test/india.png",
                                    "description": "Flag of India",
                                },
                            }
                        ],
                        "meta": {"more": False},
                    }
                }
            )
        ],
        capture,
    )

    result = await get_countries()

    assert result == [
        {
            "name": {
                "common": "India",
                "official": "Republic of India",
            },
            "flags": {
                "png": "https://example.test/india.png",
                "alt": "Flag of India",
            },
            "capital": ["New Delhi"],
            "region": "Asia",
            "population": 1000,
            "cca3": "IND",
        }
    ]
    assert capture["requests"][0]["url"] == COUNTRIES_API_URL
    assert capture["requests"][0]["headers"] == {"Authorization": "Bearer test-key"}
    assert capture["requests"][0]["params"]["offset"] == 0
    assert capture["requests"][0]["params"]["limit"] == 100


@pytest.mark.asyncio
async def test_countries_paginates_until_provider_has_no_more(monkeypatch):
    monkeypatch.setenv("REST_COUNTRIES_API_KEY", "test-key")
    capture = {}

    first_page = {
        "data": {
            "objects": [
                {
                    "names": {"common": "A", "official": "Country A"},
                    "meta": {},
                },
                {
                    "names": {"common": "B", "official": "Country B"},
                    "meta": {},
                },
            ],
            "meta": {"more": True},
        }
    }
    second_page = {
        "data": {
            "objects": [
                {
                    "names": {"common": "C", "official": "Country C"},
                }
            ],
            "meta": {"more": False},
        }
    }

    mock_client(
        monkeypatch,
        [make_response(first_page), make_response(second_page)],
        capture,
    )

    result = await get_countries()

    assert [item["name"]["common"] for item in result] == ["A", "B", "C"]
    assert [item["params"]["offset"] for item in capture["requests"]] == [
        0,
        2,
    ]


@pytest.mark.asyncio
async def test_countries_handles_missing_optional_fields(monkeypatch):
    monkeypatch.setenv("REST_COUNTRIES_API_KEY", "test-key")

    mock_client(
        monkeypatch,
        [
            make_response(
                {
                    "data": {
                        "objects": [{}],
                        "meta": {"more": False},
                    }
                }
            )
        ],
    )

    result = await get_countries()

    assert result[0]["name"] == {
        "common": "Unknown",
        "official": "Unknown",
    }
    assert result[0]["capital"] == []
    assert result[0]["flags"] == {"png": "", "alt": ""}
    assert result[0]["region"] == "Unknown"
    assert result[0]["population"] == 0
    assert result[0]["cca3"] == ""


@pytest.mark.asyncio
async def test_countries_requires_api_key(monkeypatch):
    monkeypatch.delenv("REST_COUNTRIES_API_KEY", raising=False)

    with pytest.raises(HTTPException) as exc:
        await get_countries()

    assert exc.value.status_code == 500
    assert exc.value.detail == "REST_COUNTRIES_API_KEY is not configured."


@pytest.mark.asyncio
async def test_countries_maps_provider_http_error(monkeypatch):
    request = httpx.Request("GET", COUNTRIES_API_URL)
    mock_client(
        monkeypatch,
        [httpx.Response(403, request=request)],
    )

    with pytest.raises(HTTPException) as exc:
        await get_countries()

    assert exc.value.status_code == 502
    assert "rejected the request" in exc.value.detail


@pytest.mark.asyncio
async def test_countries_maps_connection_error(monkeypatch):
    monkeypatch.setenv("REST_COUNTRIES_API_KEY", "test-key")
    mock_client(
        monkeypatch,
        [httpx.ConnectError("Connection failed")],
    )

    with pytest.raises(HTTPException) as exc:
        await get_countries()

    assert exc.value.status_code == 502
    assert exc.value.detail == "Unable to retrieve country data."


# ---------------------------------------------------------------------
# JokeBox
# ---------------------------------------------------------------------


@pytest.mark.asyncio
async def test_joke_returns_single_part_joke(monkeypatch):
    joke = {
        "error": False,
        "type": "single",
        "joke": "A test joke.",
    }
    capture = {}
    mock_client(monkeypatch, [make_response(joke)], capture)

    result = await get_random_joke()

    assert result == joke
    assert capture["requests"][0]["params"]["safe-mode"] == ""
    assert "explicit" in capture["requests"][0]["params"]["blacklistFlags"]


@pytest.mark.asyncio
async def test_joke_returns_two_part_joke(monkeypatch):
    joke = {
        "error": False,
        "type": "twopart",
        "setup": "Why test?",
        "delivery": "To catch bugs.",
    }
    mock_client(monkeypatch, [make_response(joke)])

    assert await get_random_joke() == joke


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"error": True},
        [],
        None,
    ],
)
async def test_joke_rejects_invalid_response(monkeypatch, payload):
    mock_client(monkeypatch, [make_response(payload)])

    with pytest.raises(HTTPException) as exc:
        await get_random_joke()

    assert exc.value.status_code == 502
    assert exc.value.detail == "JokeAPI returned an invalid response."


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"type": "single", "joke": ""},
        {"type": "twopart", "setup": "Question", "delivery": ""},
    ],
)
async def test_joke_rejects_incomplete_joke(monkeypatch, payload):
    mock_client(monkeypatch, [make_response(payload)])

    with pytest.raises(HTTPException) as exc:
        await get_random_joke()

    assert exc.value.status_code == 502
    assert exc.value.detail == "JokeAPI returned an incomplete joke."


@pytest.mark.asyncio
async def test_joke_rejects_unsupported_format(monkeypatch):
    mock_client(
        monkeypatch,
        [make_response({"error": False, "type": "unknown"})],
    )

    with pytest.raises(HTTPException) as exc:
        await get_random_joke()

    assert exc.value.status_code == 502
    assert exc.value.detail == "JokeAPI returned an unsupported joke format."


@pytest.mark.asyncio
async def test_joke_maps_provider_http_error(monkeypatch):
    request = httpx.Request("GET", "https://example.test")
    mock_client(monkeypatch, [httpx.Response(503, request=request)])

    with pytest.raises(HTTPException) as exc:
        await get_random_joke()

    assert exc.value.status_code == 502
    assert exc.value.detail == "JokeAPI returned an unsuccessful response."


@pytest.mark.asyncio
async def test_joke_maps_connection_error(monkeypatch):
    mock_client(monkeypatch, [httpx.ConnectError("Connection failed")])

    with pytest.raises(HTTPException) as exc:
        await get_random_joke()

    assert exc.value.status_code == 502
    assert exc.value.detail == "Unable to retrieve a joke right now."


# ---------------------------------------------------------------------
# Daily Inspiration / Quotes
# ---------------------------------------------------------------------


@pytest.mark.asyncio
async def test_quote_maps_provider_response(monkeypatch):
    mock_client(
        monkeypatch,
        [make_response([{"q": "Keep learning.", "a": "A Test Author"}])],
    )

    assert await get_daily_quote() == {
        "quote": "Keep learning.",
        "author": "A Test Author",
        "source": "ZenQuotes",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        [],
        {},
        None,
        ["invalid"],
        [{"q": "", "a": "Author"}],
        [{"q": "A quote", "a": ""}],
    ],
)
async def test_quote_rejects_invalid_provider_data(monkeypatch, payload):
    mock_client(monkeypatch, [make_response(payload)])

    with pytest.raises(HTTPException) as exc:
        await get_daily_quote()

    assert exc.value.status_code == 502
    assert exc.value.detail == "ZenQuotes returned an invalid quote."


@pytest.mark.asyncio
async def test_quote_maps_provider_http_error(monkeypatch):
    request = httpx.Request("GET", "https://example.test")
    mock_client(monkeypatch, [httpx.Response(503, request=request)])

    with pytest.raises(HTTPException) as exc:
        await get_daily_quote()

    assert exc.value.status_code == 502
    assert exc.value.detail == "ZenQuotes returned an unsuccessful response."


@pytest.mark.asyncio
async def test_quote_maps_connection_error(monkeypatch):
    mock_client(monkeypatch, [httpx.ConnectError("Connection failed")])

    with pytest.raises(HTTPException) as exc:
        await get_daily_quote()

    assert exc.value.status_code == 502
    assert exc.value.detail == "Unable to retrieve today's quote right now."


# ---------------------------------------------------------------------
# API route validation and service integration
# ---------------------------------------------------------------------


def test_countries_route_returns_service_result(monkeypatch):
    expected = [{"name": {"common": "India"}}]
    mock = AsyncMock(return_value=expected)
    monkeypatch.setattr(
        "app.integrations.plugins.countries.routes.get_countries",
        mock,
    )

    response = client.get("/api/v1/integrations/countries")

    assert response.status_code == 200
    assert response.json() == expected
    mock.assert_awaited_once_with()


def test_countries_route_propagates_service_error(monkeypatch):
    mock = AsyncMock(
        side_effect=HTTPException(status_code=502, detail="Provider error")
    )
    monkeypatch.setattr(
        "app.integrations.plugins.countries.routes.get_countries",
        mock,
    )

    response = client.get("/api/v1/integrations/countries")

    assert response.status_code == 502
    assert response.json()["detail"] == "Provider error"


def test_joke_route_returns_service_result(monkeypatch):
    expected = {"type": "single", "joke": "A test joke."}
    mock = AsyncMock(return_value=expected)
    monkeypatch.setattr(
        "app.integrations.plugins.jokes.routes.get_random_joke",
        mock,
    )

    response = client.get("/api/v1/integrations/jokebox/random")

    assert response.status_code == 200
    assert response.json() == expected
    mock.assert_awaited_once_with()


def test_quote_route_returns_service_result(monkeypatch):
    expected = {
        "quote": "Keep learning.",
        "author": "A Test Author",
        "source": "ZenQuotes",
    }
    mock = AsyncMock(return_value=expected)
    monkeypatch.setattr(
        "app.integrations.plugins.quotes.routes.get_daily_quote",
        mock,
    )

    response = client.get("/api/v1/integrations/quotes/daily")

    assert response.status_code == 200
    assert response.json() == expected
    mock.assert_awaited_once_with()


def test_history_route_requires_month_and_day_together():
    response = client.get(
        "/api/v1/integrations/history/today",
        params={"month": 10},
    )

    assert response.status_code == 422


def test_history_route_rejects_out_of_range_month():
    response = client.get(
        "/api/v1/integrations/history/today",
        params={"month": 13, "day": 10},
    )

    assert response.status_code == 422


def test_space_route_rejects_invalid_date():
    response = client.get(
        "/api/v1/integrations/space/apod",
        params={"date": "not-a-date"},
    )

    assert response.status_code == 422


def test_word_route_rejects_invalid_word():
    for word in ("", "two words", "word123", "hello!"):
        response = client.get(
            "/api/v1/integrations/word/definition",
            params={"word": word},
        )
        assert response.status_code == 422, word


def test_word_route_rejects_overlong_word():
    response = client.get(
        "/api/v1/integrations/word/definition",
        params={"word": "a" * 81},
    )

    assert response.status_code == 422
