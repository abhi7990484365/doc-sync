# Copilot Instructions: doc-sync

## Project
doc-sync is a Python CLI that scans a repository (local path or GitHub API)
and generates/updates `docs/PROJECT_DOC.md`. A GitHub Action re-runs it on push
so documentation never goes stale.

## User story source
- If I give a JIRA issue key or Confluence link, fetch it with the Atlassian MCP
tools. Never write credentials or tokens into any file.

## Tech stack
- Python 3.11, standard library first; add a dependency only when needed
- `pytest` for tests, `pytest-cov` for coverage
- `requests` for GitHub API calls
- `pip-audit` for dependency safety
- Layout: `src/`, `tests/`, `docs/`

## SDLC workflow (follow in order)
1. Requirements  -> docs/requirements.md
2. Architecture  -> docs/architecture.md
3. Design review -> docs/design-review.md
4. Impl. planning -> docs/impl-plan.md
5. Implementation, 6. Review, 7. Verify, 8. PR
- Do not skip steps or write production code before the plan is approved.
- Work on one task from the active implementation plan at a time.
- Always ask for my approval before creating or changing files.
- For direct/manual workflows, use the standard `docs/` artifact paths. If an
  orchestrator supplies a workflow artifact directory, read and write workflow
  documents there instead; do not overwrite the standard docs with that run's
  artifacts.

## Coding rules
- Use type hints and short docstrings on public functions.
- Function names must be self-explanatory; keep functions small (one job each).
- No duplicated logic: put shared code in one helper function.
- Follow PEP 8.

## Missing data rule
- If a field, file, or value cannot be found, write exactly `Not Found`.
- Never guess, invent, or fill in placeholder values.

## Error handling
- Handle API failures, timeouts, rate limits, missing files, and empty repos
  without crashing. Return a clear message and a non-zero exit code.

## Security
- Never print, log, or write secrets, tokens, or passwords to output or docs.
- Read credentials only from environment variables, never hard-code them.
- Validate and sanitise all user input (paths, repo names, URLs).

## Testing
- Every function gets tests for the happy path AND these edge cases:
  Not Found, missing field, empty repo, API failure.
- Run `pytest` after code changes and show me the result.

## Commits and PRs
- Use Conventional Commits (feat:, fix:, docs:, test:, chore:).
- Small, focused commits: one per task.
- Every PR must include: Summary, Changes Made, Test Evidence,
  Known Limitations, and Reviewer Checklist.

## How to talk to me
- Keep answers short and simple.
- Ask when unclear instead of assuming.