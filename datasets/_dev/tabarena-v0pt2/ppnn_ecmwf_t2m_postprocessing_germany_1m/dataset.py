"""Curated dataset definition for `ppnn_ecmwf_t2m_postprocessing_germany_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

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
)

RAW_FILE = "data_RL18.feather"

# The 18 forecast variables of Rasp and Lerch (2018), Table 1, as the file names them. Each has the mean and the
# variance of the 50 ensemble members (`<v>_mean`, `<v>_var`).
ENSEMBLE_VARIABLES = (
    "t2m",
    "cape",
    "sp",
    "tcc",
    "u_pl850",
    "v_pl850",
    "q_pl850",
    "u_pl500",
    "v_pl500",
    "gh_pl500",
    "sshf",
    "slhf",
    "u10",
    "v10",
    "ssr",
    "str",
    "d2m",
    "sm",
)
STATION_FEATURES = ("lat", "lon", "alt", "orog")

# Test windows: three two-week windows, four months apart, walking back from the end of the release (2016-12-31).
WINDOW_STARTS = ("2016-04-18", "2016-08-18", "2016-12-18")
LEAD_DAYS = 2  # the forecasts are started at 00 UTC two days before the valid time (48 h lead)

# Impossible observations (CLEAN-11): station, first and last valid date, rows, the value the station reported.
BAD_LABELS = (
    (254, "2016-08-25", "2016-08-25", 1, 0.0),  # 0.0 between 18.1 and 18.2, forecast 19.8 (August test window)
    (288, "2014-12-20", "2014-12-31", 12, 11.3),  # 11.3 on 12 nights while the forecast runs from 9.4 to -3.0
)


def _bad_labels(df: pd.DataFrame) -> pd.Series:
    """The rows of `BAD_LABELS`, each run guarded by its row count and its reported value."""
    bad = pd.Series(False, index=df.index)
    for station, first, last, n_rows, value in BAD_LABELS:
        hit = df["station"].eq(station) & df["date"].between(pd.Timestamp(first), pd.Timestamp(last))
        if hit.sum() != n_rows or not df.loc[hit, "t2m_obs"].sub(value).abs().lt(0.01).all():  # stored as float32
            raise ValueError(f"Expected {n_rows} rows of {value} at station {station}, {first} to {last}")
        bad |= hit
    return bad


class PpnnEcmwfT2mPostprocessingGermany1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What 2 m temperature will a German weather station observe at 00 UTC two days from now, given ECMWF's "
            "ensemble forecast for that place and time?"
        ),
        use_case=(
            "A weather service post-processes the ECMWF ensemble forecast at each of its stations: when the 00 UTC "
            "run is in, it corrects the 48-hour temperature forecast for the station's systematic errors before "
            "issuing it (Rasp and Lerch 2018)."
        ),
        row=(
            "One station on one day: 535 stations of the German weather service (DWD), forecasts valid at 00 UTC "
            "from 3 January 2007 to 31 December 2016, the temperature forecast interpolated to the station and the "
            "other fields taken at the nearest grid point."
        ),
        predicted=(
            "The 2 m air temperature observed at the station at the forecast's valid time, 00 UTC, 48 hours after "
            "the forecast started, in degrees Celsius."
        ),
        known=(
            "The ensemble mean and variance of 18 forecast variables for that place and time (temperature, dew "
            "point, pressure, cloud, winds, humidity, heat and radiation fluxes, soil moisture), the station with "
            "its latitude, longitude and altitude, the model's ground height there, and the valid date."
        ),
        split=(
            "Three two-week windows of 2016, four months apart (late April, late August, late December); a correction "
            "trained on a random million of the station-days valid more than two days before each window is scored "
            "on that window."
        ),
        changes=(
            "We score a point forecast by its absolute error (the CRPS of a point forecast), where the source scores "
            "a predictive distribution by the CRPS, and test on three two-week windows instead of the whole of 2016."
        ),
        fit="direct",
        fit_reason=(
            "Every input is out when the 00 UTC run is in, the stations are the ones served later, and the windows "
            "follow the release in time. The source issues a distribution; here the corrected forecast is one value."
        ),
    )

    # Dataset
    unique_name = "ppnn_ecmwf_t2m_postprocessing_germany_1m"
    version_of = "ppnn_ecmwf_t2m_postprocessing_germany"
    version_comment = """
        We sample per test window (v2 split protocol): each window keeps all of its rows (6,936 to 7,003, under the
        500k test budget), and its train side is a random 1M of the station-days valid before the window minus the
        two-day gap (1,679,488 to 1,800,927 rows), drawn in one random order for all windows; the frame keeps only the
        rows a split uses (1,081,263). Random rows rather than the newest ones keep every season and year of the
        history, as the source's models trained on 2007-2015 (Rasp and Lerch 2018, Sect. 2.1).
    """
    year = "2021"
    domain = "environmental science & climate"
    source = "Other"
    source_url = "https://doi.org/10.6084/m9.figshare.13516301.v1"
    license = "CC BY 4.0"
    data_tags = ("Spatial",)
    download_description = """
        We download the one file of the figshare deposit "PPNN full data (feather format)" (Rasp 2021, CC BY 4.0;
        data_RL18.feather, 615,496,032 bytes, md5 18bb8d47b47692a2bda193572b0683ed, downloaded 2026-11-08).

        mkdir -p local-data-warehouse/ppnn_ecmwf_t2m_postprocessing_germany
        wget -O local-data-warehouse/ppnn_ecmwf_t2m_postprocessing_germany/data_RL18.feather https://ndownloader.figshare.com/files/25942496
    """
    bibtex = """
        @misc{rasp2021ppnn,
          title = {{PPNN} full data (feather format)},
          author = {Rasp, Stephan},
          year = {2021},
          howpublished = {figshare},
          doi = {10.6084/m9.figshare.13516301.v1}
        }
        @article{rasp2018neural,
          title = {Neural Networks for Postprocessing Ensemble Weather Forecasts},
          author = {Rasp, Stephan and Lerch, Sebastian},
          journal = {Monthly Weather Review},
          volume = {146},
          number = {11},
          pages = {3885--3900},
          year = {2018},
          doi = {10.1175/MWR-D-18-0187.1}
        }
    """
    curation_comments = """
        We start with data_RL18.feather from the figshare deposit of Rasp (2021), the full data of Rasp and Lerch
        (2018): 1,808,942 station-days with the date, the station, the observed 2 m temperature (`obs`), the ensemble
        mean and variance of 18 ECMWF forecast variables and 4 station features. The forecasts come from ECMWF's
        TIGGE archive, whose licence asks works that use them to acknowledge TIGGE.

        - Prediction point: the 00 UTC start of the ECMWF 50-member ensemble forecast, 48 h before the valid time in
          `date` (Sect. 2.1; the code splits the data by valid hour and calls the time "valid time of forecasts and
          observations, UTC", data_processing/split_data_by_validHour.R in github.com/slerch/ppnn). Every input is a
          forecast for the valid time or a fixed station property, so all are known at that point; the observation is
          known at the valid time.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): a 14-day test window holds a station's rows
          for the next two valid dates, whose forecasts were started one and two days after a row's prediction point.
          Joining them to the row by station and date lowers the task gamer's MAE from 1.0833 to 1.0692 (per window,
          newest first, -0.002 / -0.011 / -0.029; with 1000 trees from 1.0662 to 1.0606: +0.006 / -0.012 / -0.012),
          where adding a random column moves the mean by about 0.005 (measured before the two label fixes below).
          Each test row is predicted from the training rows and its own features only; no feature or model step may
          use other test rows. The rows and the test days stay.
        - Year: 2021, the first deposit that holds every value we ship (PROV-9, as in
          2_month_survival_rate_prediction). The earlier deposit "Interpolated PPNN data" (Rasp 2020, figshare
          10.6084/m9.figshare.9762980.v1, published 2020-02-11) holds all 1,808,942 rows with the identical target
          and the 50 members of the temperature forecast, whose mean and variance equal `t2m_mean` and `t2m_var`,
          with the stations' latitude, longitude and altitude: 5 of the 40 inputs, not the other 17 variables or
          `orog` (compared value by value, review panel of 2026-11-08).
        - The rows are the paper's: 1,626,724 in 2007-2015 and 182,218 in 2016 "after removing missing observations"
          (Sect. 2.2); the file has no missing target and one row per station and date. The 2020 deposit lists 537
          stations (as the paper and the README); two of them (DWD 3246 and 6184) never reported, so 535 have rows.
          Anomaly: 502 stations have rows in 2016 in both deposits, where the paper says 499; one station has a single
          row.
        - We rename the target `obs` to `t2m_obs`, the name in the source's netCDF files, and drop the time zone of
          `date` (all values are 00:00 UTC).
        - Two impossible observations become missing, and their 13 rows leave (CLEAN-11, CLEAN-15, as in
          airqo_low_cost_air_quality_monitor_calibration_challenge): station 254 reports 0.0 °C on 2016-08-25, between
          18.1 and 18.2 on the days around it, with a forecast of 19.8 (a test row of the August window, +0.0028 MAE
          for every model there); station 288 reports 11.3 °C on the 12 nights from 2014-12-20 to 2014-12-31 while
          its forecast runs between 9.4 and -3.0 (training rows). The source keeps every value but -999 and does not
          read DWD's quality flags.
        - Note: the spread columns `<variable>_var` hold the variance of the 50 members (R's `var` in
          data_processing/generate_Rdata_files/data_preparation.R, which writes these column names), while the paper
          (Sect. 2.3) and its network code use the standard deviation. We keep the variance as published.
        - Note: only the temperature forecast (`t2m_*`) is interpolated bilinearly to the station; the other 17
          fields are taken at the nearest 0.5° grid point, so the stations of one grid box share them (interpolation.R
          and interpolation_aux_surface_more_part2.R). `orog` is the model's ground height at that grid point, read
          from the first time step of 2007 and held constant through the model upgrades of 2010 and 2016
          (interpolation_aux_geo.R).
        - Note: units as published: temperatures in degrees Celsius except the dew point `d2m_*` in kelvin (only the
          temperature was converted), the heat and radiation fluxes `sshf`, `slhf`, `ssr`, `str` accumulated over the
          48 h in J m^-2, CAPE in J kg^-1, pressure in Pa, geopotential height in gpm, specific humidity in kg kg^-1,
          winds in m s^-1, cloud cover in percent, soil moisture in kg m^-3; each `_var` column in the square of its
          variable's unit.
        - Soil moisture (`sm_mean`, `sm_var`) is missing on 6.6% of the rows and stays missing: at every station on the
          121 days from 2014-03-06 to 2014-07-04; always at 17 coastal and island stations; and on 9,891 rows at 11
          Baltic-coast stations by model period: stations 11, 127, 128 and 424 before 2010-01-29, stations 171, 333,
          399 and 401 from 2016-03-11, stations 147, 153 and 203 in both periods (the dates match ECMWF's ensemble
          upgrades of January 2010 and March 2016). So 7 stations (147, 153, 171, 203, 333, 399, 401) have soil
          moisture in training and none in any test window: 4.2% of the test rows miss it, 6.6% to 6.8% of each train
          side. The missingness does not track the target (leak probe: the indicator alone scores R^2 -3.1). The
          replication notebook of the source drops both columns; the paper's Table 1 keeps soil moisture.
        - `station` (the deposit's station index 1 to 535, not the DWD station number) is a categorical feature: the
          same stations report on later days, and the paper's best networks learn an embedding per station (Sect.
          4.2). Latitude, longitude and altitude (from DWD's station list at download) and model orography are constant
          per station.
        - `date` stays a feature: the season is known at the prediction point.
        - Left out: the 36 h lead time (valid at 12 UTC) named in the source's README is not in the deposit. The Chen
          and Lerch (2022) deposit (figshare 10.6084/m9.figshare.19453580.v2) holds the same rows with the 50 raw
          members of the temperature forecast; it is a version of this data with no distinct task (PROV-6), not used.
        - Note: the ensemble mean forecast `t2m_mean` is the natural core of the task, and models clearly beat it
          (TP-4, TP-10). Mean MAE over the three windows, trained on each shipped train side: the raw ensemble mean
          1.447, plus each station's mean error 1.350, a linear correction per station (MOS) 1.296, ridge on all inputs
          1.318, LightGBM untuned 1.121, LightGBM with 1000 trees 1.029 (below MOS on 3 of 3 windows). No input is a
          lag of the observation.
        - Note: the task probes flag no_spread (LightGBM against random forest +0.023 skill, paired SE 0.012), on the
          newest 200,000 training rows the probe keeps, about four months of one season. On the full train sides the
          families spread on every window (above: ridge 1.318 against LightGBM 1.029 to 1.121); check against tuned
          results once they exist (TP-3).
        - Note: leak probe 13 (the target by quarter) flags two things, neither a change in recording (EV-3). The rows
          per day of the second and third quarters of 2016 (z +4.9, +3.3) come from the sampled frame: the test windows
          keep all their rows while the training rows are sampled; on the full file 2016 has 182,218 rows against
          179,759 to 183,971 a year in 2008-2015. The target's 90th percentile in the third quarters of 2015 and 2016
          (z +6.3, +6.4) is weather: the summer heat of 2015 (20.3 °C on the full file, against 17.5 to 19.0 in
          2007-2014), and in 2016 the late-August test window, kept whole (19.9 alone; the quarter 18.7 with it, 18.4
          without it, 18.6 on the full file).
    """

    # Task
    target = "t2m_obs"
    problem_type = "regression"
    metric = Metric.stand_in(
        "mae",
        original="CRPS of the predictive distribution, mean over all stations and days of 2016 (Table 2)",
        reason=(
            "the source issues a predictive distribution and ranks the models by its mean CRPS; the benchmark's "
            "regression task takes one value per row, and the CRPS of a point forecast (a distribution with all its "
            "mass at one value) is its absolute error, so MAE is the CRPS of the predictions the task takes; on the "
            "shipped windows, over 10 models each scored by the MAE of its point and by the CRPS of that point with a "
            "fitted spread, Kendall's tau between the two is 0.944 / 0.989 / 0.944 (December / August / April), with "
            "the same best model in 3 of 3 windows, against 0.989 / 0.944 / 0.899 for RMSE (review panel of "
            "2026-11-08, before the two label fixes)"
        ),
        reference=(
            "Rasp and Lerch 2018, Monthly Weather Review 146(11):3885-3900 (https://doi.org/10.1175/MWR-D-18-0187.1), "
            "Sect. 5.1 and Table 2 (mean CRPS), Appendix B (CRPS)"
        ),
        definition="mean(|y - yhat|) in degrees Celsius; equal to the mean CRPS of point forecasts",
    )

    # Splits
    temporal = Temporal(
        on="date",
        splits=TemporalSplits(window=14, unit="days", cutoffs=WINDOW_STARTS, gap=LEAD_DAYS),
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)
    splits_comment = """
        Three test windows of 14 days, 2016-12-18 to 12-31, 2016-08-18 to 08-31 and 2016-04-18 to
        05-01 (newest first): weather test windows of one to two weeks (SPLIT-18), four months apart so they fall in
        three seasons rather than all in the Christmas weeks at the end of the release (SPLIT-20). Each trains on every
        station-day valid before the window start minus a gap of 2 days, the convention of the source's own
        rolling-window code for the 48 h lead (`get_train_test_sets`, fclt=48: training stops two days before the
        predicted date). At the prediction point of a window's first day (00 UTC two days before it) the observation
        of the day before is not yet in, while the one taken at the run's own start is, so the gap is one day longer
        than needed (SPLIT-10). Each train side is a random 1M of those rows (the row budget); each window keeps all
        its rows. The source holds out the whole of 2016 and trains on 2007-2015. Each test row is predicted from the
        training rows and its own features only; no feature or model step may use other test rows (LEAK-9: the later
        forecasts of the same station sit in other test rows of a window).
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_feather(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. The columns are the paper's Table 1: the mean and variance of 18 forecast variables, 4 station features.
        expected = ["date", "station", "obs"]
        expected += [f"{v}_{s}" for v in ENSEMBLE_VARIABLES for s in ("mean", "var")] + list(STATION_FEATURES)
        assert list(raw.columns) == expected, list(raw.columns)
        # 2. The target under the source's netCDF name; `date` is the valid time, 00 UTC on every row.
        df = raw.rename(columns={"obs": "t2m_obs"})
        df["date"] = df["date"].dt.tz_localize(None)
        # 3. The rows are the paper's: no missing target, one row per station and valid date.
        assert df["t2m_obs"].notna().all()
        assert not df.duplicated(["station", "date"]).any()
        # 4. Two impossible observations become missing (CLEAN-11), and a row without a target leaves (CLEAN-15).
        df["t2m_obs"] = df["t2m_obs"].mask(_bad_labels(df))
        df = df.loc[df["t2m_obs"].notna()]
        # 5. Soil moisture stays missing where the forecast has none (2014-03-06 to 2014-07-04; sea grid points).
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["station"], datetime=["date"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        # The full release: `df` holds only the rows the sampled splits use.
        frame = raw.rename(columns={"obs": "t2m_obs"})
        frame["date"] = frame["date"].dt.tz_localize(None)
        frame = frame.loc[~_bad_labels(frame)].sort_values("date", kind="stable").reset_index(drop=True)
        options = {
            "3 x 14 days, four months apart, gap 2 days (shipped)": self.temporal.splits,
            "3 x 7 days at the end of 2016, gap 2 days": TemporalSplits(
                window=7, unit="days", n_windows=3, gap=LEAD_DAYS
            ),
            "the years 2014, 2015, 2016, gap 2 days (the source's test year and two before)": TemporalSplits(
                window=1, unit="years", cutoffs=(2014, 2015, 2016), gap=LEAD_DAYS, gap_unit="days"
            ),
        }
        # Per option: the windows, their size, and the raw forecast against a correction by each station's mean error
        # on the window's (full) train side, by MAE in degrees Celsius; no model is fitted (SPLIT-21).
        rows = {}
        for name, option in options.items():
            windows = [folds[0] for folds in option.splits(frame, "date").values()]
            raw_mae, corrected_mae = [], []
            for train, test in windows:
                past, future = frame.iloc[train], frame.iloc[test]
                offset = (past["t2m_obs"] - past["t2m_mean"]).groupby(past["station"], observed=True).mean()
                corrected = future["t2m_mean"] + future["station"].map(offset).astype(float).fillna(0.0)
                raw_mae.append(float((future["t2m_obs"] - future["t2m_mean"]).abs().mean()))
                corrected_mae.append(float((future["t2m_obs"] - corrected).abs().mean()))
            months = sorted({int(m) for _, test in windows for m in frame["date"].iloc[test].dt.month.unique()})
            rows[name] = {
                "windows": len(windows),
                "test rows": f"{min(len(t) for _, t in windows):,}-{max(len(t) for _, t in windows):,}",
                "train rows before the budget": f"{min(len(t) for t, _ in windows):,}-"
                f"{max(len(t) for t, _ in windows):,}",
                "test months": ", ".join(str(m) for m in months),
                "MAE of the raw ensemble mean, per window": " / ".join(f"{v:.3f}" for v in raw_mae),
                "MAE after the station's mean error, per window": " / ".join(f"{v:.3f}" for v in corrected_mae),
            }

        year = frame["date"].dt.year
        soil = pd.DataFrame(
            {
                "rows": frame.groupby(year).size(),
                "stations": frame.groupby(year)["station"].nunique(),
                "share without soil moisture": frame["sm_mean"].isna().groupby(year).mean().round(3),
            }
        ).rename_axis("year (valid date)")

        return [
            Decision(
                "Three two-week windows of 2016, four months apart, with a two-day gap",
                "Weather test windows are one to two weeks (SPLIT-18); spread over 2016 they fall in three seasons, "
                "not all in the last weeks of December (SPLIT-20). The source tests the whole of 2016; its models "
                "trained once on 2007-2015, updating the networks daily brought no improvement (Sect. 7), and rolling "
                "training windows for EMOS only marginal ones (Sect. 5.1, footnote 4). The table gives each option's "
                "windows (newest first) and the raw forecast's error, without models (SPLIT-21).",
                pd.DataFrame(rows).T.rename_axis("option"),
            ),
            Decision(
                "Soil moisture stays missing where the forecast has none",
                "The soil moisture forecast is missing at every station from 2014-03-06 to 2014-07-04, always at 17 "
                "coastal and island stations, and at 11 Baltic-coast stations before 2010-01-29, from 2016-03-11 or "
                "both (the dates of ECMWF's ensemble upgrades), so 7 of them have it in training and in no test "
                "window; the other inputs are complete.",
                soil,
            ),
        ]
