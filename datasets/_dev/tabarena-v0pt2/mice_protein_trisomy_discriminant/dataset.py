"""Curated dataset definition for `mice_protein_trisomy_discriminant` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class MiceProteinTrisomyDiscriminant(AbstractCuratedDataset):
    # Dataset
    unique_name = "mice_protein_trisomy_discriminant"
    year = "2015"
    domain = "biology & life sciences"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C50S3Z"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/342/mice+protein+expression.zip && unzip mice+protein+expression.zip && rm -rf mice+protein+expression.zip
        mkdir -p local-data-warehouse/mice_protein_trisomy_discriminant && mv Data_Cortex_Nuclear.xls local-data-warehouse/mice_protein_trisomy_discriminant/
    """
    bibtex = """
        @article{higuera2015self,
          title={Self-organizing feature maps identify proteins critical to learning in a mouse model of down syndrome},
          author={Higuera, Clara and Gardiner, Katheleen J and Cios, Krzysztof J},
          journal={PloS one},
          volume={10},
          number={6},
          pages={e0129126},
          year={2015},
          publisher={Public Library of Science San Francisco, CA USA}
        }
    """
    curation_comments = """
        We start with the dataset from UCI.

        - We drop the three feature that make up the target to remove the leakage.
        - We reduce the mouse ID to represent the ID of the mouse instead of the experiment for the mouse.
        - We drop the duplicated feature pS6_N.
    """

    # Task
    target = "class"
    problem_type = "multiclass_classification"
    group_on = "MouseID"
    group_labels = "per_group"

    # Splits
    splits_comment = """
        We create stratified grouped 20-repeated 3-fold split. This creates 24 group members (360 samples) per test set.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "Data_Cortex_Nuclear.xls")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Fix the ID so it reduces to the same mouse
        df["MouseID"] = df["MouseID"].str.split("_").str[0]
        # Drop leaky features that are part of the target
        df = df.drop(columns=["Genotype", "Treatment", "Behavior"])
        # Drop duplicated column
        df = df.drop(columns=["pS6_N"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "MouseID",
            ],
        )


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
