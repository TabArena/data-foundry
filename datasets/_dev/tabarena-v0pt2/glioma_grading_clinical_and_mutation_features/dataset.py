"""Curated dataset definition for `glioma_grading_clinical_and_mutation_features` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

DEMOGRAPHICS = ("Gender", "Age_at_diagnosis", "Race")
"""The three clinical columns of the file; the 20 gene columns follow them."""


def age_in_years(text: pd.Series) -> pd.Series:
    """Years from a GDC age text such as "51 years 108 days" ("87 years" has no day part; "--" is missing).

    The GDC portal writes the days from birth to diagnosis as whole years of 365.25 days plus the remaining days, so
    years + days / 365.25 gives the GDC's day count, in years, within one day.
    """
    parts = text.str.extract(r"^(\d+) years?(?: (\d+) days?)?$").astype(float)
    return parts[0] + parts[1].fillna(0) / 365.25


class GliomaGradingClinicalAndMutationFeatures(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Is a diffuse glioma a lower-grade glioma or a glioblastoma, judging from its gene mutations and the "
            "patient's age, sex and race?"
        ),
        use_case=(
            "After a diffuse glioma has been removed or biopsied, graded from the tissue and its DNA sequenced, a "
            "neuropathology lab checks the histological grade against the tumour's mutation profile and flags a "
            "disagreement for review. The source's own task is the grading from these features."
        ),
        row=(
            "One patient of the US Cancer Genome Atlas glioma projects (lower-grade glioma and glioblastoma), 862 "
            "patients diagnosed between 1989 and 2013."
        ),
        predicted=(
            "Whether the tumour is a lower-grade glioma (WHO grade II or III) or a glioblastoma (grade IV), as "
            "diagnosed from the tissue."
        ),
        known=(
            "Whether each of the 20 Cancer Gene Census genes mutated most often in these patients (the GDC portal's "
            "list) carries a mutation (from whole-exome sequencing), and the patient's sex, race and age at diagnosis."
        ),
        split=("Random patients, so the test data stands for new patients like those of the two projects."),
        changes=(
            "We drop the project and the primary diagnosis, which give the label, and the patient code, whose site "
            "part also gives it; we keep the patients without a clinical record or race, whom the authors' own file "
            "drops."
        ),
        fit="approximate",
        fit_reason=(
            "A histological grade of its era (1989-2013) stands in for today's WHO 2021 integrated grade, from an exome "
            "gene set without TERT, CDKN2A/B, EGFR amplification or +7/-10; the mutations are known after the "
            "histology."
        ),
    )

    # Dataset
    unique_name = "glioma_grading_clinical_and_mutation_features"
    year = "2022"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5R62J"
    license = "CC BY 4.0"
    download_description = """
        We download the UCI archive of dataset 759. It holds the original file TCGA_GBM_LGG_Mutations_all.csv (862
        patients; sha256 6c617f370467b99e3d9b17633ac735fb900801fd6ffc8cc865344067e84b6312), which we read, and the
        authors' preprocessed TCGA_InfoWithGrade.csv (839 patients, numeric codes; the file of OpenML 46604).

        mkdir -p local-data-warehouse/glioma_grading_clinical_and_mutation_features && cd local-data-warehouse/glioma_grading_clinical_and_mutation_features
        wget https://archive.ics.uci.edu/static/public/759/glioma+grading+clinical+and+mutation+features+dataset.zip
        unzip glioma+grading+clinical+and+mutation+features+dataset.zip && rm glioma+grading+clinical+and+mutation+features+dataset.zip
    """
    bibtex = """
        @article{tasci2022hierarchical,
          title={Hierarchical Voting-Based Feature Selection and Ensemble Learning Model Scheme for Glioma Grading with Clinical and Molecular Characteristics},
          author={Tasci, Erdal and Zhuge, Ying and Kaur, Harpreet and Camphausen, Kevin and Krauze, Andra Valentina},
          journal={International Journal of Molecular Sciences},
          volume={23},
          number={22},
          pages={14155},
          year={2022},
          publisher={MDPI},
          doi={10.3390/ijms232214155}
        }
    """
    curation_comments = """
        We start with TCGA_GBM_LGG_Mutations_all.csv, the original file of UCI dataset 759 (Tasci et al. 2022): 862 patients of the TCGA lower-grade glioma (TCGA-LGG) and glioblastoma (TCGA-GBM) projects, with sex, race, age at diagnosis and the mutation status of the 20 Cancer Gene Census genes mutated most often in these patients (the GDC portal's list).

        - Prediction point: a diffuse glioma has been resected or biopsied, graded from the tissue and its DNA sequenced; a neuropathology lab checks the histological grade class, lower-grade glioma (WHO grade II or III) or glioblastoma (grade IV), against the 20 mutation flags and the patient's sex, race and age, and flags a disagreement for review. The grading from these features is the source's task.
        - Target: `Grade` is the TCGA project of every row, so the label is the histological diagnosis that put a tumour in one of the two projects. We keep the labels LGG and GBM. LGG merges WHO grades II and III (238 grade II, 259 grade III and 2 without a grade in the GDC).
        - We drop `Project` (a copy of the label), `Primary_Diagnosis` (the histology the grade follows from; decision table) and `Case_ID` (the TCGA patient barcode, one row per patient, whose tissue source site gives the label: each of the 45 sites sent patients to one project only).
        - IID split: the 45 sites are each pure in the label, but the features do not predict the site (below the majority rate within each grade), and holding out whole sites scores like the shipped split (mean per-fold ROC AUC over 10 repeats of 3 folds: logistic regression 0.921 and random forest 0.927, against 0.921 and 0.924).
        - The mutation flags are the GDC's open-access somatic calls from whole-exome sequencing for every patient (decision table). The 70 patients with no mutation in the 20 genes have 3 to 110 calls in other genes, so `NOT_MUTATED` is a wildtype call. The flags, sex and race are categories. The 20 genes are the Cancer Gene Census genes mutated most often over all patients of both projects, chosen without the label; longer genes outside the census, such as TTN, are not among them.
        - `Age_at_diagnosis` is a GDC text such as "51 years 108 days"; we convert it to years as years + days / 365.25, which gives the GDC's day count within one day.
        - `--` (4 patients without a clinical record, and the age of one more) and `not reported` (race of 18 patients) become missing. We keep these patients, which the authors' preprocessed file TCGA_InfoWithGrade.csv (OpenML 46604) drops.
        - Note: the grades are histological, from diagnoses between 1989 and 2013, and WHO 2021 regrades some of these tumours with markers the data lacks. Without IDH1 and IDH2 the models keep ROC AUC 0.888 (logistic regression) and 0.893 (random forest), so the label is not built from the features; we keep the source's label.
        - Note: the two classes are two separately collected TCGA projects. Both were exome-sequenced at one centre (Broad Institute), and the GDC called all 994 mutation files with one workflow. The DNA of 142 GBM patients was whole-genome amplified (no LGG). The features do not tell amplified from plain DNA (random forest ROC AUC 0.532 within GBM), and without the amplified GBM the ROC AUC stays at random forest 0.922 / logistic regression 0.919 (all rows 0.919 / 0.917), so the batch carries none of the grade signal.
        - Note: lgg_low_grade_glioma and glioblastoma, which share TCGA patients with this file, are both retired, so no shipped dataset overlaps it.
    """

    # Task
    target = "Grade"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # the file starts with a byte-order mark
        return pd.read_csv(raw_dir / "TCGA_GBM_LGG_Mutations_all.csv", encoding="utf-8-sig")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # the project is a copy of the label, the primary diagnosis the histology the label follows from
        if not (df["Project"].str.removeprefix("TCGA-") == df[self.target]).all():
            raise ValueError("Grade no longer equals the TCGA project.")
        df = drop_columns(df, ["Project", "Primary_Diagnosis", "Case_ID"])
        # "--" (no clinical record) and "not reported" (race) are missing values
        clinical = list(DEMOGRAPHICS)
        df[clinical] = df[clinical].replace({"--": np.nan, "not reported": np.nan})
        df["Age_at_diagnosis"] = age_in_years(df["Age_at_diagnosis"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[c for c in df.columns if c not in ("Age_at_diagnosis", self.target)])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        genes = [c for c in df.columns if c not in (*DEMOGRAPHICS, self.target)]
        mutated = df[genes].eq("MUTATED").groupby(df[self.target], observed=True).mean().T.round(3)
        mutated.columns = [f"mutated share, {grade}" for grade in mutated.columns]
        mutated.index.name = "gene"
        diagnosis = pd.crosstab(raw["Primary_Diagnosis"], raw[self.target])
        return [
            Decision(
                title="Project and Primary_Diagnosis dropped: they give away the label",
                why=(
                    "The label is the TCGA project, and the histological diagnosis decides the project: "
                    "'Glioblastoma' occurs only in TCGA-GBM."
                ),
                evidence=diagnosis,
            ),
            Decision(
                title="Mutation status by grade",
                why=(
                    "The 20 flags are the GDC's somatic calls (17,220 of 17,240 cells match the GDC API in 2026); "
                    "IDH1 separates the grades best, as expected for diffuse gliomas."
                ),
                evidence=mutated,
            ),
        ]
