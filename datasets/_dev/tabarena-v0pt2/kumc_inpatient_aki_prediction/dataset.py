"""Curated dataset definition for `kumc_inpatient_aki_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    decode,
    drop_columns,
    set_missing,
)

# The published file (the source's Perspective #2: data up to the admission day, AKI on any day of the stay) and its
# dictionary. Column `X<i>` is the dictionary's attribute i + 1; `X1917` is the label (README.txt of the deposit).
DATA_FILE = "Perspective_scrb_2.csv"
DICTIONARY_FILE = "AKI_dataset_attributes_map.xlsx"

# The 22 attributes that are no yes/no flag, by their dictionary id (labs by the test's name).
BASE_NAMES = {
    "age": "age_band",
    "race": "race_code",
    "gender": "sex",
    "bmi": "bmi_band",
    "diastolic": "diastolic_bp_band",
    "systolic": "systolic_bp_band",
    "pulse": "pulse_band",
    "temp": "temperature_band",
}
LAB_NAMES = {
    "Albumin": "lab_albumin",
    "ALT": "lab_alt",
    "AST": "lab_ast",
    "Ammonia": "lab_ammonia",
    "Calcium": "lab_calcium",
    "BUN": "lab_bun",
    "TotalBilirubin": "lab_total_bilirubin",
    "CK-MB": "lab_ck_mb",
    "CK": "lab_ck",
    "Glucose": "lab_glucose",
    "Lipase": "lab_lipase",
    "Platelets": "lab_platelets",
    "TroponinI": "lab_troponin_i",
    "WBC": "lab_wbc",
}
# Names fixed by hand: the dictionary's typo, a lost ">", and a flag that mostly means "no comorbidity" (notes).
RENAMES = {
    "comorbidity_coagulopthy": "comorbidity_coagulopathy",
    "admission_drg_head_trauma_w_coma_1_hr": "admission_drg_head_trauma_w_coma_over_1_hr",
    "comorbidity_diabetes_w_ccs": "comorbidity_diabetes_w_ccs_or_none",
}
VITAL_COLUMNS = ["bmi_band", "diastolic_bp_band", "systolic_bp_band", "pulse_band", "temperature_band"]
# Labs: "present and normal", "present and abnormal" or "unknown" (paper, Methods); which code is which is read from
# the data (curation notes, Decisions): 0 is the unknown state, 1 normal, 2 abnormal.
LAB_LABELS = {1: "normal", 2: "abnormal"}
# Sex, read from sex-specific diagnoses without exception (curation notes).
SEX_LABELS = {1: "female", 2: "male"}
# Six age bands, youngest first; the edges are inferred from the authors' earlier study (curation notes).
AGE_LABELS = {1: "18-25", 2: "26-35", 3: "36-45", 4: "46-55", 5: "56-64", 6: "65+"}
# The flag blocks of the dictionary, by id prefix: the stay's base APR-DRG and comorbidities (UHC discharge abstract),
# and the medical history (ICD-9 codes up to the admission day grouped by AHRQ CCS).
FLAG_PREFIXES = {"DRG": "admission_drg_", "COM": "comorbidity_", "CCS": "history_ccs"}
MAX_NAME = 64

# Dropped as known only after the prediction point (curation notes, LEAK-10): the comorbidity that in part records
# this stay's AKI, and the base APR-DRG groups defined by a procedure done in the stay.
RENAL_FAILURE = "comorbidity_renal_failure"
OR_PROCEDURE_GROUPS = [  # operating-room groups; 710 is `infect_parasitic_disease`, 443 `kidney_urin_tract_nonmalig`
    "craniotomy_exc_for_trauma",
    "cardiac_valve_proc_w_0_cath",
    "coronary_bypass_w_card_cath",
    "cor_bypass_w_o_card_cath",
    "other_vascular_procedures",
    "maj_stom_esoph_duod_proc",
    "maj_small_large_bowel_proc",
    "hernia_proc_exc_inguinal_fem",
    "maj_pancreas_liver_shunt_proc",
    "hip_joint_replacement",
    "knee_joint_replacement",
    "dor_lumb_fus_exc_crv_bck",
    "hip_femur_proc_traum",
    "intervertebral_disc_excision",
    "knee_lower_leg_proc",
    "shoulder_up_arm_forearm_proc",
    "uter_adnex_exc_leiomyoma",
    "infect_parasitic_disease",
    "post_op_trauma_infect_proc",
    "o_r_proc_oth_comp_treat",
    "kidney_urin_tract_nonmalig",
]
OTHER_PROCEDURE_GROUPS = [  # non-operating-room procedure groups
    "bone_marrow_transplant",
    "percut_cardiovasc_proc_w_ami",
    "percut_cardiovasc_w_o_ami",
    "card_cathet_exc_ischemia",
    "card_cathet_w_ischemia",
]
PROCEDURE_GROUPS = [FLAG_PREFIXES["DRG"] + g for g in OR_PROCEDURE_GROUPS + OTHER_PROCEDURE_GROUPS]

# Diagnoses that imply an abnormal value of a lab (the review panel's claim audit), evidence for the lab decoding.
LAB_DIAGNOSIS_PAIRS = [
    ("lab_lipase", "admission_drg_pancreas_disord_exc_malig"),
    ("lab_troponin_i", "admission_drg_percut_cardiovasc_proc_w_ami"),
    ("lab_troponin_i", "admission_drg_card_cathet_w_ischemia"),
    ("lab_ammonia", "admission_drg_hepatic_coma_oth_maj_liv_dis"),
    ("lab_platelets", "admission_drg_bone_marrow_transplant"),
    ("lab_platelets", "comorbidity_coagulopathy"),
    ("lab_wbc", "admission_drg_septicemia_dissem_infect"),
    ("lab_glucose", "admission_drg_diabetes"),
    ("lab_albumin", "comorbidity_liver_disease"),
    ("lab_albumin", "comorbidity_weight_loss"),
    ("lab_alt", "admission_drg_other_disorders_of_liver"),
    ("lab_ast", "admission_drg_hepatic_coma_oth_maj_liv_dis"),
    ("lab_total_bilirubin", "admission_drg_disorders_of_gallbladder"),
    ("lab_total_bilirubin", "admission_drg_hepatic_coma_oth_maj_liv_dis"),
    ("lab_bun", "comorbidity_congestive_heart_failure"),
    ("lab_calcium", "comorbidity_metastatic_cancer"),
    ("lab_ck", "admission_drg_head_trauma_w_coma_over_1_hr"),
    ("lab_ck_mb", "admission_drg_percut_cardiovasc_proc_w_ami"),
]


def _slug(text: str) -> str:
    """Lower-case snake case of a dictionary name, without the CCS phrase "except that caused by ...", cut to
    `MAX_NAME` characters at an underscore.
    """
    text = re.sub(r"\(?except that caused by.*$", "", text, flags=re.IGNORECASE)
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    if len(slug) > MAX_NAME:
        slug = slug[:MAX_NAME].rsplit("_", 1)[0]
    return slug


def column_names(dictionary: pd.DataFrame) -> dict[str, str]:
    """`X<i>` -> a readable name, from the deposit's dictionary (Attribute_ID, ID, Name, States)."""
    names = {}
    for attribute_id, code, name in dictionary[["Attribute_ID", "ID", "Name"]].itertuples(index=False):
        column = f"X{int(attribute_id) - 1}"
        prefix = re.sub(r"\d+$", "", str(code))
        if code in BASE_NAMES:
            names[column] = BASE_NAMES[code]
        elif prefix == "lab":
            names[column] = LAB_NAMES[str(name).split(":")[0]]
        elif prefix == "CCS":
            ccs_code, label = str(name).split("|", 1)
            names[column] = f"{FLAG_PREFIXES['CCS']}{ccs_code}_{_slug(label)}"
        elif prefix in FLAG_PREFIXES:
            names[column] = FLAG_PREFIXES[prefix] + _slug(str(name))
        elif code == "Class":
            names[column] = "aki_during_stay"
    return {column: RENAMES.get(name, name) for column, name in names.items()}


def lab_reference_ranges(dictionary: pd.DataFrame) -> dict[str, str]:
    """Lab column -> the reference range the dictionary gives with the test's name ("Albumin:3.5-5.5")."""
    labs = dictionary[dictionary["ID"].astype(str).str.match(r"lab\d+$")]
    return {LAB_NAMES[str(name).split(":")[0]]: str(name).split(":", 1)[1] for name in labs["Name"]}


class KumcInpatientAkiPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will an adult admitted to hospital develop acute kidney injury during the stay, judged on the day of "
            "admission?"
        ),
        use_case=(
            "On the day of admission, the team of an academic hospital flags the patients at risk of acquiring acute "
            "kidney injury in hospital, to decide on preventive care for them, such as sparing kidney-toxic drugs and "
            "checking creatinine more often."
        ),
        row=(
            "One hospital stay of 2 days or more of an adult at the University of Kansas Health System, November 2007 "
            "to December 2016 (76,957 stays), without signs of reduced kidney function in the first 24 hours."
        ),
        predicted=(
            "Whether the creatinine rises far enough for acute kidney injury by the KDIGO criteria on any day up to "
            "discharge, however long the stay; 9.4% of the stays do."
        ),
        known=(
            "Age band, sex, race, banded vital signs and whether 14 lab tests were normal, abnormal or not done (the "
            "last values up to the admission day), 192 groups of diagnoses recorded up to the admission day, and, "
            "from the hospital's discharge abstract, 26 comorbidities and the stay's diagnosis group for 35 frequent "
            "medical groups, all as yes/no flags."
        ),
        split=(
            "Random stays, so the test data stands for new admissions of the same hospital and years. The file has no "
            "dates and no patient key, so one patient's repeat stays can fall on both sides."
        ),
        changes=(
            "We decode the lab codes into normal and abnormal and the sex codes into female and male, set the codes "
            "for a test or vital sign not taken to missing, and drop 27 columns of the discharge abstract a team does "
            "not have at admission: a comorbidity that in part records this stay's kidney injury, and the 26 "
            "diagnosis groups defined by a procedure done in the stay."
        ),
        fit="approximate",
        fit_reason=(
            "The source built this exact admission-day task, but the public file has no medications, rare flags or "
            "admission creatinine, and the cohort is cut on facts known only after admission: a stay of 2+ days, 2+ "
            "creatinine values, normal creatinine and eGFR over the first 24 hours. Comorbidities and medical "
            "diagnosis groups from the discharge abstract are kept with a note; the procedure groups are dropped."
        ),
    )

    # Dataset
    unique_name = "kumc_inpatient_aki_prediction"
    year = "2018"
    domain = "medical & healthcare"
    source = "Other"  # the authors' Dryad deposit, published with the JAMIA Open paper
    source_url = "https://doi.org/10.5061/dryad.qc90qb4"
    license = "CC0 1.0"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        The Dryad deposit of He et al. (2018), doi:10.5061/dryad.qc90qb4, CC0 (one version, 2018-11-16). Dryad's per-file API answers 401 without a token, but the version download of its API redirects without a token to a zip of the version; the MD5 digests of the two files equal those Dryad lists (checked 2026-11-08).
        mkdir -p local-data-warehouse/kumc_inpatient_aki_prediction && cd local-data-warehouse/kumc_inpatient_aki_prediction
        curl -L -o dryad_qc90qb4_v20181116.zip https://datadryad.org/api/v2/versions/23022/download
        unzip dryad_qc90qb4_v20181116.zip  # AKI_Prediction_Scrubbed_EMR.zip, README_for_AKI_Prediction_Scrubbed_EMR.txt
        md5sum AKI_Prediction_Scrubbed_EMR.zip  # ba97b2ffce83868c421e7ac187dbd013
        unzip AKI_Prediction_Scrubbed_EMR.zip  # Perspective_scrb_1.csv to _4.csv, AKI_dataset_attributes_map.xlsx, README.txt
        sha256sum Perspective_scrb_2.csv  # 39cdf824d825f23e51d9afdc98675635d991bf3c1628365a655b8f6aafdb471a
        sha256sum AKI_dataset_attributes_map.xlsx  # 0e0f253344227ffe0ebecf84caf0a75f304d006197b6aa20c91aa94fdb19042a
    """
    bibtex = r"""
        @article{he2019multiperspective,
          title = {Multi-perspective predictive modeling for acute kidney injury in general hospital populations using electronic medical records},
          author = {He, Jianqin and Hu, Yong and Zhang, Xiangzhou and Wu, Lijuan and Waitman, Lemuel R. and Liu, Mei},
          journal = {JAMIA Open},
          volume = {2},
          number = {1},
          pages = {115--122},
          year = {2019},
          doi = {10.1093/jamiaopen/ooy043},
          note = {Published online 2018-11-15. Data: \url{https://doi.org/10.5061/dryad.qc90qb4}, CC0}
        }
    """
    curation_comments = """
        We start with `Perspective_scrb_2.csv` (76,957 stays, 302 coded attributes and the label) and its dictionary `AKI_dataset_attributes_map.xlsx`, from the Dryad deposit of He et al. (2018), version of 2018-11-16, and ship 275 of the attributes as features.

        - Prediction point: the day of admission, the source's Perspective #2: "use admission day as the prediction point, predicting if a patient will develop AKI during their stay ... the data collection window becomes (past, admission) and the prediction window becomes (admission, discharge). This aligns with a clinical application scenario in which clinicians can use the models to make AKI risk prediction for everyone at admission and make subsequent treatment decisions" (Methods, "Experiment design"). Labs and vitals are "the last recorded value before a prediction point"; the medical history is ICD-9 diagnoses time-stamped before it; "Comorbidities, admission diagnosis, and demographics were presumed to be available at admission and not time dependent" (Methods, "Data collection").
        - The public file is a cut of the study data: "Our de-identified dataset contain total 1287 variables. However, to anonymize the dataset for public sharing, we further scrubbed the de-identified dataset by removing variables. ... Our institutional IRB requires a signed data use agreement" for the full set (README.txt). Of the dictionary's 1,917 attributes this file keeps 302: demographics, vitals and labs (22), 61 admission diagnoses, 27 comorbidities and 192 history groups, and no medication; every kept flag is set in at least 398 stays, so the rare ones were removed. We use the public file only.
        - Target: `aki_during_stay` (`X1917`, "AKI_label"), "Yes" for the 7,259 stays (9.4%) with acute kidney injury by the KDIGO creatinine criteria, a rise of 0.3 mg/dL within 48 hours or to 1.5 times the baseline within 7 days (the criteria as quoted in Cheng et al. 2017, the authors' earlier study); the baseline is "the last measurement within 2-day time window prior to hospital admission or the first SCr measured after hospital admission", and every creatinine up to discharge counts (Methods, "Study population"). Creatinine and eGFR are not features ("SCr and eGFR were not included as predictive variables"), so the admission creatinine a team has is missing. The counts equal the paper's (7,259 and 69,698).
        - The other files of the deposit are other prediction points, not used: Perspective #1 anchors the data one day before the onset of AKI, a point "not available in a real-life clinical application" (Methods, "Relations between perspectives"); Perspective #3 is this file with the label cut to AKI within one day of admission (1,611 stays, the later cases counted as no AKI); Perspective #4 is the next-day risk one day after admission (72,846 stays).
        - Renamed the `X<i>` columns from the dictionary: the 22 measured attributes by hand, the flags as `admission_drg_`, `comorbidity_` and `history_ccs<code>_` with the dictionary's name (`column_names`); three names fixed by hand: `comorbidity_coagulopathy` (the dictionary's "Coagulopthy"), `admission_drg_head_trauma_w_coma_over_1_hr` ("HEAD TRAUMA W COMA >1 HR") and `comorbidity_diabetes_w_ccs_or_none` (below).
        - Labs (`lab_*`, 14): the paper codes each as "present and normal", "present and abnormal" or "unknown"; the dictionary gives each test's reference range ("Albumin:3.5–5.5", "Glucose:80–160", "TroponinI:0–0.06") and the states 0, 1, 2, but not which state is which. Read from the data without the target (Decisions): code 0 is the unknown state, 97% of the stays for ammonia and 72% for troponin I, tests run on few patients, against 6% for platelets; code 1 is normal, the majority of the measured values in all 14 tests (78% of measured platelets, 80% of glucose with its wide 80-160 range); code 2 is abnormal, far more common in 16 of 18 diagnoses that imply an abnormal value than in the other stays (lipase in pancreatitis 30.9% against 1.4%, troponin I in a heart attack treated by PCI 95.0% against 12.7%, glucose in a diabetes admission 87.8% against 19.1%). As a check only, code 2 has the higher AKI rate in 12 of 14 tests. Code 0 is set to missing (CLEAN-10; the source kept "unknown" because "information may be contained in the choice to not perform the measurement", which a missing value keeps), 1 and 2 decoded to `normal` and `abnormal` (CLEAN-12).
        - Vitals (`*_band`, 5): banded as in the earlier study (Cheng et al. 2017, Table 2: BMI <18.5, 18.5-24.9, 25-29.9, >=30; diastolic <80, 80-89, 90-99, >=100; systolic <120, 120-139, 140-159, >=160; pulse <50, 50-65, 66-80, 81-100, >100; temperature <95.0, 95.0-97.6, 97.7-99.5, 99.5-104.0, >104.0 °F; each with an unknown state). Code 0 is the unknown state (75 stays in blood pressure and pulse, 123 in temperature, 72 of them in all four; 5,111 in BMI) and is set to missing; the other codes ship as integers. Which code is which band is not documented. For BMI and blood pressure the data agrees with the table's order without the target: 92% of the stays with the obesity comorbidity are in BMI code 4 (37% of all), 20.7% of those with weight loss in code 1 (3.3% of all); the diastolic shares 71.8/19.5/7.1/1.4% fit the four bands; hypertension shifts systolic stays to codes 3-4 (28.9% against 21.3%). For pulse and temperature the counts contradict the table's order (pulse code 1 holds 16% of the stays, where the first band is under 50 beats per minute; temperature code 2 holds 80%, where the second band is 95.0-97.6 °F). All five stay unordered codes (CLEAN-14).
        - `age_band`: six bands, an ordered category labelled 18-25, 26-35, 36-45, 46-55, 56-64 and 65+, the edges inferred: the authors' earlier study at the same hospital (Cheng et al. 2017, Table 3) bands its 18- to 64-year-olds this way, and the shares of codes 1-5 among them (8.8/14.1/16.8/28.1/32.2%) match its 8.5/14.6/17.3/28.9/30.7% within 1.5 points; code 6 is then 65 and older (this cohort has no upper age). The order rests on facts without the target (CLEAN-14): the counts rise with the code (4,953 to 20,789), as an adult inpatient population does with age, and stays with a pregnancy or delivery in the history fall from 4.3% in codes 1 and 2 to 0.9% in code 3, 2 of 33,882 stays in codes 4 and 5, and none in code 6.
        - `sex`: decoded 1 `female`, 2 `male`, read from sex-specific diagnoses without exception: all 1,553 stays with prostate hyperplasia in the history are code 2, all 413 operations on the uterus and adnexa code 1 (CLEAN-12).
        - `race_code`: four codes without words in the deposit. The earlier study lists White, African American, Asian and Other (Cheng et al. 2017, Table 3), and the code shares 76.1/13.5/0.8/9.5% follow that order within 3 points (73.4/15.2/0.9/10.5%); kept as codes, the mapping being inferred (CLEAN-12).
        - The 253 flags are 0/1 categories (CLEAN-14).
        - `comorbidity_diabetes_w_ccs_or_none` (the dictionary's "Diabetes w/CCs") is set in 14,107 stays, 11,759 (83%) of them with no other comorbidity, and in 99.5% of the stays with no other comorbidity. Those 11,759 look nothing like diabetes (2.4% have an earlier diabetes record, against 64% of the other 2,348; 5.1% AKI). The deposit seems to store "no comorbidity" in this flag; a diabetic stay with no other comorbidity cannot be told from a stay with none, so the column ships as it is, renamed.
        - Dropped as known only after the prediction point (LEAK-10): the comorbidities and the admission diagnosis come from the University HealthSystem Consortium (now Vizient) data of the stay, a discharge abstract with no present-on-admission flag in the deposit. The source "presumed" both "to be available at admission"; its authors' earlier paper calls these data "well adjudicated, but not immediately available" (Cheng et al. 2017, Limitations). Untuned LightGBM, 5-fold ROC AUC on the 302 features: 0.7234.
          - `comorbidity_renal_failure`, in part a code for this stay's AKI (a consequence of the target; LEAK-6): in a cohort with normal kidney function on admission, the 881 flagged stays with no earlier record of chronic kidney disease (CCS 158) have 28.8% AKI, against 16.6% for the 899 flagged stays with one (z 6.2; 9.1% without the flag). Dropping it costs 0.0024 (5 of 5 folds).
          - The 26 base APR-DRG groups defined by a procedure done in the stay: 21 operating-room groups (coronary bypass 27% AKI, valve surgery 22%, bowel surgery 15%, joint replacements; `infect_parasitic_disease` is APR-DRG 710, infectious diseases with an operation, 31.3% AKI, and `kidney_urin_tract_nonmalig` is APR-DRG 443, kidney and urinary tract procedures, 18.9%, both read from the dictionary's APR-DRG order) and five other procedure groups (PCI with and without a heart attack, cardiac catheterisation with and without ischaemia, bone marrow transplant). An operation decided during an emergency stay is not known at admission, and the file cannot tell elective from emergency stays, so the late part cannot be located row by row. Dropping 25 of them costs 0.7234 to 0.7083; after the renal flag and the first 20 operating-room groups, APR-DRG 443 is worth +0.0029 and the five other groups +0.0041 (10 of 10 folds each, 5 folds x 2 seeds).
        - Potential leak, kept on purpose: the 35 remaining APR-DRG groups (medical groups, set at discharge from the principal diagnosis "after study") and the 26 remaining comorbidities come from the same discharge abstract. Where a late part can be traced it shows no gain (LEAK-10, second clause): for each comorbidity that can arise in a stay, the flagged stays with no matching record up to the admission day have the AKI rate of the flagged stays with one (fluid and electrolyte disorders +0.6 points, coagulopathy +0.6, weight loss 0.0, deficiency anaemias +0.5, chronic blood loss anaemia -2.4, pulmonary circulation disease +1.7; all with z below 1, and within the spread of 15 chronic comorbidities that cannot arise in a stay, against renal failure's +12.3), and for 19 medical groups a diagnosis missing from the admission-day record changes the AKI rate by +0.4 points (z 0.8). The rest is kept on the source's presumption. Untuned LightGBM, ROC AUC on the 275 shipped features (5 folds x 2 seeds): 0.705; 0.694 without the medical groups, 0.693 without the comorbidities, 0.681 without both; dropping only the six comorbidities that can arise in a stay costs 0.005 (0.700, 10 of 10 folds), and these six with the medical groups 0.017 (0.689). Revisit if Vizient's present-on-admission flags or coding dates can be had.
        - Note: the history holds diagnoses recorded up to the admission day, not the codes of this stay's discharge. The later cut of Perspective #1 adds 55,819 flags and removes none, so the block is cut by date; "acute and unspecified renal failure" (CCS 157) is flagged in 9.1% of the AKI stays and 5.3% of the others, where the stay's own billing codes would flag a large share of the coded AKI stays. The stay's own diagnosis is in it for 44-76% of acute medical admissions (pulmonary embolism 68%), recorded on the admission day, against 9-18% of trauma stays. The history maps ICD-9 codes to CCS groups; the stays after the switch to ICD-10 in October 2015 may have a thinner history.
        - Selection, from the source: adults with a stay of at least 2 days and at least two creatinine values, excluding stays with eGFR below 60 or creatinine above 1.3 mg/dL within 24 hours of admission; of 179,370 stays of 96,590 patients, 76,957 (42.9%) remain (Methods). The length of stay, the second creatinine and the 24-hour values come after the prediction point, so a team at admission meets a wider population, with the short and the unmonitored stays (`Selection Bias`, named in the fit).
        - Duplicates kept (LEAK-18): 316 stays fall in 150 groups identical in all 275 features (166 copies beyond the first, 0.2%), 16 groups with both labels. Most are sparse profiles (median 1 flag set of 253, against 8 over all stays), distinct stays coded the same on coarse bands.
        - The split is forced (ForcedIIDFromTemporal, SPLIT-8): a hospital would train on earlier years and score new admissions, but the file has no dates (2007-2016, across the switch from ICD-9 to ICD-10) and no patient key, and the order of the rows within each label block is unrelated to the features (ROC AUC 0.52 and 0.50 for the first against the second half), so it ships as random stays. Against a dated split the score is likely optimistic by an unknown amount (nine years of practice and coding change); a dated release, which the full set behind the authors' data use agreement may be, should be split by time. The raw file lists the 7,259 AKI stays first; the base class shuffles.
        - Repeat stays of one patient fall on both sides (SPLIT-29): the paper's 179,370 stays of 96,590 patients imply that 44-61% of the kept stays share a patient with another kept stay, and 16.6% of the rows have a likely stay of the same patient in the data (same sex and race, age band within one, at least 4 history flags, 80% of the history and comorbidity flags alike; 23 times the rate across sexes). Removing each test stay's likely twins from training costs untuned LightGBM 0.0015 ROC AUC (0.019 on the 13% of test stays that have one), a deep random forest 0.008 and logistic regression 0.0003, against random removals; the order of the models does not change. Under the dated split the use case implies, a returning patient's earlier stays would be in training anyway (SPLIT-13), so about half of this is legitimate.
    """

    # Task
    target = "aki_during_stay"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The paper (He et al. 2019, Methods, 'Experimental methodology') reports AUC, sensitivity, specificity, "
            "precision and F-measure side by side, with the threshold picked per model for the best F-measure. AUC "
            "is its headline (abstract and conclusion) and the measure it ranks the prediction windows of "
            "Perspective #3 by, but it compares the models on AUC and F-measure together, and a headline number is "
            "not by itself a deliberate choice (MET-5); there is no fixed threshold (MET-6, MET-8). The Dryad "
            "deposit names no metric."
        )
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "data": pd.read_csv(raw_dir / DATA_FILE),
            "dictionary": pd.read_excel(raw_dir / DICTIONARY_FILE, engine="openpyxl"),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw["data"]
        names = column_names(raw["dictionary"])
        assert set(df.columns) <= set(names), sorted(set(df.columns) - set(names))
        df = df.rename(columns=names)
        assert df.columns.is_unique
        # Known only after the prediction point: a code of this stay's AKI and the procedure groups (LEAK-10; notes).
        df = drop_columns(df, [RENAL_FAILURE, *PROCEDURE_GROUPS])
        # The label in words (CLEAN-25): "Yes" is a stay with AKI.
        df = decode(df, {self.target: {0: "No", 1: "Yes"}})
        # Labs and vitals: code 0 is the unknown state (not measured), set to missing (CLEAN-10).
        labs = [c for c in df.columns if c.startswith("lab_")]
        df = set_missing(df, {key: [0] for key in labs + VITAL_COLUMNS})
        df[VITAL_COLUMNS] = df[VITAL_COLUMNS].astype("Int64")
        # Labs: 1 present and normal, 2 present and abnormal; sex and age bands in words (read from the data; notes).
        df = decode(df, {**dict.fromkeys(labs, LAB_LABELS), "sex": SEX_LABELS, "age_band": AGE_LABELS})
        # Duplicate rows stay: mostly sparse profiles of distinct stays (curation notes, LEAK-18).
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        flags = [c for c in df.columns if c.startswith(tuple(FLAG_PREFIXES.values()))]
        labs = [c for c in df.columns if c.startswith("lab_")]
        return FeatureTypes(
            ordinal={"age_band": list(AGE_LABELS.values())},
            categorical=["race_code", "sex", *VITAL_COLUMNS, *labs, *flags],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        data = raw["data"].rename(columns=column_names(raw["dictionary"]))
        y = data["aki_during_stay"]
        ranges = lab_reference_ranges(raw["dictionary"])
        rows = []
        for col in [c for c in data.columns if c.startswith("lab_")]:
            share = data[col].value_counts(normalize=True)
            rate = y.groupby(data[col]).mean()
            rows.append(
                {
                    "lab": col,
                    "reference range (dictionary)": ranges[col],
                    "code 0 share": round(share.get(0, 0.0), 3),
                    "code 1 share of measured": round(share.get(1, 0.0) / (1 - share.get(0, 0.0)), 3),
                    "check: AKI rate, code 1": round(rate.get(1, float("nan")), 3),
                    "check: AKI rate, code 2": round(rate.get(2, float("nan")), 3),
                }
            )
        labs = pd.DataFrame(rows).set_index("lab")
        pairs = []
        for lab, diagnosis in LAB_DIAGNOSIS_PAIRS:
            measured = data[lab] != 0
            flagged = data[diagnosis] == 1
            code2 = data[lab] == 2
            pairs.append(
                {
                    "lab": lab,
                    "diagnosis": diagnosis,
                    "measured stays with it": int((measured & flagged).sum()),
                    "code 2 share, with it": round(code2[measured & flagged].mean(), 3),
                    "code 2 share, others": round(code2[measured & ~flagged].mean(), 3),
                }
            )
        return [
            Decision(
                title="Lab codes: 0 unknown, 1 normal, 2 abnormal",
                why=(
                    "The deposit's dictionary gives each test's reference range and the states 0, 1, 2, and the paper "
                    "the words 'unknown', 'present and normal' and 'present and abnormal', without saying which code "
                    "is which. Without the target: code 0 is largest for the tests run on few patients (ammonia, "
                    "troponin I, CK-MB), and code 1 is the majority of the measured values in every test, as values "
                    "inside a reference range are. The AKI rates are a check only: code 2 has the higher rate in all "
                    "but lipase and ammonia."
                ),
                evidence=labs,
            ),
            Decision(
                title="Lab code 2 is abnormal: diagnoses that imply an abnormal value",
                why=(
                    "In stays whose diagnosis implies an abnormal value of a test (lipase in pancreatitis, troponin I "
                    "in a heart attack, glucose in a diabetes admission), code 2 is far more common among the measured "
                    "values than in the other stays, in 16 of 18 pairs. The two exceptions are catheterisation for "
                    "ischaemia without a heart attack (troponin I) and CK in head trauma, measured in 14 stays."
                ),
                evidence=pd.DataFrame(pairs).set_index(["lab", "diagnosis"]),
            ),
        ]
