"""Shared Snowflake session helpers."""

from __future__ import annotations

import os
from typing import Any
from pprint import pprint

from snowflake.snowpark import Session

CONNECTION_NAME = os.environ.get("SF_CONNECTION", "CHARTIS-ANALYTICS")


def get_session(
    role: str | None = None,
    warehouse: str | None = None,
    database: str | None = None,
    schema: str | None = None,
) -> Session:
    """Open a Snowpark session from the named connection in connections.toml.

    Arguments left as None fall back to the SF_ROLE / SF_WAREHOUSE / SF_DATABASE / SF_SCHEMA
    environment variables, then to the user's defaults.
    """
    overrides: dict[str, Any] = {
        "connection_name": CONNECTION_NAME,
        "client_store_temporary_credential": True,
    }
    for key, value, env in (
        ("role", role, "SF_ROLE"),
        ("warehouse", warehouse, "SF_WAREHOUSE"),
        ("database", database, "SF_DATABASE"),
        ("schema", schema, "SF_SCHEMA"),
    ):
        resolved = value or os.environ.get(env)
        if resolved:
            overrides[key] = resolved
    session = Session.builder.configs(overrides).create()
    pprint(
        "Active session: "
        f"role={session.get_current_role()}, "
        f"warehouse={session.get_current_warehouse()}, "
        f"database={session.get_current_database()}, "
        f"schema={session.get_current_schema()}"
    )
    return session



def try_sql(session: Session, sql: str) -> list[dict[str, Any]] | str:
    """Run a statement and return rows as dicts, or the error text if it fails."""
    try:
        return [row.as_dict() for row in session.sql(sql).collect()]
    except Exception as exc:  # noqa: BLE001 - probes record failures instead of raising
        return f"ERROR: {type(exc).__name__}: {str(exc).splitlines()[0]}"
