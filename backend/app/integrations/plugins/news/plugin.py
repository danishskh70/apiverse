
from app.schemas.integration import IntegrationManifest

manifest = IntegrationManifest(
    name="Newsroom",
    slug="news",
    category="news",
    description="Discover news and current events.",
    icon="newspaper",
    requires_api_key=True,
    tags=["news", "headlines"],
)
    