## Summary
Adds a deterministic documentation generator for local and GitHub repositories, a push-to-main documentation sync workflow, and automated verification. Reference: EPMCDMETST-72247 (Jira search returned no result).

## Changes Made
- `.github/agents/pr-writer.agent.md` — adds an agent for writing fact-based PR metadata from repository history, documentation, and test evidence.
- `.github/prompts/create-pr.prompt.md` — adds the prompt/workflow for preparing PR metadata, including required sections and reviewer checklist.
- `.github/workflows/doc-sync.yml` — runs the generator on pushes to `main` using Python 3.11 and commits/pushes the generated document only when it changes.
- `CHANGELOG.md` — adds an Unreleased entry scoped to this branch's documentation-generator work.
- `README.md` — documents requirements, installation, local and GitHub usage, output options, and generated sections.
- `docs/PROJECT_DOC.md` — refreshes the generated project overview with current repository metadata.
- `docs/architecture.md` — documents the CLI, local/GitHub scanners, renderer, workflow, data rules, and error/security handling.
- `docs/code-review.md` — records the implementation review scope, resolved findings, checklist, and acceptance.
- `docs/design-review.md` — updates the design findings, requirement coverage, and GitHub output-path decision.
- `docs/impl-plan.md` — replaces the prior plan with implementation tasks for local scanning, GitHub scanning, workflow, and verification.
- `docs/pr-description.md` — prepares this branch's PR metadata.
- `docs/requirements.md` — specifies the generator's scope, functional requirements, acceptance criteria, and clarification log.
- `docs/test-output.txt` — records the full pytest and coverage output for this branch.
- `docs/verification-report.md` — records test and acceptance evidence plus verification limitations.
- `requirements.txt` — adds `httpx==0.28.1` for the FastAPI TestClient test dependency.
- `src/doc_sync/generator.py` — adds/extends local and GitHub repository scanning, CLI validation, deterministic rendering, output writing, error handling, and sanitization.
- `tests/test_doc_sync.py` — expands automated coverage for local and mocked GitHub cases, missing data, failures, sanitization, and deterministic output.

## Test Evidence
The run used Python 3.13 because Python 3.11 is not installed locally; the GitHub Actions workflow targets Python 3.11. GitHub API tests use mocks. No live API call or Action push was performed. Full output from `docs/test-output.txt`:

```text
....................................                                     [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\starlette\testclient.py:40
  <WORKSPACE>\.venv\Lib\site-packages\starlette\testclient.py:40: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = typing.Callable[[], typing.ContextManager[anyio.abc.BlockingPortal]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

---------- coverage: platform win32, python 3.13.0-final-0 -----------
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
src\__init__.py                 0      0   100%
src\app.py                     12      0   100%
src\doc_sync\__init__.py        2      0   100%
src\doc_sync\__main__.py        3      0   100%
src\doc_sync\generator.py     345     43    88%   83-84, 147, 173, 193-194, 224-225, 254, 256, 258, 269, 284, 295, 321, 323, 357-358, 367, 371-372, 380, 384-386, 429, 435, 439, 444-445, 470, 477, 479, 484, 488, 493, 535, 562, 564, 621-626, 633
---------------------------------------------------------
TOTAL                         362     43    88%

36 passed, 1 warning in 10.04s
```

## Known Limitations
- Jira search for `EPMCDMETST-72247` returned no result; it is included only as a plain reference, with no issue details inferred.
- GitHub API behavior was tested with mocked responses only; no live API call or GitHub Actions push was performed.
- Local verification used Python 3.13 because Python 3.11 is not installed; the workflow targets Python 3.11.
- Missing repository values are represented as `Not Found`; generated documentation reports available repository facts rather than inferring missing ones.
- Secret filtering covers recognized credential patterns and absolute paths; arbitrary unlabelled secret-like text may not be distinguishable from legitimate content.
- `pip-audit -r requirements.txt` found 20 known advisories across the pinned `pytest`, `requests`, and transitive `starlette` versions; dependency upgrades are outside this documentation-sync change.
- Generating API reference documentation, supporting repository hosts other than GitHub, and providing a web interface are out of scope.

## Reviewer Checklist
- [ ] Requirements in `docs/requirements.md` are met
- [ ] No secrets or tokens in code, tests, or docs
- [ ] Errors, missing files, and empty repos are handled
- [ ] Tests pass and cover Not Found / missing-field cases
- [ ] Dependencies have no known vulnerabilities (`pip-audit`)
- [ ] Generated `PROJECT_DOC.md` has all sections
- [ ] `CHANGELOG.md` updated
