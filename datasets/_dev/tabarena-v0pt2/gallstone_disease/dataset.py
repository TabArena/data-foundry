"""Curated dataset definition for `gallstone_disease` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

# Rows of dataset-uci.xlsx are counted from 0 after the header: the 161 people without gallstones come first (rows
# 0-160), then the 158 with gallstones (rows 161-318).
TARGET = "Gallstone Status"
TBFR, OBESITY, BMI = "Total Body Fat Ratio (TBFR) (%)", "Obesity (%)", "Body Mass Index (BMI)"
ECW, ICW, ECF_TBW = (
    "Extracellular Water (ECW)",
    "Intracellular Water (ICW)",
    "Extracellular Fluid/Total Body Water (ECF/TBW)",
)
VITAMIN_D, VMA = "Vitamin D", "Visceral Muscle Area (VMA) (Kg)"

# The decimals of the measured values. GFR is written to two decimals mostly for people without gallstones, and the
# filled cells carry up to 8 decimals in one group only, so the number format would give the group away.
MEASURED_PRECISION = {
    "Glomerular Filtration Rate (GFR)": 0,
    VITAMIN_D: 1,
    VMA: 1,
    "C-Reactive Protein (CRP)": 2,
    "Creatinine": 2,
}


def straight_line_fills(s: pd.Series) -> pd.Series:
    """Cells on a straight line between the cells above and below.

    A cell whose step from the row above equals its step to the row below (and is not zero), in a run of two or more
    such cells, or alone when the step is finer than the column's 0.01 precision. It finds the fills in vitamin D,
    visceral muscle area, GFR, CRP and creatinine (curation comments); in bone mass, ALT, glucose and ECF/TBW it also
    flags runs of round values that are measured or could be chance.
    """
    step_in, step_out = s.diff(), -s.diff(-1)
    hit = ((step_in - step_out).abs() < 1e-6 * s.abs().clip(lower=1)) & (step_in.abs() > 1e-9)
    run_size = hit.groupby((hit != hit.shift()).cumsum()).transform("size")
    finer = (step_in * 100 - (step_in * 100).round()).abs() > 1e-6
    return hit & ((run_size >= 2) | finer)


def recording_traits(df: pd.DataFrame) -> pd.DataFrame:
    """The four ways a second recording route writes the body-composition values, one boolean column each."""

    def whole(col: str) -> pd.Series:
        return (df[col] - df[col].round()).abs() < 1e-9

    return pd.DataFrame(
        {
            "body fat % at two decimals": (df[TBFR] * 10 - (df[TBFR] * 10).round()).abs() > 1e-6,
            "water in whole kg": whole(ECW) & whole(ICW),
            "ECF/TBW with decimals": ~whole(ECF_TBW),
            "obesity % not from BMI": (df[OBESITY] - (df[BMI] / 22 - 1).abs() * 100).abs() > 1,
        }
    )


def second_route(df: pd.DataFrame) -> pd.Series:
    """Rows with at least two of the four traits: 72 of the 158 with gallstones and 5 of the 161 without."""
    return recording_traits(df).sum(axis=1) >= 2


class GallstoneDisease(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does an outpatient have gallstone disease?",
        use_case=(
            "An internal-medicine clinic screens outpatients for gallstone disease from a body-composition scan and "
            "routine blood tests, for example to decide who goes on to imaging (the source paper's aim is early "
            "prediction)."
        ),
        row=(
            "One outpatient seen at the Internal Medicine Outpatient Clinic of Ankara VM Medical Park Hospital, Turkey, "
            "June 2022 to June 2023, who still had a gallbladder (the study left out 134 of 454 whose gallbladder had "
            "been removed); 242 of the 319 in the file, without those recorded through a second route."
        ),
        # 1 = gallstones, as the paper's coding and its sex counts say; the UCI page has it reversed ("0 (Yes)"), but
        # class 1 has the known risk factors (more women, more body fat, higher CRP, lower vitamin D, more diabetes).
        predicted=(
            "Whether the person was diagnosed with gallstone disease (coded 1; 86 of 242, about a third); how it was "
            "diagnosed is not stated."
        ),
        known=(
            "Age, sex, other illnesses (coronary disease, hypothyroidism, diabetes), height and "
            "weight, body composition from bioimpedance (water, fat, muscle, bone, visceral fat), the fatty-liver "
            "grade from ultrasound, and blood tests (sugar, lipids, liver and kidney values, inflammation, "
            "haemoglobin, vitamin D)."
        ),
        split="Random people, so the test data stands for new patients of the same clinic and year.",
        fit="approximate",
        fit_reason=(
            "The values are measured at the visit where the diagnosis is made, but the fatty-liver grade comes from "
            "the ultrasound that also finds gallstones, and the two groups were recorded apart: vitamin D for all "
            "with gallstones and half of the others, and most with gallstones through a second recording route "
            "(dropped here)."
        ),
    )

    # Dataset
    unique_name = "gallstone_disease"
    year = "2025"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://archive.ics.uci.edu/dataset/1150/gallstone-1"  # the paper says its data are not public
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/1150/gallstone-1.zip && unzip gallstone-1.zip && rm gallstone-1.zip && unzip dataset-uci.zip && rm dataset-uci.zip && mkdir -p local-data-warehouse/gallstone_disease && mv dataset-uci.xlsx local-data-warehouse/gallstone_disease/
    """
    bibtex = r"""
        @article{esen2024early,
          title={Early prediction of gallstone disease with a machine learning-based method from bioimpedance and laboratory data},
          author={Esen, {\.I}rfan and Arslan, Hilal and Esen, Selin Akt{\"u}rk and G{\"u}l{\c{s}}en, Mervenur and K{\"u}ltekin, Nimet and {\"O}zdemir, O{\u{g}}uzhan},
          journal={Medicine},
          volume={103},
          number={8},
          pages={e37258},
          year={2024},
          publisher={LWW}
        }
    """
    curation_comments = """
        We start with dataset-uci.xlsx from UCI: 319 outpatients, the 161 without gallstones first (rows 0-160), then the 158 with. 1 = gallstones, as in the paper; the UCI page has the coding reversed. We change what lets a model tell the groups apart for reasons other than gallstones, and document the rest. ROC AUC is for 3-fold x 20 random splits: on the UCI file TabPFN 3.5 reaches 0.913 and logistic regression 0.857; here TabPFN 3.5 0.838, gradient boosting 0.778, random forest 0.773 and logistic regression 0.762. The task probes flag `no_spread` (their untuned linear model, random forest and LightGBM reach 0.754-0.768), but methods spread: TabPFN 3.5 beats the other three by 0.06-0.08 on 92-93% of the splits.

        - We drop 77 rows (72 with gallstones, 5 without) recorded through a second route: at least two of body-fat % at two decimals, extracellular and intracellular water in whole kilograms, ECF/TBW (extracellular share of body water) with decimals, and an obesity % that is not the BMI-based degree of obesity (decision table). Their ECF/TBW is lower although they are heavier, and models recognise them: with these rows, TabPFN 3.5 separates them from the people without gallstones at 0.993 and the other people with gallstones at 0.842, and gives the 5 recorded this way without gallstones a mean gallstone probability of 0.77 (0.22 for the others). They cannot be aligned with the other rows: only 5 people without gallstones were recorded this way.
        - We drop hyperlipidemia: it is set for 8 with gallstones and nobody without, although total cholesterol of 240 mg/dL or more is as common (32 of 158 with, 35 of 161 without), so it was recorded for one group only.
        - We write five columns at the precision of their measured values: GFR (kidney filtration rate) in whole numbers, vitamin D and visceral muscle area to one decimal, CRP and creatinine to two. GFR was written to two decimals for 80% of those without gallstones and 15% of those with, and the filled cells (next point) carry up to 8 decimals in one group only. The number format alone gives ROC AUC 0.947 on the UCI file and 0.557 here.
        - Kept: 134 cells filled with straight lines between the rows above and below (figure), although the UCI page calls the file complete: vitamin D 77 (all without gallstones), visceral muscle area 35 (all with), GFR 13 (all with), CRP 6 and creatinine 3. They come from neighbours of the same group but do not carry the label: re-imputed from the other features inside each training fold, without the label, TabPFN 3.5 reaches 0.864 and logistic regression 0.744. Set to missing instead, the gaps would mark the groups, since they follow them: vitamin D was measured for all 86 with gallstones but only 79 of the 156 without.
        - Kept: runs of round values that the same test flags in bone mass, ALT and glucose (could be chance) and in ECF/TBW (each equals the rounded 100 x ECW / TBW, so measured).
        - Kept: the fatty-liver grade (hepatic fat accumulation), which the paper grades on the ultrasound that also finds gallstones. Without it TabPFN 3.5 reaches 0.834, logistic regression 0.763.
        - Kept: data-entry errors such as GFR 11.34 in row 117 (the CKD-EPI 2021 equation gives 111.34), triglyceride 1.39 in row 127 and total body water that is not extracellular + intracellular water in rows 168, 178 and 300. CRP is exactly 0 for 58% of those without gallstones and 28% of those with; both groups also have small nonzero values, so these are low values, not a recording habit.
        - The rows are sorted by class and, among those without gallstones, by sex; the base class shuffles them.
    """

    # Task
    target = TARGET
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "dataset-uci.xlsx", sheet_name="dataset", engine="calamine")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. The second recording route, found on the file's values (decision table).
        df = df[~second_route(df)]
        # 2. Recorded for people with gallstones only.
        df = drop_columns(df, ["Hyperlipidemia"])
        # 3. The precision of the measured values.
        return df.round(MEASURED_PRECISION)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Coronary Artery Disease (CAD)",
                "Hypothyroidism",
                "Gender",
                "Comorbidity",
                "Diabetes Mellitus (DM)",
            ],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 1, figsize=(8, 4.5), sharex=True)
        rows = np.arange(len(raw))
        for ax, col in zip(axes, [VITAMIN_D, VMA]):
            filled = straight_line_fills(raw[col]).to_numpy()
            ax.plot(rows, raw[col], lw=0.7)
            ax.plot(rows[filled], raw[col][filled], "o", ms=2.5, color="tab:red", label="filled cell")
            ax.axvspan(161, len(raw), color="tab:orange", alpha=0.15, lw=0)
            ax.set_ylabel(col.replace(" (Kg)", ""))
        axes[0].legend(loc="upper right", frameon=False)
        axes[1].set_xlabel("row of dataset-uci.xlsx (shaded: with gallstones)")
        fig.tight_layout()

        label = raw[TARGET].map({0: "without gallstones", 1: "with gallstones"})
        traits = recording_traits(raw)
        group = np.where(second_route(raw), "second route, ", "other rows, ") + label
        routes = traits.groupby(group).mean().T.round(2)
        routes.loc["ECF/TBW median"] = raw[ECF_TBW].groupby(group).median().round(1)
        routes.loc["BMI median"] = raw[BMI].groupby(group).median().round(1)
        routes.loc["rows"] = pd.Series(group).value_counts()

        return [
            Decision(
                "A second recording route: 77 rows dropped",
                "Share of rows with each way of writing the body-composition values, by group; rows with at least two "
                "of the four form the second route.",
                routes,
            ),
            Decision(
                "Cells filled from the neighbouring rows: kept",
                "Vitamin D and visceral muscle area along the file; the filled cells lie on straight lines between "
                "their neighbours.",
                fig,
            ),
        ]
