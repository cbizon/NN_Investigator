"""Tests for database operations."""

import pytest
import sqlite3
import tempfile
import os
from src.nn_investigator import database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    database.init_db(path)
    yield path
    os.unlink(path)


def test_init_db(temp_db):
    """Test database initialization."""
    conn = database.get_connection(temp_db)
    cursor = conn.cursor()

    # Check that the table exists
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='entity_pairs'
    """)

    assert cursor.fetchone() is not None
    conn.close()


def test_add_pair(temp_db):
    """Test adding an entity pair."""
    pair_id = database.add_pair(
        entity_name="test entity",
        curie_1="TEST:001",
        curie_2="TEST:002",
        curie_1_label="Test Label 1",
        curie_2_label="Test Label 2",
        notes="Test notes",
        db_path=temp_db
    )

    assert pair_id > 0

    # Verify the pair was added
    pair = database.get_pair(pair_id, temp_db)
    assert pair["entity_name"] == "test entity"
    assert pair["curie_1"] == "TEST:001"
    assert pair["curie_2"] == "TEST:002"
    assert pair["curie_1_label"] == "Test Label 1"
    assert pair["curie_2_label"] == "Test Label 2"
    assert pair["notes"] == "Test notes"


def test_add_pair_without_labels(temp_db):
    """Test adding a pair without labels."""
    pair_id = database.add_pair(
        entity_name="minimal entity",
        curie_1="TEST:003",
        curie_2="TEST:004",
        db_path=temp_db
    )

    pair = database.get_pair(pair_id, temp_db)
    assert pair["curie_1_label"] is None
    assert pair["curie_2_label"] is None
    assert pair["notes"] is None


def test_get_all_pairs(temp_db):
    """Test retrieving all pairs."""
    # Add multiple pairs
    database.add_pair("entity1", "TEST:001", "TEST:002", db_path=temp_db)
    database.add_pair("entity2", "TEST:003", "TEST:004", db_path=temp_db)
    database.add_pair("entity3", "TEST:005", "TEST:006", db_path=temp_db)

    pairs = database.get_all_pairs(temp_db)
    assert len(pairs) == 3

    # Check they're sorted by entity_name
    assert pairs[0]["entity_name"] == "entity1"
    assert pairs[1]["entity_name"] == "entity2"
    assert pairs[2]["entity_name"] == "entity3"


def test_get_pair_not_found(temp_db):
    """Test getting a non-existent pair."""
    pair = database.get_pair(999, temp_db)
    assert pair is None


def test_delete_pair(temp_db):
    """Test deleting a pair."""
    pair_id = database.add_pair(
        entity_name="to delete",
        curie_1="TEST:001",
        curie_2="TEST:002",
        db_path=temp_db
    )

    # Delete the pair
    result = database.delete_pair(pair_id, temp_db)
    assert result is True

    # Verify it's gone
    pair = database.get_pair(pair_id, temp_db)
    assert pair is None


def test_delete_nonexistent_pair(temp_db):
    """Test deleting a non-existent pair."""
    result = database.delete_pair(999, temp_db)
    assert result is False


def test_get_connection(temp_db):
    """Test getting a database connection."""
    conn = database.get_connection(temp_db)
    assert isinstance(conn, sqlite3.Connection)
    assert conn.row_factory == sqlite3.Row
    conn.close()
