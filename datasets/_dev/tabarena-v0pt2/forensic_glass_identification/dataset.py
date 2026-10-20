"""Curated dataset definition for `forensic_glass_identification` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


class ForensicGlassIdentification(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What kind of glass does a fragment come from, judging from its chemical make-up?",
        use_case=(
            "A forensic scientist identifies the type of a glass fragment left at a crime scene, so that it can be "
            "used as evidence (the source's motivation)."
        ),
        row=(
            "One glass fragment collected in forensic work by the UK Home Office Forensic Science Service, 1987 "
            "(213 fragments)."
        ),
        predicted=(
            "The glass type, one of six: building windows, float-processed (32%) or not (36%), float-processed "
            "vehicle windows, containers, tableware or headlamps."
        ),
        known=(
            "The refractive index and the weight percent of the oxides of eight elements (sodium, magnesium, "
            "aluminium, silicon, potassium, calcium, barium, iron)."
        ),
        split="Random samples, so the test data stands for new fragments of the same types.",
        fit="approximate",
        fit_reason=(
            "The features are measurements on a fragment and the label is what an investigator wants to know, but both "
            "are dated: casework today compares fragments by trace elements, non-float window glass (36%) has hardly "
            "been made since the 1970s, and the class shares are those of the collection, not of casework. Two classes "
            "have 9 and 13 samples."
        ),
    )

    # Dataset
    unique_name = "forensic_glass_identification"
    year = "1987"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5WW2P"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/42/glass+identification.zip && unzip glass+identification.zip && rm glass+identification.zip glass.names glass.tag Index
        mkdir -p local-data-warehouse/forensic_glass_identification && mv glass.data local-data-warehouse/forensic_glass_identification/
    """
    bibtex = """
        @misc{German1987glass,
          author       = {German, B.},
          title        = {{Glass Identification}},
          year         = {1987},
          howpublished = {UCI Machine Learning Repository},
          note         = {{DOI}: https://doi.org/10.24432/C5WW2P}
        }
    """
    curation_comments = """
        We start with the data from UCI. Its documentation (`glass.names`) gives the creator as B. German of the Home Office Forensic Science Service, Aldermaston (UK); the abstract on the UCI page says "USA Forensic Science Service".

        - We drop the ID column, as it is a just a row identifier and does not contain any useful information for modeling.
        - We drop one of two identical rows (Ids 39 and 40, float window glass), so that a copy cannot sit on both sides of a split.
        - The source file is sorted by class and, within a class, in a few blocks that each run roughly from high to low magnesium; the features predict the order (Spearman 0.67-0.90 per class). We shuffle the rows, so the order carries no information here. Beyond that sort, fragments of one object sit next to each other in the file (Ids 67-69 share the refractive index), but holding out blocks of 3 neighbouring rows costs at most 0.06 log loss and leaves the ranking of models unchanged, so the split stays random.
    """

    # Task
    target = "Type_of_glass"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = ["Id", "RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "Type_of_glass"]
        df = pd.read_csv(raw_dir / "glass.data", header=None, names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["Id"])
        # Ids 39 and 40 are identical in every column
        df = df.drop_duplicates(keep="first")
        return df
