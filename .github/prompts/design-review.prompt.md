---
name: design-review
description: Independently review the Doc-Sync architecture against approved requirements and create a structured design review report.
agent: design-reviewer
---

# Design Review Workflow

## Objective

Perform an independent review of the Doc-Sync solution architecture against approved requirements.

Identify design gaps, security risks, technical risks, integration issues, and architecture inconsistencies.

Prepare a structured design review report.

## Inputs

Use:

- `docs/requirements.md`
- `docs/architecture.md`
- Relevant existing project documentation.

Workflow artifact directory:

`${input:workflowDir:docs}`

If the input is not supplied, use `docs`.

## Step 1: Verify Source Documents

1. Locate `docs/requirements.md`.
2. Locate `docs/architecture.md`.
3. Read both documents completely.
4. Verify that requirements are approved.
5. Confirm that the architecture is ready for independent review.

If either document is missing or approval status is unclear, ask the user before proceeding.

Do not invent missing requirements or architecture details.

## Step 2: Understand the Requirements

Identify:

- Functional requirements.
- Non-functional requirements.
- Acceptance criteria.
- Security requirements.
- Integration requirements.
- Data requirements.
- Technical constraints.
- Scope exclusions.

Preserve original requirement IDs.

## Step 3: Understand the Architecture

Analyze:

- System boundaries.
- Major components.
- Component responsibilities.
- Integration points.
- Communication patterns.
- Data flows.
- Technology choices.
- Security boundaries.
- Architecture diagrams.
- Architecture Decision Records.

Understand how the proposed architecture addresses the requirements.

## Step 4: Perform Independent Review

Evaluate:

1. Requirements alignment.
2. Architecture completeness.
3. Component boundaries.
4. Component dependencies.
5. Integration architecture.
6. API design.
7. Data architecture.
8. Authentication and authorization.
9. Security and privacy.
10. Error handling and reliability.
11. Scalability and performance.
12. Maintainability.
13. Technical feasibility.
14. Deployment considerations, where applicable.
15. Diagram consistency.
16. Architecture Decision Records.
17. Requirement traceability.
18. Technical risks and dependencies.

Do not limit the review to these areas if additional relevant risks are found.

Do not report unsupported assumptions as confirmed defects.

## Step 5: Create Requirement Coverage Matrix

For each approved requirement, identify its architecture coverage.

Use these statuses:

- Fully Addressed.
- Partially Addressed.
- Not Addressed.
- Unable to Verify.

Include:

- Requirement ID.
- Requirement summary.
- Architecture component or section.
- Coverage status.
- Review comments.

## Step 6: Record Architecture Findings

Create finding IDs:

- `DR-001`
- `DR-002`
- `DR-003`

For each finding, include:

- Finding ID.
- Severity.
- Finding type.
- Related requirement IDs.
- Architecture section or component.
- Description.
- Evidence.
- Impact.
- Recommended action.

Use severity levels:

- Critical.
- High.
- Medium.
- Low.
- Informational.

## Step 7: Evaluate Security, Integration, and Reliability

Review whether the architecture sufficiently addresses:

- Authentication and authorization.
- Least-privilege access.
- Secret management.
- Secure communication.
- Input validation.
- External integration failures.
- Retry and timeout behavior.
- Data handling.
- Auditability.
- Error recovery.
- Scalability and performance.

Record missing information as open questions when evidence is insufficient.

## Step 8: Determine Review Outcome

Choose one:

- **Approved:** No unresolved critical or high-severity findings remain, and the architecture sufficiently addresses documented requirements.
- **Approved with Conditions:** No unresolved critical findings remain, but specific high-priority actions or conditions must be addressed.
- **Changes Required:** Critical or significant high-severity issues prevent proceeding with the current architecture.
- **Unable to Complete:** Required information is missing or the review cannot be completed reliably.

Explain the selected outcome and supporting evidence.

## Step 9: Prepare Review Report

Prepare the complete `design-review.md` content.

Use these sections:

1. Document Information.
2. Review Scope.
3. Source Documents.
4. Architecture Summary.
5. Requirement Coverage Matrix.
6. Architecture Review Findings.
7. Component Architecture Review.
8. Integration Architecture Review.
9. Data Architecture Review.
10. Security Review.
11. Reliability and Performance Review.
12. Diagram and ADR Review.
13. Risks and Dependencies.
14. Recommendations.
15. Review Outcome.
16. Open Questions.
17. Required Follow-up Actions.

Do not create the file yet.

Present the complete report to the user for review.

## Step 10: Obtain Explicit Approval

Create or modify the report only after the user explicitly types:

`Create File`

General confirmations such as "looks good" or "continue" do not authorize file creation.

## Step 11: Create Review Document

After receiving `Create File`:

1. Use the supplied workflow artifact directory.
2. Otherwise use `docs/design-review.md`.
3. Preserve requirement IDs and architecture references.
4. Include evidence for significant findings.
5. Clearly identify assumptions and open questions.
6. Record the review outcome.
7. Do not modify `docs/architecture.md`.
8. Do not modify unrelated files.
9. Do not commit or push changes.

## Step 12: Report Completion

After creating the file, report:

- Created file path.
- Review outcome.
- Total findings by severity.
- Critical and high-severity findings.
- Required architecture changes.
- Open questions.
- Recommended next action.

Hand off the report to the Architect or Orchestrator.

Do not automatically start implementation planning or development.

## Boundaries

- Do not modify approved requirements.
- Do not redesign the architecture during the review.
- Do not modify the architecture document without separate authorization.
- Do not create implementation tasks.
- Do not write application code.
- Do not commit, push, merge, or create pull requests.
- Do not automatically invoke the next phase.
