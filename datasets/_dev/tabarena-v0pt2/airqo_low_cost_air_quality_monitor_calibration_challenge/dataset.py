"""Same-hour reference PM2.5 calibration for represented historical AirQo records."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary, drop_columns


class AirqoLowCostAirQualityMonitorCalibrationChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What reference-monitor PM2.5 value corresponds to this historical low-cost monitor reading?",
        use_case=(
            "AirQo corrects archived low-cost readings using a model learned from hours with collocated reference "
            "measurements. This task estimates missing reference-equivalent values within the represented sites "
            "and historical conditions; it does not validate later operation or transfer to new devices."
        ),
        row="One hourly collocated low-cost/reference observation at one of three Kampala sites, from 2019 to 2021.",
        predicted="The same-hour reference-monitor PM2.5 mass concentration in micrograms per cubic metre.",
        known=(
            "The recorded hour and site, both low-cost sensors' PM2.5 and PM10 readings, temperature, humidity "
            "and site descriptors. Reference values from other hours are not added as predictors."
        ),
        split=(
            "Random held-out labeled hours within the represented historical collocations. Sites and nearby times "
            "can recur; this tests retrospective correction, not later-month or unseen-site generalization."
        ),
        changes=(
            "Use only the labeled Train.csv; retain all rows and values. Drop the opaque row ID, parse the "
            "recorded UTC+3 timestamp, and type the site and discrete 90m landform as categorical."
        ),
        fit="approximate",
        fit_reason=(
            "The organizer explicitly describes retrospective correction as the initial use. This narrow "
            "three-site task does not establish network/device transfer. Exact hourly reference aggregation, "
            "upstream filtering and availability timing of weather/site metadata remain unverified."
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
        We start with all 10,932 labeled rows in the supplied 2021 competition Train.csv.

        - Prediction point: retrospective correction of an already recorded cheap-monitor hour, using the
          supplied sensor readings and archived weather/site context. The reference value for that hour is
          withheld. The organizer's 16 May 2021 discussion reply describes historical correction first, followed
          by real-time conversion; the benchmark tests the first application only.
        - Myunghwan's 2026-10-27 clarification supports the original setup when historical calibration is useful.
          The source and paired measurements establish that use. Myunghwan approved this presented retrospective
          definition for shipping on 2026-10-28. Known site descriptors do not establish future or device transfer.
        - Keep ref_pm2_5 on its original micrograms-per-cubic-metre scale, with source RMSE. All labels are observed
          and positive (0.1 to 459.0); no target transformation, clipping, weighting or row filter is applied.
        - Drop ID: it is an opaque, unique row key. Parse created_at as the supplied UTC+3 time without adding
          another three-hour shift. No target lags, leads, reference-neighbor features or full-data label transforms.
        - Treat site and landform_90m as nominal. The source's Google Earth Engine links identify landform_90m as
          discrete ALOS landform classes and landform_270m as continuous mTPI; its -11 valley value is valid.
          Keep landform_270m numeric. Keep the original greenness scale because its rescaling is undocumented.
        - Keep ordinary missingness: six humidity and 17 temperature values. Sensor2 PM2.5/PM10 are jointly zero
          in 500 labeled USEmbassy hours, including long runs. An outage code is not documented, so retain these
          values without guessing a repair or removing rows; sensor1 remains available. Exact upstream averaging
          and reference-label construction are unknown; unusual positive values are not proven erroneous.
        - All 16 predictors remain after ID removal. The eight geographic/site descriptors are constant within
          each site and can encode its identity; recurrence is legitimate only for this represented-site task.
          Weather readings at shared clock times agree across sites. No duplicate site-hour or exact predictor copy
          occurs in the supplied labeled file.
        - The supplied Test.csv has 2,733 rows, approximately 20 percent within each site, over overlapping dates.
          It has no reference labels. Training uses only labeled Train.csv; random CV follows the source-described
          retrospective sampling rather than pretending to recreate the unlabeled leaderboard split.
        - Later-month and unseen-site comparisons are separate application diagnostics, not a score-based reason
          to select random CV. New-site transfer and future drift require their own qualified protocols. Exact
          device serials, source reference aggregation and site-metadata snapshot dates remain unverified.

        - On all nine declared folds, fixed untuned models gave mean fold RMSE 35.568 for the training mean,
          21.048 for raw sensor1, 20.296 for a two-sensor linear correction, 16.424 for Ridge, 14.204 for a forest
          and 13.237 for LightGBM. The best single feature, selected within training only, was PM10 (19.298).
          All three model families beat the dummy on every fold; these repeated scores are not independent deployments.
        - Two Nakawa references, at 2020-10-03 10:00 and 2020-10-17 09:00 UTC+3 (444.0 and 374.5), disagree
          with both cheap PM2.5 channels (about 35 and 37).
          They account for 14.13 percent of the final LightGBM's repeated out-of-fold squared error. Reference quality
          flags and original aggregation are unavailable; neither corruption nor a general timestamp shift was proved.
          Retain these observations and source RMSE rather than delete difficult outcomes or change the metric.
        - Exact feature-copy share is zero. Native hidden-group probes report no hits; quantized near-copy profiles
          cover 17.72 percent of rows but have only a 0.001215 skill gap. Examined pairs are same-site, different-hour
          observations, not duplicate dynamic readings. The source's target-neighbor discussion does not imply that
          such inputs were added: a training-label-only interpolation control scored 19.835 RMSE on these nine folds.
        - About 77.68 percent of test rows have a same-site training hour within one hour. That recurrence is explicit
          in retrospective calibration. It does not certify accuracy on held-out future periods. Native task probes
          cover five of nine folds and have no flags. The separate fixed-model qualification covers all nine folds.
        - The pinned leak CLI fails on timezone-aware date selection in this runtime. A local diagnostic compatibility
          run restores its intended datetime exclusion and checks 15 predictors on three folds; it is not a successful
          unchanged CLI run or a timestamp leakage test. The separate full 16-predictor qualification includes time.
        - Myunghwan approved the presented package on 2026-10-28, retaining the site-balanced random folds.
          Site stratification balances three discrete non-target categories; its regression warning is accepted
          for this represented-site archive population. Public data redistribution permission
          is not established by these checks; the source's private-participant restrictions remain in force.
    """
    accepted_check_warnings = {
        "task_stratify_on_regression": "Balance random regression folds on the three discrete non-target site categories so each fold represents the same known-site archive population; this does not stratify continuous target values or claim unseen-site evaluation. Myunghwan approved the presented calibration package for shipping on 2026-10-28.",
    }

    target = "ref_pm2_5"
    problem_type = "regression"
    stratify_on = "site"
    metric = Metric.source(
        "rmse",
        original="Root Mean Squared Error",
        reference="https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge#evaluation",
        definition="Square root of the mean squared error on original reference PM2.5, in micrograms per cubic metre",
    )
    splits_comment = """
        Site-stratified random three-fold cross-validation repeated three times, split seed 4267 and row shuffle 42.
        Test observations are withheld historical hours from the represented collocations. Sites and nearby times
        recur. At the correction moment the archive is already recorded; this does not simulate a model trained only
        before each measured hour. No future-operation, entirely new site or arbitrary new-device claim follows.
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
        return drop_columns(raw, ["ID"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=("site", "landform_90m"), datetime={"created_at": "ISO8601"})

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        evidence = raw.groupby("site").agg(
            labeled_hours=("ID", "size"),
            sensor2_joint_zero=("s2_pm2_5", lambda x: int(x.eq(0).sum())),
            reference_min=("ref_pm2_5", "min"),
            reference_max=("ref_pm2_5", "max"),
        )
        return [
            Decision(
                "Preserve observed readings for retrospective calibration",
                "Keep all source rows, missing weather and unverified zero-sensor states. The task concerns "
                "represented historical collocations; the evidence does not establish arbitrary device transfer.",
                evidence,
            )
        ]
