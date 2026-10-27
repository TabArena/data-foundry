"""Curated dataset definition for `horse_colic_survival` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


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
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
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
