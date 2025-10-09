"""Client for Node Normalization API."""

import requests
from typing import Optional


NODENORM_URL = "https://nodenormalization-sri.renci.org/get_normalized_nodes"


def normalize_curies(
    curies: list[str],
    conflate: bool = True,
    drug_chemical_conflate: bool = True,
    description: bool = False
) -> dict:
    """
    Normalize CURIEs using the Node Normalization API.

    Args:
        curies: List of CURIEs to normalize
        conflate: Enable gene/protein conflation (default: True)
        drug_chemical_conflate: Enable drug/chemical conflation (default: True)
        description: Return descriptions (default: False)

    Returns:
        Dictionary mapping input CURIEs to their normalized results
    """
    payload = {
        "curies": curies,
        "conflate": conflate,
        "drug_chemical_conflate": drug_chemical_conflate,
        "description": description
    }

    response = requests.post(NODENORM_URL, json=payload)
    response.raise_for_status()

    return response.json()


def get_preferred_id(curie: str, conflate: bool = True, drug_chemical_conflate: bool = True) -> Optional[str]:
    """
    Get the preferred identifier for a CURIE.

    Args:
        curie: The CURIE to look up
        conflate: Enable gene/protein conflation (default: True)
        drug_chemical_conflate: Enable drug/chemical conflation (default: True)

    Returns:
        The preferred identifier, or None if not found
    """
    result = normalize_curies([curie], conflate=conflate, drug_chemical_conflate=drug_chemical_conflate)

    if curie in result and result[curie] is not None:
        return result[curie]["id"]["identifier"]

    return None


def get_equivalent_identifiers(
    curie: str,
    conflate: bool = True,
    drug_chemical_conflate: bool = True
) -> list[dict]:
    """
    Get all equivalent identifiers for a CURIE.

    Args:
        curie: The CURIE to look up
        conflate: Enable gene/protein conflation (default: True)
        drug_chemical_conflate: Enable drug/chemical conflation (default: True)

    Returns:
        List of equivalent identifier dictionaries with 'identifier' and optional 'label' keys
    """
    result = normalize_curies([curie], conflate=conflate, drug_chemical_conflate=drug_chemical_conflate)

    if curie in result and result[curie] is not None:
        return result[curie].get("equivalent_identifiers", [])

    return []


def get_types(curie: str, conflate: bool = True, drug_chemical_conflate: bool = True) -> list[str]:
    """
    Get the Biolink types for a CURIE.

    Args:
        curie: The CURIE to look up
        conflate: Enable gene/protein conflation (default: True)
        drug_chemical_conflate: Enable drug/chemical conflation (default: True)

    Returns:
        List of Biolink types (most specific first)
    """
    result = normalize_curies([curie], conflate=conflate, drug_chemical_conflate=drug_chemical_conflate)

    if curie in result and result[curie] is not None:
        return result[curie].get("type", [])

    return []
