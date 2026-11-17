import base64
import os
import subprocess
import sys
from pathlib import Path

import pytest
import requests

from src.doc_sync.generator import (
    GitHubAPIError,
    detect_dependencies,
    detect_languages,
    determine_how_to_run,
    discover_entry_points,
    fetch_github_repo_metadata,
    generate_github_project_doc,
    generate_project_doc,
    get_last_commit,
    main,
    read_repo_description,
    render_project_doc,
)


class StubResponse:
    def __init__(self, status_code: int, payload: object, headers=None) -> None:
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}

    def json(self) -> object:
        return self._payload


def _mock_github_success(monkeypatch, token: str = "test-token") -> list[dict]:
    readme = base64.b64encode(b"# Demo\n\nA remote example.\n").decode("ascii")
    dependencies = base64.b64encode(b"requests==2.32.3\n").decode("ascii")
    observed_headers: list[dict] = []

    def get(url: str, **kwargs):
        observed_headers.append(kwargs["headers"])
        if url.endswith("/repos/acme/demo"):
            return StubResponse(
                200,
                {
                    "full_name": "acme/demo",
                    "name": "demo",
                    "default_branch": "main",
                },
            )
        if "/git/trees/main?recursive=1" in url:
            return StubResponse(
                200,
                {
                    "truncated": False,
                    "tree": [
                        {"path": "README.md", "type": "blob", "sha": "readme"},
                        {
                            "path": "requirements.txt",
                            "type": "blob",
                            "sha": "requirements",
                        },
                        {"path": "main.py", "type": "blob", "sha": "main"},
                        {
                            "path": "docs/PROJECT_DOC.md",
                            "type": "blob",
                            "sha": "generated",
                        },
                    ],
                },
            )
        if url.endswith("/git/blobs/readme"):
            return StubResponse(200, {"encoding": "base64", "content": readme})
        if url.endswith("/git/blobs/requirements"):
            return StubResponse(
                200, {"encoding": "base64", "content": dependencies}
            )
        if url.endswith("/commits/main"):
            return StubResponse(200, {"sha": "1234567890abcdef"})
        raise AssertionError(f"Unexpected GitHub API URL: {url}")

    monkeypatch.setenv("GITHUB_TOKEN", token)
    monkeypatch.setattr(requests, "get", get)
    return observed_headers


def test_read_repo_description_happy_path(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Example service\n\nA sample app.\n", encoding="utf-8")

    assert read_repo_description(tmp_path) == "A sample app."


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


def test_detect_dependencies_ignores_other_manifests(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\ndependencies = ["requests"]\n', encoding="utf-8"
    )

    assert detect_dependencies(tmp_path) == "Not Found"


def test_detect_entry_points_combines_common_and_declared_scripts(
    tmp_path: Path,
) -> None:
    (tmp_path / "main.py").write_text("print('hello')\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        '[project.scripts]\nexample = "example.cli:main"\n', encoding="utf-8"
    )

    assert discover_entry_points(tmp_path) == (
        "python main.py, example: example.cli:main"
    )


def test_detect_entry_points_reads_setup_cfg_scripts(tmp_path: Path) -> None:
    (tmp_path / "setup.cfg").write_text(
        "[options.entry_points]\n"
        "console_scripts =\n"
        "    example = example.cli:main\n",
        encoding="utf-8",
    )

    assert discover_entry_points(tmp_path) == "example: example.cli:main"
    assert determine_how_to_run(tmp_path) == "example"


def test_detect_languages_ignores_generated_directories(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("", encoding="utf-8")
    virtualenv = tmp_path / ".venv" / "Lib"
    virtualenv.mkdir(parents=True)
    (virtualenv / "installed.js").write_text("", encoding="utf-8")

    assert detect_languages(tmp_path) == "Python"


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

    with pytest.raises(GitHubAPIError, match="GitHub API request failed"):
        fetch_github_repo_metadata("https://github.com/example/repo")


def test_github_generation_reads_repository_and_writes_to_cwd(
    tmp_path: Path, monkeypatch
) -> None:
    headers = _mock_github_success(monkeypatch)
    monkeypatch.chdir(tmp_path)

    generated = generate_github_project_doc("acme/demo")

    written = (tmp_path / "docs" / "PROJECT_DOC.md").read_text(encoding="utf-8")
    assert written == generated
    assert "A remote example." in generated
    assert "Python" in generated
    assert "requests==2.32.3" in generated
    assert "python main.py" in generated
    assert "1234567" in generated
    assert all(header["Authorization"] == "Bearer test-token" for header in headers)
    assert "test-token" not in generated


def test_github_generation_supports_explicit_output_path(
    tmp_path: Path, monkeypatch
) -> None:
    _mock_github_success(monkeypatch)
    output_path = tmp_path / "custom" / "PROJECT_DOC.md"

    generated = generate_github_project_doc("acme/demo", output_path)

    assert output_path.read_text(encoding="utf-8") == generated


def test_github_empty_repository_has_all_not_found(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    def get(url: str, **kwargs):
        return StubResponse(200, {"full_name": "acme/empty", "default_branch": None})

    monkeypatch.setattr(requests, "get", get)
    generated = generate_github_project_doc("acme/empty")

    assert [section.splitlines()[1] for section in generated.strip().split("\n\n")] == [
        "Not Found"
    ] * 7


def test_github_rate_limit_is_reported_without_response_details(monkeypatch) -> None:
    monkeypatch.setattr(
        requests,
        "get",
        lambda *args, **kwargs: StubResponse(
            403,
            {"message": "API rate limit exceeded: secret-token"},
            {"X-RateLimit-Remaining": "0"},
        ),
    )

    with pytest.raises(GitHubAPIError, match="rate limit exceeded") as error:
        generate_github_project_doc("acme/demo")

    assert "secret-token" not in str(error.value)


def test_github_timeout_is_reported_clearly(monkeypatch) -> None:
    def timeout(*args, **kwargs):
        raise requests.Timeout("sensitive request detail")

    monkeypatch.setattr(requests, "get", timeout)

    with pytest.raises(GitHubAPIError, match="request timed out") as error:
        generate_github_project_doc("acme/demo")

    assert "sensitive request detail" not in str(error.value)


def test_github_missing_repository_is_reported(monkeypatch) -> None:
    monkeypatch.setattr(
        requests, "get", lambda *args, **kwargs: StubResponse(404, {})
    )

    with pytest.raises(GitHubAPIError, match="GitHub repository not found"):
        generate_github_project_doc("acme/missing")


def test_cli_reports_github_failure_with_nonzero_exit(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.chdir(tmp_path)

    def timeout(*args, **kwargs):
        raise requests.Timeout("secret request details")

    monkeypatch.setattr(requests, "get", timeout)
    result = main(["acme/demo"])
    captured = capsys.readouterr()

    assert result != 0
    assert "GitHub API request timed out" in captured.err
    assert "secret request details" not in captured.err


def test_github_rejects_malformed_repository_response(monkeypatch) -> None:
    monkeypatch.setattr(
        requests, "get", lambda *args, **kwargs: StubResponse(200, [])
    )

    with pytest.raises(GitHubAPIError, match="invalid repository response"):
        generate_github_project_doc("acme/demo")


def test_github_rejects_missing_default_branch_field(monkeypatch) -> None:
    monkeypatch.setattr(
        requests,
        "get",
        lambda *args, **kwargs: StubResponse(200, {"full_name": "acme/demo"}),
    )

    with pytest.raises(GitHubAPIError, match="invalid repository response"):
        generate_github_project_doc("acme/demo")


def test_github_rejects_invalid_repository_identifier(monkeypatch) -> None:
    def fail_if_called(*args, **kwargs):
        raise AssertionError("Invalid repository must not cause an API request")

    monkeypatch.setattr(requests, "get", fail_if_called)

    with pytest.raises(ValueError, match="owner/name"):
        generate_github_project_doc("../acme/demo")


def test_render_project_doc_has_required_sections_in_order(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "# Example repo\n\nAn example project.\n", encoding="utf-8"
    )
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

    assert "An example project." in document
    assert "requests" in document
    assert "Python" in document


def test_render_project_doc_uses_directory_name_for_relative_path(
    tmp_path: Path, monkeypatch
) -> None:
    (tmp_path / "README.md").write_text("A project.\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    document = render_project_doc(".")

    assert f"Name\n{tmp_path.name}" in document


def test_local_acceptance_fixture_populates_all_sections(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "# Sample project\n\nA complete local example.\n", encoding="utf-8"
    )
    (tmp_path / "requirements.txt").write_text(
        "requests==2.32.3\n", encoding="utf-8"
    )
    (tmp_path / "main.py").write_text("print('hello')\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.name", "Tester"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "config", "user.email", "tester@example.com"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "add", "README.md", "requirements.txt", "main.py"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=tmp_path,
        check=True,
        stdout=subprocess.DEVNULL,
    )

    document = generate_project_doc(tmp_path)
    values = {
        section.splitlines()[0]: section.splitlines()[1]
        for section in document.strip().split("\n\n")
    }

    assert values == {
        "Name": tmp_path.name,
        "Description": "A complete local example.",
        "Languages": "Python",
        "Dependencies": "requests==2.32.3",
        "Entry Points": "python main.py",
        "How to Run": "python main.py",
        "Last Commit": get_last_commit(tmp_path),
    }
    assert all(value != "Not Found" for value in values.values())


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


def test_generated_document_redacts_credentials_and_absolute_paths(
    tmp_path: Path,
) -> None:
    (tmp_path / "README.md").write_text(
        "A project stored at C:\\Users\\private user\\source.\n\n"
        "API_TOKEN=ghp_123456789012345678901234\n",
        encoding="utf-8",
    )
    (tmp_path / "requirements.txt").write_text(
        "https://user:password@example.com/package\n"
        "https://url-secret@example.com/package\n"
        "API_TOKEN=top-secret-value\n"
        "AWS_SECRET_ACCESS_KEY=aws-sensitive-value\n"
        "-e /home/private user/package\n",
        encoding="utf-8",
    )

    generated = render_project_doc(tmp_path)

    assert "C:\\Users\\private" not in generated
    assert "private user\\source" not in generated
    assert "/home/private" not in generated
    assert "user:password" not in generated
    assert "url-secret" not in generated
    assert "top-secret-value" not in generated
    assert "aws-sensitive-value" not in generated


def test_empty_repository_has_not_found_for_every_section(tmp_path: Path) -> None:
    document = render_project_doc(tmp_path)

    assert [section.splitlines()[1] for section in document.strip().split("\n\n")] == [
        "Not Found"
    ] * 7


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
    first_document = output_path.read_text(encoding="utf-8")
    assert [section.splitlines()[1] for section in first_document.strip().split("\n\n")] == [
        "Not Found"
    ] * 7

    second_result = subprocess.run(
        [sys.executable, "-m", "src.doc_sync", str(repo_dir), "--output", str(output_path)],
        cwd=str(Path(__file__).resolve().parents[1]),
        capture_output=True,
        text=True,
        check=False,
    )
    assert second_result.returncode == 0, second_result.stderr
    assert output_path.read_text(encoding="utf-8") == first_document


def test_cli_rejects_missing_path_without_exposing_it(tmp_path: Path) -> None:
    missing_path = tmp_path / "private" / "missing"
    result = subprocess.run(
        [sys.executable, "-m", "src.doc_sync", str(missing_path)],
        cwd=str(Path(__file__).resolve().parents[1]),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "repository path does not exist" in result.stderr
    assert str(tmp_path) not in result.stderr
