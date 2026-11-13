"""Curated dataset definition for `indian_liver_patient_dataset` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode


class IndianLiverPatientDataset(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a patient have liver disease, judging from age, sex and routine blood tests?",
        use_case=(
            "For example, a doctor reads a patient's liver blood tests to decide whether to refer the patient for a "
            "liver work-up."
        ),
        row=(
            "One patient record from the north-east of Andhra Pradesh, India (406 liver patients and 164 others); the"
            " period is not stated."
        ),
        predicted=("Whether the record is of a liver patient (71%); how the diagnosis was made is not stated."),
        known=(
            "Age, sex, total and direct bilirubin, alkaline phosphatase, two liver enzymes (ALT and AST), total "
            "protein, albumin and the albumin-to-globulin ratio."
        ),
        split="Random patients, so the test data stands for new patients from the same collection.",
        fit="approximate",
        fit_reason=(
            "Liver patients and other patients were collected as two groups (71% liver patients), not as the "
            "patients a doctor sees; a physician labelled them, but the label's criterion is not stated, and the lab "
            "values contradict it for part of the records."
        ),
    )

    # Dataset
    unique_name = "indian_liver_patient_dataset"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5D02C",
            license="CC BY 4.0",
            year="2012",
            bibtex="""
                @article{ramana2012critical,
                  title={A critical comparative study of liver patients from USA and INDIA: an exploratory analysis},
                  author={Ramana, Bendi Venkata and Babu, M Surendra Prasad and Venkateswarlu, NB},
                  journal={International Journal of Computer Science Issues (IJCSI)},
                  volume={9},
                  number={3},
                  pages={506},
                  year={2012},
                  publisher={International Journal of Computer Science Issues (IJCSI)}
                }
            """,
        ),
    )
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/225/ilpd+indian+liver+patient+dataset.zip && unzip ilpd+indian+liver+patient+dataset.zip && rm ilpd+indian+liver+patient+dataset.zip
        mkdir -p local-data-warehouse/indian_liver_patient_dataset && mv "Indian Liver Patient Dataset (ILPD).csv" local-data-warehouse/indian_liver_patient_dataset/
    """
    curation_comments = """
        - Label and source (2026-11-11, PROV-2, USE-8): the values are real lab reports, transcribed by hand: the
          albumin-to-globulin ratio equals albumin / (total protein - albumin) cut to one decimal in 471 of 566 rows,
          ages and enzymes heap on numbers ending in 0 or 5, the 13 copies sit on adjacent rows, and nothing looks
          generated. A physician labelled them (Ramana et al. 2011 thank Dr. Bevera Lakshmana Rao "in labeling
          samples"), on a criterion not stated; the hospital and period are not stated either, and the 583 records
          are a subset, chosen in an unstated way, of the 751 of that paper. The others are other patients tested,
          not healthy people (median albumin 3.4 g/dL). The lab values contradict the label for part of the 583
          records: 85 of the 167 others have low albumin and 18 high bilirubin or liver enzymes, and 55 of the 416
          patients have normal bilirubin, ALT, AST and albumin. The number format of the values gives ROC AUC 0.50
          for the label, so no recording difference shows between the two groups.
        - Time basis: ForcedIIDFromTemporal: patients seen over a period the sources do not state; the file keeps no
          date, so random patients stand in for the patients to come. The file order carries some structure (lag-1
          correlation of 0.10 to 0.26 for age and the lab values, none for the label: 0.03) but no cost: held out by
          file position (contiguous 5-fold, or the last third after the first two) ROC AUC stays within the spread
          of random splits for logistic regression, random forest and TabPFN 3.5. A dated release would test later
          patients and whether the two groups were collected in different periods, which this split cannot.
        - Repeated records (2026-11-11, LEAK-18, LEAK-19): 13 records appear twice, equal in age, sex and all eight
          blood tests and with the same label; each pair sits on adjacent rows of the UCI file (rows 19/20 to 201/202),
          and none of 500 tables with each column shuffled on its own held a repeated row. They are one record
          entered twice, so the second copy is dropped: 583 to 570 rows, 10 liver patients and 3 others; the patient
          share moves from 71.4% to 71.2%.
        - Impossible values (2026-11-11, CLEAN-11): direct bilirubin is part of total bilirubin, yet it is the larger
          in 3 rows: both bilirubin values are set to missing there. The albumin-to-globulin ratio follows from
          albumin and total protein (globulin = total protein - albumin); where the published ratio differs from
          that by more than 0.2 (8 rows after the drop) it is set to missing. The rows stay.
        - Ages above 89 are recorded as 90 (UCI); this concerns 1 row and is kept as published.
        - The target (2026-11-01, CLEAN-25): `Selector` ships its classes as words (1 means a liver patient (UCI)).
          Binary: "Yes" is the event, the class that sorts second, so it is the metrics' positive class.
    """

    # Task
    target = "Selector"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The UCI page defines no task metric and the cited paper (Ramana et al. 2012) is a statistical "
            "comparison of the USA and India patient groups, not a benchmark with a declared score; later "
            "uses report accuracy only."
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(
            raw_dir / "Indian Liver Patient Dataset (ILPD).csv",
            header=None,
            names=["Age", "Gender", "TB", "DB", "Alkphos", "Sgpt", "Sgot", "TP", "ALB", "A/G", "Selector"],
        )
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # each of the 13 repeated records is one record entered twice on adjacent rows (LEAK-18, LEAK-19)
        df = raw.drop_duplicates().reset_index(drop=True)
        # impossible values become missing, the row stays (CLEAN-11)
        df = df.astype({"TB": "float64", "DB": "float64", "A/G": "float64"})
        bili_bad = df["DB"] > df["TB"]
        df.loc[bili_bad, ["TB", "DB"]] = float("nan")
        ag_bad = (df["A/G"] - df["ALB"] / (df["TP"] - df["ALB"])).abs() > 0.2
        df.loc[ag_bad, "A/G"] = float("nan")
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"1": "Yes", "2": "No"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Gender",
            ],
        )
