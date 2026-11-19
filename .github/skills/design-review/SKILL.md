---
name: design-review
description: Independently review the Doc-Sync solution architecture against approved requirements. Identify architecture gaps, security risks, technical risks, inconsistencies, and recommendations. Use when evaluating architecture.md and preparing design-review.md.
---

# Design Review

## Purpose

Provide an independent technical evaluation of the Doc-Sync solution architecture.

The Design Reviewer evaluates whether the proposed architecture:

- Satisfies approved requirements.
- Has clear component boundaries.
- Uses appropriate integration and data designs.
- Addresses security and reliability.
- Is technically feasible.
- Is maintainable and extensible.
- Provides sufficient information for implementation planning.

The Design Reviewer Agent defines the role, tools, responsibilities, and decision boundaries.

This skill defines the reusable architecture review procedure.

The Design Review Prompt starts the workflow.

## When to Use

Use this skill when:

- An architecture document is ready for independent review.
- Architecture decisions need validation.
- Technical risks and design gaps need identification.
- Security and reliability considerations need evaluation.
- Architecture diagrams need consistency checks.
- A formal design review report needs creation.

Do not use this skill to discover business requirements, design a new architecture from scratch, create implementation tasks, or write application code.

## Inputs

Use:

- Approved `docs/requirements.md`.
- Proposed or reviewed `docs/architecture.md`.
- Existing project documentation.
- Documented technology constraints.
- Existing Architecture Decision Records.

If the requirements or architecture document is missing, ask the user to complete the relevant phase first.

Do not assume that a draft architecture is approved.

## Workflow

### 1. Verify Review Inputs

1. Locate `docs/requirements.md`.
2. Locate `docs/architecture.md`.
3. Read both documents completely.
4. Verify that requirements are approved.
5. Confirm that the architecture is ready for review.
6. Identify missing documents, incomplete sections, and unclear approval status.

Do not begin a formal review if critical source information is unavailable.

### 2. Understand Requirements

Extract:

- Functional requirements.
- Non-functional requirements.
- Acceptance criteria.
- Security requirements.
- Performance requirements.
- Integration requirements.
- Data requirements.
- Technical constraints.
- Scope exclusions.

Use the original requirement IDs.

Do not introduce new requirements during the review.

### 3. Understand the Proposed Architecture

Identify:

- System boundaries.
- External systems.
- Major components.
- Component responsibilities.
- Communication patterns.
- Data flows.
- Technology choices.
- Security boundaries.
- Deployment approach, where documented.
- Architecture decisions.

Build an understanding of how the proposed solution is expected to work.

### 4. Evaluate Requirement Alignment

For each approved requirement:

1. Identify its architectural coverage.
2. Find the component or design decision responsible for satisfying it.
3. Evaluate whether the proposed solution is sufficient.
4. Identify missing or unclear coverage.
5. Record unsupported assumptions.

Classify coverage as:

- Fully Addressed.
- Partially Addressed.
- Not Addressed.
- Unable to Verify.

### 5. Review Component Architecture

Evaluate:

- Component responsibilities.
- Separation of concerns.
- Component boundaries.
- Dependencies.
- Coupling and cohesion.
- Duplicate responsibilities.
- Missing responsibilities.
- Unnecessary complexity.

Identify components that have no clear requirement or technical justification.

### 6. Review Integration Architecture

Evaluate:

- External system dependencies.
- Communication mechanisms.
- Authentication requirements.
- Data exchanged.
- Error handling.
- Retry and timeout behavior.
- Rate limits, where documented.
- Failure isolation.
- Integration security.

Do not assume undocumented API behavior.

Record missing integration information as an open finding.

### 7. Review Data Architecture

Evaluate:

- Data entities and relationships.
- Data ownership.
- Data validation.
- Data storage.
- Data lifecycle.
- Data retention.
- Sensitive information handling.
- Auditability.
- Data consistency.

Identify missing or unclear data responsibilities.

### 8. Review Security Architecture

Evaluate:

- Authentication.
- Authorization.
- Least-privilege access.
- Secret management.
- Secure communication.
- Trust boundaries.
- Input validation.
- Sensitive data exposure.
- Logging and auditability.

Identify security gaps and explain their potential impact.

Do not invent security policies or claim a vulnerability without supporting evidence.

### 9. Review Reliability and Performance

Evaluate:

- Error handling.
- Retry mechanisms.
- Timeout handling.
- Failure recovery.
- Availability.
- Scalability.
- Performance considerations.
- External dependency failures.
- Operational monitoring, where applicable.

Identify missing failure scenarios and unsupported performance assumptions.

### 10. Review Diagrams and Architecture Decisions

Verify:

- Diagrams reflect the written architecture.
- Component interactions are consistent.
- Data flows are understandable.
- System boundaries are clear.
- ADRs explain significant decisions.
- Decision statuses are accurate.
- Technology recommendations have documented rationale.

Identify contradictions between diagrams, ADRs, and architecture descriptions.

### 11. Maintain Finding Traceability

For each finding, create an ID:

- `DR-001`
- `DR-002`
- `DR-003`

Each finding must include:

- Finding ID.
- Severity.
- Finding type.
- Related requirement IDs.
- Architecture section or component.
- Description.
- Evidence.
- Impact.
- Recommended action.

Use only evidence available in the source documents.

### 12. Classify Findings

Use these severity levels:

- **Critical:** Fundamental issue that could make the solution unsafe, infeasible, or unable to satisfy a critical requirement.
- **High:** Significant issue that should be resolved before implementation.
- **Medium:** Important improvement or clarification.
- **Low:** Minor concern or improvement.
- **Informational:** Observation without required corrective action.

Distinguish confirmed issues from assumptions and open questions.

### 13. Determine Review Outcome

Select one outcome:

**Approved**

No unresolved critical or high-severity findings remain, and the architecture sufficiently addresses documented requirements.

**Approved with Conditions**

No unresolved critical findings remain, but specific high-priority actions or conditions must be addressed.

**Changes Required**

Critical or significant high-severity issues prevent implementation planning from proceeding on the current architecture.

**Unable to Complete**

Required source information is missing or the architecture cannot be evaluated reliably.

Explain the evidence and rationale behind the outcome.

### 14. Prepare Review Report

Present the complete review report to the user.

Include:

1. Review Information.
2. Review Scope.
3. Source Documents.
4. Architecture Summary.
5. Requirement Coverage Matrix.
6. Architecture Review Findings.
7. Security Review.
8. Integration Review.
9. Data Architecture Review.
10. Reliability and Performance Review.
11. Diagram and ADR Review.
12. Risks and Dependencies.
13. Recommendations.
14. Review Outcome.
15. Open Questions.
16. Required Follow-up Actions.

Create or modify a file only after the user explicitly types:

`Create File`

General confirmations such as "looks good" or "continue" are not file-creation approval.

### 15. Create Design Review Document

After receiving `Create File`:

1. Use the workflow artifact directory supplied by the prompt or orchestrator.
2. Otherwise use `docs/design-review.md`.
3. Do not create multiple competing review documents.
4. Preserve requirement and architecture traceability.
5. Include evidence for every significant finding.
6. Clearly distinguish confirmed findings from open questions.
7. Record the review outcome and rationale.
8. Do not modify the architecture document automatically.
9. Do not modify unrelated files.
10. Do not commit or push changes.

After creating the document, report its path and summarize the review outcome.

### 16. Handoff

Hand the completed review to the Architect or Orchestrator.

The handoff must include:

- Review outcome.
- Critical and high-severity findings.
- Recommended architecture changes.
- Open findings.
- Deferred decisions.
- Items requiring stakeholder approval.

If changes are required, the Architect may revise `docs/architecture.md` in a separate workflow.

The revised architecture must be reviewed again before it is treated as ready for implementation planning.

Do not automatically start the next phase.

## Expected Design Review Document

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

## Rules and Boundaries

- Perform an independent review.
- Follow approved requirements.
- Never invent requirements or technical constraints.
- Support findings with evidence.
- Do not modify approved requirements.
- Do not rewrite the architecture during the review.
- Do not approve your own findings without evidence.
- Do not create implementation tasks.
- Do not write application source code.
- Do not commit, push, merge, or create pull requests.
- Do not automatically start implementation planning.
