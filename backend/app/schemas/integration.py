
from pydantic import BaseModel, Field


class IntegrationManifest(BaseModel):
    name: str
    slug: str
    category: str
    description: str
    icon: str
    requires_api_key: bool = False
    enabled: bool = True
    tags: list[str] = Field(default_factory=list)
