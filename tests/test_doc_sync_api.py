"""Startup and configuration tests for the Doc-Sync API runtime."""

import subprocess
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import src.doc_sync_api as api


def test_application_requires_store_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(api.STORE_PATH_ENV, raising=False)

    with pytest.raises(RuntimeError, match="DOC_SYNC_STORE_PATH must be configured"):
        api.get_configured_store_path()


def test_application_rejects_relative_store_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(api.STORE_PATH_ENV, "documents/store.json")

    with pytest.raises(RuntimeError, match="must be an absolute path"):
        api.get_configured_store_path()


@pytest.mark.parametrize(
    "unc_path",
    [
        r"\\server\share\store.json",
        "//server/share/store.json",
        r"\\?\UNC\server\share\store.json",
    ],
)
def test_application_rejects_unc_store_path(
    monkeypatch: pytest.MonkeyPatch,
    unc_path: str,
) -> None:
    monkeypatch.setenv(api.STORE_PATH_ENV, unc_path)

    with pytest.raises(
        RuntimeError,
        match="UNC network paths are unsupported",
    ):
        api.get_configured_store_path()


def test_application_rejects_detectable_mapped_remote_drive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    configured_path = r"Z:\documents\store.json"
    queried_roots: list[str] = []

    def remote_drive_type(drive_root: str) -> int:
        queried_roots.append(drive_root)
        return api._DRIVE_REMOTE

    monkeypatch.setenv(api.STORE_PATH_ENV, configured_path)
    monkeypatch.setattr(api, "_get_windows_drive_type", remote_drive_type)

    with pytest.raises(
        RuntimeError,
        match="detectable remote drive paths are unsupported",
    ):
        api.get_configured_store_path()

    assert queried_roots == ["Z:\\"]


@pytest.mark.parametrize(
    ("drive_type", "description"),
    [
        (0, "unknown"),
        (3, "local fixed"),
    ],
)
def test_application_does_not_treat_unknown_or_local_drive_as_remote(
    monkeypatch: pytest.MonkeyPatch,
    drive_type: int,
    description: str,
) -> None:
    monkeypatch.setattr(
        api,
        "_get_windows_drive_type",
        lambda drive_root: drive_type,
    )

    assert not api._is_windows_remote_drive_path(r"Z:\documents\store.json"), (
        f"A {description} drive type must not be reported as a detectable "
        "remote drive"
    )


def test_application_accepts_existing_local_store_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    store_path = tmp_path / "store.json"
    store_path.write_text("{}", encoding="utf-8")
    monkeypatch.setenv(api.STORE_PATH_ENV, str(store_path))

    assert api.get_configured_store_path() == store_path.resolve(strict=False)


def test_application_rejects_directory_as_store_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(api.STORE_PATH_ENV, str(tmp_path))

    with pytest.raises(
        RuntimeError,
        match="must refer to an existing store file",
    ):
        api.get_configured_store_path()


def test_application_rejects_missing_store_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(api.STORE_PATH_ENV, str(tmp_path / "missing.json"))

    with pytest.raises(
        RuntimeError,
        match="must refer to an existing store file",
    ):
        api.get_configured_store_path()


def test_application_lifespan_fails_when_store_file_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(api.STORE_PATH_ENV, str(tmp_path / "missing.json"))

    with pytest.raises(
        RuntimeError,
        match="must refer to an existing store file",
    ):
        with TestClient(api.app):
            pytest.fail("The application must not start without a store file")


def test_application_lifespan_exposes_absolute_store_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    store_path = tmp_path / "store.json"
    monkeypatch.setattr(
        api,
        "get_configured_store_path",
        lambda: store_path.resolve(strict=False),
    )

    with TestClient(api.app) as client:
        assert client.app.state.store_path == store_path.resolve(strict=False)
        assert isinstance(client.app, FastAPI)
    assert client.app.state.store_path is None


def test_main_uses_approved_uvicorn_runtime(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    store_path = tmp_path / "store.json"
    monkeypatch.setattr(
        api,
        "get_configured_store_path",
        lambda: store_path.resolve(strict=False),
    )
    arguments: dict[str, object] = {}

    def fake_run(application: FastAPI, **kwargs: object) -> None:
        arguments["application"] = application
        arguments.update(kwargs)

    monkeypatch.setattr(api.uvicorn, "run", fake_run)

    api.main()

    assert arguments == {
        "application": api.app,
        "host": "127.0.0.1",
        "port": 8000,
        "workers": 1,
        "reload": False,
    }


def test_scanner_cli_still_generates_local_repository_document(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "sample-repository"
    repository.mkdir()
    (repository / "README.md").write_text(
        "# Sample repository\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "PROJECT_DOC.md"
    project_root = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.doc_sync",
            str(repository),
            "--output",
            str(output_path),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output_path.is_file()
    generated_document = output_path.read_text(encoding="utf-8")
    assert "sample-repository" in generated_document
    assert result.stdout == generated_document
