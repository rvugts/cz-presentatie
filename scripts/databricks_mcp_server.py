"""
Databricks MCP Server – exposes workspace tools to GitHub Copilot via stdio.

Tools provided:
  - list_catalogs      : List all Unity Catalog catalogs
  - list_schemas       : List schemas in a catalog
  - list_tables        : List tables in a catalog.schema
  - get_table_info     : Describe a table (columns, type, comment)
  - execute_sql        : Run a SQL statement on SQL Warehouse and return results
  - list_clusters      : List active clusters
  - list_jobs          : List Databricks jobs

Authentication: uses ~/.databrickscfg or env vars DATABRICKS_HOST + DATABRICKS_TOKEN,
identical to the Databricks CLI.
"""

import json
import os
import sys

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementState
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("databricks")
_client: WorkspaceClient | None = None


def _ws() -> WorkspaceClient:
    global _client
    if _client is None:
        _client = WorkspaceClient()
    return _client


# ---------------------------------------------------------------------------
# Unity Catalog tools
# ---------------------------------------------------------------------------


@mcp.tool()
def list_catalogs() -> str:
    """List all Unity Catalog catalogs in the workspace."""
    catalogs = list(_ws().catalogs.list())
    if not catalogs:
        return "No catalogs found."
    rows = [f"- {c.name}" + (f"  # {c.comment}" if c.comment else "") for c in catalogs]
    return "\n".join(rows)


@mcp.tool()
def list_schemas(catalog_name: str) -> str:
    """List all schemas inside a catalog.

    Args:
        catalog_name: Name of the catalog (e.g. 'main' or 'hive_metastore').
    """
    schemas = list(_ws().schemas.list(catalog_name=catalog_name))
    if not schemas:
        return f"No schemas found in catalog '{catalog_name}'."
    rows = [f"- {s.name}" + (f"  # {s.comment}" if s.comment else "") for s in schemas]
    return "\n".join(rows)


@mcp.tool()
def list_tables(catalog_name: str, schema_name: str) -> str:
    """List all tables in a catalog.schema.

    Args:
        catalog_name: Name of the catalog (e.g. 'main').
        schema_name:  Name of the schema (e.g. 'default').
    """
    tables = list(_ws().tables.list(catalog_name=catalog_name, schema_name=schema_name))
    if not tables:
        return f"No tables found in '{catalog_name}.{schema_name}'."
    rows = []
    for t in tables:
        row = f"- {t.name}  [{t.table_type.value if t.table_type else 'UNKNOWN'}]"
        if t.comment:
            row += f"  # {t.comment}"
        rows.append(row)
    return "\n".join(rows)


@mcp.tool()
def get_table_info(full_table_name: str) -> str:
    """Get full metadata for a table including columns.

    Args:
        full_table_name: Three-part name: 'catalog.schema.table'
    """
    parts = full_table_name.strip().split(".")
    if len(parts) != 3:
        return "Error: full_table_name must be 'catalog.schema.table'."
    catalog_name, schema_name, table_name = parts
    table = _ws().tables.get(full_name=full_table_name)
    lines = [
        f"Table:   {table.full_name}",
        f"Type:    {table.table_type.value if table.table_type else 'UNKNOWN'}",
        f"Comment: {table.comment or '(none)'}",
        "",
        "Columns:",
    ]
    if table.columns:
        for col in table.columns:
            col_line = f"  {col.name}  {col.type_name.value if col.type_name else '?'}"
            if col.comment:
                col_line += f"  # {col.comment}"
            lines.append(col_line)
    else:
        lines.append("  (no column info)")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# SQL execution tool
# ---------------------------------------------------------------------------


def _find_warehouse_id() -> str | None:
    """Return the first running SQL warehouse id, or None."""
    for wh in _ws().warehouses.list():
        if wh.state and wh.state.value in ("RUNNING", "STARTING"):
            return wh.id
    # Fall back to any warehouse
    warehouses = list(_ws().warehouses.list())
    if warehouses:
        return warehouses[0].id
    return None


@mcp.tool()
def execute_sql(
    statement: str,
    warehouse_id: str = "",
    row_limit: int = 100,
) -> str:
    """Execute a SQL statement on a Databricks SQL Warehouse and return results.

    Args:
        statement:    SQL to execute (e.g. 'SELECT * FROM main.default.my_table LIMIT 10').
        warehouse_id: Optional warehouse id. Auto-detected when empty.
        row_limit:    Maximum rows to return (default 100, max 1000).
    """
    row_limit = min(max(1, row_limit), 1000)
    wh_id = warehouse_id.strip() or _find_warehouse_id()
    if not wh_id:
        return "Error: no SQL Warehouse found. Create one in the Databricks UI first."

    response = _ws().statement_execution.execute_statement(
        warehouse_id=wh_id,
        statement=statement,
        wait_timeout="30s",
    )

    state = response.status.state if response.status else None
    if state == StatementState.FAILED:
        err = response.status.error
        return f"SQL Error: {err.message if err else 'unknown'}"
    if state not in (StatementState.SUCCEEDED,):
        return f"Statement ended with state: {state}"

    result = response.result
    manifest = response.manifest
    if not result or not result.data_array:
        return "Query returned no rows."

    # Build header from manifest
    headers: list[str] = []
    if manifest and manifest.schema and manifest.schema.columns:
        headers = [c.name or "" for c in manifest.schema.columns]

    rows_data = result.data_array[:row_limit]
    lines: list[str] = []
    if headers:
        lines.append(" | ".join(headers))
        lines.append("-" * (sum(len(h) for h in headers) + 3 * (len(headers) - 1)))
    for row in rows_data:
        lines.append(" | ".join(str(v) if v is not None else "NULL" for v in (row or [])))

    total = manifest.total_row_count if manifest else "?"
    lines.append(f"\n({len(rows_data)} of {total} rows shown)")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Cluster & job tools
# ---------------------------------------------------------------------------


@mcp.tool()
def list_clusters() -> str:
    """List all clusters in the workspace with their state."""
    clusters = list(_ws().clusters.list())
    if not clusters:
        return "No clusters found."
    rows = []
    for c in clusters:
        state = c.state.value if c.state else "UNKNOWN"
        rows.append(f"- {c.cluster_name}  [{state}]  id={c.cluster_id}")
    return "\n".join(rows)


@mcp.tool()
def list_jobs(limit: int = 25) -> str:
    """List Databricks jobs.

    Args:
        limit: Maximum number of jobs to return (default 25).
    """
    jobs = list(_ws().jobs.list(limit=min(limit, 100)))
    if not jobs:
        return "No jobs found."
    rows = [f"- #{j.job_id}  {j.settings.name if j.settings else '(unnamed)'}" for j in jobs]
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
