# Architecture: CSV Validator for Customer Uploads

## 1. Overview

Implement a local, single-purpose Python 3.11 CLI, invoked exactly as
`python -m src.csv_check <csv-path>`. It reads and validates one CSV, renders
one concise report, writes it to `reports/csv_report.md` relative to the
current working directory, and prints the same report only after the write
succeeds. It does not load data, access cloud services, or validate amount
values. [FR-1, FR-1a, FR-10; Goal and Scope]

## 2. Components and Responsibilities

### 2.1 CLI (`src.csv_check`)

- Parse exactly one required positional CSV path. Missing/invalid invocation
  uses standard CLI usage diagnostics and exit status 2. [FR-1, FR-1a, FR-9]
- Call the validation flow, then use its report and outcome to write/print
  output and select the exit status. [FR-3, FR-9, FR-10]
- Return 0 for PASS, 1 for a completed validation FAIL, and 2 for usage,
  input, or report I/O errors. [FR-9]

### 2.2 CSV reader and validator

- Open the input as UTF-8 with BOM handling (`utf-8-sig`) and CSV newline
  handling (`newline=""`); use the standard-library CSV reader in strict
  mode. A decoding, open, or read error is an input error, not a validation
  report. [FR-2, FR-8, FR-9, NFR-1, NFR-2]
- Read one header record. Strip surrounding whitespace from each header
  name, compare required names case-sensitively, and detect duplicates
  after trimming. Report every absent required name and duplicate name.
  Keep the first occurrence of a duplicate name for any row-field lookup;
  the duplicate itself remains a validation failure. [FR-2, FR-4]
- If strict CSV parsing fails while reading the header, report a malformed
  header as a validation failure; it is not a data record and therefore has
  no data-record number. [FR-8]
- Require `id`, `email`, and `amount`. Use `id` and `email` fields for row
  checks when their headers are present; if either is missing, report the
  missing header and skip that unavailable field's row check. Do not inspect
  amount values. [FR-2, FR-4, FR-5; Goal and Scope]
- Stream subsequent logical CSV records. The first record after the header
  is data record 1; a quoted multiline CSV record remains one data record.
  Check each record's field count against the header width before field
  validation. A record with a different width is a validation failure and
  stops processing. [FR-5, FR-8]
- Treat `csv.Error` during record parsing and row-width mismatch as
  unrecoverable: stop at the first one, report its 1-based data-record
  number and the number of completely parsed, width-correct data records
  before it. Retain any earlier row findings. Do not count the erroneous
  record as complete. [FR-8]
- For complete, width-correct rows, count the record and report an empty
  `id` or invalid email using 1-based data-record numbering. An ID is empty
  when its field value has zero characters; do not trim it, since
  whitespace normalization is specified for email and headers, not IDs.
  [FR-2, FR-5, FR-8]
- Validate email by stripping surrounding whitespace, then requiring
  exactly one `@`, non-empty local and domain parts, no whitespace anywhere
  in the stripped value, and at least one dot in the domain. This is the
  specified practical check, not full RFC validation. [FR-5a]
- An absent header record or no data records results in `FAIL: no data
  rows`; report header findings too when a header exists. [FR-7]

### 2.3 Report renderer

- Render a deterministic concise Markdown report: a PASS/FAIL status,
  complete-data-row count, and applicable findings with row/column
  identifiers. For a structural parse/width failure, include the failing
  data-record number and preceding complete-record count. Validation
  findings accumulated before that failure remain in the report.
  [FR-3–FR-8]
- Render `FAIL: no data rows` for empty/header-only input. A complete file
  passes only if it has at least one data record and no validation
  findings. [FR-3, FR-7, FR-8]
- Before rendering any email detail, strip surrounding whitespace and mask
  it: if there is exactly one `@` and a non-empty local part, retain only
  its first character followed by `***`, and preserve the domain (for
  example `alice@example.com` becomes `a***@example.com`). Otherwise render
  `[invalid email]`. Never include the unmasked input value. [FR-6, FR-11]

### 2.4 Report writer and output

- Resolve `reports/csv_report.md` from the process current working
  directory, create its parent directory as needed, and overwrite the
  destination on every completed validation run. Encode report text as
  UTF-8. [FR-10]
- Write the complete report before printing it. If directory creation or
  writing fails, emit a clear error to stderr, emit no report or
  success-shaped output to stdout, and return 2. A validation FAIL is still
  written and printed when writing succeeds, then returns 1. [FR-9, FR-10]

## 3. Data Flow

1. Parse the required path from `python -m src.csv_check <csv-path>`.
   [FR-1, FR-1a]
2. Open and stream the input with BOM-aware UTF-8 decoding and strict CSV
   parsing. Convert usage/open/read/decoding failures to exit 2 and a clear
   stderr diagnostic; do not render a validation report for these
   operational errors. [FR-2, FR-8, FR-9]
3. Normalize header whitespace, check case-sensitive required headers and
   post-trim duplicates, then stream and validate complete data records.
   Stop on the first unrecoverable parser error or width mismatch.
   [FR-2, FR-4, FR-5, FR-5a, FR-8]
4. Render status, counts, and findings. Mask email details before they are
   added to rendered output; leave amount values unchecked. [FR-3–FR-8,
   FR-11; Goal and Scope]
5. Create the cwd-relative report directory, overwrite the report, and
   print identical report text only on successful write. Return 0 for PASS
   or 1 for validation FAIL. [FR-9, FR-10]

## 4. Error, Count, and Privacy Policies

| Condition | Result |
| --- | --- |
| Missing argument or CLI usage error | Usage diagnostic on stderr; status 2; no validation report. [FR-1, FR-9] |
| Input path missing, unreadable, invalid UTF-8, or other input I/O/decode error | Clear stderr diagnostic; status 2; no validation report. [FR-9] |
| Empty file or header with no following records | Validation report contains `FAIL: no data rows`; status 1 if report write succeeds. [FR-7, FR-9, FR-10] |
| Missing/duplicate header, invalid data row, malformed CSV, or width mismatch | Validation FAIL report; structural errors stop at first error and include its data-record number and prior complete-record count. [FR-2, FR-4–FR-8] |
| Report directory creation or write failure | Clear stderr diagnostic, no stdout report/success claim, status 2. [FR-9, FR-10] |
| Email included in a finding | Mask before rendering; raw address is never included. [FR-6, FR-11] |

“Data-row count” means complete, width-correct data records processed; for a
fully parsed file it is the full number of data records. For an early
structural stop, show the completed count separately from the 1-based
failing record number. CSV logical records, not physical file lines,
determine row numbers. [FR-3, FR-5, FR-8]

## 5. Testing and Performance Plan

- Automated tests shall cover invocation and status codes, clean PASS and
  row count, each missing required header, trimmed and case-sensitive
  header behavior, duplicate-after-trimming detection, BOM input, empty
  IDs, each email rule and masking fallback, amount values left unchecked,
  empty/header-only inputs, missing/unreadable input, malformed CSV,
  width mismatch and stop/count semantics, report directory creation and
  overwrite, identical stdout/report content, and report-write failure
  output behavior. [FR-1–FR-11, NFR-4]
- Test the supported Python 3.11 runtime and ensure runtime implementation
  dependencies use only the standard library. [NFR-1, NFR-2]
- For performance acceptance, generate a 10,000-row CSV before starting
  the timer. Measure input reading, CSV parsing, validation, and report
  rendering through completion; exclude fixture generation. The measured
  operation must complete in under 2 seconds on a normal local run.
  [NFR-3]

## 6. Technology Choices

| Choice | Reason | Alternative considered |
| --- | --- | --- |
| Python 3.11 standard library | Meets the specified runtime and avoids non-standard runtime dependencies. [NFR-1, NFR-2] | Third-party parsing/validation packages; excluded by NFR-2. |
| `argparse` in the `src.csv_check` module | Provides the required positional path and standard usage errors for the exact module invocation. [FR-1, FR-1a, FR-9] | A separately installed `csv-check` console script; unnecessary because FR-1a specifies `python -m`. |
| `csv.reader` with `strict=True` and streaming iteration | Parses quoted CSV records correctly, detects unrecoverable syntax errors, and avoids reading all input records into memory. [FR-8, NFR-2, NFR-3] | Manual string splitting; mishandles quoted delimiters and multiline records. |
| `open(..., encoding="utf-8-sig", newline="")` | Handles an initial UTF-8 BOM while preserving correct CSV newline parsing. [FR-2, NFR-2] | Plain UTF-8 decoding; leaves a BOM in the first header name. |
| `pathlib.Path` | Constructs the report path relative to cwd and creates its parent directory. [FR-10, NFR-2] | Manual string path concatenation; less reliable across supported path forms. |
| `unittest` for automated tests | Supplies standard-library test support for required functional and error cases. [NFR-2, NFR-4] | Third-party test framework; adds a test dependency when standard-library testing suffices. |

## 7. Requirement Traceability

| Requirement | Architectural support |
| --- | --- |
| FR-1, FR-1a | One required path argument; exact invocation is `python -m src.csv_check <csv-path>`. |
| FR-2 | BOM-aware UTF-8 header parse; trim header whitespace; case-sensitive required names; duplicate comparison after trimming. |
| FR-3, FR-4 | PASS/count only for a valid non-empty file; report all missing required headers. |
| FR-5, FR-5a | 1-based data-record findings for empty IDs and practical email validation policy. |
| FR-6, FR-11 | Mask email details before report rendering; use `[invalid email]` where safe masking is not possible; never emit the full address. |
| FR-7 | Empty and header-only input report `FAIL: no data rows`. |
| FR-8 | Strict CSV parse; width validation; stop at first structural error; report its data-record number and prior complete-record count. |
| FR-9 | Status 0 PASS / 1 validation FAIL / 2 usage, input, or report I/O error. |
| FR-10 | Cwd-relative report path, parent creation, overwrite; print only after a successful write; report-write failure is stderr-only. |
| NFR-1, NFR-2 | Python 3.11 and standard-library runtime. |
| NFR-3 | Generated 10,000-row benchmark; timed read, parse, validate, and render under 2 seconds, excluding fixture generation. |
| NFR-4 | Automated functional, error-handling, privacy, output, and performance coverage. |
