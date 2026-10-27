import httpx
import pytest
from fastapi import HTTPException

from app.integrations.plugins.news.service import (
    NEWS_API_URL,
    NEWS_SEARCH_URL,
    get_top_headlines,
)


def response_with_json(data, status=200):
    request = httpx.Request("GET", "https://example.test")
    return httpx.Response(status, json=data, request=request)


def mock_news_client(monkeypatch, responses, capture):
    class MockClient:
        def __init__(self, *args, **kwargs):
            capture["timeout"] = kwargs.get("timeout")

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def get(self, url, **kwargs):
            capture.setdefault("requests", []).append(
                {
                    "url": url,
                    "params": kwargs.get("params"),
                    "headers": kwargs.get("headers"),
                }
            )

            result = responses.pop(0)

            if isinstance(result, Exception):
                raise result

            return result

    monkeypatch.setattr(httpx, "AsyncClient", MockClient)


@pytest.mark.asyncio
async def test_news_returns_top_headlines_successfully(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "test-api-key")

    articles = [
        {"title": "India technology news"},
        {"title": "India business news"},
    ]
    capture = {}

    mock_news_client(
        monkeypatch,
        [response_with_json({"status": "ok", "totalResults": 2, "articles": articles})],
        capture,
    )

    result = await get_top_headlines()

    assert result == {"totalResults": 2, "articles": articles}
    request = capture["requests"][0]
    assert request["url"] == NEWS_API_URL
    assert request["params"] == {
        "country": "in",
        "category": "general",
        "pageSize": 12,
    }
    assert request["headers"] == {"X-Api-Key": "test-api-key"}


@pytest.mark.asyncio
async def test_news_normalizes_country_and_query(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "test-api-key")
    capture = {}

    mock_news_client(
        monkeypatch,
        [
            response_with_json(
                {
                    "status": "ok",
                    "totalResults": 1,
                    "articles": [{"title": "AI news"}],
                }
            )
        ],
        capture,
    )

    result = await get_top_headlines(
        country="IN",
        category="technology",
        q="  AI  ",
        page_size=5,
    )

    assert len(result["articles"]) == 1
    assert capture["requests"][0]["params"] == {
        "country": "in",
        "category": "technology",
        "pageSize": 5,
        "q": "AI",
    }


@pytest.mark.asyncio
async def test_news_falls_back_when_headlines_are_empty(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "test-api-key")
    capture = {}

    fallback_articles = [{"title": "Technology research in India"}]

    mock_news_client(
        monkeypatch,
        [
            response_with_json({"status": "ok", "totalResults": 0, "articles": []}),
            response_with_json(
                {
                    "status": "ok",
                    "totalResults": 1,
                    "articles": fallback_articles,
                }
            ),
        ],
        capture,
    )

    result = await get_top_headlines(category="technology")

    assert result == {
        "totalResults": 1,
        "articles": fallback_articles,
    }
    assert len(capture["requests"]) == 2
    assert capture["requests"][0]["url"] == NEWS_API_URL

    fallback_request = capture["requests"][1]
    assert fallback_request["url"] == NEWS_SEARCH_URL
    assert fallback_request["params"] == {
        "q": "India AND (technology OR tech OR software)",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 12,
    }


@pytest.mark.asyncio
async def test_news_fallback_combines_query_and_category(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "test-api-key")
    capture = {}

    mock_news_client(
        monkeypatch,
        [
            response_with_json({"status": "ok", "totalResults": 0, "articles": []}),
            response_with_json(
                {
                    "status": "ok",
                    "totalResults": 0,
                    "articles": [],
                }
            ),
        ],
        capture,
    )

    await get_top_headlines(
        category="technology",
        q="AI",
        page_size=6,
    )

    assert capture["requests"][1]["params"] == {
        "q": "(AI) AND (India AND (technology OR tech OR software))",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 6,
    }


@pytest.mark.asyncio
async def test_news_limits_returned_articles_to_page_size(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "test-api-key")
    articles = [{"title": f"Article {number}"} for number in range(5)]
    capture = {}

    mock_news_client(
        monkeypatch,
        [
            response_with_json(
                {"status": "ok", "totalResults": 50, "articles": articles}
            )
        ],
        capture,
    )

    result = await get_top_headlines(page_size=2)

    assert result["totalResults"] == 50
    assert len(result["articles"]) == 2
    assert result["articles"] == articles[:2]


@pytest.mark.asyncio
async def test_news_requires_api_key(monkeypatch):
    monkeypatch.delenv("NEWS_API_KEY", raising=False)

    with pytest.raises(HTTPException) as exc:
        await get_top_headlines()

    assert exc.value.status_code == 500
    assert exc.value.detail == "NEWS_API_KEY is not configured."


@pytest.mark.asyncio
async def test_news_maps_provider_rate_limit(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "test-api-key")
    request = httpx.Request("GET", NEWS_API_URL)
    response = httpx.Response(429, request=request)
    capture = {}

    mock_news_client(monkeypatch, [response], capture)

    with pytest.raises(HTTPException) as exc:
        await get_top_headlines()

    assert exc.value.status_code == 429
    assert exc.value.detail == "NewsAPI rate limit reached. Try again later."


@pytest.mark.asyncio
async def test_news_maps_other_provider_http_errors(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "test-api-key")
    request = httpx.Request("GET", NEWS_API_URL)
    response = httpx.Response(503, request=request)
    capture = {}

    mock_news_client(monkeypatch, [response], capture)

    with pytest.raises(HTTPException) as exc:
        await get_top_headlines()

    assert exc.value.status_code == 502
    assert exc.value.detail == (
        "The news provider rejected the request. Check API access and credentials."
    )


@pytest.mark.asyncio
async def test_news_rejects_provider_error_payload(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "test-api-key")
    capture = {}

    mock_news_client(
        monkeypatch,
        [response_with_json({"status": "error", "message": "Invalid API key"})],
        capture,
    )

    with pytest.raises(HTTPException) as exc:
        await get_top_headlines()

    assert exc.value.status_code == 502
    assert exc.value.detail == "The news provider returned an error."


@pytest.mark.asyncio
async def test_news_rejects_invalid_article_list(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "test-api-key")
    capture = {}

    mock_news_client(
        monkeypatch,
        [
            response_with_json(
                {"status": "ok", "totalResults": 1, "articles": "invalid"}
            )
        ],
        capture,
    )

    with pytest.raises(HTTPException) as exc:
        await get_top_headlines()

    assert exc.value.status_code == 502
    assert exc.value.detail == ("The news provider returned an invalid article list.")


@pytest.mark.asyncio
async def test_news_maps_invalid_json_response(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "test-api-key")
    request = httpx.Request("GET", NEWS_API_URL)
    response = httpx.Response(200, text="not valid JSON", request=request)
    capture = {}

    mock_news_client(monkeypatch, [response], capture)

    with pytest.raises(HTTPException) as exc:
        await get_top_headlines()

    assert exc.value.status_code == 502
    assert exc.value.detail == "Unable to retrieve news right now."
