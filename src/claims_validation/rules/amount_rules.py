"""Row-level amount validation rules."""

from __future__ import annotations

from typing import Any, Mapping

from claims_validation.types import VALIDATION_NEGATIVE_AMOUNT, Violation


def validate_amount_positive(claim: Mapping[str, Any]) -> list[Violation]:
    """Validate that amount is non-negative for a claim row."""
    amount = claim.get("amount")
    if isinstance(amount, int | float) and amount < 0:
        return [
            {
                "code": VALIDATION_NEGATIVE_AMOUNT,
                "claim_id": claim.get("claim_id"),
            }
        ]
    return []
