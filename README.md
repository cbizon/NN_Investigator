# NN_Investigator

A web application for investigating why pairs of biomedical entities do or do not merge into node normalization cliques.

## Quick Start

**Prerequisites**: Install [uv](https://github.com/astral-sh/uv) if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Run the application** (uv handles environment and dependencies automatically):
```bash
uv run python -m src.nn_investigator.app
```

Open http://localhost:5000 in your browser.

## How to Use

### 1. View Entity Pairs
The landing page shows all 30 entity pairs from [GitHub issue #335](https://github.com/NCATSTranslator/NodeNormalization/issues/335). Each row shows:
- Entity name
- Two CURIEs that should potentially normalize together
- Current evaluation status

Click **Investigate** to analyze any pair.

### 2. Investigate a Pair
The investigation page shows:
- Whether the CURIEs normalize to the same clique (✓ or ✗)
- Auto-detection of type mismatches (e.g., Cell vs Chemical)
- Preferred IDs for each CURIE
- All equivalent identifiers with clickable linkouts to external resources

**Navigation**: Use **Previous/Next** buttons to move between pairs sequentially.

### 3. Evaluate Pairs
At the bottom of each investigation page:
1. Select an assessment from the dropdown:
   - Should merge
   - Should not merge
   - Should not merge, different salt
   - Different types (cell/chemical)
   - Different types (chemical/protein)
   - Different species
   - Dangling CHEMBL
   - Requires further investigation

2. Add evaluation notes (optional)
3. Click **Save Evaluation**

Your evaluation appears in the main table and can be exported.

### 4. Export Results
Click **Export to Markdown** on the landing page to download a markdown table of all evaluations. Perfect for pasting into GitHub comments.

### 5. Add New Pairs
Click **Add Pair** in the navigation to investigate additional entity pairs.

## Installation (for development)

```bash
# Install dependencies in isolated environment
uv pip install --python .venv/bin/python -e ".[dev]"

# Run tests
uv run pytest tests/unit/
```

## About

This tool uses Node Normalization API with both conflation types enabled:
- **Gene/Protein conflation**: Merges genes with their protein products
- **Chemical/Drug conflation**: Merges drug formulations with active ingredients

The database (`nn_investigator.db`) contains 30 entity pairs from [NodeNormalization issue #335](https://github.com/NCATSTranslator/NodeNormalization/issues/335) where entities that should theoretically be the same are not merging into the same normalization clique.
