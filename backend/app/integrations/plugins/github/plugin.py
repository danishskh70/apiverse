from app.schemas.integration import IntegrationManifest

manifest = IntegrationManifest(
    name="Developer Hub",
    slug="github",
    category="development",
    description="Explore GitHub repositories and developer activity.",
    icon="github",
    tags=["GitHub", "repositories"],
)
