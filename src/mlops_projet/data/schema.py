"""Contrat de données du jeu Bank Marketing."""

import pandera.pandas as pa

OUI_NON = ["yes", "no"]

bank_schema = pa.DataFrameSchema(
    {
        "age": pa.Column(int, pa.Check.in_range(18, 100)),
        "job": pa.Column(str, pa.Check.isin([
            "admin.", "blue-collar", "entrepreneur", "housemaid",
            "management", "retired", "self-employed", "services",
            "student", "technician", "unemployed", "unknown",
        ])),
        "marital": pa.Column(str, pa.Check.isin(["married", "single", "divorced"])),
        "education": pa.Column(str, pa.Check.isin(["primary", "secondary", "tertiary", "unknown"])),
        "default": pa.Column(str, pa.Check.isin(OUI_NON)),
        "balance": pa.Column(int),
        "housing": pa.Column(str, pa.Check.isin(OUI_NON)),
        "loan": pa.Column(str, pa.Check.isin(OUI_NON)),
        "contact": pa.Column(str, pa.Check.isin(["cellular", "telephone", "unknown"])),
        "day": pa.Column(int, pa.Check.in_range(1, 31)),
        "month": pa.Column(str, pa.Check.isin([
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec",
        ])),
        "duration": pa.Column(int, pa.Check.ge(0)),
        "campaign": pa.Column(int, pa.Check.ge(1)),
        "pdays": pa.Column(int, pa.Check.ge(-1)),
        "previous": pa.Column(int, pa.Check.ge(0)),
        "poutcome": pa.Column(str, pa.Check.isin(["success", "failure", "other", "unknown"])),
        "y": pa.Column(str, pa.Check.isin(OUI_NON)),
    },
    checks=[
        # 1. Entre colonnes : pdays = -1 si et seulement si previous = 0
        pa.Check(
            lambda d: (d["pdays"] == -1) == (d["previous"] == 0),
            name="jamais_contacte_coherent",
        ),
        # 2. Entre colonnes, en simple avertissement
        pa.Check(
            lambda d: (d["poutcome"] == "unknown") <= (d["previous"] == 0),
            name="poutcome_unknown_si_jamais_contacte",
            raise_warning=True,
        ),
        # 3. Statistique : le taux de « yes » doit rester plausible
        pa.Check(
            lambda d: 0.05 <= d["y"].eq("yes").mean() <= 0.25,
            name="taux_de_yes_plausible",
        ),
    ],
    strict=True,  # aucune colonne en plus, aucune en moins
)


def validate_bank_data(df):
    """Vérifie le contrat. Lève une erreur qui liste TOUS les problèmes."""
    return bank_schema.validate(df, lazy=True)