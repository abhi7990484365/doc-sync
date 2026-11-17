---
description: Run the complete project workflow through approval-gated pull request publication.
agent: orchestrator
---

User story:
${input:userStory:paste the user story}

Requirement:
${input:requirementText:paste the requirement text}

Run the complete sequential workflow, including the final PR-writer stage
after successful verification. Pass artifacts between stages without asking
the user to re-enter completed outputs. Keep all existing clarification,
file-write, review-decision, and implementation-task approvals. Also obtain
separate approval before commit, push, and PR creation/update. Do not skip
stages or start dependent work before its required artifacts and approvals
exist. Never merge a PR automatically.
