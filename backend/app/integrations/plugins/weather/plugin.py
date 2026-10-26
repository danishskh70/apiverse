
from app.schemas.integration import IntegrationManifest


manifest = IntegrationManifest(
    name="Weather",
    slug="weather",
    category="environment",
    description="Explore current weather and forecasts.",
    icon="cloud-sun",
    tags=["weather", "forecast"],
)
