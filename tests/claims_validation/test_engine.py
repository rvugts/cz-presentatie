"""Validation engine orchestration tests for FR-1 and FR-7."""

from __future__ import annotations

from datetime import date
from typing import Any

from claims_validation.engine import ValidationEngine, validate_claims


def test_validate_claims_aggregates_row_and_dataset_violations_in_order(
    claim_factory: Any,
    patient_reference_ids: set[str],
    provider_reference_ids: set[str],
) -> None:
    """Engine should aggregate row and dataset violations for mixed-validity batches."""
    claims = [
        claim_factory(claim_id="C-DUP-1"),
        claim_factory(
            claim_id="C-DUP-1",
            amount=-5.0,
            claim_date=date(2026, 4, 3),
            submitted_date=date(2026, 4, 2),
            patient_id="PAT-MISSING",
            provider_id="PRV-MISSING",
        ),
        claim_factory(claim_id="C-VALID-3", patient_id="PAT-002", provider_id="PRV-002"),
    ]

    violations = ValidationEngine.validate_claims(
        claims=claims,
        patient_ids=patient_reference_ids,
        provider_ids=provider_reference_ids,
    )

    assert [violation["code"] for violation in violations] == [
        "VALIDATION_NEGATIVE_AMOUNT",
        "VALIDATION_INVALID_DATE_ORDER",
        "NOT_FOUND_PATIENT",
        "NOT_FOUND_PROVIDER",
        "CONFLICT_DUPLICATE_CLAIM_ID",
        "CONFLICT_DUPLICATE_CLAIM_ID",
    ]
    assert [violation["claim_id"] for violation in violations] == [
        "C-DUP-1",
        "C-DUP-1",
        "C-DUP-1",
        "C-DUP-1",
        "C-DUP-1",
        "C-DUP-1",
    ]


def test_validate_claims_is_registry_driven_and_extensible(monkeypatch: Any) -> None:
    """Engine should orchestrate whichever rules are returned by the registry."""

    def custom_row_rule(claim: dict[str, Any]) -> list[dict[str, Any]]:
        return [{"code": "ROW_CUSTOM", "claim_id": claim["claim_id"]}]

    def custom_dataset_rule(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{"code": "DATASET_CUSTOM", "claim_id": claims[0]["claim_id"]}]

    monkeypatch.setattr("claims_validation.engine.get_row_rules", lambda patient_reference_ids, provider_reference_ids: (custom_row_rule,))
    monkeypatch.setattr("claims_validation.engine.get_dataset_rules", lambda: (custom_dataset_rule,))

    violations = validate_claims(
        claims=[{"claim_id": "C-EXT-1"}],
        patient_ids={"PAT-001"},
        provider_ids={"PRV-001"},
    )

    assert violations == [
        {"code": "ROW_CUSTOM", "claim_id": "C-EXT-1"},
        {"code": "DATASET_CUSTOM", "claim_id": "C-EXT-1"},
    ]
