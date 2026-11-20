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
        row=(
            "One glass fragment collected in forensic work by the UK Home Office Forensic Science Service, 1987 "
            "(212 fragments)."
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
    data_tags = ("Timeless",)
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/42/glass+identification.zip && unzip glass+identification.zip && rm glass+identification.zip glass.names glass.tag Index
        mkdir -p local-data-warehouse/forensic_glass_identification && mv glass.data local-data-warehouse/forensic_glass_identification/
    """
    curation_comments = """
        We start with the data from UCI. Its documentation (`glass.names`) gives the creator as B. German of the Home Office Forensic Science Service, Aldermaston (UK); the abstract on the UCI page says "USA Forensic Science Service".

        - We drop the ID column, as it is a just a row identifier and does not contain any useful information for modeling.
        - We drop one of two identical rows (Ids 39 and 40, float window glass), so that a copy cannot sit on both sides of a split.
        - We drop Id 68 (2026-11-12, Andrej, review issue 4, B): it agrees with Id 67 in eight of nine values and differs only in silicon (72.22 against 72.32), while two analyses of one glass do not agree to 0.01 percent in six oxides, so it reads as Id 67 entered a second time. Float building windows go from 69 to 68 of 212 rows; the class shares move by less than 0.2 points.
        - The source file is sorted by class and, within a class, in a few blocks that each run roughly from high to low magnesium; the features predict the order (Spearman 0.67-0.90 per class). We shuffle the rows, so the order carries no information here. Beyond that sort, fragments of one object sit next to each other in the file (Ids 67 and 69 share the refractive index), but holding out blocks of 3 neighbouring rows costs at most 0.06 log loss and leaves the ranking of models unchanged. Near-copies: 6 rows have a copy within 0.08 SD on RI, Mg, Al, K and Ca (all of the same type, 4 of them file neighbours), 75 (35%) within 0.16 SD (95% of the same type, 31% file neighbours; about six times what a within-class shuffle of the columns gives); looking such copies up gains an explicit model 0.03 to 0.045 log loss on random splits. 7 glass objects (14 rows) share an identical refractive index with every oxide within the tolerance of two analyses (7 such pairs where chance gives 1.8); they are not grouped, and the split stays random by decision (splits comment).
        - The target (2026-11-01, CLEAN-25): `Type_of_glass` ships its classes as words (glass.names, 11. Type of
          glass).
        - Time basis: Timeless: the glass type is a property of the object the fragment came from, and the refractive
          index and oxides are measured on the fragment, so nothing in a row arrives later. The Home Office laboratory
          gathered the fragments from casework before September 1987 and no date is published; the Id order is a sort by
          class and by magnesium within it. Not tested: glass made since then (36% of the rows are non-float window
          glass, hardly made since the mid-1970s) and today's trace-element casework.
    """

    # Task
    splits_comment = """
        Default splits: random fragments, stratified on the glass type. The random split is a deliberate choice
        (2026-11-12, Andrej, review issue 2, A), weighed against a split grouped on glass objects: no clean groups
        govern how the collection was made. Only 7 objects (14 rows, 7%) are tied together by a link calibrated against
        chance (identical refractive index, the same type and every oxide within the tolerance of two analyses: 7
        pairs where chance gives 1.8, so one or two may be chance), and their fragments can sit on both sides. The
        other near-copies are different objects of the same kind of glass, which a reference collection holds, so a
        random split over them matches the use. Holding out the 7 objects cost TabPFN 0.009 log loss (0.571 against
        0.562) and the random forest 0.008, and left the ranking of models unchanged (2026-11-06, on 213 rows).
    """
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
        # Id 68 is Id 67 entered again: equal in eight of nine values, silicon 72.32 against 72.22
        df = df[df["Id"] != 68]
        df = df.drop(columns=["Id"])
        # Ids 39 and 40 are identical in every column
        df = df.drop_duplicates(keep="first")
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
