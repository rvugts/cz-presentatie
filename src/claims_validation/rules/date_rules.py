"""Row-level date validation rules."""

from __future__ import annotations

from datetime import date
from typing import Any, Mapping

from claims_validation.types import VALIDATION_INVALID_DATE_ORDER, Violation


def validate_submitted_after_claim(claim: Mapping[str, Any]) -> list[Violation]:
    """Validate that submitted_date is not earlier than claim_date."""
    claim_date = claim.get("claim_date")
    submitted_date = claim.get("submitted_date")
    if isinstance(claim_date, date) and isinstance(submitted_date, date) and claim_date > submitted_date:
        return [
            {
                "code": VALIDATION_INVALID_DATE_ORDER,
                "claim_id": claim.get("claim_id"),
            }
        ]
    return []
