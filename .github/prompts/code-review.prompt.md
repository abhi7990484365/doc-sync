---
description: Review the implementation against the 7-point checklist before creating the PR.
agent: reviewer
---

Workflow artifact directory: ${input:workflowDir:optional workflow artifact directory; leave blank to use docs/}

Review all code in `src/` and `tests/` against `requirements.md` in the
supplied workflow artifact directory, or `docs/requirements.md` if no
directory was supplied.
Check each area below and give a verdict of Pass / Issues found for each.

| Area | Question |
|---|---|
| Correctness | Does each component behave as specified in requirements.md? |
| Security | Are secrets excluded from output? Is user input validated? |
| Error Handling | Are all API failures, missing files, and empty repos handled gracefully? |
| Test Coverage | Do tests cover the happy path AND the "Not Found" / missing-field edge cases? |
| Code Clarity | Are function names self-explanatory? Is the logic easy to follow without comments? |
| DRY Principle | Is there duplicated logic that could be refactored into a shared function? |
| Dependency Safety | Are any package versions known to be vulnerable? |

For each issue give: ID, severity (High/Medium/Low), file and line, problem,
and a suggested fix. Cite requirement IDs where relevant.
Do not edit any files. End by asking me to Accept, Reject, or Defer each issue.