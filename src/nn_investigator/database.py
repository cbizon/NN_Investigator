"""Database operations for NN Investigator."""

import sqlite3
from typing import Optional


def get_connection(db_path: str = "nn_investigator.db") -> sqlite3.Connection:
    """Get a database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = "nn_investigator.db") -> None:
    """Initialize the database schema."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entity_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_name TEXT NOT NULL,
            curie_1 TEXT NOT NULL,
            curie_1_label TEXT,
            curie_2 TEXT NOT NULL,
            curie_2_label TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            evaluation TEXT,
            evaluation_notes TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_pair(
    entity_name: str,
    curie_1: str,
    curie_2: str,
    curie_1_label: Optional[str] = None,
    curie_2_label: Optional[str] = None,
    notes: Optional[str] = None,
    db_path: str = "nn_investigator.db"
) -> int:
    """Add an entity pair to the database."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entity_pairs (entity_name, curie_1, curie_1_label, curie_2, curie_2_label, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (entity_name, curie_1, curie_1_label, curie_2, curie_2_label, notes))

    pair_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return pair_id


def get_all_pairs(db_path: str = "nn_investigator.db") -> list[dict]:
    """Get all entity pairs from the database."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, entity_name, curie_1, curie_1_label, curie_2, curie_2_label, notes, created_at, evaluation, evaluation_notes
        FROM entity_pairs
        ORDER BY entity_name
    """)

    pairs = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return pairs


def get_pair(pair_id: int, db_path: str = "nn_investigator.db") -> Optional[dict]:
    """Get a specific entity pair by ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, entity_name, curie_1, curie_1_label, curie_2, curie_2_label, notes, created_at, evaluation, evaluation_notes
        FROM entity_pairs
        WHERE id = ?
    """, (pair_id,))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def update_evaluation(
    pair_id: int,
    evaluation: str,
    evaluation_notes: Optional[str] = None,
    db_path: str = "nn_investigator.db"
) -> bool:
    """Update the evaluation for an entity pair."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE entity_pairs
        SET evaluation = ?, evaluation_notes = ?
        WHERE id = ?
    """, (evaluation, evaluation_notes, pair_id))

    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return updated


def delete_pair(pair_id: int, db_path: str = "nn_investigator.db") -> bool:
    """Delete an entity pair by ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM entity_pairs WHERE id = ?", (pair_id,))

    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return deleted
