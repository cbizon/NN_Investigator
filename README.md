# NN_Investigator

A web application for investigating why pairs of nodes do or do not merge into a node normalization clique.

## Overview

NN_Investigator helps users analyze entity pairs that should theoretically normalize to the same concept but don't according to Node Normalization services. The application provides a visual interface to:

- View a list of entity pairs that may or may not merge
- Investigate individual pairs to see their normalization results
- Compare equivalent identifiers between two CURIEs
- Add new pairs for investigation

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for package and environment management.

```bash
# Create virtual environment
uv venv

# Install dependencies
uv pip install -e ".[dev]"
```

## Usage

### Load Initial Data

Load the initial set of entity pairs from [GitHub issue #335](https://github.com/NCATSTranslator/NodeNormalization/issues/335):

```bash
python load_initial_data.py
```

### Run the Application

```bash
python -m src.nn_investigator.app
```

Then open http://localhost:5000 in your browser.

### Run Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run with coverage
pytest --cov=src --cov-report=term-missing
```

## Project Structure

```
NN_investigator/
├── src/nn_investigator/
│   ├── __init__.py
│   ├── app.py              # Flask application
│   ├── database.py         # Database operations
│   ├── nodenorm.py         # Node Normalization API client
│   └── nameres.py          # Name Resolution API client
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Landing page
│   ├── investigate.html    # Investigation page
│   └── add_pair.html       # Add pair form
├── tests/
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests with real APIs
├── load_initial_data.py    # Script to load initial pairs
└── pyproject.toml          # Project configuration
```

## APIs

The application uses two key APIs:

- **Node Normalization**: Converts CURIEs to their preferred identifiers and finds equivalent identifiers
- **Name Resolution**: Maps between entity names and CURIEs, provides synonyms

See documentation in `docs/` for more details.

## Features

- **Landing Page**: Browse all entity pairs in a table
- **Investigation Page**: For each pair:
  - Shows normalization results from Node Normalization API
  - Displays preferred IDs and labels
  - Lists all equivalent identifiers
  - Indicates whether the pair merges into the same clique
  - Provides clickable CURIE links
- **Add Pairs**: Users can add new entity pairs to investigate
- **Delete Pairs**: Remove pairs from the database

## Normalization

The application uses Node Normalization with both types of conflation enabled:

- **Gene/Protein conflation**: Merges genes with their protein products
- **Chemical/Drug conflation**: Merges drug formulations with active ingredients

## Development

### Running in Debug Mode

The Flask app runs with `debug=True` by default when executed directly:

```bash
python -m src.nn_investigator.app
```

### Database

The application uses SQLite3 for storing entity pairs. The database file is `nn_investigator.db` (ignored by git).

To reset the database, simply delete the file and run `load_initial_data.py` again.
