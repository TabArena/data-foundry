"""Curated dataset definition for `qsar_oral_toxicity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes

N_BITS = 1024
"""The UCI file holds 1,024 fingerprint bits, then the class."""

N_TRAINING_ROWS = 6744
"""The file stores the authors' 6,744 training molecules first, then their 2,248 test molecules (paper, Table 1)."""


class QsarOralToxicity(AbstractCuratedDataset):
    # Dataset
    unique_name = "qsar_oral_toxicity"
    year = "2019"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5PS4J"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository (dataset 508, donated by the Milano Chemometrics and QSAR
        Research Group in 2019) and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/qsar_oral_toxicity && wget -P local-data-warehouse/qsar_oral_toxicity/ https://archive.ics.uci.edu/static/public/508/qsar+oral+toxicity.zip && unzip local-data-warehouse/qsar_oral_toxicity/qsar+oral+toxicity.zip -d local-data-warehouse/qsar_oral_toxicity/ && rm local-data-warehouse/qsar_oral_toxicity/qsar+oral+toxicity.zip

        sha256 of qsar_oral_toxicity.csv: c8ec16179f505370c13491a2c98e0918aae3680270aad0a6f95de3aeb300c874
    """
    bibtex = """
        @article{ballabio2019integrated,
          title={Integrated {QSAR} Models to Predict Acute Oral Systemic Toxicity},
          author={Ballabio, Davide and Grisoni, Francesca and Consonni, Viviana and Todeschini, Roberto},
          journal={Molecular Informatics},
          volume={38},
          number={8-9},
          pages={1800124},
          year={2019},
          doi={10.1002/minf.201800124}
        }
        @article{mansouri2021catmos,
          title={{CATMoS}: Collaborative Acute Toxicity Modeling Suite},
          author={Mansouri, Kamel and Karmaus, Agnes L. and Fitzpatrick, Jeremy and Patlewicz, Grace and Pradeep, Prachi and others},
          journal={Environmental Health Perspectives},
          volume={129},
          number={4},
          pages={047013},
          year={2021},
          doi={10.1289/EHP8495}
        }
    """
    curation_comments = """
        We start with qsar_oral_toxicity.csv from UCI 508: 8,992 chemicals, 1,024 binary fingerprint bits and the class (no header, no identifiers). It is the very toxic (VT) endpoint of the calibration set of the ICCVAM "Predictive Models for Acute Oral Systemic Toxicity" project (rat oral LD50 data; its consensus models became CATMoS), with fingerprints computed by Ballabio et al. (2019).

        - Prediction point: a chemical without an acute oral toxicity test, before any animal test. Every feature is computed from its QSAR-ready structure (salts, solvents and stereochemistry removed), so all of them exist at prediction time.
        - Target: `very_toxic` is "Yes" when the rat oral LD50 is below 50 mg/kg (the file's "positive"), else "No" (paper, Sec. 2.1). The paper scores the non-error rate; we keep the collection's ROC AUC.
        - Features: binary extended connectivity fingerprints computed with Dragon 7 (paper, Sec. 2.2), 1,024 hashed bits, named `ecfp_1` to `ecfp_1024` in file order and kept as numeric 0/1 columns. No bit is constant and no two bits are equal.
        - Duplicates dropped: the salt forms, hydrates and stereoisomers of one compound share the QSAR-ready parent structure and so the bit vector (406 repeated vectors, 894 rows; the project's training file shows the same 406 repeated parents by InChIKey). We drop the 477 exact copies and then every row of the 11 bit vectors that occur with both classes (22 rows), as for wine_quality and jm1, so a test chemical never has its parent structure in train; 8,493 chemicals remain (708 very toxic, 8.3%; decision table). The source kept the copies.
        - Note: the class depends on the counter-ion in some cases (sodium and potassium cyanide are very toxic, silver cyanide is not), which the parent structure does not show.
        - IID split: stratified 3-fold cross-validation with 3 repeats over the chemicals. The source splits at random: the project drew its evaluation set "without supervised sampling of the chemicals based on structures" (Mansouri et al. 2021), and the file stores the authors' stratified random training and test sets in order (decision table), which we do not keep. The file holds no structure or identifier, so a scaffold split cannot be built.
        - Note: the score depends on how close a test chemical is to the training chemicals, the applicability domain of any QSAR model (random forest ROC AUC 0.681 below a Tanimoto similarity of 0.5 to the nearest training chemical, 0.954 above 0.85). It does not come from series a random split lets a model memorise: at Tanimoto 0.9 only 456 rows (5.4%) have any analog, and the 708 very toxic chemicals sit in 692 distinct clusters.
        - Scope: the features are a vectorised molecular graph, as in qsar_tid_11. On repeat 0 of the shipped splits a random forest (ROC AUC 0.883) and LightGBM (0.869) match a similarity-weighted nearest-neighbour model of the paper's N3 kind (0.877).
    """

    # Task
    target = "very_toxic"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "qsar_oral_toxicity.csv", sep=";", header=None)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        bits = [f"ecfp_{i + 1}" for i in range(N_BITS)]
        df.columns = [*bits, self.target]
        df[self.target] = df[self.target].map({"positive": "Yes", "negative": "No"})
        # Salt forms, hydrates and stereoisomers of one parent structure share the bit vector: keep one row per
        # vector, and drop every vector that occurs with both classes.
        df = df.drop_duplicates()
        return df[~df.duplicated(subset=bits, keep=False)]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The 1,024 bits stay numeric 0/1; the target becomes a category.
        return FeatureTypes()

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        positive = raw[N_BITS] == "positive"
        vector = pd.util.hash_pandas_object(raw.iloc[:, :N_BITS], index=False)
        copies = vector.map(vector.value_counts())
        classes = positive.groupby(vector).transform("nunique")
        kind = pd.Series("bit vector occurs once", index=raw.index)
        kind[(copies > 1) & (classes == 1)] = "repeated bit vector, one class"
        kind[classes > 1] = "repeated bit vector, both classes"
        order = ["bit vector occurs once", "repeated bit vector, one class", "repeated bit vector, both classes"]
        duplicates = pd.DataFrame(
            {
                "rows": kind.value_counts(),
                "distinct bit vectors": vector.groupby(kind).nunique(),
                "very toxic rows": positive.groupby(kind).sum(),
            }
        ).reindex(order)
        duplicates["rows kept"] = [
            duplicates.loc[order[0], "rows"],
            duplicates.loc[order[1], "distinct bit vectors"],
            0,
        ]
        duplicates.loc["total"] = duplicates.sum()
        duplicates.index.name = "UCI rows"

        block = pd.Series("authors' training set", index=raw.index)
        block.iloc[N_TRAINING_ROWS:] = "authors' test set"
        file_order = pd.DataFrame(
            {"rows": block.value_counts(sort=False), "very toxic": positive.groupby(block, sort=False).sum()}
        )
        file_order.index.name = "position in the UCI file"
        return [
            Decision(
                "Copies of a parent structure dropped",
                "The bits are computed from the QSAR-ready parent structure, so salts, hydrates and stereoisomers "
                "of one compound share the bit vector. One row per vector is kept, and vectors with both classes "
                f"are dropped; {len(df):,} chemicals remain.",
                duplicates,
            ),
            Decision(
                "The file's order is the authors' split; we use cross-validation",
                "The first 6,744 rows are the authors' stratified random training set and the last 2,248 their test "
                "set (Ballabio et al. 2019, Table 1: 556 and 185 very toxic). Both were drawn at random, so the "
                "recommended IID cross-validation replaces them.",
                file_order,
            ),
        ]
