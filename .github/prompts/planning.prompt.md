---
name: planning
description: Create a prioritized and dependency-ordered implementation plan from approved Doc-Sync requirements, architecture, and design review findings.
agent: planner
---

# Implementation Planning Workflow

## Objective

Create a structured implementation plan for Doc-Sync using approved requirements, approved architecture, and design review findings.

The plan must contain actionable tasks, dependencies, priorities, completion criteria, verification activities, and requirement traceability.

## Inputs

Use:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- Relevant existing project documentation.

Workflow artifact directory:

`${input:workflowDir:docs}`

## Step 1: Verify Source Documents

1. Locate `docs/requirements.md`.
2. Locate `docs/architecture.md`.
3. Locate `docs/design-review.md`, if available.
4. Read the relevant documents completely.
5. Verify requirements approval.
6. Verify architecture approval for planning.
7. Identify unresolved design review findings.

If required documents are missing or approval status is unclear, ask the user before proceeding.

If the design review outcome is `Changes Required`, stop planning and request an updated, reviewed architecture.

If the outcome is `Approved with Conditions`, document the conditions and identify their impact on implementation.

If no design review exists, ask whether the user authorizes planning without it.

## Step 2: Analyze Requirements

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

## Step 3: Analyze Architecture

Identify:

- Architecture components.
- Component responsibilities.
- Integrations.
- APIs and interfaces.
- Data flows.
- Security controls.
- Error handling.
- Deployment considerations.

Use the approved architecture as the technical baseline.

## Step 4: Analyze Design Review Findings

Identify:

- Critical findings.
- High-severity findings.
- Required architecture changes.
- Conditions.
- Deferred decisions.
- External dependencies.
- Implementation blockers.

Do not ignore unresolved findings.

## Step 5: Define Workstreams

Identify logical implementation workstreams based on approved scope.

Possible Doc-Sync workstreams include:

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

These are candidate workstreams only. Include a workstream only when supported by approved requirements and architecture.

## Step 6: Create Tasks

Create sequential task IDs:

- `TASK-001`
- `TASK-002`
- `TASK-003`

For every task, include:

- Task ID.
- Title.
- Description.
- Related requirement IDs.
- Architecture component.
- Dependencies.
- Priority.
- Completion criteria.
- Verification approach.
- Status.

Keep tasks small, actionable, and verifiable.

## Step 7: Establish Dependencies

1. Identify prerequisite tasks.
2. Reference dependency task IDs.
3. Verify that all referenced task IDs exist.
4. Avoid circular dependencies.
5. Identify blocked tasks.
6. Explain why a task is blocked.
7. Establish a logical implementation order.

## Step 8: Assign Priorities

Use:

- P0 - Critical.
- P1 - High.
- P2 - Medium.
- P3 - Low.

Justify priorities based on requirements, dependencies, or documented risks.

Do not invent delivery dates or estimates.

## Step 9: Define Completion and Verification Criteria

For every task, specify:

- Observable completion criteria.
- Relevant tests or verification activities.
- Expected evidence of completion.

Consider unit, integration, API, UI, security, and documentation tests where relevant to the task.

Align verification with approved acceptance criteria.

## Step 10: Maintain Requirement Traceability

Maintain:

`Requirement -> Architecture Component -> Implementation Task -> Verification`

Identify:

- Requirements without implementation tasks.
- Tasks without requirement or architecture justification.
- Architecture components without planned work.
- Tasks without verification criteria.
- Unresolved dependencies.

Explain intentional exclusions.

## Step 11: Identify Risks and Blockers

Document:

- Unresolved design review findings.
- Pending technical decisions.
- External dependencies.
- Access requirements.
- Environment dependencies.
- Integration risks.
- Blocked tasks.

Clearly distinguish confirmed blockers from assumptions.

## Step 12: Validate the Plan

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
12. Implementation sequence.

Report gaps instead of inventing missing information.

## Step 13: Prepare Implementation Plan

Prepare the complete `docs/impl-plan.md` content.

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

Present the complete plan to the user.

Do not create the file yet.

## Step 14: Obtain Explicit Approval

Create or modify the implementation plan only after the user explicitly types:

`Create File`

General confirmations such as "looks good" or "continue" do not authorize file creation.

## Step 15: Create Implementation Plan

After receiving `Create File`:

1. Use the supplied workflow artifact directory.
2. Otherwise use `docs/impl-plan.md`.
3. Preserve original requirement IDs.
4. Verify task IDs and dependencies.
5. Document blocked tasks.
6. Include completion and verification criteria.
7. Record assumptions and open decisions.
8. Do not write application source code.
9. Do not modify unrelated files.
10. Do not commit or push changes.

## Step 16: Report Completion

After creating the file, report:

- Created file path.
- Total task count.
- Workstreams.
- Priority distribution.
- Dependencies.
- Blocked tasks.
- Open decisions.
- Recommended next action.

Hand off the implementation plan to the Developer or Orchestrator.

Do not automatically start development.

## Boundaries

- Do not modify approved requirements.
- Do not redesign architecture.
- Do not override design review findings.
- Do not write application code.
- Do not execute implementation tasks.
- Do not commit, push, merge, or create pull requests.
- Do not automatically start development.