import pytest
from utils import dbHelpers

def test_database_connection():
    """Basic test to confirm the database is reachable and queries work."""

    # Try to fetch one item from the items table
    try:
        result = dbHelpers.fetch_one("SELECT name FROM items LIMIT 1")
        print("Sample item fetched from DB:", result)

        # Assert result is not None (we expect at least one row in items table)
        assert result is not None, "No items found in the database."

    except Exception as e:
        pytest.fail(f"Database connection or query failed: {e}")
