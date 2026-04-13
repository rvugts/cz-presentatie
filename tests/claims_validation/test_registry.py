"""Tests for row-rule registry wiring and deterministic ordering."""

from __future__ import annotations

from claims_validation.rules.registry import get_row_rules


def test_get_row_rules_returns_expected_rule_order() -> None:
    """Registry should expose row rules in deterministic FR order."""
    rules = get_row_rules(
        patient_reference_ids={"PAT-001"},
        provider_reference_ids={"PRV-001"},
    )

    assert len(rules) == 4
    assert rules[0].__name__ == "validate_amount_positive"
    assert rules[1].__name__ == "validate_submitted_after_claim"
    assert rules[2].__name__ == "validate_patient_reference_exists"
    assert rules[3].__name__ == "validate_provider_reference_exists"
