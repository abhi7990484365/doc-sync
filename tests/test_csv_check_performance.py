"""Bounded performance coverage for large customer CSV files."""

import time
from pathlib import Path

from src.csv_check import read_csv_header, render_report, validate_csv_rows


def test_validates_and_renders_10000_csv_rows_in_under_two_seconds(
    tmp_path: Path,
) -> None:
    """Read, validate, and render a valid 10,000-row file within the budget."""
    csv_path = tmp_path / "customers.csv"
    data_rows = (
        f"{row_number},customer{row_number}@example.com,not-checked"
        for row_number in range(1, 10_001)
    )
    csv_path.write_text(
        "id,email,amount\n" + "\n".join(data_rows) + "\n",
        encoding="utf-8",
    )

    start = time.perf_counter()
    header = read_csv_header(csv_path)
    rows = validate_csv_rows(csv_path, header)
    report = render_report(header, rows)
    elapsed = time.perf_counter() - start

    assert rows.row_count == 10_000
    assert "PASS" in report
    assert "Rows: 10000" in report
    assert elapsed < 2.0
