"""Red-phase tests for referential integrity row rules (FR-5)."""

from __future__ import annotations

from typing import Any

try:
    from claims_validation.rules.referential_rules import (
        validate_patient_reference_exists,
        validate_provider_reference_exists,
    )
except ImportError:

    def validate_patient_reference_exists(
        claim: dict[str, Any],
        patient_reference_ids: set[str],
    ) -> list[dict[str, Any]]:
        """Fallback used in red phase until referential rules are implemented."""
        return []

    def validate_provider_reference_exists(
        claim: dict[str, Any],
        provider_reference_ids: set[str],
    ) -> list[dict[str, Any]]:
        """Fallback used in red phase until referential rules are implemented."""
        return []


def test_missing_patient_reference_detected(
    claim_factory: Any,
    patient_reference_ids: set[str],
) -> None:
    """FR-5: unknown patient_id must emit NOT_FOUND_PATIENT with claim context."""
    invalid_claim = claim_factory(claim_id="C-2001", patient_id="PAT-999")

    violations = validate_patient_reference_exists(invalid_claim, patient_reference_ids)

    assert len(violations) == 1
    assert violations[0]["code"] == "NOT_FOUND_PATIENT"
    assert violations[0]["claim_id"] == invalid_claim["claim_id"]


def test_missing_provider_reference_detected(
    claim_factory: Any,
    provider_reference_ids: set[str],
) -> None:
    """FR-5: unknown provider_id must emit NOT_FOUND_PROVIDER with claim context."""
    invalid_claim = claim_factory(claim_id="C-2002", provider_id="PRV-999")

    violations = validate_provider_reference_exists(invalid_claim, provider_reference_ids)

    assert len(violations) == 1
    assert violations[0]["code"] == "NOT_FOUND_PROVIDER"
    assert violations[0]["claim_id"] == invalid_claim["claim_id"]
