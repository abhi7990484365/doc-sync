---
description: Break architecture.md into a dependency-ordered implementation plan.
agent: planner
---

Workflow artifact directory: ${input:workflowDir:optional workflow artifact directory; leave blank to use docs/}

Read `architecture.md`, `design-review.md`, and `requirements.md` from the
supplied workflow artifact directory. If no directory was supplied, use the
corresponding files in `docs/`.

Create `impl-plan.md` in the supplied workflow artifact directory, or
`docs/impl-plan.md` if no directory was supplied. Use this structure:

# Implementation Plan
## 1. Task Summary  (total tasks, and a one-line build order)
## 2. Task List  (table: ID | Title | Priority | Requirements | Blocked by | Status)
## 3. Task Details  (for each task: description, acceptance criteria, tests needed)
## 4. Dependency Order  (a Mermaid flow diagram of task dependencies)
## 5. Blocked Tasks  (which tasks cannot start until another finishes, and why)
## 6. Definition of Done  (tests pass, no secrets, "Not Found" rule followed, reviewed)

Include project setup only if it is required by the approved requirements.
Order core components by dependency, include tests and error handling, and
include a GitHub Action only when the requirements call for one. Set every
Status to "To Do".
Keep it simple. No code. Write the file to disk when done.