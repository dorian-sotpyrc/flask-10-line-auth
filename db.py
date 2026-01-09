from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash


@dataclass(frozen=True)
class User:
    id: int
    email: str


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            pw_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()


def create_user(conn: sqlite3.Connection, email: str, password: str) -> int:
    email = email.strip().lower()
    pw_hash = generate_password_hash(password)
    cur = conn.execute(
        "INSERT INTO users (email, pw_hash) VALUES (?, ?)",
        (email, pw_hash),
    )
    conn.commit()
    return int(cur.lastrowid)


def verify_user(conn: sqlite3.Connection, email: str, password: str) -> Optional[int]:
    email = email.strip().lower()
    row = conn.execute("SELECT id, pw_hash FROM users WHERE email = ?", (email,)).fetchone()
    if not row:
        return None
    if not check_password_hash(row["pw_hash"], password):
        return None
    return int(row["id"])


def get_user_by_id(conn: sqlite3.Connection, uid: int) -> Optional[User]:
    row = conn.execute("SELECT id, email FROM users WHERE id = ?", (int(uid),)).fetchone()
    if not row:
        return None
    return User(id=int(row["id"]), email=str(row["email"]))
