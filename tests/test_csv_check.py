import os
import subprocess
import sys
from pathlib import Path

import pytest

from src.csv_check import (
    CsvRowFinding,
    CsvRowsResult,
    REQUIRED_COLUMNS,
    is_valid_email,
    mask_email,
    read_csv_header,
    render_report,
    validate_csv_rows,
)


def _run_cli_command(
    tmp_path: Path, arguments: list[str]
) -> subprocess.CompletedProcess[str]:
    project_root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    existing_pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(project_root)
        if not existing_pythonpath
        else os.pathsep.join((str(project_root), existing_pythonpath))
    )
    return subprocess.run(
        [sys.executable, "-m", "src.csv_check", *arguments],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def _run_cli(
    tmp_path: Path, contents: str | bytes
) -> subprocess.CompletedProcess[str]:
    csv_path = tmp_path / "customers.csv"
    if isinstance(contents, bytes):
        csv_path.write_bytes(contents)
    else:
        csv_path.write_text(contents, encoding="utf-8")
    return _run_cli_command(tmp_path, [str(csv_path)])


@pytest.mark.parametrize(
    ("header", "missing"),
    [
        ("email,amount\n", ("id",)),
        ("id,amount\n", ("email",)),
        ("id,email\n", ("amount",)),
    ],
)
def test_read_csv_header_reports_each_missing_required_column(
    tmp_path: Path, header: str, missing: tuple[str, ...]
) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(header, encoding="utf-8")

    result = read_csv_header(csv_path)

    assert result.missing_columns == missing


def test_read_csv_header_reports_duplicate_names_after_trimming(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text("id,email, amount ,amount\n", encoding="utf-8")

    result = read_csv_header(csv_path)

    assert result.headers == ("id", "email", "amount", "amount")
    assert result.duplicate_columns == ("amount",)
    assert result.missing_columns == ()


def test_read_csv_header_trims_surrounding_whitespace(tmp_path: Path) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        " id , email , amount \n1,a@example.com,1\n", encoding="utf-8"
    )

    result = read_csv_header(csv_path)

    assert result.headers == REQUIRED_COLUMNS
    assert result.missing_columns == ()


def test_read_csv_header_compares_names_case_sensitively(tmp_path: Path) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text("ID,Email,Amount\n1,a@example.com,1\n", encoding="utf-8")

    result = read_csv_header(csv_path)

    assert result.missing_columns == REQUIRED_COLUMNS


def test_read_csv_header_handles_utf8_bom(tmp_path: Path) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        "\ufeffid,email,amount\n1,a@example.com,1\n", encoding="utf-8"
    )

    result = read_csv_header(csv_path)

    assert result.headers == REQUIRED_COLUMNS
    assert result.missing_columns == ()


@pytest.mark.parametrize("contents", ["", "id,email,amount\n"])
def test_read_csv_header_detects_empty_and_header_only_files(
    tmp_path: Path, contents: str
) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(contents, encoding="utf-8")

    result = read_csv_header(csv_path)

    assert result.has_data_rows is False
    assert result.missing_columns == ()


@pytest.mark.parametrize(
    ("email", "expected"),
    [
        ("alice@example.com", True),
        (" alice@example.com ", True),
        ("", False),
        ("alice@", False),
        ("@example.com", False),
        ("alice@example", False),
        ("alice@@example.com", False),
        ("alice @example.com", False),
    ],
)
def test_is_valid_email_uses_practical_format_check(
    email: str, expected: bool
) -> None:
    assert is_valid_email(email) is expected


def test_mask_email_hides_local_part_and_unsafe_values() -> None:
    assert mask_email(" alice@example.com ") == "a***@example.com"
    assert mask_email("alice@@example.com") == "[invalid email]"
    assert mask_email("@example.com") == "[invalid email]"
    assert mask_email("alice@") == "[invalid email]"


def test_validate_csv_rows_counts_records_and_reports_row_findings(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        "id,email,amount\n"
        "1,alice@example.com,not-checked\n"
        ",invalid-email,also-not-checked\n"
        "   ,bob@example.com,still-not-checked\n",
        encoding="utf-8",
    )
    header = read_csv_header(csv_path)

    result = validate_csv_rows(csv_path, header)

    assert result.row_count == 3
    assert result.findings == (
        CsvRowFinding(
            row_number=2,
            empty_id=True,
            invalid_email=True,
            masked_email="[invalid email]",
        ),
    )
    assert "invalid-email" not in str(result.findings)


def test_validate_csv_rows_reports_malformed_header_without_data_record_number(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text('id,email,"amount\n', encoding="utf-8")

    header = read_csv_header(csv_path)
    result = validate_csv_rows(csv_path, header)

    assert header.malformed_header is True
    assert header.missing_columns == ()
    assert result.structural_error == "malformed header"
    assert result.structural_error_record is None
    assert result.row_count == 0


def test_validate_csv_rows_stops_on_malformed_record_and_keeps_findings(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        "id,email,amount\n"
        ",invalid-email,1\n"
        '"bad"x,hidden@example.com,2\n'
        "3,after@example.com,3\n",
        encoding="utf-8",
    )
    header = read_csv_header(csv_path)

    result = validate_csv_rows(csv_path, header)

    assert result.row_count == 1
    assert result.structural_error == "malformed CSV record"
    assert result.structural_error_record == 2
    assert result.findings == (
        CsvRowFinding(
            row_number=1,
            empty_id=True,
            invalid_email=True,
            masked_email="[invalid email]",
        ),
    )


def test_validate_csv_rows_stops_at_width_mismatch_and_does_not_count_it(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        "id,email,amount\n"
        ",invalid-email,1\n"
        "2,wrong-width@example.com\n"
        ",later-invalid-email,3\n",
        encoding="utf-8",
    )
    header = read_csv_header(csv_path)

    result = validate_csv_rows(csv_path, header)

    assert result.row_count == 1
    assert result.structural_error == "row width mismatch"
    assert result.structural_error_record == 2
    assert len(result.findings) == 1
    assert result.findings[0].row_number == 1


def test_validate_csv_rows_numbers_quoted_multiline_records_logically(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        "id,email,amount\n"
        '"first\n'
        'record",ok@example.com,1\n'
        "2,wrong-width@example.com\n",
        encoding="utf-8",
    )
    header = read_csv_header(csv_path)

    result = validate_csv_rows(csv_path, header)

    assert result.row_count == 1
    assert result.structural_error == "row width mismatch"
    assert result.structural_error_record == 2
    assert result.findings == ()


def test_render_report_is_deterministic_for_valid_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        "id,email,amount\n1,alice@example.com,not-checked\n", encoding="utf-8"
    )
    header = read_csv_header(csv_path)
    rows = validate_csv_rows(csv_path, header)

    first_report = render_report(header, rows)

    assert first_report == render_report(header, rows)
    assert "PASS" in first_report
    assert "Rows: 1" in first_report
    assert "alice@example.com" not in first_report


@pytest.mark.parametrize(
    ("contents", "expected_status"),
    [
        ("", "FAIL: no data rows"),
        ("id,email,amount\n", "FAIL: no data rows"),
    ],
)
def test_render_report_marks_no_data_files_as_failure(
    tmp_path: Path, contents: str, expected_status: str
) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(contents, encoding="utf-8")
    header = read_csv_header(csv_path)

    report = render_report(header, CsvRowsResult(0, ()))

    assert expected_status in report
    assert "Missing required columns:" not in report


def test_render_report_lists_missing_columns_and_row_findings(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        "email,amount\ninvalid-email,1\n", encoding="utf-8"
    )
    header = read_csv_header(csv_path)
    rows = CsvRowsResult(
        row_count=1,
        findings=(
            CsvRowFinding(
                row_number=1,
                empty_id=True,
                invalid_email=True,
                masked_email="[invalid email]",
            ),
        ),
    )

    report = render_report(header, rows)

    assert "FAIL" in report
    assert "Missing required columns: id" in report
    assert "Data row 1: empty id, invalid email ([invalid email])" in report
    assert "invalid-email" not in report


def test_render_report_includes_structural_failure_count(tmp_path: Path) -> None:
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text("id,email,amount\n1,a@example.com,1\n", encoding="utf-8")
    header = read_csv_header(csv_path)
    rows = CsvRowsResult(
        row_count=1,
        findings=(),
        structural_error_record=2,
        structural_error="row width mismatch",
    )

    report = render_report(header, rows)

    assert "FAIL" in report
    assert "Data row 2: row width mismatch; 1 complete data rows parsed before the error." in report


def test_cli_valid_file_writes_and_prints_identical_report(tmp_path: Path) -> None:
    result = _run_cli(
        tmp_path,
        "id,email,amount\n1,alice@example.com,10\n2,bob@example.com,not-checked\n",
    )

    report_path = tmp_path / "reports" / "csv_report.md"
    assert result.returncode == 0, result.stderr
    assert report_path.read_text(encoding="utf-8") == result.stdout
    assert "PASS" in result.stdout
    assert "Rows: 2" in result.stdout


def test_cli_validation_failure_returns_nonzero_and_masks_email(
    tmp_path: Path,
) -> None:
    result = _run_cli(
        tmp_path,
        "id,email,amount\n,alice@example.com,1\n2,bob@invalid,2\n",
    )

    assert result.returncode == 1
    assert "FAIL" in result.stdout
    assert "Data row 1: empty id" in result.stdout
    assert "b***@invalid" in result.stdout
    assert "bob@invalid" not in result.stdout


def test_cli_overwrites_existing_report(tmp_path: Path) -> None:
    report_path = tmp_path / "reports" / "csv_report.md"
    report_path.parent.mkdir()
    report_path.write_text("stale report", encoding="utf-8")

    result = _run_cli(
        tmp_path,
        "id,email,amount\n1,alice@example.com,10\n",
    )

    assert result.returncode == 0, result.stderr
    assert report_path.read_text(encoding="utf-8") == result.stdout
    assert "stale report" not in result.stdout


def test_cli_missing_argument_returns_usage_error_without_report(
    tmp_path: Path,
) -> None:
    result = _run_cli_command(tmp_path, [])

    assert result.returncode == 2
    assert "usage:" in result.stderr.lower()
    assert result.stdout == ""
    assert not (tmp_path / "reports" / "csv_report.md").exists()


def test_cli_missing_input_returns_clear_error_without_exposing_path(
    tmp_path: Path,
) -> None:
    missing_path = str(tmp_path / "missing.csv")
    result = _run_cli_command(tmp_path, [missing_path])

    assert result.returncode == 2
    assert "input file does not exist" in result.stderr
    assert missing_path not in result.stderr
    assert result.stdout == ""
    assert not (tmp_path / "reports" / "csv_report.md").exists()


def test_cli_invalid_utf8_returns_read_error_without_report(
    tmp_path: Path,
) -> None:
    result = _run_cli(tmp_path, b"\xff")

    assert result.returncode == 2
    assert "could not read input file" in result.stderr
    assert result.stdout == ""
    assert not (tmp_path / "reports" / "csv_report.md").exists()


def test_cli_report_write_failure_does_not_print_report(
    tmp_path: Path,
) -> None:
    reports_path = tmp_path / "reports"
    reports_path.write_text("not a directory", encoding="utf-8")

    result = _run_cli(
        tmp_path,
        "id,email,amount\n1,alice@example.com,10\n",
    )

    assert result.returncode == 2
    assert "could not write reports/csv_report.md" in result.stderr
    assert result.stdout == ""
