"""Curated dataset definition for `qsar_oral_toxicity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary

N_BITS = 1024
"""The UCI file holds 1,024 fingerprint bits, then the class."""

N_TRAINING_ROWS = 6744
"""The file stores the authors' 6,744 training molecules first, then their 2,248 test molecules (paper, Table 1)."""

PARENT_PAIRS = (
    (3238, 6358),
    (3952, 7628),
    (3785, 8179),
    (6671, 6689),
    (6675, 8967),
    (2900, 5706),
    (4384, 4996),
    (4538, 7203),
    (6672, 6690),
)
"""Rows of the UCI file that hold one parent structure twice, as (the row kept, the row dropped).

Nine parents (a free acid and its salt or tautomer under two CASRNs, all not very toxic) survive the deduplication
twice, because the two entries differ in their bits. The pairs come from linking the file to the project's
structure file `trainingset_171130.txt` by row order; both blocks of the file are in CASRN order.
"""

PARENT_KEPT_TWICE = tuple(dropped for _, dropped in PARENT_PAIRS)


class QsarOralToxicity(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a chemical very toxic when swallowed, judged from its structure alone?",
        use_case=(
            "A regulator or a chemical maker screens chemicals without animal test data and flags the very toxic "
            "ones, to set priorities and labels without new animal tests (the US ICCVAM project behind the CATMoS "
            "models)."
        ),
        row=(
            "One chemical of the calibration set of the US ICCVAM acute oral toxicity project, with rat test data "
            "(8,484 chemicals after removing salt forms and copies)."
        ),
        predicted=(
            "Whether the swallowed dose that kills half of the rats is 50 mg per kg of body weight or less, the top "
            "acute oral hazard category (8% are very toxic). A quarter of the chemicals carry that category without "
            "a measured dose."
        ),
        known=(
            "1,024 on/off fingerprint bits computed from the chemical's structure, with salts, solvents and "
            "stereochemistry removed."
        ),
        split=(
            "Random chemicals; salt forms and hydrates of one compound share a fingerprint and are kept once, so a "
            "test chemical never has its parent structure in training. The rows carry no identifier, but they can be "
            "linked to the project's structure file by their order, which is how we checked this."
        ),
        changes=(
            "We drop exact copies of a fingerprint, the 22 rows of fingerprints that occur with both classes, and "
            "nine rows whose parent structure is already in another row; the source kept them and fixed one training "
            "and test set."
        ),
        fit="direct",
        fit_reason=(
            "The features come from the structure, which exists before any test. The score depends on how close a new"
            " chemical is to the reference set (random forest ROC AUC 0.681 for distant chemicals, 0.954 for close "
            "ones)."
        ),
    )

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
        - Target: `very_toxic` is "Yes" when the rat oral LD50 is 50 mg/kg or less (the file's "positive"), else "No" (paper, Sec. 2.1; CATMoS Methods, "LD50<=50mg/kg"). The 44 chemicals at exactly 50 mg/kg are positive, and the label is the top regulatory hazard category on every row: 2,258 rows (25%) carry that category without a point LD50.
        - Features: binary extended connectivity fingerprints (paper, Sec. 2.2) computed with Dragon 7 (Sec. 2.7), radius 2 with 2 bits per fragment (ECFP_1024_02 or _02R of Table 2; the file does not say which), 1,024 hashed bits, named `ecfp_1` to `ecfp_1024` in file order and typed categorical, the house form for 0/1 presence flags (CLEAN-14; Lennart, 2026-10-21). No bit is constant and no two bits are equal. 97 of the project's QSAR-ready structures still carry stereo markers, which the fingerprint ignores.
        - Duplicates dropped: the salt forms, hydrates and stereoisomers of one compound share the QSAR-ready parent structure and so the bit vector (406 repeated vectors, 894 rows; by InChIKey the project's training file has 405 repeated parents over 891 rows, which agrees with the vectors on 394 of them, and 12 of the repeated vectors are hash collisions of different chemicals rather than one parent). We drop the 477 exact copies and then every row of the 11 bit vectors that occur with both classes (22 rows), as for wine_quality and jm1; nine parents still keep two rows with different vectors (tautomer or salt entries, all "No"), of which we drop the later row, so a test chemical never has its parent structure in train. 8,484 chemicals remain (708 very toxic, 8.3%; decision tables). The source kept the copies.
        - Note: the class depends on the counter-ion in some cases (sodium and potassium cyanide are very toxic, silver cyanide is not), which the parent structure does not show.
        - IID split: stratified 3-fold cross-validation with 3 repeats over the chemicals. The source splits at random: the project drew its evaluation set "without supervised sampling of the chemicals based on structures" (Mansouri et al. 2021), and the file stores the authors' stratified random training and test sets in order (decision table), which we do not keep. The split rests on the use case, a new chemical each time with no entity that recurs, and on these structure-blind source protocols; the file carries no identifier, but its rows can be linked to the project's structure file by order, so a scaffold key could be reconstructed.
        - Note: the score depends on how close a test chemical is to the training chemicals, the applicability domain of any QSAR model (random forest ROC AUC 0.681 below a Tanimoto similarity of 0.5 to the nearest training chemical, 0.954 above 0.85). Near copies carry little of it (at Tanimoto 0.9 only 456 rows, 5.4%, have any analog, the near-copy gap is 0.006), but chemotypes do: held out by structure clusters (Butina, Tanimoto 0.5) a random forest falls from 0.882 to 0.842, and on the reconstructed Murcko scaffolds from 0.887 to 0.843, with the model ranking unchanged.
        - Scope: the features are a vectorised molecular graph, as in qsar_tid_11. On repeat 0 of the shipped splits a random forest (ROC AUC 0.883) and LightGBM (0.869) match a similarity-weighted nearest-neighbour model of the paper's N3 kind (0.877).
    """

    # Task
    target = "very_toxic"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Ballabio et al. 2019 report the non-error rate with sensitivity and specificity, the group's "
            "house measure, without costs; 25% very toxic. Original rejected: NER. roc_auc is the binary "
            "fallback."
        ),
    )

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
        df = df[~df.duplicated(subset=bits, keep=False)]
        # Nine parents survive with two different vectors (tautomer or salt entries); keep the first row of each.
        return df.drop(index=list(PARENT_KEPT_TWICE))

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The 1,024 bits are 0/1 presence flags: categorical (CLEAN-14); the target becomes a category.
        return FeatureTypes(categorical=[f"ecfp_{i + 1}" for i in range(N_BITS)])

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

        pairs = pd.DataFrame(PARENT_PAIRS, columns=["row kept", "row dropped"])
        pairs["bits in common"] = [
            int((raw.iloc[kept, :N_BITS].to_numpy() & raw.iloc[dropped, :N_BITS].to_numpy()).sum())
            for kept, dropped in PARENT_PAIRS
        ]
        pairs["very toxic"] = [bool(positive.iloc[kept] or positive.iloc[dropped]) for kept, dropped in PARENT_PAIRS]
        return [
            Decision(
                "Copies of a parent structure dropped",
                "The bits are computed from the QSAR-ready parent structure, so salts, hydrates and stereoisomers "
                "of one compound share the bit vector (12 of the repeated vectors are hash collisions of different "
                "chemicals instead). One row per vector is kept, and vectors with both classes are dropped, which "
                f"leaves {len(df) + len(PARENT_KEPT_TWICE):,} chemicals before the nine rows of the next decision.",
                duplicates,
            ),
            Decision(
                "Nine parents that survive twice reduced to one row",
                "Linking the rows to the project's structure file by order shows nine parent structures in two kept "
                "rows each (a free acid and its salt or tautomer under two CASRNs, all not very toxic), whose bits "
                f"differ. We keep the first row of each pair, so {len(df):,} chemicals remain.",
                pairs,
            ),
            Decision(
                "The file's order is the authors' split; we use cross-validation",
                "The first 6,744 rows are the authors' stratified random training set and the last 2,248 their test "
                "set (Ballabio et al. 2019, Table 1: 556 and 185 very toxic). Both were drawn at random, so the "
                "recommended IID cross-validation replaces them.",
                file_order,
            ),
        ]
