# utils/dbHelpers.py
"""SQLite helpers used by tests for simple reads/writes against the demo app DB."""

from __future__ import annotations  # defer type-hint evaluation (only needed for < Python 3.11)

# Stdlib
import os  # read DB_PATH from environment
import sqlite3  # built-in SQLite driver
from pathlib import Path  # robust path handling

from typing import Any, Iterable, Optional, Sequence, Tuple

# Third‑party
from dotenv import load_dotenv

# Load environment variables from .env (optional).
load_dotenv()

# Resolve the database path:
# - Prefer DB_PATH from the environment if set
# - Otherwise default to "<repo-root>/shop.db"
DB_PATH: Path = Path(os.getenv("DB_PATH", Path(__file__).resolve().parent.parent / "shop.db"))

def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection to the resolved DB_PATH."""
    # sqlite3.connect accepts str or Path; cast to str for clarity
    return sqlite3.connect(str(DB_PATH))


def fetch_one(query: str, params: Sequence[Any] | None = None) -> Optional[Tuple[Any, ...]]:
    """Execute a SELECT and return the first row (or None).

    Args:
        query: SQL SELECT statement with optional placeholders (e.g., '?').
        params: Values for the placeholders. Use a sequence (tuple/list). Optional.

    Returns:
        A single row as a tuple (e.g., ('Koala',)) or None if no rows match.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, tuple(params or ()))
        return cur.fetchone()


def fetch_all(query: str, params: Sequence[Any] | None = None) -> list[Tuple[Any, ...]]:
    """Execute a SELECT and return all rows.

    Args:
        query: SQL SELECT statement with optional placeholders.
        params: Values for the placeholders. Use a sequence (tuple/list). Optional.

    Returns:
        A list of rows; each row is a tuple.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, tuple(params or ()))
        return cur.fetchall()


def execute_query(query: str, params: Sequence[Any] | None = None) -> None:
    """Execute a write (INSERT/UPDATE/DELETE) and commit.

    Args:
        query: SQL statement with optional placeholders.
        params: Values for the placeholders. Use a sequence (tuple/list). Optional.

    Notes:
        Using the connection as a context manager commits on success and rolls back on error.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, tuple(params or ()))
        # Commit handled by the context manager on successful exit.


def reset_table(table_name: str) -> None:
    """Delete all rows from the given table (simple test cleanup helper)."""
    execute_query(f"DELETE FROM {table_name}")


def get_item_name(item_id: int) -> Optional[str]:
    """Return the display name for an item id, or None if not found."""
    row = fetch_one("SELECT name FROM items WHERE id = ?", (item_id,))
    return row[0] if row else None


def get_cart_quantity(item_id: int) -> int:
    """Return the quantity for an item in the cart, or 0 if not present."""
    row = fetch_one("SELECT quantity FROM cart WHERE item_id = ?", (item_id,))
    return int(row[0]) if row else 0
