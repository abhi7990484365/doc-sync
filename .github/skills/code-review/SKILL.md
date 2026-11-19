---
name: code-review
description: Independently review Doc-Sync implementation changes against approved requirements, architecture, and implementation tasks. Identify defects, security risks, code quality issues, and test coverage gaps. Use when reviewing Developer changes and preparing docs/code-review.md.
---

# Code Review

## Purpose

Provide an independent quality review of Doc-Sync implementation changes.

The Code Reviewer evaluates whether the implementation:

- Satisfies the selected task.
- Meets approved requirements.
- Follows the architecture.
- Handles expected errors.
- Applies appropriate security controls.
- Has sufficient automated test coverage.
- Is maintainable and readable.
- Avoids unnecessary dependencies and unrelated changes.

The Code Reviewer Agent defines the role, tools, responsibilities, and decision boundaries.

This skill defines the reusable code review procedure.

The Code Review Prompt starts the workflow.

## When to Use

Use this skill when:

- The Developer has completed an implementation task.
- Code changes need independent review.
- Security and error-handling practices need evaluation.
- Test coverage needs assessment.
- Implementation needs verification against approved requirements.
- A formal code review report needs creation.

Do not use this skill to implement features, redesign architecture, or execute the complete testing phase.

## Inputs

Use:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`
- Developer implementation report, if available.
- Actual source code changes.
- Existing tests.
- Dependency and configuration files.

If required source code or context is unavailable, ask the user before proceeding.

## Workflow

### 1. Verify Review Inputs

1. Locate approved requirements.
2. Locate approved architecture.
3. Locate the implementation plan.
4. Identify the selected task.
5. Locate the Developer's changes.
6. Review the implementation report, if available.
7. Identify relevant tests and project configuration.

Do not review an unspecified implementation task.

### 2. Understand the Selected Task

Identify:

- Task ID.
- Task description.
- Related requirement IDs.
- Architecture component.
- Dependencies.
- Completion criteria.
- Verification approach.

Use the implementation plan as the task baseline.

### 3. Inspect Code Changes

Inspect:

- New files.
- Modified files.
- Deleted files.
- Changed functions and classes.
- Configuration changes.
- Dependency changes.
- Test changes.

Understand the implementation before evaluating it.

Do not assume the Developer's summary fully represents the actual changes.

### 4. Review Functional Correctness

Evaluate:

- Expected behavior.
- Business logic.
- Requirement alignment.
- Acceptance criteria.
- Edge cases.
- Invalid inputs.
- Error scenarios.
- Unexpected state handling.

Identify defects that can cause incorrect or incomplete behavior.

### 5. Review Architecture Compliance

Verify:

- Component responsibilities.
- Interfaces.
- Data flows.
- Dependency direction.
- Integration patterns.
- Approved technology choices.
- Security boundaries.

Identify implementation decisions that conflict with the approved architecture.

Do not independently redesign the architecture.

### 6. Review Code Quality

Evaluate:

- Readability.
- Naming conventions.
- Modularity.
- Separation of concerns.
- Reusability.
- Duplication.
- Complexity.
- Maintainability.
- Appropriate abstractions.

Avoid treating personal style preferences as defects.

### 7. Review Error Handling

Check:

- Exception handling.
- Invalid input handling.
- External dependency failures.
- Timeouts.
- Retry behavior, where required.
- Logging.
- Recovery behavior.
- User-facing or API error responses, where applicable.

Verify that errors are not silently swallowed.

### 8. Review Security

Check:

- Hardcoded secrets.
- Authentication and authorization.
- Input validation.
- Sensitive data handling.
- Unsafe logging.
- Secure communication.
- Injection risks.
- File access and path handling.
- Dependency security.
- Permission boundaries.

Report only evidence-supported findings.

### 9. Review Dependencies

Evaluate:

- New dependency necessity.
- Version constraints.
- Compatibility.
- Maintenance status, where verifiable.
- Security concerns.
- Unnecessary packages.

Do not invent vulnerability claims.

### 10. Review Tests

Evaluate:

- Test relevance.
- Positive scenarios.
- Negative scenarios.
- Boundary conditions.
- Error handling.
- Regression coverage.
- Assertions.
- Test isolation.
- Test readability.

Compare tests with task completion criteria.

Do not treat the existence of tests as proof of correctness.

### 11. Verify Test Evidence

Review actual execution evidence where available.

If execution is possible and authorized, run relevant existing test commands.

Record:

- Command.
- Result.
- Passed tests.
- Failed tests.
- Skipped tests.
- Execution limitations.

Never claim successful execution without evidence.

### 12. Identify and Classify Findings

Assign sequential IDs:

- `CR-001`
- `CR-002`
- `CR-003`

For every finding, include:

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

Use severity levels:

- Critical.
- High.
- Medium.
- Low.
- Informational.

### 13. Evaluate Review Outcome

Choose one:

**Approved**

No unresolved critical or high-severity findings remain, and the implementation satisfies its completion criteria.

**Approved with Conditions**

No unresolved critical findings remain, but specific non-blocking conditions or improvements remain.

**Changes Required**

Critical or high-severity defects prevent acceptance.

**Unable to Complete**

Required source code, test evidence, or project context is unavailable.

Explain the rationale.

### 14. Prepare Code Review Report

Present the complete report to the user.

Include:

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

Create or modify a file only after the user explicitly types:

`Create File`

General confirmations such as "looks good" or "continue" are not file-creation approval.

### 15. Create Code Review Document

After receiving `Create File`:

1. Use the workflow artifact directory supplied by the prompt or orchestrator.
2. Otherwise use `docs/code-review.md`.
3. Preserve requirement and task traceability.
4. Include evidence for findings.
5. Record actual validation results.
6. Clearly state the review outcome.
7. Do not modify source code.
8. Do not modify tests.
9. Do not modify unrelated files.
10. Do not commit or push changes.

After creating the report, provide its path and summarize the outcome.

### 16. Handoff

Hand the completed review to the Developer or Orchestrator.

If the outcome is `Changes Required`:

- Identify the findings that must be corrected.
- Reference finding IDs.
- Explain the expected correction.
- Request a focused implementation update.
- Review the corrected changes again.

Do not automatically modify the Developer's implementation.

If the outcome permits progression, hand off the implementation and review evidence to the Tester Agent or Orchestrator.

Do not automatically start testing.

## Expected Code Review Document

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

## Rules and Boundaries

- Perform an independent review.
- Review actual source changes.
- Follow approved requirements and architecture.
- Support findings with evidence.
- Do not invent defects or vulnerabilities.
- Do not modify source code during review.
- Do not modify tests during review.
- Do not redesign architecture.
- Do not create implementation tasks.
- Do not automatically start testing.
- Do not commit, push, merge, or create pull requests.
