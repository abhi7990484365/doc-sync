---
name: testing
description: Execute comprehensive unit, integration, regression, and documentation quality tests for Doc-Sync and prepare the final test report.
agent: tester
---

# Testing and Verification Workflow

## Objective

Perform comprehensive testing and final verification of the Doc-Sync implementation.

Verify that implemented functionality satisfies approved requirements, architecture, implementation tasks, and acceptance criteria.

Validate generated documentation for completeness, accuracy, and consistency.

Workflow artifact directory:

`${input:workflowDir:docs}`

Optional task ID:

`${input:taskId:Enter a task ID to test a specific implementation, or leave empty for the approved implementation scope}`

## Step 1: Verify Source Documents

Read:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`
- `docs/code-review.md`

Verify:

1. Requirements are approved.
2. Architecture is approved.
3. Implementation tasks are completed or ready for testing.
4. Code review has been completed.
5. Critical and high-severity code review findings have been addressed.
6. Test environment and dependencies are available.

If required documents are missing, ask the user before proceeding.

If the Code Review outcome is `Changes Required`, stop final verification and return the findings to the Developer.

## Step 2: Define Testing Scope

Identify applicable testing activities:

- Unit testing.
- Integration testing.
- Regression testing.
- API testing, where applicable.
- UI testing, where applicable.
- Security checks, where applicable.
- Documentation quality testing.

If a task ID is supplied, focus on that task and its related dependencies.

Otherwise, test the approved implementation scope.

Do not test unapproved functionality as a required feature.

## Step 3: Map Requirements to Tests

Maintain:

`Requirement -> Acceptance Criteria -> Test Case -> Execution Result -> Evidence`

Identify missing test coverage and unresolved verification dependencies.

## Step 4: Prepare Unit Tests

Identify and execute unit test scenarios for:

- Individual functions and methods.
- Component behavior.
- Input validation.
- Business logic.
- Expected outputs.
- Error handling.
- Boundary conditions.

Use the repository's existing testing framework.

## Step 5: Prepare Integration Tests

Identify and execute integration test scenarios for:

- Component interactions.
- API integrations.
- External service interactions.
- Authentication and authorization.
- Data flow.
- Data transformation.
- Error propagation.
- Retry and timeout behavior.

Use controlled environments and test data.

Do not unintentionally modify production data.

## Step 6: Perform Regression Testing

Identify functionality affected by recent changes.

Execute relevant regression tests.

Verify that previously implemented functionality remains correct.

## Step 7: Execute Tests

Run the applicable test commands supported by the repository.

Record:

- Command executed.
- Environment.
- Total tests.
- Passed tests.
- Failed tests.
- Blocked tests.
- Skipped tests.
- Error messages.
- Evidence.

Do not invent execution results.

## Step 8: Analyze Failures

For every failed test:

1. Identify the test ID.
2. Identify the related requirement.
3. Capture expected behavior.
4. Capture actual behavior.
5. Record reproduction steps.
6. Collect logs or evidence.
7. Assign a defect ID.
8. Recommend corrective action.

Do not modify application code to hide failures.

## Step 9: Validate Documentation Quality

Inspect generated documentation and verify:

- Required sections exist.
- Content is complete.
- Technical descriptions match the implementation.
- Requirements and architecture references are consistent.
- File paths are correct.
- Internal links work.
- Markdown formatting is valid.
- Mermaid diagrams are syntactically valid, where applicable.
- Unsupported functionality is not documented as implemented.
- Unresolved placeholders are clearly identified.

Record documentation issues with file paths and relevant sections.

## Step 10: Determine Test Coverage

Check:

- Functional requirement coverage.
- Acceptance criteria coverage.
- Unit test coverage.
- Integration test coverage.
- Regression coverage.
- Positive scenarios.
- Negative scenarios.
- Boundary scenarios.
- Error handling.
- Documentation quality coverage.

Do not invent coverage percentages without a real coverage report.

## Step 11: Determine Final Verification Outcome

Select one:

- **Passed:** All required tests passed, no unresolved critical or high-severity defects remain, and documentation quality checks passed.
- **Passed with Limitations:** Required tests passed, but documented non-critical checks could not be completed.
- **Failed:** Required tests failed or unresolved critical or high-severity defects remain.
- **Blocked:** Testing could not be completed because required access, dependencies, or environments were unavailable.

Explain the selected outcome.

## Step 12: Prepare Test Report

Prepare the complete `docs/test-report.md` content.

Use these sections:

1. Document Information.
2. Testing Scope.
3. Source Documents.
4. Test Environment.
5. Requirement Traceability Matrix.
6. Unit Test Results.
7. Integration Test Results.
8. Regression Test Results.
9. Documentation Quality Results.
10. Defects and Failures.
11. Blocked and Skipped Tests.
12. Test Execution Summary.
13. Final Verification Outcome.
14. Risks and Limitations.
15. Recommendations.
16. Handoff Notes.

Present the complete report to the user.

Do not create the file yet.

## Step 13: Obtain Explicit Approval

Create or modify the test report only after the user explicitly types:

`Create File`

General confirmations such as "looks good" or "continue" do not authorize file creation.

## Step 14: Create Test Report

After receiving `Create File`:

1. Use the supplied workflow artifact directory.
2. Otherwise use `docs/test-report.md`.
3. Preserve requirement and task traceability.
4. Include actual test execution results.
5. Document failures and defects.
6. Identify blocked and skipped tests.
7. Include documentation quality results.
8. Do not modify application source code.
9. Do not weaken existing tests.
10. Do not modify unrelated files.
11. Do not commit or push changes.

## Step 15: Report Completion

Report:

- Created file path.
- Testing scope.
- Total tests.
- Passed tests.
- Failed tests.
- Blocked tests.
- Skipped tests.
- Defect count and severity.
- Documentation quality results.
- Final verification outcome.
- Known limitations.
- Recommended next action.

Hand off the report and evidence to the Orchestrator or PR Writer.

If defects remain, send them to the Developer for correction and retesting.

Do not automatically create a pull request.

## Boundaries

- Do not modify approved requirements.
- Do not redesign architecture.
- Do not modify application code to hide failures.
- Do not weaken existing tests.
- Do not invent test results.
- Do not ignore failed tests.
- Do not commit, push, merge, or create pull requests.
- Do not automatically start the PR workflow.
