"""Curated dataset definition for `qsar_tid_11` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary

# Salt forms of a compound that is also in the data (LEAK-19). The raw file has no structures, so the ids come from
# ChEMBL's molecule_hierarchy (API, 2026-10-21) for the rows in repeated fingerprint vectors: 37 groups of two
# ChEMBL ids with one parent_chembl_id, the same fingerprint and nearly the same target. We keep the parent's own
# row (the lowest ChEMBL id in the one group without it) and drop the other.
SALT_FORM_COPIES = frozenset(
    {
        "CHEMBL79422",
        "CHEMBL84575",
        "CHEMBL93210",
        "CHEMBL152854",
        "CHEMBL153611",
        "CHEMBL160489",
        "CHEMBL216318",
        "CHEMBL307446",
        "CHEMBL318112",
        "CHEMBL323543",
        "CHEMBL327331",
        "CHEMBL328069",
        "CHEMBL328298",
        "CHEMBL328582",
        "CHEMBL330496",
        "CHEMBL534707",
        "CHEMBL535862",
        "CHEMBL536721",
        "CHEMBL539053",
        "CHEMBL540119",
        "CHEMBL540121",
        "CHEMBL543817",
        "CHEMBL553840",
        "CHEMBL556575",
        "CHEMBL557579",
        "CHEMBL558198",
        "CHEMBL559015",
        "CHEMBL599035",
        "CHEMBL603888",
        "CHEMBL607008",
        "CHEMBL1159688",
        "CHEMBL1159692",
        "CHEMBL1160045",
        "CHEMBL1215083",
        "CHEMBL1215085",
        "CHEMBL1215086",
        "CHEMBL2337676",
    }
)


class QsarTid11(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How potent will a molecule be against one drug target?",
        use_case=(
            "In drug discovery, a medicinal chemist screens candidate molecules for activity on one protein target "
            "before making and testing them (the Meta-QSAR project builds one such model per target)."
        ),
        row=(
            "One compound measured against human thrombin (ChEMBL target 11, CHEMBL204; ChEMBL version 17, Meta-QSAR "
            "project 2015; 5,704 compounds after the salt-form copies leave)."
        ),
        predicted=(
            "The compound's median measured potency, as the negative log of the concentration that gives half the "
            "effect; higher means more potent."
        ),
        known=("A 1,024-bit fingerprint of the molecule's structure (which circular substructures it contains)."),
        split=(
            "Random compounds, so close relatives of a test compound can be in training. The file is roughly in "
            "ChEMBL ID order, with the mean activity drifting along it; the shuffle removes this order."
        ),
        changes=(
            "We drop one row with a negative activity value, judged a data error, and 37 rows that are salt forms "
            "of a compound already in the data."
        ),
        fit="direct",
        fit_reason=(
            "The fingerprint comes from the structure alone, which is all a chemist has before synthesis, and "
            "held-out compounds stand for unmeasured ones. The activities are medians over measurements of many "
            "sources."
        ),
    )

    # Dataset
    unique_name = "qsar_tid_11"
    year = "2015"
    domain = "chemistry & material science"
    source = "OpenML"
    source_url = "https://www.openml.org/d/3050"
    license = "Public Domain"
    download_description = """
        We download the dataset from OpenML to a predefined folder.

        mkdir -p local-data-warehouse/qsar_tid_11/ && wget -P local-data-warehouse/qsar_tid_11/ https://www.openml.org/data/download/1674848/11.arff
    """
    bibtex = """
        @article{olier2018meta,
          title={Meta-QSAR: a large-scale application of meta-learning to drug design and discovery},
          author={Olier, Ivan and Sadawi, Noureddin and Bickerton, G Richard and Vanschoren, Joaquin and Grosan, Crina and Soldatova, Larisa and King, Ross D},
          journal={Machine Learning},
          volume={107},
          pages={285--311},
          year={2018},
          publisher={Springer}
        }
    """
    curation_comments = """
        - The target is ChEMBL target 11, human prothrombin (thrombin, CHEMBL204), named by OpenML's original data URL.
        - OpenML (uploaded 2015-10-06, creators the Meta-QSAR team) is the first publication; the Mendeley Data release
          (doi:10.17632/spwgrcnjdg.1) came in 2020 and computes the fingerprints with RDKit instead of Pipeline Pilot.
        - We drop the "MOLECULE_CHEMBL_ID" column.
        - The file lists the compounds roughly in ChEMBL ID order, and the mean activity drifts along it (6.8 in the
          first tenth, 5.6 in the ninth); the standard shuffle removes this order.
        - Only one row has a negative value (-6.24) and is thus extremely out-of-distribution, which is likely results from the target being log scaled in the original domain. We remove this row as it is unclear if this is a scaling or labeling error, but we judge it is in all cases a data artifact.
        - Why the row may leave (CLEAN-11, CLEAN-15): a pXC50 of -6.24 is a half-effect concentration of 10^6.24 mol/L, about 1.7 million mol/L, which no substance reaches (pure water is 55 mol/L). The value is impossible, so the target is missing and the row drops. It does not meet CLEAN-11's clause for an extreme target in the training period only: the split is random, and the source does not name the row.
        - We do not log scale the target (it could make sense for this distribution), as the original label is already log transformed.
        - Repeated fingerprints (LEAK-16 asks for a recorded decision; Lennart, 2026-10-21): 870 of 5,741 rows sit in
          387 repeated FCFP vectors (116 with the same target too), and every row has its own ChEMBL compound id. We
          traced 798 of the 870 rows in ChEMBL (the other 72 ids are no longer in ChEMBL). Most repeats are different
          compounds the fingerprint cannot tell apart: stereoisomers (179 vectors) and analogs such as F against Cl
          (125 vectors), with their own measured potency. These stay. Untuned LightGBM RMSE (5-fold, 2 seeds): random
          split 0.765, grouped on the vector 0.781, one row per vector 0.757; predicting a repeated row by its
          vector-mates' mean gives 0.798, worse than the model. Grouping on a bare fingerprint hash is barred
          (SPLIT-24) and would test whether the fingerprint resolves stereoisomers.
        - We drop 37 rows that are salt forms of a compound also in the data (LEAK-19, as in qsar_oral_toxicity): two
          ChEMBL ids with one ChEMBL parent (molecule_hierarchy), the same fingerprint and nearly the same target
          (median sd 0.04 within a pair; 0.006 in the 31 pairs that make up a whole vector). The rule does not read
          the target: we keep the parent's own row (in the one pair without it, the lowest ChEMBL id). The ids are
          embedded as SALT_FORM_COPIES, since the raw file has no structures.
        - The 1,024 fingerprint bits are 0/1 presence flags (OpenML stores them as floats): integers typed categorical, the house form for 0/1 presence flags (CLEAN-14; Lennart, 2026-10-21).
    """

    # Task
    target = "MEDIAN_PXC50"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(raw_dir / "11.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Salt-form copies of a compound in the data leave (LEAK-19); the parent's row stays.
        df = df[~df["MOLECULE_CHEMBL_ID"].isin(SALT_FORM_COPIES)]
        df = df.drop(columns=["MOLECULE_CHEMBL_ID"])
        # Remove one negative outlier row
        df = df[df["MEDIAN_PXC50"] >= 0].reset_index(drop=True)
        bits = df.columns.drop("MEDIAN_PXC50")
        df[bits] = df[bits].astype("int8")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The fingerprint bits are 0/1 presence flags: categorical (CLEAN-14).
        return FeatureTypes(categorical=list(df.columns.drop(self.target)))
