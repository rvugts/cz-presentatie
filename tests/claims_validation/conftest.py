"""Shared pytest fixtures for claims validation tests."""

from __future__ import annotations

from copy import deepcopy
from datetime import date
from typing import Any

import pytest


@pytest.fixture
def claim_factory() -> Any:
    """Build a claim payload and allow field overrides per test."""

    def _build_claim(**overrides: Any) -> dict[str, Any]:
        claim = {
            "claim_id": "C-1001",
            "patient_id": "PAT-001",
            "provider_id": "PRV-001",
            "treatment_code": "TREAT-100",
            "amount": 125.50,
            "claim_date": date(2026, 4, 1),
            "submitted_date": date(2026, 4, 2),
            "status": "submitted",
        }
        claim.update(overrides)
        return claim

    return _build_claim


@pytest.fixture
def valid_claim_payload(claim_factory: Any) -> dict[str, Any]:
    """A valid claim payload used as the default happy-path fixture."""
    return claim_factory()


@pytest.fixture
def invalid_amount_variants(valid_claim_payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Claims with invalid negative amounts for amount-rule red tests."""
    first_variant = deepcopy(valid_claim_payload)
    first_variant["amount"] = -0.01

    second_variant = deepcopy(valid_claim_payload)
    second_variant["claim_id"] = "C-1002"
    second_variant["amount"] = -999.99

    return [first_variant, second_variant]


@pytest.fixture
def invalid_date_ordering_variant(valid_claim_payload: dict[str, Any]) -> dict[str, Any]:
    """Claim where claim_date is later than submitted_date."""
    invalid_payload = deepcopy(valid_claim_payload)
    invalid_payload["claim_id"] = "C-1003"
    invalid_payload["claim_date"] = date(2026, 4, 5)
    invalid_payload["submitted_date"] = date(2026, 4, 4)
    return invalid_payload


@pytest.fixture
def patient_reference_ids() -> set[str]:
    """Known patient IDs used for referential validation tests."""
    return {"PAT-001", "PAT-002", "PAT-003"}


@pytest.fixture
def provider_reference_ids() -> set[str]:
    """Known provider IDs used for referential validation tests."""
    return {"PRV-001", "PRV-002", "PRV-003"}
