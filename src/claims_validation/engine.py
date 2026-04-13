"""Validation engine orchestration for row and dataset rule execution."""

from __future__ import annotations

from typing import Any, Mapping

from claims_validation.rules.registry import get_dataset_rules, get_row_rules
from claims_validation.types import Violation


class ValidationEngine:
    """Orchestrate registered row and dataset rules for a claims batch."""

    @staticmethod
    def validate_claims(
        claims: list[Mapping[str, Any]],
        patient_ids: set[str],
        provider_ids: set[str],
    ) -> list[Violation]:
        """Run row rules first, then dataset rules, and return aggregated violations.

        :param claims: Claim payloads to validate.
        :param patient_ids: Known patient IDs for referential checks.
        :param provider_ids: Known provider IDs for referential checks.
        :return: Aggregated violations in deterministic execution order.
        """
        row_rules = get_row_rules(
            patient_reference_ids=patient_ids,
            provider_reference_ids=provider_ids,
        )
        dataset_rules = get_dataset_rules()

        violations: list[Violation] = []

        for claim in claims:
            for row_rule in row_rules:
                violations.extend(row_rule(claim))

        for dataset_rule in dataset_rules:
            violations.extend(dataset_rule(claims))

        return violations


def validate_claims(
    claims: list[Mapping[str, Any]],
    patient_ids: set[str],
    provider_ids: set[str],
) -> list[Violation]:
    """Convenience function for validating claims through ``ValidationEngine``."""
    return ValidationEngine.validate_claims(
        claims=claims,
        patient_ids=patient_ids,
        provider_ids=provider_ids,
    )
