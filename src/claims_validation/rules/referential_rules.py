"""Row-level referential integrity validation rules."""

from __future__ import annotations

from typing import Any, Callable, Mapping

from claims_validation.reporting import build_error_record
from claims_validation.types import NOT_FOUND_PATIENT, NOT_FOUND_PROVIDER, Violation


def validate_patient_reference_exists(
    claim: Mapping[str, Any],
    patient_reference_ids: set[str],
) -> list[Violation]:
    """Validate that patient_id exists in the provided reference ID set."""
    patient_id = claim.get("patient_id")
    if patient_id not in patient_reference_ids:
        return [
            build_error_record(
                code=NOT_FOUND_PATIENT,
                details={
                    "claim_id": claim.get("claim_id"),
                    "field": "patient_id",
                    "value": patient_id,
                },
            )
        ]
    return []


def validate_provider_reference_exists(
    claim: Mapping[str, Any],
    provider_reference_ids: set[str],
) -> list[Violation]:
    """Validate that provider_id exists in the provided reference ID set."""
    provider_id = claim.get("provider_id")
    if provider_id not in provider_reference_ids:
        return [
            build_error_record(
                code=NOT_FOUND_PROVIDER,
                details={
                    "claim_id": claim.get("claim_id"),
                    "field": "provider_id",
                    "value": provider_id,
                },
            )
        ]
    return []


def build_patient_reference_rule(
    patient_reference_ids: set[str],
) -> Callable[[Mapping[str, Any]], list[Violation]]:
    """Bind patient reference IDs to a row-rule callable."""

    def _rule(claim: Mapping[str, Any]) -> list[Violation]:
        return validate_patient_reference_exists(claim, patient_reference_ids)

    _rule.__name__ = "validate_patient_reference_exists"
    return _rule


def build_provider_reference_rule(
    provider_reference_ids: set[str],
) -> Callable[[Mapping[str, Any]], list[Violation]]:
    """Bind provider reference IDs to a row-rule callable."""

    def _rule(claim: Mapping[str, Any]) -> list[Violation]:
        return validate_provider_reference_exists(claim, provider_reference_ids)

    _rule.__name__ = "validate_provider_reference_exists"
    return _rule
