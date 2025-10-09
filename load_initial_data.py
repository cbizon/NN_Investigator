"""Load initial entity pairs from GitHub issue #335."""

from src.nn_investigator.database import init_db, add_pair


def load_initial_pairs():
    """Load the initial pairs from issue #335."""
    # Initialize the database
    init_db()

    # Data from https://github.com/NCATSTranslator/NodeNormalization/issues/335
    pairs = [
        ("lovotibeglogene autotemcel", "UMLS:C5447474", "lovotibeglogene autotemcel", "DRUGBANK:DB18680", "Lovotibeglogene autotemcel"),
        ("coagulation factor xiii", "NCBIGene:100153504", "F13A1", "UniProtKB:A0A8D0SF31", "A0A8D0SF31_PIG Coagulation factor XIII A chain (trembl)"),
        ("lebrikizumab", "UNII:U9JLP7V031", "lebrikizumab", "DRUGBANK:DB11914", "Lebrikizumab"),
        ("haem arginate", "UNII:R1B526117P", "Heme arginate", "PUBCHEM.COMPOUND:135564839", "Haem arginate"),
        ("nogapendekin alfa", "CHEMBL.COMPOUND:CHEMBL4297690", "NOGAPENDEKIN ALFA", "RXCUI:2682677", "nogapendekin alfa inbakicept-pmln 1 MG/ML"),
        ("botulinum toxin type a", "CHEBI:3160", "botulinum toxin type A", "DRUGBANK:DB00083", "Botulinum toxin type A"),
        ("samarium sm-153 lexidronam", "UNII:745X144DZY", "Unii-745X144dzy", "UNII:7389YR3OOV", "Samarium Sm-153 Lexidronam Pentasodium"),
        ("atidarsagene autotemcel", "UMLS:C5556517", "atidarsagene autotemcel", "DRUGBANK:DB17538", "Atidarsagene autotemcel"),
        ("idecabtagene vicleucel", "UMLS:C3899973", "idecabtagene vicleucel", "DRUGBANK:DB16665", "Idecabtagene vicleucel"),
        ("afamitresgene autoleucel", "UMLS:C5448035", "afamitresgene autoleucel", "DRUGBANK:DB18592", "Afamitresgene autoleucel"),
        ("vilobelimab", "UNII:F5T0RF9ZJA", "vilobelimab", "PUBCHEM.COMPOUND:137254326", "Vilobelimab"),
        ("pancrelipase", "CHEBI:81916", "Pancrelipase", "UNII:FQ3DRG0N5K", "Pancrelipase"),
        ("donislecel", "UMLS:C5707881", "donislecel", "DRUGBANK:DB17961", "Donislecel"),
        ("toripalimab", "UNII:8JXN261VVA", "toripalimab", "DRUGBANK:DB15043", "Toripalimab"),
        ("ziconotide", "CHEBI:142406", "ziconotide", "PUBCHEM.COMPOUND:16135415", "Ziconotide"),
        ("berdazimer", "UNII:ORT9SID4QY", "berdazimer sodium", "DRUGBANK:DB18712", "Berdazimer"),
        ("fitusiran", "CHEMBL.COMPOUND:CHEMBL4297754", "FITUSIRAN", "DRUGBANK:DB15002", "Fitusiran"),
        ("cosibelimab", "CHEMBL.COMPOUND:CHEMBL4297729", "COSIBELIMAB", "GTOPDB:13676", "cosibelimab"),
        ("dibucaine", "CHEBI:247956", "Cinchocaine", "UNII:J31043J63M", "Dibucaine benzoate"),
        ("lifileucel", "UMLS:C4053624", "lifileucel", "DRUGBANK:DB17107", "Lifileucel"),
        ("coagulation factor x", "PR:000007294", "coagulation factor X", "DRUGBANK:DB13148", "Coagulation factor X human"),
        ("marstacimab", "UNII:0UB3OA67O7", "marstacimab", "DRUGBANK:DB17725", "Marstacimab"),
        ("thymoglobulin", "UNII:D7RD81HE4W", "thymoglobulin", "UMLS:C0359156", "Thymoglobulin"),
        ("pegzilarginase", "CHEMBL.COMPOUND:CHEMBL4297803", "PEGZILARGINASE", "UNII:4YV4KW88GD", "PEGZILARGINASE"),
        ("anti-d immunoglobulin", "DRUGBANK:DB09312", "Antilymphocyte immunoglobulin (horse)", "UMLS:C5192004", "Human anti-D immunoglobulin-containing product"),
        ("tarlatamab", "GTOPDB:12969", "tarlatamab", "DRUGBANK:DB17256", "Tarlatamab"),
        ("axatilimab", "UNII:R96Z451BMC", "axatilimab", "DRUGBANK:DB16388", "Axatilimab"),
        ("interferon gamma", "PR:000000017", "interferon gamma", "DRUGBANK:DB15753", "Interferon Gamma"),
        ("bleomycin", "CHEBI:3139", "bleomycin", "CHEBI:22907", "Bleomycin"),
        ("pericyazine", "CHEBI:31981", "Periciazine", "PUBCHEM.COMPOUND:71751521", "Pericyazine-d4"),
    ]

    for entity_name, curie_1, label_1, curie_2, label_2 in pairs:
        add_pair(
            entity_name=entity_name,
            curie_1=curie_1,
            curie_1_label=label_1,
            curie_2=curie_2,
            curie_2_label=label_2,
            notes="From GitHub issue #335"
        )

    print(f"Loaded {len(pairs)} entity pairs into the database")


if __name__ == "__main__":
    load_initial_pairs()
