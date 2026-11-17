# Implementation Plan: CSV Validator for Customer Uploads

Approved implementation plan. Task status is updated after implementation
and validation. Tasks use Python 3.11 and the standard library only. The
command is `python -m src.csv_check <csv-path>` and the report destination is
`reports/csv_report.md` relative to the current working directory.

## Ordered Tasks

### CV-01 — Implement CSV input and header validation

- **Status:** Done
- **Description:** Add the input/header portion of the validation flow using
  BOM-aware UTF-8 decoding and CSV newline handling. Normalize headers by
  trimming whitespace, compare required names case-sensitively, find all
  missing required columns, and detect duplicates after trimming. Treat an
  empty file and a header-only file as no-data failures. Add focused standard
  library tests for these cases, including BOM and header normalization.
- **Requirement IDs:** FR-2, FR-4, FR-7, FR-9, NFR-1, NFR-2, NFR-4
- **Acceptance criteria:**
  - `id`, `email`, and `amount` are required; all missing names and duplicate
    trimmed names are identified.
  - Header comparison remains case-sensitive and an initial UTF-8 BOM is
    handled.
  - Empty and header-only input are represented as `FAIL: no data rows`.
  - Tests cover each required header missing, duplicates, trimming, case,
    BOM, and no-data inputs.
- **Priority:** P1
- **Blocked by:** None
- **Validation command:** `py -m pytest tests/test_csv_check.py`

### CV-02 — Implement data-row checks and email privacy policy

- **Status:** Done
- **Description:** Add streaming checks for complete data rows: count records,
  flag IDs with zero characters without trimming them, and validate email
  values using the approved stripped-value policy (exactly one `@`, nonempty
  local/domain, no whitespace, and a dot in the domain). Leave amount values
  unchecked. Mask report-bound email details by retaining only the first
  local-part character and domain when safe; otherwise use `[invalid email]`.
  Add focused unit tests for each rule and masking behavior.
- **Requirement IDs:** FR-3, FR-5, FR-5a, FR-6, FR-11, NFR-2, NFR-4
- **Acceptance criteria:**
  - Findings use 1-based data-record numbering and complete rows contribute
    to the count.
  - Email rules match the specified practical policy; surrounding whitespace
    is stripped for validation.
  - Safe email details are masked and unsafe values are represented only as
    `[invalid email]`; full input addresses are absent from report-bound
    details.
  - Amount contents, including nonnumeric values, do not cause failure.
  - Tests cover empty IDs, valid/invalid email cases, masking fallback, and
    amount values.
- **Priority:** P1
- **Blocked by:** CV-01
- **Validation command:** `py -m pytest tests/test_csv_check.py`

### CV-03 — Handle malformed records and row-width mismatches

- **Status:** Done
- **Description:** Enable strict CSV parsing and validate each data record's
  field count against the header width. Stop on the first `csv.Error` or
  width mismatch, retaining earlier findings and reporting the failing
  1-based data-record number and preceding complete-record count. Add focused
  tests for malformed headers/records, width mismatch, and stop/count
  behavior, including a quoted multiline logical record.
- **Requirement IDs:** FR-8, FR-9, NFR-2, NFR-4
- **Acceptance criteria:**
  - Parsing is strict; malformed header syntax is a validation failure with
    no data-record number.
  - The first malformed data record or width mismatch ends processing.
  - The failure identifies the data-record number and number of preceding
    complete, width-correct records; the bad record is not counted.
  - Earlier row findings remain present and logical CSV records, not physical
    lines, determine row numbers.
  - Tests verify each behavior and that later records are not processed.
- **Priority:** P1
- **Blocked by:** CV-01, CV-02
- **Validation command:** `py -m pytest tests/test_csv_check.py`

### CV-04 — Render deterministic validation reports

- **Status:** Done
- **Description:** Render the validation result as concise deterministic
  Markdown with PASS/FAIL status, complete data-row count, applicable
  findings, and row/column identifiers. Include structural failure counts
  from CV-03 and ensure email details are masked before they enter the
  rendered text. Add report-focused tests, including a privacy assertion that
  raw addresses do not appear.
- **Requirement IDs:** FR-3, FR-4, FR-5, FR-6, FR-7, FR-8, FR-11, NFR-4
- **Acceptance criteria:**
  - PASS is possible only for a nonempty file without validation findings;
    validation failures name applicable missing columns and row findings.
  - Empty/header-only inputs render `FAIL: no data rows`.
  - Structural failures show the failing record and preceding complete count.
  - Rendered reports are deterministic and never contain unmasked email
    input values.
  - Tests cover PASS, each principal failure category, and email privacy.
- **Priority:** P1
- **Blocked by:** CV-01, CV-02, CV-03
- **Validation command:** `py -m pytest tests/test_csv_check.py`

### CV-05 — Add CLI invocation and successful report output

- **Status:** Done
- **Description:** Implement the `src.csv_check` module entry point with one
  required CSV path. Connect validation and rendering, write UTF-8 report
  text to `reports/csv_report.md` relative to cwd (creating directories and
  replacing prior content), and print identical text only after a successful
  write. Add CLI tests for the exact module invocation, PASS/FAIL status
  codes, report creation/overwrite, and stdout/report identity.
- **Requirement IDs:** FR-1, FR-1a, FR-3, FR-9, FR-10, AC1, AC8, AC10, NFR-1,
  NFR-2, NFR-4
- **Acceptance criteria:**
  - `python -m src.csv_check <csv-path>` accepts the required path.
  - A successful validation returns 0; a completed validation failure
    returns 1.
  - Report directory creation and overwrite work relative to the process cwd.
  - On successful writing, stdout is identical to the saved report.
  - Tests exercise invocation, status codes, output equality, directory
    creation, and overwrite.
- **Priority:** P1
- **Blocked by:** CV-04
- **Validation command:** `py -m pytest tests/test_csv_check.py`

### CV-06 — Cover operational and report-writing failures

- **Status:** Done
- **Description:** Complete CLI error handling for missing/unreadable paths,
  invalid UTF-8 or input read errors, missing arguments, and report directory
  creation/write failures. Add focused tests for stderr, stdout, and exit
  status behavior.
- **Requirement IDs:** FR-1, FR-9, FR-10, AC5, AC10, NFR-4
- **Acceptance criteria:**
  - Usage, input, and report I/O errors return 2 with a clear stderr
    diagnostic.
  - Input/usage errors do not produce a validation report.
  - If report writing fails, stdout contains no report or success-shaped
    output and stderr does not claim that the report was saved.
  - Tests cover missing argument, nonexistent input, invalid/unreadable
    input where portable, and report-write failure.
- **Priority:** P1
- **Blocked by:** CV-05
- **Validation command:** `py -m pytest tests/test_csv_check.py`

### CV-07 — Add bounded 10,000-row performance test

- **Status:** Done
- **Description:** Add a standard-library performance test that generates a
  valid 10,000-row CSV before timing. Measure reading, parsing, validation,
  and report rendering, and assert completion in under 2 seconds. Keep
  fixture generation outside the timed interval and document the focused
  command.
- **Requirement IDs:** NFR-3, NFR-4, AC9
- **Acceptance criteria:**
  - The test fixture contains 10,000 data records and is created before the
    timer starts.
  - The timed operation includes input reading, CSV parsing, validation, and
    report rendering, and completes in under 2 seconds on a normal local run.
  - The test is separately runnable and does not add a third-party
    dependency.
- **Priority:** P2
- **Blocked by:** CV-05
- **Validation command:** `py -m pytest tests/test_csv_check_performance.py`

### CV-08 — Resolve accepted empty-file review finding

- **Status:** Done
- **Description:** Suppress missing-column findings when an empty file has no
  header record or when a malformed header could not be parsed. Preserve
  missing-column findings for a parsed header that omits required columns.
- **Requirement IDs:** FR-4, FR-7, AC2, AC4
- **Acceptance criteria:**
  - An empty file reports `FAIL: no data rows` without listing missing
    columns.
  - A malformed, unparsed header reports a structural failure without
    claiming each required column is missing.
  - A nonempty parsed header that omits required columns still names them.
  - Focused regression tests pass.
- **Priority:** P1
- **Blocked by:** CV-07
- **Validation command:** `py -m pytest tests/test_csv_check.py`

## Final Validation

After all tasks are complete, run the focused performance test above and the
full standard-library test suite:

```text
py -m pytest
```

No GitHub Action is included; the approved requirements do not require one.
