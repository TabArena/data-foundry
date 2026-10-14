"""Curated dataset definition for `qsar_tid_11` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


class QsarTid11(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How potent will a molecule be against one drug target?",
        use_case=(
            "In drug discovery, a medicinal chemist screens candidate molecules for activity on one protein target "
            "before making and testing them (the Meta-QSAR project builds one such model per target)."
        ),
        row=(
            "One compound measured against human thrombin (ChEMBL target 11, CHEMBL204; ChEMBL version 17, Meta-QSAR "
            "project 2015; 5,741 compounds)."
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
        changes="We drop one row with a negative activity value, judged a data error.",
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
        - We do not log scale the target (it could make sense for this distribution), as the original label is already log transformed.
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
        df.drop(columns=["MOLECULE_CHEMBL_ID"], inplace=True)
        # Remove one negative outlier row
        df = df[df["MEDIAN_PXC50"] >= 0].reset_index(drop=True)
        return df
