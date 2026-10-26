"""Curated dataset definition for `concrete_compressive_strength` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, TaskSummary


class ConcreteCompressiveStrength(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How strong will a new concrete mix be after a given number of days?",
        use_case=(
            "A civil engineer designing a high-performance concrete mix estimates its compressive strength at a given "
            "age before casting and testing specimens; the data's author used such models to design mixes (Yeh 1999)."
        ),
        row=(
            "One laboratory test of one concrete mix at one age (1,030 tests of 428 mixes, published by I-Cheng Yeh in"
            " 1998); 182 mixes are tested at several ages, up to 20 times."
        ),
        predicted="The compressive strength, in megapascals (2 to 83 in the data).",
        known=(
            "The amount of each of seven ingredients per cubic metre (cement, blast-furnace slag, fly ash, water, "
            "superplasticizer, coarse and fine aggregate) and the age at the test, 1 to 365 days."
        ),
        split=(
            "Whole mixes are held out, so the test data stands for mixes never tested, at every age; mixes that share "
            "some ingredient amounts can be on both sides."
        ),
        changes=(
            "We added the mix as a group column and split by it; with random tests, 73% of the test rows had their "
            "mix in training at another age."
        ),
        fit="direct",
        fit_reason=(
            "The inputs are what an engineer chooses, and a held-out mix is a design not yet tested. The task is "
            "narrow (one laboratory's family of high-performance mixes) but real."
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
        - The 1,030 tests are 428 mixes: a mix is its amounts of the seven ingredients, and 182 mixes are tested at several ages (up to 20 tests). We add the mix as the group column `mix`, built from identical values in all seven ingredient columns; it is no feature.
        - Grouped by mix since 2026-10-14 (IID before, the split shipped in TabArena v0.1 and BeyondArena): a model is used for a mix that was not tested, while a random split gave 73% of the test rows their mix in training at another age. Mixes carry 65% of the target variance. R^2, random against grouped by mix: LightGBM 0.925 / 0.874, extra trees 0.912 / 0.881, random forest 0.901 / 0.856, MLP 0.916 / 0.838, kNN 0.882 / 0.826, ridge 0.816 / 0.804; the ranking of the models changes.
        - Note: 34 rows repeat the features of another row, a mix tested again at the same age (25 with the same strength, 9 with another); they stay, and the grouped split keeps them in the fold of their mix.
    """

    # Task
    target = "ConcreteCompressiveStrength"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "Yeh 1998 (closed access) is cited for R^2 of predicted vs measured strength (about 0.91-0.92"
            " for the ANN) by secondary sources; not read, and R^2 ranks models as RMSE does within a "
            "fold. rmse is the regression fallback."
        ),
    )
    grouping = Grouping(
        on="mix",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a concrete mix: one set of amounts of the seven ingredients (kg per m3 of cement, blast-furnace slag, fly ash, water, superplasticizer, coarse and fine aggregate), identical in all seven columns; its rows are the laboratory tests of that mix, each at one age (1 to 20 tests, 428 mixes). The UCI page describes a row as the strength "for a given mixture under a specific age", and the data's author used such models to design new mixtures (Yeh 1999, "Design of High Performance Concrete Mixture Using Neural Networks"). A new prediction is for a mix not tested before, so the test mixes are new to the model. Each row is one prediction, made from the mix and the age.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the mix: all tests of one mix stay on one side, so a model predicts the strength of a mix it has not seen, at any age. Mixes that share some ingredient amounts can be on both sides.
    """

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
        # a mix is its amounts of the seven ingredients; its tests at other ages are rows with the same amounts
        ingredients = df.columns[:7].tolist()
        df["mix"] = df.groupby(ingredients, sort=False).ngroup().map("mix_{:03d}".format)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=("mix",))
