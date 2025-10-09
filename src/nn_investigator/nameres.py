"""Client for Name Resolution API."""

import requests
from typing import Optional


NAMERES_URL = "https://name-resolution-sri.renci.org"


def get_synonyms(preferred_curies: list[str]) -> dict:
    """
    Get synonyms for preferred CURIEs.

    Args:
        preferred_curies: List of preferred CURIEs to get synonyms for

    Returns:
        Dictionary mapping CURIEs to their synonym data
    """
    url = f"{NAMERES_URL}/synonyms"
    payload = {"preferred_curies": preferred_curies}

    response = requests.post(url, json=payload)
    response.raise_for_status()

    return response.json()


def lookup(
    query: str,
    autocomplete: bool = False,
    highlighting: bool = False,
    offset: int = 0,
    limit: int = 10,
    biolink_type: Optional[str] = None,
    only_prefixes: Optional[list[str]] = None,
    only_taxa: Optional[list[str]] = None
) -> list[dict]:
    """
    Look up CURIEs by name.

    Args:
        query: The search string
        autocomplete: Enable autocomplete/partial matching (default: False)
        highlighting: Enable search term highlighting (default: False)
        offset: Number of results to skip for pagination (default: 0)
        limit: Maximum number of results (default: 10)
        biolink_type: Filter by Biolink entity type (e.g., 'Disease', 'SmallMolecule')
        only_prefixes: Only include results from these namespaces
        only_taxa: Only include results from these taxa (e.g., ['NCBITaxon:9606'] for humans)

    Returns:
        List of matching entities with their CURIEs and metadata
    """
    url = f"{NAMERES_URL}/lookup"

    params = {
        "string": query,
        "autocomplete": str(autocomplete).lower(),
        "highlighting": str(highlighting).lower(),
        "offset": offset,
        "limit": limit
    }

    if biolink_type:
        params["biolink_type"] = biolink_type

    payload = {}
    if only_prefixes:
        payload["only_prefixes"] = only_prefixes
    if only_taxa:
        payload["only_taxa"] = only_taxa

    if payload:
        response = requests.post(url, params=params, json=payload)
    else:
        response = requests.post(url, params=params)

    response.raise_for_status()

    return response.json()


def bulk_lookup(queries: dict[str, dict]) -> dict:
    """
    Look up multiple names at once.

    Args:
        queries: Dictionary mapping query IDs to their search parameters.
                 Each value should be a dict with keys like 'string', 'biolink_type', etc.

    Returns:
        Dictionary mapping query IDs to their results
    """
    url = f"{NAMERES_URL}/bulk_lookup"

    response = requests.post(url, json=queries)
    response.raise_for_status()

    return response.json()
