---
name: code-review
description: Independently review the implementation of a selected Doc-Sync task and create a structured code review report.
agent: code reviewer
---

# Code Review Workflow

## Objective

Independently review implementation changes produced by the Developer Agent.

Evaluate correctness, requirements alignment, architecture compliance, security, code quality, error handling, dependencies, and test coverage.

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

Identify the selected task and verify its approval status.

If required documents are missing, ask the user before proceeding.

## Step 2: Understand Selected Task

Locate the selected task ID in `docs/impl-plan.md`.

Extract:

- Task description.
- Requirement IDs.
- Architecture component.
- Dependencies.
- Completion criteria.
- Verification approach.

Do not review an unspecified task.

## Step 3: Inspect Developer Changes

Inspect:

- New files.
- Modified files.
- Deleted files.
- Source code.
- Test files.
- Dependency changes.
- Configuration changes.
- Developer implementation report, if available.

Review actual changes rather than relying only on the implementation summary.

## Step 4: Review Functional Correctness

Evaluate:

- Expected behavior.
- Business logic.
- Requirement alignment.
- Acceptance criteria.
- Positive scenarios.
- Negative scenarios.
- Boundary conditions.
- Invalid inputs.
- Error handling.

Identify defects with supporting evidence.

## Step 5: Review Architecture Compliance

Verify:

- Component responsibilities.
- Interfaces.
- Data flows.
- Dependency direction.
- Integration patterns.
- Technology choices.
- Security boundaries.

Identify implementation decisions that conflict with the approved architecture.

## Step 6: Review Code Quality

Evaluate:

- Readability.
- Naming conventions.
- Modularity.
- Separation of concerns.
- Reusability.
- Duplication.
- Complexity.
- Maintainability.

Do not report subjective preferences as defects.

## Step 7: Review Security and Reliability

Check:

- Hardcoded secrets.
- Authentication and authorization.
- Input validation.
- Sensitive information exposure.
- Unsafe logging.
- Secure communication.
- Injection risks.
- File access and path handling.
- Error handling.
- External dependency failures.
- Dependency risks.

Report only evidence-supported issues.

## Step 8: Review Test Coverage

Evaluate:

- Positive test scenarios.
- Negative test scenarios.
- Boundary conditions.
- Error handling.
- Regression coverage.
- Assertions.
- Test isolation.
- Alignment with task completion criteria.

Do not treat test existence as proof of correctness.

## Step 9: Verify Validation Evidence

Review available test execution evidence.

If execution is possible and authorized, run relevant checks.

Record:

- Command executed.
- Passed tests.
- Failed tests.
- Skipped tests.
- Execution limitations.

Do not claim successful execution without evidence.

## Step 10: Record Review Findings

Create finding IDs:

- `CR-001`
- `CR-002`
- `CR-003`

For each finding, include:

- Finding ID.
- Severity.
- Finding type.
- File path.
- Relevant code location.
- Related task ID.
- Related requirement IDs.
- Description.
- Evidence.
- Impact.
- Recommended correction.

Use these severity levels:

- Critical.
- High.
- Medium.
- Low.
- Informational.

## Step 11: Determine Review Outcome

Choose one:

- **Approved:** No unresolved critical or high-severity findings remain, and completion criteria are satisfied.
- **Approved with Conditions:** No unresolved critical findings remain, but non-blocking conditions remain.
- **Changes Required:** Critical or high-severity findings prevent acceptance.
- **Unable to Complete:** Required source code or review evidence is unavailable.

Explain the selected outcome.

## Step 12: Prepare Code Review Report

Prepare the complete `docs/code-review.md` content.

Use these sections:

1. Document Information.
2. Review Scope.
3. Source Documents.
4. Selected Task Information.
5. Implementation Summary.
6. Files Reviewed.
7. Functional Review.
8. Architecture Compliance Review.
9. Code Quality Review.
10. Error Handling Review.
11. Security Review.
12. Dependency Review.
13. Test Coverage Review.
14. Validation Evidence.
15. Code Review Findings.
16. Review Outcome.
17. Recommendations.
18. Open Issues.
19. Handoff Notes.

Present the complete report to the user.

Do not create the file yet.

## Step 13: Obtain Explicit Approval

Create or modify the review report only after the user explicitly types:

`Create File`

General confirmations such as "looks good" or "continue" do not authorize file creation.

## Step 14: Create Review Document

After receiving `Create File`:

1. Use the supplied workflow artifact directory.
2. Otherwise use `docs/code-review.md`.
3. Preserve requirement and task traceability.
4. Include evidence for every significant finding.
5. Record actual validation results.
6. Clearly state the review outcome.
7. Do not modify source code.
8. Do not modify tests.
9. Do not modify unrelated files.
10. Do not commit or push changes.

## Step 15: Report Completion

Report:

- Created file path.
- Selected task ID.
- Review outcome.
- Finding count by severity.
- Critical and high-severity findings.
- Required corrections.
- Open issues.
- Recommended next action.

If changes are required, hand findings to the Developer.

If review is acceptable, hand off to the Tester Agent or Orchestrator.

Do not automatically start testing.

## Boundaries

- Do not modify implementation code.
- Do not modify tests during review.
- Do not change approved requirements.
- Do not redesign architecture.
- Do not invent defects or vulnerabilities.
- Do not create implementation tasks.
- Do not commit, push, merge, or create pull requests.
- Do not automatically start testing.
