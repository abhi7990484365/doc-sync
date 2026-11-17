"""CSV header validation for customer upload checks."""

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_COLUMNS = ("id", "email", "amount")


@dataclass(frozen=True)
class CsvHeaderResult:
    """Normalized CSV headers and their validation findings."""

    headers: tuple[str, ...]
    missing_columns: tuple[str, ...]
    duplicate_columns: tuple[str, ...]
    has_data_rows: bool
    malformed_header: bool = False


@dataclass(frozen=True)
class CsvRowFinding:
    """A validation issue found in one data record."""

    row_number: int
    empty_id: bool
    invalid_email: bool
    masked_email: str | None


@dataclass(frozen=True)
class CsvRowsResult:
    """Data-record count and row-level validation findings."""

    row_count: int
    findings: tuple[CsvRowFinding, ...]
    structural_error_record: int | None = None
    structural_error: str | None = None


def read_csv_header(path: str | Path) -> CsvHeaderResult:
    """Read and validate a CSV header, also detecting whether data rows exist."""
    with Path(path).open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.reader(csv_file, strict=True)
        try:
            headers = tuple(column.strip() for column in next(reader))
        except StopIteration:
            return CsvHeaderResult((), (), (), False)
        except csv.Error:
            return CsvHeaderResult((), (), (), False, malformed_header=True)

        seen: set[str] = set()
        duplicate_columns: list[str] = []
        duplicate_set: set[str] = set()
        for column in headers:
            if column in seen and column not in duplicate_set:
                duplicate_columns.append(column)
                duplicate_set.add(column)
            seen.add(column)

        missing_columns = tuple(
            column for column in REQUIRED_COLUMNS if column not in seen
        )

        try:
            next(reader)
        except StopIteration:
            has_data_rows = False
        except csv.Error:
            # The record exists, but its parse failure is reported by the
            # row-validation pass with its data-record number.
            has_data_rows = True
        else:
            has_data_rows = True

    return CsvHeaderResult(
        headers=headers,
        missing_columns=missing_columns,
        duplicate_columns=tuple(duplicate_columns),
        has_data_rows=has_data_rows,
    )


def is_valid_email(value: str) -> bool:
    """Apply the approved practical email format check."""
    email = value.strip()
    if email.count("@") != 1 or any(character.isspace() for character in email):
        return False

    local_part, domain = email.split("@")
    return bool(local_part and domain and "." in domain)


def mask_email(value: str) -> str:
    """Mask an email value without exposing an unsafe or malformed address."""
    email = value.strip()
    if email.count("@") != 1:
        return "[invalid email]"

    local_part, domain = email.split("@")
    if not local_part or not domain:
        return "[invalid email]"

    return f"{local_part[0]}***@{domain}"


def validate_csv_rows(path: str | Path, header: CsvHeaderResult) -> CsvRowsResult:
    """Count CSV data records and identify empty IDs and invalid emails."""
    if header.malformed_header:
        return CsvRowsResult(
            row_count=0,
            findings=(),
            structural_error="malformed header",
        )
    if header.missing_columns or header.duplicate_columns:
        raise ValueError("CSV row validation requires a valid header")

    id_index = header.headers.index("id")
    email_index = header.headers.index("email")
    findings: list[CsvRowFinding] = []
    row_count = 0

    with Path(path).open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.reader(csv_file, strict=True)
        next(reader, None)
        record_number = 1
        while True:
            try:
                row = next(reader)
            except StopIteration:
                break
            except csv.Error:
                return CsvRowsResult(
                    row_count=row_count,
                    findings=tuple(findings),
                    structural_error_record=record_number,
                    structural_error="malformed CSV record",
                )

            if len(row) != len(header.headers):
                return CsvRowsResult(
                    row_count=row_count,
                    findings=tuple(findings),
                    structural_error_record=record_number,
                    structural_error="row width mismatch",
                )

            row_count += 1
            empty_id = row[id_index] == ""
            email = row[email_index]
            invalid_email = not is_valid_email(email)
            if empty_id or invalid_email:
                findings.append(
                    CsvRowFinding(
                        row_number=record_number,
                        empty_id=empty_id,
                        invalid_email=invalid_email,
                        masked_email=mask_email(email) if invalid_email else None,
                    )
                )
            record_number += 1

    return CsvRowsResult(row_count=row_count, findings=tuple(findings))


def render_report(header: CsvHeaderResult, rows: CsvRowsResult) -> str:
    """Render a stable Markdown report without exposing raw email values."""
    passed = _validation_passed(header, rows)
    if passed:
        status = "PASS"
    elif not header.has_data_rows and not header.malformed_header:
        status = "FAIL: no data rows"
    else:
        status = "FAIL"

    if header.malformed_header or (
        header.has_data_rows
        and (header.missing_columns or header.duplicate_columns)
    ):
        row_count = "Not Counted"
    else:
        row_count = str(rows.row_count)

    lines = [
        "# CSV Validation Report",
        "",
        status,
        f"Rows: {row_count}",
    ]

    if header.missing_columns:
        lines.extend(
            ("", f"Missing required columns: {', '.join(header.missing_columns)}")
        )
    if header.duplicate_columns:
        lines.extend(
            ("", f"Duplicate columns: {', '.join(header.duplicate_columns)}")
        )
    if header.malformed_header or rows.structural_error == "malformed header":
        lines.extend(("", "Malformed CSV header."))
    elif rows.structural_error:
        record_number = rows.structural_error_record
        if record_number is None:
            lines.extend(("", f"Malformed CSV: {rows.structural_error}."))
        else:
            lines.extend(
                (
                    "",
                    f"Data row {record_number}: {rows.structural_error}; "
                    f"{rows.row_count} complete data rows parsed before the error.",
                )
            )

    for finding in rows.findings:
        messages = []
        if finding.empty_id:
            messages.append("empty id")
        if finding.invalid_email:
            masked_email = mask_email(finding.masked_email or "")
            messages.append(f"invalid email ({masked_email})")
        lines.extend(("", f"Data row {finding.row_number}: {', '.join(messages)}"))

    return "\n".join(lines).rstrip() + "\n"


def _validation_passed(header: CsvHeaderResult, rows: CsvRowsResult) -> bool:
    return bool(
        header.has_data_rows
        and not header.malformed_header
        and not header.missing_columns
        and not header.duplicate_columns
        and not rows.findings
        and not rows.structural_error
    )


def main(argv: list[str] | None = None) -> int:
    """Run the CSV validator command."""
    parser = argparse.ArgumentParser(prog="csv-check")
    parser.add_argument("csv_path", help="path to the customer CSV file")
    arguments = parser.parse_args(argv)
    csv_path = Path(arguments.csv_path)

    try:
        header = read_csv_header(csv_path)
        if header.malformed_header:
            rows = validate_csv_rows(csv_path, header)
        elif (
            not header.has_data_rows
            or header.missing_columns
            or header.duplicate_columns
        ):
            rows = CsvRowsResult(row_count=0, findings=())
        else:
            rows = validate_csv_rows(csv_path, header)
    except FileNotFoundError:
        print("csv-check: input file does not exist.", file=sys.stderr)
        return 2
    except IsADirectoryError:
        print("csv-check: input path is not a file.", file=sys.stderr)
        return 2
    except (OSError, UnicodeError):
        print("csv-check: could not read input file.", file=sys.stderr)
        return 2

    report = render_report(header, rows)
    report_path = Path("reports") / "csv_report.md"
    try:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
    except OSError:
        print("csv-check: could not write reports/csv_report.md.", file=sys.stderr)
        return 2

    print(report, end="")
    return 0 if _validation_passed(header, rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
