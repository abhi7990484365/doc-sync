"""FastAPI application entry point for Doc-Sync."""

from __future__ import annotations

import ctypes
import os
from contextlib import asynccontextmanager
from pathlib import Path, PureWindowsPath
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI


STORE_PATH_ENV = "DOC_SYNC_STORE_PATH"
_DRIVE_REMOTE = 4


def _is_windows_unc_path(path: str | Path) -> bool:
    """Return whether a path uses Windows UNC network-path syntax."""
    drive = PureWindowsPath(str(path)).drive
    if not drive.startswith("\\\\"):
        return False

    components = drive[2:].split("\\")
    if components[0].casefold() in {"?", "."}:
        return len(components) > 1 and components[1].casefold() == "unc"
    return len(components) >= 2


def _get_windows_drive_type(drive_root: str) -> int | None:
    """Return the Windows drive type, or None when this is not Windows."""
    if os.name != "nt":
        return None

    get_drive_type = ctypes.windll.kernel32.GetDriveTypeW
    get_drive_type.argtypes = [ctypes.c_wchar_p]
    get_drive_type.restype = ctypes.c_uint
    return int(get_drive_type(drive_root))


def _is_windows_remote_drive_path(path: str | Path) -> bool:
    """Return whether a Windows drive-letter path is on a remote drive."""
    windows_path = PureWindowsPath(str(path))
    drive = windows_path.drive
    if (
        not windows_path.is_absolute()
        or len(drive) != 2
        or drive[1] != ":"
    ):
        return False

    drive_type = _get_windows_drive_type(f"{drive}\\")
    return drive_type == _DRIVE_REMOTE


def get_configured_store_path() -> Path:
    """Return the configured local store path if it is an existing file.

    Detectable UNC paths and Windows mapped remote drives are rejected.
    Mounted network filesystems that cannot be reliably identified remain
    unsupported operationally but may not be automatically detectable.
    """
    configured_path = os.environ.get(STORE_PATH_ENV)
    if not configured_path:
        raise RuntimeError(f"{STORE_PATH_ENV} must be configured")

    if _is_windows_unc_path(configured_path):
        raise RuntimeError(
            f"{STORE_PATH_ENV} must use a local filesystem path; "
            "UNC network paths are unsupported"
        )
    if _is_windows_remote_drive_path(configured_path):
        raise RuntimeError(
            f"{STORE_PATH_ENV} must use a local filesystem path; "
            "detectable remote drive paths are unsupported"
        )

    store_path = Path(configured_path)
    if not store_path.is_absolute():
        raise RuntimeError(f"{STORE_PATH_ENV} must be an absolute path")
    resolved_path = store_path.resolve(strict=False)
    if _is_windows_unc_path(resolved_path):
        raise RuntimeError(
            f"{STORE_PATH_ENV} must use a local filesystem path; "
            "UNC network paths are unsupported"
        )
    if _is_windows_remote_drive_path(resolved_path):
        raise RuntimeError(
            f"{STORE_PATH_ENV} must use a local filesystem path; "
            "detectable remote drive paths are unsupported"
        )
    if not resolved_path.is_file():
        raise RuntimeError(
            f"{STORE_PATH_ENV} must refer to an existing store file"
        )
    return resolved_path


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Validate runtime configuration for the lifetime of the API process."""
    application.state.store_path = get_configured_store_path()
    try:
        yield
    finally:
        application.state.store_path = None


app = FastAPI(lifespan=lifespan)


def main() -> None:
    """Start the approved loopback-only Uvicorn runtime."""
    get_configured_store_path()
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        workers=1,
        reload=False,
    )


if __name__ == "__main__":
    main()
