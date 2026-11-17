# Requirements

## 1. User Story

As a data engineer, I want a command-line tool that checks a customer CSV
file before it is loaded, so that invalid files are caught early and do not
break the pipeline.

## 2. Goal and Scope

The `csv-check` command accepts a local CSV file path, validates the file,
prints a concise report, and writes the same report to
`reports/csv_report.md`, relative to the current working directory.
The command is invoked as `python -m src.csv_check <csv-path>`.

In scope:
- Require the `id`, `email`, and `amount` columns.
- Report whether the file passes validation and include the data-row count.
- Identify data rows with empty IDs or invalid email addresses.
- Mask email addresses in any report details, preserving only the first
  local-part character, for example `alice@example.com` as
  `a***@example.com`.
- Report missing required columns and malformed CSV structure or duplicate
  column names as failures.
- Create the report directory when needed and overwrite the report on each
  run.
- Handle a UTF-8 byte-order mark at the beginning of the file. Trim
  surrounding whitespace from header names, then compare names
  case-sensitively; duplicate names after trimming are invalid.
- On an unrecoverable malformed record or row-width mismatch, stop at the
  first error and report its 1-based data-record number and the number of
  completely parsed data records before it.
- Return exit status 0 for PASS, 1 for validation FAIL, and 2 for usage,
  input, or report I/O errors.
- If report writing fails, emit a clear error to stderr, return 2, and do not
  claim the report was saved or print a success-shaped report.

Out of scope:
- Database loading, cloud storage, and non-CSV file formats.
- Validating `amount` values beyond requiring the `amount` column.

## 3. Functional Requirements

- FR-1: The CLI shall accept a local CSV file path.
- FR-1a: The CLI shall be invokable as
  `python -m src.csv_check <csv-path>`.
- FR-2: The CSV header shall contain the required columns `id`, `email`, and
  `amount`. Header names shall be decoded with UTF-8 BOM handling, stripped
  of surrounding whitespace, and compared case-sensitively. Duplicate names
  after trimming shall be invalid.
- FR-3: A file with all required columns and no invalid data rows shall report
  `PASS` and the number of data rows.
- FR-4: Missing required columns shall report `FAIL` and name every missing
  column.
- FR-5: Rows with an empty `id` or invalid `email` shall be reported using
  1-based data-row numbering (the first record after the header is row 1).
- FR-5a: Email validation shall strip surrounding whitespace and require
  exactly one `@`, non-empty local and domain parts, no whitespace, and at
  least one dot in the domain. This is a practical check, not full RFC
  validation.
- FR-6: Email addresses included in the report shall be masked as
  `a***@example.com`; full addresses shall not be included. For a value with
  exactly one `@`, preserve the domain and only the first local-part
  character. If an invalid value cannot be safely masked, show
  `[invalid email]` instead of the input value.
- FR-7: An empty file or a file containing only a header shall report
  `FAIL: no data rows`.
- FR-8: Malformed CSV structure and duplicate header names shall report
  `FAIL`, identifying affected rows or columns when possible. Parse strictly
  and stop at the first unrecoverable malformed record or row-width mismatch.
  Report its 1-based data-record number and the number of completely parsed
  data records preceding it.
- FR-9: A path that does not exist shall produce a clear error and a non-zero
  exit code. Exit status shall be 0 for PASS, 1 for validation FAIL, and 2
  for usage, input, or report I/O errors.
- FR-10: The CLI shall print a concise report and write the report to
  `reports/csv_report.md`, relative to the current working directory. It shall
  create the parent directory if necessary and replace the prior report. If
  writing fails, it shall print a clear error to stderr, return 2, and not
  claim that the report was saved.
- FR-11: Report content shall not expose unmasked email addresses.

## 4. Non-Functional Requirements

- NFR-1: The tool shall run on Python 3.11.
- NFR-2: The implementation shall use only the Python standard library.
- NFR-3: Validation of a generated 10,000-row file shall complete in under
  2 seconds on a normal local run. Fixture setup shall be outside the timed
  interval; reading, parsing, validation, and report rendering shall be
  included.
- NFR-4: Automated tests shall cover successful validation and required
  failure cases.

## 5. Acceptance Criteria

- AC1: A valid CSV produces `PASS` and its data-row count.
- AC2: A missing required column produces `FAIL` and names the missing
  column.
- AC3: Empty IDs and invalid emails are reported by 1-based data-row number.
- AC4: An empty file or header-only file produces `FAIL: no data rows`.
- AC5: A nonexistent path produces a clear error and a non-zero exit code.
- AC6: Email addresses in the report are masked, for example
  `alice@example.com` appears as `a***@example.com`.
- AC7: Malformed CSV structure and duplicate headers produce `FAIL`.
- AC8: The report is printed and written to the specified relative path,
  creating its parent directory and replacing prior contents.
- AC9: The implementation uses only the standard library and validates
  10,000 rows in under 2 seconds.
- AC10: The command is invokable as `python -m src.csv_check <csv-path>`;
  exit status is 0 for PASS, 1 for validation FAIL, and 2 for usage, input, or
  report I/O errors.

## 6. Clarification Log

- Row numbering: 1-based data-row numbering; the header is not counted.
- Email handling: strip surrounding whitespace; require one `@`, non-empty
  local/domain parts, no whitespace, and a dotted domain; this is a practical
  check, not full RFC validation. Mask report values, using
  `[invalid email]` if an invalid value cannot be safely masked.
- Amount handling: require the column but do not validate its values.
- Header handling: remove an initial UTF-8 BOM, trim surrounding header
  whitespace, then compare case-sensitively. Duplicate trimmed headers fail.
- CSV structure: stop at the first unrecoverable malformed record or
  row-width mismatch; count only completely parsed data records before it.
- CLI status: 0 for PASS, 1 for validation FAIL, and 2 for usage, input, or
  report I/O errors.
- CLI invocation: `python -m src.csv_check <csv-path>`.
- Report path: relative to the current working directory; create parent
  directories and overwrite on each run.
- Performance test: generate 10,000 rows before timing; time file reading,
  parsing, validation, and report rendering, with a target under 2 seconds.
