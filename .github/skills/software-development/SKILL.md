---
name: software-development
description: Implement approved Doc-Sync development tasks using the implementation plan, requirements, and architecture. Use when implementing a selected TASK-ID, writing source code, updating tests, or validating implementation changes.
---

# Software Development

## Purpose

Implement one approved task using the approved requirements, architecture, and implementation plan.

The Developer Agent defines the role and decision boundaries. This skill defines the development procedure. The Development Prompt starts the workflow.

## When to Use

Use when a specific task is selected for implementation.

Do not use this skill to discover requirements, redesign architecture, or create an implementation plan.

## Inputs

Use:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`
- Relevant source code, tests, and project documentation

The user or Orchestrator must provide the selected task ID. If required artifacts or approvals are missing, ask before proceeding.

## Workflow

### 1. Verify the Task

Review the selected task, its requirements, architecture component, dependencies, completion criteria, verification approach, and status.

Do not proceed if the task is unapproved, blocked, or has incomplete dependencies. Raise conflicts or unclear requirements before implementation.

### 2. Inspect the Repository

Review the project structure, relevant code and tests, configuration, dependencies, and existing conventions.

Identify the files and interfaces likely to be affected. Prefer existing patterns and reusable components.

### 3. Plan the Change

Briefly identify the task, requirements addressed, expected file changes, affected functionality, and testing approach.

Ask for clarification if the task cannot be implemented safely or accurately within the approved design.

### 4. Implement

- Implement only the selected task.
- Follow the approved requirements and architecture.
- Keep changes modular and consistent with project conventions.
- Handle relevant errors and invalid inputs.
- Protect secrets and sensitive information.
- Avoid unnecessary dependencies and unrelated refactoring.

Do not add unsupported functionality or change approved requirements.

### 5. Add or Update Tests

Use the existing test framework and conventions. Cover relevant positive, negative, boundary, error-handling, integration, and regression scenarios.

Tests must verify the task’s completion criteria.

### 6. Run Validation

Run applicable project checks, such as tests, linting, static analysis, type checks, or builds.

Record the actual commands and results. If a check cannot be run, state why. Never claim that unexecuted checks passed.

### 7. Review Scope and Traceability

Confirm that:

- Changes match the selected task.
- Only intended files were modified.
- Requirements and architecture remain unchanged and aligned.
- Relevant tests cover the completion criteria.
- No secrets or unrelated changes were introduced.

Trace the work as:

`Requirement → Architecture Component → Task → Code Change → Test`

Identify any unmet completion criteria.

### 8. Report and Hand Off

Provide:

- Task ID and completion status
- Implementation summary and requirement traceability
- Files created or modified
- Tests added or updated
- Validation commands and actual results
- Known limitations and unresolved issues

Hand the evidence to the Code Reviewer or Orchestrator. Do not automatically start another task.

## Task Status

Update `docs/impl-plan.md` only when the user or workflow authorizes the update and the evidence supports it.

Use these statuses:

- Not Started
- In Progress
- Blocked
- Completed

Do not mark a task Completed while required verification is incomplete.

## Rules and Boundaries

- Implement only the selected approved task.
- Respect task dependencies and approved design.
- Do not invent functionality, redesign architecture, or change business requirements.
- Do not remove tests to hide failures.
- Do not claim unverified results.
- Do not commit or push without authorization.
- Do not automatically implement another task.