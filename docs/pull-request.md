# Pull Request

## Summary

This change completes TASK-005 for DOC-001 by adding the approved FastAPI/Uvicorn runtime and fail-closed validation of the configured local store path. It preserves the scanner CLI and rejects detectable UNC and remote-drive paths without claiming that unknown mounted network filesystems can be detected.

## Changes Made

- Added the FastAPI application lifespan and Uvicorn entry point, configured for one worker on `127.0.0.1:8000` with reload disabled.
- Added pinned `uvicorn==0.30.6`.
- Validated `DOC_SYNC_STORE_PATH` at startup; reject unset, relative, missing, non-file, UNC, and detectable Windows remote-drive paths.
- Added startup/configuration and scanner-independence tests, including unknown and local Windows drive-type cases.
- **Traceability:** DOC-001 FR-001–FR-006 -> HTTP/API layer and application runtime -> TASK-005 -> `src/doc_sync_api.py` and `tests/test_doc_sync_api.py`.

## Test Evidence

- `python -m pytest tests/test_doc_sync_api.py` — **15 passed**, 1 warning, 1.09s.
- `python -m pytest` — **15 passed**, 1 warning, 0.93s.
- Both runs reported a Starlette/AnyIO `BlockingPortal` deprecation warning. The warning did not fail the tests.
- Evidence is recorded in [`test-report.md`](./test-report.md).

## Known Limitations

- UNC/mapped remote-drive rejection was not exercised against a real remote-drive environment. Unknown mounted network filesystems may not be automatically detectable and are unsupported; operators must configure local storage.
- The test report records no separate pytest exit status, although both supplied summaries reported all 15 tests passing.
- Code review outcome: Approved with Conditions; F-001 was resolved. The review report predates the later test execution, and the exact disposition of earlier CR-001–CR-004 is not independently verifiable from the available review artifact.
- **Publication:** This document is prepared, but the PR is not published. Source branch, target branch, commit, push, and PR URL are not verified; they must be filled from actual Git/GitHub results after publication.

## Reviewer Checklist

- [ ] Confirm startup rejects unset, relative, missing, non-file, UNC, and detectable remote store paths.
- [ ] Confirm unknown mounted network filesystems are documented as unsupported and not claimed as detectable.
- [ ] Confirm Uvicorn uses one worker, loopback binding, and reload disabled.
- [ ] Confirm scanner CLI behavior remains independent.
- [ ] Review the focused and full pytest evidence and the documented warning.

## Changelog

- Added the approved loopback API runtime and fail-closed local store-path validation for TASK-005.
- Added regression coverage for detectable remote paths, unknown/local Windows drive types, and scanner independence.
