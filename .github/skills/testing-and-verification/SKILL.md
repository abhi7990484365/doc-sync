---
name: testing-and-verification
description: Perform comprehensive unit, integration, regression, and documentation quality testing for Doc-Sync. Use when verifying implemented tasks, executing automated tests, validating acceptance criteria, or preparing docs/test-report.md.
---

# Testing and Verification

## Purpose

Verify that the Doc-Sync implementation satisfies approved requirements and acceptance criteria.

Perform comprehensive unit and integration testing, regression checks, and final documentation quality validation.

The Tester Agent defines the role, tools, responsibilities, and decision boundaries.

This skill defines the reusable testing and verification procedure.

The Testing Prompt starts the workflow.

## When to Use

Use this skill when:

- Implementation tasks have been completed.
- Code review has been completed.
- Unit tests need to be executed.
- Integration tests need to be executed.
- Acceptance criteria need verification.
- Regression testing is required.
- Generated documentation needs quality validation.
- A final test report needs creation.

Do not use this skill to implement application features or independently redesign architecture.

## Inputs

Use:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`
- `docs/code-review.md`
- Application source code.
- Existing tests.
- Test configuration.
- Generated documentation.

If required source documents or test dependencies are unavailable, identify the limitation before proceeding.

## Workflow

### 1. Verify Testing Inputs

1. Locate approved requirements.
2. Locate approved architecture.
3. Locate the implementation plan.
4. Review the design review outcome.
5. Review the Code Review report.
6. Identify completed implementation tasks.
7. Identify acceptance criteria.
8. Identify available test environments.

Do not proceed with final verification if critical code review findings remain unresolved.

### 2. Define Testing Scope

Identify applicable testing activities:

- Unit testing.
- Integration testing.
- Regression testing.
- API testing, where applicable.
- UI testing, where applicable.
- Security checks, where applicable.
- Documentation quality testing.

Use approved requirements and architecture to establish scope.

Do not introduce tests for unapproved functionality.

### 3. Build Requirement-to-Test Traceability

Maintain:

`Requirement -> Acceptance Criteria -> Test Case -> Execution Result -> Evidence`

Identify:

- Requirements without test coverage.
- Acceptance criteria without verification.
- Tests without requirement or technical justification.
- Tests that cannot execute.
- Missing test data or dependencies.

### 4. Prepare Unit Tests

Verify individual components and functions.

Consider:

- Valid inputs.
- Invalid inputs.
- Empty values.
- Boundary values.
- Expected outputs.
- Exception handling.
- Business rules.
- Failure scenarios.

Use the existing test framework and project conventions.

### 5. Prepare Integration Tests

Verify interactions between components.

Consider:

- Component communication.
- API integrations.
- External service interactions.
- Authentication and authorization.
- Data transfer.
- Data transformation.
- Error propagation.
- Retry and timeout behavior.
- Integration failure scenarios.

Use controlled environments or mocks where appropriate.

Do not send unintended requests to production systems.

### 6. Perform Regression Testing

Identify existing functionality affected by the implementation.

Verify:

- Previously implemented functionality.
- Related components.
- Existing acceptance criteria.
- Existing automated tests.
- Known defect fixes.

Do not remove existing regression coverage to obtain a passing result.

### 7. Execute Tests

Run relevant tests using the commands supported by the repository.

Record:

- Test command.
- Environment.
- Execution result.
- Passed tests.
- Failed tests.
- Blocked tests.
- Skipped tests.
- Error messages.
- Evidence.

Do not claim that a test passed unless it actually executed successfully.

### 8. Analyze Failures

For each failed test:

1. Identify the test ID.
2. Identify the related requirement.
3. Capture the actual result.
4. Compare expected and actual behavior.
5. Collect logs and relevant evidence.
6. Identify the likely failure area.
7. Record the defect.
8. Recommend the next action.

Do not silently change application code to make tests pass.

Send implementation defects to the Developer.

### 9. Perform Documentation Quality Validation

Identify generated documentation and verify:

- Required sections exist.
- Content is complete.
- Technical descriptions match implementation.
- Requirements and architecture references are consistent.
- File paths are correct.
- Internal links work.
- Markdown formatting is valid.
- Mermaid diagrams are syntactically valid, where applicable.
- No unsupported functionality is documented.
- No unresolved placeholders are presented as completed content.

Document all relevant issues.

### 10. Record Defects

Assign sequential defect IDs:

- `BUG-001`
- `BUG-002`
- `BUG-003`

For each defect, include:

- Defect ID.
- Related test ID.
- Related requirement ID.
- Related implementation task.
- Summary.
- Environment.
- Steps to reproduce.
- Expected result.
- Actual result.
- Severity.
- Evidence.

### 11. Validate Test Coverage

Check:

1. Functional requirement coverage.
2. Acceptance criteria coverage.
3. Unit test coverage.
4. Integration test coverage.
5. Regression coverage.
6. Negative scenarios.
7. Boundary scenarios.
8. Error handling.
9. Documentation quality coverage.

Do not invent coverage percentages when no coverage report is available.

### 12. Determine Final Verification Outcome

Choose one:

**Passed**

All required tests passed, no unresolved critical or high-severity defects remain, and documentation quality checks passed.

**Passed with Limitations**

Required tests passed, but non-critical checks could not be completed. Clearly document the limitations.

**Failed**

Required tests failed or unresolved critical or high-severity defects remain.

**Blocked**

Testing could not be completed because required access, dependencies, or environments were unavailable.

Explain the selected outcome using execution evidence.

### 13. Prepare Test Report

Present the complete report to the user.

Include:

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

Create or modify a file only after the user explicitly types:

`Create File`

General confirmations such as "looks good" or "continue" are not file-creation approval.

### 14. Create Test Report

After receiving `Create File`:

1. Use the workflow artifact directory supplied by the prompt or orchestrator.
2. Otherwise use `docs/test-report.md`.
3. Preserve requirement and task traceability.
4. Include actual execution results.
5. Include evidence for failures and defects.
6. Clearly document blocked and skipped tests.
7. Record documentation quality results.
8. Do not modify application code.
9. Do not modify tests to hide failures.
10. Do not modify unrelated files.
11. Do not commit or push changes.

### 15. Handoff

Provide the final test report to the Orchestrator or PR Writer.

Include:

- Final verification outcome.
- Test execution summary.
- Defects.
- Remaining limitations.
- Documentation quality results.
- Required follow-up actions.

If the outcome is `Failed`, send defects to the Developer for correction.

After corrections, execute the relevant tests again.

Do not automatically create a pull request.

## Expected Test Report Document

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

## Rules and Boundaries

- Follow approved requirements.
- Follow approved architecture.
- Review code review findings.
- Use actual test execution evidence.
- Do not invent test results.
- Do not ignore failed tests.
- Do not modify source code to hide failures.
- Do not weaken existing tests.
- Do not test unapproved functionality as a required feature.
- Do not commit, push, merge, or create pull requests.
- Do not automatically start the PR workflow.
