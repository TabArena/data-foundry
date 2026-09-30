"""Curated dataset definition for `pancreatic_cancer_mouse_detection` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


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
        - We label the samples based on name of the folder they are located in: "PanINCTL" translates to healthy animals cases while "03-PanIN" to individuals with a pancreatic cancer.
        - Anomaly: The data from the website has one more mouse than accounted for in the paper (73 vs (33 + 39))) but the same number of serums (181).
    """

    # Task
    target = "HasCancer"
    problem_type = "binary_classification"
    group_on = "mouse_id"
    group_labels = "per_group"

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
                row["HasCancer"] = label
                rows.append(row)
        df = pd.DataFrame(rows)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "mouse_id",
            ],
        )
