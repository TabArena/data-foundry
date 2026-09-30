"""Curated dataset definition for `hazelnut_spread_contaminant_detection` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class HazelnutSpreadContaminantDetection(AbstractCuratedDataset):
    # Dataset
    unique_name = "hazelnut_spread_contaminant_detection"
    year = "2020"
    domain = "biology & life sciences"
    source = "OpenML"
    source_url = "https://www.openml.org/d/45538"
    license = "CC BY-SA"
    download_description = """
        mkdir -p local-data-warehouse/hazelnut_spread_contaminant_detection/ && wget https://api.openml.org/data/download/22116506/dataset -O ./local-data-warehouse/hazelnut_spread_contaminant_detection/hazelnut.arff
    """
    bibtex = r"""
        @article{ricci2021machine,
          title={Machine-learning-based microwave sensing: A case study for the food industry},
          author={Ricci, Marco and {\v{S}}titi{\'c}, Bernardita and Urbinati, Luca and Di Guglielmo, Giuseppe and Vasquez, Jorge A Tob{\'o}n and Carloni, Luca P and Vipiana, Francesca and Casu, Mario R},
          journal={IEEE Journal on Emerging and Selected Topics in Circuits and Systems},
          volume={11},
          number={3},
          pages={503--514},
          year={2021},
          publisher={IEEE}
        }
    """
    curation_comments = """
        - We select a features from a single frequency (10 GHz) as the authors also only considered this frequency for the final experiments.
        - Anomaly: we use the publicly available dataset state, which is without preprocessing. Moreover, we were not able to inverse the original ordinal encoding of the label.
    """

    # Task
    target = "Contaminated"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(f"{raw_dir}/hazelnut.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "Contaminated"
        df = df.rename(columns={"class": target_feature})
        df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"}).astype("category")
        return df
