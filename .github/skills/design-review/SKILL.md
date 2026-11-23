---
name: design-review
description: Independently review the Doc-Sync architecture against approved requirements and document findings.
---

# Design Review

## Purpose

Check whether the proposed architecture meets approved requirements and is clear, secure, reliable, and practical to implement.

Review the architecture independently. Do not redesign it during the review.

## Inputs

Use:
- Approved requirements from `docs/requirements.md`.
- Architecture draft from `docs/architecture.md`.
- Existing project documentation and documented technical constraints.

If the requirements or architecture are missing, or approval status is unclear, ask before proceeding. Do not treat a draft as approved.

## Workflow

### 1. Understand the design

Identify the system boundaries, components, responsibilities, integrations, data flows, technology choices, and documented constraints.

Use the original requirement IDs. Do not introduce new requirements.

### 2. Review requirement coverage

For each requirement, check whether the architecture explains how it will be met.

Mark coverage as **Fully Addressed**, **Partially Addressed**, **Not Addressed**, or **Unable to Verify**.

Identify missing coverage and unsupported assumptions.

### 3. Review the architecture

Check:
- Component responsibilities and boundaries.
- Dependencies and unnecessary complexity.
- Integrations, data flows, and error handling.
- Authentication, authorization, secrets, and sensitive data.
- Reliability, performance, and recovery considerations.
- Consistency between diagrams, architecture text, and ADRs.
- Whether the design is feasible and maintainable.

Do not assume undocumented API behavior or security policies.

### 4. Record findings

Give each finding an ID such as `DR-001`.

Include its severity, related requirement IDs, architecture section, evidence, impact, and recommended action.

Use **Critical**, **High**, **Medium**, **Low**, or **Informational**. Distinguish confirmed issues from open questions.

### 5. Set the review outcome

Choose one and explain the reason:

- **Approved** — no unresolved critical or high-severity findings remain.
- **Approved with Conditions** — no critical findings remain, but follow-up actions are needed.
- **Changes Required** — significant issues must be resolved before planning can proceed.
- **Unable to Complete** — required information is missing.

Present the report for approval. Do not create or modify a file until the user explicitly types:

`Create File`

### 6. Create the report

After receiving `Create File`, use the artifact path provided by the Orchestrator. If none is provided, use `docs/design-review.md`.

Include the review scope, requirement coverage, findings, risks, recommendations, outcome, and follow-up actions. Keep the report focused on evidence from the source documents.

Do not automatically change the architecture, modify unrelated files, or commit or push changes.

## Handoff

Send the outcome, important findings, open questions, and required follow-up actions to the Architect or Orchestrator.

If changes are required, the Architect can revise the architecture in a separate workflow. Review the revised architecture before it moves to implementation planning.

Do not automatically start the next phase.

## Boundaries

- Review independently and support findings with evidence.
- Follow approved requirements; do not invent requirements or constraints.
- Do not rewrite the architecture or create implementation tasks.
- Do not write application code.
- Do not commit, push, merge, or create pull requests.