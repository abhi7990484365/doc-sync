---
name: sdlc-orchestration
description: Coordinate the eight Doc-Sync SDLC phases, specialist agents, artifact handoffs, approval gates, implementation feedback loops, and GitHub PR workflow.
---

# Doc-Sync SDLC Orchestration Skill

## Objective

Coordinate the Doc-Sync workflow through specialist agents and repository artifacts. Verify each phase’s inputs, outputs, and required approvals before advancing.

## Phase 1: Requirements

**Agent:** analyst

**Input:** User story, business requirements, and available source material.

**Output:** `docs/requirements.md`

Verify that requirements are classified as Confirmed, Assumption, Not Found, or Open; functional and non-functional requirements are identifiable; acceptance criteria are testable; and traceability is available.

Obtain user approval before Architecture.

## Phase 2: Architecture

**Agent:** architect

**Input:** Approved `docs/requirements.md`

**Output:** `docs/architecture.md`

Verify that the architecture addresses approved requirements and documents components, data flows, technical decisions, open questions, and applicable security considerations.

Obtain user approval before Design Review.

## Phase 3: Design Review

**Agent:** design reviewer

**Input:** `docs/requirements.md`, `docs/architecture.md`

**Output:** `docs/design-review.md`

Keep the review independent of the Architect.

- **Approved:** Continue to Planning.
- **Approved with Conditions:** Track conditions and obtain any required acceptance.
- **Changes Required:** Return findings to the Architect and repeat the review.
- **Unable to Complete:** Stop and resolve missing information.

## Phase 4: Implementation Planning

**Agent:** planner

**Input:** Approved requirements, architecture, and design review.

**Output:** `docs/impl-plan.md`

Verify that tasks have unique IDs, priorities, dependencies, testable completion criteria, requirement traceability, and coverage of design review conditions.

Obtain user approval before implementation.

## Phase 5: Implementation

**Agent:** developer

**Input:** Approved requirements, architecture, design review, and implementation plan.

For each authorized task:

1. Confirm the selected task ID and its dependencies.
2. Inspect the repository.
3. Implement only the selected task.
4. Add or update relevant tests and run applicable checks.
5. Report the changes and actual test evidence.

Verify that the changes match the approved task and its scope. Do not start another task automatically; the user must select or authorize it.

## Phase 6: Code Review

**Agent:** code reviewer

**Input:** Actual changes and the approved requirements, architecture, design review, and implementation plan.

**Output:** `docs/code-review.md`

- **Approved:** Continue to Verification.
- **Approved with Conditions:** Track conditions and determine whether verification can proceed.
- **Changes Required:** Return findings to the Developer and repeat review.
- **Unable to Complete:** Stop and resolve blockers.

Unresolved Critical or High findings block final verification.

## Phase 7: Verification

**Agent:** tester

**Input:** Approved implementation, requirements, architecture, design review, implementation plan, and code review.

**Output:** `docs/test-report.md`

Verify applicable unit, integration, regression, API/UI, security-related, and documentation behavior.

- **Passed:** Continue to PR.
- **Passed with Limitations:** Document limitations and assess readiness.
- **Failed:** Return failures to the Developer, then repeat Code Review and relevant testing.
- **Blocked:** Stop and report blockers.

After a code change, repeat Code Review before relevant retesting.

## Phase 8: Pull Request

**Agent:** pr-writer

**Input:** Approved artifacts, actual source changes, and Git information.

**Output:** `docs/pull-request.md`, commit, pushed feature branch, and verified GitHub PR URL.

Verify that review and test gates are satisfied, only approved files are committed, the branch is pushed, and the PR contains the required sections.

The PR Writer workflow must be explicitly started. It may commit approved changes, push the feature branch, and create the PR. It must not merge the PR.

## Feedback Loops

- **Architecture:** Design Reviewer → Architect → Design Reviewer
- **Code:** Code Reviewer → Developer → Code Reviewer
- **Testing:** Tester → Developer → Code Reviewer → Tester

Repeat the relevant loop until its gate is satisfied. Do not bypass review or testing.

## Handoff Protocol

For each handoff, provide:

1. Current phase and previous outcome
2. Required input artifact paths
3. Relevant task, requirement, and finding IDs
4. Expected output artifact
5. Required approval or authorization

Verify the actual output before advancing.

## Execution Modes

- **Guided:** Run one phase at a time and wait at approval gates.
- **Phase continuation:** Resume from a specified phase only after verifying prerequisite artifacts and approvals.
- **Status:** Inspect artifacts and report progress without modifying files.

Starting the Orchestrator does not authorize fully autonomous execution.

## Final Status

Report phase status, completed agents, generated artifacts, pending approvals, open findings, blockers, and the next permitted action.