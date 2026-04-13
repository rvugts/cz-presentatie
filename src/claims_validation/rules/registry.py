"""Rule registry for claims validation orchestration."""

from __future__ import annotations

from typing import Any, Callable, Mapping

from claims_validation.rules.amount_rules import validate_amount_positive
from claims_validation.rules.dataset_rules import validate_duplicate_claim_ids
from claims_validation.rules.date_rules import validate_submitted_after_claim
from claims_validation.rules.referential_rules import (
    build_patient_reference_rule,
    build_provider_reference_rule,
)
from claims_validation.types import Violation

RowRule = Callable[[Mapping[str, Any]], list[Violation]]
DatasetRule = Callable[[list[Mapping[str, Any]]], list[Violation]]


def get_row_rules(
    patient_reference_ids: set[str] | None = None,
    provider_reference_ids: set[str] | None = None,
) -> tuple[RowRule, ...]:
    """Return row-rule callables in deterministic execution order."""
    patient_ids = patient_reference_ids or set()
    provider_ids = provider_reference_ids or set()

    return (
        validate_amount_positive,
        validate_submitted_after_claim,
        build_patient_reference_rule(patient_ids),
        build_provider_reference_rule(provider_ids),
    )


def get_dataset_rules() -> tuple[DatasetRule, ...]:
    """Return dataset-rule callables in deterministic execution order."""
    return (validate_duplicate_claim_ids,)
