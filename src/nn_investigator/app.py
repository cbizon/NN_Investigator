"""Flask application for NN Investigator."""

from flask import Flask, render_template, request, redirect, url_for, flash
from . import database
from . import nodenorm
from .linkouts import get_curie_url


app = Flask(__name__, template_folder="../../templates", static_folder="../../static")
app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"

# Register the linkout function as a template filter
app.jinja_env.globals.update(get_curie_url=get_curie_url)


@app.route("/")
def index():
    """Landing page showing all entity pairs."""
    pairs = database.get_all_pairs()
    return render_template("index.html", pairs=pairs)


@app.route("/export")
def export_markdown():
    """Export all pairs to markdown table format."""
    pairs = database.get_all_pairs()

    # Build markdown table
    md_lines = []
    md_lines.append("| Entity Name | Evaluation | Notes |")
    md_lines.append("|------------|------------|-------|")

    for pair in pairs:
        entity_name = pair["entity_name"]
        evaluation = pair["evaluation"] or "—"
        notes = pair["evaluation_notes"] or "—"

        # Escape pipe characters in the content
        entity_name = entity_name.replace("|", "\\|")
        evaluation = evaluation.replace("|", "\\|")
        notes = notes.replace("|", "\\|").replace("\n", " ")

        md_lines.append(f"| {entity_name} | {evaluation} | {notes} |")

    markdown_content = "\n".join(md_lines)

    # Return as downloadable file
    from flask import Response
    return Response(
        markdown_content,
        mimetype="text/markdown",
        headers={"Content-Disposition": "attachment;filename=entity_pairs_export.md"}
    )


@app.route("/pair/<int:pair_id>", methods=["GET", "POST"])
def investigate_pair(pair_id):
    """Investigation page for a specific entity pair."""
    pair = database.get_pair(pair_id)

    if not pair:
        flash("Pair not found", "error")
        return redirect(url_for("index"))

    # Handle evaluation submission
    if request.method == "POST":
        evaluation = request.form.get("evaluation")
        evaluation_notes = request.form.get("evaluation_notes")

        if evaluation:
            database.update_evaluation(pair_id, evaluation, evaluation_notes or None)
            flash("Evaluation saved", "success")
            return redirect(url_for("investigate_pair", pair_id=pair_id))
        else:
            flash("Please select an evaluation", "error")

    # Normalize both CURIEs
    norm_result = nodenorm.normalize_curies(
        [pair["curie_1"], pair["curie_2"]],
        conflate=True,
        drug_chemical_conflate=True
    )

    # Extract normalization data
    curie_1_data = norm_result.get(pair["curie_1"])
    curie_2_data = norm_result.get(pair["curie_2"])

    # Check if they normalize to the same preferred ID
    same_clique = False
    different_types_cell_chemical = False

    if curie_1_data and curie_2_data:
        preferred_1 = curie_1_data.get("id", {}).get("identifier")
        preferred_2 = curie_2_data.get("id", {}).get("identifier")
        same_clique = preferred_1 == preferred_2

        # Check for different types: Cell vs ChemicalEntity
        types_1 = set(curie_1_data.get("type", []))
        types_2 = set(curie_2_data.get("type", []))

        has_cell_1 = any("Cell" in t for t in types_1)
        has_cell_2 = any("Cell" in t for t in types_2)
        has_chemical_1 = any("Chemical" in t for t in types_1)
        has_chemical_2 = any("Chemical" in t for t in types_2)

        different_types_cell_chemical = (has_cell_1 and has_chemical_2) or (has_chemical_1 and has_cell_2)

    # Get all pair IDs for navigation
    all_pairs = database.get_all_pairs()
    pair_ids = [p["id"] for p in all_pairs]

    # Find previous and next pair IDs
    try:
        current_index = pair_ids.index(pair_id)
        prev_id = pair_ids[current_index - 1] if current_index > 0 else None
        next_id = pair_ids[current_index + 1] if current_index < len(pair_ids) - 1 else None
    except ValueError:
        prev_id = None
        next_id = None

    return render_template(
        "investigate.html",
        pair=pair,
        curie_1_data=curie_1_data,
        curie_2_data=curie_2_data,
        same_clique=same_clique,
        different_types_cell_chemical=different_types_cell_chemical,
        prev_id=prev_id,
        next_id=next_id
    )


@app.route("/add", methods=["GET", "POST"])
def add_pair():
    """Add a new entity pair."""
    if request.method == "POST":
        entity_name = request.form.get("entity_name")
        curie_1 = request.form.get("curie_1")
        curie_1_label = request.form.get("curie_1_label")
        curie_2 = request.form.get("curie_2")
        curie_2_label = request.form.get("curie_2_label")
        notes = request.form.get("notes")

        if not all([entity_name, curie_1, curie_2]):
            flash("Entity name, curie_1, and curie_2 are required", "error")
            return redirect(url_for("add_pair"))

        pair_id = database.add_pair(
            entity_name=entity_name,
            curie_1=curie_1,
            curie_2=curie_2,
            curie_1_label=curie_1_label or None,
            curie_2_label=curie_2_label or None,
            notes=notes or None
        )

        flash(f"Added new pair: {entity_name}", "success")
        return redirect(url_for("investigate_pair", pair_id=pair_id))

    return render_template("add_pair.html")


@app.route("/pair/<int:pair_id>/delete", methods=["POST"])
def delete_pair(pair_id):
    """Delete an entity pair."""
    deleted = database.delete_pair(pair_id)

    if deleted:
        flash("Pair deleted successfully", "success")
    else:
        flash("Pair not found", "error")

    return redirect(url_for("index"))


def init_app():
    """Initialize the application and database."""
    database.init_db()
    return app


if __name__ == "__main__":
    app = init_app()
    app.run(debug=True)
