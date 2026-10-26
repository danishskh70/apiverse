from app.schemas.integration import IntegrationManifest

manifest = IntegrationManifest(
    name="Word of the Day",
    slug="word",
    category="education",
    description="Explore word meanings, pronunciation, and examples.",
    icon="book-open",
    tags=["word", "vocabulary", "learning", "daily"],
)