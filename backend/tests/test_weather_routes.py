
from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi.testclient import TestClient

from app.integrations.plugins.weather.routes import router
from app.main import app


client = TestClient(app)


def test_current_weather_success(monkeypatch) -> None:
    expected_data = {
        "latitude": 18.52,
        "longitude": 73.86,
        "timezone": "Asia/Kolkata",
        "current": {
            "temperature_2m": 29.5,
            "relative_humidity_2m": 60,
        },
    }

    mock_weather = AsyncMock(return_value=expected_data)
    monkeypatch.setattr(
        "app.integrations.plugins.weather.routes.get_current_weather",
        mock_weather,
    )

    response = client.get(
        "/api/v1/integrations/weather/current",
        params={"latitude": 18.52, "longitude": 73.86},
    )

    assert response.status_code == 200
    assert response.json() == expected_data
    mock_weather.assert_awaited_once_with(18.52, 73.86)


def test_current_weather_rejects_invalid_coordinates() -> None:
    response = client.get(
        "/api/v1/integrations/weather/current",
        params={"latitude": 100, "longitude": 73.86},
    )

    assert response.status_code == 422


def test_current_weather_provider_failure(monkeypatch) -> None:
    mock_weather = AsyncMock(
        side_effect=httpx.ConnectError("Connection failed")
    )
    monkeypatch.setattr(
        "app.integrations.plugins.weather.routes.get_current_weather",
        mock_weather,
    )

    response = client.get(
        "/api/v1/integrations/weather/current",
        params={"latitude": 18.52, "longitude": 73.86},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "The weather provider is currently unavailable."
    )
