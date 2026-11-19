---
name: software-development
description: Implement approved Doc-Sync development tasks using the implementation plan, requirements, and architecture. Use when implementing a selected TASK-ID, writing source code, updating tests, or validating implementation changes.
---

# Software Development

## Purpose

Implement approved Doc-Sync development tasks in accordance with the approved requirements, architecture, and implementation plan.

The Developer Agent defines the role, tools, responsibilities, and decision boundaries.

This skill defines the reusable software development procedure.

The Development Prompt starts the workflow.

## When to Use

Use this skill when:

- An implementation plan has been approved.
- A specific implementation task has been selected.
- Source code needs to be created or modified.
- Existing tests need to be updated.
- New automated tests need to be added.
- Implementation changes need verification.

Do not use this skill to discover requirements, redesign architecture, or create implementation plans.

## Inputs

Use:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`
- Existing source code.
- Existing tests.
- Project configuration and development documentation.

The selected task ID must be supplied by the user or Orchestrator.

If required documents are missing, ask the user before proceeding.

## Workflow

### 1. Verify Development Inputs

1. Locate the implementation plan.
2. Locate the approved requirements.
3. Locate the approved architecture.
4. Review the design review outcome and relevant findings.
5. Identify the selected task.
6. Verify that the task is approved for implementation.

Do not begin implementation if required approvals are missing.

### 2. Analyze the Selected Task

For the selected task, identify:

- Task ID.
- Task title.
- Description.
- Related requirement IDs.
- Architecture component.
- Dependencies.
- Priority.
- Completion criteria.
- Verification approach.
- Current task status.

Do not implement tasks that are blocked or have incomplete dependencies.

### 3. Inspect the Existing Repository

Before modifying files:

1. Inspect the project directory structure.
2. Identify the programming language and framework.
3. Review relevant existing modules.
4. Review dependency and configuration files.
5. Inspect existing tests.
6. Identify reusable utilities and patterns.
7. Identify affected interfaces and integrations.

Prefer existing project conventions over introducing new patterns.

### 4. Prepare an Implementation Approach

Describe:

- Selected task.
- Requirements addressed.
- Architecture component.
- Files expected to change.
- New files required.
- Existing functionality affected.
- Dependencies.
- Testing approach.

Identify any conflict with approved requirements or architecture.

Ask the user for clarification when the task cannot be implemented safely or accurately.

### 5. Implement the Task

1. Implement only the selected task.
2. Follow the approved architecture.
3. Reuse existing components where appropriate.
4. Write modular and maintainable code.
5. Apply project naming and coding conventions.
6. Handle documented errors and failure scenarios.
7. Validate external inputs.
8. Protect secrets and sensitive information.
9. Avoid unnecessary dependencies.
10. Avoid unrelated refactoring.

Do not introduce functionality that is not supported by the selected task.

### 6. Create or Update Tests

Add or update relevant tests.

Consider:

- Positive scenarios.
- Negative scenarios.
- Boundary conditions.
- Invalid inputs.
- Error handling.
- Integration behavior.
- Regression scenarios.

Use the existing test framework and repository conventions.

Ensure tests verify the task's completion criteria.

### 7. Execute Validation

Run applicable checks:

- Unit tests.
- Integration tests.
- API tests.
- UI tests.
- Linting.
- Static analysis.
- Type checking.
- Build checks.

Execute only checks supported by the project.

Record the actual commands and results.

If validation cannot be completed, document the limitation.

### 8. Review Implementation Scope

Verify:

- Only intended files were modified.
- Changes match the selected task.
- Requirements remain unchanged.
- Architecture remains consistent.
- Tests cover relevant behavior.
- No secrets or sensitive information were introduced.
- No unrelated changes were made.

### 9. Map Implementation to Requirements

Maintain:

`Requirement -> Architecture Component -> Implementation Task -> Code Change -> Test`

Identify:

- Requirements addressed.
- Source files implementing the functionality.
- Tests verifying the functionality.
- Completion criteria not yet satisfied.

### 10. Prepare Implementation Report

Present:

1. Task Information.
2. Implementation Summary.
3. Requirements Addressed.
4. Architecture Component.
5. Files Created.
6. Files Modified.
7. Tests Added or Updated.
8. Validation Commands.
9. Actual Test Results.
10. Known Limitations.
11. Remaining Issues.
12. Completion Status.
13. Handoff Notes.

Do not claim successful execution without evidence.

### 11. Update Task Status

Update task status in `docs/impl-plan.md` only when:

- The selected task's status needs updating.
- The user or workflow explicitly authorizes that documentation update.
- The completion criteria and verification evidence support the new status.

Use clear statuses:

- Not Started.
- In Progress.
- Blocked.
- Completed.

Do not mark a task Completed if its required verification is incomplete.

### 12. Handoff

Provide the implementation summary and evidence to the Code Reviewer or Orchestrator.

Include:

- Task ID.
- Changed files.
- Test results.
- Known limitations.
- Unresolved issues.

Do not automatically start another task.

## Expected Implementation Report

Use these sections:

1. Task Information.
2. Implementation Summary.
3. Requirement Traceability.
4. Architecture Alignment.
5. Files Created.
6. Files Modified.
7. Test Coverage.
8. Validation Results.
9. Known Limitations.
10. Remaining Issues.
11. Completion Status.
12. Handoff Notes.

## Rules and Boundaries

- Implement only the selected approved task.
- Follow approved requirements and architecture.
- Respect task dependencies.
- Do not invent functionality.
- Do not change approved business requirements.
- Do not redesign architecture.
- Do not remove existing tests to hide failures.
- Do not claim unexecuted tests passed.
- Do not commit or push without authorization.
- Do not automatically implement another task.
