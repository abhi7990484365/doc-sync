# Verification Report: CSV Validator for Customer Uploads

**Verification date:** 2026-11-17  
**Scope:** Verification only; no production or test code was changed.  
**Environment:** Windows; final verification ran with Python 3.11.9 and
pytest 8.3.3. Earlier runs used Python 3.13.0.

## Result

- Functional requirements and acceptance cases exercised below: **PASS**.
- Full suite: **72 passed**.
- Focused 10,000-row performance test: **PASS**.
- Standard-library-only validator implementation: **PASS** by source/import
  inspection.
- Python 3.11 runtime compatibility (NFR-1): **PASS**. The full suite and
  focused performance test passed on Python 3.11.9.
- The accepted code-review finding is **RESOLVED**: an empty file now reports
  `FAIL: no data rows` without listing missing columns. Header-only input has
  the same no-data behavior; a parsed header that lacks a required column
  still reports that missing column.

## Test evidence

### Full suite

Command:

```text
py -m pytest
```

Actual output:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.0, pytest-8.3.3, pluggy-1.7.0
rootdir: C:\Users\AbhiVijaybhaiVachhan\doc-sync
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.16.0, cov-5.0.0
collected 72 items

tests\test_app.py ....                                                   [  5%]
tests\test_csv_check.py ...................................              [ 54%]
tests\test_csv_check_performance.py .                                    [ 55%]
tests\test_doc_sync.py ................................                  [100%]

============================== warnings summary ===============================
..\AppData\Roaming\Python\Python313\site-packages\starlette\testclient.py:40
  C:\Users\AbhiVijaybhaiVachhan\AppData\Roaming\Python\Python313\site-packages\starlette\testclient.py:40: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = typing.Callable[[], typing.ContextManager[typing.Any]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 72 passed, 1 warning in 5.25s ========================
```

### Focused performance test

Command:

```text
py -m pytest tests/test_csv_check_performance.py -q
```

Actual output:

```text
.                                                                        [100%]
1 passed in 0.06s
```

The test creates its 10,000-row fixture before timing and times header read,
row parsing/validation, and report rendering.

### Python 3.11.9 verification

The Python 3.11.9 runtime was installed and configured in an isolated
temporary virtual environment. The repository's declared test dependencies
were installed there without changing `requirements.txt`.

- Full suite: **72 passed**, 1 unrelated Starlette/AnyIO deprecation warning
  in 7.33 seconds.
- Focused performance test: **1 passed** in 0.04 seconds.
- Command: `python -m pytest`, run with the configured Python 3.11.9
  interpreter.

## Requirement and acceptance traceability

Each entry associates the named test(s) with the requirement IDs exercised.
The test names refer to `tests/test_csv_check.py` unless noted.

| Requirement IDs | Test evidence |
| --- | --- |
| FR-1, FR-1a, AC10 | `test_cli_valid_file_writes_and_prints_identical_report`; `test_cli_missing_argument_returns_usage_error_without_report` |
| FR-2, FR-4, AC2 | `test_read_csv_header_reports_each_missing_required_column`; `test_read_csv_header_reports_duplicate_names_after_trimming`; `test_read_csv_header_trims_surrounding_whitespace`; `test_read_csv_header_compares_names_case_sensitively`; `test_read_csv_header_handles_utf8_bom`; `test_render_report_lists_missing_columns_and_row_findings` |
| FR-3, AC1 | `test_render_report_is_deterministic_for_valid_csv`; `test_cli_valid_file_writes_and_prints_identical_report` (PASS and exact row count) |
| FR-5, AC3 | `test_validate_csv_rows_counts_records_and_reports_row_findings`; `test_cli_validation_failure_returns_nonzero_and_masks_email` |
| FR-5a | `test_is_valid_email_uses_practical_format_check` |
| FR-6, FR-11, AC6 | `test_mask_email_hides_local_part_and_unsafe_values`; `test_validate_csv_rows_counts_records_and_reports_row_findings`; `test_render_report_is_deterministic_for_valid_csv`; `test_render_report_lists_missing_columns_and_row_findings`; `test_cli_validation_failure_returns_nonzero_and_masks_email` |
| FR-7, AC4 | `test_read_csv_header_detects_empty_and_header_only_files`; `test_render_report_marks_no_data_files_as_failure` |
| FR-8, AC7 | `test_validate_csv_rows_reports_malformed_header_without_data_record_number`; `test_validate_csv_rows_stops_on_malformed_record_and_keeps_findings`; `test_validate_csv_rows_stops_at_width_mismatch_and_does_not_count_it`; `test_validate_csv_rows_numbers_quoted_multiline_records_logically`; `test_render_report_includes_structural_failure_count`; `test_read_csv_header_reports_duplicate_names_after_trimming` |
| FR-9, AC5, AC10 | `test_cli_missing_argument_returns_usage_error_without_report`; `test_cli_missing_input_returns_clear_error_without_exposing_path`; `test_cli_invalid_utf8_returns_read_error_without_report`; `test_cli_validation_failure_returns_nonzero_and_masks_email`; `test_cli_valid_file_writes_and_prints_identical_report` |
| FR-10, AC8 | `test_cli_valid_file_writes_and_prints_identical_report`; `test_cli_overwrites_existing_report`; `test_cli_report_write_failure_does_not_print_report` |
| NFR-1 | Full test suite and focused performance test passed on Python 3.11.9. |
| NFR-2, AC9 | `src/csv_check.py` imports `argparse`, `csv`, `sys`, `dataclasses`, and `pathlib`; all are Python standard-library modules. No third-party runtime import is present. |
| NFR-3, AC9 | `tests/test_csv_check_performance.py::test_validates_and_renders_10000_csv_rows_in_under_two_seconds`; focused test passed. |
| NFR-4 | Full suite result above; 72 tests passed. |

## Additional isolated CLI checks

The exact module invocation was exercised in temporary workspaces, with no
live API calls or tokens. The final assertion-checked run printed:

```text
Runtime: 3.13.0
CLI PASS: exit=0; report contains PASS and Rows: 2; stdout equals report file
CLI FAIL findings: exit=1; empty ID row 1, invalid email row 2; raw addresses absent and invalid email masked
CLI missing column: exit=1; names amount
CLI empty file: exit=1; FAIL: no data rows; no missing-column diagnostic
CLI header-only: exit=1; FAIL: no data rows; Rows: 0
CLI parsed header missing amount: exit=1; FAIL; reports Missing required columns: amount
CLI structural failures: duplicate header, malformed record and width mismatch all exit=1; first error/count reported
CLI missing path: exit=2; clear stderr; no stdout report
CLI report overwrite: prior contents replaced; stdout equals saved report
Implementation imports: argparse, csv, sys, dataclasses, pathlib (standard library only)
```

Final supplemental checks used temporary workspaces and no live API calls or
tokens. The real output for the empty, header-only, and parsed-header/missing-
column checks was:

```text
CASE empty: exit=1
REPORT:
# CSV Validation Report

FAIL: no data rows
Rows: 0
ASSERTIONS: PASS

CASE header_only: exit=1
REPORT:
# CSV Validation Report

FAIL: no data rows
Rows: 0
ASSERTIONS: PASS

CASE parsed_missing_column: exit=1
REPORT:
# CSV Validation Report

FAIL
Rows: Not Counted

Missing required columns: amount
ASSERTIONS: PASS

Runtime: 3.13.0
```

In each case CLI stdout matched the report written in the temporary working
directory. The suite's one warning is an unrelated Starlette/AnyIO deprecation
warning.

## Final status

The accepted empty-file code-review finding is resolved and verified. NFR-1
is verified on Python 3.11.9. No PR/publication stage was started.
