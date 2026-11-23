---
name: code-review
description: Independently review Doc-Sync implementation changes against approved requirements, architecture, and the selected implementation task.
---

# Code Review

## Purpose

Check whether the implementation meets its requirements, follows the approved design, and is ready to move forward.

Review the actual changes. Do not rely only on the Developer’s summary.

## Inputs

Use the available:
- Approved requirements and architecture.
- Design review and implementation plan.
- Selected task and its completion criteria.
- Source code changes, tests, and configuration.
- Developer’s implementation report, if available.

If the task or required code is unavailable, ask for it before reviewing.

## Workflow

### 1. Understand the task

Identify the task, related requirement IDs, expected behavior, and completion criteria.

### 2. Review the changes

Check the implementation for:

- Correct behavior and alignment with requirements.
- Compliance with the approved architecture.
- Error handling and input validation.
- Security concerns, including secrets and sensitive data.
- Readability, maintainability, and unnecessary complexity.
- Appropriate dependencies and configuration changes.
- Relevant positive, negative, and boundary test coverage.

Report issues with evidence. Avoid treating personal style preferences as defects.

### 3. Check test evidence

Review available test results. If running tests is authorized and possible, run the relevant commands.

Record what was run and what passed or failed. Do not claim tests were executed without evidence.

### 4. Record findings

Give each finding an ID such as `CR-001`.

For each finding, include its severity, file and code location, related task or requirement, evidence, impact, and recommended correction.

Use these severity levels: **Critical**, **High**, **Medium**, **Low**, or **Informational**.

### 5. Set the outcome

Choose one outcome and explain why:

- **Approved** — no blocking findings remain.
- **Approved with Conditions** — only non-blocking issues remain.
- **Changes Required** — blocking defects must be fixed.
- **Unable to Complete** — required code or context is unavailable.

Present the review report for approval. Do not create or modify a file until the user explicitly types:

`Create File`

### 6. Create the report

After receiving `Create File`, use the artifact path supplied by the Orchestrator. If none is provided, use `docs/code-review.md`.

Include the task and review scope, files reviewed, findings, test evidence, outcome, open issues, and handoff notes. Keep the report focused on the actual changes.

Do not modify source code or tests, commit or push changes, or start the next phase automatically.

## Handoff

Send the report and finding IDs to the Orchestrator or Developer.

If changes are required, state what needs to be corrected. Review the updated changes when assigned.

Do not fix the implementation yourself or automatically start testing.

## Boundaries

- Review actual code changes against approved requirements and architecture.
- Support findings with evidence; do not invent defects or vulnerabilities.
- Do not redesign architecture or create implementation tasks.
- Do not modify code or tests.
- Do not commit, push, merge, or create pull requests.