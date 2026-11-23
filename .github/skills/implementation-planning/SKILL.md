---
name: implementation-planning
description: Turn approved Doc-Sync requirements, architecture, and design review findings into a prioritized implementation plan.
---

# Implementation Planning

## Purpose

Create a practical plan that breaks the approved design into tasks the Developer can implement and verify.

## Inputs

Use:
- Approved `docs/requirements.md`
- Approved `docs/architecture.md`
- `docs/design-review.md`
- Relevant project documentation and approved technical decisions

If a required document is missing or approval is unclear, ask before planning. Do not plan around unresolved critical design findings.

## Workflow

### 1. Review the inputs

Identify the requirements, architecture components, design review findings, constraints, and open decisions that affect implementation.

Preserve the original requirement IDs. Do not add scope or treat recommendations as approved decisions.

### 2. Create implementation tasks

Break the work into small, actionable tasks. Give each task a sequential ID, such as `TASK-001`.

Each task must include:
- Title and description
- Related requirement IDs
- Architecture component
- Dependencies
- Priority
- Completion criteria
- Verification approach
- Status

Include only work supported by the approved requirements and architecture.

### 3. Set order and priority

Identify which tasks depend on others. Reference dependency task IDs, avoid circular dependencies, and mark blocked tasks.

Use:
- **P0 — Critical:** Required prerequisite or critical functionality
- **P1 — High:** Important for planned delivery
- **P2 — Medium:** Supporting work or improvement
- **P3 — Low:** Optional work that does not block core delivery

Base priorities on requirements, dependencies, and documented risks. Do not invent owners, dates, or estimates.

### 4. Define completion and verification

For each task, state what must be true for it to be complete and how that result will be checked.

Use relevant verification such as unit, integration, API, UI, security, or documentation tests. Do not invent behavior that is not in the approved design.

### 5. Check the plan

Verify that:
- Requirements are covered or their exclusion is explained.
- Tasks align with the approved architecture.
- Dependencies are valid and tasks are in a workable order.
- Each task has completion and verification criteria.
- Design findings, risks, blockers, and open decisions are recorded.

Flag gaps rather than filling them with assumptions.

### 6. Present and create the plan

Present the plan for approval, including tasks, priorities, dependencies, traceability, verification, risks, and blockers.

Create or modify a file only after the user explicitly types:

`Create File`

After receiving that command, use the artifact path provided by the Orchestrator. If none is provided, use `docs/impl-plan.md`.

Keep the plan focused. Do not write code, modify unrelated files, or commit or push changes.

## Handoff

Give the Developer or Orchestrator the task IDs, priorities, dependencies, completion criteria, verification expectations, and any blockers.

The Developer should work only on explicitly selected and approved tasks. Do not start development automatically.

## Boundaries

- Follow approved requirements and architecture.
- Consider design review findings.
- Do not invent scope or technical constraints.
- Do not redesign architecture or change approved requirements.
- Do not execute implementation tasks or write application code.
- Do not commit, push, merge, or create pull requests.