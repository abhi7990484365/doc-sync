---
description: Break architecture.md into a dependency-ordered implementation plan.
agent: planner
---

Read `docs/architecture.md`, `docs/design-review.md`, and `docs/requirements.md`.

Create `docs/impl-plan.md` with this structure:

# Implementation Plan
## 1. Task Summary  (total tasks, and a one-line build order)
## 2. Task List  (table: ID | Title | Priority | Requirements | Blocked by | Status)
## 3. Task Details  (for each task: description, acceptance criteria, tests needed)
## 4. Dependency Order  (a Mermaid flow diagram of task dependencies)
## 5. Blocked Tasks  (which tasks cannot start until another finishes, and why)
## 6. Definition of Done  (tests pass, no secrets, "Not Found" rule followed, reviewed)

Start with project setup, then the core components in dependency order,
then tests and the GitHub Action. Set every Status to "To Do".
Keep it simple. No code. Write the file to disk when done.