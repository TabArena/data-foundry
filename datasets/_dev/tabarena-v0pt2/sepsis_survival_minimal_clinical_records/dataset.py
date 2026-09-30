"""Curated dataset definition for `sepsis_survival_minimal_clinical_records` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class SepsisSurvivalMinimalClinicalRecords(AbstractCuratedDataset):
    # Dataset
    unique_name = "sepsis_survival_minimal_clinical_records"
    year = "2020"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C53C8N"
    license = "CC BY 4.0"
    download_description = """
        We download the data from UCI.

        wget https://archive.ics.uci.edu/static/public/827/sepsis+survival+minimal+clinical+records.zip && unzip sepsis+survival+minimal+clinical+records.zip && unzip s41598-020-73558-3_sepsis_survival_dataset.zip -d data_files &&  rm sepsis+survival+minimal+clinical+records.zip && rm s41598-020-73558-3_sepsis_survival_dataset.zip
        mkdir -p local-data-warehouse/sepsis_survival_minimal_clinical_records && mv data_files local-data-warehouse/sepsis_survival_minimal_clinical_records/
    """
    bibtex = """
        @article{chicco2020survival,
          title={Survival prediction of patients with sepsis from age, sex, and septic episode number alone},
          author={Chicco, Davide and Jurman, Giuseppe},
          journal={Scientific reports},
          volume={10},
          number={1},
          pages={17156},
          year={2020},
          publisher={Nature Publishing Group UK London}
        }
    """
    curation_comments = """
        We use only the primary cohort from Norway and ignore the subset and the small data (137 samples) from the South Korea cohort.

        - The data has only 3 features. Moreover, any other information (such as timestamps from the collection) are not provided. But this should not limit the applicability of the data, as there should be no temporal leakage.
        - We reverse the ordinal encoding of gender and the target variable.
        - The data has a lot of naturally occurring duplicates. We keep them in as they make sense they would exist and leave it to the pipeline or methods to handle.
        - The alternative subset (the study cohort in the original paper) contains only patients that had a sepsis according to the official Sepsis-3 definition. The paper discusses this in more detail and opts for using/testing all cohorts. We could introduce several datasets from this source but this would bias the benchmark too much towards this specific data distribution. We stick to using all data from the primary cohort.
    """

    # Task
    target = "sepsis_outcome_after9pt5_days_in_hospital"  # we rename the target column during preprocessing
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "data_files" / "s41598-020-73558-3_sepsis_survival_primary_cohort.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Reverse the ordinal encoding
        df["gender"] = df["sex_0male_1female"].replace({0: "Male", 1: "Female"}).astype("category")
        df["sepsis_outcome_after9pt5_days_in_hospital"] = (
            df["hospital_outcome_1alive_0dead"].replace({0: "Dead", 1: "Alive"}).astype("category")
        )
        df = df.drop(columns=["sex_0male_1female", "hospital_outcome_1alive_0dead"])
        return df
