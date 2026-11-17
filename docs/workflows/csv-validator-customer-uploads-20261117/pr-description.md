## Summary
Add a standard-library CSV validator for customer uploads and include its workflow records.

## Changes Made
- `src/csv_check.py` — CSV validation, email masking, deterministic reports, CLI and error handling.
- `tests/test_csv_check.py` — functional, CLI, error-handling, and privacy tests.
- `tests/test_csv_check_performance.py` — 10,000-row performance test.
- Workflow records: `requirements.md`, `architecture.md`, `design-review.md`, `impl-plan.md`, `code-review.md`, and `verification-report.md` under `docs/workflows/csv-validator-customer-uploads-20261117/`.

## Test Evidence
- Python 3.11.9: `py -m pytest` — 72 passed, 1 unrelated Starlette/AnyIO deprecation warning.
- Python 3.11.9 performance test — passed in 0.04s.
- The accepted empty-file review finding was fixed and reverified.

## Known Limitations
- Amount values are not validated; only the required `amount` column is checked.
- Email validation is a practical format check, not full RFC validation.
- Database loading, cloud storage, and other file formats are out of scope.

## Reviewer Checklist
- [ ] Confirm required columns, row findings, and structural-error behavior.
- [ ] Confirm email masking, report output, and operational error handling.
- [ ] Confirm Python 3.11.9 and 10,000-row performance evidence.
