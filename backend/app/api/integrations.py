from fastapi import APIRouter, HTTPException

from app.integrations.registry import (
    get_integration,
    list_integrations,
)
from app.schemas.integration import IntegrationManifest

router = APIRouter(
    prefix="/api/v1/integrations",
    tags=["Integrations"],
)


@router.get("", response_model=list[IntegrationManifest])
async def get_integrations() -> list[IntegrationManifest]:
    return list_integrations()


@router.get("/{slug}", response_model=IntegrationManifest)
async def get_integration_by_slug(slug: str) -> IntegrationManifest:
    integration = get_integration(slug)

    if integration is None:
        raise HTTPException(
            status_code=404,
            detail=f"Integration '{slug}' was not found.",
        )

    return integration
