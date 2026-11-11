"""Curated dataset definition for `horse_colic_survival` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    set_missing,
)

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
        question="Will a horse with colic survive to leave the hospital?",
        use_case=(
            "For example, a veterinarian examining a horse with colic on arrival estimates whether it will survive, "
            "to advise the owner on surgery, treatment or euthanasia, with a model built on the hospital's earlier "
            "admissions; the horse may be on its first or a return visit."
        ),
        row=(
            "One admission of a horse with colic to the teaching hospital of the Ontario Veterinary College, Guelph "
            "(344 admissions of 334 horses, in the order of their case numbers; the period is not stated, likely the "
            "1980s)."
        ),
        predicted="Whether the horse did not survive, that is died or was euthanized: 129 of 344 (37.5%).",
        known=(
            "Age group, rectal temperature, pulse and breathing rate, the state of the legs, gums and gut (pain, gut "
            "sounds, distension, rectal exam, abdomen), stomach-tube reflux and its acidity, and blood and "
            "belly-fluid values (packed cell volume, total protein)."
        ),
        split=(
            "Three windows of 57 horses in case-number order, each trained on all earlier horses, so a model meets "
            "later admissions, including the hospital's change in how it recorded some lab values."
        ),
        changes=(
            "We merge died and euthanized into did not survive, drop whether the horse had surgery and the lesion "
            "found, which come after the examination, and keep one row per hospital number."
        ),
        fit="approximate",
        fit_reason=(
            "Not surviving includes euthanasia, a decision by owner and vet that the prediction would inform, and "
            "the source states neither when the examination values were taken nor the calendar period of the cases."
        ),
    )

    # Dataset
    unique_name = "horse_colic_survival"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C58W23",
            license="CC BY 4.0",
            year="1989",
            bibtex="""
                @misc{McLeish1989HorseColic,
                  author       = {McLeish, Mary and Cecile, Matt},
                  title        = {{Horse Colic}},
                  year         = {1989},
                  howpublished = {UCI Machine Learning Repository},
                  note         = {{DOI}: https://doi.org/10.24432/C58W23}
                }
            """,
        ),
    )
    download_description = """
        Get the train and test data from UCI.

        wget https://archive.ics.uci.edu/static/public/47/horse+colic.zip && unzip horse+colic.zip horse-colic.data horse-colic.test && rm horse+colic.zip && mkdir -p local-data-warehouse/horse_colic_survival && mv horse-colic.data horse-colic.test local-data-warehouse/horse_colic_survival/
    """
    curation_comments = """
        We start with the data from UCI and merge the train and test data.

        - We encode missing values as NaN.
        - We drop features that leak the target.
        - We keep the first row per hospital number. The 22 repeated hospital numbers are one visit with several lesion
          codes (one pair with conflicting outcomes), not repeat visits; the first row is kept (corrected 2026-11-10).
        - Target (2026-11-10, Andrej, review issue 1 B): `did_not_survive`, "Yes" when the horse died or was
          euthanized (129 of 344), "No" when it lived, the usual survival-to-discharge outcome of colic prognosis
          (Bishop et al. 2022, Vet Surg 51:891, https://doi.org/10.1111/vsu.13839). Died against euthanized follows the
          admission period (earlier case numbers 58 died / 14 euthanized among non-survivors, later ones 4 / 34) with
          similar clinical findings, so the three classes are not kept. We drop cases with no outcome recorded.
        - Collection (2026-11-10, from the creators' papers): the horses came to the teaching hospital of the Ontario
          Veterinary College, Guelph, one hospital; the rows come from its patient information system, which stores
          the presenting complaint, treatment, diagnosis and outcome, with much of the clinical pathology "electronically
          generated by the lab equipment" (Cecile & McLeish, arXiv:1304.2344; McLeish et al., arXiv:1304.1519). No
          admission date is given; the hospital number is "the case number assigned to the horse" (UCI codebook) and
          orders the admissions. The first 229 case numbers (up to 530,560; 60% lived) match in size and survival the
          231 teaching-hospital horses of Pascoe et al. 1990 (Can J Vet Res, PMC1255672, 61% survivors); the later 115
          (67% lived) mostly follow a second recording route (below). This reading rests on the counts, not on a
          statement of the source. Missing values can follow the outcome: "sometimes records ended because euthanasia
          was chosen as a solution for cost reasons" (arXiv:1304.2344). UCI's 300/68 files are not a time split (both
          span the whole range of case numbers).
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
        - Recording change, kept (Exception to CLEAN-21, 2026-11-10, Andrej, review issue 2 A): `total_protein` is
          recorded in g/L (values above 15) for 95 horses, 92 of them with case numbers above 530,560, and in g/dL for
          209; in the g/L rows every measured `abdominocentesis_total_protein` (44 values) and `nasogastric_reflux_ph`
          (11) is exactly 1 or 2, codes the source does not explain, while elsewhere these columns hold measurements.
          All three stay as recorded: the recording changes once, along the time order, and is unrelated to the label
          (Fisher p = 0.16), so the middle window tests what the hospital met, a model trained on the old recording (3
          g/L rows of 230) scoring later horses recorded the new way (45 g/L of 57). Serves P4 (a split that mirrors
          the application) and P5 (the data as recorded). Untuned, three windows newest first: as recorded LightGBM
          log loss 0.549 / 0.783 / 0.917, logistic regression 0.548 / 2.324 / 0.768; harmonised 0.611 / 0.841 / 0.911
          and 0.587 / 0.720 / 0.809. Under the source's three classes the unit told died from euthanized (ROC AUC 0.79
          alone), which the `Class-dependent Recording` marker records.
        - Time order (2026-11-10, Andrej, review issue 3 B): `case_number` is the hospital number's first six digits (the
          42 seven-digit numbers are a six-digit case number with one digit appended, a 9 for 25 of 28 foals); the
          frame is sorted by case number, then by the full number, so a case's suffixed later visits come after its
          first visit. It is the time column and ships as a feature.
        - Return visits kept (2026-11-10, Andrej, review issue 4 A): nine cases appear two or three times under one
          six-digit case number with a suffix (10 later rows; the codebook: "may not be unique if the horse is treated >
          1 time"), all first visits survived. A return visit is an admission to score; the time order keeps each
          later visit after its first, so no window trains on a later visit and tests the first.
    """

    # Task
    target = "did_not_survive"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="The UCI donation (McLeish & Cecile, 1989) defines no metric; its stated class attribute is the surgical lesion (attr 24), not the outcome we predict, and the survival models of the field (Pascoe et al. 1990, Bishop et al. 2022) report sensitivity and specificity at a chosen cut, not a ranking metric.",
    )

    # Splits
    splits_comment = """
        Three test windows of 57 horses in case-number order, walking back from the newest; each trains on all earlier
        horses (50%, 67% and 83% of the rows), so no window trains on less than half of the data (SPLIT-14). The case
        number orders the admissions but gives no dates, so the windows are counts of horses, not calendar periods.
        The outcome is known by discharge, far sooner than a window, so there is no gap. The oldest window tests
        horses recorded the old way, the middle one is the first to meet the second recording route (trained on
        almost none of it), the newest is tested after a refit that has seen it (2026-11-10, Andrej, review issue 3 B).
    """
    temporal = Temporal(
        on="case_number",
        splits=TemporalSplits(window=57, unit="rows", n_windows=3, min_train_fraction=0.5),
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
        # the case number orders the admissions: a seven-digit number is a six-digit case number with a digit appended;
        # sort by it, then by the full number, so suffixed later visits follow the first visit (review issue 3)
        df["case_number"] = np.where(
            df["hospital_number"] >= 1_000_000, df["hospital_number"] // 10, df["hospital_number"]
        ).astype(int)
        df = df.sort_values(["case_number", "hospital_number"], kind="stable").reset_index(drop=True)
        df = df.drop(
            columns=[
                "hospital_number",  # the case number carries its order
                "surgery",  # leaks target
                "cp_data",  # no significance according to original data description
                # Other target outcomes and thus leaking of outcome
                "surgical_lesion",
                "lesion_type_1",
                "lesion_type_2",
                "lesion_type_3",
            ]
        )
        # did not survive: died (2) or euthanized (3), the event "Yes" (review issue 1 B; CLEAN-25)
        df["did_not_survive"] = df.pop("outcome").map({1: "No", 2: "Yes", 3: "Yes"})
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
