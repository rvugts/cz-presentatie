"""Red-phase tests for Section 9 JSON error contract and code categories."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from claims_validation.rules.amount_rules import validate_amount_positive
from claims_validation.rules.dataset_rules import validate_duplicate_claim_ids
from claims_validation.rules.date_rules import validate_submitted_after_claim
from claims_validation.rules.referential_rules import (
    validate_patient_reference_exists,
    validate_provider_reference_exists,
)


def _assert_required_error_contract(error_record: dict[str, Any]) -> None:
    """Assert the required Section 9.1 fields for each emitted error record."""
    assert set(error_record).issuperset({"code", "message", "details", "request_id"})
    assert isinstance(error_record["code"], str) and error_record["code"]
    assert isinstance(error_record["message"], str) and error_record["message"]
    assert isinstance(error_record["details"], dict)
    assert isinstance(error_record["request_id"], str) and error_record["request_id"]


@pytest.mark.parametrize(
    ("rule_name", "producer"),
    [
        (
            "negative_amount",
            lambda claim_factory, patient_reference_ids, provider_reference_ids: validate_amount_positive(
                claim_factory(claim_id="C-9001", amount=-1.0)
            ),
        ),
        (
            "invalid_date_order",
            lambda claim_factory, patient_reference_ids, provider_reference_ids: validate_submitted_after_claim(
                claim_factory(
                    claim_id="C-9002",
                    claim_date=claim_factory().get("submitted_date"),
                    submitted_date=claim_factory().get("claim_date"),
                )
            ),
        ),
        (
            "missing_patient_reference",
            lambda claim_factory, patient_reference_ids, provider_reference_ids: validate_patient_reference_exists(
                claim_factory(claim_id="C-9003", patient_id="PAT-UNKNOWN"),
                patient_reference_ids,
            ),
        ),
        (
            "missing_provider_reference",
            lambda claim_factory, patient_reference_ids, provider_reference_ids: validate_provider_reference_exists(
                claim_factory(claim_id="C-9004", provider_id="PRV-UNKNOWN"),
                provider_reference_ids,
            ),
        ),
        (
            "duplicate_claim_conflict",
            lambda claim_factory, patient_reference_ids, provider_reference_ids: validate_duplicate_claim_ids(
                [
                    claim_factory(claim_id="C-9005"),
                    claim_factory(claim_id="C-9005", patient_id="PAT-002"),
                ]
            ),
        ),
    ],
)
def test_error_records_include_required_json_contract_fields(
    rule_name: str,
    producer: Callable[[Any, set[str], set[str]], list[dict[str, Any]]],
    claim_factory: Any,
    patient_reference_ids: set[str],
    provider_reference_ids: set[str],
) -> None:
    """Task 9 red test: each emitted record must satisfy Section 9.1 contract."""
    error_records = producer(claim_factory, patient_reference_ids, provider_reference_ids)

    assert error_records, f"Expected at least one error record for scenario: {rule_name}"
    for error_record in error_records:
        _assert_required_error_contract(error_record)


@pytest.mark.parametrize(
    ("code", "expected_prefix"),
    [
        ("VALIDATION_NEGATIVE_AMOUNT", "VALIDATION_"),
        ("VALIDATION_INVALID_DATE_ORDER", "VALIDATION_"),
        ("NOT_FOUND_PATIENT", "NOT_FOUND_"),
        ("NOT_FOUND_PROVIDER", "NOT_FOUND_"),
        ("CONFLICT_DUPLICATE_CLAIM_ID", "CONFLICT_"),
        ("SERVER_UNEXPECTED_EXCEPTION", "SERVER_"),
    ],
)
def test_error_code_prefix_matches_category_convention(code: str, expected_prefix: str) -> None:
    """Task 9 red test: Section 9.2 category names must use stable code prefixes."""
    assert code.startswith(expected_prefix)
