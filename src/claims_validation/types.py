"""Shared types and constants for claims validation rules."""

from __future__ import annotations

from typing import Any

VALIDATION_NEGATIVE_AMOUNT = "VALIDATION_NEGATIVE_AMOUNT"
VALIDATION_INVALID_DATE_ORDER = "VALIDATION_INVALID_DATE_ORDER"
NOT_FOUND_PATIENT = "NOT_FOUND_PATIENT"
NOT_FOUND_PROVIDER = "NOT_FOUND_PROVIDER"
CONFLICT_DUPLICATE_CLAIM_ID = "CONFLICT_DUPLICATE_CLAIM_ID"
SERVER_UNEXPECTED_EXCEPTION = "SERVER_UNEXPECTED_EXCEPTION"

ERROR_MESSAGES: dict[str, str] = {
	VALIDATION_NEGATIVE_AMOUNT: "Claim amount must be non-negative.",
	VALIDATION_INVALID_DATE_ORDER: "Claim date must be on or before submitted date.",
	NOT_FOUND_PATIENT: "Patient reference was not found.",
	NOT_FOUND_PROVIDER: "Provider reference was not found.",
	CONFLICT_DUPLICATE_CLAIM_ID: "Duplicate claim_id found in batch.",
	SERVER_UNEXPECTED_EXCEPTION: "Unexpected server-side validation error.",
}

Violation = dict[str, Any]
