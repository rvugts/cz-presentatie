"""Shared types and constants for claims validation rules."""

from __future__ import annotations

from typing import Any

VALIDATION_NEGATIVE_AMOUNT = "VALIDATION_NEGATIVE_AMOUNT"
VALIDATION_INVALID_DATE_ORDER = "VALIDATION_INVALID_DATE_ORDER"

Violation = dict[str, Any]
