# tests/db/test_db_connection.py
"""DB smoke test: confirm the SQLite DB is readable and `items` has data."""

from utils import dbHelpers as db  # shared DB helpers (fetch_one, etc.)


def test_database_connection() -> None:
    """Expect at least one row in `items` (read-only check)."""
    # Run a simple, predictable query
    row = db.fetch_one("SELECT COUNT(*) FROM items")

    # Basic assertions with minimal assumptions
    assert row is not None, "`items` table missing or unreadable"
    count = row[0]  # fetch_one returns a single row; first column is COUNT(*)

    print(f"✅ DB reachable. items count = {count}")
    assert count >= 1, "Expected seeded items in the database"

