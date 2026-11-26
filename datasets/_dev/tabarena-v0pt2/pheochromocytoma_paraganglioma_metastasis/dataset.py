"""Curated dataset definition for `pheochromocytoma_paraganglioma_metastasis` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    GroupBasis,
    Metric,
    NonFeature,
    Source,
    TaskSummary,
    TimeBasis,
    decode,
    drop_columns,
)

# The first 14 columns of the sheet (header row 2), renamed; the 2 empty and the 24 specialist columns after them are
# not read.
COLUMNS = {
    "Patient ID": "patient_id",
    "Internal Testing (IT)/External Validatio (EV)": "cohort",
    "Sex (M/F)": "sex",
    "Age at diagnosis of first tumor {s)": "age_at_first_diagnosis",
    "Predictions for metastatic disease": "pmt_investigator_prediction",
    "Plasma NMN pg/ml": "plasma_normetanephrine",
    "Plasma MN pg/ml": "plasma_metanephrine",
    "Plasma MTY  pg/ml": "plasma_methoxytyramine",
    "Previous history of PPGLs?  (YES/NO)": "previous_ppgl",
    "Adrenal/Extra-adrenal location of primary tumor": "primary_tumour_location",
    "Presence of SDHB": "sdhb_variant",
    "Tumor category of primary tumor(S;B, M)": "tumour_category",
    "Spherical volume of  primary  tumor{s)": "primary_tumour_volume",
    "Metastatic YES/NO": "metastatic",
}
PLASMA = ["plasma_normetanephrine", "plasma_metanephrine", "plasma_methoxytyramine"]
NUMERIC = ["age_at_first_diagnosis", *PLASMA, "primary_tumour_volume"]
LABELS = {
    "sex": {"F": "female", "M": "male"},
    "previous_ppgl": {"NO": "No", "YES": "Yes"},
    "primary_tumour_location": {"Adrenal": "adrenal", "Extra-adrenal": "extra-adrenal"},
    "sdhb_variant": {"NO": "No", "YES": "Yes", "not tested": "not tested"},
    "tumour_category": {"S": "single", "B": "bilateral", "M": "multifocal"},
    "metastatic": {"NO": "No", "YES": "Yes"},
}


class PheochromocytomaParagangliomaMetastasis(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Does a patient with a pheochromocytoma or paraganglioma have, or go on to develop, distant metastases?"
        ),
        use_case=(
            "At presentation with a first or a recurrent tumour, before surgery, an endocrinologist estimates the "
            "chance of metastatic disease to decide on functional imaging before the operation and how intensive and "
            "long the follow-up should be (the source's stated use)."
        ),
        row=(
            "One patient of seven tertiary centres in the USA and Europe at presentation with a first or a recurrent "
            "tumour (788; 221 with an earlier tumour): 493 from earlier cohorts, 295 from the prospective PMT trial."
        ),
        predicted=(
            "Whether metastases in tissues where chromaffin tissue is normally absent were found, at diagnosis or "
            "during follow-up of varying length (223 patients, 28%)."
        ),
        known=(
            "At presentation with a first or a recurrent tumour: sex, age at the first tumour, the plasma levels of "
            "normetanephrine, metanephrine and methoxytyramine, whether the patient had an earlier tumour, the primary "
            "tumour's location, size and focality, and the germline SDHB test result, or that no test was done."
        ),
        split="Random patients, so the test data stands for new patients of the same centres.",
        changes=(
            "We leave out the trial investigator's own prediction and the 24 risk ratings of 12 specialists, the "
            "source's comparators, and do not tell the model which cohort a patient came from."
        ),
        fit="approximate",
        fit_reason=(
            "The features are the preoperative findings the source names, but the label has no fixed horizon: "
            "metastases count at diagnosis or during follow-up, shorter for the negatives (PMT trial 49 against 100 "
            "months), so some 'No' are not final. Rows are first or recurrent presentations; "
            "for a recurrence, age, location and volume describe the first tumour, the plasma values the later one. "
            "Transfer to a new centre is untested."
        ),
    )

    # Dataset
    unique_name = "pheochromocytoma_paraganglioma_metastasis"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.5281/zenodo.7749613",
            license="CC BY 4.0",
            year="2023",
            bibtex="""
                @article{pamporaki2023prediction,
                  title   = {Prediction of metastatic pheochromocytoma and paraganglioma: a machine learning modelling
                             study using data from a cross-sectional cohort},
                  author  = {Pamporaki, Christina and Berends, Annika M. A. and Filippatos, Angelos and Prodanov, Tamara
                             and Meuter, Leah and Prejbisz, Aleksander and Beuschlein, Felix and Fassnacht, Martin and
                             Timmers, Henri J. L. M. and N{\\"o}lting, Svenja and Abhyankar, Kaushik and Constantinescu,
                             Georgiana and Kunath, Carola and de Haas, Robbert J. and Wang, Katharina and Remde, Hanna
                             and Bornstein, Stefan R. and Januszewicz, Andrzej and Robledo, Mercedes and Lenders, Jacques
                             W. M. and Kerstens, Michiel N. and Pacak, Karel and Eisenhofer, Graeme},
                  journal = {The Lancet Digital Health},
                  volume  = {5},
                  number  = {9},
                  pages   = {e551--e559},
                  year    = {2023},
                  doi     = {10.1016/S2589-7500(23)00094-8},
                  note    = {Data: Zenodo, https://doi.org/10.5281/zenodo.7749613}
                }
            """,
            files=("DataZonodo.xlsx",),
        ),
    )
    download_description = """
        We download the one file of the Zenodo record 7749613 (published 2023-03-19, CC BY 4.0; md5
        ba4001d382fa638b46fd2b180a003017).

        mkdir -p local-data-warehouse/pheochromocytoma_paraganglioma_metastasis
        wget -O local-data-warehouse/pheochromocytoma_paraganglioma_metastasis/DataZonodo.xlsx "https://zenodo.org/records/7749613/files/DataZonodo.xlsx?download=1"
    """
    curation_comments = """
        We start with `DataZonodo.xlsx` from Zenodo 7749613, the data of Pamporaki et al. (2023, Lancet Digit Health): one sheet, 788 patients, 14 named columns, 2 empty ones and 24 columns of specialists' risk ratings. The release has this one file.

        - Prediction point: the presentation with a first or a recurrent tumour, before surgery. The source says "at first diagnosis" ("these models allow for predictions at first diagnosis of PPGL by utilizing clinical features routinely and preoperatively available", Discussion), but some patients enter at a recurrent presentation, with plasma values taken then. The ten features are the paper's nine plus SDHB status.
        - We drop the 24 specialist columns (`1M` to `12M`, without and with SDHB status) and `Predictions for metastatic disease`: they are the paper's comparators, risk calls made by people on the same features (Methods, objectives 1 and 3), not inputs a model has at diagnosis. The prediction column exists only for the 295 PMT patients, and its value "false negative" marks the 28 PMT patients whose biochemical tests were negative (Methods; 9 metastatic).
        - We drop `Patient ID`: the file is sorted by cohort and, within each cohort, by the outcome (IDs 1-295 the PMT cohort, its 57 metastatic patients last; IDs 623-788 are the earlier cohorts' 166 metastatic patients), so the ID encodes the label.
        - The cohort flag (`Internal Testing (IT)/External Validatio (EV)`, kept as `cohort`) is no feature (curator's decision, 2026-11-25, Andrej): 493 patients of the earlier cohorts (34% metastatic) and 295 of the prospective PMT trial (19%). It says which study enrolled the patient, not anything known about the patient, and a new patient belongs to neither. We declare it a provenance non-feature, so no task uses it as an input and a later task can hold the PMT trial out.
        - `sdhb_variant` keeps "not tested" as its own value (curator's decision, 2026-11-25, Andrej): 80 patients, as many as Table 1 counts without genetic testing (60 + 17 + 2 + 1). The paper's best model (AUC 0.942) does not use SDHB status, and one with it scores 0.940; the Discussion calls it "often not available at initial diagnosis".
        - Class-dependent recording (record marker `Class-dependent Recording`): 14 patients, all metastatic and all in the earlier cohorts (IDs 626-788), carry plasma values with decimals (methoxytyramine 8.35, 16.70, 41.46; metanephrine 23.4), apparently converted from nmol/L (0.05 and 0.1 nmol/L of methoxytyramine are 8.35 and 16.7 pg/mL); every other value is a whole number. We round the three plasma values to whole pg/mL, which removes the format; the rounded values 8 and 17 occur in both classes (31 and 20 patients). The format alone scores ROC AUC 0.531 on the raw values, and rounding leaves the models' scores unchanged (random forest 0.9445 either way, 10 x 3 folds), so the fix costs nothing and closes the shortcut.
        - `primary_tumour_volume` is the file's "spherical volume of primary tumor(s)", unit not stated (0 to 2,368, which fits cubic centimetres of a sphere up to about 16.5 cm across); the paper's Table 1 reports size in cm. Missing for 36 patients, 29 of them metastatic (13% of the metastatic against 1.2% of the others) and 29 of them with an earlier tumour (27 of the metastatic); we keep it missing as published (decision table). The missing indicator alone scores ROC AUC 0.559, and filling the 36 with the median moves no model by more than 0.001 (random forest 0.9445 against 0.9436), so models do not read the outcome off the gap. One volume of 0.0 cm³ (under 0.05, extra-adrenal, not metastatic) is kept: unusual for a tumour, not impossible, and next to values of 0.1.
        - `age_at_first_diagnosis` (1 patient), `plasma_metanephrine` (6), `plasma_normetanephrine` and `plasma_methoxytyramine` (1 each) are missing as published. Methoxytyramine is 0 for 4 PMT patients (below the assay's limit, presumably) and kept.
        - Note: `previous_ppgl` (221 patients, "local recurrence and/or new tumor", Table 1) marks patients who are not at their first tumour; their metastases may have shown before this presentation. It is one of the paper's nine features and stays. 156 of the 221 are metastatic (54% in the PMT trial, 79% in the earlier cohorts); without the column the random forest falls from 0.945 to 0.899, and on the 567 first-tumour patients alone (67 metastatic) the models score 0.87 to 0.92.
        - Note: follow-up differs by outcome (geometric means 82.8 against 95.6 months in the earlier cohorts, 49.3 against 99.7 in the PMT trial, Table 1), so some patients labelled non-metastatic may develop metastases later (the paper's stated limitation).
        - No duplicate rows, and no test row has an exact copy of its features in training.
        - Note: one patient is probably entered twice (curator's decision, 2026-11-26, Andrej: both rows kept): raw `Patient ID` 468 and 475, both of the earlier cohorts, match on all six fields that stay fixed across enrolments: men, age 54.9 at the first tumour, adrenal, no SDHB variant, bilateral tumours of volume 159.5 (no other row has it), and both have no earlier tumour and are not metastatic. Their plasma values differ, and row 475's metanephrine equals its normetanephrine (537), a likely entry error. A six-field match is expected 0.13 times by chance (age and volume shuffled within sex and location, 200 draws); no pair across the two cohorts matches on all six (the 47 that match on the other five all differ in volume). Without a patient key we cannot tell which row is right, and one pair with the same label cannot move a score.
        - Note: the cohort is not hidden in the features: they tell the PMT patients from the others with ROC AUC 0.71-0.72. Adding the cohort flag gains at most 0.002 (random forest 0.9463 against 0.9445), and a model trained on the earlier cohorts alone scores 0.93-0.95 on the PMT trial (95% CI about ±0.03 on 295 patients), as random folds score on its patients (0.943-0.947), so the random split does not flatter a transfer the source tested.
        - Note: an untrained count of five risk factors (extra-adrenal location, an earlier tumour, an SDHB variant, methoxytyramine over 33 pg/mL, volume over 33.5 cm³) scores ROC AUC 0.904 against 0.94-0.95 for trained models (TP-4). The methoxytyramine cutoff is 0.2 nmol/L, the level above which Eisenhofer et al. (2012, Eur J Cancer 48:1739) report a higher likelihood of metastases; the volume cutoff, a sphere 4 cm across, is chosen by us (that paper uses 5 cm). Paired on the 30 shipped splits, LightGBM gains 0.033 (SE 0.002) over the count and is ahead on all 30 splits (random forest +0.040, logistic regression on logged plasma values +0.044, each ahead on 30 of 30).
    """
    non_features = (
        NonFeature(
            "cohort",
            "provenance",
            "the study that enrolled the patient: earlier cohorts (IT) or the PMT trial (EV)",
        ),
    )
    split_leaf = "L-PLACE.random"
    time_basis = TimeBasis(
        "ForcedIIDFromTemporal",
        """
        the patients were enrolled over years (earlier cohorts, then the prospective PMT trial)
        and the file carries no date of diagnosis or enrolment, so the time is lost; the two cohorts differ in place
        as well as time and are too few periods. A dated release would test patients diagnosed later, under later
        imaging and genetic testing.
        """,
    )
    group_basis = GroupBasis(
        """
        ForcedIIDFromGrouped (Andrej, 2026-11-25): the source's use is at other centres (it trains on the
        earlier cohorts and validates on the PMT trial), which whole centres held out would stand for, but the file
        names no centre, only two cohorts, too few groups to hold out; the cohort flag is no feature. Overlap left:
        every test fold holds patients of both cohorts and of centres seen in training; trained on the earlier
        cohorts alone, models score 0.93-0.95 on the PMT trial (95% CI about ±0.03 on 295 patients), about what
        random folds give its patients. About 10-18 pairs across the cohorts match on sex, age, SDHB status,
        location and category beyond chance (possibly patients enrolled twice, at most about 2% of rows); without
        IDs they cannot be linked, and the score from the earlier cohorts to the PMT trial shows no effect.
        """,
    )

    # Task
    target = "metastatic"
    problem_type = "binary_classification"
    splits_comment = """
        Default splits: repeated 3-fold cross-validation over all 788 patients, stratified on the outcome, on the
        forced random leaf L-PLACE.random (curator's decision, 2026-11-25, Andrej). The source trains on the 493
        patients of the earlier cohorts and tests once on the 295 of the PMT trial; that split was weighed and not
        taken, as it gives a single training side and two cohorts are too few groups to test transfer to a centre.
    """
    metric = Metric.source(
        "roc_auc",
        original="AUC",
        reference="Pamporaki et al. 2023, Methods: candidate and top models selected according to AUC",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # Header in row 2 (row 1 labels the specialist blocks); the first 14 columns are the patient data.
        return pd.read_excel(raw_dir / "DataZonodo.xlsx", sheet_name="Sheet1", header=1, usecols="A:N")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.rename(columns=COLUMNS)
        assert list(df.columns) == list(COLUMNS.values()), list(df.columns)
        # the ID sorts the file by cohort and outcome; the PMT investigator's call is a comparator, given for one
        # cohort only ("false negative" marks the PMT patients with negative biochemistry); the cohort stays as a
        # provenance non-feature
        df = drop_columns(df, ["patient_id", "pmt_investigator_prediction"])
        df[NUMERIC] = df[NUMERIC].apply(pd.to_numeric)
        # 14 metastatic patients of the earlier cohorts carry values converted from nmol/L (8.35, 16.70); whole
        # pg/mL everywhere else
        df[PLASMA] = df[PLASMA].round(0)
        df = decode(df, LABELS)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["sex", "previous_ppgl", "primary_tumour_location", "sdhb_variant", "tumour_category"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        data = raw.rename(columns=COLUMNS)
        metastatic = data["metastatic"].eq("YES")

        plasma = data[PLASMA].apply(pd.to_numeric)
        decimals = (plasma.ne(plasma.round(0)) & plasma.notna()).any(axis=1)
        formats = pd.crosstab(
            [data["cohort"], data["metastatic"]], decimals.map({True: "with decimals", False: "whole numbers"})
        )

        missing = pd.DataFrame(
            {
                "patients": metastatic.groupby(data["metastatic"]).size(),
                "volume missing": data["primary_tumour_volume"].isna().groupby(data["metastatic"]).sum(),
                "volume missing, earlier tumour": (
                    data["primary_tumour_volume"].isna() & data["previous_ppgl"].eq("YES")
                )
                .groupby(data["metastatic"])
                .sum(),
            }
        )
        by_cohort = pd.crosstab(data["cohort"], data["metastatic"], margins=True)
        return [
            Decision(
                title="Plasma values with decimals only among metastatic patients",
                why=(
                    "Values converted from nmol/L carry decimals in 14 rows, all metastatic; rounding to whole pg/mL "
                    "removes the format."
                ),
                evidence=formats,
            ),
            Decision(
                title="Tumour volume missing mostly for metastatic patients",
                why="Kept missing as published; most of these patients had an earlier tumour.",
                evidence=missing,
            ),
            Decision(
                title="The two cohorts",
                why="The cohort flag is no feature; the split is random over both cohorts.",
                evidence=by_cohort,
            ),
        ]
