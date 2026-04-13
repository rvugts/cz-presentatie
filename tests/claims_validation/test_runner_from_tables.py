"""Tests for Databricks runner orchestration and DBFS JSON sink behavior."""

from __future__ import annotations

import importlib.util
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any


def _load_runner_module() -> Any:
    module_path = Path(__file__).resolve().parents[2] / "scripts" / "run_claims_validation_from_tables.py"
    module_spec = importlib.util.spec_from_file_location("run_claims_validation_from_tables", module_path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError("Unable to load runner module specification")

    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


runner = _load_runner_module()


class _FakeRow:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    def asDict(self, recursive: bool = False) -> dict[str, Any]:  # noqa: N802 - Spark naming parity
        return dict(self._payload)


class _FakeDataFrame:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def select(self, *columns: str) -> "_FakeDataFrame":
        projected_rows = [{column: row.get(column) for column in columns} for row in self._rows]
        return _FakeDataFrame(projected_rows)

    def collect(self) -> list[_FakeRow]:
        return [_FakeRow(row) for row in self._rows]


class _FakeSparkSession:
    def __init__(self, table_data: dict[str, list[dict[str, Any]]]) -> None:
        self._table_data = table_data
        self.accessed_tables: list[str] = []

    def table(self, table_name: str) -> _FakeDataFrame:
        self.accessed_tables.append(table_name)
        return _FakeDataFrame(self._table_data[table_name])


def test_run_validation_from_tables_loads_hardcoded_sources_and_writes_dbfs_json(
    monkeypatch: Any,
) -> None:
    """Runner should read required tables, validate with reference IDs, and write output."""
    spark = _FakeSparkSession(
        {
            "workspace.demo.claims": [{"claim_id": "C-1"}],
            "workspace.demo.patients": [{"patient_id": "PAT-1"}, {"patient_id": "PAT-2"}],
            "workspace.demo.providers": [{"provider_id": "PRV-1"}, {"provider_id": "PRV-2"}],
        }
    )

    captured: dict[str, Any] = {}

    def _fake_validate_claims(
        claims: list[dict[str, Any]],
        patient_ids: set[str],
        provider_ids: set[str],
    ) -> list[dict[str, Any]]:
        captured["claims"] = claims
        captured["patient_ids"] = patient_ids
        captured["provider_ids"] = provider_ids
        return [
            {
                "code": "VALIDATION_NEGATIVE_AMOUNT",
                "message": "Claim amount must be non-negative.",
                "details": {"claim_id": "C-1", "field": "amount", "value": -1.0},
                "request_id": "req-1",
            }
        ]

    monkeypatch.setattr(runner, "validate_claims", _fake_validate_claims)

    def _fake_write_json_report(records: list[dict[str, Any]], output_path: str) -> None:
        captured["written_records"] = records
        captured["output_path"] = output_path

    monkeypatch.setattr(runner, "write_json_report", _fake_write_json_report)

    result = runner.run_validation_from_tables(spark)

    assert spark.accessed_tables == [
        "workspace.demo.claims",
        "workspace.demo.patients",
        "workspace.demo.providers",
    ]
    assert captured["claims"] == [{"claim_id": "C-1"}]
    assert captured["patient_ids"] == {"PAT-1", "PAT-2"}
    assert captured["provider_ids"] == {"PRV-1", "PRV-2"}
    assert captured["output_path"] == "/dbfs/tmp/validation_report.json"
    assert result == captured["written_records"]
    assert result == [
        {
            "error": {
                "code": "VALIDATION_NEGATIVE_AMOUNT",
                "message": "Claim amount must be non-negative.",
                "details": {"claim_id": "C-1", "field": "amount", "value": -1.0},
                "request_id": "req-1",
            }
        }
    ]


def test_write_json_report_serializes_supported_values(tmp_path: Path) -> None:
    """JSON writer should safely serialize dates and decimals without throwing."""
    output_path = tmp_path / "validation_report.json"
    records = [
        {
            "error": {
                "code": "VALIDATION_NEGATIVE_AMOUNT",
                "message": "Claim amount must be non-negative.",
                "details": {
                    "claim_id": "C-100",
                    "service_date": date(2026, 4, 13),
                    "amount": Decimal("10.25"),
                },
                "request_id": "req-100",
            }
        }
    ]

    runner.write_json_report(records, str(output_path))

    content = output_path.read_text(encoding="utf-8")
    assert "2026-04-13" in content
    assert "10.25" in content


def test_main_returns_zero_for_successful_run(monkeypatch: Any) -> None:
    """CLI should return zero exit code when orchestration succeeds."""
    monkeypatch.setattr(runner, "create_spark_session", lambda: object())
    monkeypatch.setattr(runner, "run_validation_from_tables", lambda spark: [])

    assert runner.main() == 0


def test_main_returns_one_on_execution_failure(monkeypatch: Any) -> None:
    """CLI should return non-zero exit code for orchestration failures."""
    monkeypatch.setattr(runner, "create_spark_session", lambda: object())

    def _raise_failure(_: Any) -> list[dict[str, Any]]:
        raise RuntimeError("boom")

    monkeypatch.setattr(runner, "run_validation_from_tables", _raise_failure)

    assert runner.main() == 1
