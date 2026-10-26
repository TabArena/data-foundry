"""Curated dataset definition for `musk` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, TaskSummary, anonymize_ids


class Musk(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a new molecule smell of musk, judging from the shapes it can take?",
        use_case=(
            "A fragrance chemist screens candidate molecules and decides which to make and test, from shape features "
            "computed for each molecule's low-energy conformations (Dietterich et al.)."
        ),
        row=(
            "One low-energy conformation (3D shape) of one of 102 molecules, with 1 to 1,044 conformations per "
            "molecule (6,598 rows)."
        ),
        predicted=(
            "Whether the molecule is a musk, as judged by human experts (39 musks, 63 not); a molecule counts as a "
            "musk if any of its conformations is scored as one, and scores are per molecule."
        ),
        known=(
            "166 numbers describing the conformation's shape: distances from its centre to its surface along fixed "
            "rays, and the position of an oxygen atom. All conformations of the molecule can be used."
        ),
        split=(
            "Whole molecules are held out (20 repeats of 3 folds), so the test data stands for molecules never tested."
        ),
        changes=(
            "We rename the molecules, whose names gave the label away, drop the conformation names, and score per "
            "molecule instead of per conformation."
        ),
        fit="direct",
        fit_reason=(
            "The shapes can be computed from a molecule's structure before it is made, and a held-out molecule is a "
            "new candidate. The task is tiny: 102 molecules, 34 per test fold."
        ),
    )

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
    metric = Metric.fallback(
        reason=(
            "Dietterich et al. 1997 report per-molecule accuracy (10-fold CV), as all multiple-instance work does: a "
            "habit without costs; 34 molecules per test fold, so accuracy moves in steps of about 3% (MET-10). "
            "Original rejected: accuracy. roc_auc is the binary fallback, per molecule (aggregation any)."
        )
    )
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
        We create stratified grouped 20-repeated 3-fold split. Each test set holds 34 molecules, 675 to 5,046 conformations, as the molecules have 1 to 1,044 conformations each.
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
