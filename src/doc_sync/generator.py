"""Generate repository documentation for a local repo or GitHub URL."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

import requests


MISSING = "Not Found"


def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def read_repo_description(repo_path: str | Path) -> str:
    """Return the repository description from README.md or the project metadata."""
    root = Path(repo_path)
    readme_candidates = [root / "README.md", root / "readme.md", root / "README.rst"]
    for candidate in readme_candidates:
        if candidate.exists():
            text = _safe_read_text(candidate)
            for line in text.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    if stripped.startswith("# "):
                        title = stripped[2:].strip()
                        if title:
                            return title
                    continue
                if stripped:
                    return stripped
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            import tomllib

            with pyproject.open("rb") as handle:
                data = tomllib.load(handle)
            project = data.get("project") or {}
            description = project.get("description")
            if description:
                return description
        except (OSError, ValueError, TypeError):
            pass
    return MISSING


def detect_languages(repo_path: str | Path) -> str:
    """Detect the programming languages used in the repository."""
    root = Path(repo_path)
    if not root.exists() or not any(root.iterdir()):
        return MISSING

    languages: set[str] = set()
    extension_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".md": "Markdown",
    }
    for path in root.rglob("*"):
        if path.is_file():
            suffix = path.suffix.lower()
            language = extension_map.get(suffix)
            if language:
                languages.add(language)

    if not languages:
        return MISSING
    return ", ".join(sorted(languages))


def detect_dependencies(repo_path: str | Path) -> str:
    """Return the project dependencies from the standard packaging manifests."""
    root = Path(repo_path)
    if not root.exists():
        return MISSING

    for manifest in (root / "requirements.txt", root / "pyproject.toml", root / "Pipfile"):
        if manifest.exists():
            text = _safe_read_text(manifest)
            if not text.strip():
                return MISSING
            if manifest.name == "requirements.txt":
                deps = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")]
                return ", ".join(deps) if deps else MISSING
            if manifest.name == "pyproject.toml":
                try:
                    import tomllib

                    with manifest.open("rb") as handle:
                        data = tomllib.load(handle)
                    deps = data.get("project", {}).get("dependencies", [])
                    if deps:
                        return ", ".join(deps)
                    tool = data.get("tool", {})
                    deps = tool.get("poetry", {}).get("dependencies", {})
                    if deps:
                        cleaned = [f"{name}={value}" for name, value in deps.items() if name != "python"]
                        if cleaned:
                            return ", ".join(cleaned)
                except (OSError, ValueError, TypeError):
                    pass
    return MISSING


def discover_entry_points(repo_path: str | Path) -> str:
    """Return the callable entry points used to run the project."""
    root = Path(repo_path)
    if not root.exists():
        return MISSING

    cli_candidates = [
        root / "src" / "doc_sync" / "__main__.py",
        root / "src" / "__main__.py",
        root / "main.py",
        root / "app.py",
    ]
    for candidate in cli_candidates:
        if candidate.exists():
            module_name = candidate.relative_to(root).with_suffix('').as_posix().replace('/', '.')
            if module_name.endswith(".__main__"):
                module_name = module_name[:-9]
            return f"python -m {module_name}"

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            import tomllib

            with pyproject.open("rb") as handle:
                data = tomllib.load(handle)
            scripts = (data.get("project") or {}).get("scripts") or {}
            if scripts:
                return ", ".join(f"{name}: {command}" for name, command in scripts.items())
        except (OSError, ValueError, TypeError):
            pass

    return MISSING


def determine_how_to_run(repo_path: str | Path) -> str:
    """Return the command used to run the project in a local environment."""
    root = Path(repo_path)
    if not root.exists():
        return MISSING
    if (root / "src" / "doc_sync" / "__main__.py").exists():
        return "python -m src.doc_sync"
    if (root / "src" / "__main__.py").exists():
        return "python -m src"
    if (root / "main.py").exists():
        return "python main.py"
    if (root / "README.md").exists() or (root / "README.rst").exists():
        return "python -m pytest"
    return MISSING


def get_last_commit(repo_path: str | Path) -> str:
    """Return the most recent git commit hash for the repository."""
    repo = Path(repo_path)
    if not repo.exists():
        return MISSING

    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            check=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return MISSING

    commit = result.stdout.strip()
    return commit or MISSING


def fetch_github_repo_metadata(repo_url: str) -> dict[str, str]:
    """Fetch repository metadata from the GitHub API and return it as a dict."""
    sanitized = repo_url.strip()
    if not sanitized or not sanitized.startswith("https://github.com/"):
        return {"name": MISSING, "description": MISSING}

    api_url = sanitized.replace("https://github.com/", "https://api.github.com/repos/")
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return {"name": MISSING, "description": MISSING}

    try:
        data = response.json()
    except ValueError:
        return {"name": MISSING, "description": MISSING}

    return {
        "name": data.get("full_name") or MISSING,
        "description": data.get("description") or MISSING,
    }


def render_project_doc(repo_path: str | Path) -> str:
    """Render the repository overview document using the required section order."""
    root = Path(repo_path)
    name = root.resolve().name if root.exists() else MISSING
    description = read_repo_description(root)
    languages = detect_languages(root)
    dependencies = detect_dependencies(root)
    entry_points = discover_entry_points(root)
    how_to_run = determine_how_to_run(root)
    last_commit = get_last_commit(root)

    return "\n\n".join(
        [
            f"Name\n{name}",
            f"Description\n{description}",
            f"Languages\n{languages}",
            f"Dependencies\n{dependencies}",
            f"Entry Points\n{entry_points}",
            f"How to Run\n{how_to_run}",
            f"Last Commit\n{last_commit}",
        ]
    ) + "\n"


def generate_project_doc(repo_path: str | Path, output_path: str | Path | None = None) -> str:
    """Render and write the PROJECT_DOC.md file for a repo."""
    root = Path(repo_path)
    rendered = render_project_doc(root)
    target = Path(output_path) if output_path is not None else root / "docs" / "PROJECT_DOC.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")
    return rendered


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for generating repository documentation."""
    parser = argparse.ArgumentParser(description="Generate documentation for a repository.")
    parser.add_argument("repo_path", nargs="?", default=".")
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    output = generate_project_doc(args.repo_path, args.output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
