"""Curated dataset definition for `indian_liver_patient_dataset` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class IndianLiverPatientDataset(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a patient have liver disease, judging from age, sex and routine blood tests?",
        use_case=(
            "For example, a doctor reads a patient's liver blood tests to decide whether to refer the patient for a "
            "liver work-up."
        ),
        row=(
            "One patient record from the north-east of Andhra Pradesh, India (416 liver patients and 167 others); the"
            " period is not stated."
        ),
        predicted=("Whether the record is of a liver patient (71%); how the diagnosis was made is not stated."),
        known=(
            "Age, sex, total and direct bilirubin, alkaline phosphatase, two liver enzymes (ALT and AST), total "
            "protein, albumin and the albumin-to-globulin ratio."
        ),
        split="Random patients, so the test data stands for new patients from the same collection.",
        fit="approximate",
        fit_reason=(
            "Liver patients and others were collected as two groups (71% patients), not as the patients a doctor "
            "sees, and the basis of the diagnosis is not stated."
        ),
    )

    # Dataset
    unique_name = "indian_liver_patient_dataset"
    year = "2012"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5D02C"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/225/ilpd+indian+liver+patient+dataset.zip && unzip ilpd+indian+liver+patient+dataset.zip && rm ilpd+indian+liver+patient+dataset.zip
        mkdir -p local-data-warehouse/indian_liver_patient_dataset && mv "Indian Liver Patient Dataset (ILPD).csv" local-data-warehouse/indian_liver_patient_dataset/
    """
    bibtex = """
        @article{ramana2012critical,
          title={A critical comparative study of liver patients from USA and INDIA: an exploratory analysis},
          author={Ramana, Bendi Venkata and Babu, M Surendra Prasad and Venkateswarlu, NB},
          journal={International Journal of Computer Science Issues (IJCSI)},
          volume={9},
          number={3},
          pages={506},
          year={2012},
          publisher={International Journal of Computer Science Issues (IJCSI)}
        }
    """
    curation_comments = """
        We keep the data as is as it does not require any further cleaning.
        Note, the data contains a few (n=13) duplicates, that are likely naturally occurring duplicates given the features.
    """

    # Task
    target = "Selector"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(
            raw_dir / "Indian Liver Patient Dataset (ILPD).csv",
            header=None,
            names=["Age", "Gender", "TB", "DB", "Alkphos", "Sgpt", "Sgot", "TP", "ALB", "A/G", "Selector"],
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Gender",
            ],
        )
