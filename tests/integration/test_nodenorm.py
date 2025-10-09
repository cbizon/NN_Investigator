"""Integration tests for Node Normalization API client."""

import pytest
from src.nn_investigator import nodenorm


def test_normalize_curies():
    """Test normalizing CURIEs with the real API."""
    # Test with water (MESH and NCIT for ALS from the docs)
    result = nodenorm.normalize_curies(
        ["MESH:D014867", "NCIT:C34373"],
        conflate=True,
        drug_chemical_conflate=True
    )

    # Check that we got results for both
    assert "MESH:D014867" in result
    assert "NCIT:C34373" in result

    # Check water normalization
    water = result["MESH:D014867"]
    assert water is not None
    assert "id" in water
    assert water["id"]["identifier"] == "CHEBI:15377"
    assert "equivalent_identifiers" in water
    assert len(water["equivalent_identifiers"]) > 0

    # Check ALS normalization
    als = result["NCIT:C34373"]
    assert als is not None
    assert "id" in als
    assert als["id"]["identifier"] == "MONDO:0004976"


def test_get_preferred_id():
    """Test getting preferred ID for a CURIE."""
    preferred = nodenorm.get_preferred_id("MESH:D014867")
    assert preferred == "CHEBI:15377"


def test_get_preferred_id_not_found():
    """Test getting preferred ID for non-existent CURIE."""
    preferred = nodenorm.get_preferred_id("FAKE:999999")
    assert preferred is None


def test_get_equivalent_identifiers():
    """Test getting equivalent identifiers."""
    equivs = nodenorm.get_equivalent_identifiers("MESH:D014867")

    assert len(equivs) > 0
    assert any(e["identifier"] == "CHEBI:15377" for e in equivs)
    assert any(e["identifier"] == "MESH:D014867" for e in equivs)

    # Check that some have labels
    labeled = [e for e in equivs if "label" in e and e["label"]]
    assert len(labeled) > 0


def test_get_types():
    """Test getting Biolink types."""
    types = nodenorm.get_types("MESH:D014867")

    assert len(types) > 0
    assert "biolink:SmallMolecule" in types
    assert "biolink:ChemicalEntity" in types

    # First type should be most specific
    assert types[0] == "biolink:SmallMolecule"


def test_normalize_with_conflation_disabled():
    """Test normalization with different conflation settings."""
    # This is more of a functional test to ensure parameters are passed correctly
    result = nodenorm.normalize_curies(
        ["MESH:D014867"],
        conflate=False,
        drug_chemical_conflate=False
    )

    assert "MESH:D014867" in result
    # We still expect a result, just potentially different merging behavior
    assert result["MESH:D014867"] is not None
