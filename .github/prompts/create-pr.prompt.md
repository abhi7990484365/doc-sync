---
description: Prepare and publish a pull request from verified, approved changes.
agent: pr-writer
---

Prepare and publish a pull request for the current feature branch. If invoked
by the orchestrator, use only its supplied workflow directory and approved
changed-file list. Otherwise use the standard project artifact paths.

1. Confirm successful verification and inspect the actual Git branch, status,
   diff, and history. Use `main` as the base unless the user supplied another
   base. Stop if the current branch is the base, the approved changed paths
   cannot be distinguished from unrelated work, authentication or `origin`
   is unavailable, or verification failed.
2. Prepare a Keep a Changelog-style `CHANGELOG.md` entry (Added / Changed /
   Fixed) based on the verified changes. Show the proposed entry and target
   path; obtain explicit user approval before writing it.
3. Prepare the PR description at `<workflow-dir>/pr-description.md` for an
   orchestrated run, or `docs/pr-description.md` for manual use. Show the
   target and obtain explicit user approval before writing. Include exactly
   these sections:

   ## Summary
   2-3 factual sentences about what was built and why. Reference a Jira key
   only if it was supplied or verified in the workflow inputs.

   ## Changes Made
   Bulleted list of every approved file added or modified for the PR,
   including `CHANGELOG.md` if changed, with the reason.

   ## Test Evidence
   Actual output and coverage from the successful verification run. Do not
   report tests that were not run.

   ## Known Limitations
   Anything "Not Found", deferred in the design/code review, or out of scope.

   ## Reviewer Checklist
   A tick-list (- [ ]) the reviewer must complete before approving:
   - [ ] Approved requirements are met
   - [ ] No secrets or tokens in code, tests, or docs
   - [ ] Errors, missing files, and empty repos are handled
   - [ ] Tests pass and cover Not Found / missing-field cases
   - [ ] Dependencies have no known vulnerabilities (pip-audit)
   - [ ] Generated PROJECT_DOC.md has all sections
   - [ ] CHANGELOG.md updated

4. Show the exact Conventional Commit message and approved paths. Obtain
   explicit approval before committing. Stage only those paths; never use
   `git add .` or `git add -A`.
5. Show the branch and `origin` target. Obtain separate explicit approval
   before pushing. Never push the base branch or force-push.
6. Find an existing open PR with the same head and base. If exactly one
   exists, show the URL and proposed title/body and obtain approval before
   updating it. If none exists, show the title, head, base, and body and
   obtain approval before creating the PR. If multiple matches exist, stop
   for user direction. Never merge.
7. Report the commit hash, pushed branch, and PR URL. If any step fails,
   report the failure and do not claim successful publication.