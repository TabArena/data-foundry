"""Curated dataset definition for `horse_colic_survival` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, decode, set_missing

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "temperature_of_extremities": ["cold", "cool", "normal", "warm"],
    "peripheral_pulse": ["absent", "reduced", "normal", "increased"],
    "capillary_refill_time": ["< 3 seconds", ">= 3 seconds"],  # open-ended
    "peristalsis": ["absent", "hypomotile", "normal", "hypermotile"],
    "abdominal_distension": ["none", "slight", "moderate", "severe"],
    "nasogastric_tube": ["none", "slight", "significant"],
    "nasogastric_reflux": ["none", "< 1 liter", "> 1 liter"],  # open-ended
    "rectal_exam_feces": ["absent", "decreased", "normal", "increased"],
}


# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "temperature_of_extremities": {"1": "normal", "2": "warm", "3": "cool", "4": "cold"},
    "peripheral_pulse": {"1": "normal", "2": "increased", "3": "reduced", "4": "absent"},
    "capillary_refill_time": {"1": "< 3 seconds", "2": ">= 3 seconds"},
    "peristalsis": {"1": "hypermotile", "2": "normal", "3": "hypomotile", "4": "absent"},
    "abdominal_distension": {"1": "none", "2": "slight", "3": "moderate", "4": "severe"},
    "nasogastric_tube": {"1": "none", "2": "slight", "3": "significant"},
    "nasogastric_reflux": {"1": "none", "2": "> 1 liter", "3": "< 1 liter"},
    "rectal_exam_feces": {"1": "normal", "2": "increased", "3": "decreased", "4": "absent"},
    "mucous_membranes": {
        "1": "normal pink",
        "2": "bright pink",
        "3": "pale pink",
        "4": "pale cyanotic",
        "5": "bright red / injected",
        "6": "dark cyanotic",
    },
    "pain": {
        "1": "alert, no pain",
        "2": "depressed",
        "3": "intermittent mild pain",
        "4": "intermittent severe pain",
        "5": "continuous severe pain",
    },
    "abdomen": {
        "1": "normal",
        "2": "other",
        "3": "firm feces in the large intestine",
        "4": "distended small intestine",
        "5": "distended large intestine",
    },
    "abdominocentesis_appearance": {"1": "clear", "2": "cloudy", "3": "serosanguinous"},
    "age": {"1": "adult", "9": "young (< 6 months)"},
}


class HorseColicSurvival(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a horse with colic live, die or be put down?",
        use_case=(
            "For example, a veterinarian examining a horse with colic on arrival estimates whether it will survive, "
            "to advise the owner on surgery, treatment or euthanasia."
        ),
        row=(
            "One horse with colic at its first visit to a veterinary hospital (344 horses; place and period not "
            "stated)."
        ),
        predicted=("What eventually happened to the horse; it lived (62.5%), died (23%) or was euthanized (14.5%)."),
        known=(
            "Age group, rectal temperature, pulse and breathing rate, the state of the legs, gums and gut (pain, gut "
            "sounds, distension, rectal exam, abdomen), stomach-tube reflux and its acidity, and blood and "
            "belly-fluid values (packed cell volume, total protein)."
        ),
        split="Random horses, so the test data stands for new cases of the same hospital.",
        changes=(
            "We drop whether the horse had surgery and the lesion found, which come after the examination, and keep "
            "each horse's first visit only."
        ),
        fit="approximate",
        fit_reason=(
            "One of the three outcomes, euthanasia, is a decision by owner and vet that the prediction would inform, "
            "and the source states neither when the examination values were taken nor how long the horses were "
            "followed."
        ),
    )

    # Dataset
    unique_name = "horse_colic_survival"
    year = "1989"
    domain = "biology & life sciences"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C58W23"
    license = "CC BY 4.0"
    download_description = """
        Get the train and test data from UCI.

        wget https://archive.ics.uci.edu/static/public/47/horse+colic.zip && unzip horse+colic.zip horse-colic.data horse-colic.test && rm horse+colic.zip && mkdir -p local-data-warehouse/horse_colic_survival && mv horse-colic.data horse-colic.test local-data-warehouse/horse_colic_survival/
    """
    bibtex = """
        @misc{McLeish1989HorseColic,
          author       = {McLeish, Mary and Cecile, Matt},
          title        = {{Horse Colic}},
          year         = {1989},
          howpublished = {UCI Machine Learning Repository},
          note         = {{DOI}: https://doi.org/10.24432/C58W23}
        }
    """
    curation_comments = """
        We start with the data from UCI and merge the train and test data.

        - We encode missing values as NaN.
        - We drop features that leak the target.
        - We keep only the first instance (hospital number) per horse, as they can be treated multiple times and otherwise leaks information about the target.
        - We use the target "outcome" to model a task where we aim to predict if the horse survives or not. We drop cases that have not outcome recorded.
        - We keep the duplicates occurring in the data.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 8 columns are ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); 8 of them decoded from the source's codes
          into its words (`CODE_LABELS`, 2026-11-01); codes that mean unknown are missing (CLEAN-10).
        - Partial order, left unordered (2026-11-01, CLEAN-14): `pain`: the codebook says it "should NOT be treated as
          ordered"; alert (1) < intermittent mild (3) < intermittent severe (4) < continuous severe pain (5) is a line,
          and depressed (2) is off it. `mucous_membranes` has two lines from normal pink (1): pallor and cyanosis (3 < 4
          < 6) and congestion (2 < 5).
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 8 ordered codes carry their codebook's
          words (`CODE_LABELS`), in the same order; 5 unordered codes carry their words: `mucous_membranes`, `pain`,
          `abdomen`, `abdominocentesis_appearance`, `age`.
        - Class-dependent recording (record marker `Class-dependent Recording`): `total_protein` is recorded in two units, g/L (above 15) for 95 horses, of which 1 died and 27 were euthanized, and g/dL for 209, of which 64 died and 16 were euthanized. The switch follows the hospital number, that is the admission period, so the unit tells died from euthanized (ROC AUC 0.79 alone). Not harmonised yet: one unit for all rows removes the cue (TabPFN 3.5 log loss 0.682 to 0.724).
    """

    # Task
    target = "outcome"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason="The UCI donation (McLeish & Cecile, 1989) defines no metric; its stated class attribute is the surgical lesion (attr 24), not the outcome we predict, and no paper defines an evaluation for the outcome task.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "surgery",
            "age",
            "hospital_number",
            "rectal_temperature",
            "pulse",
            "respiratory_rate",
            "temperature_of_extremities",
            "peripheral_pulse",
            "mucous_membranes",
            "capillary_refill_time",
            "pain",
            "peristalsis",
            "abdominal_distension",
            "nasogastric_tube",
            "nasogastric_reflux",
            "nasogastric_reflux_ph",
            "rectal_exam_feces",
            "abdomen",
            "packed_cell_volume",
            "total_protein",
            "abdominocentesis_appearance",
            "abdominocentesis_total_protein",
            "outcome",
            "surgical_lesion",
            "lesion_type_1",
            "lesion_type_2",
            "lesion_type_3",
            "cp_data",
        ]
        df = pd.read_csv(raw_dir / "horse-colic.data", header=None, names=columns, na_values="?", sep=r"\s+")
        df_test = pd.read_csv(raw_dir / "horse-colic.test", header=None, names=columns, na_values="?", sep=r"\s+")
        return {"df": df, "df_test": df_test}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, df_test = raw["df"], raw["df_test"]
        df = pd.concat([df, df_test], ignore_index=True)
        # Drop duplicates by hospital number, keeping the first instance, as they can be treated multiple times and otherwise leaks information about the target.
        df = df.drop_duplicates(subset=["hospital_number"], keep="first")
        # Only keep non nan outcome rows
        df = df[~df["outcome"].isna()]
        df = df.drop(
            columns=[
                "hospital_number",  # constant now
                "surgery",  # leaks target
                "cp_data",  # no significance according to original data description
                # Other target outcomes and thus leaking of outcome
                "surgical_lesion",
                "lesion_type_1",
                "lesion_type_2",
                "lesion_type_3",
            ]
        )
        df["outcome"] = df["outcome"].map({1: "Lived", 2: "Died", 3: "Euthanized"})
        # codes outside a scale that mean unknown, and states outside it placed as missing (CLEAN-10,
        # CLEAN-14): don't know, refused, not asked, other
        df = set_missing(
            df,
            {
                "capillary_refill_time": [3.0],
            },
        )
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "age",
                "temperature_of_extremities",
                "peripheral_pulse",
                "mucous_membranes",
                "capillary_refill_time",
                "pain",
                "peristalsis",
                "abdominal_distension",
                "nasogastric_tube",
                "nasogastric_reflux",
                "rectal_exam_feces",
                "abdomen",
                "abdominocentesis_appearance",
            ],
        )
