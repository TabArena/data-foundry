"""Curated dataset definition for `glioma_grading_clinical_and_mutation_features` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, drop_columns

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
        We start with TCGA_GBM_LGG_Mutations_all.csv, the original file of UCI dataset 759 (Tasci et al. 2022): 862 patients of the TCGA lower-grade glioma (TCGA-LGG) and glioblastoma (TCGA-GBM) projects, with sex, race, age at diagnosis and the mutation status of the 20 genes mutated most often in these patients.

        - Prediction point: a diffuse glioma has been resected or biopsied and its DNA sequenced; the model assigns the grade class, lower-grade glioma (WHO grade II or III) or glioblastoma (grade IV), from the 20 mutation flags and the patient's sex, race and age. This is the source's task.
        - Target: `Grade` is the TCGA project of every row, so the label is the histological diagnosis that put a tumour in one of the two projects. We keep the labels LGG and GBM.
        - We drop `Project` (a copy of the label), `Primary_Diagnosis` (the histology the grade follows from; decision table) and `Case_ID` (the TCGA patient barcode, one row per patient, whose tissue source site gives the label: each of the 45 sites sent patients to one project only).
        - IID split: the features do not carry the site, since holding out whole sites scores like a random split (logistic regression ROC AUC 0.919 against 0.918).
        - The mutation flags are the GDC's open-access somatic calls from whole-exome sequencing for every patient (decision table). The 70 patients with no mutation in the 20 genes have 3 to 110 calls in other genes, so `NOT_MUTATED` is a wildtype call. The flags, sex and race are categories. The authors chose the 20 genes by mutation frequency in all patients, without the label.
        - `Age_at_diagnosis` is a GDC text such as "51 years 108 days"; we convert it to years as years + days / 365.25, which gives the GDC's day count within one day.
        - `--` (4 patients without a clinical record) and `not reported` (race of 18 patients) become missing. We keep these patients, which the authors' preprocessed file TCGA_InfoWithGrade.csv (OpenML 46604) drops.
        - Note: the grades are histological, from diagnoses between 1989 and 2013, and WHO 2021 regrades some of these tumours with markers the data lacks. Without IDH1 and IDH2 the models keep ROC AUC 0.888 (logistic regression) and 0.893 (random forest), so the label is not built from the features; we keep the source's label.
        - Note: lgg_low_grade_glioma and glioblastoma share TCGA patients with this file (240 of 247 and 180 of 274) but predict molecular subtypes within one grade from omics profiles; the overlap matters only for a method trained across datasets.
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
