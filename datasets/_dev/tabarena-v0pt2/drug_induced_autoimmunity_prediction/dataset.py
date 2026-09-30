"""Curated dataset definition for `drug_induced_autoimmunity_prediction` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class DrugInducedAutoimmunityPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "drug_induced_autoimmunity_prediction"
    year = "2025"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5332M"
    license = "CC BY 4.0"
    download_description = """
        wget https://archive.ics.uci.edu/static/public/1104/drug_induced_autoimmunity_prediction.zip && unzip drug_induced_autoimmunity_prediction.zip && rm drug_induced_autoimmunity_prediction.zip RDKit_ChemDes.xlsx && mkdir -p local-data-warehouse/drug_induced_autoimmunity_prediction && mv DIA_trainingset_RDKit_descriptors.csv local-data-warehouse/drug_induced_autoimmunity_prediction/ && mv DIA_testset_RDKit_descriptors.csv local-data-warehouse/drug_induced_autoimmunity_prediction/
    """
    bibtex = """
        @article{huang2025interdia,
          title={InterDIA: Interpretable prediction of drug-induced autoimmunity through ensemble machine learning approaches},
          author={Huang, Lina and Liu, Peineng and Huang, Xiaojie},
          journal={Toxicology},
          volume={511},
          pages={154064},
          year={2025},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        We start with the dataset from UCI.

        - We drop the constant columns.
        - We keep the SMILES code as string for later pipelines to handle.
    """

    # Task
    target = "Label"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "DIA_trainingset_RDKit_descriptors.csv")
        df = pd.concat([df, pd.read_csv(raw_dir / "DIA_testset_RDKit_descriptors.csv")], ignore_index=True)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Drop constant columns
        constant_cols = df.columns[df.nunique(dropna=False) == 1]
        df = df.drop(columns=constant_cols)
        # dropping duplicated columns (by chance)
        duplicated = ["fr_Nhpyrrole", "MaxEStateIndex", "fr_benzene"]
        df = df.drop(columns=duplicated)
        as_string_type = ["SMILES"]
        for c in as_string_type:
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        return df
