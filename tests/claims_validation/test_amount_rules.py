"""Baseline scaffolding tests for amount row rules."""

from __future__ import annotations

from typing import Any

try:
    from claims_validation.rules.amount_rules import validate_amount_positive
except ImportError:
    def validate_amount_positive(claim: dict[str, Any]) -> list[dict[str, Any]]:
        """Fallback used in red phase until rule module is implemented."""

        return []


def test_amount_scaffolding_uses_valid_claim_fixture(
    valid_claim_payload: dict[str, Any],
) -> None:
    """Smoke test to verify shared claim fixture is discoverable."""
    assert valid_claim_payload["amount"] >= 0


def test_amount_scaffolding_exposes_invalid_variants(
    invalid_amount_variants: list[dict[str, Any]],
) -> None:
    """Smoke test to verify invalid amount fixtures are reusable."""
    assert invalid_amount_variants


def test_negative_amount_rejected(invalid_amount_variants: list[dict[str, Any]]) -> None:
    """FR-3: negative amount must emit the expected validation code."""
    invalid_claim = invalid_amount_variants[0]

    violations = validate_amount_positive(invalid_claim)

    assert len(violations) == 1
    assert violations[0]["code"] == "VALIDATION_NEGATIVE_AMOUNT"
    assert violations[0]["claim_id"] == invalid_claim["claim_id"]


def test_zero_amount_allowed(claim_factory: Any) -> None:
    """FR-3: zero amount is valid and must not emit violations."""
    zero_amount_claim = claim_factory(amount=0)

    violations = validate_amount_positive(zero_amount_claim)

    assert violations == []
