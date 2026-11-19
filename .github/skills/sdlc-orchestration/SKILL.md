
---
name: sdlc-orchestration
description: Coordinate the eight Doc-Sync SDLC phases, specialist agents, artifact handoffs, approval gates, implementation feedback loops, and GitHub PR workflow.
---

# Doc-Sync SDLC Orchestration Skill

## Objective

Coordinate the complete Doc-Sync workflow using specialist agents and repository artifacts.

The Orchestrator ensures that every phase receives the required inputs, produces its expected outputs, and satisfies its approval gates before the next phase begins.

## Phase 1: Requirements

**Agent:** analyst

### Input
- User story or business requirements.
- Available source material, such as Jira, Confluence, Word, or user-provided content.

### Expected output
- `docs/requirements.md`

### Validation
- Requirements are classified as Confirmed, Assumption, Not Found, or Open.
- Functional requirements and non-functional requirements are identifiable.
- Acceptance criteria are testable.
- Requirement traceability is available.
- User approval is recorded.

Do not proceed to Architecture until requirements are approved.

## Phase 2: Architecture

**Agent:** architect

### Input
- Approved `docs/requirements.md`

### Expected output
- `docs/architecture.md`

### Validation
- Architecture addresses approved requirements.
- Components and data flows are documented.
- Technical decisions and open questions are recorded.
- Security considerations and trust boundaries are addressed where applicable.
- Architecture is ready for independent review.
- User approval is obtained before Design Review.

## Phase 3: Design Review

**Agent:** design reviewer

### Input
- `docs/requirements.md`
- `docs/architecture.md`

### Expected output
- `docs/design-review.md`

### Outcome handling

| Outcome | Orchestrator action |
|---|---|
| Approved | Continue to Planning |
| Approved with Conditions | Track conditions and obtain required acceptance |
| Changes Required | Return findings to Architect and repeat review |
| Unable to Complete | Stop and resolve missing information |

The Design Reviewer must remain independent of the Architect.

## Phase 4: Implementation Planning

**Agent:** planner

### Input
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`

### Expected output
- `docs/impl-plan.md`

### Validation
- Tasks have unique IDs.
- Dependencies are identified.
- Priorities are assigned.
- Completion criteria are testable.
- Requirement-to-task traceability exists.
- Design review conditions are addressed.

Obtain user approval before implementation begins.

## Phase 5: Implementation

**Agent:** developer

### Input
- Approved requirements.
- Approved architecture.
- Accepted design review.
- Approved implementation plan.

### Execution
- Select one task ID.
- Verify dependencies.
- Inspect the existing repository.
- Implement only the selected task.
- Add or update relevant tests.
- Execute applicable checks.
- Report actual implementation evidence.

### Validation
- Confirm the selected task's changes exist.
- Confirm actual test execution results.
- Confirm scope matches the approved task.

Do not automatically start the next task.

The user must select or authorize the next implementation task.

## Phase 6: Code Review

**Agent:** code reviewer

### Input
- Actual implementation changes.
- Approved requirements.
- Architecture.
- Design review.
- Implementation plan.

### Expected output
- `docs/code-review.md`

### Outcome handling

| Outcome | Orchestrator action |
|---|---|
| Approved | Continue to Verification |
| Approved with Conditions | Track conditions and determine whether they permit verification |
| Changes Required | Return findings to Developer and repeat review |
| Unable to Complete | Stop and resolve blockers |

Unresolved Critical or High findings prevent progression to final verification.

## Phase 7: Verification

**Agent:** tester

### Input
- Approved implementation changes.
- Requirements and acceptance criteria.
- Architecture and design review.
- Implementation plan.
- Code review findings and outcome.

### Expected output
- `docs/test-report.md`

### Verification scope

Where applicable, verify:
- Unit tests.
- Integration tests.
- Regression tests.
- API or UI behavior.
- Security-related behavior.
- Documentation content and quality.

### Outcome handling

| Outcome | Orchestrator action |
|---|---|
| Passed | Continue to PR |
| Passed with Limitations | Record limitations and assess release readiness |
| Failed | Return failures to Developer, then repeat review and testing |
| Blocked | Stop and report blockers |

After Developer fixes, repeat Code Review before relevant retesting.

## Phase 8: Pull Request

**Agent:**  pr-writer

### Input
- Approved requirements.
- Architecture.
- Design review.
- Implementation plan.
- Code review.
- Test report.
- Actual source changes and Git information.

### Expected output
- `docs/pull-request.md`
- Git commit.
- Pushed feature branch.
- GitHub Pull Request URL.

### Validation
- Required review and test gates are satisfied.
- Only approved files are committed.
- Feature branch is pushed successfully.
- PR contains all required sections.
- PR URL is verified.

The PR Writer workflow must be explicitly started. Its defined authorization permits committing approved changes, pushing the feature branch, and creating the PR.

Merging is not included.

## Feedback Loops

### Architecture correction loop

design reviewer -> architect -> design reviewer.

Repeat until the architecture review is acceptable.

### Code correction loop

code reviewer -> developer -> code reviewer.

Repeat until code review is acceptable.

### Test failure loop

tester -> developer -> code reviewer -> tester.

Repeat relevant checks after changes.

Do not bypass these loops.

## Handoff Protocol

For each handoff, provide:

1. Current phase.
2. Previous agent's outcome.
3. Required input artifact paths.
4. Relevant task, requirement, and finding IDs.
5. Expected output artifact.
6. Approval or authorization requirements.

Verify the actual output before advancing.

## Execution Modes

### Guided mode

Execute one phase at a time and wait for user approval at required gates.

### Phase continuation

Continue from a specified phase only after verifying all prerequisite artifacts and approvals.

### Status mode

Inspect existing artifacts and report workflow progress without modifying files.

Do not assume that full autonomous execution is enabled merely because the Orchestrator is started.

## Final Status

Report:

- Phase status.
- Completed agents.
- Generated artifacts.
- Pending approvals.
- Open findings.
- Blockers.
- Next permitted action.
