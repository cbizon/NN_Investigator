"""Generate linkout URLs for different CURIE types."""


def get_curie_url(curie: str) -> str:
    """
    Get the appropriate URL for a CURIE based on its prefix.

    Args:
        curie: The CURIE (e.g., "UMLS:C5448035", "CHEBI:15377")

    Returns:
        URL string for the external resource
    """
    if ":" not in curie:
        return ""

    prefix, identifier = curie.split(":", 1)
    prefix = prefix.upper()

    # Map prefixes to their URL patterns
    url_patterns = {
        "UMLS": f"https://uts.nlm.nih.gov/uts/umls/concept/{identifier}",
        "MONDO": f"https://www.ebi.ac.uk/ols4/ontologies/mondo/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FMONDO_{identifier}",
        "CHEBI": f"https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:{identifier}",
        "DRUGBANK": f"https://go.drugbank.com/drugs/{identifier}",
        "DRUGCENTRAL": f"https://drugcentral.org/drugcard/{identifier}",
        "MESH": f"https://meshb.nlm.nih.gov/record/ui?ui={identifier}",
        "NCIT": f"https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&code={identifier}",
        "DOID": f"https://disease-ontology.org/?id=DOID:{identifier}",
        "HP": f"https://hpo.jax.org/app/browse/term/{curie}",
        "HGNC": f"https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/HGNC:{identifier}",
        "NCBIGENE": f"https://www.ncbi.nlm.nih.gov/gene/{identifier}",
        "UNIPROT": f"https://www.uniprot.org/uniprot/{identifier}",
        "UNIPROTKB": f"https://www.uniprot.org/uniprot/{identifier}",
        "ENSEMBL": f"https://useast.ensembl.org/id/{identifier}",
        "PUBCHEM.COMPOUND": f"https://pubchem.ncbi.nlm.nih.gov/compound/{identifier}",
        "CHEMBL.COMPOUND": f"https://www.ebi.ac.uk/chembl/compound_report_card/{identifier}",
        "RXCUI": f"https://mor.nlm.nih.gov/RxNav/search?searchBy=RXCUI&searchTerm={identifier}",
        "UNII": f"https://precision.fda.gov/uniisearch/srs/unii/{identifier}",
        "PR": f"https://www.ebi.ac.uk/ols4/ontologies/pr/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F{curie.replace(':', '_')}",
        "GTOPDB": f"https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId={identifier}",
    }

    # Return the specific URL if we have a pattern, otherwise use a generic search
    return url_patterns.get(prefix, f"https://biolink.github.io/biolink-model/?curie={curie}")
