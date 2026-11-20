"""Curated dataset definition for `diabetes_130_us` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    set_missing,
)

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "age": [
        "[0-10)",
        "[10-20)",
        "[20-30)",
        "[30-40)",
        "[40-50)",
        "[50-60)",
        "[60-70)",
        "[70-80)",
        "[80-90)",
        "[90-100)",
    ],
    "weight": [
        "[0-25)",
        "[25-50)",
        "[50-75)",
        "[75-100)",
        "[100-125)",
        "[125-150)",
        "[150-175)",
        "[175-200)",
        ">200",
    ],  # open-ended
    "max_glu_serum": ["Norm", ">200", ">300"],  # open-ended
    "A1Cresult": ["Norm", ">7", ">8"],  # open-ended
    "metformin": ["Down", "Steady", "Up"],
    "repaglinide": ["Down", "Steady", "Up"],
    "nateglinide": ["Down", "Steady", "Up"],
    "chlorpropamide": ["Down", "Steady", "Up"],
    "glimepiride": ["Down", "Steady", "Up"],
    "glipizide": ["Down", "Steady", "Up"],
    "glyburide": ["Down", "Steady", "Up"],
    "pioglitazone": ["Down", "Steady", "Up"],
    "rosiglitazone": ["Down", "Steady", "Up"],
    "acarbose": ["Down", "Steady", "Up"],  # Down only in 3 later stays, not in the first stays
    "miglitol": ["Down", "Steady", "Up"],
    "insulin": ["Down", "Steady", "Up"],
    "glyburide-metformin": ["Down", "Steady", "Up"],
}


class Diabetes130Us(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a diabetic patient be readmitted to hospital within 30 days of discharge?",
        use_case=(
            "For example, at discharge a hospital decides which diabetic patients get extra follow-up, such as a call"
            " or an early visit, to prevent an early readmission."
        ),
        row=(
            "One hospital stay of a diabetic patient at one of 130 US hospitals, 1999-2008: every stay in the file "
            "(99,343 stays of 69,990 patients), in the order of the hospitals' encounter numbers."
        ),
        predicted=(
            "Whether the patient is readmitted within 30 days of discharge (9% are); a later readmission counts as no."
        ),
        known=(
            "Age, sex, race, payer, admission type and source, discharge destination, admitting specialty, three "
            "diagnoses, length of stay, counts of lab tests, procedures and medications in the stay and of visits in "
            "the year before, glucose and HbA1c results, and the diabetes drugs and their changes."
        ),
        split=(
            "Nine windows of later stays in encounter order, each trained on every earlier stay, so the test data "
            "stands for the next discharges, as when a hospital scores them; a returning patient's earlier stays can "
            "be in training."
        ),
        changes=(
            "We keep every stay, where the paper keeps each patient's first, and drop stays that ended in death or "
            "discharge to a hospice, as the paper does; the encounter number becomes a time index."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is recorded by discharge and the outcome follows within 30 days, as when the "
            "model is used. The stays carry no dates, but the encounter number runs as a calendar over 1999-2008 across all "
            "hospitals, so the windows test on later care; a window counts stays, not days."
        ),
    )

    # Dataset
    unique_name = "diabetes_130_us"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5230J",
            license="CC BY 4.0",
            year="2014",
            bibtex="""
                @article{strack2014impact,
                  title={Impact of HbA1c measurement on hospital readmission rates: analysis of 70,000 clinical database patient records},
                  author={Strack, Beata and DeShazo, Jonathan P and Gennings, Chris and Olmo, Juan L and Ventura, Sebastian and Cios, Krzysztof J and Clore, John N},
                  journal={BioMed research international},
                  volume={2014},
                  number={1},
                  pages={781670},
                  year={2014},
                  publisher={Wiley Online Library}
                }
            """,
        ),
    )
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/diabetes_130_us/ && wget -P local-data-warehouse/diabetes_130_us/ https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip && unzip local-data-warehouse/diabetes_130_us/diabetes+130-us+hospitals+for+years+1999-2008.zip -d local-data-warehouse/diabetes_130_us/
    """
    curation_comments = """
        - Every stay (2026-11-11, Andrej, review issue 1 d): we keep all encounters of a patient, 99,343 stays of 69,990 patients after the filter below. The paper kept "only the first encounter for each patient as the primary admission" (Strack et al. 2014, Sec. 2.3) for the independence its logistic regression assumes; a hospital scores every discharge and knows a returning patient's earlier stays (USE-10, LEAK-34). In windows of encounter order the first stays are a group that narrows over the years (30-day rate 9.9% in the oldest half, 9.3%, 8.3% and 6.4% in three windows from the newest half), while over every stay it holds at 10.8% to 11.3%. TabArena v0.1 and BeyondArena kept the first stay (`drop_duplicates(subset="patient_nbr")`) with random folds; v0.2 did the same until 2026-11-11 (69,973 rows).
        - We remove encounters that ended in death or discharge to a hospice, as the paper does ("we removed all encounters that resulted in either discharge to a hospice or patient death, to avoid biasing our analysis", Sec. 2.3): a patient who died cannot be readmitted (the 1,084 "Expired" encounters were all "No"), so these rows are not part of the readmission task.
        - We set "?" (race, weight, payer code, specialty, diagnoses) and the "NULL" code of the three ID columns to missing values; pandas also reads the "None" (test not taken) of max_glu_serum and A1Cresult as missing.
        - We reversed the original ordinal encoding for three ID-based features (admission_type_id, discharge_disposition_id, admission_source_id).
        - We created the target from the "readmitted" column following the original task description: "<30" becomes "Yes", everything else "No".
        - We drop "patient_nbr", the patient id. "encounter_id" becomes `time_index` (encounter_id // 6, below) and is dropped otherwise. A patient's earlier stays as features of their own (their count in the file, the last stay's label) would be allowed under the temporal split (USE-10) and are a step to measure separately; the stay already carries the visits of the year before.
        - The other codes for an unknown value ("Not Available" and "Not Mapped" in the ID columns, "Unknown/Invalid" in gender) stay as categories, as IDS_mapping.csv lists them as codes of their own next to "NULL".
        - We drop examide and citoglipton, which are constant ("No") after the filters above, and glimepiride-pioglitazone, "Steady" in a single stay and "No" in all others.
        - Time order (2026-11-06 analysis, review issue 1): `encounter_id` is the Health Facts warehouse's running number of encounters (6 times a running number, 6n + 2 for the newest 11% of stays after a change of the id scheme; it ends at 73,977,870, close to the paper's 74,036,643 encounters), and it runs as a calendar across all hospitals: the distance in that number to the same patient's next stay tells a `<30` label from a `>30` one (ROC AUC 0.89), and summed over the file the 30-day scale gives 9.3 years from the first stay to the last, for the source's 1999-2008. Had the hospitals been loaded one after another, 30 days at one hospital would span far fewer numbers. We keep `time_index` = encounter_id // 6 (monotone in encounter_id across the scheme change) as the time column (SPLIT-22). The shift along the order that the earlier notes saw (payer code missing in the oldest fifth, up to 16 diagnoses only in the newest fifth) is time: a change of the warehouse's recording, which the windows now test. The drugs date the order without the label or a returning patient (2026-11-11 check, tenths of the stays in encounter order): troglitazone, withdrawn in March 2000, is in 3 stays, all in the first 0.1%; glipizide-metformin (approved 2002) first appears at 40%, metformin-rosiglitazone (2002) at 85%, metformin-pioglitazone (2005) at 97%; rosiglitazone falls from about 770 stays a tenth to 319 and 222 in the newest two (the 2007 safety warning); and among first stays alone payer code is missing in all of the oldest two tenths and 9% to 19% of the newest four.
        - Hospitals: the 130 hospitals are not recoverable; no copy (UCI, OpenML 4541 and 43874, the R package `readmission`) has a hospital id, both ids interleave the hospitals, and recording habits mark only 14.6% of the stays (SPLIT-24, SPLIT-25). A hospital scores its own next discharges, so the hospital would be a feature, not a reason for another split.
        - Target (2026-11-11, Andrej, review issue 2 A): the source's three-way `readmitted` (`<30`, `>30`, `NO`) stays binary, 30 days against the rest. Only `<30` has one horizon for every stay and is complete to the end of the file (10.5% to 12% in each estimated year); `>30` counts a readmission at any later time, so the oldest stays were followed about nine years longer than the newest. On the first stays the three classes rank `<30` as the binary model does (P(`<30`) ROC AUC 0.644 against 0.643, LightGBM), the order of the levels adds nothing, and any readmission (ROC AUC 0.668) loses its skill in the newest window (log-loss skill 0.006 against 0.059 at random).
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 17 columns are
          ordered categories in the order of the source's codebook (`ORDINAL_LEVELS`); 13 hold a state outside the
          scale, placed by the curator's rule (missing when the column has no other missing value, else the lowest
          level; a state that is simply not on the scale, such as Other, is missing); codes that mean unknown are
          missing (CLEAN-10).
    """

    # Task
    target = "EarlyReadmission"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The first publication is an explanatory logistic-regression study (odds ratios, significance of HbA1c "
            "measurement); it defines no predictive score, and the UCI page names none."
        )
    )

    # Splits
    splits_comment = """
        Nine test windows of 5,519 stays in encounter order (`time_index`), walking back from the newest; each trains on
        every earlier stay (50.0% to 94.4% of the rows), so no window trains on less than half of the data (SPLIT-14),
        and nine windows match the 3 x 3 folds a random split of this size gets (SPLIT-15). Each window holds 573 to 645
        readmissions within 30 days (10.4% to 11.7%). The encounter number runs as a calendar over 1999-2008 (curation
        notes), so the windows are later care, but they count stays, not days. No gap: the outcome horizon is a fixed 30
        days, and a 30-day gap before each window changed nothing measurable (untuned LightGBM over every stay, three
        windows of the newest half: 0.652 with, 0.654 without; SPLIT-10). A patient's earlier stays can train a window
        that tests their later ones (22% to 37% of the test stays, the most in the newest window), as when a hospital
        scores a returning patient (USE-10, SPLIT-13). The split stays temporal, not grouped: the cut is in time, and
        the test mixes returning and new patients as a hospital's next discharges do; holding returning patients out
        would test new patients only, which is not the use case. The windows cost little against random folds over every stay (LightGBM
        0.654 against 0.662; on the first stays 0.625 against 0.643). (2026-11-11, Andrej, review issue 1 d.)
    """
    temporal = Temporal(
        on="time_index",
        splits=TemporalSplits(window=5519, unit="rows", n_windows=9, min_train_fraction=0.5),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/diabetic_data.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Every stay, in encounter order; the encounter number runs as a calendar across all hospitals (curation
        # notes). It is 6n, or 6n + 2 after a change of the id scheme, so encounter_id // 6 is the running number.
        df = df.sort_values("encounter_id", kind="stable")
        df["time_index"] = df["encounter_id"] // 6
        # "we removed all encounters that resulted in either discharge to a hospice or patient death" (Sec. 2.3):
        # a patient who died cannot be readmitted (11 Expired, 19-21 Expired ... hospice; 13-14 Hospice)
        df = df[~df["discharge_disposition_id"].isin([11, 13, 14, 19, 20, 21])]
        # Drop identifier columns
        df = df.drop(columns=["encounter_id", "patient_nbr"])
        # Reverse ordinal encoding for ID-based features
        inverse_mappings = {
            "admission_type_id": {
                1: "Emergency",
                2: "Urgent",
                3: "Elective",
                4: "Newborn",
                5: "Not Available",
                6: "NULL",
                7: "Trauma Center",
                8: "Not Mapped",
            },
            "discharge_disposition_id": {
                1: "Discharged to home",
                2: "Discharged/transferred to another short term hospital",
                3: "Discharged/transferred to SNF",
                4: "Discharged/transferred to ICF",
                5: "Discharged/transferred to another type of inpatient care institution",
                6: "Discharged/transferred to home with home health service",
                7: "Left AMA",
                8: "Discharged/transferred to home under care of Home IV provider",
                9: "Admitted as an inpatient to this hospital",
                10: "Neonate discharged to another hospital for neonatal aftercare",
                11: "Expired",
                12: "Still patient or expected to return for outpatient services",
                13: "Hospice / home",
                14: "Hospice / medical facility",
                15: "Discharged/transferred within this institution to Medicare approved swing bed",
                16: "Discharged/transferred/referred another institution for outpatient services",
                17: "Discharged/transferred/referred to this institution for outpatient services",
                18: "NULL",
                19: "Expired at home. Medicaid only, hospice.",
                20: "Expired in a medical facility. Medicaid only, hospice.",
                21: "Expired, place unknown. Medicaid only, hospice.",
                22: "Discharged/transferred to another rehab fac including rehab units of a hospital .",
                23: "Discharged/transferred to a long term care hospital.",
                24: "Discharged/transferred to a nursing facility certified under Medicaid but not certified under Medicare.",
                25: "Not Mapped",
                26: "Unknown/Invalid",
                27: "Discharged/transferred to a federal health care facility.",
                28: "Discharged/transferred/referred to a psychiatric hospital of psychiatric distinct part unit of a hospital",
                29: "Discharged/transferred to a Critical Access Hospital (CAH).",
                30: "Discharged/transferred to another Type of Health Care Institution not Defined Elsewhere",
            },
            "admission_source_id": {
                1: "Physician Referral",
                2: "Clinic Referral",
                3: "HMO Referral",
                4: "Transfer from a hospital",
                5: "Transfer from a Skilled Nursing Facility (SNF)",
                6: "Transfer from another health care facility",
                7: "Emergency Room",
                8: "Court/Law Enforcement",
                9: "Not Available",
                10: "Transfer from critial access hospital",
                11: "Normal Delivery",
                12: "Premature Delivery",
                13: "Sick Baby",
                14: "Extramural Birth",
                15: "Not Available",
                17: "NULL",
                18: "Transfer From Another Home Health Agency",
                19: "Readmission to Same Home Health Agency",
                20: "Not Mapped",
                21: "Unknown/Invalid",
                22: "Transfer from hospital inpt/same fac reslt in a sep claim",
                23: "Born inside this hospital",
                24: "Born outside this hospital",
                25: "Transfer from Ambulatory Surgery Center",
                26: "Transfer from Hospice",
            },
        }
        for feature, inverse_map in inverse_mappings.items():
            df[feature] = df[feature].map(inverse_map)
        # Create binary target
        target_feature = "EarlyReadmission"
        df = df.rename(columns={"readmitted": target_feature})
        label_mask = df[target_feature] == "<30"
        df.loc[label_mask, target_feature] = "Yes"
        df.loc[~label_mask, target_feature] = "No"
        # "?" (race, weight, payer code, specialty, diagnoses) and "NULL" (the ID mappings) mean missing
        df = df.mask(df.isin(["?", "NULL"]))
        # Drop constant features
        df = df.drop(columns=["examide", "citoglipton", "glimepiride-pioglitazone"])
        # codes outside a scale that mean unknown, and states outside it placed as missing (CLEAN-10,
        # CLEAN-14): don't know, refused, not asked, other
        df = set_missing(
            df,
            {
                "metformin": ["No"],
                "repaglinide": ["No"],
                "nateglinide": ["No"],
                "chlorpropamide": ["No"],
                "glimepiride": ["No"],
                "glipizide": ["No"],
                "glyburide": ["No"],
                "pioglitazone": ["No"],
                "rosiglitazone": ["No"],
                "acarbose": ["No"],
                "miglitol": ["No"],
                "insulin": ["No"],
                "glyburide-metformin": ["No"],
            },
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "race",
                "gender",
                "age",
                "weight",
                "admission_type_id",
                "discharge_disposition_id",
                "admission_source_id",
                "payer_code",
                "medical_specialty",
                "diag_1",
                "diag_2",
                "diag_3",
                "max_glu_serum",
                "A1Cresult",
                "metformin",
                "repaglinide",
                "nateglinide",
                "chlorpropamide",
                "glimepiride",
                "acetohexamide",
                "glipizide",
                "glyburide",
                "tolbutamide",
                "pioglitazone",
                "rosiglitazone",
                "acarbose",
                "miglitol",
                "troglitazone",
                "tolazamide",
                "insulin",
                "glyburide-metformin",
                "glipizide-metformin",
                "metformin-rosiglitazone",
                "metformin-pioglitazone",
                "change",
                "diabetesMed",
            ],
        )
