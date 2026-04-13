"""Tests for row-rule registry wiring and deterministic ordering."""

from __future__ import annotations

from claims_validation.rules.registry import get_row_rules


def test_get_row_rules_returns_expected_rule_order() -> None:
    """Registry should expose amount rule first, then date ordering rule."""
    rules = get_row_rules()

    assert len(rules) == 2
    assert rules[0].__name__ == "validate_amount_positive"
    assert rules[1].__name__ == "validate_submitted_after_claim"
