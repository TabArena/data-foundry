"""Curated dataset definition for `indian_liver_patient_dataset` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class IndianLiverPatientDataset(AbstractCuratedDataset):
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
