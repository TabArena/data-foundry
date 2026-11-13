"""Curated dataset definition for `gallstone_disease` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Hepatic Fat Accumulation (HFA)": ["no fat accumulation", "mild", "moderate", "severe", "very severe"],
}


# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "Hepatic Fat Accumulation (HFA)": {
        "0": "no fat accumulation",
        "1": "mild",
        "2": "moderate",
        "3": "severe",
        "4": "very severe",
    },
    "Gender": {"0": "male", "1": "female"},
    "Comorbidity": {"0": "none", "1": "any"},
}


class GallstoneDisease(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does an outpatient have gallstone disease?",
        use_case=(
            "An internal-medicine clinic screens outpatients for gallstone disease from a body-composition scan and "
            "routine blood tests, for example to decide who goes on to imaging (the source paper's aim is early "
            "prediction)."
        ),
        row=(
            "One person seen at the Internal Medicine Outpatient Clinic of Ankara VM Medical Park Hospital, Turkey, "
            "June 2022 to June 2023 (319 people)."
        ),
        predicted=(
            "Whether the person was diagnosed with gallstone disease (161 of 319, about half); how it was diagnosed "
            "is not stated."
        ),
        known=(
            "Age, sex, other illnesses (coronary disease, hypothyroidism, high blood lipids, diabetes), height and "
            "weight, body composition from bioimpedance (water, fat, muscle, bone, visceral and liver fat), and blood"
            " tests (sugar, lipids, liver and kidney values, inflammation, haemoglobin, vitamin D)."
        ),
        split="Random people, so the test data stands for new patients of the same clinic and year.",
        fit="direct",
        fit_reason=(
            "The values are measured at the visit where the diagnosis is made, as in screening. The base is narrow "
            "(one clinic, one year, half with gallstones), and how the people were chosen is not stated, so another "
            "clinic's mix may differ."
        ),
    )

    # Dataset
    unique_name = "gallstone_disease"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://archive.ics.uci.edu/dataset/1150/gallstone-1",  # the paper says its data are not public
            license="CC BY 4.0",
            year="2025",
            bibtex=r"""
                @article{esen2024early,
                  title={Early prediction of gallstone disease with a machine learning-based method from bioimpedance and laboratory data},
                  author={Esen, {\.I}rfan and Arslan, Hilal and Esen, Selin Akt{\"u}rk and G{\"u}l{\c{s}}en, Mervenur and K{\"u}ltekin, Nimet and {\"O}zdemir, O{\u{g}}uzhan},
                  journal={Medicine},
                  volume={103},
                  number={8},
                  pages={e37258},
                  year={2024},
                  publisher={LWW}
                }
            """,
        ),
    )
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/1150/gallstone-1.zip && unzip gallstone-1.zip && rm gallstone-1.zip && unzip dataset-uci.zip && rm dataset-uci.zip && mkdir -p local-data-warehouse/gallstone_disease && mv dataset-uci.xlsx local-data-warehouse/gallstone_disease/
    """
    curation_comments = """
        We use the data without any further curation.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); 1 of them decoded from the source's codes
          into its words (`CODE_LABELS`, 2026-11-01).
        - `Comorbidity` is "any comorbidity", 0 or 1, as the paper describes it: all 217 rows with 0 have none of the
          four listed diseases (CAD, hypothyroidism, hyperlipidemia, diabetes), and the 1s have one, two, or another
          condition. Three rows hold an undocumented 2 (1 row) or 3 (2 rows), each with exactly one listed disease: an
          entry error for 1, recoded to 1; the rows stay (CLEAN-11; the curator's marks of 2026-10-31).
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 1 ordered codes carry their codebook's
          words (`CODE_LABELS`), in the same order; 2 unordered codes carry their words: `Gender`, `Comorbidity`.
        - The target (2026-11-01, CLEAN-25): `Gallstone Status` ships its classes as words (0 means gallstones present
          (UCI)). Binary: "Yes" is the event, the class that sorts second, so it is the metrics' positive class.
        - Time basis: ForcedIIDFromTemporal (Andrej, 2026-11-13; was `StationaryRelation`, the curator's call of
          2026-11-11, which a stationary relation cannot carry without dates to measure it on): outpatients of one
          clinic, June 2022 to June 2023 (Esen et al. 2024), the diagnosis and every feature from the same visit; the
          file keeps no visit date, so the time is lost and random patients stand in for later ones. Along the file's
          order (rank within each sorted block) the relation drifts: training on one contiguous half and testing on the
          other scores 0.06-0.07 ROC AUC below random halves for every model, mostly because AST and ALT of those
          without gallstones step up mid-file; that order is not shown to be time (vitamin D has no seasonal wave along
          it). A dated release would test later outpatients and whether the two groups were recruited in different
          months (vitamin D follows the season).
    """

    # Task
    target = "Gallstone Status"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Esen et al. 2024 report accuracy, precision, recall, F-measure and AUC; accuracy is the headline, none is named as the criterion (MET-5). roc_auc is the binary fallback."
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "dataset-uci.xlsx", sheet_name="dataset", engine="calamine")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # Comorbidity is 0 (none) or 1 (any); the three 2 and 3 have one of the listed diseases each (curation notes)
        df = raw
        df["Comorbidity"] = df["Comorbidity"].replace({2: 1, 3: 1})
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"0": "Yes", "1": "No"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "Coronary Artery Disease (CAD)",
                "Hypothyroidism",
                "Gender",
                "Comorbidity",
                "Hyperlipidemia",
                "Diabetes Mellitus (DM)",
            ],
        )
