"""Curated dataset definition for `dementia_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    ScoringColumn,
    TaskSummary,
    UnitWeight,
)

# Scores and ratings with no words per level: numbers, as the source ships them (CLEAN-14).
SCORES = ["SES"]


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "CDR": ["no_dementia", "very_mild_AD", "mild_AD"],
}


class DementiaPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("How severe is an older adult's dementia, judging from a short cognitive test and a brain scan?"),
        use_case=(
            "The source defines no task. For example, at a first visit a memory clinic estimates a person's clinical "
            "dementia rating from a short cognitive test and a brain MRI, before or instead of the full clinical "
            "interview."
        ),
        row=(
            "One visit of an older adult in the OASIS-2 study, which scanned 150 people on two or more visits at "
            "least a year apart (370 visits; Marcus et al. 2010)."
        ),
        predicted=(
            "The visit's clinical dementia rating: no dementia (56%), very mild (33%) or mild (11%) Alzheimer's "
            "dementia."
        ),
        known=(
            "Sex, age, years of education, socioeconomic status, the visit's Mini-Mental State Examination score, and"
            " three brain-size measures from the visit's MRI scan."
        ),
        split=(
            "Whole people are held out, so the test data stands for people not seen before; each of their visits is "
            "scored on its own, and each person counts once in the score."
        ),
        changes=(
            "We drop the group label (derived from the ratings of all visits), the visit number and the time since "
            "the first visit, and the 3 visits rated moderate dementia."
        ),
        fit="approximate",
        fit_reason=(
            "The use case is ours, as the source states none. Follow-up visits of test people are scored as if each "
            "were a first visit, and the MRI enters as three summary numbers of an imaging study."
        ),
    )

    # Dataset
    unique_name = "dementia_prediction"
    year = "2010"
    domain = "medical & healthcare"
    source = "Other"
    source_url = "https://sites.wustl.edu/oasisbrains/"  # OASIS-2; the Mendeley deposit is a later copy
    license = "CC BY NC 3.0"
    data_tags = ("WrongDomain",)
    download_description = """
        We get the data from Mendeley version of another paper (https://www.sciencedirect.com/science/article/pii/S2352914819300917?via%3Dihub).

        wget https://data.mendeley.com/public-files/datasets/tsy6rbc5d4/files/b4978a7c-df15-46b2-be69-891d4935b652/file_downloaded && mv file_downloaded oasis_longitudinal_demographics.xlsx && mkdir -p local-data-warehouse/dementia_prediction && mv oasis_longitudinal_demographics.xlsx local-data-warehouse/dementia_prediction/
    """
    bibtex = """
        @article{marcus2010open,
          title={Open access series of imaging studies: longitudinal MRI data in nondemented and demented older adults},
          author={Marcus, Daniel S and Fotenos, Anthony F and Csernansky, John G and Morris, John C and Buckner, Randy L},
          journal={Journal of cognitive neuroscience},
          volume={22},
          number={12},
          pages={2677--2684},
          year={2010},
        }
    """
    curation_comments = """
        We start with the data from Mendeley.

        - CDR and Group are both the same target variable. CDR is the Clinical Dementia Rating (0 = no dementia, 0.5 = very mild AD, 1 = mild AD, 2 = moderate AD), which determines the group variable. 31 of the 150 subjects change their rating across visits (the 'Converted' group). We make this a task to predict for a patient (at any given time point of a scan) their dementia rating. The rating is ordinal but discrete, so we treat it as a classification problem (not regression). We drop cases with moderate_AD (n=3), as we do not have enough data on this class to include them in our prediction task.
        - We drop the group variable (Nondemented / Demented / Converted, derived from the ratings over the visits) and the time of the scan (visit number, MR delay). We predict each visit's rating from the subject's sex, age, years of education (EDUC), socioeconomic status (SES, 19 missing), the Mini-Mental State Examination score of the same visit (MMSE, 2 missing; a separate cognitive test, not derived from the rating) and three measures from the visit's MRI scan: estimated total intracranial volume (eTIV), normalized whole-brain volume (nWBV) and the atlas scaling factor (ASF, which is 1755 / eTIV, kept as in the source).
        - We also drop the constant hand column.
        - Each person counts once in the score (Lennart, 2026-11-08, review issue 1; MET-17): the log loss weights a visit by 1 over its person's number of visits (`person_weight`, counted after the moderate visits are dropped), a scoring column for the metric only, no feature and no training weight. The 150 people have 1 to 5 visits (91 two, 43 three, 13 four or five), and the memory clinic acts once per person; unweighted, a person seen five times counted five times. Follow-up visits are still scored, each as if it were a first visit, at one vote per person. On the 60 shipped splits the weighted log loss ranks 8 untuned predictors (two logistic regressions, random forest, extra trees, two LightGBM, kNN, the class shares) like the per-visit one at Kendall tau 0.94 per split on average (lowest 0.71) and 1.0 for the ranking by the mean over the splits, the same best model on 56 of 60. Scoring only the first visits was the alternative (tau 0.87 per split, 48 to 52 scored visits per fold against 112 to 138). The weight is for scoring only (MET-15 as amended 2026-11-08): training a logistic regression with it changes the weighted log loss by -0.004 (SE 0.003, lower on 35 of 60 grouped random splits), within noise.
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 1 scores with no words per level are
          numbers (`SCORES`): `SES`.
        - The target (2026-11-01, CLEAN-25): `CDR` ships its classes as words, no_dementia < very_mild_AD < mild_AD (the
          Clinical Dementia Rating's order (CDR 0, 0.5, 1)).
    """

    # Task
    target = "CDR"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The OASIS-2 paper describes the data and reports group analyses, no prediction task or metric; the "
            "Mendeley copy's paper is a later reuse, not the first publication. Each person counts once: a visit "
            "weighs 1 over its person's number of visits (`person_weight`; 1 to 5 visits per person), where "
            "unweighted a person seen five times would count five times (Lennart, 2026-11-08)."
        ),
        inputs={"weight": "person_weight"},
    )
    scoring_columns = (
        ScoringColumn(
            column="person_weight",
            role="weight",
            used_by="log_loss",
            description=(
                "1 over the number of visits of the row's person (from 1/5 to 1), so that each person counts once "
                "in the log loss; for scoring only, never a feature or a training weight"
            ),
        ),
    )
    unit_weight = UnitWeight(column="person_weight", unit="Subject ID")
    grouping = Grouping(
        on="Subject ID",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a subject of OASIS-2: older adults scanned on two or more visits at least a year apart, each visit with its own clinical dementia rating (Marcus et al. 2010). Each visit is one prediction, made from that visit alone, for a subject not seen in training: a first-visit framing, since a follow-up visit would know the earlier ratings. Each subject counts once in the score (`person_weight`). The source defines no prediction task.
        """,
    )

    # Splits
    splits_comment = """
        We create stratified grouped 20-repeated 3-fold split. This puts about 50 subjects (112-138 visits) in each test fold.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "oasis_longitudinal_demographics.xlsx")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(
            columns=[
                "MRI ID",
                "Visit",
                "MR Delay",  # uninformative time information
                "Group",  # leak
                "Hand",  # constant
            ]
        )
        # 0 = no dementia, 0.5 = very mild AD, 1 = mild AD, 2 = moderate AD)
        df["CDR"] = df["CDR"].replace({0.5: "very_mild_AD", 1: "mild_AD", 2: "moderate_AD", 0: "no_dementia"})
        df = df[df["CDR"] != "moderate_AD"].copy()
        # Each person counts once in the score: 1 over the person's visits (curation comments)
        df["person_weight"] = 1.0 / df.groupby("Subject ID")["Subject ID"].transform("size")
        df = df.sample(frac=1, random_state=42).sort_values(by=["Subject ID"], kind="stable").reset_index(drop=True)
        # scores with no words per level are numbers (CLEAN-14)
        df[SCORES] = df[SCORES].astype("object").apply(pd.to_numeric)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(ordinal=ORDINAL_LEVELS, categorical=["M/F", "Subject ID"])
