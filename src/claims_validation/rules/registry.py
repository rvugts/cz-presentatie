"""Rule registry for claims validation orchestration."""

from __future__ import annotations

from typing import Any, Callable, Mapping

from claims_validation.rules.amount_rules import validate_amount_positive
from claims_validation.rules.date_rules import validate_submitted_after_claim
from claims_validation.types import Violation

RowRule = Callable[[Mapping[str, Any]], list[Violation]]


def get_row_rules() -> tuple[RowRule, ...]:
    """Return row-rule callables in deterministic execution order."""
    return (
        validate_amount_positive,
        validate_submitted_after_claim,
    )
