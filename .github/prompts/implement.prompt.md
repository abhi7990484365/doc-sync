---
description: Implement one task from the implementation plan.
agent: developer
---

Workflow artifact directory: ${input:workflowDir:optional workflow artifact directory; leave blank to use docs/}

Implement task ${input:taskId:e.g. T-01} from `impl-plan.md` in the supplied
workflow artifact directory. If no directory was supplied, use
`docs/impl-plan.md`.

1. Confirm its blockers are Done.
2. Show me your plan and wait for "approved".
3. Implement the code and tests.
4. Run pytest and show the output.
5. Update the task Status in the same implementation plan.
6. Suggest a Conventional Commit message.