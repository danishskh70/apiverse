from types import SimpleNamespace

import pytest

from app.integrations import registry
from app.schemas.integration import IntegrationManifest

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


def test_discovers_all_nine_plugins() -> None:
    integrations = registry.discover_integrations()

    assert {item.slug for item in integrations} == EXPECTED_PLUGINS
    assert len(integrations) == len(EXPECTED_PLUGINS)


def test_plugin_slugs_are_unique() -> None:
    integrations = registry.discover_integrations()
    slugs = [item.slug for item in integrations]

    assert len(slugs) == len(set(slugs))


def test_duplicate_slugs_are_rejected(monkeypatch) -> None:
    manifest = IntegrationManifest(
        name="Test",
        slug="test",
        category="testing",
        description="Test plugin.",
        icon="flask",
    )

    monkeypatch.setattr(
        registry,
        "iter_modules",
        lambda *args, **kwargs: [
            SimpleNamespace(name="fake.first", ispkg=True),
            SimpleNamespace(name="fake.second", ispkg=True),
        ],
    )
    monkeypatch.setattr(
        registry,
        "import_module",
        lambda name: SimpleNamespace(manifest=manifest),
    )

    with pytest.raises(RuntimeError, match="Duplicate integration slug"):
        registry.discover_integrations()


def test_invalid_manifest_is_rejected(monkeypatch) -> None:
    monkeypatch.setattr(
        registry,
        "iter_modules",
        lambda *args, **kwargs: [
            SimpleNamespace(name="fake.invalid", ispkg=True),
        ],
    )
    monkeypatch.setattr(
        registry,
        "import_module",
        lambda name: SimpleNamespace(manifest="not a manifest"),
    )

    with pytest.raises(RuntimeError, match="no valid manifest"):
        registry.discover_integrations()
