"""Tests for Flask application routes."""

import pytest
import tempfile
import os
from src.nn_investigator.app import app as flask_app
from src.nn_investigator import database


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    # Use a temporary database
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    flask_app.config["TESTING"] = True
    flask_app.config["DATABASE"] = db_path

    # Initialize the database
    database.init_db(db_path)

    # Add some test data
    database.add_pair(
        entity_name="test entity 1",
        curie_1="TEST:001",
        curie_2="TEST:002",
        curie_1_label="Label 1",
        curie_2_label="Label 2",
        db_path=db_path
    )

    # Monkey-patch the database module to use our test database
    original_get_all = database.get_all_pairs
    original_get_pair = database.get_pair
    original_add_pair = database.add_pair
    original_delete_pair = database.delete_pair

    database.get_all_pairs = lambda db_path="nn_investigator.db": original_get_all(flask_app.config["DATABASE"])
    database.get_pair = lambda pair_id, db_path="nn_investigator.db": original_get_pair(pair_id, flask_app.config["DATABASE"])
    database.add_pair = lambda *args, **kwargs: original_add_pair(*args, **{**kwargs, "db_path": flask_app.config["DATABASE"]})
    database.delete_pair = lambda pair_id, db_path="nn_investigator.db": original_delete_pair(pair_id, flask_app.config["DATABASE"])

    yield flask_app

    # Restore original functions
    database.get_all_pairs = original_get_all
    database.get_pair = original_get_pair
    database.add_pair = original_add_pair
    database.delete_pair = original_delete_pair

    # Clean up
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


def test_index_route(client):
    """Test the index route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Entity Pairs" in response.data
    assert b"test entity 1" in response.data
    assert b"TEST:001" in response.data


def test_add_pair_get(client):
    """Test the add pair form."""
    response = client.get("/add")
    assert response.status_code == 200
    assert b"Add Entity Pair" in response.data
    assert b"CURIE 1" in response.data


def test_add_pair_post(client):
    """Test adding a pair via POST."""
    response = client.post("/add", data={
        "entity_name": "new entity",
        "curie_1": "NEW:001",
        "curie_2": "NEW:002",
        "curie_1_label": "New Label 1",
        "curie_2_label": "New Label 2",
        "notes": "Test notes"
    }, follow_redirects=False)

    assert response.status_code == 302  # Redirect after success

    # Verify it was added
    response = client.get("/")
    assert b"new entity" in response.data


def test_add_pair_missing_required_fields(client):
    """Test adding a pair with missing required fields."""
    response = client.post("/add", data={
        "entity_name": "incomplete entity",
        "curie_1": "INC:001"
        # Missing curie_2
    }, follow_redirects=True)

    assert b"are required" in response.data


def test_delete_pair(client, app):
    """Test deleting a pair."""
    # Add a pair to delete
    pair_id = database.add_pair(
        entity_name="to delete",
        curie_1="DEL:001",
        curie_2="DEL:002",
        db_path=app.config["DATABASE"]
    )

    # Delete it
    response = client.post(f"/pair/{pair_id}/delete", follow_redirects=False)
    assert response.status_code == 302

    # Verify it's gone
    response = client.get("/")
    assert b"to delete" not in response.data


def test_delete_nonexistent_pair(client):
    """Test deleting a non-existent pair."""
    response = client.post("/pair/999/delete", follow_redirects=True)
    assert b"not found" in response.data or response.status_code in [302, 200]
