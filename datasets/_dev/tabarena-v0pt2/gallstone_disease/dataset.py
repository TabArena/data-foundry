"""Curated dataset definition for `gallstone_disease` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class GallstoneDisease(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does an outpatient have gallstone disease?",
        use_case=(
            "An internal-medicine clinic screens outpatients for gallstone disease from a body-composition scan and "
            "routine blood tests, for example to decide who goes on to imaging (the source paper's aim is early "
            "prediction)."
        ),
        row=(
            "One person seen at the Internal Medicine Outpatient Clinic of Ankara VM Medical Park Hospital, Turkey, "
            "June 2022 to June 2023 (319 people)."
        ),
        predicted=(
            "Whether the person was diagnosed with gallstone disease (161 of 319, about half); how it was diagnosed "
            "is not stated."
        ),
        known=(
            "Age, sex, other illnesses (coronary disease, hypothyroidism, high blood lipids, diabetes), height and "
            "weight, body composition from bioimpedance (water, fat, muscle, bone, visceral and liver fat), and blood"
            " tests (sugar, lipids, liver and kidney values, inflammation, haemoglobin, vitamin D)."
        ),
        split="Random people, so the test data stands for new patients of the same clinic and year.",
        fit="direct",
        fit_reason=(
            "The values are measured at the visit where the diagnosis is made, as in screening. The base is narrow "
            "(one clinic, one year, half with gallstones), and how the people were chosen is not stated, so another "
            "clinic's mix may differ."
        ),
    )

    # Dataset
    unique_name = "gallstone_disease"
    year = "2025"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://archive.ics.uci.edu/dataset/1150/gallstone-1"  # the paper says its data are not public
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/1150/gallstone-1.zip && unzip gallstone-1.zip && rm gallstone-1.zip && unzip dataset-uci.zip && rm dataset-uci.zip && mkdir -p local-data-warehouse/gallstone_disease && mv dataset-uci.xlsx local-data-warehouse/gallstone_disease/
    """
    bibtex = r"""
        @article{esen2024early,
          title={Early prediction of gallstone disease with a machine learning-based method from bioimpedance and laboratory data},
          author={Esen, {\.I}rfan and Arslan, Hilal and Esen, Selin Akt{\"u}rk and G{\"u}l{\c{s}}en, Mervenur and K{\"u}ltekin, Nimet and {\"O}zdemir, O{\u{g}}uzhan},
          journal={Medicine},
          volume={103},
          number={8},
          pages={e37258},
          year={2024},
          publisher={LWW}
        }
    """
    curation_comments = """
        We use the data without any further curation.
    """

    # Task
    target = "Gallstone Status"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "dataset-uci.xlsx", sheet_name="dataset", engine="calamine")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Coronary Artery Disease (CAD)",
                "Hypothyroidism",
                "Gender",
                "Comorbidity",
                "Hyperlipidemia",
                "Diabetes Mellitus (DM)",
            ],
        )
