---
name: implementation-planning
description: Convert approved Doc-Sync requirements, architecture, and design review findings into a prioritized, dependency-ordered implementation plan. Use when creating or updating docs/impl-plan.md.
---

# Implementation Planning

## Purpose

Create an actionable implementation plan from approved Doc-Sync requirements and reviewed architecture.

The plan must identify:

- Implementation tasks.
- Task dependencies.
- Priority.
- Requirement traceability.
- Completion criteria.
- Verification activities.
- Blocked tasks.
- Unresolved decisions.

The Planner Agent defines the role, tools, responsibilities, and decision boundaries.

This skill defines the reusable implementation planning procedure.

The Planning Prompt starts the workflow.

## When to Use

Use this skill when:

- Requirements have been approved.
- Architecture has been approved for planning.
- Design review findings need to be considered.
- Architecture components need to be broken into implementation tasks.
- Dependencies and implementation order need to be established.
- A structured implementation plan needs to be created or updated.

Do not use this skill to discover requirements, design architecture, or write application code.

## Inputs

Use:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- Existing project documentation.
- Approved technical constraints and decisions.

If a required document is missing, ask the user before proceeding.

Do not assume draft requirements or unapproved architecture decisions are approved.

## Workflow

### 1. Verify Planning Inputs

1. Locate `docs/requirements.md`.
2. Locate `docs/architecture.md`.
3. Read both documents completely.
4. Verify their approval status.
5. Read `docs/design-review.md`, if available.
6. Review unresolved findings and conditions.
7. Identify missing decisions and external dependencies.

Do not plan implementation around unresolved critical architecture issues.

### 2. Review Requirements

Identify:

- Functional requirements.
- Non-functional requirements.
- Acceptance criteria.
- Security requirements.
- Integration requirements.
- Data requirements.
- Constraints.
- Scope exclusions.

Preserve original requirement IDs.

### 3. Review Architecture

Identify:

- System components.
- Component responsibilities.
- Integration points.
- Data structures and flows.
- APIs and interfaces.
- Security controls.
- Error handling.
- Infrastructure and deployment requirements, where applicable.

Use the approved architecture as the implementation baseline.

Do not introduce new components without documented justification and approval.

### 4. Review Design Findings

Read the design review outcome and findings.

Determine:

- Which findings must be addressed before implementation.
- Which findings can be handled as implementation tasks.
- Which findings require architecture changes.
- Which decisions remain open.
- Which conditions affect implementation order.

Do not silently convert an architecture recommendation into an approved implementation requirement.

### 5. Identify Workstreams

Group related implementation work into logical workstreams.

Possible candidate workstreams for Doc-Sync include:

- Project foundation and configuration.
- GitHub integration.
- Change detection.
- Documentation parsing.
- Documentation impact analysis.
- Documentation update generation.
- Validation.
- Human approval.
- Documentation synchronization.
- Audit logging and reporting.
- Testing and quality assurance.
- Deployment and operational readiness.

These are candidate workstreams, not mandatory project scope. Include only work supported by approved requirements and architecture.

### 6. Break Work into Tasks

Create small, actionable tasks.

Assign sequential IDs:

- `TASK-001`
- `TASK-002`
- `TASK-003`

Each task must include:

1. Task ID.
2. Title.
3. Description.
4. Related requirement IDs.
5. Architecture component.
6. Dependencies.
7. Priority.
8. Completion criteria.
9. Verification approach.
10. Status.

Avoid tasks that are too broad to implement or verify.

### 7. Define Dependencies

Identify task prerequisites.

For each dependency:

- Reference the prerequisite task ID.
- Explain the dependency.
- Verify that the prerequisite exists.
- Identify blocked tasks.
- Avoid circular dependencies.

Organize tasks in a logical implementation sequence.

### 8. Assign Priorities

Use:

- **P0 - Critical:** Required prerequisite or critical functionality.
- **P1 - High:** Important functionality needed for planned delivery.
- **P2 - Medium:** Supporting functionality or improvements.
- **P3 - Low:** Optional work that does not block core delivery.

Justify priority using approved requirements, dependencies, or documented risks.

### 9. Define Completion Criteria

Each task must have clear completion criteria.

Criteria should describe an observable result.

Examples of suitable criteria:

- Required interface is implemented according to the approved architecture.
- Expected input and output behavior is covered by tests.
- Error handling is implemented for documented failure scenarios.
- Relevant automated tests pass.
- Security requirements associated with the task are verified.

Do not invent specific technical behavior that is absent from the approved design.

### 10. Define Verification Approach

For each task, identify relevant verification activities:

- Unit tests.
- Integration tests.
- API tests.
- UI tests, where applicable.
- Security checks, where applicable.
- Documentation validation.
- Manual verification, where necessary.

Verification must align with the acceptance criteria and architecture.

### 11. Maintain Traceability

Maintain:

`Requirement -> Architecture Component -> Implementation Task -> Verification`

Identify:

- Requirements without implementation tasks.
- Tasks without requirement or architecture justification.
- Architecture components without planned implementation work.
- Tasks without verification criteria.
- Unresolved dependencies.

Explain any intentional exclusions.

### 12. Identify Risks and Blockers

Document:

- Unresolved design review findings.
- Pending technical decisions.
- External dependencies.
- Access requirements.
- Environment dependencies.
- Integration risks.
- Tasks blocked by missing information.

Do not invent owners, dates, estimates, or external commitments.

### 13. Validate the Implementation Plan

Check:

1. Requirements coverage.
2. Architecture alignment.
3. Design review conditions.
4. Task completeness.
5. Dependency validity.
6. Circular dependencies.
7. Priority justification.
8. Completion criteria.
9. Verification coverage.
10. Blocked tasks.
11. Risks and open decisions.
12. Implementation order.

Report gaps rather than silently filling them with assumptions.

### 14. Present the Plan for Approval

Present the complete implementation plan to the user.

Include:

- Planning overview.
- Source documents.
- Workstreams.
- Prioritized task list.
- Dependencies.
- Requirement traceability.
- Completion criteria.
- Verification approach.
- Blocked tasks.
- Risks and open decisions.

Create or modify a file only after the user explicitly types:

`Create File`

General confirmations such as "looks good" or "continue" are not file-creation approval.

### 15. Create Implementation Plan

After receiving `Create File`:

1. Use the workflow artifact directory supplied by the prompt or orchestrator.
2. Otherwise use `docs/impl-plan.md`.
3. Do not create multiple competing implementation plans.
4. Preserve original requirement IDs.
5. Keep dependencies consistent.
6. Clearly identify blocked tasks.
7. Record assumptions and open decisions.
8. Do not write application source code.
9. Do not modify unrelated files.
10. Do not commit or push changes.

After creating the document, report its path and summarize the plan.

### 16. Handoff

Hand the implementation plan to the Developer or Orchestrator.

Include:

- Task IDs and priorities.
- Required task dependencies.
- Completion criteria.
- Verification expectations.
- Blocked tasks.
- Unresolved decisions.
- Required approvals.

The Developer should implement only explicitly selected and approved tasks.

Do not automatically start development.

## Expected Implementation Plan Document

Use these sections:

1. Document Information.
2. Planning Overview.
3. Source Documents.
4. Planning Assumptions and Constraints.
5. Architecture Summary.
6. Implementation Workstreams.
7. Prioritized Task List.
8. Task Dependencies.
9. Requirement Traceability Matrix.
10. Completion Criteria.
11. Verification Strategy.
12. Risks and Blockers.
13. Open Decisions.
14. Implementation Sequence.
15. Handoff Notes.

## Rules and Boundaries

- Follow approved requirements.
- Follow the approved architecture.
- Consider design review findings.
- Never invent scope or technical constraints.
- Clearly identify assumptions and blockers.
- Do not redesign architecture.
- Do not modify approved requirements.
- Do not write application source code.
- Do not execute implementation tasks.
- Do not commit, push, merge, or create pull requests.
- Do not automatically start development.
