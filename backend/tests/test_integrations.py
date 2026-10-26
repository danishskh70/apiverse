
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_integrations() -> None:
    response = client.get("/api/v1/integrations")

    assert response.status_code == 200

    integrations = response.json()
    assert len(integrations) == 6
    assert any(item["slug"] == "weather" for item in integrations)


def test_get_weather_integration() -> None:
    response = client.get("/api/v1/integrations/weather")

    assert response.status_code == 200
    assert response.json()["name"] == "Weather"


def test_unknown_integration() -> None:
    response = client.get("/api/v1/integrations/unknown")

    assert response.status_code == 404
