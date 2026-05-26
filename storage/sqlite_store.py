from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from connectors.demo_sources import RetrievedDocument
from models.business import BusinessCandidate, LeadRecord


class LeadFinderStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS raw_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_name TEXT NOT NULL,
                source_url TEXT NOT NULL,
                content_type TEXT NOT NULL,
                retrieved_at TEXT NOT NULL,
                raw_text TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS candidates (
                business_id TEXT PRIMARY KEY,
                payload_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS leads (
                business_id TEXT PRIMARY KEY,
                payload_json TEXT NOT NULL
            );
            """
        )
        self.conn.commit()

    def save_raw_documents(self, docs: list[RetrievedDocument]) -> None:
        self.conn.executemany(
            """
            INSERT INTO raw_documents(source_name, source_url, content_type, retrieved_at, raw_text)
            VALUES (?, ?, ?, ?, ?)
            """,
            [(d.source_name, d.source_url, d.content_type, d.retrieved_at, d.raw_text) for d in docs],
        )
        self.conn.commit()

    def save_candidates(self, candidates: list[BusinessCandidate]) -> None:
        self.conn.executemany(
            """
            INSERT INTO candidates(business_id, payload_json)
            VALUES (?, ?)
            ON CONFLICT(business_id) DO UPDATE SET payload_json=excluded.payload_json
            """,
            [(c.business_id, c.model_dump_json()) for c in candidates],
        )
        self.conn.commit()

    def save_leads(self, leads: list[LeadRecord]) -> None:
        self.conn.executemany(
            """
            INSERT INTO leads(business_id, payload_json)
            VALUES (?, ?)
            ON CONFLICT(business_id) DO UPDATE SET payload_json=excluded.payload_json
            """,
            [(lead.business.business_id, lead.model_dump_json()) for lead in leads],
        )
        self.conn.commit()

    def counts(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for table in ["raw_documents", "candidates", "leads"]:
            result[table] = self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        return result
