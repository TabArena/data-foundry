"""Curated dataset definition for `wild_type_attr_cardiac_amyloidosis` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    GroupBasis,
    Metric,
    Source,
    TaskSummary,
    TimeBasis,
    decode,
)

VALIDATION_FILE = "ca_validation_group_input (IQVIA validation dataset).csv"
ICD_MAP_FILE = "icd_map.csv"

# The label, as Huda's `Model Validation.ipynb` sets `cohort_flag`: the code list holds E85.82 (wild-type ATTR
# amyloidosis) or E85.4 (organ-limited amyloidosis, the code the paper's Methods use to select Cohort 3).
LABEL_CODES = ("E8582", "E854")

# Every amyloidosis code (ICD-10 E85*) is removed before the features are built (paper, Methods: "Features derived
# from ICD codes of any amyloidosis condition (i.e., ICD-9 277.30 or ICD-10 E85) ... were removed").
AMYLOIDOSIS_PREFIX = "E85"

# The three levels of Huda's hierarchical mapping, each giving one flag per name.
LEVELS = ("short_desc", "major", "sub_chapter")

# Huda's rule: a flag is kept when at least 2% of the cases carry it (paper, Methods: "present in at least 2% of
# wild-type ATTR-CM patients"). Here it runs on this file's cases that remain after the exclusions.
MIN_CASE_SHARE = 0.02

# The source's own leak list (`potential_target_leaks` in `Model Training.ipynb`); issue 1 A of the screening review.
SOURCE_LEAK_FLAGS = ("cardiomyopathy_in_diseases_classified_elsewhere", "other_forms_of_heart_disease")

# A flag goes when every code behind it is an ICD-10-CM manifestation code whose "Code first underlying disease" note
# names amyloidosis (E85.-): such a code is written only together with the disease it follows, here the label's own
# amyloidosis code. The codes, read from the CMS ICD-10-CM tabular (FY2019 and FY2025 list the same 15); a code under
# one of them shares its note (M14.8 covers M14.80-M14.89).
AMYLOID_CODE_FIRST = (
    "D77", "G328", "G63", "G990", "G998", "H42", "I43", "I680", "I798", "J99", "K77", "L99", "M148", "N08", "N29",
)  # fmt: skip

# A flag goes when every code behind it is heart transplant status (Z94.1): the transplant follows the diagnosis or
# makes it (2.0% of cases, 0.2% of controls).
LATE_STATUS_CODES = ("Z941",)

# Patients dropped from both classes: the source excluded from its cases "blood cancers and other non-ATTR-CM-related
# amyloidosis terms" (Methods, Cohort 3), and its controls carry these codes while no case does. The codes: every code
# with no case and at least 10 controls in the file (end-stage renal disease, monoclonal gammopathy, other plasma-
# protein disorders, plasma-cell neoplasms, lymphomas, peritoneal dialysis catheter care and complication), cerebral
# amyloid angiopathy (I68.0), and intracranial haemorrhage (I60-I62), which in the cases has the profile of cerebral
# amyloid angiopathy (lobar haemorrhage, 238 cases against 17 controls).
EXCLUSION_CODES = ("N186", "D472", "E8809", "I680", "C8588", "C8330", "C8339", "C8510", "Z4902", "T85691A")
EXCLUSION_PREFIXES = ("C90", "I60", "I61", "I62")

TARGET = "cardiac_amyloidosis"


def clean_feature_name(names: pd.Series) -> pd.Series:
    """Huda's name cleaning (`preprocess` in `Model Validation.ipynb`): lowercase, first 100 characters, every
    character outside A-Z, a-z and 0-9 replaced by an underscore.
    """
    return names.str.lower().str[:100].str.replace(r"[^A-Za-z0-9]", "_", regex=True)


def is_excluded(codes: pd.Series) -> pd.Series:
    """Codes whose patients leave both classes (`EXCLUSION_CODES`, `EXCLUSION_PREFIXES`)."""
    return codes.isin(EXCLUSION_CODES) | codes.str.startswith(EXCLUSION_PREFIXES)


class WildTypeAttrCardiacAmyloidosis(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Does a heart-failure patient's coded diagnosis history point to cardiac amyloidosis, before anyone has "
            "tested for it?"
        ),
        use_case=(
            "A health system or cardiologist scores heart-failure patients from their claims or record codes and "
            "refers the high scorers for scintigraphy or biopsy, so that a treatable amyloid cardiomyopathy is found "
            "earlier (Huda et al. 2021, Discussion)."
        ),
        row=(
            "One heart-failure patient aged 50 or more in the IQVIA US claims data (ICD-10 codes, about October 2015 "
            "to April 2019): every diagnosis code of the patient's history, as presence flags."
        ),
        predicted=(
            "Whether the patient carries an amyloidosis code (E85.4 organ-limited, which every case holds, or E85.82 "
            "wild-type ATTR): the source's cardiac amyloidosis cohort against matched non-amyloid heart failure. The "
            "label is noisy: only 516 cases hold E85.82, E85.9 (unspecified) is in 35% of cases, E85.3 (AA) in 10% "
            "and E85.1 (hereditary) in 9%, and 47% carry neither I43 nor E85.82."
        ),
        known=(
            "Which diagnoses, diagnosis groups and chapters appear anywhere in the patient's coded history, with "
            "every amyloidosis code and the codes written with it removed. Features and label come from the same "
            "undated claims record."
        ),
        known_at_scoring="",
        split=("Random patients of the same claims database; another health system and later patients are not tested."),
        changes=(
            "We built the flags from the raw code lists with the source's map and 2% rule, removed the amyloidosis "
            "codes, the source's two leak flags, the manifestation codes coded with amyloidosis and heart transplant "
            "status, and dropped the patients with the source's case exclusions (blood cancer, end-stage renal "
            "disease, cerebral amyloid angiopathy, intracranial haemorrhage) from both classes."
        ),
        fit="approximate",
        fit_reason=(
            "The codes are real, but the flags cover the whole history, work-up codes included; the label is the "
            "source's noisy code set (every case E85.4, only 516 E85.82, some AA or hereditary), not wild-type ATTR "
            "alone; patients with cerebral amyloid angiopathy or intracranial haemorrhage leave both classes; and "
            "the 1:1 matched sample sets a prevalence far above the under 1% a health system meets."
        ),
    )

    # Dataset
    unique_name = "wild_type_attr_cardiac_amyloidosis"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://www.nature.com/articles/s41467-021-22876-9",
            license="CC BY 4.0",
            year="2021",
            bibtex="""
                @article{huda2021attrcm,
                  title = {A machine learning model for identifying patients at risk for wild-type transthyretin
                           amyloid cardiomyopathy},
                  author = {Huda, Ahsan and Casta{\\~n}o, Adam and Niyogi, Anindita and Schumacher, Jennifer and
                            Stewart, Michelle and Bruno, Marianna and Hu, Mo and Ahmad, Faraz S. and Deo, Rahul C.
                            and Shah, Sanjiv J.},
                  journal = {Nature Communications},
                  volume = {12},
                  pages = {2725},
                  year = {2021},
                  doi = {10.1038/s41467-021-22876-9}
                }
            """,
            files=(VALIDATION_FILE, ICD_MAP_FILE),
        ),
    )
    data_tags = ()
    split_leaf = "L-PLACE.random"
    time_basis = TimeBasis(
        "ForcedIIDFromTemporal",
        """
        the model scores heart-failure patients as they arrive, but the release keeps one code list per
        patient without a date, so no patient can be placed in time and the split is random. The lists hold ICD-10
        codes only (no ICD-9 code in any list; US claims moved to ICD-10 on 1 October 2015), so the history runs from
        about October 2015 to 30 April 2019, the end of the IQVIA extract (Methods; the extract starts 2008). Not tested: patients after the data, coded under later practice (more
        scintigraphy, tafamidis from 2019, a growing use of E85.82).
        """,
    )
    group_basis = GroupBasis(
        """
        the source's use is another health system (it validated on Optum and Northwestern, neither released),
        but the file is one source with no site, region or practice column, so no place can be held out. Overlap
        left: test patients share the database's coding habits with the training side, so the score is optimistic for
        another system (the source's wild-type model, trained on the derivation cohort and not on this label, fell
        from ROC AUC 0.93 on its IQVIA holdout to 0.80 at Northwestern; no model of this label was tested elsewhere).
        """,
    )
    download_description = """
        wget -O source_data.zip "https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-22876-9/MediaObjects/41467_2021_22876_MOESM4_ESM.zip"
        unzip -j source_data.zip "ATTRCM Model Training & CA Validation/ca_validation_group_input (IQVIA validation dataset).csv" "ATTRCM Model Training & CA Validation/icd_map.csv"
        mkdir -p local-data-warehouse/wild_type_attr_cardiac_amyloidosis && mv source_data.zip "ca_validation_group_input (IQVIA validation dataset).csv" icd_map.csv local-data-warehouse/wild_type_attr_cardiac_amyloidosis/
    """
    curation_comments = """
        We start with `ca_validation_group_input (IQVIA validation dataset).csv` and `icd_map.csv` from the Source
        Data of Huda et al. (Nat Commun 12:2725, 2021): the paper's Cohort 3, heart-failure patients with an
        organ-limited amyloidosis code and 1:1 propensity-matched non-amyloid heart-failure controls (age, sex, length
        of history, number of visits), one row per patient with a comma-separated list of ICD-10 codes.

        - Files left out: `training_input (IQVIA derivation dataset).csv` (the paper's 2,142-patient wild-type ATTR-CM
          cohort as 1,874 ready-made flags; the curator chose the larger validation cohort for this record, and 597 of
          its patients, 505 cases and 92 controls, are in the file with the same label), the two notebooks (code, read
          for the label and feature rules), `package-readme.txt`.
        - Label: a case when the code list holds E85.82 or E85.4, the rule of Huda's `Model Validation.ipynb`; 7,697
          cases and 7,697 controls in the file. Every case holds E85.4, 516 also E85.82; no control holds any E85 code.
          The label is noisy: E85.9 (unspecified) is in 35% of cases, E85.3 (AA) in 10%, E85.1 (hereditary) in 9%,
          and 47% of cases carry neither I43 nor E85.82. E85.4 was the code for ATTR cardiomyopathy before E85.82
          existed (October 2017), so a case without I43 is not proof of non-cardiac amyloid.
        - Every E85 code is removed before the features are built, so the label is not among them (paper, Methods).
        - Features: Huda's mapping. Each code is looked up in `icd_map.csv` (22,220 of the 22,222 distinct values are
          in it; the two that are not give no flag: `-1`, a placeholder in 1,293 patients, and N35.81, one patient),
          and each of its three names (description, category, sub-chapter)
          becomes a 0/1 flag, the name lowercased, cut at 100 characters and every other character replaced by `_`.
          Names that clean to the same string share one flag, as in the source.
        - A flag is kept when at least 2% of the cases carry it. Huda applied this rule to the derivation's
          wild-type cases, and the validation notebook reused that feature list; on this file the rule is our
          adaptation, run on the 6,899 cases that remain after the exclusions.
        - Dropped: the source's two leak flags (`Model Training.ipynb`, `potential_target_leaks`).
          `cardiomyopathy_in_diseases_classified_elsewhere` (I43, coded with the amyloidosis it accompanies) is in
          52.4% of cases and 1.4% of controls; `other_forms_of_heart_disease` (the I30-I52 sub-chapter, which holds
          the heart-failure codes) is in every patient.
        - Dropped: every flag whose codes are all ICD-10-CM manifestation codes whose "Code first underlying
          disease" note names amyloidosis (E85.-) in the CMS tabular: D77, G32.8, G63, G99.0, G99.8, H42, I43, I68.0,
          I79.8, J99, K77, L99, M14.8, N08, N29. Such a code is written with the disease it follows, here the label's
          own code. Past the 2% rule this drops I43 (already the source's leak flag) and
          `respiratory_disorders_in_diseases_classified_elsewhere` (J99: 180 cases, 11 controls in the raw file);
          the others fall under 2% now, but the rule holds for a later label (G63 passes with E85.82 alone). The
          broader rule, every "classified elsewhere" flag, would also drop flags whose notes do not name amyloidosis
          (anaemia in chronic kidney disease, dementia, infectious agents).
        - Dropped: `heart_transplant_status` (Z94.1; 2.0% of cases, 0.2% of controls in the raw file): the transplant
          follows the diagnosis or makes it.
        - Dropped from both classes: 1,940 patients (798 cases, 1,142 controls) with an excluded code. For Cohort 3
          the paper's Methods exclude "blood cancers and other non-ATTR-CM-related amyloidosis terms" (the full list
          of blood cancer, light-chain amyloidosis, end-stage renal disease, cerebral amyloid angiopathy and
          intracranial haemorrhage is the Northwestern cohort's), applied to the cases only, so 821 controls and no
          case carried those codes. We apply the exclusion to both classes: every code with no case and at least
          10 controls (N18.6 end-stage renal disease, D47.2 monoclonal gammopathy, E88.09 other plasma-protein
          disorders, C90 plasma-cell neoplasms, the lymphomas C83.30, C83.39, C85.10 and C85.88, the peritoneal
          dialysis catheter codes Z49.02 and T85.691A), I68.0 cerebral amyloid angiopathy, and I60-I62 intracranial
          haemorrhage (798 cases, 363 controls; in the cases with the profile of cerebral amyloid angiopathy, lobar
          haemorrhage 238 against 17), which follows from the clause on other amyloidosis terms. 13,454 patients
          remain, 6,899 cases and 6,555 controls. Cost: LightGBM ROC AUC 0.8294 before, 0.8256 after (3 x 3 splits),
          all of it from the haemorrhage step; the exclusion codes decoded the controls (up to +0.016).
        - Dropped: 7 flags that hold exactly the same patients as another flag under a second name (a description
          and its category, such as `essential__primary__hypertension` and `essential_hypertension`); the first name
          in sorted order stays.
        - Dropped: `patient_id`, an IQVIA identifier.
        - Note: the flags named `exposure_to_...` are ICD-10 external-cause diagnoses (W, X codes: exposure to
          mechanical forces or other factors), not an amount at risk.
        - Note: one group of 4 identical rows holds both labels; kept, as patients with the same coded history are
          natural in a sparse code set.
        - Note: every patient has a heart-failure code (I50); the matching on visit count leaves the number of codes
          close (median 112 in cases, 102 in controls without the E85 codes; 109 and 97 in the patients kept).
        - Anomaly: the paper's Table 1 gives 7,296 cases and 7,296 controls for Cohort 3; the file holds 7,697 of each.
        - Anomaly: 110 patients (56 cases, 54 controls) carry up to 152 codes of T63 (toxic effects of venomous
          animals) each, a bulk coding artefact equally common in both classes, likely from the ICD-9 to ICD-10
          conversion (ICD-9 989.5 maps to every T63 code); kept.
        - Potential leak, kept on purpose: the flags are lifetime presence ("Only the presence or absence of the ICD
          codes (and not the temporal sequence of ICD codes) were included as features", Methods), so codes written
          during or after the amyloid work-up stay: `cardiomyopathy` (I42 and its descriptions, 54.0% of cases
          against 26.1% of controls in the patients kept) above all. Issue 4 of the record's review weighs dropping that family.
        - Potential leak, kept on purpose: the 2% rule counts the cases of the whole file, the test folds' included, a
          weak transductive selection of the columns. It moves nothing: LightGBM ROC AUC 0.8256 with the rule on the
          cases (1,695 flags), 0.8256 with a label-free rule (2% of all patients, 1,641 flags), 3 x 3 splits. Issue 7
          of the record's review weighs the label-free rule.
        - Selection: 1:1 matched case-control sample from a claims database, labels from codes (undiagnosed amyloid
          patients may sit among the controls, as the paper says), record marker `Selection Bias`.
    """

    # Task
    target = TARGET
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUROC",
        reference=(
            'Huda et al. 2021, Nat Commun 12:2725, Methods: "The Random Forest model, which had the best diagnostic '
            'performance (as evaluated by the AUROC curve), was carried forward for further validation"; the '
            "Northwestern models are ranked by AUROC only"
        ),
        definition="ROC AUC of cardiac amyloidosis against matched non-amyloid heart failure.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # Huda's join: each patient's codes, one row per code, with the three names of the ICD-10 map.
        wide = pd.read_csv(raw_dir / VALIDATION_FILE, dtype=str)
        long = wide.assign(code=wide["codes"].str.split(",")).explode("code")[["patient_id", "code"]]
        icd_map = pd.read_csv(raw_dir / ICD_MAP_FILE, dtype=str)
        icd_map = icd_map.loc[icd_map["type"] == "ICD10", ["codes", *LEVELS]].rename(columns={"codes": "code"})
        assert not icd_map["code"].duplicated().any()
        return long.merge(icd_map, on="code", how="left", validate="many_to_one").reset_index(drop=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        long = raw
        # 1. Patients with an excluded code leave both classes.
        excluded = long.loc[is_excluded(long["code"]), "patient_id"].unique()
        long = long[~long["patient_id"].isin(excluded)]
        # 2. The label from the codes, before they are removed.
        cases = pd.Index(long.loc[long["code"].isin(LABEL_CODES), "patient_id"].unique())
        patients = pd.Index(sorted(long["patient_id"].unique()))
        # 3. Every amyloidosis code goes before any feature is built.
        long = long[~long["code"].str.startswith(AMYLOIDOSIS_PREFIX)]
        # 4. One flag per cleaned name at each of the three levels (codes the map lacks give none).
        flags = long.melt(id_vars=["patient_id", "code"], value_vars=list(LEVELS), value_name="name")
        flags = flags.dropna(subset=["name"])
        flags = pd.DataFrame(
            {
                "patient_id": flags["patient_id"].to_numpy(),
                "code": flags["code"].to_numpy(),
                "feature": clean_feature_name(flags["name"]).to_numpy(),
            }
        )
        # 5. Flags whose every code is a code-first amyloid manifestation or heart transplant status.
        only_codes = flags.groupby("feature")["code"].agg(lambda c: c.str.startswith(AMYLOID_CODE_FIRST).all())
        late = flags.groupby("feature")["code"].agg(lambda c: c.str.startswith(LATE_STATUS_CODES).all())
        dropped = set(only_codes.index[only_codes]) | set(late.index[late]) | set(SOURCE_LEAK_FLAGS)
        flags = flags[["patient_id", "feature"]].drop_duplicates()
        # 6. Huda's 2% rule over the remaining cases, then the drops of step 5.
        is_case = flags["patient_id"].isin(cases)
        share = flags[is_case].groupby("feature").size() / len(cases)
        kept = sorted(f for f in share.index[share >= MIN_CASE_SHARE] if f not in dropped)
        flags = flags[flags["feature"].isin(kept)]
        # 7. The 0/1 matrix, every remaining patient a row (a patient with no kept flag is all zeros).
        rows = patients.get_indexer(flags["patient_id"])
        cols = pd.Index(kept).get_indexer(flags["feature"])
        matrix = np.zeros((len(patients), len(kept)), dtype=np.int8)
        matrix[rows, cols] = 1
        # 8. Flags of two levels that hold the same patients (a description that is its own category under another
        #    name) are one feature: keep the first name in sorted order.
        same = pd.Series([matrix[:, j].tobytes() for j in range(matrix.shape[1])]).duplicated().to_numpy()
        df = pd.DataFrame(matrix[:, ~same], columns=[f for f, dup in zip(kept, same) if not dup])
        df[TARGET] = patients.isin(cases).astype(int)
        return decode(df, {TARGET: {0: "No", 1: "Yes"}})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # Every feature is a yes/no presence flag of a named diagnosis, so categorical (0/1 values as built).
        return FeatureTypes(categorical=[c for c in df.columns if c != TARGET])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        long = raw
        cases = set(long.loc[long["code"].isin(LABEL_CODES), "patient_id"])
        n_cases = len(cases)
        n_controls = long["patient_id"].nunique() - n_cases

        def counts(mask: pd.Series) -> tuple[int, str, int, str]:
            hit = set(long.loc[mask, "patient_id"])
            in_cases = len(hit & cases)
            in_controls = len(hit) - in_cases
            return in_cases, f"{in_cases / n_cases:.1%}", in_controls, f"{in_controls / n_controls:.1%}"

        code = long["code"]
        both = "patients excluded from both classes"
        rows = {
            "E85* (any amyloidosis; removed)": code.str.startswith(AMYLOIDOSIS_PREFIX),
            "I43 cardiomyopathy in diseases classified elsewhere (flag dropped)": code.str.startswith("I43"),
            "J99 respiratory disorders in diseases classified elsewhere (flag dropped)": code.str.startswith("J99"),
            "any code-first amyloid manifestation code (flags dropped)": code.str.startswith(AMYLOID_CODE_FIRST),
            "Z94.1 heart transplant status (flag dropped)": code.isin(LATE_STATUS_CODES),
            "I50 heart failure (in every patient)": code.str.startswith("I50"),
            "I42 cardiomyopathy (kept; issue 4)": code.str.startswith("I42"),
            f"N18.6 end-stage renal disease ({both})": code == "N186",
            f"D47.2 monoclonal gammopathy ({both})": code == "D472",
            f"E88.09 plasma-protein disorder ({both})": code == "E8809",
            f"C90 plasma-cell neoplasms ({both})": code.str.startswith("C90"),
            f"C83.30, C83.39, C85.10, C85.88 lymphomas ({both})": code.isin(["C8330", "C8339", "C8510", "C8588"]),
            f"Z49.02, T85.691A dialysis catheter ({both})": code.isin(["Z4902", "T85691A"]),
            f"I68.0 cerebral amyloid angiopathy ({both})": code == "I680",
            f"I60-I62 intracranial haemorrhage ({both})": code.str.match(r"I6[0-2]"),
            f"any exclusion code ({both})": is_excluded(code),
        }
        table = pd.DataFrame(
            [(name, *counts(mask)) for name, mask in rows.items()],
            columns=["codes", "cases", "cases %", "controls", "controls %"],
        ).set_index("codes")
        return [
            Decision(
                title="Codes that give the label away or mark the selection",
                why=(
                    "The label is read from the E85 codes, so they are removed; the manifestation codes whose "
                    "ICD-10-CM note says to code amyloidosis first (I43, J99 and others) and heart transplant status "
                    "follow the diagnosis, so their flags go; the codes the source excluded from the cases only mark "
                    "controls, so their patients leave both classes. Patients in the raw file (15,394)."
                ),
                evidence=table,
            )
        ]
