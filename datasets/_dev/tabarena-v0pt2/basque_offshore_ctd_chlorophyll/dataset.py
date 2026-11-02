"""Curated dataset definition for `basque_offshore_ctd_chlorophyll` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

NO_DATA = -999  # "NO DATA is indicated by -999" (Notes sheet of Hydrographic_variables.xlsx)

RENAME = {
    "STATION": "station",
    "PRESSURE (dbar)": "pressure_dbar",
    "TEMPERATURE (°C)": "temperature_c",
    "SALINITY": "salinity_pss78",
    "SIGMA THETA (kg m-3)": "sigma_theta_kg_m3",
    "LT (%)": "light_transmission_pct",
    "PAR (µmol m-2 s-1)": "par_umol_m2_s",
    "CHLOROPHYLL-a (µg l-1)": "chlorophyll_a_ug_l",
    "DISSOLVED OXYGEN (ml l-1)": "dissolved_oxygen_ml_l",
    "OXYGEN SATURATION (%)": "oxygen_saturation_pct",
}
CHANNELS = [
    "temperature_c",
    "salinity_pss78",
    "sigma_theta_kg_m3",
    "light_transmission_pct",
    "par_umol_m2_s",
    "chlorophyll_a_ug_l",
    "dissolved_oxygen_ml_l",
    "oxygen_saturation_pct",
]
REFERENCE_STATION = "Mendexa-Control"  # surveyed 2014-2023; its bin stands in when the other station has none


def _last_survey(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """The chlorophyll in ug/l at the same station and 1-dbar bin on the latest earlier survey day, else
    REFERENCE_STATION's at that bin, never the same day; and its age in days. `df` is sorted by `cast_date`.
    """
    keys = df[["station", "pressure_dbar", "cast_date"]].reset_index(drop=True)
    past = keys.assign(last=df["chlorophyll_a_ug_l"].to_numpy(), last_date=keys["cast_date"])
    own = pd.merge_asof(keys, past, on="cast_date", by=["station", "pressure_dbar"], allow_exact_matches=False)
    reference = past[past["station"] == REFERENCE_STATION].drop(columns="station")
    ref = pd.merge_asof(keys, reference, on="cast_date", by="pressure_dbar", allow_exact_matches=False)
    use_ref = own["last"].isna()
    value = own["last"].mask(use_ref, ref["last"])
    age = (keys["cast_date"] - own["last_date"].mask(use_ref, ref["last_date"])).dt.days
    return value.set_axis(df.index), age.set_axis(df.index)


class BasqueOffshoreCtdChlorophyll(AbstractCuratedDataset):
    # In brief: the task in plain words, for a reader who has not seen the source (first in the README).
    task_summary = TaskSummary(
        question=(
            "What is the chlorophyll-a concentration at a given depth of a CTD profile off the Basque coast, on a "
            "survey whose fluorometer failed, read from the other channels of the same casts and the station's "
            "earlier surveys?"
        ),
        use_case=(
            "For example, when a survey's fluorometer fails, AZTI's monitoring team estimates that survey's "
            "chlorophyll profile from the other channels of the same casts and the station's earlier surveys, as it "
            "reports the survey to the shellfish managers and the mussel farm (food supply, bloom warning). No "
            "source names this use."
        ),
        row=(
            "One 1-dbar depth bin of one CTD cast at the Mendexa offshore aquaculture site, SE Bay of Biscay: 180 "
            "casts on 146 survey days at two stations 1.8 km apart, May 2014 to December 2023, 31 to 52 bins each "
            "(AZTI, Solaun et al. 2025)."
        ),
        predicted=(
            "The fluorometer's chlorophyll-a in micrograms per litre at that depth, shipped on a log scale and "
            "scored on the concentration itself."
        ),
        known=(
            "The depth, the bin's temperature, salinity, density, light transmission, light (PAR), dissolved oxygen "
            "and oxygen saturation, the station, the date and the time of the cast, and the station's chlorophyll at "
            "the same depth on its last earlier survey, with how many days ago that was."
        ),
        split=(
            "Test surveys come after every training survey: nine windows of two survey days each, from September "
            "2022 to December 2023, each trained on all earlier surveys, as for a model refit about once a month. "
            "Both stations' casts of a day are always on the same side."
        ),
        changes=(
            "We rebuilt the table from AZTI's release rather than the benchmark copy that cut bloom values, set the "
            "no-data code to missing, dropped the one bin without chlorophyll, and added the station's last measured "
            "chlorophyll at the same depth."
        ),
        fit="approximate",
        fit_reason=(
            "No source names the fill, and the fluorometer's calibration over the record is undocumented: a "
            "2018-2022 floor and a 2022-10 step may be instrument periods. The channels predict the reading only "
            "against the date, and part of PAR's skill is daylight quenching. Refit on all earlier surveys, untuned "
            "LightGBM scores RMSE 0.485 ug/l against 0.623 for the training mean and 0.617 for the last survey "
            "(0.543 without the date)."
        ),
    )

    # Dataset
    unique_name = "basque_offshore_ctd_chlorophyll"
    year = "2025"  # Mendeley Data v1 of 2025-03-26 (PROV-9); v2 of 2025-05-23 left this table unchanged
    domain = "environmental science & climate"
    source = "Other"  # AZTI's release on Mendeley Data (PROV-8); the GitHub benchmark of Zhou et al. 2026 is a copy
    source_url = "https://doi.org/10.17632/vyz9zvddz4.2"
    license = "CC BY 4.0"  # stated on the Mendeley Data page (the Data in Brief article itself is CC BY-NC)
    data_tags = ()
    download_description = """
        We download version 2 of AZTI's release from Mendeley Data (doi:10.17632/vyz9zvddz4.2), the table "Hydrographic_variables.xlsx" (sha256 d7a00558...).
        mkdir -p local-data-warehouse/basque_offshore_ctd_chlorophyll && cd local-data-warehouse/basque_offshore_ctd_chlorophyll
        curl -L -o Hydrographic_variables.xlsx https://data.mendeley.com/public-files/datasets/vyz9zvddz4/files/74f2f926-2186-4678-b5c5-4d5e32bbf6f7/file_downloaded
    """
    bibtex = """
        @misc{solaun2025basque,
          title = {Long-term monitoring of potentially toxic phytoplankton, marine biotoxins and hydrographic variables in open waters off the Basque coast ({SE} Bay of Biscay)},
          author = {Solaun, Oihana and Zorita, Izaskun and Revilla, Marta and Gonz{\\'a}lez, Manuel and Larreta, Joana and Cuesta, Luis and Font{\\'a}n, Almudena and Ferrer, Luis and Sagarminaga, Yolanda and Laza, Aitor and Assadi, Carolina and Rodr{\\'i}guez, Jos{\\'e} Germ{\\'a}n},
          year = {2025},
          publisher = {Mendeley Data},
          note = {Version 2. Data descriptor: Solaun et al. (2025), Data in Brief 61:111736, doi:10.1016/j.dib.2025.111736},
          doi = {10.17632/vyz9zvddz4.2},
          howpublished = {\\url{https://doi.org/10.17632/vyz9zvddz4.2}}
        }
    """
    curation_comments = """
        We start with the sheet "Hydrographic variables" of Hydrographic_variables.xlsx in AZTI's Mendeley Data release v2 (Solaun et al. 2025): 8,195 one-dbar bins of 180 Sea-Bird SBE-25/25plus CTD casts on 146 survey days at Mendexa-Control (145, 2014-05-20 to 2023-12-18) and CTD-Mussel Farm (35, 2021-02-17 to 2023-12-18), 1.82 km apart.

        - Prediction point: a survey whose fluorometer failed, when the survey is reported and before the next one; the other channels of the same casts, the station, the date, the time and the station's earlier surveys are known. Our wording: the data descriptor names no use for the chlorophyll channel, only trends, toxin limits, shellfish management and early warning for the series as a whole ("could be useful to develop early warning systems for toxic algal blooms", Value of the Data), and Zhou et al. 2026 chose the target for a cross-dataset benchmark. In this release the fluorometer never failed (the one bin without chlorophyll lacks every channel); five casts lost another whole channel, each on a single survey, and AZTI published them as no data.
        - Rebuilt from AZTI's release, not from the "hydrographic" table of Zhou et al. 2026 (GitHub zhm12305/marine-ml-benchmark), whose IQR filter keeps 4,653 bins of 132 casts, cuts the bloom values (maximum 1.47 against 11.13) and drops every Mussel Farm row (PROV-13, PROV-15).
        - The no-data code -999 set to missing (CLEAN-10); shipped rows: PAR 296, salinity and sigma-theta 94, temperature, dissolved oxygen and oxygen saturation 46, light transmission none, the cast time 45 (one cast, 2016-04-15). The one bin with chlorophyll -999 (2017-09-04, 39 dbar, -999 in every channel) leaves (no target, CLEAN-15).
        - Target: chlorophyll-a in ug/l shipped as its natural log (`target_transform="log"`, scored on ug/l); median 0.43, maximum 11.13. Values at or below 0.03 are reported as 0.03, a floor of 2018-11-19 to 2022-09-12 only: 287 bins (3.5%) in 25 casts, against 37 at 0.04 and none at 0.03 before or after. A reporting floor of one period, so no two-regime zero (the next most frequent value, 0.21, holds 1.9%).
        - Last survey (USE-10): `last_chlorophyll_a_ug_l` is the station's chlorophyll at the same 1-dbar bin on its latest earlier survey day, Mendexa-Control's at that bin when the station has none there, never the same day (`_last_survey`); `last_chlorophyll_age_days` is its age (median 21 days, maximum 868). Missing on 52 rows, bins not reached before (2014-05-20, 2014-06-09, 2014-08-20). It is the profile the team would carry forward without a model, and the only lag of the target.
        - Windows: temporal on whole survey days (splits comment). A fill at the survey cannot use the surveys after it (USE-3, SPLIT-3); the stations are known entities with a history (USE-10). A day is never split: the other station's cast, 1.82 km away and from the same boat trip, alone gives R^2 0.736 on the log scale at the same depth.
        - Dropped latitude, longitude and datum: one value per station, copies of `station`. The date and the time of the cast ship as `cast_date` and `time_of_day_utc_h`.
        - Light transmission and PAR are optical channels of the same CTD package, kept: a survey whose fluorometer failed still has them (on the windows, RMSE 0.485 ug/l with both, 0.513 without light transmission, 0.505 without PAR, 0.534 without both). Part of PAR's signal is the fluorometer's daylight quenching, not chlorophyll: in 55 casts whose top 15 m are mixed, the ratio of the reading in the top 5 m to 6-15 m falls from 0.97 to 0.47 from the lowest to the highest quarter of surface PAR (Spearman -0.73).
        - Not forecasting (TP-10): on the 9 windows untuned LightGBM (mean of 3 seeds, the date as day of year and fractional year) scores RMSE 0.485 ug/l against 0.623 for the training mean, 0.617 for the station's last survey and 0.541 for the level of the newest training surveys; better than each in 7, 7 and 6 of 9 windows. One bloom window (2023-03-06 and 03-13, 1.51) carries a third of the average. The task probes (log scale, the 5 newest windows, the date as a raw number) flag no_signal, drift_baseline and unstable: the level drifts between windows; re-check with tuned results (TP-1).
        - Note: the date carries the period of the relation between the channels and the reading, not the season, and neither carries the skill alone. On the windows, RMSE in ug/l: all inputs 0.485, without the date 0.543, without the day of year 0.488; the date, depth and station alone 0.543; without the date and the last survey 0.592.
        - Note: the record may hold instrument periods. Besides the floor, cast minima step from 0.03 (2022-09-12) to 0.44 and 0.47 (2022-10-03), and below 10 dbar the slope of log chlorophyll on light transmission is -0.038 (2014 to 2018-10), +0.009 (2018-11 to 2022) and -0.027 (2023). The descriptor names the CTD models but no fluorometer model, calibration or dates. On the windows the fill reads too low by a factor of about 1.7 over the 7 survey days after the step (2022-10-03 to 2023-03-13). Kept: the fill reports the series' own reading (USE-5); revisit with AZTI's instrument history.
        - Note: sigma-theta is computed from temperature, salinity and pressure, and oxygen saturation from dissolved oxygen, temperature and salinity; the source ships both, and they stay.
    """

    # Task
    target = "log_chlorophyll_a_ug_l"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "The data descriptor (Solaun et al. 2025, Data in Brief 61:111736) fits no model, and the Mendeley page "
            'defines no task. Zhou et al. 2026 (PLOS ONE, Sec. 2.4) rank their benchmark by R^2 "for cross-dataset '
            'comparability" and also report MAE, RMSE, NRMSE, NSE and event F1, on an IQR-filtered copy without the '
            "bloom values and the Mussel Farm station: a choice for comparing datasets, on a task that does not carry "
            "over (MET-1, MET-2). Within a window R^2 on ug/l ranks models as RMSE does. RMSE on the concentration "
            "in ug/l."
        ),
        target_transform="log",
    )
    temporal = Temporal(
        on="cast_date",
        splits=TemporalSplits(window=2, unit="unique", n_windows=9),
        horizon=2,
        horizon_unit="steps",
    )
    splits_comment = """
        Expanding-window temporal splits on whole survey days: nine test windows of two distinct survey days each, walking back from the newest, from 2023-12-11 and 2023-12-18 (split 0) to 2022-09-12 and 2022-10-03 (split 8), 129 to 172 test rows each (1,386 in all); train is every earlier survey, 98% down to 83% of the rows. The horizon is two survey days. Two surveys are about a month at the programme's "monthly or biweekly" cadence (descriptor, Abstract), a plausible refit cadence for a fill made at the survey (SPLIT-12). One-day windows hold one or two casts, and 2 of 9 fall below 50 rows (SPLIT-17); two-day windows reach back to September 2022, so every calendar month is tested (SPLIT-20). The windows were chosen from counts and dates, before any score (SPLIT-21). A survey day always falls in one window: both casts of a day come from one boat trip, 8 to 94 minutes apart and probably with one CTD, and the other station's same-day reading at the same depth alone gives R^2 0.736 on the log scale (1,218 pairs). The one transient glitch on a two-cast day (2023-12-11, temperature and salinity lost) hit one cast only.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_excel(raw_dir / "Hydrographic_variables.xlsx", sheet_name="Hydrographic variables")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.rename(columns=RENAME)

        # 1. The no-data code -999 to missing, in every sensor channel and in the cast time (CLEAN-10).
        for col in [*CHANNELS, "UTC TIME (hhmmss)"]:
            df[col] = df[col].mask(df[col] == NO_DATA)

        # 2. Bins without chlorophyll carry no target (CLEAN-15): one bin.
        df = df[df["chlorophyll_a_ug_l"].notna()].copy()

        # 3. Date and time of day as features; the frame in time order (one cast per station and day).
        df["cast_date"] = pd.to_datetime(df["UTC DATE (YYYYMMDD)"].astype(str), format="%Y%m%d")
        hhmmss = df["UTC TIME (hhmmss)"]
        df["time_of_day_utc_h"] = (hhmmss // 10000) + (hhmmss // 100 % 100) / 60 + (hhmmss % 100) / 3600
        df = df.sort_values(["cast_date", "station", "pressure_dbar"], kind="stable").reset_index(drop=True)

        # 4. The station's last measured chlorophyll at the same bin, from a strictly earlier survey day (USE-10).
        df["last_chlorophyll_a_ug_l"], df["last_chlorophyll_age_days"] = _last_survey(df)

        # 5. Target on the log scale; scored on ug/l through target_transform="log".
        df[self.target] = np.log(df["chlorophyll_a_ug_l"])

        # 6. Coordinates and datum are one value per station; the raw date and time are rebuilt above.
        return drop_columns(
            df,
            [
                "chlorophyll_a_ug_l",
                "LATITUDE (degrees North)",
                "LONGITUDE (degrees East)",
                "DATUM",
                "UTC DATE (YYYYMMDD)",
                "UTC TIME (hhmmss)",
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["station"],
            datetime={"cast_date": "%Y-%m-%d"},
        )
