"""Curated dataset definition for `nchs_linked_birth_infant_death_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

# The birth cohorts we read, one NCHS zip each ("<cohort + 1>PE<cohort>CO.zip": the cohort's births and the linked
# infant deaths of the cohort year and the next). 2017 is the first cohort of the combined period/cohort format.
COHORTS = (2017, 2018, 2019, 2020, 2021, 2022, 2023)
PREPARED = "nchs_linked_cohorts_2017_2023.parquet"
DENOMINATOR_WIDTH = 1346  # record length of the births ("denominator") file
NUMERATOR_WIDTH = 1743  # record length of the linked infant deaths ("numerator") file

# Items read from the births file, by their 1-based positions in the record layout of the 2024 period / 2023 cohort
# user guide (the same positions in the guides of 2018/2017 to 2023/2022). Read as published, codes as text.
BIRTH_ITEMS = {
    "DOB_YY": (9, 12), "DOB_MM": (13, 14), "DOB_TT": (19, 22), "DOB_WK": (23, 23), "BFACIL": (32, 32),
    "MAGEIMP": (73, 73), "MAGER": (75, 76), "MBSTATE_REC": (84, 84), "RESTATUS": (104, 104), "MRACE15": (108, 109),
    "MRACEIMP": (111, 111), "MHISP_R": (115, 115), "F_MHISP": (116, 116), "MAR_P": (119, 119), "DMAR": (120, 120),
    "MAR_IMP": (121, 121), "F_MAR_P": (123, 123), "MEDUC": (124, 124), "F_MEDUC": (126, 126), "FAGECOMB": (147, 148),
    "FRACE15": (154, 155), "FHISP_R": (160, 160), "F_FHISP": (161, 161), "FEDUC": (163, 163), "F_FEDUC": (165, 165),
    "PRIORLIVE": (171, 172), "PRIORDEAD": (173, 174), "PRIORTERM": (175, 176), "ILLB_R": (198, 200),
    "ILOO_R": (206, 208), "PRECARE": (224, 225), "F_MPCB": (226, 226), "PREVIS": (238, 239), "F_TPCV": (244, 244),
    "WIC": (251, 251), "F_WIC": (252, 252), "CIG_0": (253, 254), "CIG_1": (255, 256), "CIG_2": (257, 258),
    "CIG_3": (259, 260), "F_CIGS_0": (265, 265), "F_CIGS_1": (266, 266), "F_CIGS_2": (267, 267),
    "F_CIGS_3": (268, 268), "MHTR": (280, 281), "F_M_HT": (282, 282), "BMI": (283, 286), "PWGT_R": (292, 294),
    "F_PWGT": (295, 295), "DWGT_R": (299, 301), "F_DWGT": (303, 303), "WTGAIN": (304, 305),
    "RF_PDIAB": (313, 313), "RF_GDIAB": (314, 314), "RF_PHYPE": (315, 315), "RF_GHYPE": (316, 316),
    "RF_EHYPE": (317, 317), "RF_PPB": (318, 318), "F_RF_PDIAB": (319, 319), "F_RF_GDIAB": (320, 320),
    "F_RF_PHYPE": (321, 321), "F_RF_GHYPE": (322, 322), "F_RF_EHYPE": (323, 323), "F_RF_PPB": (324, 324),
    "RF_INFT": (325, 325), "RF_DRG": (326, 326), "RF_ART": (327, 327), "F_RF_INFT": (328, 328),
    "F_RF_DRG": (329, 329), "F_RF_ART": (330, 330), "RF_CESAR": (331, 331), "RF_CESARN": (332, 333),
    "F_RF_CESAR": (335, 335), "F_RF_NCESAR": (336, 336), "IP_GON": (343, 343), "IP_SYPH": (344, 344),
    "IP_CHLAM": (345, 345), "IP_HEPB": (346, 346), "IP_HEPC": (347, 347), "F_IP_GON": (348, 348),
    "F_IP_SYPH": (349, 349), "F_IP_CHLAM": (350, 350), "F_IP_HEPB": (351, 351), "F_IP_HEPC": (352, 352),
    "OB_SUCC": (360, 360), "OB_FAIL": (361, 361), "F_OB_SUCC": (363, 363), "F_OB_FAIL": (364, 364),
    "CO_SEQNUM": (365, 371), "CO_YOD": (372, 375), "LD_INDL": (383, 383), "LD_AUGM": (384, 384),
    "LD_STER": (385, 385), "LD_ANTB": (386, 386), "LD_CHOR": (387, 387), "LD_ANES": (388, 388),
    "F_LD_INDL": (389, 389), "F_LD_AUGM": (390, 390), "F_LD_STER": (391, 391), "F_LD_ANTB": (392, 392),
    "F_LD_CHOR": (393, 393), "F_LD_ANES": (394, 394), "ME_PRES": (401, 401), "ME_ROUT": (402, 402),
    "ME_TRIAL": (403, 403), "F_ME_PRES": (404, 404), "F_ME_ROUT": (405, 405), "F_ME_TRIAL": (406, 406),
    "MM_MTR": (415, 415), "MM_PLAC": (416, 416), "MM_RUPT": (417, 417), "MM_UHYST": (418, 418), "MM_AICU": (419, 419),
    "F_MM_MTR": (421, 421), "F_MM_PLAC": (422, 422), "F_MM_RUPT": (423, 423), "F_MM_UHYST": (424, 424),
    "F_MM_AICU": (425, 425), "ATTEND": (433, 433), "MTRAN": (434, 434), "PAY": (435, 435), "PAY_REC": (436, 436),
    "F_PAY": (437, 437), "F_PAY_REC": (438, 438), "APGAR5": (444, 445), "F_APGAR5": (447, 447),
    "APGAR10": (448, 449), "DPLURAL": (454, 454), "IMP_PLUR": (456, 456), "SETORDER_R": (459, 459),
    "SEX": (475, 475), "IMP_SEX": (476, 476), "COMBGST_IMP": (488, 488), "OBGEST_FLG": (489, 489),
    "COMBGEST": (490, 491), "LMPUSED": (498, 498), "OEGEST_COMB": (499, 500), "BRTHWGT": (512, 515),
    "BWTIMP": (516, 516), "AB_AVEN1": (517, 517), "AB_AVEN6": (518, 518), "AB_NICU": (519, 519),
    "AB_SURF": (520, 520), "AB_ANTI": (521, 521), "AB_SEIZ": (522, 522), "CA_ANEN": (537, 537),
    "CA_MNSB": (538, 538), "CA_CCHD": (539, 539), "CA_CDH": (540, 540), "CA_OMPH": (541, 541), "CA_GAST": (542, 542),
    "F_CA_ANEN": (543, 543), "F_CA_MNSB": (544, 544), "F_CA_CCHD": (545, 545), "F_CA_CDH": (546, 546),
    "F_CA_OMPH": (547, 547), "F_CA_GAST": (548, 548), "CA_LIMB": (549, 549), "CA_CLEFT": (550, 550),
    "CA_CLPAL": (551, 551), "CA_DOWN": (552, 552), "CA_DISOR": (553, 553), "CA_HYPO": (554, 554),
    "F_CA_LIMB": (555, 555), "F_CA_CLEFT": (556, 556), "F_CA_CLPAL": (557, 557), "F_CA_DOWN": (558, 558),
    "F_CA_DISOR": (559, 559), "F_CA_HYPO": (560, 560), "ITRAN": (567, 567), "ILIVE": (568, 568), "BFED": (569, 569),
    "FLGND": (1346, 1346),
}  # fmt: skip
# Items read from the linked infant deaths file: the keys of the user guide's "User Created Cohort File" join and the
# age at death (read for the evidence of the notes only, never a feature).
DEATH_ITEMS = {
    "DOB_YY": (9, 12), "RESTATUS": (104, 104), "CO_SEQNUM": (365, 371), "CO_YOD": (372, 375), "AGEDX": (1356, 1358),
    "AGER5X": (1359, 1359),
}  # fmt: skip

TARGET = "infant_death"

# The checkbox items (Y yes, N no, U unknown), renamed to English.
CHECKBOXES = {
    "WIC": "wic_food_assistance",
    "RF_PDIAB": "prepregnancy_diabetes",
    "RF_GDIAB": "gestational_diabetes",
    "RF_PHYPE": "prepregnancy_hypertension",
    "RF_GHYPE": "gestational_hypertension",
    "RF_EHYPE": "eclampsia",
    "RF_PPB": "previous_preterm_birth",
    "RF_INFT": "infertility_treatment",
    "RF_CESAR": "previous_cesarean",
    "IP_GON": "gonorrhea",
    "IP_SYPH": "syphilis",
    "IP_CHLAM": "chlamydia",
    "IP_HEPB": "hepatitis_b",
    "IP_HEPC": "hepatitis_c",
    "OB_SUCC": "external_cephalic_version_successful",
    "OB_FAIL": "external_cephalic_version_failed",
    "LD_INDL": "labor_induced",
    "LD_AUGM": "labor_augmented",
    "LD_STER": "steroids_for_fetal_lung_maturation",
    "LD_ANTB": "antibiotics_during_labor",
    "LD_CHOR": "chorioamnionitis",
    "LD_ANES": "epidural_or_spinal_anesthesia",
    "MM_PLAC": "perineal_laceration",
    "MM_RUPT": "ruptured_uterus",
    "MTRAN": "mother_transferred_before_delivery",
    "CA_ANEN": "anencephaly",
    "CA_MNSB": "spina_bifida",
    "CA_CDH": "congenital_diaphragmatic_hernia",
    "CA_OMPH": "omphalocele",
    "CA_GAST": "gastroschisis",
    "CA_LIMB": "limb_reduction_defect",
    "CA_CLEFT": "cleft_lip",
    "CA_CLPAL": "cleft_palate_alone",
    "CA_HYPO": "hypospadias",
}
# Coded items with words for every code (user guide, record layout), renamed to English.
CODED = {
    "BFACIL": "birth_place",
    "MBSTATE_REC": "mother_nativity",
    "RESTATUS": "residence_status",
    "MRACE15": "mother_race",
    "MHISP_R": "mother_hispanic_origin",
    "DMAR": "marital_status",
    "FRACE15": "father_race",
    "FHISP_R": "father_hispanic_origin",
    "RF_DRG": "fertility_enhancing_drugs",
    "RF_ART": "assisted_reproductive_technology",
    "ME_PRES": "fetal_presentation",
    "ME_ROUT": "delivery_route",
    "ME_TRIAL": "trial_of_labor",
    "ATTEND": "birth_attendant",
    "PAY_REC": "payment_source",
    "PAY": "payment_source_detail",
    "SEX": "infant_sex",
    "CA_DOWN": "down_syndrome",
    "CA_DISOR": "suspected_chromosomal_disorder",
}
# Ordered scales, decoded into the words of each level (CLEAN-14).
ORDINAL = {
    "MAGER": "mother_age",
    "MEDUC": "mother_education",
    "FEDUC": "father_education",
    "CIG_0": "cigarettes_before_pregnancy",
    "CIG_1": "cigarettes_first_trimester",
    "CIG_2": "cigarettes_second_trimester",
    "CIG_3": "cigarettes_third_trimester",
    "DPLURAL": "plurality",
    "SETORDER_R": "set_order",
}
# Numbers (counts and measurements without an open end), renamed to English.
NUMBERS = {
    "DOB_WK": "birth_weekday",
    "FAGECOMB": "father_age",
    "PRIORLIVE": "prior_births_now_living",
    "PRIORDEAD": "prior_births_now_dead",
    "PRIORTERM": "prior_other_pregnancy_outcomes",
    "ILLB_R": "months_since_last_live_birth",
    "ILOO_R": "months_since_last_other_outcome",
    "PRECARE": "prenatal_care_start_month",
    "PREVIS": "prenatal_visits",
    "MHTR": "mother_height_inches",
    "PWGT_R": "prepregnancy_weight_pounds",
    "DWGT_R": "delivery_weight_pounds",
    "RF_CESARN": "previous_cesareans",
    "APGAR5": "apgar_score_5_minutes",
    "OEGEST_COMB": "gestation_weeks_obstetric_estimate",
    "COMBGEST": "gestation_weeks_combined",
    "BRTHWGT": "birthweight_grams",
}

YES_NO = {"Y": "Yes", "N": "No"}
EDUCATION = {
    "1": "8th grade or less",
    "2": "9th through 12th grade with no diploma",
    "3": "high school graduate or GED completed",
    "4": "some college credit, but no degree",
    "5": "associate degree",
    "6": "bachelor's degree",
    "7": "master's degree",
    "8": "doctorate or professional degree",
}
RACE15 = {
    "01": "White", "02": "Black", "03": "American Indian or Alaska Native", "04": "Asian Indian", "05": "Chinese",
    "06": "Filipino", "07": "Japanese", "08": "Korean", "09": "Vietnamese", "10": "Other Asian", "11": "Hawaiian",
    "12": "Guamanian", "13": "Samoan", "14": "Other Pacific Islander", "15": "more than one race",
}  # fmt: skip
HISPANIC = {
    "0": "non-Hispanic",
    "1": "Mexican",
    "2": "Puerto Rican",
    "3": "Cuban",
    "4": "Central and South American",
    "5": "other and unknown Hispanic",
}
CIGARETTES = {f"{n:02d}": str(n) for n in range(98)} | {"98": "98 or more"}
MOTHER_AGE = {"12": "10-12"} | {str(n): str(n) for n in range(13, 50)} | {"50": "50 and over"}
CODE_LABELS = {
    "BFACIL": {
        "1": "hospital",
        "2": "freestanding birth center",
        "3": "home (intended)",
        "4": "home (not intended)",
        "5": "home (unknown if intended)",
        "6": "clinic or doctor's office",
        "7": "other",
    },
    "MBSTATE_REC": {"1": "born in the U.S.", "2": "born outside the U.S."},
    "RESTATUS": {"1": "resident", "2": "intrastate nonresident", "3": "interstate nonresident"},
    "MRACE15": RACE15,
    "MHISP_R": HISPANIC,
    "DMAR": {"1": "married", "2": "unmarried"},
    "FRACE15": RACE15,
    "FHISP_R": HISPANIC,
    "RF_DRG": {"Y": "Yes", "N": "No", "X": "not applicable (no infertility treatment)"},
    "RF_ART": {"Y": "Yes", "N": "No", "X": "not applicable (no infertility treatment)"},
    "ME_PRES": {"1": "cephalic", "2": "breech", "3": "other"},
    "ME_ROUT": {"1": "spontaneous", "2": "forceps", "3": "vacuum", "4": "cesarean"},
    "ME_TRIAL": {"Y": "Yes", "N": "No", "X": "not applicable (vaginal delivery)"},
    "ATTEND": {
        "1": "doctor of medicine (MD)",
        "2": "doctor of osteopathy (DO)",
        "3": "certified nurse midwife (CNM)",
        "4": "other midwife",
        "5": "other",
    },
    "PAY_REC": {"1": "Medicaid", "2": "private insurance", "3": "self-pay", "4": "other"},
    "PAY": {
        "1": "Medicaid",
        "2": "private insurance",
        "3": "self-pay",
        "4": "Indian Health Service",
        "5": "CHAMPUS/TRICARE",
        "6": "other government (federal, state, local)",
        "8": "other",
    },
    "SEX": {"M": "male", "F": "female"},
    # Karyotype confirmed and pending become one "Yes": the status comes from a genetic consult after the birth.
    "CA_DOWN": {"C": "Yes", "P": "Yes", "N": "No"},
    "CA_DISOR": {"C": "Yes", "P": "Yes", "N": "No"},
    "MAGER": MOTHER_AGE,
    "MEDUC": EDUCATION,
    "FEDUC": EDUCATION,
    **dict.fromkeys(["CIG_0", "CIG_1", "CIG_2", "CIG_3"], CIGARETTES),
    # Until the 2019 cohort 4 is a quadruplet and 5 a quintuplet or higher; from 2020 4 is a quadruplet or higher.
    "DPLURAL": {"1": "single", "2": "twin", "3": "triplet", "4": "quadruplet or higher", "5": "quadruplet or higher"},
    "SETORDER_R": {"1": "1st", "2": "2nd", "3": "3rd", "4": "4th", "5": "5th to 16th"},
    **dict.fromkeys(CHECKBOXES, YES_NO),
}
# Codes that mean unknown or not stated (or a blank field), set missing before decoding (CLEAN-10).
MISSING_CODES = {
    **{key: ["U", ""] for key in CHECKBOXES},
    "BFACIL": ["9", ""],
    "MBSTATE_REC": ["3", ""],
    "MHISP_R": ["9", ""],
    "FHISP_R": ["9", ""],
    "FRACE15": ["99", ""],
    # DMAR is blank for births in California, whose marital status NCHS may not release.
    "DMAR": ["9", ""],
    "RF_DRG": ["U", ""],
    "RF_ART": ["U", ""],
    "ME_PRES": ["9", ""],
    "ME_ROUT": ["9", ""],
    "ME_TRIAL": ["U", ""],
    "ATTEND": ["9", ""],
    "PAY_REC": ["9", ""],
    "PAY": ["9", ""],
    "CA_DOWN": ["U", ""],
    "CA_DISOR": ["U", ""],
    "MEDUC": ["9", ""],
    "FEDUC": ["9", ""],
    **{key: ["99", ""] for key in ["CIG_0", "CIG_1", "CIG_2", "CIG_3"]},
    # 9 is every singleton (not applicable) and a plural birth whose order is not stated.
    "SETORDER_R": ["9", ""],
    "FAGECOMB": ["99", ""],
    **{key: ["99", ""] for key in ["PRIORLIVE", "PRIORDEAD", "PRIORTERM", "PREVIS", "MHTR", "RF_CESARN", "APGAR5"]},
    **{key: ["99", ""] for key in ["OEGEST_COMB", "COMBGEST"]},
    # 000-003: the code "plural delivery" (the last birth is in this delivery), which plurality and set order say;
    # 888: no earlier live birth (other outcome), which the prior counts say; 999: unknown.
    **{key: ["000", "001", "002", "003", "888", "999", ""] for key in ["ILLB_R", "ILOO_R"]},
    # 00: no prenatal care, which prenatal_visits = 0 says (the two agree on every row); 99: unknown.
    "PRECARE": ["00", "99", ""],
    **{key: ["999", ""] for key in ["PWGT_R", "DWGT_R"]},
    "BRTHWGT": ["9999", ""],
}
# Items whose reporting flag (user guide: 0 "Not reported in birth year") marks the areas that do not report them:
# missing there. Birth place keeps its values: the areas without its flag report every home birth as "home (unknown
# if intended)".
REPORTING_FLAGS = {
    "MHISP_R": "F_MHISP", "MEDUC": "F_MEDUC", "FHISP_R": "F_FHISP", "FEDUC": "F_FEDUC",
    "PRECARE": "F_MPCB", "PREVIS": "F_TPCV", "WIC": "F_WIC", "CIG_0": "F_CIGS_0", "CIG_1": "F_CIGS_1",
    "CIG_2": "F_CIGS_2", "CIG_3": "F_CIGS_3", "MHTR": "F_M_HT", "PWGT_R": "F_PWGT", "DWGT_R": "F_DWGT",
    "RF_PDIAB": "F_RF_PDIAB", "RF_GDIAB": "F_RF_GDIAB", "RF_PHYPE": "F_RF_PHYPE", "RF_GHYPE": "F_RF_GHYPE",
    "RF_EHYPE": "F_RF_EHYPE", "RF_PPB": "F_RF_PPB", "RF_INFT": "F_RF_INFT", "RF_DRG": "F_RF_DRG",
    "RF_ART": "F_RF_ART", "RF_CESAR": "F_RF_CESAR", "RF_CESARN": "F_RF_NCESAR", "IP_GON": "F_IP_GON",
    "IP_SYPH": "F_IP_SYPH",
    "IP_CHLAM": "F_IP_CHLAM", "IP_HEPB": "F_IP_HEPB", "IP_HEPC": "F_IP_HEPC", "OB_SUCC": "F_OB_SUCC",
    "OB_FAIL": "F_OB_FAIL", "LD_INDL": "F_LD_INDL", "LD_AUGM": "F_LD_AUGM", "LD_STER": "F_LD_STER",
    "LD_ANTB": "F_LD_ANTB", "LD_CHOR": "F_LD_CHOR", "LD_ANES": "F_LD_ANES", "ME_PRES": "F_ME_PRES",
    "ME_ROUT": "F_ME_ROUT", "ME_TRIAL": "F_ME_TRIAL", "MM_PLAC": "F_MM_PLAC", "MM_RUPT": "F_MM_RUPT",
    "PAY_REC": "F_PAY_REC", "PAY": "F_PAY", "APGAR5": "F_APGAR5", "CA_ANEN": "F_CA_ANEN", "CA_MNSB": "F_CA_MNSB",
    "CA_CDH": "F_CA_CDH", "CA_OMPH": "F_CA_OMPH", "CA_GAST": "F_CA_GAST",
    "CA_LIMB": "F_CA_LIMB", "CA_CLEFT": "F_CA_CLEFT", "CA_CLPAL": "F_CA_CLPAL", "CA_DOWN": "F_CA_DOWN",
    "CA_DISOR": "F_CA_DISOR", "CA_HYPO": "F_CA_HYPO",
}  # fmt: skip

# Items recorded after the birth, the prediction point (LEAK-10): the abnormal conditions of the newborn (assisted
# ventilation, NICU admission, surfactant, antibiotics, seizures), the transfer within 24 hours, living at the time of
# the report, breastfed at discharge, the 10-minute Apgar (scored only when the 5-minute score is under 7), the
# mother's transfusion, unplanned hysterectomy and ICU admission, the cyanotic congenital heart disease (from the
# physician's progress notes) and the paternity acknowledgement (signed in the hospital).
AFTER_BIRTH = [
    "AB_AVEN1", "AB_AVEN6", "AB_NICU", "AB_SURF", "AB_ANTI", "AB_SEIZ", "ITRAN", "ILIVE", "BFED", "APGAR10",
    "MM_MTR", "MM_UHYST", "MM_AICU", "CA_CCHD", "MAR_P",
]  # fmt: skip
# The link to the death record (the cohort sequence number is filled only on a linked birth; FLGND marks a birth
# linked in the period file) and the age at death: the target and its parts.
DEATH_LINK = ["CO_SEQNUM", "CO_YOD", "FLGND", "AGEDX", "AGER5X"]
# NCHS's imputation flags (mother's age, race and marital status, plurality, sex, gestation, birthweight): the
# imputed values stay, the flags go.
IMPUTATION_FLAGS = ["MAGEIMP", "MRACEIMP", "MAR_IMP", "IMP_PLUR", "IMP_SEX", "COMBGST_IMP", "OBGEST_FLG", "LMPUSED",
                    "BWTIMP"]  # fmt: skip
# Items NCHS derives from kept ones: BMI (from height and pre-pregnancy weight) and weight gain (delivery minus
# pre-pregnancy weight, 0 for a loss, 98 for 98 pounds and more).
DERIVED = ["BMI", "WTGAIN"]


def _read_fixed(archive: zipfile.ZipFile, member: str, items: dict, width: int, chunk_rows: int = 250_000):
    """Read the named items of a fixed-width member (records of ``width`` bytes and CR LF) as stripped text."""
    import pyarrow as pa
    import pyarrow.compute as pc

    record = width + 2
    chunks: dict[str, list] = {name: [] for name in items}
    with archive.open(member) as f:
        while buffer := f.read(record * chunk_rows):
            assert len(buffer) % record == 0, f"{member}: a record is not {width} bytes long"
            rows = np.frombuffer(buffer, dtype="S1").reshape(-1, record)
            assert (rows[:, width] == b"\r").all(), member
            assert (rows[:, width + 1] == b"\n").all(), member
            for name, (start, end) in items.items():
                field = np.ascontiguousarray(rows[:, start - 1 : end]).view(f"S{end - start + 1}").ravel()
                chunks[name].append(pc.utf8_trim_whitespace(pa.array(field, pa.binary()).cast(pa.string())))
    return pa.table({name: pa.chunked_array(parts, pa.string()) for name, parts in chunks.items()})


class NchsLinkedBirthInfantDeath1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a baby born alive in the United States die before its first birthday, judged from what its birth "
            "certificate records at the birth?"
        ),
        use_case=(
            "For example, a state health department or a perinatal quality collaborative estimates each newborn's "
            "risk of dying in its first year from what was known at the birth, as the expected deaths against which "
            "hospitals' and counties' infant deaths are compared (risk adjustment). NCHS publishes the files for "
            "analyses of infant mortality; the use case is ours."
        ),
        row=(
            "One live birth to a mother living in the United States, 2017 to 2023 (25.9 million births of NCHS's "
            "public-use birth cohort files), with the items of the 2003 U.S. standard birth certificate."
        ),
        predicted=(
            "Whether the infant died before its first birthday, by a death certificate NCHS linked to the birth "
            "record (0.55% of births); the deaths NCHS could not link (0.4% to 1.4%) count as survivors."
        ),
        known=(
            "The parents' age, race, Hispanic origin and education, the mother's nativity, marital status and "
            "payment source, earlier births and pregnancies, prenatal care, smoking, height and weights, pregnancy "
            "risk factors and infections, labour and delivery, and the newborn's sex, plurality, gestational age, "
            "birthweight, five-minute Apgar score and the congenital anomalies the certificate reports (not the "
            "heart disease of the progress notes); the birth month and time of day."
        ),
        split=(
            "Each test window is one of the last three birth years (2021, 2022, 2023), up to 500,000 births each; "
            "training is a random million of the births of all earlier years back to 2017, as for a model refit "
            "each year."
        ),
        changes=(
            "We join the linked deaths to the births as NCHS's user guide does, keep births to U.S. residents, and "
            "leave out what the certificate records after the birth: the newborn's conditions and transfer, the "
            "10-minute Apgar, living at the report, breastfeeding, the mother's ICU care, the cyanotic heart disease, "
            "the paternity acknowledgement and a later-born twin's counts of earlier births (which count its co-twin)."
        ),
        fit="direct",
        fit_reason=(
            "The inputs are the certificate's items known at the birth and the label is the linked death. The public "
            "file has no state, county or hospital, which a health department would know. The record of an infant "
            "who died within a day is less complete, a small mark kept with a note. A screen at registration acts "
            "later and is not this task."
        ),
    )

    # Dataset
    unique_name = "nchs_linked_birth_infant_death_1m"
    version_of = "nchs_linked_birth_infant_death"
    version_comment = """
        We sample per test window (v2 split protocol): each yearly window keeps a random 500k of its 3.6M to 3.7M births, and each train side is a random 1M of all births of the earlier cohorts back to 2017, drawn in one random order for all windows and stratified on the target, so every side keeps the infant-death share; the frame keeps only the rows a split uses. The sampling fraction is therefore not the same for every year: about 6.7% of the births of 2017-2020 against about 13.7% of those of 2021 (a training year of the 2022 and 2023 windows and a test year), an artefact of the row budget.
    """
    year = "2026"
    domain = "medical & healthcare"
    source = "GOV Website"
    source_url = "https://www.cdc.gov/nchs/nvss/linked-birth.htm"
    license = "Public domain (U.S. federal government data), under the NCHS data use restrictions"
    data_tags = ()
    download_description = """
        We download the seven combined period/cohort zips (432-452 MB each) and the user guides from the NCHS FTP server, linked from Vital Statistics Online (https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm, "Cohort Linked Birth / Infant Death Data"). Each zip holds the cohort's births file and the linked infant deaths of the cohort year and the next; the 2024PE2023CO zip was posted on 2026-01-22, the 2018PE2017CO zip on 2020-05-26 (server dates). No registration; the files fall under the NCHS data use restrictions (https://www.cdc.gov/nchs/data_access/restrictions.htm).

        mkdir -p local-data-warehouse/nchs_linked_birth_infant_death/docs && cd local-data-warehouse/nchs_linked_birth_infant_death
        for p in 2018PE2017CO 2019PE2018CO 2020PE2019CO 2021PE2020CO 2022PE2021CO 2023PE2022CO 2024PE2023CO; do wget https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/DVS/period-cohort-linked/$p.zip; done
        for g in 18PE17CO 19PE18CO 20PE19CO 21PE20CO 22PE21CO 23PE22CO 24PE23CO; do wget -P docs https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/period-cohort-linked/${g}_linkedUG.pdf; done
    """
    bibtex = """
        @misc{nchs2026linkedbirthinfantdeath,
          author = {{National Center for Health Statistics}},
          title = {Linked Birth/Infant Death Data Sets, 2018 Period/2017 Cohort to 2024 Period/2023 Cohort Public-Use Files},
          howpublished = {\\url{https://www.cdc.gov/nchs/nvss/linked-birth.htm}},
          year = {2026},
          note = {National Vital Statistics System, Centers for Disease Control and Prevention. Files of 2020-05-26 to 2026-01-22},
        }
    """
    curation_comments = """
        We start with the public-use linked birth/infant death files of NCHS for the birth cohorts 2017 to 2023: the zips 2018PE2017CO to 2024PE2023CO, each with the cohort's births file and the linked infant deaths of the cohort year and the next, read by the record layout of the 2024 period / 2023 cohort user guide (the guides of 2018/2017 to 2023/2022 give the same positions).

        - Prediction point: the birth, once the newborn is weighed and its sex, plurality, gestational age, five-minute Apgar score and the congenital anomalies the certificate reports are recorded (they may be diagnosed before or after the delivery; the heart disease, from the physician's progress notes, and the karyotype status are left out, see below), with what the certificate holds about the parents, the pregnancy, prenatal care and labour and delivery. Only those items are features. NCHS describes the files as "a valuable tool for monitoring and exploring the complex inter-relationships between infant death and risk factors present at birth" (linked-birth page) and names no model or decision; the use case (risk adjustment of hospitals' and counties' infant deaths by the expected deaths at the birth) is ours; a follow-up screen at registration acts later, on infants still alive, and is not this task.
        - Rows: births to U.S. residents (RESTATUS 1 to 3), as NCHS tabulates and as the user guide's cohort code selects; the 58,268 births to foreign residents go (a death abroad is not linked). 25,936,466 births remain.
        - Target: `infant_death` is "Yes" for a birth linked to an infant death of its cohort in the two numerator files, joined on the cohort sequence number and the year of death as the guide's "User Created Cohort File" section does: 143,474 deaths (0.553%; 0.535% to 0.575% by cohort). The 2017 births file writes the sequence number with six digits, its deaths file with seven, so both are padded to seven before the join. Infant deaths NCHS could not link to a birth (0.4% in 2017 to 1.4% in 2022; 260 of the 2023 cohort, 1.3%) count as survivors (LEAK-25).
        - History: the seven cohorts of the combined period/cohort format, one record layout; the 2016 cohort, the first of that format, is not needed by the windows or the training floor and is not read.
        - Dropped as recorded after the birth (LEAK-10): the abnormal conditions of the newborn (assisted ventilation, ventilation over six hours, NICU admission, surfactant, antibiotics, seizures), the transfer within 24 hours, living at the time of the report ("No" for 7,566 of the 19,743 deaths of 2023), breastfed at discharge, the 10-minute Apgar (scored only when the five-minute score is under 7; unknown for 19% of the 2023 deaths in the first hour against 0.45% of survivors), and the mother's transfusion, unplanned hysterectomy and ICU admission.
        - Also dropped as recorded after the birth (LEAK-10): the cyanotic congenital heart disease, whose source on the facility worksheet is the physician's progress notes (reported for 0.83% of deaths under one hour, 2.76% of deaths at 1-27 days), and the paternity acknowledgement, signed in the hospital after the birth. Down syndrome and the suspected chromosomal disorder keep "Yes" for both "karyotype confirmed" and "karyotype pending": the status comes from a genetic consult after the birth (confirmed on 63% of the day-0 deaths' reports that carry the disorder, 27% of survivors').
        - Co-twins (LEAK-10): a later-born member of a plural delivery counts its co-multiples among its earlier live births "now living" and "now dead" as of the report, so a co-twin's death after the birth is in its record (a dead earlier birth on 31.5% of the second-born twins who died on day 0, 5.0% of the first-born). Both counts are missing on every plural birth whose set order is not 1st; blanking them moved ROC AUC within the seed spread.
        - Dropped as the target and its parts: the cohort sequence number and the year of death (filled only on a linked birth), the match flag FLGND and the age at death.
        - NCHS's imputations stay and their flags go, but for one: a missing birthweight is filled from the previous record of the same gestation, race, sex and plurality, and the mother's age, race and marital status, plurality and sex are imputed too. The imputation is not free of the label: in the files of 2017-2019 the birthweight was imputed only for linked deaths (764, 860 and 947 births, every one died), in 2020 mostly (81.6%) and from 2021 for 38.6% to 42.1%; so the imputed birthweights of 2017-2019 become missing again (LEAK-13), which moved ROC AUC within the seed spread (0.9213 and 0.9226). The flags together add no ROC AUC to the features (0.9147 with them, 0.9149 and 0.9158 without, LightGBM, 1M births of 2020-2022, 500k of 2023; seed spread of that model 0.004).
        - Reporting flags: an item whose flag says the birth's area does not report it becomes missing, then the flags go: eclampsia, fertility drugs and assisted reproduction in one area in 2017-2021 (57,000 to 150,000 births a year), and the detailed payment source for 26% to 43% of the births of a year (`payment_source`, the national four-level recode, is kept beside it). Birth place keeps its values where its flag is 0 (2017-2020, about 450,000 births a year, the same births whose marital status is withheld, so California): that area reports every home birth as "home (unknown if intended)".
        - Dropped as derived from kept items: BMI (height and pre-pregnancy weight, within 0.05 for 99% of the 2023 births) and the weight gain (delivery minus pre-pregnancy weight, 0 for a loss, capped at 98). NCHS's recodes (age, race and education groups, birthweight and gestation bands, birth order, delivery method) are not read.
        - Both gestation estimates stay: the obstetric estimate, NCHS's standard since 2014, and the combined gestation; they differ on 34% of the 2023 births.
        - Codes become the guide's words (CLEAN-12); unknown, not stated and blank (U, 9, 99, 999, 9999) are missing. 000-003 of the two birth intervals ("plural delivery": the last birth is in this delivery, which plurality and set order say) and 888 (no earlier birth, or other outcome) and 00 of the month prenatal care began (no care) are missing too: the prior-birth counts and `prenatal_visits` = 0 hold them (00 and 0 visits coincide on every birth of 2023). Set order is missing for every singleton. Plurality 4 (quadruplet) and 5 (quintuplet or higher) of 2017-2019 become "quadruplet or higher", the code from 2020.
        - Ordered categories (CLEAN-14): the mother's age, whose ends the guide cuts ("10-12", "50 and over"), both parents' education, the daily cigarettes before and in each trimester ("98 or more"), plurality and set order ("5th to 16th"). Height and the two weights stay numbers though NCHS caps them (30 and 78 inches, 75 and 375 pounds, 100 and 400 pounds); the five-minute Apgar (0-10) stays a score. The time of birth ships as minutes after midnight, the weekday as 1 (Sunday) to 7; the public file has no day of birth, so the time column is the first day of the birth month.
        - Note (SEL-1): the parents' race and Hispanic origin are inputs, as in NCHS's tables of infant mortality. Without them ROC AUC is 0.9148 (0.9149 and 0.9158 with them, same splits); the curator decides whether they stay (the across-datasets protected-grounds item; every reviewer recommends dropping them).
        - Potential leak, kept on purpose: the certificate of an infant who died within a day is less complete. In 2023 most items are unknown 3 to 12 times as often among those deaths as among survivors (prenatal care month 8.2% against 1.9%), the newborn's measurements 17 to 90 times (five-minute Apgar 6.7% against 0.4%, birthweight 1.8% against 0.02%), and most items 1 to 3 times as often among deaths after 28 days. These unknowns cannot be told from the others, so they stay: filling every missing value but the father's with random training values moved ROC AUC within the seed spread of 0.004 (0.9171 against 0.9149 and 0.9158) and log loss from 0.0190 to 0.0192 (+1%). Revisit if log loss is reported for this task.
        - Licence: U.S. government data in the public domain, under NCHS's data use restrictions (statistical reporting and analysis only, no attempt to identify anyone, no linkage to identifiable data).
    """

    # Task
    target = TARGET
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "NCHS defines no metric: the linked-file page and the 2024 period / 2023 cohort user guide report infant "
            "mortality rates per 1,000 births with their confidence intervals, no prediction score, and no "
            "competition set a task on these files; the one paper we read (Saravanou et al. 2019, files of 2000-2002) "
            "reports precision-recall and ROC AUC, so no single metric. A rate, a threshold or a share to act on is "
            "not fixed (MET-6, MET-7), so ROC AUC on the probabilities (MET-8): the actor ranks newborns by risk. The 0.5% "
            "positive share alone is no reason for the area under the precision-recall curve (MET-9)."
        )
    )

    temporal = Temporal(on="birth_month", splits=TemporalSplits(window=1, unit="years", n_windows=3))
    splits_comment = """
        A model refit once a year scores the next year's births. Test windows are the last three birth years, 2023, 2022 and 2021 (3.60M, 3.67M and 3.66M births; 0.549%, 0.553% and 0.545% infant deaths), newest first; each keeps a random 500k of its births, stratified (about 2,700 deaths each). Each train side is a random 1M of the births of all earlier cohorts back to 2017 (15.0M to 22.3M births, 58% to 86% of the rows).
        No gap: every label is a death within the year after the birth and is final in the release, so the newest training cohort is not selected by its outcome (SPLIT-10, a fixed horizon). A model refit on 1 January would not yet know the deaths of the previous year's late births; at equal size the newest cohort adds no ROC AUC and a little log loss (1M births of 2022, 2021 or 2020 alone, tested on 500k of 2023: 0.9137, 0.9142, 0.9151; log loss 0.0190, 0.0192, 0.0193; LightGBM, one seed and one window, against a seed spread of 0.004; averaged over the three windows, gaps of one and two years cost 0.0012 and 0.0008 ROC AUC). NCHS posts a cohort's file 23 to 29 months after the cohort's year ends (the 2023 cohort on 2026-01-22), so a model built on the public files alone would train on older cohorts; a health department linking its own records would not.
        COVID-19: the training cohorts from 2020 and all three windows follow its arrival; the infant death share fell from 0.575% (2017) to 0.535% (2020) and was 0.545% to 0.553% in the windows.
    """
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (PREPARED,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # Each cohort's zip holds its births file (the "denominator", record length 1,346) and the linked infant
        # deaths of the cohort year and the next ("numerator" files, 1,743). As the user guide's "User Created Cohort
        # File" section does, the deaths of infants born in the cohort year join the births on the cohort sequence
        # number and the year of death. Codes stay as published, as text.
        import pyarrow as pa
        import pyarrow.compute as pc
        import pyarrow.parquet as pq

        keys = ["CO_SEQNUM", "CO_YOD"]
        columns = [*BIRTH_ITEMS, "AGEDX", "AGER5X"]
        schema = pa.schema([(name, pa.dictionary(pa.int32(), pa.string())) for name in columns])
        with pq.ParquetWriter(raw_dir / PREPARED, schema) as writer:
            for cohort in COHORTS:  # one cohort at a time, one row group each
                with zipfile.ZipFile(raw_dir / f"{cohort + 1}PE{cohort}CO.zip") as archive:
                    names = archive.namelist()
                    prefixes = (f"VS{cohort}LINK", f"VS{cohort % 100:02d}LINK")
                    (births_member,) = [n for n in names if "DENPUB" in n and n.startswith(prefixes)]
                    death_members = sorted(n for n in names if "NUMPUB" in n)
                    assert len(death_members) == 2, names
                    births = _read_fixed(archive, births_member, BIRTH_ITEMS, DENOMINATOR_WIDTH)
                    deaths = pa.concat_tables(
                        [_read_fixed(archive, member, DEATH_ITEMS, NUMERATOR_WIDTH) for member in death_members]
                    )
                deaths = deaths.filter(pc.equal(deaths["DOB_YY"], str(cohort))).select([*keys, "AGEDX", "AGER5X"])
                # The 2017 births file writes the cohort sequence number with six digits, its deaths file with seven.
                births, deaths = _zero_pad(births), _zero_pad(deaths)
                key = pc.binary_join_element_wise(deaths["CO_SEQNUM"], deaths["CO_YOD"], "-")
                assert pc.count_distinct(key).as_py() == deaths.num_rows, "one death per key"
                linked = births.filter(pc.not_equal(births["CO_SEQNUM"], "")).num_rows
                assert linked == deaths.num_rows, f"{cohort}: {linked} births with a cohort number, {deaths.num_rows}"
                births = births.append_column("row", pa.array(np.arange(births.num_rows)))
                table = births.join(deaths, keys=keys, join_type="left outer", use_threads=False).sort_by("row")
                assert table.num_rows == births.num_rows
                assert pc.sum(pc.is_valid(table["AGEDX"])).as_py() == deaths.num_rows, f"{cohort}: unmatched deaths"
                table = pa.table({name: pc.dictionary_encode(table[name]).combine_chunks() for name in columns})
                writer.write_table(table.cast(schema))
                del births, deaths, table

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import pyarrow.parquet as pq

        # Column by column, each a categorical of the published codes (the whole table at once would take ~17 GB).
        path = raw_dir / PREPARED
        names = pq.read_schema(path).names
        return pd.DataFrame({name: pq.read_table(path, columns=[name]).column(0).to_pandas() for name in names})

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. The cohort: births to U.S. residents (RESTATUS 1-3), as NCHS tabulates and the user guide's cohort code
        #    selects; a foreign resident's death abroad is never linked.
        df = raw[raw["RESTATUS"] != "4"].copy()
        # 2. The target: a linked death of the infant before its first birthday (the numerator files hold deaths under
        #    one year of age only).
        df[TARGET] = np.where(df["AGEDX"].notna(), "Yes", "No")
        # 3. The time column and the time of day: the birth month (the public file has no day) and the minutes after
        #    midnight of the time of birth (9999 not stated).
        df["birth_month"] = pd.to_datetime(
            df["DOB_YY"].astype(str) + "-" + df["DOB_MM"].astype(str) + "-01", format="%Y-%m-%d"
        )
        df["birth_time_minutes"] = _clock_minutes(df["DOB_TT"])
        # 3b. A later-born member of a plural delivery counts its co-multiples among its earlier births "now living"
        #     and "now dead" as of the report, so a co-twin's death after the birth is in its record (LEAK-10): both
        #     counts become missing on the plural births not born first (set order 1).
        later_born = ((df["DPLURAL"] != "1") & (df["SETORDER_R"] != "1")).to_numpy()
        for item in ("PRIORLIVE", "PRIORDEAD"):
            df[item] = df[item].mask(later_born)
        # 3c. The files of 2017-2019 impute a missing birthweight only for linked deaths (BWTIMP 1: every one died),
        #     so those imputed weights become missing again (LEAK-13).
        imputed = ((df["BWTIMP"] == "1") & df["DOB_YY"].isin(["2017", "2018", "2019"])).to_numpy()
        df["BRTHWGT"] = df["BRTHWGT"].mask(imputed)
        # 4. Items the reporting flag marks as not reported in the birth's area become missing.
        for item, flag in REPORTING_FLAGS.items():
            df[item] = df[item].mask((df[flag] == "0").to_numpy())
        # 5. Codes that mean unknown become missing, then codes become the words of the codebook (CLEAN-10, CLEAN-12).
        for item, codes in MISSING_CODES.items():
            df[item] = _remove_codes(df[item], codes)
        for item, labels in CODE_LABELS.items():
            df[item] = _decode_categories(df[item], labels, item)
        for item in NUMBERS:
            df[item] = _numbers(df[item])
        # 6. Drop what is not an input: the items recorded after the birth (LEAK-10), the death link and the age at
        #    death (the target), NCHS's imputation flags, the reporting flags, derived items and the raw time fields.
        flags = [c for c in df.columns if c.startswith("F_")]
        df = drop_columns(
            df, [*AFTER_BIRTH, *DEATH_LINK, *IMPUTATION_FLAGS, *flags, *DERIVED, "DOB_YY", "DOB_MM", "DOB_TT"]
        )
        return df.rename(columns={**CHECKBOXES, **CODED, **ORDINAL, **NUMBERS})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        cigarettes = [ORDINAL[c] for c in ("CIG_0", "CIG_1", "CIG_2", "CIG_3")]
        return FeatureTypes(
            categorical=[*CHECKBOXES.values(), *CODED.values()],
            datetime={"birth_month": "%Y-%m-%d"},
            ordinal={
                "mother_age": list(MOTHER_AGE.values()),
                "mother_education": list(EDUCATION.values()),
                "father_education": list(EDUCATION.values()),
                **{key: list(CIGARETTES.values()) for key in cigarettes},
                "plurality": list(dict.fromkeys(CODE_LABELS["DPLURAL"].values())),
                "set_order": list(CODE_LABELS["SETORDER_R"].values()),
            },
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        births = raw[raw["RESTATUS"] != "4"]
        died = births["AGEDX"].notna()

        def death_share(item: str) -> pd.DataFrame:
            table = died.groupby(births[item], observed=True).agg(["size", "mean"])
            table.index = [f"{item} = {v!r}" for v in table.index]
            return table.rename(columns={"size": "births", "mean": "infant death share"})

        after_birth = pd.concat(
            [death_share(item) for item in ("ILIVE", "ITRAN", "AB_NICU", "AB_AVEN6", "BFED", "MM_AICU")]
        )
        after_birth["infant death share"] = after_birth["infant death share"].round(4)

        age = births["AGER5X"].astype(object)
        group = pd.Series(
            np.select(
                [~died, age.isin(["1", "2"]), age.isin(["3", "4"])],
                ["survived", "died, first day", "died, day 1 to 27"],
                default="died, day 28 to 364",
            ),
            index=births.index,
        )
        unknown = {
            "prenatal care month (99)": births["PRECARE"] == "99",
            "mother's education (9)": births["MEDUC"] == "9",
            "WIC (U)": births["WIC"] == "U",
            "five-minute Apgar (99)": births["APGAR5"] == "99",
            "obstetric gestation (99)": births["OEGEST_COMB"] == "99",
            "birthweight, not imputed (9999)": births["BRTHWGT"] == "9999",
            "congenital anomalies (U)": births["CA_ANEN"] == "U",
            "father's age (99)": births["FAGECOMB"] == "99",
        }
        shares = pd.DataFrame({name: flag.groupby(group).mean() for name, flag in unknown.items()}).T.round(4)
        shares = shares[["survived", "died, first day", "died, day 1 to 27", "died, day 28 to 364"]]

        imputed = pd.concat([death_share(flag) for flag in ("BWTIMP", "IMP_SEX", "MAGEIMP", "MAR_IMP", "IMP_PLUR")])
        imputed["infant death share"] = imputed["infant death share"].round(4)
        return [
            Decision(
                "Items recorded after the birth are left out",
                "The prediction point is the birth: the newborn's conditions after it (NICU admission, ventilation), "
                "the transfer, living at the report, breastfeeding at discharge and the mother's ICU admission are "
                "recorded later, and several follow the infant's course (LEAK-10). Births to U.S. residents, "
                "2017-2023.",
                after_birth,
            ),
            Decision(
                "Unknown items mark early deaths: kept with a note",
                "The certificate of an infant who died in its first day is less complete. The unknowns cannot be "
                "told from the others, and hiding them moved ROC AUC within the seed spread (notes). Share "
                "of each item unknown, by the infant's age at death.",
                shares,
            ),
            Decision(
                "NCHS's imputed values stay, their flags go",
                "An imputation flag marks a missing item, and a missing birthweight or sex marks a death; the "
                "imputed values hide that, and the flags add no ROC AUC to the features (notes).",
                imputed,
            ),
        ]


def _zero_pad(table):
    """``table`` with its cohort sequence numbers as seven digits; a blank (a birth without a linked death) stays."""
    import pyarrow.compute as pc

    numbers = table["CO_SEQNUM"].combine_chunks()
    padded = pc.if_else(pc.equal(numbers, ""), numbers, pc.utf8_lpad(numbers, 7, "0"))
    return table.set_column(table.schema.get_field_index("CO_SEQNUM"), "CO_SEQNUM", padded)


def _remove_codes(values: pd.Series, codes: list[str]) -> pd.Series:
    """A categorical of codes with ``codes`` (unknown, not stated, blank) set missing, on the categories."""
    present = [c for c in codes if c in values.cat.categories]
    return values.cat.remove_categories(present) if present else values


def _decode_categories(values: pd.Series, labels: dict[str, str], item: str) -> pd.Series:
    """The codes of a categorical replaced by their words, on the categories (``decode`` maps row by row, too slow
    for 26 million rows); a code without a label raises, as in ``decode``.
    """
    values = values.cat.remove_unused_categories()
    unlabelled = sorted(set(values.cat.categories) - set(labels))
    if unlabelled:
        raise ValueError(f"Codes of {item!r} without a label: {unlabelled[:10]}")
    words = [labels[code] for code in values.cat.categories]
    levels = list(dict.fromkeys(words))  # two codes may share a label (plurality 4 and 5 before 2020)
    position = np.append(np.array([levels.index(w) for w in words], dtype=np.int64), -1)
    codes = position[values.cat.codes.to_numpy()]
    return pd.Series(pd.Categorical.from_codes(codes, levels), index=values.index, name=values.name)


def _numbers(values: pd.Series) -> pd.Series:
    """A categorical of numeric codes as floats, on the categories."""
    values = values.cat.remove_unused_categories()
    numbers = np.append(pd.to_numeric(pd.Series(values.cat.categories, dtype=object)).to_numpy(dtype=float), np.nan)
    return pd.Series(numbers[values.cat.codes.to_numpy()], index=values.index, name=values.name)


def _clock_minutes(values: pd.Series) -> pd.Series:
    """Hhmm as minutes after midnight; 9999 (not stated) missing."""
    hhmm = _numbers(_remove_codes(values, ["9999", ""]))
    return (hhmm // 100) * 60 + hhmm % 100
