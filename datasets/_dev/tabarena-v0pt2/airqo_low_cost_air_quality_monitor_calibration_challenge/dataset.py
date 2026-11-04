"""Same-hour reference PM2.5 calibration of AirQo low-cost monitors at three Kampala collocation sites."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
)

SENSOR2 = ("s2_pm2_5", "s2_pm10")


LANDFORMS = {21: "Upper slope (warm)", 31: "Lower slope (warm)"}  # ALOS landforms, Earth Engine CSP/ERGo/1_0/Global


def _reference_spikes(df: pd.DataFrame) -> pd.Series:
    """Reference hours above 3 times both low-cost PM2.5 channels and above 3 times the same site's reference in both
    neighbouring hours: a single-hour artefact of the reference monitor, not a reading the sensors share.
    """
    t = pd.to_datetime(df["created_at"])
    d = df.assign(_t=t).sort_values(["site", "_t"], kind="stable")
    by_site = d.groupby("site")
    hour = pd.Timedelta(hours=1)
    adjacent = (d["_t"] - by_site["_t"].shift(1)).eq(hour) & (by_site["_t"].shift(-1) - d["_t"]).eq(hour)
    ref = d["ref_pm2_5"]
    spike = (
        adjacent
        & ref.gt(3 * d["pm2_5"])
        & ref.gt(3 * d["s2_pm2_5"])
        & ref.gt(3 * by_site["ref_pm2_5"].shift(1))
        & ref.gt(3 * by_site["ref_pm2_5"].shift(-1))
    )
    return spike.reindex(df.index)


def _sensor2_dead(df: pd.DataFrame) -> pd.Series:
    """Hours in which both sensor-2 channels read exactly 0: a dead channel, as sensor 1 and the reference show."""
    return df[SENSOR2[0]].eq(0) & df[SENSOR2[1]].eq(0)


class AirqoLowCostAirQualityMonitorCalibrationChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What reference-monitor PM2.5 value corresponds to this hour's low-cost monitor reading at a site?",
        use_case=(
            "AirQo corrects low-cost PM2.5 readings with a model learned from hours in which its devices sat next "
            "to a reference monitor. Here a model refit at the start of each month corrects that month's new "
            "hourly readings at the three collocated devices."
        ),
        row="One hourly collocated low-cost/reference observation at one of three Kampala sites, from 2019 to 2021.",
        predicted="The same-hour reference-monitor PM2.5 mass concentration in micrograms per cubic metre.",
        known=(
            "The recorded hour and site, both low-cost sensors' PM2.5 and PM10 readings, the city-wide temperature "
            "and humidity, and the site descriptors. No reference value from the month being corrected is known, "
            "so reference values from other hours are not predictors."
        ),
        split=(
            "Three monthly windows, December 2020 to February 2021 (Kampala's dry season), each trained on every "
            "earlier hour: a model refit at the start of each month corrects that month's readings."
        ),
        changes=(
            "Use only the labeled Train.csv. Drop the opaque row ID, set sensor 2's two channels missing in the "
            "500 hours where both read exactly 0 (a dead channel), drop 5 single-hour reference spikes (10,927 of "
            "10,932 rows stay), parse the recorded UTC+3 timestamp, type the site as categorical and decode the "
            "90m landform class into its catalogue words."
        ),
        fit="approximate",
        fit_reason=(
            "AirQo's main use is correcting network devices that have no reference monitor; with three sites that "
            "transfer cannot be tested (leaving one site out, an untuned LightGBM scores RMSE 26.18 against 21.11 "
            "for the raw sensor). The task tests the next monthly refit at known collocated sites, a cadence the "
            "curator chose; the source paper names seasonal retraining as future work. Reference aggregation and "
            "site-metadata dates are unverified."
        ),
    )
    unique_name = "airqo_low_cost_air_quality_monitor_calibration_challenge"
    year = "2021"
    domain = "environmental science & climate"
    source = "Zindi"
    source_url = "https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge"
    license = "Zindi competition data terms: private participant use; redistribution to nonparticipants prohibited."
    data_tags = ("Spatial",)
    download_description = """
        Download Train.csv, Test.csv and optionally SampleSubmission.csv through an authorized account at
        https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge/data.
        Myunghwan supplied these original-download files on 2026-10-27 with a _LowCost filename suffix.
        We archived those bytes and restored the published filenames without editing their contents.
        This is user-supplied provenance; no agent-authenticated download or publisher checksum is claimed.
        Place Train.csv under the warehouse's airqo_low_cost_air_quality_monitor_calibration_challenge/.
        Its SHA-256 must be e856a03d70873f70630a1cb39c30ec9214f3710a8f343b72ca148081b66c5d92.
        Test.csv and SampleSubmission.csv are provenance/partition checks, not additional training labels.
        Keep competition data private under the published terms.
    """
    bibtex = """
        @misc{AirQoCalibration2021,
          author = {{AirQo} and {Zindi}},
          title = {AirQo Low-Cost Air Quality Monitor Calibration Challenge},
          year = {2021},
          howpublished = {https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge},
          note = {Three Kampala collocations; source evaluation uses RMSE}
        }
    """
    curation_comments = """
        We start with the 10,932 labeled rows of the supplied 2021 competition Train.csv; 10,927 ship.

        - Prediction point: the start of each month, when a model refit on every earlier collocated hour corrects
          that month's new hourly readings at the three collocated devices. No reference value from that month is
          known, so lagged or neighbouring reference values are not features (a previous-hour reference lowers an
          untuned LightGBM's mean RMSE from 18.21 to 16.28 on the three windows, all from test-month labels).
          Lennart chose this forward reading on 2026-11-04 with the temporal split; it supersedes the retrospective
          correction of archived hours that Myunghwan approved on 2026-10-27/28.
        - Keep ref_pm2_5 on its original micrograms-per-cubic-metre scale, with source RMSE; no target
          transformation, clipping or weighting. Labels run from 0.1 to 459.0. The low end includes 92 Nakawa hours
          (2020-11-10 to 2020-11-23) in which the reference reads 0.1 to 4 while both low-cost channels read 10 to
          120; they are kept for now, all on the training side of every window (open review issue).
        - Drop ID: it is an opaque, unique row key. Parse created_at as the supplied UTC+3 time without adding
          another three-hour shift. No target lags, leads, reference-neighbor features or full-data label transforms.
        - Treat site and landform_90m as nominal. The source's Google Earth Engine links identify landform_90m as
          discrete ALOS landform classes, decoded into the catalogue's words (21 "Upper slope (warm)", 31 "Lower slope
          (warm)"; CLEAN-12, Lennart 2026-11-04). The ALOS classes cross slope position with a warm/cool aspect, a
          partial order, so they stay unordered (CLEAN-14). landform_270m is continuous mTPI and stays numeric; its
          -11 valley value is valid. Keep the original greenness scale because its rescaling is undocumented.
        - Reference spikes (Lennart, 2026-11-04: "mark it well in the dataset notes"): a reference hour above 3 times
          both low-cost PM2.5 channels and above 3 times the same site's reference in both neighbouring hours is a
          single-hour artefact of the reference monitor, set missing and its row dropped (CLEAN-11, CLEAN-15). The
          rule catches 5 hours: Nakawa 2020-10-03 10:00 (444.0), 2020-10-05 09:00 (176.8), 2020-10-17 09:00 (374.5),
          2020-10-30 17:00 (150.6) and Makerere 2021-02-17 20:00 (249.1). The rule reads the target and its
          neighbouring labels. The four Nakawa hours are on the training side of every window; the Makerere hour is
          in the February 2021 test window, where CLEAN-11 lets a single extreme target leave only from the training
          period (open review issue). The rule follows the spike (rate-of-change) screening that hourly
          reference-monitor feeds such as EPA's AirNow run as automated QC (no published QC document is quoted
          yet). It needs both neighbouring hours in the file, so four look-alike hours with a missing neighbour
          stay, two of them in the December and January test windows, and USEmbassy 2021-02-10 07:00 (459.0,
          February window) misses the threshold by 0.55. Spikes lasting several hours, often at two sites at once,
          stay: they look like real pollution events.
        - Keep ordinary missingness: six humidity and 17 temperature values. Exact upstream averaging and
          reference-label construction are unknown; unusual positive values are not proven erroneous.
        - Sensor 2's PM2.5 and PM10 both read exactly 0 in 500 labeled hours, all at USEmbassy between
          2019-11-18 and 2019-12-17 in 13 runs of 11 to 117 hours; neither channel is 0 anywhere else, and sensor 1
          never reads below 0.57. In those hours sensor 1 reads a mean PM2.5 of 52 and the reference 59, so the
          zeros are a dead channel, not clean air. Both sensor-2 channels are set missing for those hours and the
          rows stay, with sensor 1 and the reference (CLEAN-11: an impossible value becomes missing; Lennart,
          2026-11-04). The definition raises if the joint zeros no longer number 500. Sixteen more hours of the same
          outage, with sensor 2 near zero (0.0014 to 1.37 in 15 of them), and 18 USEmbassy hours with sensor 1 dead
          (2019-11-13/14, 2020-06-07/08) stay as readings (open review issue).
        - All 16 predictors remain after ID removal. The eight geographic/site descriptors are constant within
          each site and encode its identity; recurrence is legitimate for this known-site task. Temperature and
          humidity are identical across sites at every shared hour: one city-wide ("prevailing") series, not device
          sensors. No duplicate site-hour or exact predictor copy occurs in the supplied labeled file.
        - The supplied Test.csv has 2,733 rows, approximately 20 percent within each site, over overlapping dates.
          It has no reference labels. Training uses only labeled Train.csv; the leaderboard's random split is not
          recreated.
        - New-site transfer, AirQo's network use, cannot be tested with three sites whose periods barely overlap
          (see fit_reason). Exact device serials, source reference aggregation and site-metadata snapshot dates
          remain unverified.
        - On the three windows, untuned models give mean RMSE 41.22 for the training mean, 25.32 for raw sensor 1,
          24.76 for a linear model, 19.21 for a forest and 18.26 for LightGBM (26.9, 13.6 and 14.3 per window,
          February first). February, the highest-pollution month, dominates the mean.
        - Exact feature-copy share is zero. Native hidden-group probes report no hits; quantized near-copy profiles
          cover 17.72 percent of rows but have only a 0.001215 skill gap. Examined pairs are same-site, different-hour
          observations, not duplicate dynamic readings. Only 2 of 2,720 test rows have a same-site training hour
          within one hour.
        - The pinned leak CLI fails on timezone-aware date selection in this runtime. A by-hand substitute on the three
          windows found no leak: no single column moves an untuned LightGBM's mean RMSE by more than 0.86 when
          dropped, and created_at alone has no skill.
        - The split is temporal (Lennart, 2026-11-04), replacing the site-balanced random folds Myunghwan approved on
          2026-10-28; see the splits comment. Public data redistribution permission
          is not established by these checks; the source's private-participant restrictions remain in force.
    """

    target = "ref_pm2_5"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="Root Mean Squared Error",
        reference="https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge#evaluation",
        definition="Square root of the mean squared error on original reference PM2.5, in micrograms per cubic metre",
    )
    temporal = Temporal(on="created_at", splits=TemporalSplits(window=1, unit="months", n_windows=3))
    splits_comment = """
        Three one-month windows, newest first: February 2021, January 2021, December 2020. Each trains on every
        earlier hour (8,207 to 10,093 rows, 75-92%). A model refit at the start of each month corrects that month's
        readings; the monthly cadence is the curator's judgment (Lennart, 2026-11-04). Adong et al. (2022) say it is
        "important to retrain these models periodically" and name "seasonal re-calibration" as future work; AirQo's
        refit practice is not documented. All three test months fall in Kampala's December-February dry season (mean
        reference 44.9, 49.6 and 74.4 against 35.9 to 43.1 in September to November 2020); whether to widen the
        windows is an open review issue (SPLIT-20). Site coverage differs by month: December has no USEmbassy rows,
        January 45, February no Nakawa. Before its test months Makerere (from 2020-07-15) has 4.5 to 6.5 months of
        history and Nakawa (from 2020-09-19) 2.4 and 3.4. The reference is for the same hour and no reporting delay
        is documented, so no gap is needed; no training row has a label from after its window start. Random folds
        over the hourly stream gave the model reference labels of neighbouring hours and scored a third better
        (LightGBM RMSE 12.94 against 18.26 on the same test rows; review panel, 2026-11-04).
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        path = raw_dir / "Train.csv"
        if hashlib.sha256(path.read_bytes()).hexdigest() != (
            "e856a03d70873f70630a1cb39c30ec9214f3710a8f343b72ca148081b66c5d92"
        ):
            raise ValueError("Train.csv differs from the user-supplied 2021 calibration release")
        return pd.read_csv(path)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        if not raw["ID"].is_unique or raw[["site", "created_at"]].duplicated().any():
            raise ValueError("Expected unique source rows and site-hour observations")
        df = drop_columns(raw, ["ID"])
        dead = _sensor2_dead(df)
        if dead.sum() != 500:
            raise ValueError(f"Expected 500 hours with both sensor-2 channels at 0, found {int(dead.sum())}")
        df.loc[dead, list(SENSOR2)] = float("nan")
        spikes = _reference_spikes(df)
        if spikes.sum() != 5:
            raise ValueError(f"Expected 5 single-hour reference spikes, found {int(spikes.sum())}")
        # A row without a valid target is no task row (CLEAN-11, CLEAN-15; Lennart, 2026-11-04).
        df = df.loc[~spikes]
        return decode(df, {"landform_90m": LANDFORMS})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=("site", "landform_90m"), datetime={"created_at": "ISO8601"})

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        dead = _sensor2_dead(raw)
        evidence = (
            raw.assign(
                sensor2_any_zero=raw[list(SENSOR2)].eq(0).any(axis=1),
                sensor2_both_zero=dead,
                sensor1_pm2_5_when_dead=raw["pm2_5"].where(dead),
                reference_when_dead=raw["ref_pm2_5"].where(dead),
            )
            .groupby("site")
            .agg(
                labeled_hours=("ID", "size"),
                sensor2_any_zero=("sensor2_any_zero", "sum"),
                sensor2_both_zero=("sensor2_both_zero", "sum"),
                sensor1_pm2_5_min=("pm2_5", "min"),
                sensor1_pm2_5_mean_when_dead=("sensor1_pm2_5_when_dead", "mean"),
                reference_mean_when_dead=("reference_when_dead", "mean"),
            )
            .round(2)
        )
        return [
            Decision(
                "Sensor 2 missing where both its channels read 0",
                "Both sensor-2 channels read exactly 0 in 500 USEmbassy hours (2019-11-18 to 2019-12-17) while "
                "sensor 1 and the reference show ordinary pollution, so the channel was dead: both are set missing "
                "and the rows stay (CLEAN-11; Lennart, 2026-11-04). The missing weather values stay too.",
                evidence,
            ),
            Decision(
                "Single-hour reference spikes dropped",
                "Five reference hours read above 3 times both low-cost PM2.5 channels and above 3 times the same "
                "site's reference in both neighbouring hours (Nakawa 2020-10-03 10:00: 444.0 against channels of 35 "
                "and 36 and neighbours of 47.5 and 86.0). Isolated hours like this fit an artefact of the reference "
                "monitor; no input can predict them. They become missing and the rows leave (CLEAN-11, CLEAN-15; "
                "Lennart, 2026-11-04), by the rule, not by hand.",
                df_spikes_table(raw),
            ),
        ]


def df_spikes_table(raw: pd.DataFrame) -> pd.DataFrame:
    """The reference hours the spike rule drops, with both channels and the neighbouring reference values."""
    spikes = _reference_spikes(raw.assign(**{c: raw[c].where(~_sensor2_dead(raw)) for c in SENSOR2}))
    return raw.loc[spikes, ["site", "created_at", "pm2_5", "s2_pm2_5", "ref_pm2_5"]].reset_index(drop=True)
