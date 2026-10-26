from app.schemas.integration import IntegrationManifest

manifest = IntegrationManifest(
    name="Daily Inspiration",
    slug="quotes",
    category="lifestyle",
    description="Discover daily inspirational quotes and their authors.",
    icon="quote",
    tags=["quotes", "inspiration", "daily"],
)
