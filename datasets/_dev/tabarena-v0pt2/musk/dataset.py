"""Curated dataset definition for `musk` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, anonymize_ids


class Musk(AbstractCuratedDataset):
    # Dataset
    unique_name = "musk"
    year = "1994"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C51608"
    license = "CC BY 4.0"
    download_description = """
        wget https://archive.ics.uci.edu/static/public/75/musk+version+2.zip && unzip musk+version+2.zip clean2.data.Z && uncompress clean2.data.Z && rm musk+version+2.zip && mkdir -p local-data-warehouse/musk && mv clean2.data local-data-warehouse/musk/
    """
    bibtex = """
        @article{dietterich1993comparison,
          title={A comparison of dynamic reposing and tangent distance for drug activity prediction},
          author={Dietterich, Thomas and Jain, Ajay and Lathrop, Richard and Lozano-Perez, Tomas},
          journal={Advances in neural information processing systems},
          volume={6},
          year={1993}
        }
    """
    curation_comments = """
        - We rename the molecule IDs to remove the target leakage from the names.
        - We drop the conformation name as it leaks information that the real task should not have (the correlation between specific conformations across samples).
    """

    # Task
    target = "class"
    problem_type = "binary_classification"
    grouping = Grouping(
        on="molecule_name",
        labels="per_group",
        prediction_unit="group",
        aggregation="any",
        context="all_rows",
        definition="""
            One group is a molecule; its rows are its low-energy conformations (102 molecules, 1 to 1,044 conformations each). The use case is to decide whether a new molecule is a musk, and "the classifier should classify a molecule as 'musk' if ANY of its conformations is classified as a musk" (UCI `clean2.info`; Dietterich et al. 1997, who score molecules in a 10-fold cross-validation over the 102 molecules). All conformations of a new molecule can be computed from its structure, so a model may use all of its rows. The row labels are copies of the molecule's label: most conformations of a musk do not bind.
        """,
    )

    # Splits
    splits_comment = """
        We create stratified grouped 20-repeated 3-fold split. This creates ca. 30 group members (500-3000 samples) per test set.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(
            raw_dir / "clean2.data",
            header=None,
            names=[
                "molecule_name",
                "conformation_name",
                *[f"feature_{i}" for i in range(166)],
                "class",
            ],
        )
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["conformation_name"])
        df["class"] = df["class"].map({0: "non-musk", 1: "musk"})
        # stable anonymous ids (random uuid4 ids changed the data and the grouped splits on every run)
        df["molecule_name"] = anonymize_ids(df["molecule_name"])
        # cast before the sort below, which orders by category
        df["molecule_name"] = df["molecule_name"].astype("category")
        df = df.sample(frac=1, random_state=42).sort_values(by="molecule_name", kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["molecule_name"])


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
