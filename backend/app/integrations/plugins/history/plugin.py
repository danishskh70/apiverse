from app.schemas.integration import IntegrationManifest

manifest = IntegrationManifest(
    name="This Day in History",
    slug="history",
    category="education",
    description="Discover notable historical events from this day.",
    icon="history",
    tags=["history", "events", "today", "learning"],
)
