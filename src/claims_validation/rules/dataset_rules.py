"""Dataset-level validation rules for claims batches."""

from __future__ import annotations

from collections import Counter
from typing import Any, Mapping

from claims_validation.types import CONFLICT_DUPLICATE_CLAIM_ID, Violation


def validate_duplicate_claim_ids(claims: list[Mapping[str, Any]]) -> list[Violation]:
    """Emit one conflict violation for each claim occurrence in duplicate claim_id groups."""
    claim_ids = [claim.get("claim_id") for claim in claims]
    duplicate_claim_ids = {
        claim_id
        for claim_id, count in Counter(claim_ids).items()
        if claim_id is not None and count > 1
    }

    return [
        {
            "code": CONFLICT_DUPLICATE_CLAIM_ID,
            "claim_id": claim.get("claim_id"),
        }
        for claim in claims
        if claim.get("claim_id") in duplicate_claim_ids
    ]
