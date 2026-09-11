from __future__ import annotations

import json
import os
import sqlite3
import threading
from pathlib import Path
from typing import Any

from .artifacts import utc_now

RUN_UPDATE_SQL = {
    "status": "UPDATE runs SET status=? WHERE run_id=?",
    "updated_at": "UPDATE runs SET updated_at=? WHERE run_id=?",
    "error": "UPDATE runs SET error=? WHERE run_id=?",
    "budget_json": "UPDATE runs SET budget_json=? WHERE run_id=?",
    "worker_pid": "UPDATE runs SET worker_pid=? WHERE run_id=?",
    "heartbeat_at": "UPDATE runs SET heartbeat_at=? WHERE run_id=?",
}
CHAPTER_UPDATE_SQL = {
    "status": "UPDATE chapters SET status=? WHERE run_id=? AND chapter_id=?",
    "stage": "UPDATE chapters SET stage=? WHERE run_id=? AND chapter_id=?",
    "rci_findings": "UPDATE chapters SET rci_findings=? WHERE run_id=? AND chapter_id=?",
    "sei_findings": "UPDATE chapters SET sei_findings=? WHERE run_id=? AND chapter_id=?",
    "error": "UPDATE chapters SET error=? WHERE run_id=? AND chapter_id=?",
    "packet_json": "UPDATE chapters SET packet_json=? WHERE run_id=? AND chapter_id=?",
}


class StateStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._write_lock = threading.Lock()
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=30000")
        return connection

    def _initialize(self) -> None:
        with self._connect() as db:
            db.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    input_root TEXT NOT NULL,
                    output_root TEXT NOT NULL,
                    project_label TEXT NOT NULL,
                    case_owner TEXT NOT NULL,
                    classification TEXT NOT NULL,
                    provider_approved INTEGER NOT NULL,
                    approval_at TEXT NOT NULL,
                    model TEXT NOT NULL,
                    crossref_enabled INTEGER NOT NULL,
                    concurrency INTEGER NOT NULL,
                    run_mode TEXT NOT NULL,
                    worker_pid INTEGER,
                    heartbeat_at TEXT,
                    manifest_hash TEXT NOT NULL,
                    plan_hash TEXT NOT NULL,
                    error TEXT,
                    budget_json TEXT
                );
                CREATE TABLE IF NOT EXISTS chapters (
                    run_id TEXT NOT NULL,
                    chapter_id TEXT NOT NULL,
                    relative_path TEXT NOT NULL,
                    source_path TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    rci_findings INTEGER NOT NULL DEFAULT 0,
                    sei_findings INTEGER NOT NULL DEFAULT 0,
                    error TEXT,
                    packet_json TEXT,
                    PRIMARY KEY (run_id, chapter_id),
                    FOREIGN KEY (run_id) REFERENCES runs(run_id)
                );
                CREATE TABLE IF NOT EXISTS events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    FOREIGN KEY (run_id) REFERENCES runs(run_id)
                );
                """
            )
            columns = {row[1] for row in db.execute("PRAGMA table_info(runs)")}
            if "run_mode" not in columns:
                db.execute("ALTER TABLE runs ADD COLUMN run_mode TEXT NOT NULL DEFAULT 'baseline'")
            if "worker_pid" not in columns:
                db.execute("ALTER TABLE runs ADD COLUMN worker_pid INTEGER")
            if "heartbeat_at" not in columns:
                db.execute("ALTER TABLE runs ADD COLUMN heartbeat_at TEXT")

    def create_run(self, record: dict[str, Any], chapters: list[dict[str, Any]]) -> None:
        fields = [
            "run_id", "created_at", "updated_at", "status", "input_root", "output_root",
            "project_label", "case_owner", "classification", "provider_approved", "approval_at",
            "model", "crossref_enabled", "concurrency", "run_mode", "manifest_hash", "plan_hash", "error", "budget_json",
            "worker_pid", "heartbeat_at",
        ]
        with self._write_lock, self._connect() as db:
            db.execute(
                """INSERT INTO runs(
                    run_id,created_at,updated_at,status,input_root,output_root,project_label,case_owner,
                    classification,provider_approved,approval_at,model,crossref_enabled,concurrency,run_mode,
                    manifest_hash,plan_hash,error,budget_json,worker_pid,heartbeat_at
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                [record.get(field) for field in fields],
            )
            db.executemany(
                "INSERT INTO chapters(run_id,chapter_id,relative_path,source_path,sha256,size,status,stage) VALUES(?,?,?,?,?,?,?,?)",
                [(record["run_id"], item["chapter_id"], item["relative_path"], item["source_path"], item["sha256"], item["size"], "pending", "pending") for item in chapters],
            )

    def update_run(self, run_id: str, **values: Any) -> None:
        allowed = {"status", "updated_at", "error", "budget_json", "worker_pid", "heartbeat_at"}
        values = {key: value for key, value in values.items() if key in allowed}
        values.setdefault("updated_at", utc_now())
        with self._write_lock, self._connect() as db:
            for key, value in values.items():
                db.execute(RUN_UPDATE_SQL[key], (value, run_id))

    def update_chapter(self, run_id: str, chapter_id: str, **values: Any) -> None:
        allowed = {"status", "stage", "rci_findings", "sei_findings", "error", "packet_json"}
        values = {key: value for key, value in values.items() if key in allowed}
        if not values:
            return
        with self._write_lock, self._connect() as db:
            for key, value in values.items():
                db.execute(CHAPTER_UPDATE_SQL[key], (value, run_id, chapter_id))

    def append_event(self, run_id: str, event_type: str, payload: dict[str, Any]) -> None:
        with self._write_lock, self._connect() as db:
            db.execute("INSERT INTO events(run_id,created_at,event_type,payload_json) VALUES(?,?,?,?)", (run_id, utc_now(), event_type, json.dumps(payload, ensure_ascii=False, sort_keys=True)))

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        with self._connect() as db:
            row = db.execute("SELECT * FROM runs WHERE run_id=?", (run_id,)).fetchone()
        if row is None:
            return None
        result = dict(row)
        result["provider_approved"] = bool(result["provider_approved"])
        result["crossref_enabled"] = bool(result["crossref_enabled"])
        result["budget"] = json.loads(result.pop("budget_json") or "{}")
        return result

    def get_chapters(self, run_id: str) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute("SELECT * FROM chapters WHERE run_id=? ORDER BY chapter_id", (run_id,)).fetchall()
        output = []
        for row in rows:
            item = dict(row)
            item["packet"] = json.loads(item.pop("packet_json") or "{}")
            output.append(item)
        return output

    def list_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute("SELECT run_id,created_at,updated_at,status,project_label,output_root,error FROM runs ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in rows]

    def reset_incomplete(self, run_id: str) -> None:
        with self._write_lock, self._connect() as db:
            db.execute("UPDATE chapters SET status='pending', stage='pending', error=NULL WHERE run_id=? AND status!='packet_built'", (run_id,))

    def recover_orphaned_runs(self) -> int:
        """Mark active records interrupted only when their owning process is gone."""
        recovered = 0
        with self._write_lock, self._connect() as db:
            rows = db.execute("SELECT run_id,worker_pid FROM runs WHERE status IN ('queued','running','cancelling')").fetchall()
            for row in rows:
                pid = int(row["worker_pid"] or 0)
                alive = False
                if pid > 0:
                    try:
                        os.kill(pid, 0)
                        alive = True
                    except PermissionError:
                        alive = True
                    except (ProcessLookupError, OSError):
                        alive = False
                if alive:
                    continue
                now = utc_now()
                db.execute("UPDATE runs SET status='interrupted',updated_at=?,worker_pid=NULL,heartbeat_at=? WHERE run_id=?", (now, now, row["run_id"]))
                db.execute("UPDATE chapters SET status='pending',stage='pending',error=NULL WHERE run_id=? AND status!='packet_built'", (row["run_id"],))
                recovered += 1
        return recovered
