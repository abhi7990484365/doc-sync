---
name: testing-and-verification
description: Perform unit, integration, regression, and documentation quality testing for Doc-Sync. Use when verifying implemented tasks, executing tests, checking acceptance criteria, or preparing docs/test-report.md.
---

# Testing and Verification

## Purpose

Verify that the implementation meets approved requirements and acceptance criteria.

The Tester Agent defines the role and boundaries. This skill defines the testing procedure. The Testing Prompt starts the workflow.

## When to Use

Use after implementation and code review when tests, acceptance criteria, regression checks, or documentation need verification.

Do not implement application features or redesign architecture.

## Inputs

Use:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`
- `docs/code-review.md`
- Relevant source code, tests, configuration, and generated documentation

If required inputs or dependencies are unavailable, report the limitation. Do not begin final verification while Critical or High code review findings remain unresolved.

## Workflow

### 1. Define Scope

Review approved requirements, acceptance criteria, architecture, implementation tasks, code review findings, and available test environments.

Identify applicable unit, integration, regression, API/UI, security, and documentation checks. Do not treat unapproved functionality as required scope.

### 2. Establish Traceability

Use:

`Requirement → Acceptance Criteria → Test Case → Execution Result → Evidence`

Identify uncovered requirements, unverified criteria, unjustified tests, and missing test data or dependencies.

### 3. Prepare and Run Tests

Use the repository’s existing test framework and conventions.

Cover relevant valid and invalid inputs, boundaries, business rules, error handling, integrations, and regression scenarios.

Run applicable checks supported by the project. Do not send unintended requests to production systems or remove existing tests to obtain a passing result.

Record actual commands, environment, results, and evidence. Never claim an unexecuted test passed.

### 4. Analyze Failures

For each failure, record the test ID, related requirement, expected and actual results, environment, evidence, and likely failure area.

Recommend the next action and send implementation defects to the Developer. Do not modify application code to make tests pass.

### 5. Check Documentation Quality

Review generated documentation for:

- Required sections and complete content
- Accuracy against the implementation
- Consistent requirement and architecture references
- Correct file paths and working internal links
- Valid Markdown and applicable Mermaid diagrams
- Unsupported functionality or unresolved placeholders presented as complete

Record relevant issues.

### 6. Record Defects and Coverage

Assign sequential IDs such as `BUG-001`.

For each defect, include its related test, requirement, and task IDs; summary; environment; reproduction steps; expected and actual results; severity; and evidence.

Check functional requirements, acceptance criteria, unit, integration and regression coverage, negative and boundary scenarios, error handling, and documentation quality.

Do not invent coverage percentages when no coverage report is available.

### 7. Determine the Outcome

Choose one outcome and support it with execution evidence:

- **Passed:** Required tests and documentation checks passed; no unresolved Critical or High defects remain.
- **Passed with Limitations:** Required tests passed, but non-critical checks could not be completed. Document the limitations.
- **Failed:** Required tests failed or unresolved Critical or High defects remain.
- **Blocked:** Testing could not be completed because required access, dependencies, or environments were unavailable.

### 8. Prepare the Test Report

Include:

1. Document Information
2. Testing Scope and Environment
3. Source Documents
4. Requirement Traceability
5. Unit, Integration, and Regression Results
6. Documentation Quality Results
7. Defects and Failures
8. Blocked and Skipped Tests
9. Execution Summary and Final Outcome
10. Risks, Limitations, and Recommendations
11. Handoff Notes

Present the report for review. Create or modify a file only after the user explicitly types `Create File`. General confirmations such as “looks good” or “continue” do not authorize file creation.

After `Create File`, use the artifact directory supplied by the prompt or Orchestrator; otherwise use `docs/test-report.md`. Include actual results and evidence. Do not modify application code, tests, or unrelated files.

### 9. Hand Off

Provide the report and outcome to the Orchestrator or PR Writer, including defects, limitations, documentation issues, and follow-up actions.

If testing failed, send defects to the Developer. After fixes, repeat Code Review before relevant retesting.

Do not automatically create a pull request.

## Rules and Boundaries

- Follow approved requirements and architecture.
- Use actual test evidence and report failures honestly.
- Do not modify source code to hide failures or weaken tests.
- Do not test unapproved functionality as a required feature.
- Do not commit, push, merge, or create pull requests.
- Do not automatically start the PR workflow.