"""Curated dataset definition for `pancreatic_cancer_mouse_detection` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping


class PancreaticCancerMouseDetection(AbstractCuratedDataset):
    # Dataset
    unique_name = "pancreatic_cancer_mouse_detection"
    year = "2003"
    domain = "medical & healthcare"
    source = "Other"
    source_url = "https://home.ccr.cancer.gov/ncifdaproteomics/ppatterns.asp"
    license = "None"  # Not given, likely public
    download_description = r"""
        We download the data to a predefined folder.

        mkdir -p local-data-warehouse/pancreatic_cancer_mouse_detection && \
        wget -P local-data-warehouse/pancreatic_cancer_mouse_detection https://home.ccr.cancer.gov/ncifdaproteomics/CancerCellPanINDataBinned.zip && \
        unzip local-data-warehouse/pancreatic_cancer_mouse_detection/CancerCellPanINDataBinned.zip -d local-data-warehouse/pancreatic_cancer_mouse_detection/ && \
        rm local-data-warehouse/pancreatic_cancer_mouse_detection/CancerCellPanINDataBinned.zip && \
        mv local-data-warehouse/pancreatic_cancer_mouse_detection/CancerCellPanINDataBinned/02-Control/PanINCTL local-data-warehouse/pancreatic_cancer_mouse_detection/ && \
        mv local-data-warehouse/pancreatic_cancer_mouse_detection/CancerCellPanINDataBinned/03-PanIN local-data-warehouse/pancreatic_cancer_mouse_detection && \
        rm -r local-data-warehouse/pancreatic_cancer_mouse_detection/CancerCellPanINDataBinned
    """
    bibtex = """
        "@article{hingorani2003preinvasive,
          title={Preinvasive and invasive ductal pancreatic cancer and its early detection in the mouse},
          author={Hingorani, Sunil R and Petricoin, Emanuel F and Maitra, Anirban and Rajapakse, Vinodh and King, Catrina and Jacobetz, Michael A and Ross, Sally and Conrads, Thomas P and Veenstra, Timothy D and Hitt, Ben A and others},
          journal={Cancer cell},
          volume={4},
          number={6},
          pages={437--450},
          year={2003},
          publisher={Elsevier}
        }"
    """
    curation_comments = """
        The task in the original data is grouped as multiple serums per mouse were taken.
        - We merge all samples located in the .csv files into one DataFrame and recover target labels, group IDs, and feature names.
        - We label the samples based on name of the folder they are located in: "PanINCTL" are the littermate control mice, "03-PanIN" the compound-mutant mice with pancreatic intraepithelial neoplasia (PanIN), preinvasive lesions with "no evidence of invasive or metastatic disease" (Hingorani et al. 2003). The target is therefore `HasPanIN`, not cancer.
        - Anomaly: the download holds 181 serum spectra (80 PanIN, 101 control) from 73 mouse IDs (35 PanIN, 38 control); the paper reports 191 spectra after quality control (80 PanIN, 111 control) from 72 mice (33 compound mutants, 39 littermate controls). The 10 missing spectra are controls, and no mouse ID occurs in both classes; the difference cannot be resolved without the authors.
        - The file names encode the class: the third token is `02` for every control file and `03` for every PanIN file, some with a `t` suffix of unknown meaning (42 of 101 control and 24 of 80 PanIN files; it is not the paper's training/blinded-test split). We take the label from the folder and the mouse ID from the second token; the class code never enters the features.
    """

    # Task
    target = "HasPanIN"
    problem_type = "binary_classification"
    grouping = Grouping(
        on="mouse_id",
        labels="per_group",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a mouse; its rows are serum samples from 1 to 6 bleeds, collected "as independent events" at least 5 days apart (Hingorani et al. 2003). The use case is a serum test for the preinvasive state, so each sample is one prediction, made from that sample alone. The paper split the samples at random, ignoring the mice; holding out whole mice simulates testing a new patient.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        BASE_DIR = raw_dir
        LABEL_MAP = {
            "PanINCTL": "No",
            "03-PanIN": "Yes",
        }
        rows = []
        for folder, label in LABEL_MAP.items():
            for filepath in sorted((BASE_DIR / folder).glob("*.csv")):
                sample = pd.read_csv(filepath)

                # Filename format: {id}_{group_id}_{rest}.txt_PQ.csv
                group_id = filepath.stem.split("_")[1]

                row = dict(zip("M/Z:" + sample["M/Z"].astype(str), sample["Intensity"]))
                row["mouse_id"] = group_id
                row["HasPanIN"] = label
                rows.append(row)
        df = pd.DataFrame(rows)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "mouse_id",
            ],
        )
