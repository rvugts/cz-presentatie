# Execute The Validator Against Databricks Tables

This document explains how to run the claims validator against the hardcoded Databricks tables used by the current implementation.

## What The Runner Uses

The runner script is [scripts/run_claims_validation_from_tables.py](/Users/ai-chitect/Development/cz-presentatie/scripts/run_claims_validation_from_tables.py).

It reads these hardcoded tables:

- `workspace.demo.claims`
- `workspace.demo.patients`
- `workspace.demo.providers`

It writes the validation result to:

- `/dbfs/tmp/validation_report.json`

The configured Databricks workspace in this repository is:

- `https://dbc-a070d6b0-c1c0.cloud.databricks.com`

Source: [databricks.yml](/Users/ai-chitect/Development/cz-presentatie/databricks.yml)

## Prerequisites

Before running the validator in Databricks, make sure all of the following are true:

1. Your Databricks workspace is the one configured in [databricks.yml](/Users/ai-chitect/Development/cz-presentatie/databricks.yml).
2. You have access to the `workspace.demo` catalog and schema objects listed above.
3. The repository is available inside Databricks as a Repo or otherwise copied to the workspace filesystem.
4. A cluster is attached and can create a `SparkSession`.
5. The Python code under `src/` is available on `PYTHONPATH` when you run the script.

Notes:

- The script imports `pyspark` lazily, so local unit tests can run without Databricks, but actual table execution still requires a Spark-enabled Databricks runtime.
- `requirements.txt` does not pin `pyspark`; Databricks runtime is expected to provide it.

## Recommended Execution Options

Use one of these approaches.

### Option 0: Run From The Deployed Databricks Bundle Files

If you deployed the bundle with the VS Code Databricks extension, the files can be available under the bundle path in the Databricks workspace filesystem.

For the current repository and `dev` target, the deployed path can look like this:

```bash
/Workspace/Users/info@aichitect.eu/.bundle/cz-presentatie/dev/files
```

Do not use `%sh` as the primary execution mode for this script when it needs Spark table access.

Why:

- `%sh` starts a separate shell process
- that shell process does not share the notebook's live `spark` session
- `SparkSession.builder.getOrCreate()` can fail there with Spark Connect errors such as `INVALID_CONNECT_URL`

Use a Python notebook cell instead.

If your environment can read the Databricks tables but should not write to `/dbfs`, call the
runner with `output_path=None`.

Example:

```python
import sys

bundle_root = "/Workspace/Users/info@aichitect.eu/.bundle/cz-presentatie/dev/files"
if bundle_root not in sys.path:
  sys.path.insert(0, bundle_root)
src_path = f"{bundle_root}/src"
if src_path not in sys.path:
  sys.path.insert(0, src_path)

from scripts.run_claims_validation_from_tables import run_validation_from_tables

records = run_validation_from_tables(spark, output_path=None)
len(records), records[:3]
```

If you want to inspect the deployed files first, use `%sh` only for filesystem inspection:

```bash
%sh
cd /Workspace/Users/info@aichitect.eu/.bundle/cz-presentatie/dev/files
ls -al
python3 --version
```

Why the Python notebook cell works:

- the bundle deploy copies your project files into the `.bundle/.../files` directory
- the imported module runs inside the notebook Python process
- that notebook Python process already has access to the live Databricks `spark` session
- adding the bundle root and `src` path makes the deployed code importable

Then inspect the output:

```bash
%sh
ls -l /dbfs/tmp/validation_report.json
python3 -m json.tool /dbfs/tmp/validation_report.json | head -100
```

Use this mode when:

- you deploy with Databricks Asset Bundles
- you want to validate the exact deployed artifact instead of a Databricks Repo checkout
- the `.bundle/.../files` path exists on the workspace filesystem

### Option 1: Run From A Databricks Repo Notebook Cell

This is the simplest path when the repository is checked out in Databricks Repos.

In a notebook attached to a cluster, run:

```bash
%sh
cd /Workspace/Repos/<your-org>/cz-presentatie
source ./venv/bin/activate
PYTHONPATH=src python scripts/run_claims_validation_from_tables.py
```

Then inspect the output:

```bash
%sh
cat /dbfs/tmp/validation_report.json
```

If you want to pretty-print the result:

```bash
%sh
python -m json.tool /dbfs/tmp/validation_report.json
```

### Option 2: Run Inside A Python Notebook Cell

If you prefer Python instead of `%sh`, run the same flow directly:

```python
from scripts.run_claims_validation_from_tables import run_validation_from_tables
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
records = run_validation_from_tables(spark)
len(records), records[:3]
```

This uses the same hardcoded table names. In notebook mode you can either:

- keep the default `output_path` to write `/dbfs/tmp/validation_report.json`
- pass `output_path=None` to return records without writing a file

If you are executing from deployed bundle files rather than a Repo checkout, use the bundle-root example from Option 0.

### Option 3: Run As A Databricks Job Task

Create a Python script task that points at:

- Script: `scripts/run_claims_validation_from_tables.py`
- Working directory: repository root
- Environment: ensure `src` is on `PYTHONPATH`

If your job task allows environment variables, set:

```text
PYTHONPATH=src
```

The task succeeds when the script exits with code `0` and fails with code `1`.

## Which Execution Mode To Choose

- Use the bundle-files path when you deployed with the VS Code Databricks extension and want to run the deployed artifact.
- Use the Repo path when you are actively iterating from Databricks Repos.
- Use the Python notebook form when you want to call the runner function directly.
- Use a Job task when you want scheduled or repeatable execution.

## What The Script Does

Execution flow:

1. Creates a `SparkSession`.
2. Loads all rows from `workspace.demo.claims`.
3. Loads reference IDs from `workspace.demo.patients` and `workspace.demo.providers`.
4. Calls the validation engine in [src/claims_validation/engine.py](/Users/ai-chitect/Development/cz-presentatie/src/claims_validation/engine.py).
5. Converts violations into the canonical JSON envelope.
6. Writes the output to `/dbfs/tmp/validation_report.json`.

## Output Format

The output is a JSON array. Each item has this structure:

```json
{
  "error": {
    "code": "VALIDATION_NEGATIVE_AMOUNT",
    "message": "Claim amount must be non-negative.",
    "details": {
      "claim_id": "C-100",
      "field": "amount",
      "value": -5.0
    },
    "request_id": "validation-run-uuid"
  }
}
```

Common code prefixes:

- `VALIDATION_*`
- `NOT_FOUND_*`
- `CONFLICT_*`
- `SERVER_*`

## Typical End-To-End Run

Use this sequence in Databricks Repos:

```bash
%sh
cd /Workspace/Repos/<your-org>/cz-presentatie
source ./venv/bin/activate
PYTHONPATH=src python scripts/run_claims_validation_from_tables.py
echo "exit_code=$?"
```

Then inspect the generated file:

```bash
%sh
ls -l /dbfs/tmp/validation_report.json
python -m json.tool /dbfs/tmp/validation_report.json | head -100
```

If you are running from deployed bundle files instead of Repos, use a Python notebook cell like this:

```python
import sys

bundle_root = "/Workspace/Users/info@aichitect.eu/.bundle/cz-presentatie/dev/files"
if bundle_root not in sys.path:
  sys.path.insert(0, bundle_root)
src_path = f"{bundle_root}/src"
if src_path not in sys.path:
  sys.path.insert(0, src_path)

from scripts.run_claims_validation_from_tables import run_validation_from_tables

records = run_validation_from_tables(spark, output_path=None)
len(records), records[:3]
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'claims_validation'`

Cause: `src` is not on `PYTHONPATH`.

Fix:

```bash
export PYTHONPATH=src
python scripts/run_claims_validation_from_tables.py
```

If you are using a bundle deployment path and need Spark table access, prefer a Python notebook cell instead of `%sh`:

```python
import sys

bundle_root = "/Workspace/Users/info@aichitect.eu/.bundle/cz-presentatie/dev/files"
sys.path.insert(0, bundle_root)
sys.path.insert(0, f"{bundle_root}/src")

from scripts.run_claims_validation_from_tables import run_validation_from_tables

records = run_validation_from_tables(spark, output_path=None)
```

### `No module named pyspark`

Cause: The script is being run outside a Spark-enabled Databricks runtime.

Fix:

- Run on an attached Databricks cluster.
- Or execute from a Databricks notebook/job instead of a plain local shell.

### `[INVALID_CONNECT_URL] Invalid URL for Spark Connect`

Cause: The script was started from `%sh` or another separate Python process that does not share the Databricks notebook Spark session.

Fix:

1. Stop running the validator from `%sh` when it needs live table access.
2. Run it from a Python notebook cell instead:

```python
import sys

bundle_root = "/Workspace/Users/info@aichitect.eu/.bundle/cz-presentatie/dev/files"
sys.path.insert(0, bundle_root)
sys.path.insert(0, f"{bundle_root}/src")

from scripts.run_claims_validation_from_tables import run_validation_from_tables

records = run_validation_from_tables(spark)
```

3. Keep `%sh` only for checking files, Python version, or output files under `/dbfs/tmp/`.

### I can read tables, but writing `/dbfs/tmp/validation_report.json` fails

Cause: Some Databricks environments, especially serverless-oriented notebook execution paths, may
allow Spark table access while still making `/dbfs` writes undesirable or unavailable for this
workflow.

Fix:

Run the validator from a Python notebook cell and skip file output:

```python
import sys

bundle_root = "/Workspace/Users/info@aichitect.eu/.bundle/cz-presentatie/dev/files"
if bundle_root not in sys.path:
  sys.path.insert(0, bundle_root)
src_path = f"{bundle_root}/src"
if src_path not in sys.path:
  sys.path.insert(0, src_path)

from scripts.run_claims_validation_from_tables import run_validation_from_tables

records = run_validation_from_tables(spark, output_path=None)
len(records), records[:5]
```

This keeps the default CLI/script behavior intact while giving notebook users a no-write mode.

### Table not found errors

Cause: The hardcoded `workspace.demo.*` tables do not exist in the current workspace or are inaccessible.

Fix:

1. Confirm the workspace host in [databricks.yml](/Users/ai-chitect/Development/cz-presentatie/databricks.yml).
2. Confirm the tables exist:

```sql
SELECT * FROM workspace.demo.claims LIMIT 10;
SELECT * FROM workspace.demo.patients LIMIT 10;
SELECT * FROM workspace.demo.providers LIMIT 10;
```

3. Confirm your cluster identity has permission to read them.

### Output file is missing

Cause: The script failed before writing the report.

Fix:

1. Check stderr for `Validation runner failed: ...`.
2. Re-run in a notebook cell so the full exception context is visible.
3. Confirm `/dbfs/tmp/` is writable from the cluster.

### Bundle path exists but script still fails

Cause: The bundle files were deployed, but execution is happening from a shell process instead of the notebook Python process, or the import path is incomplete.

Fix:

1. Confirm the current working directory:

```bash
%sh
cd /Workspace/Users/info@aichitect.eu/.bundle/cz-presentatie/dev/files
pwd
ls -al
```

2. Run from a Python notebook cell with both bundle paths added:

```python
import sys

bundle_root = "/Workspace/Users/info@aichitect.eu/.bundle/cz-presentatie/dev/files"
sys.path.insert(0, bundle_root)
sys.path.insert(0, f"{bundle_root}/src")

from scripts.run_claims_validation_from_tables import run_validation_from_tables

records = run_validation_from_tables(spark)
```

3. If needed, inspect whether `src/claims_validation/` and `scripts/run_claims_validation_from_tables.py` are present under the deployed bundle root.

## Related Files

- [scripts/run_claims_validation_from_tables.py](/Users/ai-chitect/Development/cz-presentatie/scripts/run_claims_validation_from_tables.py)
- [src/claims_validation/engine.py](/Users/ai-chitect/Development/cz-presentatie/src/claims_validation/engine.py)
- [src/claims_validation/reporting.py](/Users/ai-chitect/Development/cz-presentatie/src/claims_validation/reporting.py)
- [docs/specs/spec.md](/Users/ai-chitect/Development/cz-presentatie/docs/specs/spec.md)
- [README.md](/Users/ai-chitect/Development/cz-presentatie/README.md)
