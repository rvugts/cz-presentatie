"""Reporting helpers for canonical validation error records."""

from __future__ import annotations

from uuid import uuid4

from claims_validation.types import ERROR_MESSAGES, SERVER_UNEXPECTED_EXCEPTION, Violation


def build_error_record(
    *,
    code: str,
    details: dict[str, object],
    request_id: str | None = None,
) -> Violation:
    """Build a JSON-compatible canonical error record for Section 9 contract."""
    resolved_request_id = request_id or str(uuid4())
    message = ERROR_MESSAGES.get(code, ERROR_MESSAGES[SERVER_UNEXPECTED_EXCEPTION])
    record: Violation = {
        "code": code,
        "message": message,
        "details": details,
        "request_id": resolved_request_id,
    }

    # Keep claim_id at top-level for compatibility with existing rule tests and callers.
    claim_id = details.get("claim_id")
    if claim_id is not None:
        record["claim_id"] = claim_id

    return record