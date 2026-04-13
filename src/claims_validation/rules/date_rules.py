"""Row-level date validation rules."""

from __future__ import annotations

from datetime import date
from typing import Any, Mapping

from claims_validation.reporting import build_error_record
from claims_validation.types import VALIDATION_INVALID_DATE_ORDER, Violation


def validate_submitted_after_claim(claim: Mapping[str, Any]) -> list[Violation]:
    """Validate that submitted_date is not earlier than claim_date."""
    claim_date = claim.get("claim_date")
    submitted_date = claim.get("submitted_date")
    if isinstance(claim_date, date) and isinstance(submitted_date, date) and claim_date > submitted_date:
        return [
            build_error_record(
                code=VALIDATION_INVALID_DATE_ORDER,
                details={
                    "claim_id": claim.get("claim_id"),
                    "field": "claim_date",
                    "value": claim_date.isoformat(),
                    "submitted_date": submitted_date.isoformat(),
                },
            )
        ]
    return []
