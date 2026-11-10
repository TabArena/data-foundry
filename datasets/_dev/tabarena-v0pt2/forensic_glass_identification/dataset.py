"""Curated dataset definition for `forensic_glass_identification` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Metric, Source, TaskSummary, decode


class ForensicGlassIdentification(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What kind of glass does a fragment come from, judging from its chemical make-up?",
        use_case=(
            "A forensic scientist identifies the type of a glass fragment left at a crime scene, so that it can be "
            "used as evidence (the source's motivation)."
        ),
        row="One glass sample of the US Forensic Science Service, 1987 (214 samples).",
        predicted=(
            "The glass type, one of six: building windows, float-processed (33%) or not (36%), float-processed "
            "vehicle windows, containers, tableware or headlamps."
        ),
        known=(
            "The refractive index and the weight percent of the oxides of eight elements (sodium, magnesium, "
            "aluminium, silicon, potassium, calcium, barium, iron)."
        ),
        split="Random samples, so the test data stands for new fragments of the same types.",
        fit="direct",
        fit_reason=(
            "The features are measurements made on a fragment, and the label is what the investigator wants to know. "
            "The data is small and from 1987; two classes have 9 and 13 samples."
        ),
    )

    # Dataset
    unique_name = "forensic_glass_identification"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5WW2P",
            license="CC BY 4.0",
            year="1987",
            bibtex="""
                @misc{German1987glass,
                  author       = {German, B.},
                  title        = {{Glass Identification}},
                  year         = {1987},
                  howpublished = {UCI Machine Learning Repository},
                  note         = {{DOI}: https://doi.org/10.24432/C5WW2P}
                }
            """,
        ),
    )
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/42/glass+identification.zip && unzip glass+identification.zip && rm glass+identification.zip glass.names glass.tag Index
        mkdir -p local-data-warehouse/forensic_glass_identification && mv glass.data local-data-warehouse/forensic_glass_identification/
    """
    curation_comments = """
        We start with the data from UCI.

        - We drop the ID column, as it is a just a row identifier and does not contain any useful information for modeling.
        - The data contains one naturally occurring duplicate.
        - The target (2026-11-01, CLEAN-25): `Type_of_glass` ships its classes as words (glass.names, 11. Type of
          glass).
    """

    # Task
    accepted_check_warnings = {
        "dataset_row_order_leaks_target": "The row order is the definition's fixed shuffle, which depends on the rows' contents; decoding the target into the glass types' names (2026-11-01) reshuffled the 214 rows, and the category codes of this nominal target now correlate with position at rho -0.21, an outcome 0.4% of random shuffles reach. The source file is not sorted by type in this frame.",
    }

    target = "Type_of_glass"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The source defines no metric for the 6-class task; its only result (Spiehler's BEAGLE vs NN vs DA "
            "comparison) counts incorrect answers for a different, binary target (float vs non-float processed windows)."
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = ["Id", "RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "Type_of_glass"]
        df = pd.read_csv(raw_dir / "glass.data", header=None, names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["Id"])
        # the target's classes in words (CLEAN-25): the source's class names
        df = decode(
            df,
            {
                self.target: {
                    "1": "building windows float processed",
                    "2": "building windows non float processed",
                    "3": "vehicle windows float processed",
                    "5": "containers",
                    "6": "tableware",
                    "7": "headlamps",
                }
            },
        )
        return df
