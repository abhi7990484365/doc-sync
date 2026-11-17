# Changelog

## [Unreleased] - 2026-11-16

### Added
- A CLI that generates `docs/PROJECT_DOC.md` from local or GitHub repositories.
- A GitHub Actions workflow that syncs generated documentation after pushes to `main`.
- Automated local and mocked GitHub scanner, rendering, and failure-case tests.

### Changed
- Documented supported usage, architecture, requirements, implementation, review, and verification for the repository-documentation generator.
- Added `httpx` for the FastAPI TestClient test dependency.

### Fixed
- Added handling for invalid inputs and GitHub API failures, deterministic missing-value output, and recognized-secret/path sanitization.
