"""Curated dataset definition for `south_africa_coronary_heart_disease` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class SouthAfricaCoronaryHeartDisease(AbstractCuratedDataset):
    # Dataset
    unique_name = "south_africa_coronary_heart_disease"
    year = "1983"
    domain = "medical & healthcare"
    source = "Kaggle"  # Originally from http://statweb.stanford.edu/~tibs/ElemStatLearn/data.html
    source_url = "https://www.kaggle.com/datasets/waalbannyantudre/south-african-heart-disease-dataset"
    license = "CC BY-SA 4.0"
    download_description = """
        We get the data from Kaggle, as it has the best curation and documentation.

        kaggle datasets download waalbannyantudre/south-african-heart-disease-dataset && unzip south-african-heart-disease-dataset.zip && rm south-african-heart-disease-dataset.zip
        mkdir -p local-data-warehouse/south_africa_coronary_heart_disease && mv SAHeart.csv local-data-warehouse/south_africa_coronary_heart_disease/
    """
    bibtex = r"""
        @article{rossouw1983coronary,
          title={Coronary risk factor screening in three rural communities. The CORIS baseline study.},
          author={Rossouw, JE and Du Plessis, JP and Benad{\'e}, AJ and Jordaan, PC and Kotze, JP and Jooste, PL and Ferreira, JJ},
          journal={South African medical journal= Suid-Afrikaanse tydskrif vir geneeskunde},
          volume={64},
          number={12},
          pages={430--436},
          year={1983}
        }
    """
    curation_comments = """
        We start with the data from Kaggle.

        - We remove the row id column.
        - The data is a retrospective sample of males from the CORIS study (cases with coronary heart disease and controls). Hastie, Tibshirani & Friedman (The Elements of Statistical Learning, 2nd ed., Sec. 5.2.2, p. 148) note: "These measurements were made sometime after the patients suffered a heart attack, and in many cases they had already benefited from a healthier diet and lifestyle". Some risk factors of the cases (e.g. sbp, obesity) were therefore measured after the outcome. This weakens their signal rather than leaking the target (dropping sbp and obesity changes ROC AUC from 0.774 to 0.778), so we keep all features.
    """

    # Task
    target = "chd"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "SAHeart.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["row.names"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "famhist",
            ],
        )
