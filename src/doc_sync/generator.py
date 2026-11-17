"""Generate repository documentation for a local or GitHub repository."""

from __future__ import annotations

import argparse
import base64
import binascii
import configparser
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from urllib.parse import quote

import requests


MISSING = "Not Found"
_IGNORED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}
_LANGUAGE_BY_EXTENSION = {
    ".c": "C",
    ".cpp": "C++",
    ".cs": "C#",
    ".go": "Go",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".php": "PHP",
    ".py": "Python",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
}
_SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b([A-Z0-9_-]*(?:password|passwd|secret|token|api[_-]?key|"
    r"authorization)[A-Z0-9_-]*)\b\s*([=:])\s*[^\r\n]*"
)
_KNOWN_SECRET = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9_]{12,}|github_pat_[A-Za-z0-9_]{12,}|"
    r"AKIA[A-Z0-9]{16}|sk-[A-Za-z0-9_-]{16,})\b"
)
_BEARER_SECRET = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]+=*")
_URL_CREDENTIALS = re.compile(r"(https?://)[^/\s:@]+(?::[^/\s@]*)?@")
_WINDOWS_PATH = re.compile(r"(?<!\w)(?:[A-Za-z]:[\\/]|\\\\[^\\\s]+\\)[^\r\n]*")
_UNIX_PATH = re.compile(r"(?<![\w:/])/(?:[^/\r\n]+)")
_COMMON_ENTRY_POINT_PATHS = (
    "main.py",
    "app.py",
    "cli.py",
    "manage.py",
    "src/main.py",
    "src/app.py",
    "src/cli.py",
    "src/__main__.py",
    "src/doc_sync/__main__.py",
    "__main__.py",
)
_README_PATHS = ("README.md", "readme.md", "README.rst", "README")


class GitHubAPIError(RuntimeError):
    """A sanitized GitHub API error suitable for CLI output."""


def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _sanitize_value(value: str) -> str:
    """Redact recognized credentials and absolute local paths from output."""
    sanitized = _SECRET_ASSIGNMENT.sub(
        lambda match: f"{match.group(1)}{match.group(2)} [REDACTED]",
        value,
    )
    sanitized = _KNOWN_SECRET.sub("[REDACTED]", sanitized)
    sanitized = _BEARER_SECRET.sub("Bearer [REDACTED]", sanitized)
    sanitized = _URL_CREDENTIALS.sub(r"\1[REDACTED]@", sanitized)
    sanitized = _WINDOWS_PATH.sub("[REDACTED]", sanitized)
    sanitized = _UNIX_PATH.sub("[REDACTED]", sanitized)
    return sanitized.strip() or MISSING


def _repository_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, directories, filenames in os.walk(root):
        directories[:] = sorted(
            name for name in directories if name not in _IGNORED_DIRECTORIES
        )
        current_path = Path(current)
        for filename in sorted(filenames):
            path = current_path / filename
            relative = path.relative_to(root).as_posix()
            if relative == "docs/PROJECT_DOC.md":
                continue
            files.append(path)
    return files


def _readme_summary(text: str) -> str:
    paragraph: list[str] = []
    started = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if started:
                break
            continue
        if stripped.startswith("#") and not started:
            continue
        started = True
        paragraph.append(stripped)
    return _sanitize_value(" ".join(paragraph)) if paragraph else MISSING


def read_repo_description(repo_path: str | Path) -> str:
    """Return the first non-empty README paragraph."""
    root = Path(repo_path)
    for relative in _README_PATHS:
        candidate = root / relative
        if candidate.is_file():
            return _readme_summary(_safe_read_text(candidate))
    return MISSING


def detect_languages(repo_path: str | Path) -> str:
    """Detect programming languages from repository source-file extensions."""
    root = Path(repo_path)
    if not root.is_dir():
        return MISSING

    languages = {
        _LANGUAGE_BY_EXTENSION[path.suffix.lower()]
        for path in _repository_files(root)
        if path.suffix.lower() in _LANGUAGE_BY_EXTENSION
    }
    return ", ".join(sorted(languages)) if languages else MISSING


def detect_dependencies(repo_path: str | Path) -> str:
    """Return dependencies listed in requirements.txt, if present."""
    manifest = Path(repo_path) / "requirements.txt"
    if not manifest.is_file():
        return MISSING

    return _dependencies_from_text(_safe_read_text(manifest))


def _dependencies_from_text(text: str) -> str:
    dependencies = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not dependencies:
        return MISSING
    return _sanitize_value(", ".join(dependencies))


def _declared_scripts(root: Path) -> list[tuple[str, str]]:
    manifest = root / "pyproject.toml"
    scripts = (
        _declared_scripts_from_text(_safe_read_text(manifest))
        if manifest.is_file()
        else []
    )
    setup_config = root / "setup.cfg"
    if setup_config.is_file():
        scripts.extend(_setup_cfg_scripts_from_text(_safe_read_text(setup_config)))
    return sorted(set(scripts))


def _declared_scripts_from_text(text: str) -> list[tuple[str, str]]:
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return []

    project = data.get("project")
    if not isinstance(project, dict):
        project = {}
    tool = data.get("tool")
    if not isinstance(tool, dict):
        tool = {}
    poetry = tool.get("poetry")
    if not isinstance(poetry, dict):
        poetry = {}
    scripts: list[tuple[str, str]] = []
    for section in (
        project.get("scripts") or {},
        project.get("gui-scripts") or {},
        poetry.get("scripts") or {},
    ):
        if isinstance(section, dict):
            scripts.extend(
                (str(name), str(target))
                for name, target in section.items()
                if isinstance(target, str)
            )
    return sorted(set(scripts))


def _setup_cfg_scripts_from_text(text: str) -> list[tuple[str, str]]:
    parser = configparser.ConfigParser(interpolation=None)
    try:
        parser.read_string(text)
    except configparser.Error:
        return []

    section = "options.entry_points"
    if not parser.has_section(section):
        return []
    scripts: list[tuple[str, str]] = []
    for key in ("console_scripts", "gui_scripts"):
        for line in parser.get(section, key, fallback="").splitlines():
            name, separator, target = line.partition("=")
            if separator and name.strip() and target.strip():
                scripts.append((name.strip(), target.strip()))
    return sorted(set(scripts))


def _common_entry_points(root: Path) -> list[tuple[str, str]]:
    existing = {
        relative
        for relative in _COMMON_ENTRY_POINT_PATHS
        if (root / relative).is_file()
    }
    return _common_entry_points_for_paths(existing)


def _common_entry_points_for_paths(file_paths: set[str]) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for relative in _COMMON_ENTRY_POINT_PATHS:
        if relative not in file_paths:
            continue
        if relative == "src/__main__.py":
            command = "python -m src"
        elif relative == "src/doc_sync/__main__.py":
            command = "python -m src.doc_sync"
        elif relative == "__main__.py":
            command = "python __main__.py"
        else:
            command = f"python {relative}"
        found.append((relative, command))
    return found


def discover_entry_points(repo_path: str | Path) -> str:
    """Return common script and declared packaging entry points."""
    root = Path(repo_path)
    if not root.is_dir():
        return MISSING

    entry_points = [command for _, command in _common_entry_points(root)]
    entry_points.extend(
        f"{name}: {target}" for name, target in _declared_scripts(root)
    )
    if not entry_points:
        return MISSING
    return _sanitize_value(", ".join(dict.fromkeys(entry_points)))


def determine_how_to_run(repo_path: str | Path) -> str:
    """Return commands directly supported by detected entry points."""
    root = Path(repo_path)
    if not root.is_dir():
        return MISSING

    commands = [command for _, command in _common_entry_points(root)]
    commands.extend(name for name, _ in _declared_scripts(root))
    return _sanitize_value(", ".join(dict.fromkeys(commands))) if commands else MISSING


def get_last_commit(repo_path: str | Path) -> str:
    """Return the most recent git commit hash for the repository."""
    repo = Path(repo_path)
    if not repo.is_dir():
        return MISSING

    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            check=True,
            text=True,
            timeout=5,
        )
    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ):
        return MISSING

    return _sanitize_value(result.stdout.strip())


def _validate_github_repo(repository: str) -> tuple[str, str]:
    parts = repository.split("/")
    if len(parts) != 2:
        raise ValueError("GitHub repository must be in owner/name form")
    owner, name = parts
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", owner):
        raise ValueError("GitHub repository must be in owner/name form")
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?", name):
        raise ValueError("GitHub repository must be in owner/name form")
    return owner, name


def _github_api_json(url: str, not_found_message: str) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.Timeout:
        raise GitHubAPIError("GitHub API request timed out") from None
    except requests.RequestException:
        raise GitHubAPIError("GitHub API request failed") from None

    status = response.status_code
    response_headers = response.headers or {}
    if status == 404:
        raise GitHubAPIError(not_found_message)
    if status in (403, 429):
        rate_message = False
        try:
            response_data = response.json()
            message = (
                response_data.get("message", "")
                if isinstance(response_data, dict)
                else ""
            )
            rate_message = "rate limit" in str(message).lower()
        except ValueError:
            pass
        if (
            status == 429
            or response_headers.get("X-RateLimit-Remaining") == "0"
            or response_headers.get("Retry-After")
            or rate_message
        ):
            raise GitHubAPIError("GitHub API rate limit exceeded")
    if status >= 400:
        raise GitHubAPIError(f"GitHub API request failed with HTTP {status}")

    try:
        data = response.json()
    except ValueError:
        raise GitHubAPIError("GitHub API returned an invalid response") from None
    return data


def fetch_github_repo_metadata(repo_url: str) -> dict[str, str]:
    """Fetch GitHub repository metadata and return the documented fields."""
    prefix = "https://github.com/"
    if not repo_url.startswith(prefix):
        raise ValueError("GitHub repository must be in owner/name form")
    owner, name = _validate_github_repo(repo_url[len(prefix) :].strip("/"))
    url = f"https://api.github.com/repos/{quote(owner)}/{quote(name)}"
    data = _github_api_json(url, "GitHub repository not found")
    if not isinstance(data, dict):
        raise GitHubAPIError("GitHub API returned an invalid response")
    return {
        "name": _sanitize_value(str(data.get("full_name") or MISSING)),
        "description": _sanitize_value(str(data.get("description") or MISSING)),
    }


def _render_values(values: list[str]) -> str:
    sections = (
        "Name",
        "Description",
        "Languages",
        "Dependencies",
        "Entry Points",
        "How to Run",
        "Last Commit",
    )
    return "\n\n".join(
        f"{section}\n{value}" for section, value in zip(sections, values)
    ) + "\n"


def render_project_doc(repo_path: str | Path) -> str:
    """Render repository facts using the required section order."""
    root = Path(repo_path)
    if not root.is_dir() or not _repository_files(root):
        values = [MISSING] * 7
    else:
        values = [
            _sanitize_value(root.resolve().name),
            read_repo_description(root),
            detect_languages(root),
            detect_dependencies(root),
            discover_entry_points(root),
            determine_how_to_run(root),
            get_last_commit(root),
        ]

    return _render_values(values)


def _read_github_blob(base_url: str, item: dict[str, object]) -> str:
    sha = item.get("sha")
    if not isinstance(sha, str) or not sha:
        raise GitHubAPIError("GitHub API returned an invalid file reference")
    data = _github_api_json(
        f"{base_url}/git/blobs/{quote(sha, safe='')}",
        "GitHub repository file was not found",
    )
    if not isinstance(data, dict):
        raise GitHubAPIError("GitHub API returned an invalid file response")
    content = data.get("content")
    encoding = data.get("encoding")
    if not isinstance(content, str) or encoding != "base64":
        raise GitHubAPIError("GitHub API returned an invalid file response")
    try:
        encoded_content = "".join(content.split())
        decoded = base64.b64decode(encoded_content, validate=True)
        return decoded.decode("utf-8", errors="replace")
    except (binascii.Error, ValueError):
        raise GitHubAPIError("GitHub API returned an invalid file response") from None


def _is_ignored_repository_file(path: str) -> bool:
    return path == "docs/PROJECT_DOC.md" or any(
        part in _IGNORED_DIRECTORIES for part in path.split("/")
    )


def render_github_project_doc(repository: str) -> str:
    """Fetch GitHub repository facts and render the standard document."""
    owner, name = _validate_github_repo(repository)
    base_url = (
        f"https://api.github.com/repos/{quote(owner)}/{quote(name)}"
    )
    metadata = _github_api_json(base_url, "GitHub repository not found")
    if not isinstance(metadata, dict):
        raise GitHubAPIError("GitHub API returned an invalid repository response")

    if "default_branch" not in metadata:
        raise GitHubAPIError("GitHub API returned an invalid repository response")
    branch = metadata["default_branch"]
    if branch is None:
        return _render_values([MISSING] * 7)
    if not isinstance(branch, str) or not branch:
        raise GitHubAPIError("GitHub API returned an invalid repository response")

    tree_data = _github_api_json(
        f"{base_url}/git/trees/{quote(branch, safe='')}?recursive=1",
        "GitHub repository contents were not found",
    )
    if not isinstance(tree_data, dict) or not isinstance(tree_data.get("tree"), list):
        raise GitHubAPIError("GitHub API returned an invalid file inventory")
    if tree_data.get("truncated"):
        raise GitHubAPIError("GitHub repository file inventory is too large to scan")

    files: dict[str, dict[str, object]] = {}
    for item in tree_data["tree"]:
        if not isinstance(item, dict):
            raise GitHubAPIError("GitHub API returned an invalid file inventory")
        path = item.get("path")
        item_type = item.get("type")
        if not isinstance(path, str) or not isinstance(item_type, str):
            raise GitHubAPIError("GitHub API returned an invalid file inventory")
        if item_type == "blob" and not _is_ignored_repository_file(path):
            files[path] = item

    if not files:
        return _render_values([MISSING] * 7)

    readme = next((path for path in _README_PATHS if path in files), None)
    description = (
        _readme_summary(_read_github_blob(base_url, files[readme]))
        if readme is not None
        else MISSING
    )
    requirements = (
        _dependencies_from_text(_read_github_blob(base_url, files["requirements.txt"]))
        if "requirements.txt" in files
        else MISSING
    )
    pyproject = (
        _read_github_blob(base_url, files["pyproject.toml"])
        if "pyproject.toml" in files
        else ""
    )
    setup_config = (
        _read_github_blob(base_url, files["setup.cfg"])
        if "setup.cfg" in files
        else ""
    )
    scripts = _declared_scripts_from_text(pyproject)
    scripts.extend(_setup_cfg_scripts_from_text(setup_config))
    scripts = sorted(set(scripts))
    common_entries = _common_entry_points_for_paths(set(files))
    entry_points = [command for _, command in common_entries]
    entry_points.extend(f"{script}: {target}" for script, target in scripts)
    how_to_run = [command for _, command in common_entries]
    how_to_run.extend(script for script, _ in scripts)

    languages = {
        _LANGUAGE_BY_EXTENSION[Path(path).suffix.lower()]
        for path in files
        if Path(path).suffix.lower() in _LANGUAGE_BY_EXTENSION
    }
    commit_data = _github_api_json(
        f"{base_url}/commits/{quote(branch, safe='')}",
        "GitHub repository commit was not found",
    )
    if not isinstance(commit_data, dict):
        raise GitHubAPIError("GitHub API returned an invalid commit response")
    commit_sha = commit_data.get("sha")

    values = [
        _sanitize_value(str(metadata.get("full_name") or MISSING)),
        description,
        ", ".join(sorted(languages)) if languages else MISSING,
        requirements,
        _sanitize_value(", ".join(dict.fromkeys(entry_points)))
        if entry_points
        else MISSING,
        _sanitize_value(", ".join(dict.fromkeys(how_to_run)))
        if how_to_run
        else MISSING,
        _sanitize_value(commit_sha[:7])
        if isinstance(commit_sha, str) and commit_sha
        else MISSING,
    ]
    return _render_values(values)


def generate_project_doc(
    repo_path: str | Path, output_path: str | Path | None = None
) -> str:
    """Render and write the PROJECT_DOC.md file for a local repository."""
    root = Path(repo_path)
    if not root.exists():
        raise ValueError("repository path does not exist")
    if not root.is_dir():
        raise ValueError("repository path is not a directory")

    rendered = render_project_doc(root)
    target = (
        Path(output_path)
        if output_path is not None
        else root / "docs" / "PROJECT_DOC.md"
    )
    _write_project_doc(rendered, target)
    return rendered


def generate_github_project_doc(
    repository: str, output_path: str | Path | None = None
) -> str:
    """Render a GitHub repository and write its documentation locally."""
    rendered = render_github_project_doc(repository)
    target = (
        Path(output_path)
        if output_path is not None
        else Path("docs") / "PROJECT_DOC.md"
    )
    _write_project_doc(rendered, target)
    return rendered


def _write_project_doc(rendered: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Run the command-line documentation generator."""
    parser = argparse.ArgumentParser(description="Generate repository documentation.")
    parser.add_argument("repo_path", nargs="?", default=".")
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    try:
        repository_path = Path(args.repo_path)
        if repository_path.exists():
            output = generate_project_doc(repository_path, args.output)
        else:
            if (
                repository_path.is_absolute()
                or "\\" in args.repo_path
                or args.repo_path.startswith((".", "~"))
            ):
                raise ValueError("repository path does not exist")
            _validate_github_repo(args.repo_path)
            output = generate_github_project_doc(args.repo_path, args.output)
    except ValueError as error:
        print(f"doc-sync: {error}", file=sys.stderr)
        return 2
    except GitHubAPIError as error:
        print(f"doc-sync: {error}", file=sys.stderr)
        return 1
    except OSError:
        print(
            "doc-sync: unable to read repository or write documentation",
            file=sys.stderr,
        )
        return 1

    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
