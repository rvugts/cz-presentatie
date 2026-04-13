"""Baseline scaffolding tests for dataset validation rules."""

from __future__ import annotations


def test_dataset_scaffolding_exposes_patient_reference_ids(
    patient_reference_ids: set[str],
) -> None:
    """Smoke test to verify patient reference fixtures are available."""
    assert "PAT-001" in patient_reference_ids


def test_dataset_scaffolding_exposes_provider_reference_ids(
    provider_reference_ids: set[str],
) -> None:
    """Smoke test to verify provider reference fixtures are available."""
    assert "PRV-001" in provider_reference_ids
