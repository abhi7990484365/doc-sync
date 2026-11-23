---
name: development
description: Implement one selected approved Doc-Sync task from docs/impl-plan.md, including source code, tests, and validation.
agent: developer
---

# Development Workflow

## Objective

Implement one explicitly selected Doc-Sync implementation task according to approved requirements, architecture, and implementation plan.

Selected task:

`${input:taskId:Enter the implementation task ID, for example TASK-001}`

Workflow artifact directory:

`${input:workflowDir:docs}`

## Step 1: Verify Source Documents

Read:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`

Verify that:

1. Requirements are approved.
2. Architecture is approved for implementation.
3. Design review findings have been considered.
4. The implementation plan exists.
5. The selected task exists.

If a required document is missing or approval is unclear, ask the user before proceeding.

## Step 2: Verify Selected Task

Locate the supplied task ID in `docs/impl-plan.md`.

Extract:

- Task ID.
- Task title.
- Description.
- Related requirement IDs.
- Architecture component.
- Dependencies.
- Priority.
- Completion criteria.
- Verification approach.
- Current status.

If the task does not exist, ask the user to select a valid task.

If the task is blocked or its dependencies are incomplete, explain why and stop.

Do not implement another task automatically.

## Step 3: Inspect the Repository

Inspect:

- Repository structure.
- Relevant source files.
- Existing tests.
- Dependency files.
- Configuration files.
- Reusable utilities.
- Existing coding conventions.

Identify the files affected by the selected task.

Do not assume technologies that are not established by the approved architecture or repository.

## Step 4: Prepare Implementation Approach

Present:

- Selected task ID.
- Requirements addressed.
- Architecture component.
- Dependencies.
- Expected files to create.
- Expected files to modify.
- Implementation approach.
- Testing and verification approach.

If the task conflicts with approved requirements or architecture, stop and request clarification.

## Step 5: Implement the Task

Implement only the selected task.

Requirements:

1. Follow the approved architecture.
2. Follow existing coding conventions.
3. Reuse appropriate existing components.
4. Write maintainable and modular code.
5. Handle expected errors.
6. Validate external inputs.
7. Protect sensitive information.
8. Avoid unnecessary dependencies.
9. Avoid unrelated refactoring.
10. Do not introduce unapproved functionality.

## Step 6: Add or Update Tests

Add or update relevant tests.

Consider:

- Positive scenarios.
- Negative scenarios.
- Boundary scenarios.
- Invalid inputs.
- Error handling.
- Integration behavior.
- Regression scenarios.

Use the repository's existing testing framework.

## Step 7: Execute Validation

Run applicable:

- Unit tests.
- Integration tests.
- API tests.
- UI tests.
- Linting.
- Static analysis.
- Type checks.
- Build checks.

Record:

- Command executed.
- Actual result.
- Passed tests.
- Failed tests.
- Skipped tests.
- Execution limitations.

Never claim a test passed unless it was actually executed successfully.

## Step 8: Verify Scope and Traceability

Verify:

- Changes match the selected task.
- Requirements are addressed.
- Architecture remains consistent.
- Only intended files were modified.
- Tests cover relevant behavior.
- Completion criteria are satisfied.
- No secrets were introduced.
- No unrelated changes were made.

Maintain:

`Requirement -> Architecture Component -> Implementation Task -> Code Change -> Test`

## Step 9: Prepare Implementation Report

Prepare a report with:

1. Task Information.
2. Implementation Summary.
3. Requirement Traceability.
4. Architecture Alignment.
5. Files Created.
6. Files Modified.
7. Tests Added or Updated.
8. Validation Commands.
9. Actual Validation Results.
10. Known Limitations.
11. Remaining Issues.
12. Completion Status.
13. Handoff Notes.

Do not mark the task Completed if its completion criteria are not verified.

## Step 10: Obtain Approval for Documentation Updates

If `docs/impl-plan.md` needs a task status update, present the proposed change.

Do not modify the implementation plan unless the user or Orchestrator explicitly authorizes the update.

Use these task statuses:

- Not Started.
- In Progress.
- Blocked.
- Completed.

## Step 11: Report Completion

Report:

- Selected task ID.
- Files created.
- Files modified.
- Implementation summary.
- Tests executed.
- Actual test results.
- Known limitations.
- Remaining issues.
- Completion status.

Hand off implementation evidence to the Code Reviewer or Orchestrator.

Do not automatically start another task.

## Boundaries

- Implement only the selected task.
- Do not modify approved requirements.
- Do not redesign architecture.
- Do not implement unapproved features.
- Do not change unrelated files.
- Do not remove tests to hide failures.
- Do not claim unexecuted tests passed.
- Do not commit, push, merge, or create pull requests without authorization.
- Do not automatically start another task.
