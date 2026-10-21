"""Curated dataset definition for `2_month_survival_rate_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

# Columns of support2.csv that are not features at the prediction point (study day 3), with the reason.
DROPPED_COLUMNS = {
    "death": "outcome: death by 31 Dec 1994 (builds the target)",
    "d.time": "outcome: days of follow-up, ends at death or censoring (builds the target)",
    "hospdead": "outcome: death in hospital",
    "slos": "outcome: days from study entry to discharge",
    "sfdm2": "outcome: functional disability at 2 months; level 5 is death before 2 months",
    "charges": "recorded at discharge: hospital charges of the whole stay",
    "totcst": "recorded at discharge: total ratio-of-costs-to-charges cost",
    "totmcst": "recorded at discharge: total micro-cost",
    "avtisst": "recorded after day 3: average TISS score over days 3-25",
    "dnr": "DNR order; 1,659 of the 2,956 orders written after study entry are dated after day 3",
    "dnrday": "day of the DNR order; equals slos for every patient without one",
    "sps": "SUPPORT physiology score: SUPPORT model output, fit on phase I survival",
    "surv2m": "SUPPORT model 2-month survival estimate (fit on phase I survival)",
    "surv6m": "SUPPORT model 6-month survival estimate (fit on phase I survival)",
    "aps": "APACHE III physiology score (phase I with imputed BUN and urine output)",
    "prg2m": "physician's 2-month survival estimate",
    "prg6m": "physician's 6-month survival estimate",
    "adls": "surrogate ADL interview (days 2-7): missing when the stay ended before the interview",
    "adlsc": "adls, else calibrated adlp, else imputed with the interview status (which records a death or discharge)",
}


# The day-3 physiology block of support2.csv, contiguous in the file. In most phase II rows it holds another patient's
# values; `_source_rows` finds the row that holds each patient's own. bun, glucose and urine were not measured in phase I.
PHYSIOLOGY = [
    "meanbp",
    "wblc",
    "hrt",
    "resp",
    "temp",
    "pafi",
    "alb",
    "bili",
    "crea",
    "sod",
    "ph",
    "glucose",
    "bun",
    "urine",
]
PHASE_2_LABS = ["bun", "glucose", "urine"]
PHASE_1_PATIENTS = 4301  # Knaus et al. 1995, abstract: "4301 hospitalized adults were selected for phase I"

# The ICPSR 2957 (V2) public-use files we read, and the 1-based column ranges of the variables we use (from the data
# maps 02957-0010-Data_map.txt and 02957-0009-Data_map.txt). No ICPSR value goes into the dataset: part 10 links each
# support2 row to its patient (`_link`) and part 9 tells which support2 row holds the patient's day-3 physiology.
ICPSR_KEY_FILE = "icpsr_2957/ICPSR_02957/DS0010/02957-0010-Data.txt"
ICPSR_PHYSIOLOGY_FILE = "icpsr_2957/ICPSR_02957/DS0009/02957-0009-Data.txt"
ICPSR_KEY_COLUMNS = {  # part 10, key common analytical variables
    "PSEUDOID": (1, 5),
    "AGE": (6, 17),
    "SEX": (20, 20),
    "DEATH": (23, 23),  # for the checks only, not the link: ICPSR follows to 1997
    "HOSPDEAD": (24, 24),
    "SLOS": (25, 27),
    "D_TIME": (28, 31),  # for the checks only
    "HDAY": (32, 34),
    "DZGROUP": (35, 35),
    "NUM_CO": (39, 39),
    "SCOMA3": (66, 68),
    "SPS3": (343, 353),
    "APS3": (404, 406),
}
ICPSR_DAY_3_COLUMNS = {  # part 9, physiology: the day-3 value of each column of PHYSIOLOGY
    "PSEUDOID": (1, 5),
    "meanbp": (51, 55),  # MEANBP3
    "wblc": (83, 94),  # WBLC3
    "hrt": (143, 154),  # HRT3
    "resp": (185, 186),  # RESP3
    "temp": (214, 224),  # TEMP3
    "pafi": (391, 403),  # PAFI3
    "alb": (454, 464),  # ALB3
    "bili": (588, 598),  # BILI3
    "crea": (643, 653),  # CREA3
    "sod": (690, 692),  # SOD3
    "ph": (823, 832),  # PH3
    "glucose": (942, 954),  # GLUCOSE3
    "bun": (995, 1006),  # BUN3
    "urine": (1047, 1059),  # URIN3
}
# ICPSR fills a missing physiology value with the previous day's value or else a normal value (codebook, Appendix B;
# bun and urine as in hbiostat's supportdesc), stored as float32; support2.csv has the normal-value fills as missing.
ICPSR_NORMAL_FILLS = {
    "wblc": 9.0,
    "pafi": 333.3125,
    "alb": 3.5,
    "bili": 1.00976563,
    "crea": 1.00976563,
    "bun": 6.50976563,
    "urine": 2502.0,
}
DZGROUP_CODES = {  # support2's disease group names and ICPSR's codes (DZGROUP 0: HELP patients, not in SUPPORT)
    "ARF/MOSF w/Sepsis": 1,
    "COPD": 2,
    "CHF": 3,
    "Cirrhosis": 4,
    "Coma": 5,
    "Colon Cancer": 6,
    "Lung Cancer": 7,
    "MOSF w/Malig": 8,
}


def _read_icpsr(path: Path, columns: dict[str, tuple[int, int]]) -> pd.DataFrame:
    """Read the given columns of an ICPSR fixed-width (LRECL) data file; blank and "." are missing."""
    df = pd.read_fwf(
        path, colspecs=[(a - 1, b) for a, b in columns.values()], names=list(columns), dtype=str, header=None
    )
    numeric = {c: pd.to_numeric(df[c].str.strip(), errors="coerce") for c in columns if c != "PSEUDOID"}
    return df.assign(PSEUDOID=df["PSEUDOID"].str.strip(), **numeric)


def _link(support2: pd.DataFrame, icpsr_key: pd.DataFrame) -> pd.Series:
    """The ICPSR patient id (PSEUDOID) of each support2 row.

    Matched on ten columns that both files hold on the patient's own row and that together are unique; age in whole
    years, as the public ICPSR file truncates it to 20-95. Follow-up and death are not used: ICPSR follows the
    patients to 1997, support2 to the end of 1994.
    """
    ours = pd.DataFrame(
        {
            "SLOS": support2["slos"],
            "HOSPDEAD": support2["hospdead"],
            "HDAY": support2["hday"],
            "NUM_CO": support2["num.co"],
            "AGE": np.floor(support2["age"]).clip(20, 95),
            "DZGROUP": support2["dzgroup"].map(DZGROUP_CODES),
            "SEX": support2["sex"].map({"female": 0, "male": 1}),
            "SPS3": support2["sps"].round(3),
            "SCOMA3": support2["scoma"],
            "APS3": support2["aps"],
        }
    ).astype(float)
    theirs = icpsr_key[icpsr_key["DZGROUP"].gt(0)].assign(SPS3=lambda d: d["SPS3"].round(3))
    linked = ours.merge(theirs, on=list(ours.columns), how="left", validate="one_to_one")
    assert linked["PSEUDOID"].notna().all(), int(linked["PSEUDOID"].isna().sum())
    return pd.Series(linked["PSEUDOID"].to_numpy(), index=support2.index)


def _source_rows(support2: pd.DataFrame, icpsr_day_3: pd.DataFrame, pseudoid: pd.Series) -> pd.Series:
    """For each support2 row, the position of the support2 row that holds its patient's day-3 physiology block.

    The patient's ICPSR day-3 values, with the normal-value fills set missing as support2 has them, are looked up among
    the blocks of support2.csv (to 3 decimals). Every block is unique in the file, and every patient's is found once.
    """
    theirs = icpsr_day_3.set_index("PSEUDOID").loc[pseudoid.to_numpy(), PHYSIOLOGY]
    for column, fill in ICPSR_NORMAL_FILLS.items():
        theirs[column] = theirs[column].mask(np.isclose(theirs[column], fill))
    holder = pd.Series(
        np.arange(len(support2)), index=pd.util.hash_pandas_object(support2[PHYSIOLOGY].round(3), index=False)
    )
    assert holder.index.is_unique
    source = pd.Series(pd.util.hash_pandas_object(theirs.round(3), index=False).to_numpy()).map(holder)
    assert source.notna().all(), int(source.isna().sum())
    assert source.is_unique
    return pd.Series(source.to_numpy(dtype=int), index=support2.index)


def _restored(support2: pd.DataFrame, source: pd.Series) -> pd.DataFrame:
    """support2 with each row's physiology block taken from the row that holds it (values of support2.csv only)."""
    out = support2.copy()
    out[PHYSIOLOGY] = support2[PHYSIOLOGY].iloc[source.to_numpy()].to_numpy()
    return out


def _phase_1(raw: pd.DataFrame) -> pd.Series:
    """The phase I patients: the runs of at least 30 consecutive rows of the file without bun, glucose and urine.

    Phase I did not measure the three labs, and the file stores each phase of each block in one run. Eleven single
    phase II rows also lack all three; the run length keeps them out.
    """
    no_labs = raw[PHASE_2_LABS].isna().all(axis=1).to_numpy()
    run = np.r_[True, no_labs[1:] != no_labs[:-1]].cumsum()
    run_length = pd.Series(run).map(pd.Series(run).value_counts()).to_numpy()
    phase_1 = pd.Series(no_labs & (run_length >= 30), index=raw.index)
    assert phase_1.sum() == PHASE_1_PATIENTS, phase_1.sum()
    return phase_1


def _alive_after_day_3(df: pd.DataFrame) -> pd.Series:
    """Patients alive at the prediction point, the end of study day 3."""
    return ~(df["death"].eq(1) & df["d.time"].le(3))


class Dataset2MonthSurvivalRatePrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a seriously ill hospital patient die within two months?",
        use_case=(
            "On the third day after study entry, the care team estimates a patient's chance of dying within two months, to "
            "discuss prognosis and the goals of care."
        ),
        row=(
            "One adult patient of five US teaching hospitals (1989-1994) with one of eight serious diagnoses, such as"
            " heart failure, COPD or lung cancer, alive at the end of study day 3."
        ),
        predicted="Whether the patient dies within 60 days of study entry (33% do).",
        known=(
            "Age, sex, diagnosis, other illnesses, the day-3 vital signs and lab values, and a few background facts "
            "(education, income, function before admission)."
        ),
        split=("Random patients, so the test data stands for new patients of the same hospitals and years."),
        changes=(
            "In the public file the day-3 measurements of most phase II patients belong to other patients; we moved "
            "them back to their own rows with the study's archive. We drop the scores, physician estimates and orders"
            " made from or after these values."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is recorded by day 3 and the outcome follows within two months, as when the "
            "model is used. The care is that of 1989-1994."
        ),
    )

    # Dataset
    unique_name = "2_month_survival_rate_prediction"
    year = "2000"
    domain = "medical & healthcare"
    source = "Other"
    source_url = "https://hbiostat.org/data/repo/supportdesc"
    license = (
        'Free use with attribution: hbiostat.org/data states "Permission is granted to anyone wishing to use the '
        'data sets provided here" and asks to cite the original paper and Vanderbilt Biostatistics. Every value of the '
        "dataset comes from that file. The ICPSR 2957 public-use files, read only to find the rows of the phase II "
        "physiology, are under ICPSR's terms of use (no redistribution without ICPSR's written agreement; cite the "
        "study) and are not part of the dataset"
    )
    download_description = """
        Two downloads. Every value of the dataset comes from the first; the second only tells where each patient's physiology sits in it.

        1. support2.csv (all 9,105 SUPPORT patients, 47 variables) from the Vanderbilt Biostatistics data repository (https://hbiostat.org/data, "SUPPORT study datasets"), which released this extract of the SUPPORT study data. The file is not versioned: ours is dated 2003-06-23 inside the zip and has SHA-256 79621945edf2a5c8dc36359684ff356d3c6025e773ba4fefac26f865f7894c78. UCI dataset 880 (SUPPORT2, https://archive.ics.uci.edu/static/public/880/data.csv) serves the same table, with the same misplaced phase II physiology (see the curation notes); it differs only in the rounding of prg6m, which we drop.
        2. The full study data, ICPSR 2957 V2 (https://doi.org/10.3886/ICPSR02957.v2, Knaus and Lynn, released 2020-02-20): the public-use parts 9 ("Physiology Data, SUPPORT Phases I and II and HELP") and 10 ("Key Common Analytical Variables, SUPPORT Phases I and II and HELP"), as ASCII data with their data maps. ICPSR asks for a free login and the acceptance of its terms of use, so there is no download command: log in at https://www.icpsr.umich.edu/web/ICPSR/studies/2957, download DS9 and DS10 (each a zip with the folder ICPSR_02957) and unzip both into local-data-warehouse/2_month_survival_rate_prediction/icpsr_2957/. Ours: 02957-0009-Data.txt SHA-256 96859cd2860862d670379def714badcd314c90ea3445c6f6da38d1c32ad56b7d, 02957-0010-Data.txt SHA-256 1a9a41ba78ba13db60d9e4ce9347922f5f2fad77f386ef02ac802d9a7bb4fd86. ICPSR's terms forbid passing these files on.

        mkdir -p local-data-warehouse/2_month_survival_rate_prediction && cd local-data-warehouse/2_month_survival_rate_prediction && wget https://hbiostat.org/data/repo/support2csv.zip && unzip support2csv.zip && rm support2csv.zip
        # after downloading DS9 and DS10 from ICPSR (login), in the same folder:
        unzip -o <DS9 zip> -d icpsr_2957 && unzip -o <DS10 zip> -d icpsr_2957
    """
    bibtex = """
        @article{knaus1995support,
          title={The {SUPPORT} prognostic model: Objective estimates of survival for seriously ill hospitalized adults},
          author={Knaus, William A and Harrell, Frank E and Lynn, Joanne and Goldman, Lee and Phillips, Russell S and Connors, Alfred F and Dawson, Neal V and Fulkerson, William J and Califf, Robert M and Desbiens, Norman and others},
          journal={Annals of Internal Medicine},
          volume={122},
          number={3},
          pages={191--203},
          year={1995},
          doi={10.7326/0003-4819-122-3-199502010-00007},
          note={Data obtained from https://hbiostat.org/data courtesy of the Vanderbilt University Department of Biostatistics}
        }
        @misc{knaus2020supporticpsr,
          title={Study to Understand Prognoses and Preferences for Outcomes and Risks of Treatment ({SUPPORT}) and Hospitalized Elderly Longitudinal Project ({HELP}), 1989-1997},
          author={Knaus, William and Lynn, Joanne},
          publisher={Inter-university Consortium for Political and Social Research [distributor]},
          year={2020},
          note={ICPSR 2957, version V2, 2020-02-20; used to restore the row order of the phase II physiology},
          doi={10.3886/ICPSR02957.v2}
        }
    """
    curation_comments = """
        We start with support2.csv from the Vanderbilt Biostatistics data repository (hbiostat.org/data): the 9,105 patients of SUPPORT phases I (1989-1991) and II (1992-1994), seriously ill adults at five US teaching hospitals. We keep the 8,967 patients alive after study day 3.

        - Prediction point: the end of study day 3, as in the SUPPORT model ("11 physiologic measures recorded on day 3 after study entry", Knaus et al. 1995, abstract).
        - Physiology restored. In most phase II rows the day-3 physiology block (meanbp to urine, 14 columns) belongs to another patient: crea against aps, the APACHE III score of the same values, has Spearman 0.52 in phase I and 0.05 in phase II. The study data, ICPSR 2957 V2 parts 9 and 10, show where each block is. `_link` matches each row to its ICPSR patient on ten columns both files hold on the patient's row (all 9,105 match once, and the 6,201 deaths agree to the day). `_source_rows` finds the block that holds the patient's ICPSR day-3 values, with ICPSR's normal-value fills set missing as in support2: phase I rows hold their own and 431 of the 4,804 phase II rows do; for 4,102 others the block sits 1 to 90 rows further down, for 181 further still (up to 1,094 rows) and for 90 above. `_restored` moves each block back. Every value comes from support2.csv; ICPSR only decides the row and is not shipped. Restored, phase II matches phase I (crea against aps 0.49).
        - Both phases, IID split over patients: the use case is new patients of the same hospitals and years. The phase II intervention "failed to improve care or patient outcomes" (SUPPORT Principal Investigators 1995, JAMA, abstract). The entry date can be recovered (a survivor entered on 31 Dec 1994 minus d.time, and within each of the file's ten blocks the rows are in entry order, Spearman 1.000), but it changes no score (LightGBM ROC AUC, review panel 2026-10-20): IID 0.818 (9 splits), three temporal windows over phase II 0.824, phase I to phase II 0.820. The ten blocks form five phase I / phase II pairs, probably the hospitals (the public ICPSR file blanks the site); leaving one pair out scores 0.815 (0.793-0.831), so we do not group by them.
        - Target `death_within_2_months`: `death` = 1 and `d.time` < 60, the cut-off of the source's sfdm2 level 5. Survivors were followed at least 344 days, so no label is censored. 2,993 of 8,967 (33.4%).
        - We drop the 138 patients who died on day 3: they are dead at the prediction point, and their values include values at death (heart rate 0 in 38% of them).
        - Dropped as the source advises (supportdesc): the model outputs sps, surv2m, surv6m and aps, the physicians' estimates prg2m and prg6m, and dnr and dnrday (dnrday equals slos for every patient without an order, and 1,659 of the 2,956 orders written after study entry are dated after day 3).
        - Dropped as outcomes or fields recorded after day 3: death, d.time, sfdm2, hospdead, slos, charges, totcst, totmcst and avtisst.
        - Dropped: bun, glucose and urine, which phase I did not measure.
        - Dropped: adls and adlsc. The ADL answers describe function two weeks before admission, but the interviews took place on days 2-7 (median day 4), and adls is missing for 46% of the patients whose stay ended by day 7 against 24% of longer stays. adlsc is adls, or calibrated adlp, or an imputation that used the interview status ("Pt Death", "Pt Discharged"; codebook Appendix A). We keep adlp, edu and income (CC 2026-10-12). adlp is missing mostly when the patient cannot answer (coma, intubation), but its gaps also hold the 475 patients whose interview status in ICPSR part 10 is "Pt Death", all of whom die within 2 months: 95.4% of the 767 deaths on days 4-7 lack adlp against 58.2% of the other patients, worth 0.0035 ROC AUC. edu and income are missing about as often for short as for long stays, but more often among the deaths on days 4-7 (edu 31.4% against 16.3%, income 43.0% against 31.5%), with no measurable effect (dropping both changes ROC AUC by 0.0001). Decision table.
        - We rename num.co to num_co.
        - Anomaly: heart rate 0 (30 patients), mean blood pressure 0 (16) and respiration rate 0 (30) remain among the patients alive after day 3. Most of them die within 2 months, so these look like arrests on day 3; we keep them. wblc 0 (9 patients, 8 with MOSF w/Malig) stays too: the smallest non-zero values are 0.05, 0.07 and 0.08, so 0 reads as a count below the lab's resolution in profound neutropenia.
        - alb above 6 g/dL (4 patients: 6.3, 8.6, 10.9 and 29.0) is set missing: serum albumin does not reach such values (29.0 reads as g/L).
        - Note: dzclass groups the eight dzgroup values into four classes; both are kept as in the source. No duplicate rows.
    """

    # Task
    target = "death_within_2_months"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            # the first, unnamed column is the row number 1..9105
            "support2": pd.read_csv(raw_dir / "support2.csv", index_col=0),
            "icpsr_key": _read_icpsr(raw_dir / ICPSR_KEY_FILE, ICPSR_KEY_COLUMNS),
            "icpsr_day_3": _read_icpsr(raw_dir / ICPSR_PHYSIOLOGY_FILE, ICPSR_DAY_3_COLUMNS),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        support2 = raw["support2"]
        # 1. each row's day-3 physiology from the row of support2.csv that holds it: in most phase II rows the block
        # belongs to another patient. The ICPSR files only say which row that is; every value comes from support2.csv
        source = _source_rows(support2, raw["icpsr_day_3"], _link(support2, raw["icpsr_key"]))
        df = _restored(support2, source)
        # serum albumin above 6 g/dL is impossible (4 patients; 29.0 reads as g/L)
        df["alb"] = df["alb"].mask(df["alb"].gt(6))
        # 2. the patients alive at the prediction point, the end of study day 3
        df = df[_alive_after_day_3(df)]
        # 3. death before day 60 after study entry, the cut-off of the source's sfdm2 level 5
        died_before_day_60 = df["death"].eq(1) & df["d.time"].lt(60)
        df[self.target] = died_before_day_60.map({True: "Yes", False: "No"})
        # 4. outcomes, fields recorded after day 3, earlier models' outputs, the physicians' estimates, the surrogate
        # interview fields, and the three labs phase I did not measure
        df = drop_columns(df, [*DROPPED_COLUMNS, *PHASE_2_LABS])
        return df.rename(columns={"num.co": "num_co"})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["sex", "dzgroup", "dzclass", "income", "race", "diabetes", "dementia", "ca"],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        from sklearn.metrics import roc_auc_score

        def auc_alone(x: pd.Series, y: pd.Series) -> float:
            # ROC AUC of one column on its non-missing rows, in the better direction
            keep = x.notna()
            if not keep.any():
                return np.nan
            auc = roc_auc_score(y[keep], x[keep])
            return max(auc, 1 - auc)

        support2 = raw["support2"]
        pseudoid = _link(support2, raw["icpsr_key"])
        source = _source_rows(support2, raw["icpsr_day_3"], pseudoid)
        restored = _restored(support2, source)
        phase_1 = _phase_1(support2)
        phase_2 = ~phase_1
        alive = _alive_after_day_3(support2)
        y_all = (support2["death"].eq(1) & support2["d.time"].lt(60)).astype(int)

        # 1. the physiology against aps, the APACHE III score computed from the same day-3 values, and alone for the
        # target, as published and restored
        def rho(frame: pd.DataFrame, rows: pd.Series, column: str) -> float:
            return frame.loc[rows, column].corr(frame.loc[rows, "aps"], method="spearman")

        alignment = pd.DataFrame(
            {
                "phase I: rho with aps": {c: rho(support2, phase_1, c) for c in PHYSIOLOGY},
                "phase II as published: rho with aps": {c: rho(support2, phase_2, c) for c in PHYSIOLOGY},
                "phase II restored: rho with aps": {c: rho(restored, phase_2, c) for c in PHYSIOLOGY},
                "phase I: ROC AUC alone": {
                    c: auc_alone(support2.loc[phase_1 & alive, c], y_all[phase_1 & alive]) for c in PHYSIOLOGY
                },
                "phase II as published: ROC AUC alone": {
                    c: auc_alone(support2.loc[phase_2 & alive, c], y_all[phase_2 & alive]) for c in PHYSIOLOGY
                },
                "phase II restored: ROC AUC alone": {
                    c: auc_alone(restored.loc[phase_2 & alive, c], y_all[phase_2 & alive]) for c in PHYSIOLOGY
                },
            }
        ).round(3)
        alignment = alignment.astype(object).where(alignment.notna(), "not measured")
        alignment.index.name = "column"

        # 2. where each block of the file took its physiology from (offset: source row minus the row)
        position = np.arange(len(support2))
        rows = pd.DataFrame(
            {
                "block": np.r_[0, np.cumsum(phase_1.to_numpy()[1:] != phase_1.to_numpy()[:-1])],
                "row": position + 1,
                "phase": np.where(phase_1, "I", "II"),
                "offset": source.to_numpy() - position,
            }
        )
        blocks = rows.groupby("block").agg(
            rows=("row", lambda r: f"{r.min():,}-{r.max():,}"),
            phase=("phase", "first"),
            patients=("row", "size"),
            own_physiology=("offset", lambda o: int(o.eq(0).sum())),
            offset_min=("offset", "min"),
            offset_median=("offset", "median"),
            offset_max=("offset", "max"),
        )
        icpsr = raw["icpsr_key"].set_index("PSEUDOID").loc[pseudoid.to_numpy()].set_axis(support2.index)
        died = support2["death"].eq(1)
        checks = pd.Series(
            {
                "support2 rows linked to one ICPSR patient": f"{pseudoid.nunique():,} of {len(support2):,}",
                "support2 deaths with the same day of death in ICPSR": (
                    f"{int((icpsr.loc[died, 'DEATH'].eq(1) & icpsr.loc[died, 'D_TIME'].eq(support2.loc[died, 'd.time'])).sum()):,}"
                    f" of {int(died.sum()):,}"
                ),
                "support2 survivors who died after 1994 (ICPSR follows to 1997)": (
                    f"{int(icpsr.loc[~died, 'DEATH'].eq(1).sum()):,}, the earliest on day "
                    f"{int(icpsr.loc[~died & icpsr['DEATH'].eq(1), 'D_TIME'].min()):,}"
                ),
                "phase I rows holding their own physiology": f"{int((source[phase_1] == position[phase_1]).sum()):,} of {int(phase_1.sum()):,}",
                "phase II rows holding their own physiology": f"{int((source[phase_2] == position[phase_2]).sum()):,} of {int(phase_2.sum()):,}",
            },
            name="result",
        ).rename_axis("check")

        # 3. the dropped columns and why
        dropped = pd.Series(DROPPED_COLUMNS, name="why").rename_axis("column").to_frame()

        # 4. all patients by day of death, with the restored physiology
        day = restored["d.time"].where(restored["death"].eq(1))
        bins = pd.cut(day, [2, 3, 4, 5, 7, 59, float("inf")], labels=["3", "4", "5", "6-7", "8-59", "60+"])
        when = bins.cat.add_categories("alive").fillna("alive").rename("day of death")
        by_day = pd.DataFrame(
            {
                "patients": restored.groupby(when, observed=True).size(),
                "heart rate 0": restored["hrt"].eq(0).groupby(when, observed=True).mean().round(3),
                "mean BP 0": restored["meanbp"].eq(0).groupby(when, observed=True).mean().round(3),
                "adls missing": restored["adls"].isna().groupby(when, observed=True).mean().round(3),
                "adlp missing": restored["adlp"].isna().groupby(when, observed=True).mean().round(3),
                "prg2m missing": restored["prg2m"].isna().groupby(when, observed=True).mean().round(3),
            }
        )

        # 5. the interview fields: missing shares by whether the stay ended (death or discharge) by study day 7, and by
        # death on study days 4-7
        alive_cohort = restored[_alive_after_day_3(restored)]
        ended = alive_cohort["slos"].le(7).map({True: "stay ended by day 7", False: "longer stay"})
        died_early = (alive_cohort["death"].eq(1) & alive_cohort["d.time"].le(7)).map(
            {True: "died on days 4-7", False: "all other patients"}
        )
        missing = alive_cohort[["adlp", "adls", "adlsc", "edu", "income"]].isna()
        interviews = (
            pd.concat([missing.groupby(ended).mean().T, missing.groupby(died_early).mean().T], axis=1)
            .round(3)
            .rename_axis("missing share")
        )
        interviews["kept"] = ["yes", "no", "no", "yes", "yes"]

        # 6. the candidate targets on the cohort
        cohort = restored[_alive_after_day_3(restored)]
        y = cohort["death"].eq(1) & cohort["d.time"].lt(60)
        follow_up = cohort.loc[cohort["death"].eq(0), "d.time"]
        targets = pd.DataFrame(
            {
                "definition": {
                    "death within 2 months (shipped)": "death = 1 and d.time < 60",
                    "death within 6 months": "death = 1 and d.time < 180",
                    "death in hospital": "hospdead = 1",
                    "death by 31 Dec 1994": f"death = 1 (follow-up {follow_up.min()}-{follow_up.max()} days)",
                },
                "positives": {
                    "death within 2 months (shipped)": int(y.sum()),
                    "death within 6 months": int((cohort["death"].eq(1) & cohort["d.time"].lt(180)).sum()),
                    "death in hospital": int(cohort["hospdead"].sum()),
                    "death by 31 Dec 1994": int(cohort["death"].sum()),
                },
            }
        )
        targets["share"] = (targets["positives"] / len(cohort)).round(3)
        return [
            Decision(
                "Phase II physiology restored: published in other patients' rows",
                "In most phase II rows of support2.csv the day-3 physiology block (meanbp to urine) holds another "
                "patient's values. Each row now takes its block from the row that holds it, found with the public "
                "ICPSR 2957 files; the values are those of support2.csv. As published, the phase II columns do not "
                "correlate with aps, the APACHE III score of the same day-3 values, and carry no signal for the target; "
                "restored, they behave as in phase I. Spearman correlations on all rows of each phase; ROC AUC alone "
                "for the target on the patients alive after day 3. bun, glucose and urine were not measured in phase I "
                "and are dropped.",
                alignment,
            ),
            Decision(
                "Where each block of the file took its physiology from",
                "The file's ten blocks of rows alternate between phase I and phase II. Phase I rows hold their own "
                "physiology; in phase II the source row lies 0 to about 90 rows further down, and the last rows of a "
                "block take the block of a later one. Offset: the source row minus the row.",
                blocks,
            ),
            Decision(
                "Checks of the link to ICPSR 2957",
                "The ten link columns are the same in both files on the patient's own row; the outcomes, which the link "
                "does not use, agree too.",
                checks.to_frame(),
            ),
            Decision(
                "Outcomes, model outputs, estimates and fields recorded after day 3 are dropped",
                "The prediction point is the end of study day 3. Outcomes, costs and scores of the whole stay come "
                "later; sps, surv2m and surv6m are outputs of the SUPPORT model fit on phase I survival, and the "
                "source advises against aps, prg2m, prg6m, dnr and dnrday (supportdesc).",
                dropped,
            ),
            Decision(
                "Surrogate interview dropped, patient interview and demographics kept",
                "The ADL answers describe function two weeks before admission, but the interviews took place on study "
                "days 2-7 (median day 4). A surrogate answer is missing far more often when the stay ended by day 7, "
                "so its gaps record events after the prediction point. The patient's answer is missing mostly when the "
                "patient cannot answer, but also for nearly every patient who died on days 4-7; edu and income are "
                "missing about as often for short as for long stays and more often among the deaths on days 4-7. "
                "Patients alive after day 3.",
                interviews,
            ),
            Decision(
                "Patients who died on study day 3 are dropped",
                "They are dead at the prediction point, and their day-3 values include values at death: heart rate 0 "
                "in 38% and mean blood pressure 0 in 25% of them, against at most 7.1% and 3.4% on any later day. All "
                "patients by day of death, with the restored physiology.",
                by_day,
            ),
            Decision(
                "Target: death within 2 months",
                "The source names 2- and 6-month survival; the record is named after the 2-month one, which is also "
                "the cut-off of the source's own outcome sfdm2. Every survivor was followed for more than 6 months, "
                f"so both are known for every patient. Counts on the cohort of {len(cohort):,} patients.",
                targets,
            ),
        ]
