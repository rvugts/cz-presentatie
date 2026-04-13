# Task 1 Baseline Module Map

## Purpose
Canonical file path map for Tasks 2-4 and downstream implementation tasks, based on:
- `docs/specs/spec.md`
- `docs/specs/tasks.md`
- current repository structure

Task 1 is documentation-only. No validation business logic is implemented here.

## Current Baseline (as-is)

- Existing source root: `src/`
- Existing Python package placeholder: `src/__init__.py`
- Existing scripts folder: `scripts/`
- Existing scripts (non-validator):
  - `scripts/append-makefile.py`
  - `scripts/append-precommit.py`
  - `scripts/databricks_mcp_server.py`
- Tests root does not currently exist: `tests/` (missing)

## Canonical Target Paths

The following paths are the authoritative locations for Tasks 2-4 (and aligned with later tasks in `docs/specs/tasks.md`).

### 1) Validation engine
- `src/claims_validation/engine.py`

### 2) Row rules and dataset rules
- `src/claims_validation/rules/amount_rules.py`
- `src/claims_validation/rules/date_rules.py`
- `src/claims_validation/rules/dataset_rules.py`

### 3) Rule registry
- `src/claims_validation/rules/registry.py`

### 4) Reporting transformer
- `src/claims_validation/reporting.py`

### 5) Databricks runner script
- `scripts/run_claims_validation_from_tables.py`

### 6) Supporting package files (required for imports)
- `src/claims_validation/__init__.py`
- `src/claims_validation/rules/__init__.py`
- `src/claims_validation/types.py`

### 7) Test locations (unit, integration, performance)

Unit tests (Task 2-4 start here):
- `tests/claims_validation/test_amount_rules.py`
- `tests/claims_validation/test_date_rules.py`
- `tests/claims_validation/test_dataset_rules.py`
- `tests/claims_validation/test_registry.py`
- `tests/claims_validation/test_engine.py`
- `tests/claims_validation/test_reporting.py`
- `tests/claims_validation/conftest.py`

Integration tests:
- `tests/integration/test_run_claims_validation_from_tables.py`

Performance tests:
- `tests/performance/test_validation_runtime.py`

## Path Decisions

1. Package namespace is `claims_validation` under `src/`.
- Rationale: aligns with spec examples and expected imports (engine, rules registry, reporting).

2. Rule modules are split by concern under `src/claims_validation/rules/`.
- Rationale: supports FR-7 extensibility and clear TDD sequencing for Tasks 3-8.

3. Runner remains in `scripts/` and not in package modules.
- Rationale: matches CLI contract in spec and Task 12 output path.

4. Test suite is rooted at `tests/` with domain and test-type separation.
- Rationale: enables Task 2 fixture scaffolding and clear unit vs integration vs performance boundaries.

## Task 2-4 Start Set (Minimal)

Task 2 should create first:
- `tests/claims_validation/conftest.py`
- `tests/claims_validation/test_amount_rules.py`
- `tests/claims_validation/test_date_rules.py`
- `tests/claims_validation/test_dataset_rules.py`

Task 3 should add failing tests in:
- `tests/claims_validation/test_amount_rules.py`
- `tests/claims_validation/test_date_rules.py`

Task 4 should implement minimal code in:
- `src/claims_validation/rules/amount_rules.py`
- `src/claims_validation/rules/date_rules.py`
- `src/claims_validation/rules/registry.py`

## Verification Checklist (Task 1)

- [x] Validation engine has an explicit target path.
- [x] Row rules and dataset rules have explicit target paths.
- [x] Rule registry has an explicit target path.
- [x] Reporting transformer has an explicit target path.
- [x] Databricks runner script has an explicit target path.
- [x] Unit/integration/performance tests have explicit target paths.
- [x] Task 2 can begin from documented test paths without additional discovery.
- [x] No business logic implementation files were modified for Task 1.
