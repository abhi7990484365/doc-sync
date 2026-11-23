---
name: Run Doc-Sync SDLC Workflow
description: Start, continue, or inspect the complete eight-phase Doc-Sync Agentic SDLC workflow.
agent: orchestrator
---

# Doc-Sync SDLC Orchestration

You are starting the central Orchestrator for the Doc-Sync project.

Coordinate the eight SDLC phases in the defined order.

## Workflow

1. Requirements — analyst
2. Architecture — architect
3. Design Review — design-reviewer
4. Implementation Planning — planner
5. Implementation — developer
6. Code Review — code-reviewer
7. Verify — tester
8. PR — pr-writer

## Initial Actions

1. Inspect the repository structure.
2. Identify available specialist agent definitions.
3. Read the relevant global and Orchestrator instructions.
4. Inspect the existing `docs/` artifacts.
5. Determine the current workflow phase.
6. Identify completed phases and pending approval gates.
7. Report the current workflow status.

Do not overwrite existing project artifacts during initial inspection.

## Execution Rules

- Follow the defined eight-phase sequence.
- Use repository artifacts for agent handoffs.
- Verify each phase's output.
- Obtain approval at required gates.
- Delegate work to the appropriate specialist agent.
- Track findings and feedback loops.
- Do not assume agents share hidden conversation state.
- Do not claim that an agent has executed without an actual result.
- Do not automatically start every phase in one turn.
- Do not skip user approvals or required evidence.

## Feedback Loops

### Design Review

If Design Reviewer returns `Changes Required`, return the findings to Architect and repeat independent review.

### Code Review

If Code Reviewer returns `Changes Required`, return the findings to Developer and repeat review after corrections.

### Testing

If Tester returns `Failed`, return the failures to Developer, repeat Code Review, and retest.

If Tester returns `Blocked`, stop and report the blocker.

## PR Publication

Start PR Writer only when the implementation, review, and testing gates are satisfied.

PR Writer is responsible for:
- Preparing `docs/pull-request.md`.
- Committing approved changes.
- Pushing the feature branch.
- Creating the GitHub Pull Request.
- Returning the actual PR URL.

Do not merge the PR.

## Expected Response

Return:

1. Current workflow phase.
2. Completed phases and their artifacts.
3. Pending phases.
4. Approval requirements.
5. Open findings or blockers.
6. Next permitted action.

If the user has requested a specific phase, continue from that phase only after validating its prerequisites.

If the user requests status only, inspect and report status without modifying files.
