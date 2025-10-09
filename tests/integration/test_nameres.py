"""Integration tests for Name Resolution API client."""

import pytest
from src.nn_investigator import nameres


def test_get_synonyms():
    """Test getting synonyms for preferred CURIEs."""
    result = nameres.get_synonyms(["MONDO:0005737"])

    assert "MONDO:0005737" in result
    data = result["MONDO:0005737"]

    assert "curie" in data
    assert data["curie"] == "MONDO:0005737"
    assert "names" in data
    assert len(data["names"]) > 0
    assert "preferred_name" in data

    # Check for expected Ebola-related names
    names_lower = [n.lower() for n in data["names"]]
    assert any("ebola" in n for n in names_lower)


def test_lookup():
    """Test looking up CURIEs by name."""
    results = nameres.lookup("doxorubicin", biolink_type="SmallMolecule", limit=10)

    assert len(results) > 0

    # First result should be the drug
    first = results[0]
    assert "curie" in first
    assert "CHEBI" in first["curie"] or "DRUGBANK" in first["curie"]
    assert "label" in first
    assert "doxorubicin" in first["label"].lower()
    assert "types" in first


def test_lookup_with_limit():
    """Test lookup with a specific limit."""
    results = nameres.lookup("aspirin", limit=5)
    assert len(results) <= 5


def test_lookup_with_offset():
    """Test lookup with pagination."""
    # Get first 5 results
    first_batch = nameres.lookup("aspirin", limit=5, offset=0)

    # Get next 5 results
    second_batch = nameres.lookup("aspirin", limit=5, offset=5)

    # They should be different
    if len(first_batch) > 0 and len(second_batch) > 0:
        assert first_batch[0]["curie"] != second_batch[0]["curie"]


def test_lookup_with_biolink_type():
    """Test lookup filtered by Biolink type."""
    # Look for a gene
    results = nameres.lookup("TP53", biolink_type="Gene", limit=10)

    assert len(results) > 0

    # Check that results are genes
    for result in results:
        types = result.get("types", [])
        assert any("Gene" in t for t in types)


def test_lookup_autocomplete():
    """Test autocomplete mode."""
    results = nameres.lookup("aspir", autocomplete=True, limit=10)

    assert len(results) > 0
    # Should find aspirin with partial match
    labels = [r.get("label", "").lower() for r in results]
    assert any("aspirin" in label for label in labels)


def test_lookup_no_results():
    """Test lookup with a query that should return no results."""
    results = nameres.lookup("xyzzynotarealentity123456", limit=10)
    assert len(results) == 0
