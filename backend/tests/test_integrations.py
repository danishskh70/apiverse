from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

EXPECTED_PLUGINS = {
    "quotes",
    "github",
    "jokebox",
    "news",
    "space",
    "history",
    "weather",
    "word",
    "world-explorer",
}


def test_list_integrations() -> None:
    response = client.get("/api/v1/integrations")

    assert response.status_code == 200

    integrations = response.json()
    assert {item["slug"] for item in integrations} == EXPECTED_PLUGINS
    assert len(integrations) == len(EXPECTED_PLUGINS)


def test_get_weather_integration() -> None:
    response = client.get("/api/v1/integrations/weather")

    assert response.status_code == 200
    assert response.json()["name"] == "Weather"


def test_unknown_integration() -> None:
    response = client.get("/api/v1/integrations/unknown")

    assert response.status_code == 404
