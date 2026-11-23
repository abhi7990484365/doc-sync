# Copilot Instructions: doc-sync

## User Story Source
- If I provide a Jira issue key or Confluence link, retrieve it using the Atlassian MCP tools.
- Never write credentials or tokens into any file.

## Tech Stack
- Python 3.11; prefer the standard library and add dependencies only when needed.
- `pytest` for tests and `pytest-cov` for coverage.
- `requests` for GitHub API calls.
- `pip-audit` for dependency safety.
- Project layout: `src/`, `tests/`, `docs/`.

## SDLC Workflow
Follow these steps in order:
1. Requirements 
2. Architecture 
3. Design review 
4. Implementation planning
5. Implementation
6. Code review
7. Verification
8. Pull request

- Do not skip steps or write production code before the implementation plan is approved.
- Work on one task from the active implementation plan at a time.
- Ask for my approval before creating or changing files.
- For direct/manual workflows, use the standard `docs/` artifact paths.
- If the orchestrator supplies a workflow artifact directory, use it for that run. Do not overwrite standard `docs/` artifacts with workflow-specific outputs.
- Keep workflow progress and decisions in `docs/sdlc-state.md` or the state file designated by the orchestrator.

## Instructions, Skills, and Rules
- Follow shared and folder-specific instructions that apply to the files being changed.
- Use an agent's skills for relevant task procedures; do not duplicate entire skills in the main instructions.
- Treat rules as constraints that must be followed, including security, scope, and approval requirements.
- Keep instructions and handoffs concise. Avoid repeating the same guidance across agents, instructions, skills, and rules.

## Context and Artifact Management
- Use source documents as evidence; do not pass entire documents to the next agent when only selected information is needed.
- Extract relevant requirements, business rules, constraints, dependencies, risks, and open questions. Exclude unrelated or duplicate content while preserving source references.
- Give each requirement and workflow run a stable ID when applicable.
- Keep artifacts for separate requirements or runs in separate folders or clearly identified files. Never silently overwrite existing artifacts.
- Before updating an existing artifact, identify it and obtain approval. Make clear whether the action creates a new artifact or updates an existing one.
- Handoffs must identify the source requirement, artifact path, status, unresolved questions, and next action.
- Treat approved project artifacts and state files as the source of truth, not chat history.

## Coding Rules
- Use type hints and short docstrings on public functions.
- Use self-explanatory function names and keep functions small, with one clear responsibility each.
- Avoid duplicated logic; put shared behavior in a helper.
- Follow PEP 8.

## Missing Data
- If a required field, file, or value cannot be found, write exactly `Not Found`.
- Never guess, invent, or fill in placeholder values.
- Clearly distinguish confirmed facts, assumptions, and unresolved questions.

## Error Handling and Recovery
- Handle API failures, timeouts, rate limits, missing files, and empty repositories without crashing.
- Return a clear error message and a non-zero exit code when a command fails.
- Define retry limits for transient failures; do not repeatedly retry errors that require a code change or user decision.
- Record the failed stage, error, and completed work in the workflow state.
- On resume, inspect the state, artifacts, and Git status. Continue from the last incomplete stage and avoid repeating completed work.
- If the state is missing or ambiguous, ask rather than guess.

## Security
- Never print, log, or write secrets, tokens, or passwords to output or documentation.
- Read credentials only from environment variables; never hard-code them.
- Validate and sanitize user input, including paths, repository names, and URLs.
- Do not include secrets, sensitive `.env` files, or unrelated user changes in commits or PRs.

## Testing
- Add tests for happy paths and relevant edge cases, including missing data, empty repositories, and API failures.
- Run `pytest` after code changes and report the actual result.
- Do not invent test evidence or modify tests to hide failures.
- Record failed, blocked, and skipped tests with reasons.

## Hooks
- Keep hook configuration separate from agent instructions and skills.
- Use hooks for event-triggered checks or guardrails; do not rely on hooks alone for workflow retries or resume behavior.
- Use repository branch protection or rulesets to enforce GitHub branch restrictions. Agent instructions and local hooks are additional safeguards, not substitutes for repository enforcement.

## Commits and Pull Requests
- Use Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, or `chore:`.
- Keep commits small and focused, preferably one per task.
- Never push directly to the default branch or force-push.
- Every PR must include:
  - Summary
  - Changes Made
  - Test Evidence
  - Known Limitations
  - Reviewer Checklist
- Prefix PR titles with `[AI generated]`.
- Apply the `AI generated` label if it already exists. Do not create it automatically; report if it is unavailable.
- Verify the PR URL, source and target branches, title, body, and label status after creation.

## How to Talk to Me
- Keep answers short and simple.
- Ask when unclear instead of assuming.
- Report what was actually completed, what failed, and what needs my approval.