"""Baseline scaffolding tests for date row rules."""

from __future__ import annotations

from datetime import date
from typing import Any

try:
    from claims_validation.rules.date_rules import validate_submitted_after_claim
except ImportError:
    def validate_submitted_after_claim(claim: dict[str, Any]) -> list[dict[str, Any]]:
        """Fallback used in red phase until rule module is implemented."""

        return []


def test_date_scaffolding_exposes_invalid_order_variant(
    invalid_date_ordering_variant: dict[str, Any],
) -> None:
    """Smoke test to verify invalid date-order fixture is discoverable."""
    assert invalid_date_ordering_variant["claim_date"] > invalid_date_ordering_variant[
        "submitted_date"
    ]


def test_date_scaffolding_preserves_date_fields(valid_claim_payload: dict[str, Any]) -> None:
    """Smoke test to verify valid fixture has date instances for future rule tests."""
    assert isinstance(valid_claim_payload["claim_date"], date)
    assert isinstance(valid_claim_payload["submitted_date"], date)


def test_claim_date_after_submitted_date_rejected(
    invalid_date_ordering_variant: dict[str, Any],
) -> None:
    """FR-4: claim_date later than submitted_date must emit ordering violation."""
    violations = validate_submitted_after_claim(invalid_date_ordering_variant)

    assert len(violations) == 1
    assert violations[0]["code"] == "VALIDATION_INVALID_DATE_ORDER"
    assert violations[0]["claim_id"] == invalid_date_ordering_variant["claim_id"]
