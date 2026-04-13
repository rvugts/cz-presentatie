"""Deterministic local benchmark harness for claims-validation engine performance."""

from __future__ import annotations

import os
from datetime import date
from time import perf_counter
from typing import Any

import pytest

from claims_validation.engine import validate_claims


def _build_claim_batch(batch_size: int) -> list[dict[str, Any]]:
    """Create deterministic synthetic claims for local performance checks."""
    claim_date = date(2026, 4, 1)
    submitted_date = date(2026, 4, 2)
    return [
        {
            "claim_id": f"C-{index:06d}",
            "patient_id": f"PAT-{index:06d}",
            "provider_id": f"PRV-{index:06d}",
            "treatment_code": "TREAT-100",
            "amount": 100.0,
            "claim_date": claim_date,
            "submitted_date": submitted_date,
            "status": "submitted",
        }
        for index in range(batch_size)
    ]


@pytest.mark.slow
def test_validation_engine_local_benchmark_harness() -> None:
    """Run a CI-safe benchmark and estimate 5M-row runtime for spec intent tracking."""
    batch_size = 25_000
    claims = _build_claim_batch(batch_size)
    patient_ids = {claim["patient_id"] for claim in claims}
    provider_ids = {claim["provider_id"] for claim in claims}

    started_at = perf_counter()
    violations = validate_claims(
        claims=claims,
        patient_ids=patient_ids,
        provider_ids=provider_ids,
    )
    elapsed_seconds = perf_counter() - started_at

    assert violations == []

    # Default threshold is intentionally practical for local/CI runs.
    max_local_seconds = float(os.getenv("CLAIMS_VALIDATION_LOCAL_BENCH_MAX_SECONDS", "10.0"))
    assert elapsed_seconds <= max_local_seconds

    projected_5m_seconds = elapsed_seconds * (5_000_000 / batch_size)
    enforce_spec_target = os.getenv("CLAIMS_VALIDATION_ENFORCE_SPEC_TARGET", "0") == "1"
    if enforce_spec_target:
        assert projected_5m_seconds <= 20 * 60
