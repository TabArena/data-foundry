"""Curated dataset definition for `concrete_compressive_strength` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


class ConcreteCompressiveStrength(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How strong will a concrete mix be after a given number of days?",
        use_case=(
            "For example, a civil engineer designing a high-performance concrete mix estimates its compressive "
            "strength at a given age before casting and testing specimens."
        ),
        row=(
            "One laboratory test of one concrete mix at one age (1,030 tests, published by I-Cheng Yeh in 1998); many"
            " mixes are tested at several ages."
        ),
        predicted="The compressive strength, in megapascals (2 to 83 in the data).",
        known=(
            "The amount of each of seven ingredients per cubic metre (cement, blast-furnace slag, fly ash, water, "
            "superplasticizer, coarse and fine aggregate) and the age at the test, 1 to 365 days."
        ),
        split=(
            "Random tests, so a test mix can be in training at another age; the test data stands for new mixes only "
            "in part."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs are what an engineer chooses, but the random split puts tests of the same mix at other ages "
            "in training, so the score mixes designing new mixes with filling in known ones; a split by mix would "
            "match the use case."
        ),
    )

    # Dataset
    unique_name = "concrete_compressive_strength"
    year = "2007"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5PK67"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/concrete_compressive_strength/ && wget -P local-data-warehouse/concrete_compressive_strength/ https://archive.ics.uci.edu/static/public/165/concrete+compressive+strength.zip && unzip local-data-warehouse/concrete_compressive_strength/concrete+compressive+strength.zip -d local-data-warehouse/concrete_compressive_strength/
    """
    bibtex = """
        @article{yeh1998modeling,
          title={Modeling of strength of high-performance concrete using artificial neural networks},
          author={Yeh, I-C},
          journal={Cement and Concrete research},
          volume={28},
          number={12},
          pages={1797--1808},
          year={1998},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - We rename features to be shorter while similar to the original names.
    """

    # Task
    target = "ConcreteCompressiveStrength"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(f"{raw_dir}/Concrete_Data.xls")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "ConcreteCompressiveStrength"
        df.columns = [
            "Cement",
            "BlastFurnaceSlag",
            "FlyAsh",
            "Water",
            "Superplasticizer",
            "CoarseAggregate",
            "FineAggregate",
            "Age",
            target_feature,
        ]
        return df
