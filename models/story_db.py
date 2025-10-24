import sqlite3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "user_story_history.db"

def _get_conn():
    # SQLite connection, allow cross-thread use for simple Flask/Streamlit use
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def add_message(role: str, content: str):
    """Insert a message into history. role is typically 'user' or 'assistant'."""
    init_db()
    conn = _get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (role, content, created_at) VALUES (?, ?, ?)",
        (role, content, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()

def get_history(limit: int = 100):
    """Return the last `limit` messages as a list of dicts, oldest-first."""
    init_db()
    conn = _get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT id, role, content, created_at FROM messages ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = c.fetchall()
    conn.close()
    # rows are newest-first, invert to oldest-first for display
    out = [dict(r) for r in reversed(rows)]
    return out

def clear_history():
    """Utility to clear history (not used by default)."""
    init_db()
    conn = _get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM messages")
    conn.commit()
    conn.close()

 