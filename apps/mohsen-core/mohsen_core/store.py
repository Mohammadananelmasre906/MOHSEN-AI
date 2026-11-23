from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from .config import settings


def _connect() -> sqlite3.Connection:
    path = Path(settings.database_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            due_at TEXT,
            status TEXT NOT NULL DEFAULT 'open',
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    connection.commit()
    return connection


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_task(title: str, due_at: str | None = None) -> dict[str, Any]:
    task_id, now = str(uuid4()), _now()
    with _connect() as db:
        db.execute(
            "INSERT INTO tasks(id,title,due_at,status,created_at) VALUES(?,?,?,'open',?)",
            (task_id, title.strip(), due_at, now),
        )
        row = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    return dict(row)


def list_tasks(status: str | None = None) -> list[dict[str, Any]]:
    with _connect() as db:
        if status:
            rows = db.execute(
                "SELECT * FROM tasks WHERE status=? ORDER BY due_at IS NULL,due_at,created_at DESC",
                (status,),
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM tasks ORDER BY status, due_at IS NULL, due_at, created_at DESC"
            ).fetchall()
    return [dict(row) for row in rows]


def complete_task(task_id: str) -> dict[str, Any] | None:
    with _connect() as db:
        cursor = db.execute(
            "UPDATE tasks SET status='completed', completed_at=? WHERE id=? AND status='open'",
            (_now(), task_id),
        )
        if cursor.rowcount == 0:
            row = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
            return dict(row) if row else None
        row = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    return dict(row)


def delete_task(task_id: str) -> bool:
    with _connect() as db:
        cursor = db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        return cursor.rowcount > 0


def create_note(title: str, content: str) -> dict[str, Any]:
    note_id, now = str(uuid4()), _now()
    with _connect() as db:
        db.execute(
            "INSERT INTO notes(id,title,content,created_at,updated_at) VALUES(?,?,?,?,?)",
            (note_id, title.strip(), content.strip(), now, now),
        )
        row = db.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    return dict(row)


def list_notes(query: str | None = None) -> list[dict[str, Any]]:
    with _connect() as db:
        if query:
            needle = f"%{query.strip()}%"
            rows = db.execute(
                "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY updated_at DESC",
                (needle, needle),
            ).fetchall()
        else:
            rows = db.execute("SELECT * FROM notes ORDER BY updated_at DESC").fetchall()
    return [dict(row) for row in rows]
