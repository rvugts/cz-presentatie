# Implementation Tasks

**Spec:** docs/specs/spec.md
**Generated:** 2026-04-13
**Total tasks:** 14

---

## Execution Order

1. Task 1: Validate project baseline and target modules
2. Task 2: Establish validation test scaffolding
3. Task 3: Write failing unit tests for amount and date rules
4. Task 4: Implement amount and date row rules
5. Task 5: Write failing tests for patient and provider reference checks
6. Task 6: Implement referential integrity row rules
7. Task 7: Write failing tests for duplicate claim ID detection
8. Task 8: Implement dataset duplicate claim ID rule
9. Task 9: Write failing tests for JSON error contract and codes
10. Task 10: Implement error model and reporting transformer
11. Task 11: Integrate rule registry and validation engine orchestration
12. Task 12: Implement Databricks runner script and DBFS JSON sink
13. Task 13: Add integration and performance tests for full flow
14. Task 14: Finalize documentation and quality gates

---

## Tasks

### Task 1: Validate project baseline and target modules

**Category:** Setup

**Description:**
Confirm module locations, existing validation package structure, and where the runner script and tests should live before any functional work begins.

**Spec reference:**
Section 5, Section 6.2, Section 8.2, Section 10.1

**Inputs:**
- docs/specs/spec.md
- Existing repository structure

**Outputs:**
- docs/specs/tasks.md (execution source of truth)
- Initial target file list captured in implementation notes or PR description

**Acceptance criteria:**
- [ ] Target code and test paths are identified for engine, rules, reporting, and runner.
- [ ] No ambiguity remains about where new tests and modules will be added.

**Dependencies:**
- None

**Prompt hint:**
Map the spec components to exact file paths and list the minimal set of files to touch first.

---

### Task 2: Establish validation test scaffolding

**Category:** Testing

**Description:**
Create or standardize pytest fixtures and shared test data builders for claims, patient IDs, and provider IDs.

**Spec reference:**
Section 3.2 (Maintainability), Section 11.1

**Inputs:**
- Task 1 file map
- Existing pytest configuration

**Outputs:**
- tests fixtures module for claims and reference sets
- Baseline test module skeletons for row and dataset rules

**Acceptance criteria:**
- [ ] Test fixtures provide reusable valid claim data and targeted invalid variants.
- [ ] Test modules run successfully with empty placeholder tests.

**Dependencies:**
- Task 1

**Prompt hint:**
Create reusable pytest fixtures for valid claims and reference sets, then verify test discovery passes.

---

### Task 3: Write failing unit tests for amount and date rules

**Category:** Testing

**Description:**
Write red-phase tests for amount non-negative and claim date ordering behavior.

**Spec reference:**
Section 3.1 (FR-3, FR-4), Section 4.2, Section 11.1

**Inputs:**
- Task 2 fixtures

**Outputs:**
- Unit tests for negative amount rejection
- Unit tests for zero amount acceptance
- Unit tests for invalid claim/submitted date ordering

**Acceptance criteria:**
- [ ] Tests clearly assert expected error codes and claim context.
- [ ] New tests fail before rule implementation.

**Dependencies:**
- Task 2

**Prompt hint:**
Write failing pytest cases for amount and date rules using explicit expected error codes.

---

### Task 4: Implement amount and date row rules

**Category:** Validation

**Description:**
Implement row-level rules so amount and date tests pass with deterministic behavior.

**Spec reference:**
Section 3.1 (FR-3, FR-4), Section 13

**Inputs:**
- Task 3 failing tests
- Rule registry design from Section 6

**Outputs:**
- Row rule implementations for amount and date checks
- Updated rule registration to include these rules

**Acceptance criteria:**
- [ ] All Task 3 tests pass.
- [ ] Rule outputs use specified codes: VALIDATION_NEGATIVE_AMOUNT and VALIDATION_INVALID_DATE_ORDER.

**Dependencies:**
- Task 3

**Prompt hint:**
Implement minimal row rules to satisfy amount and date tests, then refactor for clarity.

---

### Task 5: Write failing tests for patient and provider reference checks

**Category:** Testing

**Description:**
Write red-phase tests for missing patient and provider reference handling.

**Spec reference:**
Section 3.1 (FR-5), Section 4.2, Section 11.1

**Inputs:**
- Task 2 fixtures

**Outputs:**
- Unit tests for NOT_FOUND_PATIENT
- Unit tests for NOT_FOUND_PROVIDER

**Acceptance criteria:**
- [ ] Tests fail before referential rule implementation.
- [ ] Assertions include both error code and claim identifier context.

**Dependencies:**
- Task 2

**Prompt hint:**
Add failing tests for missing patient and provider references with code-level assertions.

---

### Task 6: Implement referential integrity row rules

**Category:** Validation

**Description:**
Implement row-level reference checks against provided patient and provider ID sets.

**Spec reference:**
Section 3.1 (FR-5), Section 7.1, Section 13

**Inputs:**
- Task 5 failing tests
- Reference ID inputs in engine contract

**Outputs:**
- Referential integrity rule implementation
- Registry updates to include reference checks

**Acceptance criteria:**
- [ ] Task 5 tests pass.
- [ ] Missing references emit NOT_FOUND_PATIENT or NOT_FOUND_PROVIDER as appropriate.

**Dependencies:**
- Task 5

**Prompt hint:**
Implement patient and provider existence checks using injected ID sets from the engine.

---

### Task 7: Write failing tests for duplicate claim ID detection

**Category:** Testing

**Description:**
Create dataset-level tests that enforce claim_id uniqueness within a batch.

**Spec reference:**
Section 3.1 (FR-2), Section 4.2, Section 13

**Inputs:**
- Task 2 fixtures

**Outputs:**
- Dataset rule test module for duplicate claim IDs

**Acceptance criteria:**
- [ ] Tests fail before duplicate rule implementation.
- [ ] Tests assert CONFLICT_DUPLICATE_CLAIM_ID for each duplicate occurrence.

**Dependencies:**
- Task 2

**Prompt hint:**
Write failing dataset tests for duplicate claim IDs, including multi-duplicate edge cases.

---

### Task 8: Implement dataset duplicate claim ID rule

**Category:** Core Logic

**Description:**
Implement dataset-level duplicate detection and violation emission for repeated claim IDs.

**Spec reference:**
Section 3.1 (FR-2), Section 6.1, Section 13

**Inputs:**
- Task 7 failing tests

**Outputs:**
- Dataset duplicate rule implementation
- Registry updates for dataset rules

**Acceptance criteria:**
- [ ] Task 7 tests pass.
- [ ] Duplicate detection is deterministic for identical input order and content.

**Dependencies:**
- Task 7

**Prompt hint:**
Implement deterministic batch duplicate detection for claim_id and wire it into dataset rules.

---

### Task 9: Write failing tests for JSON error contract and codes

**Category:** Testing

**Description:**
Write tests that lock the error object schema and required fields.

**Spec reference:**
Section 9.1, Section 9.2, Section 11.2

**Inputs:**
- Existing error output paths and rule outputs

**Outputs:**
- Tests validating code, message, details, and request_id structure

**Acceptance criteria:**
- [ ] Tests fail until reporting output matches contract.
- [ ] Tests enforce category-consistent code names.

**Dependencies:**
- Task 4, Task 6, Task 8

**Prompt hint:**
Create failing tests that enforce the JSON error schema and stable error code patterns.

---

### Task 10: Implement error model and reporting transformer

**Category:** Core Logic

**Description:**
Implement or update reporting logic that converts validation violations into the canonical JSON error contract.

**Spec reference:**
Section 3.1 (FR-6), Section 6.2, Section 9

**Inputs:**
- Task 9 failing tests
- Rule outputs from Tasks 4, 6, and 8

**Outputs:**
- Error model definitions
- Reporting transformer to JSON-compatible records

**Acceptance criteria:**
- [ ] Task 9 tests pass.
- [ ] Output contains required fields for each violation.

**Dependencies:**
- Task 9

**Prompt hint:**
Implement a reporting transformer that maps all violations to the Section 9 JSON contract.

---

### Task 11: Integrate rule registry and validation engine orchestration

**Category:** Core Logic

**Description:**
Finalize engine orchestration so row and dataset rules execute in one run and aggregate all violations.

**Spec reference:**
Section 3.1 (FR-1, FR-7), Section 6.2, Section 8.2

**Inputs:**
- Tasks 4, 6, 8 implementations
- Existing engine interface

**Outputs:**
- Updated validation engine orchestration
- Registry integration for row and dataset rule lists

**Acceptance criteria:**
- [ ] Engine processes mixed-validity batches and returns aggregated violations.
- [ ] Rule additions remain possible without changing orchestration logic.

**Dependencies:**
- Task 4, Task 6, Task 8

**Prompt hint:**
Wire row and dataset rules into a single deterministic engine execution path.

---

### Task 12: Implement Databricks runner script and DBFS JSON sink

**Category:** API/Interface

**Description:**
Implement script-level orchestration to load source tables, run validation, and write JSON output to DBFS.

**Spec reference:**
Section 3.1 (FR-6), Section 6.4, Section 8.2, Section 12

**Inputs:**
- Task 10 reporting output
- Task 11 engine orchestration

**Outputs:**
- scripts/run_claims_validation_from_tables.py
- DBFS write path handling for /dbfs/tmp/validation_report.json

**Acceptance criteria:**
- [ ] Script reads workspace.demo.claims, workspace.demo.patients, and workspace.demo.providers.
- [ ] Script writes JSON output to DBFS default path and exits with expected codes.

**Dependencies:**
- Task 10, Task 11

**Prompt hint:**
Build the Databricks runner script that reads hardcoded tables and writes JSON validation output to DBFS.

---

### Task 13: Add integration and performance tests for full flow

**Category:** Testing

**Description:**
Add end-to-end and performance-oriented tests covering script execution contract and runtime target.

**Spec reference:**
Section 3.2 (Performance), Section 11.2, Section 11.3, Section 12

**Inputs:**
- Task 12 runner script
- Existing test harness

**Outputs:**
- Integration tests for full validation flow
- Performance test definition for 5 million claim baseline target

**Acceptance criteria:**
- [ ] End-to-end test verifies output schema and sink behavior.
- [ ] Performance test or benchmark harness verifies target under defined baseline assumptions.

**Dependencies:**
- Task 12

**Prompt hint:**
Create integration and performance tests that validate runtime behavior and output contract.

---

### Task 14: Finalize documentation and quality gates

**Category:** Documentation

**Description:**
Document execution, error codes, and rule extension workflow; verify linting, tests, and coverage threshold.

**Spec reference:**
Section 10, Section 12, Section 15

**Inputs:**
- Completed implementation and tests from Tasks 1-13

**Outputs:**
- Updated project documentation (execution and extension guidance)
- Verified quality gate results (tests, coverage, lint)

**Acceptance criteria:**
- [ ] Documentation explains how to run validator and interpret errors.
- [ ] Coverage for validation modules meets or exceeds 80%.
- [ ] Linting and automated tests pass.

**Dependencies:**
- Task 13

**Prompt hint:**
Finalize docs and verify all quality gates before declaring implementation complete.

---

## Coverage Check

- FR-1: Task 11, Task 12
- FR-2: Task 7, Task 8
- FR-3: Task 3, Task 4
- FR-4: Task 3, Task 4
- FR-5: Task 5, Task 6
- FR-6: Task 10, Task 12, Task 13
- FR-7: Task 11
