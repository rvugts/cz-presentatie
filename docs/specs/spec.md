#### demo.providers

| Column        | Type   | Description |
|---------------|--------|-------------|
| provider_id   | string | Unique provider identifier |
| provider_type | string | Provider type/category |

#### demo.claims

| Column          | Type   | Description |
|-----------------|--------|-------------|
| claim_id        | string | Unique claim identifier |
| patient_id      | string | Foreign key to patient |
| provider_id     | string | Foreign key to provider |
| treatment_code  | string | Procedure or treatment code |
| amount          | double | Claimed amount |
| claim_date      | date   | Date of service |
| submitted_date  | date   | Submission date |
| status          | string | Claim lifecycle status |

*See Databricks Catalog Explorer for authoritative schema and sample data.*
# Specification: Claims Data Quality Validator

---

## 1. Project Overview

This project aims to build a **data quality validation system** for healthcare insurance claims.

The system is intended to validate enterprise data already stored in Databricks schemas,
including existing tables such as `demo.claims`, `demo.patients`, and `demo.providers`.

The system validates incoming claims data against:
- Structural rules
- Business rules
- Data integrity constraints

The goal is to **detect invalid, suspicious, or inconsistent claims early** before downstream processing (approval, payment, analytics).

This system is designed for use in a **data platform environment (Azure / Databricks / dbt)** and supports both batch and scalable processing.

---

## 2. Objectives

### Business Goals
- Prevent incorrect claim payouts
- Improve data quality for analytics and reporting
- Detect anomalies and potential fraud patterns early

### Technical Goals
Provide a Python script (`scripts/run_claims_validation_from_tables.py`) that reads claims and patient data directly from hardcoded Databricks tables (e.g., `workspace.demo.claims`, `workspace.demo.patients`) using Spark, and runs the validation logic in memory. The script must not require file-based input.

---

## 3. Target Users

### Primary Users
- Data Engineers (Databricks / PySpark / dbt)
- BI Engineers (SQL / Power BI)

### Expectations
- Clear validation output (what is wrong and why)
- Easy integration into pipelines
- Scalable to large datasets
- Transparent and explainable rules

---

## 4. Scope

### In Scope
  - Duplicate claims
  - Invalid amounts
  - Invalid dates
  - Referential integrity issues
  - Business rule violations

### Out of Scope (Non-Goals)
- Real-time streaming validation
- Full fraud detection system
- UI/dashboard development
- Payment processing
- Re-designing or replacing existing enterprise Databricks schemas

---

## 5. Functional Requirements

The system must:

1. Validate claim records individually
2. Validate dataset-level constraints (e.g. duplicates)
3. Produce a list of validation errors per claim
4. Support multiple validation rules:
   - Amount must be > 0
   - Claim date cannot be in the future
   - Submitted date must be >= claim date
   - Claim IDs must be unique
   - Patient must exist
5. Support extensible rule definitions

---

## 6. Non-Functional Requirements (NFRs)

- **Performance**: Handle datasets up to millions of records (via PySpark)
- **Scalability**: Must work in distributed environment (Databricks)
- **Maintainability**: Rules must be easy to extend
- **Observability**: Clear logging of validation results
- **Reliability**: Deterministic validation results
- **Security**: No exposure of sensitive data in logs

---

## 7. Data & Domain Model

### Entities

#### Claim
- claim_id (string)
- patient_id (string)
- provider_id (string)
- treatment_code (string)
- amount (float)
- claim_date (date)
- submitted_date (date)
- status (string)

#### Patient
- patient_id (string)
- birth_date (date)
- insurance_type (string)

#### Provider
- provider_id (string)
- provider_type (string)

---

### Databricks Table Schemas

#### demo.patients

| Column          | Type   | Description |
|-----------------|--------|-------------|
| patient_id      | string | Unique patient identifier |
| birth_date      | date   | Patient birth date |
| insurance_type  | string | Insurance policy classification |

*See Databricks Catalog Explorer for authoritative schema and sample data.*

---

## 8. Technical Architecture

### Components

1. **Validation Engine (Python)**
   - Applies rule-based validation per record

2. **SQL Validation Layer**
   - Dataset-level checks (duplicates, joins)

3. **PySpark Layer**
   - Scalable validation for large datasets

### Interaction

- Data loaded from existing Databricks tables and schemas
- Primary enterprise integration target includes schema tables such as `demo.claims` and
   `demo.patients`
- Validation rules applied
- Output stored or returned as error report

---

## 9. Deployment Architecture

- Runs in Azure Databricks environment
- Python validation runs as notebook or job
- SQL checks executed in Databricks SQL or dbt

spark = SparkSession.builder.getOrCreate()
### Databricks Execution & Usage

The validator must be runnable as a Python script (`scripts/run_claims_validation_from_tables.py`) in the Databricks environment, with all table and schema names hardcoded for the workspace `https://dbc-a070d6b0-c1c0.cloud.databricks.com` and schema `demo`.

**Execution contract:**
- The script reads claims from `workspace.demo.claims` and patients from `workspace.demo.patients` using Spark DataFrame APIs.
- No file-based input is required or supported for the main validation flow.
- The script runs the validation logic in memory and writes the output (validation errors) to a new or existing Databricks table (e.g., `workspace.demo.validation_report`) or to DBFS as a JSON file.

**Example usage:**

```python
from pyspark.sql import SparkSession
from claims_validation.engine import ValidationEngine
from claims_validation.reporting import build_error_report
from claims_validation.rules.registry import default_registry

spark = SparkSession.builder.getOrCreate()
claims_df = spark.table("workspace.demo.claims")
patients_df = spark.table("workspace.demo.patients")
claims = [row.asDict(recursive=True) for row in claims_df.collect()]
patient_ids = {str(row["patient_id"]) for row in patients_df.select("patient_id").collect()}

engine = ValidationEngine(
    row_rules=default_registry().row_rules(),
    dataset_rules=default_registry().dataset_rules(),
)
errors = engine.validate_claims(claims, patient_ids)
report = build_error_report(errors)

# Write to Databricks table or DBFS
report_df = spark.createDataFrame(report)
report_df.write.mode("overwrite").saveAsTable("workspace.demo.validation_report")
# or
# with open("/dbfs/tmp/validation_report.json", "w") as f:
#     import json; json.dump(report, f, indent=2)
```

**How to run:**
1. Submit the script as a Databricks job or run in a Databricks notebook cell.
2. Ensure the cluster has access to the `demo` schema and required Python dependencies.
3. Output will be available in the specified Databricks table or DBFS path.

**Dependencies and setup:**
- `databricks.yml` defines workspace and target metadata.
- Use the Databricks VS Code extension/workflow for workspace authentication and development.
- All table/schema/workspace names are hardcoded for demo/enterprise reproducibility.

---

## 10. Technology Stack

- Python
- PySpark
- SQL
- Databricks
- Azure Data Platform

---

## 11. Architecture Patterns

- Layered validation:
  - Row-level validation (Python)
  - Dataset-level validation (SQL)
- Rule-based validation engine
- Separation of concerns between data processing and validation

---

## 12. CI/CD Requirements

- Unit tests must pass before deployment
- Validation logic must be version-controlled
- Automated test execution (pytest)

---

## 13. Invariants

These rules must NEVER be violated:

- Claim amount must be non-negative
- Claim must reference a valid patient
- Claim IDs must be unique
- Dates must follow logical order

---

## 14. ADRs (Architecture Decision Records)

### ADR-001: Use Python for validation logic
- **Decision**: Use Python for core validation
- **Context**: Flexible and easy to extend
- **Alternative**: Pure SQL
- **Consequence**: Requires integration with Spark

### ADR-002: Use SQL for dataset validation
- **Decision**: Use SQL for aggregation checks
- **Context**: Efficient for duplicates and joins
- **Consequence**: Split logic across layers

---

## 15. Phases

### MVP
- Basic validation rules
- Python validator
- SQL queries

### Phase 1
- Extend rule set
- Add PySpark support

### Phase 2
- Integration into pipelines
- Monitoring and logging

---

## 16. Acceptance Criteria

- Validator detects all injected data issues
- Tests validate all rules
- SQL queries correctly identify duplicates and invalid references
- Output clearly explains validation failures

---

## 17. Success Metrics

- % of invalid records detected
- Reduction in downstream data errors
- Developer adoption of validation framework

---

## 18. Risks & Trade-offs

### Risks
- Incomplete rule coverage
- Performance issues on large datasets
- Misinterpretation of business rules

### Trade-offs
- Python flexibility vs SQL performance
- Simplicity vs completeness

---

## 19. Open Questions

- Should validation results be stored or only logged?
- How should rules be configured (code vs config)?
- How to integrate with dbt models?
