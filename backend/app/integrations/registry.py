
from importlib import import_module
from pkgutil import iter_modules

from app.integrations import plugins
from app.schemas.integration import IntegrationManifest


def discover_integrations() -> list[IntegrationManifest]:
    integrations: list[IntegrationManifest] = []
    seen_slugs: set[str] = set()

    for module_info in iter_modules(
        plugins.__path__,
        prefix=f"{plugins.__name__}.",
    ):
        if not module_info.ispkg:
            continue

        plugin_module = import_module(
            f"{module_info.name}.plugin"
        )

        manifest = getattr(plugin_module, "manifest", None)

        if not isinstance(manifest, IntegrationManifest):
            raise RuntimeError(
                f"Plugin '{module_info.name}' has no valid manifest."
            )

        if manifest.slug in seen_slugs:
            raise RuntimeError(
                f"Duplicate integration slug: '{manifest.slug}'."
            )

        seen_slugs.add(manifest.slug)

        if manifest.enabled:
            integrations.append(manifest)

    return sorted(integrations, key=lambda item: item.name.lower())


def list_integrations() -> list[IntegrationManifest]:
    return discover_integrations()


def get_integration(slug: str) -> IntegrationManifest | None:
    for integration in discover_integrations():
        if integration.slug == slug:
            return integration
    return None
