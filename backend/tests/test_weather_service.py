
import httpx
import pytest

from app.integrations.plugins.weather.service import get_current_weather


@pytest.mark.asyncio
async def test_get_current_weather_success(monkeypatch) -> None:
    expected_data = {
        "latitude": 18.52,
        "longitude": 73.86,
        "timezone": "Asia/Kolkata",
        "current": {
            "temperature_2m": 29.5,
            "relative_humidity_2m": 60,
            "apparent_temperature": 31.0,
            "is_day": 1,
            "precipitation": 0.0,
            "weather_code": 1,
            "wind_speed_10m": 8.2,
        },
    }

    class MockResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> dict:
            return expected_data

    class MockClient:
        def __init__(self, *args, **kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args) -> None:
            pass

        async def get(self, *args, **kwargs) -> MockResponse:
            return MockResponse()

    monkeypatch.setattr(
        "app.integrations.plugins.weather.service.httpx.AsyncClient",
        MockClient,
    )

    result = await get_current_weather(18.52, 73.86)

    assert result == {
    **expected_data,
    "condition": "Mainly clear",
}


@pytest.mark.asyncio
async def test_get_current_weather_http_error(monkeypatch) -> None:
    class MockClient:
        def __init__(self, *args, **kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args) -> None:
            pass

        async def get(self, *args, **kwargs):
            request = httpx.Request(
                "GET",
                "https://api.open-meteo.com/v1/forecast",
            )
            response = httpx.Response(503, request=request)
            response.raise_for_status()

    monkeypatch.setattr(
        "app.integrations.plugins.weather.service.httpx.AsyncClient",
        MockClient,
    )

    with pytest.raises(httpx.HTTPStatusError):
        await get_current_weather(18.52, 73.86)


@pytest.mark.asyncio
async def test_get_current_weather_invalid_response(monkeypatch) -> None:
    class MockResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> dict:
            return {"latitude": 18.52, "longitude": 73.86}

    class MockClient:
        def __init__(self, *args, **kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args) -> None:
            pass

        async def get(self, *args, **kwargs) -> MockResponse:
            return MockResponse()

    monkeypatch.setattr(
        "app.integrations.plugins.weather.service.httpx.AsyncClient",
        MockClient,
    )

    with pytest.raises(ValueError, match="Invalid weather data"):
        await get_current_weather(18.52, 73.86)


@pytest.mark.asyncio
async def test_weather_code_is_converted_to_condition(monkeypatch) -> None:
    class MockResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> dict:
            return {
                "latitude": 18.52,
                "longitude": 73.86,
                "timezone": "Asia/Kolkata",
                "current": {"weather_code": 0},
            }

    class MockClient:
        def __init__(self, *args, **kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args) -> None:
            pass

        async def get(self, *args, **kwargs) -> MockResponse:
            return MockResponse()

    monkeypatch.setattr(
        "app.integrations.plugins.weather.service.httpx.AsyncClient",
        MockClient,
    )

    result = await get_current_weather(18.52, 73.86)

    assert result["condition"] == "Clear sky"


@pytest.mark.asyncio
async def test_unknown_weather_code_uses_fallback(monkeypatch) -> None:
    class MockResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> dict:
            return {
                "latitude": 18.52,
                "longitude": 73.86,
                "timezone": "Asia/Kolkata",
                "current": {"weather_code": 12345},
            }

    class MockClient:
        def __init__(self, *args, **kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args) -> None:
            pass

        async def get(self, *args, **kwargs) -> MockResponse:
            return MockResponse()

    monkeypatch.setattr(
        "app.integrations.plugins.weather.service.httpx.AsyncClient",
        MockClient,
    )

    result = await get_current_weather(18.52, 73.86)

    assert result["condition"] == "Unknown weather condition"
