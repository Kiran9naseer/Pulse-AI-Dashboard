# =============================================================================
# database/db.py - SQLite Database Access Layer
# =============================================================================
# Purpose: Provides an abstraction layer for interacting with SQLite.
#          - User authentication (`create_user`, `login_user`)
#          - Action logging (`add_log`, `get_logs`)
# =============================================================================

import sqlite3
import hashlib
import os
from datetime import datetime

# Absolute path resolution ensures DB connects reliably from any CWD
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "saas_mvp.db")


# -----------------------------------------------------------------------------
# CORE DB CONNECTION
# -----------------------------------------------------------------------------
def get_connection():
    """Establishes and returns a dictionary-addressable SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes required database schema (users & logs).
    Idempotent operation (runs safely on every boot).
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Create User Authentication table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL
        )
    """)

    # Create General System Logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            message   TEXT    NOT NULL,
            timestamp TEXT    NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------------------------------------------------
# AUTHENTICATION FUNCTIONS
# -----------------------------------------------------------------------------
def hash_password(password: str) -> str:
    """Hashes a plaintext password using SHA-256 for basic security."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str) -> bool:
    """
    Registers a new user in the system.
    Returns True on success, False if the username already exists.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username: str, password: str) -> bool:
    """
    Verifies authentication credentials matching stored records.
    Returns True upon validation, False otherwise.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if row and row["password"] == hash_password(password):
        return True
    return False


# -----------------------------------------------------------------------------
# LOGGING FUNCTIONS
# -----------------------------------------------------------------------------
def add_log(message: str):
    """Inserts a new event log into the system with the current UTC-local timestamp."""
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO logs (message, timestamp) VALUES (?, ?)",
        (message, timestamp)
    )
    conn.commit()
    conn.close()

def get_logs(limit: int = 50) -> list:
    """
    Retrieves the most recent system logs in descending chronological order.
    Returns a list of dictionaries with 'id', 'message', 'timestamp' keys.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, message, timestamp FROM logs ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
