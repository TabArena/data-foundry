"""Curated dataset definition for `diabetes_130_us` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary

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
}


class Diabetes130Us(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a diabetic patient be readmitted to hospital within 30 days of discharge?",
        use_case=(
            "For example, at discharge a hospital decides which diabetic patients get extra follow-up, such as a call"
            " or an early visit, to prevent an early readmission."
        ),
        row=(
            "The first hospital stay of one diabetic patient at one of 130 US hospitals, 1999-2008 (69,973 patients)."
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
            "Random patients, one stay each, so the test data stands for new patients of the same hospitals and years."
        ),
        changes=(
            "We keep each patient's first stay and drop stays that ended in death or discharge to a hospice, as the "
            "paper does."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is recorded by discharge and the outcome follows within 30 days, as when the "
            "model is used. The stays carry no dates, so the test data mixes care from all of 1999-2008."
        ),
    )

    # Dataset
    unique_name = "diabetes_130_us"
    year = "2014"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5230J"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/diabetes_130_us/ && wget -P local-data-warehouse/diabetes_130_us/ https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip && unzip local-data-warehouse/diabetes_130_us/diabetes+130-us+hospitals+for+years+1999-2008.zip -d local-data-warehouse/diabetes_130_us/
    """
    bibtex = """
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
    """
    curation_comments = """
        - We keep one encounter per patient, the first one by encounter_id, following the paper ("we considered only the first encounter for each patient as the primary admission", Strack et al. 2014, Sec. 2.3); we sort by encounter_id to make this explicit (each patient's encounters already appear in that order in the raw file, so the kept encounter is the same as before).
        - We remove encounters that ended in death or discharge to a hospice, as the paper does ("we removed all encounters that resulted in either discharge to a hospice or patient death, to avoid biasing our analysis", Sec. 2.3): a patient who died cannot be readmitted (the 1,084 "Expired" encounters were all "No"), so these rows are not part of the readmission task.
        - We set "?" (race, weight, payer code, specialty, diagnoses) and the "NULL" code of the three ID columns to missing values; pandas also reads the "None" (test not taken) of max_glu_serum and A1Cresult as missing.
        - We reversed the original ordinal encoding for three ID-based features (admission_type_id, discharge_disposition_id, admission_source_id).
        - We created the target from the "readmitted" column following the original task description: "<30" becomes "Yes", everything else "No".
        - We dropped "encounter_id" and "patient_nbr", which are both unique identifiers for each row.
        - The other codes for an unknown value ("Not Available" and "Not Mapped" in the ID columns, "Unknown/Invalid" in gender) stay as categories, as IDS_mapping.csv lists them as codes of their own next to "NULL".
        - We drop examide, citoglipton and glimepiride-pioglitazone, which are constant ("No") after the filters above.
        - Anomaly: There is a distribution shift based on the original order. The reason for this might be that the encounters are ordered in some way such that later parts of the data contain different sub-groups than earlier parts. This is also indicated by the fact that the "payer_code" feature is responsible for the shift. This distribution shift vanishes after randomly shuffling the data (as done by default for this and all other datasets used in TabArena).
        - Ordinal scales (2026-10-30, CLEAN-14): 4 columns typed as ordered categories in the order of the source's
          codebook (`ORDINAL_LEVELS`).
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

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/diabetic_data.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # One encounter per patient: the first one (Strack et al. 2014, Sec. 2.3)
        df = df.sort_values("encounter_id", kind="stable").drop_duplicates(subset="patient_nbr", keep="first")
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
