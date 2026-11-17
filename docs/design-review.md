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

## Agent Orchestrator Design Review

### Summary

The proposed coordinator and sequential named-artifact handoffs cover the
orchestrator requirements while preserving the existing approval gates.
The review identified shared artifact paths and Copilot tool compatibility
as implementation risks.

### Findings

| ID | Severity | Area | Problem | Recommendation | Decision |
| --- | --- | --- | --- | --- | --- |
| DR-AO-01 | High | Artifact retention | Existing prompts target shared `docs/*.md` paths, so later runs could overwrite prior workflow outputs and project documentation. | Use a unique, sanitized directory under `docs/workflows/` per run and pass it to every stage. | Accepted by user; architecture updated. |
| DR-AO-02 | Medium | Copilot compatibility | Existing specialist agent files declare tools such as `editFiles` and `runCommands`, which may not be supported by the Copilot harness. | Update tool declarations to supported Copilot tools while preserving agent responsibilities, then verify in VS Code. | Accepted for architecture and implementation planning. |
| DR-AO-03 | Medium | Approval handling | Specialist review agents are read-only and return review findings in chat; they cannot independently persist user decisions. | The orchestrator must collect user decisions and write review artifacts only after approval. | Covered by the architecture. |

### Requirement Coverage

| Requirement | Architecture support | Status |
| --- | --- | --- |
| FR-15 to FR-17 | User inputs, sequential delegation, and named workflow artifacts | Covered |
| FR-18 to FR-19 | Planner inputs and dependency-ordered, one-task developer loop | Covered |
| FR-20 to FR-21 | Approval checkpoints and ordered review/verification stages | Covered |
| FR-22 to FR-24 | Stop-on-failure checks, tester report, and unique workflow directory | Covered |
| NFR-5 to NFR-7 | Existing agent roles, durable handoffs, and project security rules | Covered |

### Open Items

- Copilot delegation and tool availability must be verified in the target
  VS Code Copilot harness; static frontmatter checks are not sufficient.

## Agent Orchestrator PR Publication Design Review

### Findings

| ID | Severity | Area | Finding | Recommendation | Decision |
| --- | --- | --- | --- | --- | --- |
| DR-AO-04 | High | Git publication | A coordinator that commits and pushes can accidentally publish unrelated work or push directly to the base branch. | Require explicit approval for commit, push, and PR actions; verify the current branch is not the base branch and stop if unapproved changes are present. | Accepted by user; implemented. |
| DR-AO-05 | Medium | PR creation | A rerun may target a branch that already has an open PR, causing duplicate PRs. | Search for an open PR matching the current head and base; update it if found, otherwise create one. Never merge automatically. | Accepted by user; implemented. |
| DR-AO-06 | Medium | PR evidence | A generated PR body could claim tests or list changes not supported by the completed run. | Build the PR description from actual changed files and the successful workflow verification report; stop if the report is missing or verification failed. | Accepted by user; implemented. |

### Decision

The PR stage runs only after successful verification. It keeps the existing
human approval gates, targets `main` by default, updates a matching open PR
when available, and never merges. Copilot/GitHub CLI authentication and
delegation behavior still require runtime validation in the target VS Code
harness.
