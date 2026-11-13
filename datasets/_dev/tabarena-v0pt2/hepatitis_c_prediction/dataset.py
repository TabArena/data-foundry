"""Curated dataset definition for `hepatitis_c_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode, drop_columns

ROUNDED_LABS = ["ALB", "AST", "BIL", "CREA", "GGT", "PROT"]


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Category": ["blood donor", "hepatitis", "fibrosis", "cirrhosis"],
}


class HepatitisCPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a person's blood panel show hepatitis C liver disease, and at which stage?",
        use_case=(
            "For example, a laboratory physician reads a standard blood panel and flags whether the person is healthy"
            " or has hepatitis C with inflammation, fibrosis or cirrhosis, to decide on further tests (the source "
            "paper builds laboratory diagnostic pathways)."
        ),
        row=(
            "One person, either a blood donor or a hepatitis C patient (608 people); the place and period are not "
            "stated in the definition."
        ),
        predicted=("One of four classes: blood donor (88%), hepatitis (4%), fibrosis (3%) or cirrhosis (5%)."),
        known=(
            "Age, sex and eight blood values: albumin, total protein, bilirubin, two liver enzymes (AST and GGT), "
            "cholinesterase, cholesterol and creatinine."
        ),
        split="Random people of the same collection.",
        changes=(
            "We drop the 'suspect blood donor' class. Donor and patient rows were recorded with different precision, "
            "which gave the class away, so we round six values to whole numbers and drop alkaline phosphatase, "
            "missing only for patients, and ALT, recorded another way for most patients."
        ),
        fit="approximate",
        fit_reason=(
            "The rows join two groups recorded apart, healthy blood donors and hepatitis C patients, a mixture no "
            "single laboratory sees; the format differences we removed show that the groups were recorded "
            "differently, and other such differences may remain. The stage task within the patients is real."
        ),
    )

    # Dataset
    unique_name = "hepatitis_c_prediction"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5D612",
            license="CC BY 4.0",
            year="2020",
            bibtex="""
                @article{hoffmann2018using,
                  title={Using machine learning techniques to generate laboratory diagnostic pathways—a case study},
                  author={Hoffmann, Georg and Bietenbeck, Andreas and Lichtinghagen, Ralf and Klawonn, Frank},
                  journal={Journal of Laboratory and Precision Medicine},
                  volume={3},
                  number={6},
                  year={2018},
                  publisher={AME Publishing Company}
                }
            """,
        ),
    )
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/571/hcv+data.zip && unzip hcv+data.zip && rm hcv+data.zip && mkdir -p local-data-warehouse/hepatitis_c_prediction && mv hcvdat0.csv local-data-warehouse/hepatitis_c_prediction/
    """
    curation_comments = """
        We start with the data from UCI.

        - The hepatitis related classes were defined in the paper, but the blood donor class is not mentioned in it. It seems the paper might be related to a different task than the UCI release in the end. But it has the same features. Thus, after looking more into it, we adjust the classes. We drop the "suspect Blood Donor" class as we cannot map it to being part of a reasonable task. We thus treat the task as predicting whether a patient has one of three versions of hepatitis, or is "just" a blood donor.
        - The donor and patient rows were recorded under different precision conventions in the UCI source: ALB and BIL are whole numbers in about 100% of patient rows but about 10% of donor rows, CREA the other way round, and ALP is missing only for patients. These format cues alone separate patients from donors (ROC AUC 0.9997). We round ALB, AST, BIL, CREA, GGT and PROT to integers for all rows (at most +-0.5 on values in the tens to hundreds; BIL, the smallest, changes by 2.6% in the median) and drop ALP. CHE and CHOL are single-digit values without a class difference in precision, so they stay as recorded.
        - ALT is dropped (Andrej, 2026-11-10): in the 57 patients with ALP recorded its median is 4.9 to 12.8 U/L by stage, below the donors' 23.1, while AST is raised; the 18 patients without ALP have 66 to 114 U/L, as chronic hepatitis C gives. So most patients' ALT was recorded another way, and a model would learn low ALT with high AST as a sign of disease. The column cannot be repaired.
        - There are no exact or near duplicates (minimum standardised nearest-neighbour distance 0.20), so there is no evidence of several rows per patient.
        - The target (2026-11-01, CLEAN-25): `Category` ships its classes as words, blood donor < hepatitis < fibrosis <
          cirrhosis (the source's own labels without their code; ordered by the course of the disease).
        - Class-dependent recording (record marker `Class-dependent Recording`): donors and patients follow different precision conventions and ALP is missing only for patients, as described above; harmonised by the rounding and the drop of ALP; ALT, recorded another way for most patients, is dropped too. Before the rounding, BIL alone gives ROC AUC 0.881, and 0.954 with its number format; CREA 0.628, and 0.790 with its format.
        - Time basis: ForcedIIDFromTemporal: the people of the collection were sampled over time, and the file carries
          no date, so the time is lost. A dated release would test people sampled later.
    """

    # Task
    target = "Category"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason="Hoffmann et al. 2018 report overall and per-class accuracy under leave-one-out; 88% donors, so accuracy is dominated by donor vs patient; the suspect-donor class is dropped (MET-2). Original rejected: accuracy. log_loss is the multiclass fallback.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "hcvdat0.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["Unnamed: 0"])
        df = df[df["Category"] != "0s=suspect Blood Donor"].reset_index(drop=True)
        # Donor and patient rows follow different recording conventions (patients: whole numbers for ALB and BIL,
        # donors: whole numbers for CREA; ALP missing only for patients), which gives the class away. Round the lab
        # values in the tens and hundreds to integers for every row; CHE and CHOL are single digits and show no
        # class difference, so they stay as recorded.
        df[ROUNDED_LABS] = df[ROUNDED_LABS].round(0)
        df = drop_columns(df, ["ALP"])  # missing only for patients (0 of 533 donors)
        df = drop_columns(df, ["ALT"])  # recorded another way for most patients: below the donors' values
        # the target's classes in words (CLEAN-25): the source's class names
        df = decode(
            df,
            {
                self.target: {
                    "0=Blood Donor": "blood donor",
                    "1=Hepatitis": "hepatitis",
                    "2=Fibrosis": "fibrosis",
                    "3=Cirrhosis": "cirrhosis",
                }
            },
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "Sex",
            ],
        )
