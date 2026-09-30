"""Curated dataset definition for `eryhemato_squamous_disease` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class EryhematoSquamousDisease(AbstractCuratedDataset):
    # Dataset
    unique_name = "eryhemato_squamous_disease"
    year = "1997"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5FK5P"
    license = "CC BY 4.0"
    download_description = """
        We take the original data from UCI.

        wget https://archive.ics.uci.edu/static/public/33/dermatology.zip && unzip dermatology.zip && rm dermatology.zip dermatology.names
        mkdir -p local-data-warehouse/eryhemato_squamous_disease && mv dermatology.data local-data-warehouse/eryhemato_squamous_disease/
    """
    bibtex = r"""
        @article{guvenir1998learning,
          title={Learning differential diagnosis of erythemato-squamous diseases using voting feature intervals},
          author={G{\"u}venir, H Altay and Demir{\"o}z, G{\"u}l{\c{s}}en and Ilter, Nilsel},
          journal={Artificial intelligence in medicine},
          volume={13},
          number={3},
          pages={147--165},
          year={1998},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - We encode all features but age as categorical, since they are ordinal features in nature.
        - We ensure missing values in age are encoded as NaN.
    """

    # Task
    target = "class"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        feature_names = [
            "erythema",
            "scaling",
            "definite borders",
            "itching",
            "koebner phenomenon",
            "polygonal papules",
            "follicular papules",
            "oral mucosal involvement",
            "knee and elbow involvement",
            "scalp involvement",
            "family history",
            "melanin incontinence",
            "eosinophils in the infiltrate",
            "PNL infiltrate",
            "fibrosis of the papillary dermis",
            "exocytosis",
            "acanthosis",
            "hyperkeratosis",
            "parakeratosis",
            "clubbing of the rete ridges",
            "elongation of the rete ridges",
            "thinning of the suprapapillary epidermis",
            "spongiform pustule",
            "munro microabcess",
            "focal hypergranulosis",
            "disappearance of the granular layer",
            "vacuolisation and damage of basal layer",
            "spongiosis",
            "saw-tooth appearance of retes",
            "follicular horn plug",
            "perifollicular parakeratosis",
            "inflammatory monoluclear inflitrate",
            "band-like infiltrate",
            "age",
            "class",
        ]
        df = pd.read_csv(raw_dir / "dermatology.data", header=None, names=feature_names)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        as_cat_col = list(df.columns)
        as_cat_col.remove("age")  # age is numeric, and has some missing values, so
        df[as_cat_col] = df[as_cat_col].astype("category")
        df["age"] = df["age"].replace("?", np.nan).astype(float)
        return df
