"""Red-phase dataset tests for duplicate claim_id validation (FR-2)."""

from __future__ import annotations

from collections import Counter
from typing import Any

try:
    from claims_validation.rules.dataset_rules import validate_duplicate_claim_ids
except ImportError:

    def validate_duplicate_claim_ids(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Fallback used in red phase until dataset duplicate rule is implemented."""
        return []


def test_duplicate_claim_id_detected_for_each_duplicate_occurrence(
    claim_factory: Any,
) -> None:
    """FR-2: each duplicate claim occurrence emits CONFLICT_DUPLICATE_CLAIM_ID."""
    claims_batch = [
        claim_factory(claim_id="C-3001"),
        claim_factory(claim_id="C-3001", patient_id="PAT-002"),
        claim_factory(claim_id="C-3002"),
    ]

    violations = validate_duplicate_claim_ids(claims_batch)
    duplicate_violations = [
        violation
        for violation in violations
        if violation.get("code") == "CONFLICT_DUPLICATE_CLAIM_ID"
    ]

    assert len(duplicate_violations) == 2
    assert all(
        violation.get("claim_id") == "C-3001" for violation in duplicate_violations
    )


def test_multi_duplicate_groups_emit_violation_for_every_occurrence(
    claim_factory: Any,
) -> None:
    """Edge case: multiple duplicate groups emit occurrences for all duplicated rows."""
    claims_batch = [
        claim_factory(claim_id="C-4001"),
        claim_factory(claim_id="C-4001", patient_id="PAT-002"),
        claim_factory(claim_id="C-4001", patient_id="PAT-003"),
        claim_factory(claim_id="C-4002"),
        claim_factory(claim_id="C-4002", provider_id="PRV-002"),
    ]

    violations = validate_duplicate_claim_ids(claims_batch)
    duplicate_violations = [
        violation
        for violation in violations
        if violation.get("code") == "CONFLICT_DUPLICATE_CLAIM_ID"
    ]
    grouped_claim_counts = Counter(
        violation.get("claim_id") for violation in duplicate_violations
    )

    assert len(duplicate_violations) == 5
    assert grouped_claim_counts["C-4001"] == 3
    assert grouped_claim_counts["C-4002"] == 2
