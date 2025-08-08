import sqlite3
import os
from contextlib import closing
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file (if it exists)
load_dotenv()

# Resolve the database path from the environment variable
# Falls back to a default relative path if DB_PATH is not set
DB_PATH = Path(os.getenv("DB_PATH", Path(__file__).resolve().parent.parent / "shop.db"))

def get_connection():
    """
    Establish and return a SQLite database connection using the resolved DB_PATH.
    Each function below calls this to interact with the DB.
    """
    return sqlite3.connect(DB_PATH)

def fetch_one(query: str, params: tuple = ()):
    """
    Execute a SELECT query and return the first row of the result set.

    Args:
        query (str): The SQL SELECT query to run.
        params (tuple): Optional query parameters (to prevent SQL injection).

    Returns:
        A single result row or None if no match is found.
    """
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchone()

def fetch_all(query: str, params: tuple = ()):
    """
    Execute a SELECT query and return all matching rows.

    Args:
        query (str): The SQL SELECT query to run.
        params (tuple): Optional query parameters.

    Returns:
        A list of result rows.
    """
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

def execute_query(query: str, params: tuple = ()):
    """
    Execute a write query (INSERT, UPDATE, DELETE) and commit the change.

    Args:
        query (str): The SQL query to execute.
        params (tuple): Optional query parameters.
    """
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()

def reset_table(table_name: str):
    """
    Clear all rows from the specified table. Useful for test setup or cleanup.

    Args:
        table_name (str): The name of the table to truncate.
    """
    execute_query(f"DELETE FROM {table_name}")
