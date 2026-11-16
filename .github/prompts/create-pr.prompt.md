---
description: Create the PR description, changelog entry, and reviewer checklist.
agent: pr-writer
---

Prepare the pull request for the current branch.

1. Run `git log main..HEAD --oneline` and `git diff main...HEAD --stat`.
2. Create/update `CHANGELOG.md` with a new entry (Keep a Changelog style:
   Added / Changed / Fixed) with today's date.
3. Create `docs/pr-description.md` with exactly these sections:

   ## Summary
   2-3 sentences: what was built and why. Reference the Jira key EPMCDMETST-72247.

   ## Changes Made
   Bulleted list of every file added or modified, with the reason.

   ## Test Evidence
   The real output from docs/test-output.txt, including the coverage figure.

   ## Known Limitations
   Anything "Not Found", deferred in the design/code review, or out of scope.

   ## Reviewer Checklist
   A tick-list (- [ ]) the reviewer must complete before approving:
   - [ ] Requirements in docs/requirements.md are met
   - [ ] No secrets or tokens in code, tests, or docs
   - [ ] Errors, missing files, and empty repos are handled
   - [ ] Tests pass and cover Not Found / missing-field cases
   - [ ] Dependencies have no known vulnerabilities (pip-audit)
   - [ ] Generated PROJECT_DOC.md has all sections
   - [ ] CHANGELOG.md updated

4. Show me a summary and the suggested PR title (Conventional Commit style).