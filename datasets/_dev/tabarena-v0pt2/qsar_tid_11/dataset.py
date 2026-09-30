"""Curated dataset definition for `qsar_tid_11` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class QsarTid11(AbstractCuratedDataset):
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
        - We drop the "MOLECULE_CHEMBL_ID" column.
        - We shuffle the data as it has an original distribution shift.
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
