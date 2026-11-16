---
description: Generate and run the verification suite and check the output document.
agent: tester
---

Verify the project in three parts.

## A. Unit tests
Check that each function in `src/doc_sync/` has tests for: the happy path,
"Not Found", a missing field, an empty repo, and an API failure (mocked).
Add any missing tests.

## B. Integration test
Add one test that runs the CLI end to end on a sample repo in a temp folder
and checks that `PROJECT_DOC.md` is created. Add a second one for an empty repo.

## C. Output document quality check
Write tests that check the generated `PROJECT_DOC.md`:
- All required sections are present, in order (see the doc-sync-format skill).
- Missing values are exactly `Not Found`, never blank, guessed, or invented.
- No secrets, tokens, or absolute local paths appear.
- Running twice on the same repo gives identical output.

Run: `pytest --cov=src --cov-report=term-missing`
Show me the full output.

Then create `docs/verification-report.md` with: test counts, pass/fail,
coverage percentage, any failures and their cause, and a list of known gaps.