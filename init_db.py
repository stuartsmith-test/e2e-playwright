import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "test_app.db"

def init_db():
    """Create or reset the SQLite database with required schema and seed data."""
    # Ensure data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect (creates file if not exists)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop existing users table if exists
    cur.execute("DROP TABLE IF EXISTS users")

    # Create users table
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Optional seed data (one default user)
    cur.execute("""
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
    """, ("demo_user", "demo@example.com", "password123"))

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
