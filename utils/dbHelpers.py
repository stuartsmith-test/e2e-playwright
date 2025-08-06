import sqlite3
from contextlib import closing
from pathlib import Path

# Path to the SQLite database
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "test_app.db"

def get_connection():
    """Establish and return a SQLite connection."""
    return sqlite3.connect(DB_PATH)

def fetch_one(query: str, params: tuple = ()):
    """Execute a query and return a single row."""
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchone()

def fetch_all(query: str, params: tuple = ()):
    """Execute a query and return all rows."""
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

def execute_query(query: str, params: tuple = ()):
    """Execute an insert/update/delete query and commit."""
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()

def reset_table(table_name: str):
    """Utility to clear a table (used for test cleanup)."""
    execute_query(f"DELETE FROM {table_name}")
