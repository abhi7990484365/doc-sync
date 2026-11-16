import os
import subprocess
import sys
from pathlib import Path

import requests

from src.doc_sync.generator import (
    detect_dependencies,
    detect_languages,
    fetch_github_repo_metadata,
    generate_project_doc,
    get_last_commit,
    read_repo_description,
    render_project_doc,
)


def test_read_repo_description_happy_path(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Example service\n\nA sample app.\n", encoding="utf-8")

    assert read_repo_description(tmp_path) == "Example service"


def test_read_repo_description_missing_data_returns_not_found(tmp_path: Path) -> None:
    assert read_repo_description(tmp_path) == "Not Found"


def test_detect_languages_happy_path(tmp_path: Path) -> None:
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "app.py").write_text("print('hi')\n", encoding="utf-8")

    assert "Python" in detect_languages(tmp_path)


def test_detect_languages_missing_data_returns_not_found(tmp_path: Path) -> None:
    assert detect_languages(tmp_path) == "Not Found"


def test_detect_dependencies_happy_path(tmp_path: Path) -> None:
    (tmp_path / "requirements.txt").write_text("requests==2.32.3\npytest==8.3.3\n", encoding="utf-8")

    output = detect_dependencies(tmp_path)
    assert "requests==2.32.3" in output
    assert "pytest==8.3.3" in output


def test_detect_dependencies_missing_data_returns_not_found(tmp_path: Path) -> None:
    assert detect_dependencies(tmp_path) == "Not Found"


def test_get_last_commit_happy_path(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.name", "Tester"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "tester@example.com"], cwd=tmp_path, check=True)
    (tmp_path / "README.md").write_text("# Repo\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)

    assert get_last_commit(tmp_path) != "Not Found"


def test_get_last_commit_missing_or_empty_repo_returns_not_found(tmp_path: Path) -> None:
    assert get_last_commit(tmp_path) == "Not Found"


def test_fetch_github_repo_metadata_handles_api_failure(monkeypatch) -> None:
    def raise_error(*args, **kwargs):
        raise requests.RequestException("boom")

    monkeypatch.setattr(requests, "get", raise_error)

    payload = fetch_github_repo_metadata("https://github.com/example/repo")
    assert payload == {"name": "Not Found", "description": "Not Found"}


def test_render_project_doc_has_required_sections_in_order(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Example repo\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("requests\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")

    document = render_project_doc(tmp_path)
    sections = [
        "Name",
        "Description",
        "Languages",
        "Dependencies",
        "Entry Points",
        "How to Run",
        "Last Commit",
    ]
    for index, section in enumerate(sections):
        assert document.index(section) < document.index(sections[index + 1]) if index < len(sections) - 1 else True

    assert "Example repo" in document
    assert "requests" in document
    assert "Python" in document


def test_generate_project_doc_creates_file_and_avoids_secrets(tmp_path: Path) -> None:
    output_path = tmp_path / "docs" / "PROJECT_DOC.md"
    (tmp_path / "README.md").write_text("# Example repo\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")

    generated = generate_project_doc(tmp_path, output_path)

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == generated
    assert "C:\\Users" not in generated
    assert "sk-" not in generated.lower()
    assert "Not Found" in generated


def test_cli_generates_document_for_repo(tmp_path: Path) -> None:
    repo_dir = tmp_path / "example_repo"
    repo_dir.mkdir()
    (repo_dir / "README.md").write_text("# Example repo\n", encoding="utf-8")
    (repo_dir / "src").mkdir()
    (repo_dir / "src" / "__init__.py").write_text("", encoding="utf-8")
    output_path = repo_dir / "docs" / "PROJECT_DOC.md"

    result = subprocess.run(
        [sys.executable, "-m", "src.doc_sync", str(repo_dir), "--output", str(output_path)],
        cwd=str(Path(__file__).resolve().parents[1]),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output_path.exists()


def test_cli_handles_empty_repo(tmp_path: Path) -> None:
    repo_dir = tmp_path / "empty_repo"
    repo_dir.mkdir()
    output_path = repo_dir / "docs" / "PROJECT_DOC.md"

    result = subprocess.run(
        [sys.executable, "-m", "src.doc_sync", str(repo_dir), "--output", str(output_path)],
        cwd=str(Path(__file__).resolve().parents[1]),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output_path.exists()
    assert "Not Found" in output_path.read_text(encoding="utf-8")
