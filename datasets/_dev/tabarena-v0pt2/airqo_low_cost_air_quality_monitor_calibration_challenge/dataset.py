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
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
)

SENSOR1 = ("pm2_5", "pm10")
SENSOR2 = ("s2_pm2_5", "s2_pm10")
DEAD_RATIO = 0.27  # dead hours reach 0.255 of the other sensor; the lowest live ratio is 0.294 (Makerere 2020-12-05)
OUTAGE_SITE, OUTAGE_DAYS = "Nakawa", ("2020-11-10", "2020-11-23")  # the reference outage, dates inclusive


LANDFORMS = {21: "Upper slope (warm)", 31: "Lower slope (warm)"}  # ALOS landforms, Earth Engine CSP/ERGo/1_0/Global


def _neighbour_references(df: pd.DataFrame) -> pd.DataFrame:
    """The same site's reference one hour before and one hour after each row; missing when that hour is not in the
    file or its reference is missing.
    """
    t = pd.to_datetime(df["created_at"])
    d = df.assign(_t=t).sort_values(["site", "_t"], kind="stable")
    by_site = d.groupby("site")
    hour = pd.Timedelta(hours=1)
    before = by_site["ref_pm2_5"].shift(1).where((d["_t"] - by_site["_t"].shift(1)).eq(hour))
    after = by_site["ref_pm2_5"].shift(-1).where((by_site["_t"].shift(-1) - d["_t"]).eq(hour))
    return pd.DataFrame({"ref_before": before, "ref_after": after}).reindex(df.index)


def _reference_spikes(df: pd.DataFrame) -> pd.Series:
    """Reference hours above 3 times both low-cost PM2.5 channels and above 3 times the same site's reference in each
    neighbouring hour that has one, with at least one such hour: an instrument error of the reference monitor, a value
    neither the collocated sensors nor the hours around it share.
    """
    nb = _neighbour_references(df)
    ref = df["ref_pm2_5"]
    above = [ref.gt(3 * nb[c]) | nb[c].isna() for c in nb]
    return nb.notna().any(axis=1) & ref.gt(3 * df["pm2_5"]) & ref.gt(3 * df["s2_pm2_5"]) & above[0] & above[1]


def _sensor2_dead(df: pd.DataFrame) -> pd.Series:
    """Hours in which both sensor-2 channels read exactly 0: a dead channel, as sensor 1 and the reference show."""
    return df[SENSOR2[0]].eq(0) & df[SENSOR2[1]].eq(0)


def _sensor_low(df: pd.DataFrame, sensor: tuple[str, str], other: tuple[str, str]) -> pd.Series:
    """Hours in which a sensor's PM2.5 is below DEAD_RATIO times the other sensor's: a dead channel, not clean air."""
    return df[sensor[0]].lt(DEAD_RATIO * df[other[0]])


def _reference_outage(df: pd.DataFrame) -> pd.Series:
    """Nakawa hours of 2020-11-10 to 2020-11-23 with the reference below 0.3 times both low-cost PM2.5 channels: the
    reference monitor failed, as collocated instruments sample the same air.
    """
    day = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d")
    run = df["site"].eq(OUTAGE_SITE) & day.between(*OUTAGE_DAYS)
    ref = df["ref_pm2_5"]
    return run & ref.lt(0.3 * df["pm2_5"]) & ref.lt(0.3 * df["s2_pm2_5"])


def _reference_errors(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """The outage hours, then the spikes; an outage hour's reference is missing, so it is no neighbour of a spike."""
    outage = _reference_outage(df)
    return outage, _reference_spikes(df.assign(ref_pm2_5=df["ref_pm2_5"].mask(outage)))


def _mask_dead_channels(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.Series]]:
    """Set a dead sensor's two channels missing; the rows stay. Masks come from the raw readings."""
    zero2 = _sensor2_dead(df)
    masks = {
        "sensor 2, both channels 0": zero2,
        "sensor 2, below 0.27 of sensor 1": _sensor_low(df, SENSOR2, SENSOR1) & ~zero2,
        "sensor 1, below 0.27 of sensor 2": _sensor_low(df, SENSOR1, SENSOR2),
    }
    df = df.copy()
    df.loc[masks["sensor 2, both channels 0"] | masks["sensor 2, below 0.27 of sensor 1"], list(SENSOR2)] = float("nan")
    df.loc[masks["sensor 1, below 0.27 of sensor 2"], list(SENSOR1)] = float("nan")
    return df, masks


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
            "Five monthly windows, October 2020 to February 2021, each trained on every earlier hour: a model refit "
            "at the start of each month corrects that month's readings. The test covers two months of the "
            "September-November rains and Kampala's December-February dry season."
        ),
        changes=(
            "Use only the labeled Train.csv. Drop the opaque row ID; set a dead sensor's two channels missing "
            "(sensor 2 in 516 hours, sensor 1 in 18); drop 12 single-hour reference errors and 92 hours of a Nakawa "
            "reference outage (10,828 of 10,932 rows stay); parse the recorded UTC+3 timestamp, type the site as "
            "categorical and decode the 90m landform class into its catalogue words."
        ),
        fit="approximate",
        fit_reason=(
            "AirQo's main use is correcting network devices that have no reference monitor; with three sites that "
            "transfer cannot be tested (leaving one site out, an untuned LightGBM scores RMSE 24.84 against 19.90 "
            "for the raw sensor). The task tests the next monthly refit at known collocated sites, a cadence the "
            "curator chose; the source paper names seasonal retraining as future work. Reference aggregation and "
            "site-metadata dates are unverified."
        ),
    )
    unique_name = "airqo_low_cost_air_quality_monitor_calibration_challenge"
    domain = "environmental science & climate"
    sources = (
        Source(
            role="publication",
            platform="Zindi",
            url="https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge",
            license="Zindi competition data terms: private participant use; redistribution to nonparticipants prohibited.",
            year="2021",
            bibtex="""
                @misc{AirQoCalibration2021,
                  author = {{AirQo} and {Zindi}},
                  title = {AirQo Low-Cost Air Quality Monitor Calibration Challenge},
                  year = {2021},
                  howpublished = {https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge},
                  note = {Three Kampala collocations; source evaluation uses RMSE}
                }
            """,
        ),
    )
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
    curation_comments = """
        We start with the 10,932 labeled rows of the supplied 2021 competition Train.csv; 10,828 ship.

        - Prediction point: the start of each month, when a model refit on every earlier collocated hour corrects
          that month's new hourly readings at the three collocated devices. No reference value from that month is
          known, so lagged or neighbouring reference values are not features (a previous-hour reference lowers an
          untuned LightGBM's mean RMSE from 18.21 to 16.28 on the three windows, all from test-month labels;
          superseded 2026-11-05: 15.34 to 14.09 on the five windows, February 27.12 to 23.23).
          Lennart chose this forward reading on 2026-11-04 with the temporal split; it supersedes the retrospective
          correction of archived hours that Myunghwan approved on 2026-10-27/28.
        - Keep ref_pm2_5 on its original micrograms-per-cubic-metre scale, with source RMSE; no target
          transformation, clipping or weighting. Labels run from 0.2 to 459.0. The 92 Nakawa outage hours of
          2020-11-10 to 2020-11-23 were kept on 2026-11-04 (superseded 2026-11-05: they leave, CC below).
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
          2020-10-30 17:00 (150.6) and Makerere 2021-02-17 20:00 (249.1) (superseded 2026-11-05: 12 hours, CC below).
          The rule reads the target and its neighbouring labels. The four Nakawa hours are on the training side of
          every window (superseded 2026-11-05: under the five windows they are October 2020 test labels); the
          Makerere hour is in the February 2021 test window, where CLEAN-11 lets a single extreme target leave only
          from the training period (settled 2026-11-05: an impossible value, dropped in every window, issue 2, CC
          below). The rule follows the spike (rate-of-change) screening that hourly reference-monitor feeds such as
          EPA's AirNow run as automated QC (no published QC document is quoted yet). It needs both neighbouring hours
          in the file, so four look-alike hours with a missing neighbour stay (superseded 2026-11-05: the rule takes
          the neighbouring hours present and drops them, CC below), and USEmbassy 2021-02-10 07:00 (459.0, February
          window) misses the threshold by 0.55 (to sensor 1; to sensor 2 by 26.2). Spikes lasting several hours,
          often at two sites at once, stay: they look like real pollution events.
        - Keep ordinary missingness: five humidity and 17 temperature values. Exact upstream averaging and
          reference-label construction are unknown; unusual positive values are not proven erroneous.
        - Sensor 2's PM2.5 and PM10 both read exactly 0 in 500 labeled hours, all at USEmbassy between
          2019-11-18 and 2019-12-17 in 13 runs of 11 to 117 hours; neither channel is 0 anywhere else, and sensor 1
          never reads below 0.57. In those hours sensor 1 reads a mean PM2.5 of 52 and the reference 59, so the
          zeros are a dead channel, not clean air. Both sensor-2 channels are set missing for those hours and the
          rows stay, with sensor 1 and the reference (CLEAN-11: an impossible value becomes missing; Lennart,
          2026-11-04). The definition raises if the joint zeros no longer number 500. Sixteen more hours of the same
          outage, with sensor 2 near zero (0.0014 to 1.37 in 15 of them), and 18 USEmbassy hours with sensor 1 dead
          (2019-11-13/14, 2020-06-07/08) stay as readings (superseded 2026-11-05: set missing, CC below).
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
        - On the five windows, untuned models give mean RMSE 36.42 for the training mean, 21.01 for raw sensor 1,
          20.71 for a linear model, 15.08 for a forest and 15.34 for LightGBM (27.4, 14.7, 12.2, 9.3 and 13.2 per
          window, February first; one seed). February, the highest-pollution month, dominates the mean. (Superseded
          2026-11-05: 41.22, 25.32, 24.76, 19.21 and 18.26 on the three windows of 2026-11-04; LightGBM 16.69, with
          January 16.8 and November 13.0, before the 7 hours issue 2 adds.)
        - Exact feature-copy share is zero on all five windows. The hidden-group probe finds no entity-like column;
          near-copy clusters hold 6.7% of rows, and 12.1% of test rows have one on the training side (superseded
          2026-11-05: the quantized profiles' 17.72 percent and 0.001215 skill gap came from the random folds). Only 4
          of 4,624 test rows have a same-site training hour within one hour, at the window starts.
        - The leak probes run on the five windows (superseded 2026-11-05: the pinned CLI failed on timezone-aware
          dates, and a by-hand substitute on the three windows found no leak) and find none: all features score skill
          0.813, each sensor channel alone 0.61 to 0.66 and every other column alone below 0, and no test row copies
          a training row. Dropping one column moves an untuned LightGBM's mean RMSE by at most 0.62, and created_at
          alone scores a skill of 0.04.
        - The split is temporal (Lennart, 2026-11-04), replacing the site-balanced random folds Myunghwan approved on
          2026-10-28; see the splits comment.
        - CC (2026-11-05, Lennart): five monthly windows from October 2020 instead of the three dry-season months
          (issue 1, A; SPLIT-20, as aeolus and perth_house_prices widened theirs). The test now holds 4,631 hours
          (4,624 after issue 2) over both seasons, and October and November score all three sites; the smallest
          train side is 57.3% (SPLIT-14). Nakawa enters the October window with 63 hours of history (2020-09-19 to
          2020-09-23), so its October hours are close to a new-site test inside this known-site task (USE-10). It
          supersedes the three windows of 2026-11-04 ("ok (a)").
        - CC (2026-11-05, Lennart): the 92-hour Nakawa reference outage leaves (issue 3, A; CLEAN-11 impossible-value
          clause, then CLEAN-15; as qsar_tid_11 and 2024_lusaka_mobility_prediction_hackathon). A Nakawa hour of
          2020-11-10 to 2020-11-23 with the reference below 0.3 times both low-cost PM2.5 channels is a failed
          reference: 92 hours, reference 0.1 to 11.2 against channels of 12 to 190, while Nakawa's monthly median
          ratio of reference to sensor 1 is 1.04 to 1.21 elsewhere. The target is set missing and the rows leave;
          the definition raises unless the count is 92. Without the date bound the same test catches 96 Nakawa hours.
          Under the five windows these are November 2020 test labels; November keeps 599 hours, 260 of them at Nakawa
          (596 and 258 after issue 2).
        - CC (2026-11-05, Lennart): one symmetric dead-channel rule at 0.27 (issue 4, B; CLEAN-11; as heart_disease,
          ashrae and protein_model_quality_rf_pcp): a sensor whose PM2.5 is below 0.27 times the other sensor's has
          both its channels set missing, and the row stays. It adds 16 sensor-2 hours of the 2019 outage and 18
          sensor-1 hours (2019-11-13/14, 2020-06-07/08), all at USEmbassy and on every window's training side; the
          definition raises unless the counts are 500, 16 and 18. Dead hours reach a ratio of 0.255, and the lowest
          live one, Makerere 2020-12-05 06:00 at 0.294 (December test window), stays a reading.
        - CC (2026-11-05, Lennart): the spike rule becomes an instrument-error rule for every window, test windows
          included (issue 2, (a) of its consistency check; CLEAN-11 impossible-value clause, then CLEAN-15; as the
          Nakawa outage, qsar_tid_11 and 2024_lusaka_mobility_prediction_hackathon). Collocated instruments sample
          the same air, so a reference hour several times both sensors and the hours around it is a value the
          reference could not have read ("we think the value is wrong"). A reference hour above 3 times both PM2.5
          channels and above 3 times the same site's reference in each neighbouring hour present, with at least one
          present (an outage hour counts as absent), is set missing and the row leaves; the definition raises unless
          the count is 12. It adds the four look-alikes with a missing neighbour, Nakawa 2020-10-29 17:00 (172.1),
          2020-11-02 18:00 (232.1), 2021-01-01 22:00 (147.2) and Makerere 2020-12-08 14:00 (82.9), and three more:
          Nakawa 2020-10-13 05:00 (36.2 against channels of 11.1 and 11.8, the weakest at 3.06 times, before a
          morning rise the sensors show by 07:00), 2020-11-04 13:00 (40.4 against 6.7 and 7.2) and USEmbassy
          2020-11-06 02:00 (155.0 against 30.4 and 31.6). All 12 are test labels (October 6, November 3, December,
          January and February 1 each); 10,828 rows ship. USEmbassy 2021-02-10 07:00 (459.0 against 153.2 and 161.7,
          before 99.0, no 08:00 hour) stays: it is 2.84 times sensor 2, and a channel factor of 2.83 would catch it
          and no other hour. LightGBM's mean RMSE goes from 16.69 to 15.34 (November 13.0 to 9.3, January 16.8 to
          14.7).
        - CC (2026-11-05, Lennart): the declared metric (RMSE on the original micrograms-per-cubic-metre scale, the
          source's) is checked and stays as declared. Public data redistribution permission
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
    temporal = Temporal(on="created_at", splits=TemporalSplits(window=1, unit="months", n_windows=5))
    splits_comment = """
        Five one-month windows, newest first: February 2021 to October 2020 (Lennart, 2026-11-05; issue 1, A). Each
        trains on every earlier hour (6,204 to 9,994 rows, 57-92%); the test months hold 596 to 1,310 hours. A model
        refit at the start of each month corrects that month's readings; the monthly cadence is the curator's
        judgment (Lennart, 2026-11-04). Adong et al. (2022) say it is "important to retrain these models
        periodically" and name "seasonal re-calibration" as future work; AirQo's refit practice is not documented.
        The test covers both seasons: mean reference 42.3 and 40.5 in October and November, two months of the
        September-November rains, against 44.8, 49.5 and 74.2 in the December-February dry season (SPLIT-20). The
        three dry-season windows of 2026-11-04 ("ok (a)") are superseded. Site coverage differs by month: October and
        November score all three sites, December has no USEmbassy rows, January 45, February no Nakawa. History before
        the test months: USEmbassy from 2019-07-25, Makerere from 2020-07-15 (2.5 to 6.5 months), and Nakawa from
        2020-09-19 with only 63 hours (to 2020-09-23) before the October window, then 1.4 to 3.4 months; Nakawa's
        October hours are close to a new-site test (USE-10). The reference is for the same hour and no reporting
        delay is documented, so no gap is needed; no training row has a label from after its window start. Random
        folds over the hourly stream gave the model reference labels of neighbouring hours and scored a quarter better
        (untuned LightGBM, one seed, mean RMSE 11.23 against 15.34 on the same five test months; trained on an
        equal-size random draw of all other months, future included, 14.53). Superseded 2026-11-05: 12.94 against
        18.26 on the three windows (review panel, 2026-11-04).
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
        # Dead channels become missing, the rows stay (CLEAN-11; Lennart, 2026-11-04 and 2026-11-05).
        df, dead = _mask_dead_channels(df)
        expected = {"sensor 2, both channels 0": 500, "sensor 2, below 0.27 of sensor 1": 16}
        expected["sensor 1, below 0.27 of sensor 2"] = 18
        for kind, n in expected.items():
            if dead[kind].sum() != n:
                raise ValueError(f"Expected {n} dead hours ({kind}), found {int(dead[kind].sum())}")
        outage, spikes = _reference_errors(df)
        if outage.sum() != 92:
            raise ValueError(f"Expected 92 Nakawa reference-outage hours, found {int(outage.sum())}")
        if spikes.sum() != 12:
            raise ValueError(f"Expected 12 single-hour reference errors, found {int(spikes.sum())}")
        # Impossible reference values in every window; a row without a valid target is no task row (CLEAN-11,
        # CLEAN-15; Lennart, 2026-11-04 and 2026-11-05).
        df = df.loc[~(spikes | outage)]
        return decode(df, {"landform_90m": LANDFORMS})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=("site", "landform_90m"), datetime={"created_at": "ISO8601"})

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        masked, dead = _mask_dead_channels(raw)
        outage, spikes = _reference_errors(masked)
        return [
            Decision(
                "Dead sensor channels set missing",
                "Both sensor-2 channels read exactly 0 in 500 USEmbassy hours (2019-11-18 to 2019-12-17) while "
                "sensor 1 and the reference show ordinary pollution, so the channel was dead (Lennart, 2026-11-04). "
                "One symmetric rule takes the rest of the same failure (Lennart, 2026-11-05): a sensor whose PM2.5 "
                "is below 0.27 times the other sensor's is dead, 16 more sensor-2 hours of that outage and 18 "
                "sensor-1 hours (2019-11-13/14, 2020-06-07/08). Dead hours reach a ratio of 0.255; the lowest live "
                "ratio is 0.294 (Makerere 2020-12-05 06:00). The dead sensor's two channels are set missing and the "
                "rows stay (CLEAN-11). The missing weather values stay too.",
                _dead_table(raw, dead),
            ),
            Decision(
                "Single-hour reference errors dropped",
                "Twelve reference hours read above 3 times both low-cost PM2.5 channels and above 3 times the same "
                "site's reference in each neighbouring hour in the file, with at least one there (Nakawa 2020-10-03 "
                "10:00: 444.0 against channels of 35 and 36 and neighbours of 47.5 and 86.0). Collocated instruments "
                "sample the same air, so a single hour that neither the sensors nor the hours around it share is an "
                "instrument error of the reference, an impossible value. They become missing and the rows leave, in "
                "the test windows too (CLEAN-11, CLEAN-15; Lennart, 2026-11-04 and 2026-11-05, issue 2), by the rule, "
                "not by hand.",
                _spikes_table(masked, outage, spikes),
            ),
            Decision(
                "Nakawa reference outage dropped",
                "From 2020-11-10 to 2020-11-23, 92 Nakawa hours have the reference below 0.3 times both low-cost "
                "PM2.5 channels (2020-11-21 02:00: 0.1 against 101.2 and 102.0); outside these days Nakawa's monthly "
                "median ratio of reference to sensor 1 is 1.04 to 1.21. Collocated instruments sample the same air, so "
                "the reference failed: an impossible label, set missing, and the rows leave (CLEAN-11, CLEAN-15; "
                "Lennart, 2026-11-05). The rule is bounded to the run's site and days; without the date bound the same "
                "test catches 96 Nakawa hours.",
                masked.loc[outage]
                .assign(day=pd.to_datetime(masked.loc[outage, "created_at"]).dt.strftime("%Y-%m-%d"))
                .groupby("day")
                .agg(
                    hours=("ref_pm2_5", "size"),
                    reference_median=("ref_pm2_5", "median"),
                    sensor1_pm2_5_median=("pm2_5", "median"),
                    sensor2_pm2_5_median=("s2_pm2_5", "median"),
                )
                .round(1)
                .reset_index(),
            ),
        ]


def _dead_table(raw: pd.DataFrame, dead: dict[str, pd.Series]) -> pd.DataFrame:
    """Per kind of dead channel: the hours, their dates, the dead and the live sensor's PM2.5 and the reference."""
    rows = []
    for kind, mask in dead.items():
        r = raw.loc[mask]
        dead_col, live_col = ("pm2_5", "s2_pm2_5") if kind.startswith("sensor 1") else ("s2_pm2_5", "pm2_5")
        rows.append(
            {
                "kind": kind,
                "site": ", ".join(sorted(r["site"].unique())),
                "hours": len(r),
                "first": r["created_at"].min(),
                "last": r["created_at"].max(),
                "dead_pm2_5_max": round(float(r[dead_col].max()), 2),
                "live_pm2_5_mean": round(float(r[live_col].mean()), 1),
                "reference_mean": round(float(r["ref_pm2_5"].mean()), 1),
            }
        )
    return pd.DataFrame(rows)


def _spikes_table(masked: pd.DataFrame, outage: pd.Series, spikes: pd.Series) -> pd.DataFrame:
    """The reference hours the spike rule drops, with both channels and the neighbouring reference values."""
    nb = _neighbour_references(masked.assign(ref_pm2_5=masked["ref_pm2_5"].mask(outage)))
    cols = ["site", "created_at", "pm2_5", "s2_pm2_5", "ref_pm2_5"]
    return (
        masked.loc[spikes, cols]
        .join(nb.loc[spikes])
        .sort_values("created_at", kind="stable")
        .round(1)
        .reset_index(drop=True)
    )
