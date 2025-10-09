# NN_Investigator

## Goal

A web application that helps users investigate why a pair of nodes does or does not merge into a node normalization clique.

## Basic Setup

* github: This project has a github repo at https://github.com/cbizon/NN_investigator
* uv: we are using uv for package and environment management with an ISOLATED VIRTUAL ENVIRONMENT
* tests: we are using pytest, and want to maintain high code coverage

### Environment Management - CRITICAL

**NEVER EVER INSTALL ANYTHING INTO SYSTEM LIBRARIES OR ANACONDA BASE ENVIRONMENT**

- ALWAYS use the isolated virtual environment at `.venv/`
- ALWAYS use `uv run` to execute commands, which automatically uses the isolated environment
- NEVER run `uv pip install` directly - it may pollute system packages
- If you need to install packages: `uv pip install --python .venv/bin/python <package>` OR just use `uv add <package>`
- To run the app: `uv run python -m src.nn_investigator.app`
- To run tests: `uv run pytest`
- The virtual environment is sacred. System packages are not your garbage dump.

## Key Dependencies

* flask
* sqlite3

### APIs

@docs/nodenorm.md
@docs/nameres.md

## Basic Workflow

We will start with a list of pairs to identify.  These can be loaded into a sqlite3 database.  A user might also add some pairs. 
The landing page shows the list of pairs.  The user can click to go to any of the pairs, which opens an investigation page.  When loaded, we hit nodenormalization with both types of conflation set to true.  So the page will show: the original pair, the normalized pair - the other identifiers coming back from NN. Additionally, the curies should all be linkouts.  The user can follow the linkouts and then select them.  THe page at each selected linkout can be retrieved and then combined into a single input to an LLM asking it to evaluate whether the two entities should be merged or not.

## Normalization

Concepts are represented in different vocabluaries, and we are working on equivalence cliques of those identifiers.  There are some subtleties to considier.  The main is the concept of "conflation".  Conflations are cases in which we allow cliques that are not precisely exact to merge.  The two conflations that we allow are gene/protein and chemical/drug.  Gene/Protein merges genes with their products.  Chemical/Drug merges Drug formulations with their active ingredient.  Because basic chemical normalization is largely structural based, it keeps e.g. different salt forms in different cliques.  However, drug/chemical normalization also has a side effect of often merging different salts or chiral forms/mixtures.

## ***RULES OF THE ROAD***

- Don't use mocks. They obscure problems

- Ask clarifying questions

- Don't make classes just to group code. It is non-pythonic and hard to test.

- Do not implement bandaids - treat the root cause of problems

- Don't use try/except as a way to hide problems.  It is often good just to let something fail and figure out why.

- Once we have a test, do not delete it without explicit permission.  

- Do not return made up results if an API fails.  Let it fail.

- When changing code, don't make duplicate functions - just change the function. We can always roll back changes if needed.

- Keep the directories clean, don't leave a bunch of junk laying around.

- When making pull requests, NEVER ever mention a `co-authored-by` or similar aspects. In particular, never mention the tool used to create the commit message or PR.

- Check git status before commits

