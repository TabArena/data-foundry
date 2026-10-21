"""Curated dataset definition for `qsar_bioconcentration` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    drop_columns,
    rdkit_descriptors,
)

RAW_FILE = "Grisoni_et_al_2016_EnvInt88.csv"
"""The UCI file: CAS, SMILES, the authors' Train/Test set, 9 Dragon descriptors, the class and logBCF."""

CLASS_LABELS = {1: "lipid storage", 2: "additional storage sites", 3: "metabolized or eliminated"}
"""The three mechanistic classes, as the old UCI page names them."""

DESCRIPTORS = ["nHM", "piPC09", "PCD", "X2Av", "MLOGP", "ON1V", "N-072", "B02(C-N)", "F04(C-O)"]
"""The 9 Dragon descriptors of the file, with the square brackets of two names replaced by parentheses."""

SWAPPED_PAIRS = {
    ("71-43-2", "110-82-7"): ("benzene", "cyclohexane"),
    ("91-20-3", "119-64-2"): ("naphthalene", "tetralin"),
    ("108-90-7", "542-18-7"): ("chlorobenzene", "chlorocyclohexane"),
}
"""Pairs of rows that carry each other's SMILES and descriptors: (CAS, CAS) -> (chemical, chemical). The BCF and the
class of each row belong to its CAS number (the authors' 2015 table, see curation_comments)."""

WRONG_STRUCTURE = {
    "131983-72-7": ("triticonazole", "trinexapac-ethyl"),
    "33423-92-6": ("1,3,6,8-tetrachlorodibenzo-p-dioxin", "1,3,7,9-tetrachlorodibenzo-p-dioxin"),
    "39227-28-6": ("1,2,3,4,7,8-hexachlorodibenzo-p-dioxin", "1,2,3,4,6,7-hexachlorodibenzo-p-dioxin"),
}
"""Rows whose SMILES, and so the descriptors computed from it, is another chemical than their CAS number, with no
partner row to repair them from: CAS -> (the chemical of the CAS number in Wikidata and PubChem, the chemical the
file's SMILES encodes in PubChem). Checked on 2026-10-07 for every row, on the connectivity block of the InChIKey."""


class QsarBioconcentration(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How does an organic chemical build up in fish: stored in fat, held in additional sites, or broken down "
            "and eliminated?"
        ),
        use_case=(
            "Before a fish test, a chemical assessor estimates the bioconcentration mechanism of an untested organic "
            "chemical from its structure, for example to decide whether the usual estimate from its octanol-water "
            "partitioning (how readily it dissolves in fat rather than water) can be trusted."
        ),
        row=(
            "One organic chemical with a measured bioconcentration factor in fish (776 chemicals, Grisoni et al. 2016)."
        ),
        predicted=(
            "The mechanism class, read from the measured bioconcentration and the measured octanol-water "
            "partitioning: lipid storage (59%), metabolized or eliminated (33%), or additional storage sites (8%)."
        ),
        known="The chemical's structure, as the source's nine descriptors and 193 more computed with RDKit.",
        split=(
            "Random chemicals, one row each, as in the source's random split: each prediction is a new chemical, "
            "usually of a chemical family already measured. A third of the chemicals belong to such families "
            "(congener series), and the test chemicals of a family whose relatives are in training score higher."
        ),
        changes=(
            "We drop the measured bioconcentration factor the class is read from, swap back the structures of three "
            "pairs of chemicals that carried each other's, and drop three chemicals with another chemical's "
            "structure; we replace the structure's text by RDKit's descriptors of it."
        ),
        fit="direct",
        fit_reason=(
            "The structure and its descriptors are known before a fish test, and a held-out chemical is an untested "
            "one: a random member of the historical BCF compilation, which often has relatives in training. The "
            "authors chose the nine descriptors on chemicals that also sit in our test folds; that favours those "
            "chemicals by at most about 0.015 macro ROC AUC."
        ),
    )

    # Dataset
    unique_name = "qsar_bioconcentration"
    year = "2016"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C56S46"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository (dataset 510, donated in 2019 by the Milano Chemometrics and QSAR
        Research Group) and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/qsar_bioconcentration && wget -P local-data-warehouse/qsar_bioconcentration/ https://archive.ics.uci.edu/static/public/510/qsar+bioconcentration+classes+dataset.zip && unzip local-data-warehouse/qsar_bioconcentration/qsar+bioconcentration+classes+dataset.zip -d local-data-warehouse/qsar_bioconcentration/ && rm local-data-warehouse/qsar_bioconcentration/qsar+bioconcentration+classes+dataset.zip

        sha256 of Grisoni_et_al_2016_EnvInt88.csv: 5bfd2d11afcd725e31bdc60be0cd1d7989024a00463ed9fd91d8951254cdc104
    """
    bibtex = """
        @article{grisoni2016investigating,
          title={Investigating the mechanisms of bioconcentration through {QSAR} classification trees},
          author={Grisoni, Francesca and Consonni, Viviana and Vighi, Marco and Villa, Sara and Todeschini, Roberto},
          journal={Environment International},
          volume={88},
          pages={198--205},
          year={2016},
          doi={10.1016/j.envint.2015.12.024}
        }
        @article{grisoni2015qsar,
          title={{QSAR} models for bioconcentration: is the increase in the complexity justified by more accurate predictions?},
          author={Grisoni, Francesca and Consonni, Viviana and Villa, Sara and Vighi, Marco and Todeschini, Roberto},
          journal={Chemosphere},
          volume={127},
          pages={171--179},
          year={2015},
          doi={10.1016/j.chemosphere.2015.01.047}
        }
    """
    curation_comments = """
        We start with Grisoni_et_al_2016_EnvInt88.csv from UCI 510: 779 organic chemicals with CAS number, SMILES, the authors' Train/Test set, 9 Dragon descriptors, the mechanistic class and the measured fish logBCF. The authors' 2015 BCF table (Chemosphere SI), which adds the experimental logKOW, is evidence only.

        - Prediction point: an organic chemical whose bioconcentration in fish has not been measured, before a fish test. Its structure (the SMILES) and the descriptors computed from it are known; the measured BCF, and so the class read from it, are not.
        - Target: bioconcentration_mechanism, the class of the file, named as on the old UCI page. The class is a rule on the measured logBCF and the experimental logKOW: with the 2015 table's logKOW, a band of 0.5 log units around the TGD line gives the file's class for 600 of the 607 shipped chemicals with a logKOW of at least 1 (thresholds inferred from the data). The 2015 table gives a logKOW for 773 of the 776 chemicals, measured for 651 and predicted for 122; the band gives the file's class for 72% of the 122, and below a logKOW of 1 the class is mostly lipid storage by convention.
        - logBCF dropped: it is the measurement the class is read from and is not known for a new chemical. MLOGP, the calculated logKOW among the descriptors, does not complete the rule in its place (decision table). The regression on logBCF is the file's other task (OpenML 46586); we ship the class, which the paper models and the 9 descriptors were selected for.
        - Dropped CAS (registry numbers, an identifier) and Set (the authors' random 75/25 split).
        - The structure: RDKit's 2D descriptors of the repaired SMILES as `rdkit_*` columns (`rdkit_descriptors`, RDKit 2026.03.6), 193 of the 217, the others constant here or copies. The 9 descriptors do not tell positional isomers apart (61 chemicals share them with another, 14 of those with another class); with RDKit's added, every chemical has its own values (decision table). Default LightGBM's macro ROC AUC on the first 15 of our splits: 0.745 with the 9, 0.757 with RDKit's added (better on 12 of 15 splits).
        - `SMILES` dropped, as in every SMILES dataset (2026-10-14): next to the 9 descriptors the SMILES as text (character n-grams) lowered LightGBM's macro ROC AUC from 0.735 to 0.723 (run of 2026-10-14, settings not recorded).
        - Repaired rows, 6: three pairs carry each other's SMILES and descriptors (benzene and cyclohexane, naphthalene and tetralin, chlorobenzene and chlorocyclohexane; CAS numbers looked up in Wikidata and PubChem). The BCF and the class belong to the CAS number, as the 2015 table lists all six with their right SMILES and the file's logBCF, and the descriptors follow the SMILES, so we swap the SMILES and the 9 descriptors back within each pair.
        - Dropped rows, 3: triticonazole and two dioxins carry the structure of another chemical and have no partner row to repair them from.
        - Renamed B02[C-N] and F04[C-O] to B02(C-N) and F04(C-O), since LightGBM and XGBoost refuse square brackets in feature names.
        - Split: IID, one row per distinct chemical, as in the source's random split. IID rests on the use case: each prediction is a new chemical, usually of a family already measured, and no chemical recurs (no copies across the split by InChIKey).
        - Note: the test chemicals often have relatives in training. Murcko scaffolds (ring skeletons) of the SMILES put 260 chemicals (34%) in 42 congener series, such as 64 biphenyls and 24 naphthalenes. A random forest scores macro ROC AUC 0.754 on random splits and 0.650 with the series held out; on our splits it scores 0.779 on test chemicals whose scaffold is in training and 0.655 on those with a new one. A split by scaffold cannot be scored (test folds of 30 to 556 rows, 3 of 30 without a class), so IID stays; a candidate for a scaffold-grouped variant.
        - Potential leak, kept on purpose: the authors selected the 9 descriptors on their 584 training chemicals, which sit in our test folds too. A random forest scores macro ROC AUC 0.069 higher on those chemicals than on the authors' test chemicals (one-sided p = 0.04 against random subsets), but also 0.054 higher (p = 0.09) on the 193 RDKit columns nobody selected, so at most about 0.015 is the selection; logistic regression shows no gap (0.006). Kept as the source's published descriptors next to RDKit's (CC 2026-10-14); dropping them would remove the selection at little cost (RDKit's alone score 0.758 against 0.763 with both).
    """

    # Task
    target = "bioconcentration_mechanism"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason="Grisoni et al. 2016 report the non-error rate (NER, balanced accuracy) with per-class sensitivity, specificity and precision, the Milano group's house measure, at argmax with no costs. Original rejected: NER. log_loss is the multiclass fallback."
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # UTF-8 with a byte-order mark and CRLF line ends; a CAS cell can hold several numbers in quotes
        return pd.read_csv(raw_dir / RAW_FILE, encoding="utf-8-sig")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # LightGBM and XGBoost refuse square brackets in feature names
        df = df.rename(columns={"B02[C-N]": "B02(C-N)", "F04[C-O]": "F04(C-O)"})
        df = _swap_back_structures(df)
        # the SMILES of these rows, and the descriptors computed from it, is another chemical than their CAS number
        df = df[~df["CAS"].isin(WRONG_STRUCTURE)]
        df = df.assign(**{self.target: df["Class"].map(CLASS_LABELS)})
        # The structure as numbers: RDKit's 2D descriptors in place of the SMILES (data_foundry.v2.chemistry)
        df = pd.concat([df, rdkit_descriptors(df["SMILES"])], axis=1)
        # CAS is an identifier, Set the authors' random split, logBCF the measurement the class is read from
        return drop_columns(df, ["CAS", "Set", "Class", "logBCF", "SMILES"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # B02(C-N) marks the presence of a C-N pair at topological distance 2: a yes/no flag, categorical (CLEAN-14).
        # The other descriptors (floats and counts, the RDKit fragment counts too where only 0 and 1 occur) stay
        # numeric; the target becomes a category.
        del df
        return FeatureTypes(categorical=["B02(C-N)"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        kept = _swap_back_structures(raw.rename(columns={"B02[C-N]": "B02(C-N)", "F04[C-O]": "F04(C-O)"}))
        kept = kept[~kept["CAS"].isin(WRONG_STRUCTURE)]
        # the authors' rule with MLOGP in place of the experimental logKOW (not in the file)
        logkow = kept["MLOGP"]
        tgd = np.where(logkow <= 6, 0.85 * logkow - 0.70, -0.20 * logkow**2 + 2.74 * logkow - 4.72)
        residual = kept["logBCF"] - tgd
        band = np.select([residual > 0.5, residual < -0.5], [2, 3], default=1)
        rule = pd.crosstab(
            kept["Class"].map(CLASS_LABELS).rename("class"),
            pd.Series(band, index=kept.index).map(lambda c: f"band with MLOGP: {CLASS_LABELS[c]}").rename("band"),
        )
        structure = pd.DataFrame(
            [
                {
                    "CAS": cas,
                    "chemical": name,
                    "the file's SMILES is": other,
                    "action": "SMILES and descriptors swapped",
                }
                for (cas_a, cas_b), (name_a, name_b) in SWAPPED_PAIRS.items()
                for cas, name, other in ((cas_a, name_a, name_b), (cas_b, name_b, name_a))
            ]
            + [
                {"CAS": cas, "chemical": name, "the file's SMILES is": other, "action": "row dropped"}
                for cas, (name, other) in WRONG_STRUCTURE.items()
            ]
        ).set_index("CAS")
        rdkit_columns = [column for column in df.columns if column.startswith("rdkit_")]
        isomers = pd.DataFrame(
            {
                "the 9 descriptors": _shared_descriptors(df, DESCRIPTORS, self.target),
                "with RDKit's descriptors": _shared_descriptors(df, [*DESCRIPTORS, *rdkit_columns], self.target),
            }
        )
        return [
            Decision(
                "The class is the target; logBCF is dropped",
                "The class is a band of 0.5 log units around the BCF that the TGD equation expects from the "
                "experimental logKOW, so logBCF gives the class away and is not known for a new chemical. With the "
                "authors' experimental logKOW (2015 table, not in the file) the band gives the class of 600 of 607 "
                "chemicals with logKOW of at least 1; with MLOGP, the calculated logKOW among the features, it gives "
                "the class of 471 of 776 (the diagonal of the table), so no descriptor completes the rule once logBCF "
                "is gone.",
                rule,
            ),
            Decision(
                "Swapped structures are repaired, three wrong structures dropped",
                "The SMILES, and the descriptors computed from it, of these rows is not the chemical of their CAS "
                "number (Wikidata and PubChem lookup of every CAS number). Three pairs carry each other's structure "
                "and get it back; the other three rows have no partner in the file.",
                structure,
            ),
            Decision(
                "SMILES replaced by RDKit's descriptors",
                "The 9 descriptors do not tell positional isomers apart; with RDKit's 2D descriptors of the SMILES "
                "every chemical has its own values, and the SMILES as text adds nothing next to descriptors "
                "(CHANGELOG, 2026-10-14).",
                isomers,
            ),
        ]


def _shared_descriptors(df: pd.DataFrame, columns: list[str], target: str) -> pd.Series:
    """How many chemicals share all of ``columns`` with another chemical, and how many of them differ in class."""
    groups = df.groupby(columns, sort=False, dropna=False, observed=True)[target]  # 0/1 flags are categories
    size, n_classes = groups.transform("size"), groups.transform("nunique")
    return pd.Series(
        {
            "chemicals": len(df),
            "distinct descriptor vectors": int(df[columns].drop_duplicates().shape[0]),
            "chemicals sharing their descriptors with another": int(size.gt(1).sum()),
            "of them in groups with more than one class": int(n_classes.gt(1).sum()),
        }
    )


def _swap_back_structures(df: pd.DataFrame) -> pd.DataFrame:
    """Give each row of :data:`SWAPPED_PAIRS` the SMILES and descriptors of its partner row (its own chemical)."""
    # the keys of SWAPPED_PAIRS are the (CAS, CAS) pairs; each CAS number maps to its partner
    partner = {a: b for a, b in SWAPPED_PAIRS} | {b: a for a, b in SWAPPED_PAIRS}
    row_of = pd.Series(df.index, index=df["CAS"])
    rows = df.index[df["CAS"].isin(list(partner))]
    source = row_of[df.loc[rows, "CAS"].map(partner)].to_numpy()
    df = df.copy()
    for column in ["SMILES", *DESCRIPTORS]:
        df.loc[rows, column] = df.loc[source, column].to_numpy()
    return df
