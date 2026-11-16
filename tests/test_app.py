import importlib
import os

from fastapi.testclient import TestClient

import src.app as app_module

app = app_module.app
client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hello_endpoint() -> None:
    response = client.get("/hello/world")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}


def test_app_uses_development_and_local_defaults_when_env_vars_are_unset(
    monkeypatch,
) -> None:
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("APP_REGION", raising=False)

    reloaded_app = importlib.reload(app_module)

    assert reloaded_app.version() == {
        "version": "1.0.0",
        "environment": "development",
        "region": "local",
    }


def test_version_endpoint_returns_exact_default_contract() -> None:
    original_env = os.environ.get("APP_ENV")
    original_region = os.environ.get("APP_REGION")

    try:
        os.environ.pop("APP_ENV", None)
        os.environ.pop("APP_REGION", None)
        importlib.reload(app_module)
        response = client.get("/version")

        assert response.status_code == 200
        payload = response.json()
        assert set(payload) == {"version", "environment", "region"}
        assert payload["version"] == "1.0.0"
        assert payload["environment"] == "development"
        assert payload["region"] == "local"
        assert isinstance(payload["version"], str)
        assert isinstance(payload["environment"], str)
        assert isinstance(payload["region"], str)
    finally:
        if original_env is None:
            os.environ.pop("APP_ENV", None)
        else:
            os.environ["APP_ENV"] = original_env

        if original_region is None:
            os.environ.pop("APP_REGION", None)
        else:
            os.environ["APP_REGION"] = original_region
