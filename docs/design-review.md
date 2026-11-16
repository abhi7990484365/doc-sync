# Design Review

## Summary

The proposed separation between CLI validation, local/GitHub scanners,
deterministic rendering, and writing fits the approved requirements while
keeping the implementation small. The current repository already has a
local scanner and renderer, but it does not yet support `owner/name` input or
the requested push-to-main documentation workflow.

## Findings

| ID | Severity | Area | Finding | Recommendation |
| --- | --- | --- | --- | --- |
| DR-01 | High | GitHub CLI output | A remote `owner/name` source has no local repository directory, so the default destination for `docs/PROJECT_DOC.md` was undefined. | Resolved: GitHub mode writes to `docs/PROJECT_DOC.md` under the current working directory unless an output path is supplied. |
| DR-02 | Medium | GitHub API | Repository contents, metadata, and commit information may require multiple API requests and encounter rate limits or partial failures. | Apply request timeouts, validate API responses, handle rate-limit and HTTP errors explicitly, and avoid returning partially fabricated documents on API failure. |
| DR-03 | Medium | Secret handling | README text and dependency values are user-controlled and could contain credential-like strings. | Sanitize recognized secrets before rendering and never include raw API response bodies, headers, or exception text in logs/errors. Add regression tests using representative secret patterns. |
| DR-04 | Medium | Local scanning | Recursive scans can include generated directories such as `.git`, virtual environments, and caches, affecting speed and language detection. | Skip common generated/dependency directories while continuing to scan normal project source. |
| DR-05 | Low | GitHub Action | A workflow-generated commit may trigger the push workflow again. | Use a skip marker or verify the second run is a no-op; commit only when the generated file changes. |

## Requirement Coverage

| Requirement | Design area | Status |
| --- | --- | --- |
| FR-1 to FR-3 | CLI, scanners, renderer | Covered |
| FR-4 to FR-8 | README/dependency/entry-point detection and missing-data rules | Covered; secret filtering needs tests |
| FR-9 to FR-10 | Input validation and GitHub API handling | Covered in principle; DR-02 |
| FR-11 to FR-12 | Environment-only token and sanitized output | Covered in principle; DR-03 |
| FR-13 | Deterministic output | Covered |
| FR-14 | Push workflow | Covered in principle; DR-05 |
| NFR-1 to NFR-4 | Python 3.11, scan efficiency, automated testing | Covered in principle; DR-04 |

## Decision

For GitHub `owner/name` input, write the generated document to
`docs/PROJECT_DOC.md` under the current working directory unless an explicit
output path is supplied. This decision is recorded in the requirements and
architecture.
