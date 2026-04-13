"""Databricks runner for claims validation from hardcoded workspace tables."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import uuid4

from claims_validation.engine import validate_claims

CLAIMS_TABLE = "workspace.demo.claims"
PATIENTS_TABLE = "workspace.demo.patients"
PROVIDERS_TABLE = "workspace.demo.providers"
PATIENT_ID_COLUMN = "patient_id"
PROVIDER_ID_COLUMN = "provider_id"
DEFAULT_OUTPUT_PATH = "/dbfs/tmp/validation_report.json"
SUCCESS_EXIT_CODE = 0
FAILURE_EXIT_CODE = 1


def create_spark_session() -> Any:
    """Create a Spark session in Databricks or any Spark-enabled runtime."""
    from pyspark.sql import SparkSession  # Imported lazily for local testability.

    return SparkSession.builder.getOrCreate()


def _read_table_records(spark: Any, table_name: str) -> list[dict[str, Any]]:
    """Load table rows as plain dictionaries."""
    return [row.asDict(recursive=True) for row in spark.table(table_name).collect()]


def _read_reference_ids(spark: Any, table_name: str, column_name: str) -> set[str]:
    """Load a set of non-null reference IDs from a Databricks table column."""
    rows = spark.table(table_name).select(column_name).collect()
    return {
        row.asDict(recursive=True).get(column_name)
        for row in rows
        if row.asDict(recursive=True).get(column_name) is not None
    }


def to_canonical_json_records(violations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Transform internal violation payloads to Section 9 JSON error envelope records."""
    canonical_records: list[dict[str, Any]] = []
    for violation in violations:
        canonical_records.append(
            {
                "error": {
                    "code": violation.get("code", "SERVER_UNEXPECTED_EXCEPTION"),
                    "message": violation.get("message", "Unexpected server-side validation error."),
                    "details": dict(violation.get("details", {})),
                    "request_id": violation.get("request_id") or str(uuid4()),
                }
            }
        )
    return canonical_records


def _json_default(value: Any) -> Any:
    """Safely encode non-JSON-native values commonly found in validation payloads."""
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    return str(value)


def write_json_report(
    records: list[dict[str, Any]], output_path: str = DEFAULT_OUTPUT_PATH
) -> None:
    """Write canonical JSON records to DBFS output path."""
    target_path = Path(output_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w", encoding="utf-8") as report_file:
        json.dump(records, report_file, ensure_ascii=False, indent=2, default=_json_default)


def run_validation_from_tables(spark: Any) -> list[dict[str, Any]]:
    """Load hardcoded source tables, run validation, and persist canonical JSON output."""
    claims = _read_table_records(spark, CLAIMS_TABLE)
    patient_ids = _read_reference_ids(spark, PATIENTS_TABLE, PATIENT_ID_COLUMN)
    provider_ids = _read_reference_ids(spark, PROVIDERS_TABLE, PROVIDER_ID_COLUMN)

    violations = validate_claims(claims=claims, patient_ids=patient_ids, provider_ids=provider_ids)
    records = to_canonical_json_records(violations)
    write_json_report(records, DEFAULT_OUTPUT_PATH)
    return records


def main() -> int:
    """CLI entry point for Databricks execution.

    :return: Process exit code where ``0`` indicates success and ``1`` indicates failure.
    """
    try:
        spark = create_spark_session()
        run_validation_from_tables(spark)
        return SUCCESS_EXIT_CODE
    except Exception as exc:  # noqa: BLE001 - CLI boundary should map failures to exit codes
        print(f"Validation runner failed: {exc}", file=sys.stderr)
        return FAILURE_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
