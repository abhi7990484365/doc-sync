# Architecture

## 1. Overview

`doc-sync` is a Python command-line application that gathers repository facts,
renders a stable Markdown document, and writes `docs/PROJECT_DOC.md`. A local
repository is read from disk; a GitHub repository is read through the GitHub
REST API. A GitHub Actions workflow runs the local-repository mode on pushes
to `main` and commits the output only when it differs from the checked-in
document.

## 2. Components

### 2.1 CLI and Input Validation

The CLI accepts a local directory or a GitHub repository in `owner/name`
form. It validates the input before scanning. Invalid or missing local paths
and invalid repository identifiers produce a concise error and non-zero exit
status.

### 2.2 Repository Scanners

- The local scanner reads repository files and Git metadata without including
  absolute local paths in output.
- The GitHub scanner uses the GitHub API to obtain repository metadata,
  relevant file contents, a file inventory, and the latest commit. It reads a
  token only from the configured environment variable when present.
- Both scanners provide the renderer with the same normalized repository
  facts so document formatting is independent of the source.

### 2.3 Documentation Renderer and Writer

The renderer maps normalized facts to the seven required sections, in order:
Name, Description, Languages, Dependencies, Entry Points, How to Run, and
Last Commit. It uses `Not Found` for missing values and emits no guessed
metadata, secrets, or absolute local paths. Stable ordering and formatting
make unchanged inputs produce identical output.

The writer creates the `docs` directory when needed and updates
`docs/PROJECT_DOC.md` under the current working directory by default. An
explicit output path can override the default. Writing the same rendered
content twice has no observable content difference.

### 2.4 GitHub Actions

The workflow triggers on pushes to `main`, checks out the repository, sets up
Python 3.11, installs project dependencies, and runs `doc-sync` against the
checked-out repository. It stages and commits `docs/PROJECT_DOC.md` only when
that file has changed. The workflow token is provided through the Actions
environment rather than embedded in source or generated documentation.

## 3. Data Flow

1. The CLI parses and validates the input.
2. The matching scanner gathers source-independent repository facts.
3. The renderer produces the required deterministic Markdown.
4. The writer stores the document under the current working directory by
   default for either input source; an explicit output path can override it.
   The GitHub Action uses local mode on the checked-out repository so the
   result can be committed.
5. On GitHub API failures, the CLI reports a sanitized error and exits
   non-zero rather than writing a success-shaped document.

## 4. Data and Detection Rules

- Description: first non-empty paragraph from a supported README.
- Dependencies: `requirements.txt` only.
- Entry points: recognized common scripts and declared packaging entry points
  from `pyproject.toml` and `setup.cfg`.
- Languages: determined from recognized source-file extensions, with stable
  ordering.
- Last Commit: the latest commit identifier available for the source.
- Missing section values: exactly `Not Found`.
- GitHub input: `owner/name`; credentials are sourced only from an
  environment variable and never included in output or error text.

## 5. Error Handling and Security

- Validate local paths and GitHub repository identifiers before scanning.
- Bound GitHub network requests with timeouts and report HTTP, rate-limit,
  timeout, and response-format failures clearly.
- Do not print request headers, tokens, passwords, or raw response data in
  logs or user-facing errors.
- Do not put absolute local paths in the generated document.
- For a valid but empty local repository, generate all seven sections with
  `Not Found`; distinguish this from an invalid path.

## 6. Quality Attributes

- Determinism: stable section order, sorted detected values, and no
  timestamps or machine-specific paths in output.
- Performance: local scanning should complete in under 10 seconds for a
  repository with fewer than 1,000 files.
- Maintainability: scanners, rendering, writing, and CLI error handling have
  separate responsibilities.
- Testability: scanners and renderer can be tested using temporary
  repositories and mocked GitHub responses without real credentials.

## 7. Requirement Traceability

| Requirement | Architectural support |
| --- | --- |
| FR-1 to FR-2 | CLI validation and local/GitHub scanners |
| FR-3 to FR-8 | Renderer and local scanner |
| FR-9 to FR-10 | CLI validation and bounded GitHub API handling |
| FR-11 to FR-12 | Environment-only credentials and sanitized output |
| FR-13 | Stable scanner facts and deterministic renderer |
| FR-14 | Push workflow with change-conditional commit |
| NFR-1 to NFR-4 | Python 3.11 workflow, efficient scanning, focused tests |
