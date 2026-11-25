"""Curated dataset definition for GeoAI ground-level NO2. Evidence: README.md."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
from data_foundry.time_basis import TimeBasis
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, Source, TaskSummary


class GeoaiGroundLevelNo2EstimationChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is the daily ground-level nitrogen dioxide concentration at a monitoring location withheld from training?",
        use_case="An air-quality analyst reconstructs daily pollution at unmonitored locations within the observed region, using the complete 2019-2021 archive from other stations after all daily products are available, to map daily exposure between monitors.",
        row="One labeled station-day from 79 northern Italian monitoring stations during 2019-2021; 82,051 rows.",
        predicted="Daily ground-level nitrogen dioxide concentration in micrograms per cubic metre, measured by a ground station.",
        known="The location and date; that day's CHIRPS precipitation; daytime land-surface temperature, aerosol index, cloud fraction, satellite nitrogen dioxide columns and tropopause pressure from single early-afternoon satellite overpasses on that day.",
        split="Whole stations are held out across all dates. Test locations are unseen, while their observation dates overlap the training period.",
        changes="We omit station-days without a measured target, discard the submission identifier, restore training dates and evaluate on new station splits of the labeled release.",
        fit="approximate",
        fit_reason="The challenge explicitly estimates surface pollution at withheld stations. Monitoring sites stand in for unmonitored locations, and no input says how a station is sited (traffic or background). The inputs are satellite-only by the source's design, without meteorology or land use. Inputs arrive within days (satellite) to about seven weeks (CHIRPS final precipitation) after the day, which suits retrospective mapping but not same-day use. The ground-truth daily quality-control procedure is not documented.",
    )
    unique_name = "geoai_ground_level_no2_estimation_challenge"
    sources = (
        Source(
            role="publication",
            platform="Zindi",
            url="https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge",
            license="CC BY-SA 4.0",
            year="2024",
            bibtex="""
        @misc{zindi2024geoaino2,
          title={GeoAI Ground-level NO2 Estimation Challenge},
          author={{ITU AI for Good}},
          year={2024},
          howpublished={Zindi},
          url={https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge}
        }
    """,
        ),
    )
    domain = "environmental science & climate"
    data_tags = ("Spatial",)
    split_leaf = "L-FILL.whole"
    time_basis = TimeBasis(
        "RetrospectiveFillIn",
        "daily readings of 79 ground monitors of ARPA Lombardia and ARPAV (Veneto), 2019-01-01 to 2021-12-31, with "
        "same-day satellite and precipitation inputs; the use case reconstructs daily NO2 at locations without a "
        "monitor in that period, while the other stations of the same days are measured (date and coordinates are "
        "features), so their same-day readings are the use, not a leak (copying the nearest same-day station scores "
        "worse than the model on 9 of 9 folds). Not tested: a later year, or a region outside the network.",
    )
    download_description = """
        Download the original challenge archive from the Zindi Data page after accepting its access terms:
        https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge/data
        Preserve geoai-ground-level-no2-estimation-challenge20240710-12938-q3sk51.zip
        (SHA256 a9d52bff254a802f6f100a965d3e4dca3a49f97bf83b2b1c3a52f35d559bdbc4).
        Extract its files into local-data-warehouse/geoai_ground_level_no2_estimation_challenge/original-zindi-20261030/.
        This definition uses Train.csv, SHA256 fdee673ab76a4589cf118e10bcb6250ac6c58f132cec76d52ffc6f8b7d104446.
        The archive was supplied directly by the curator; an unauthenticated download command is not available.
    """
    curation_comments = """
        Start from the original challenge archive's Train.csv and its DataDescription.pdf.
        - Prediction is retrospective daily estimation at an unseen location using the complete 2019-2021 archive from other stations, after the daily satellite and weather products are available. Training includes dates later than individual test days; this is not an as-of-day forecast or real-time service. The exposure-mapping actor is our interpretation of the challenge's spatial-estimation objective.
        - Each prediction uses only the query row from the held-out station. Group context is none: no other rows from that held-out station may be used for feature aggregation or filling. The complete labeled training archive at other stations remains available; same-day spatial signal from those training stations is consistent with the retrospective task.
        - The original Train.csv has 86,584 station-days: 79 stations over 1,096 dates. Drop only the 4,533 missing targets, retaining 82,051 observations and all 79 stations. Labeled coverage is 298-1,093 days per station; two stations lack about 72% of labels. Scores represent observed station-days, not monitor downtime. The seven observed zero targets and the maximum 188.2333333 remain; their magnitude alone does not establish an invalid measurement.
        - The provided DataDescription.pdf attributes the ground measurements, in micrograms per cubic metre, to "ARPA"; the stations lie in Lombardy and Veneto, whose agencies are ARPA Lombardia and ARPAV, and their daily aggregation rules may differ (not measured, 2026-11-21). Satellite nitrogen dioxide columns are atmospheric column densities in mol/m2, not alternate measurements of the surface target. The daily aggregation and quality-control details of the ground labels are not supplied.
        - Training dates use day/month/year with mixed slash and dash separators. Parse each separator explicitly: the result is 1,096 consecutive days per raw station grid, 2019-01-01 to 2021-12-31. The unlabeled Test.csv uses month/day/year; it is preserved but is not part of this dataset.
        - ID is a station grouping key and is excluded from model features. ID_Zindi is a submission identifier and is dropped. Two submission identifiers repeat across different station-days; these are not duplicate observations and are not deduplicated by identifier.
        - Keep all eight physical predictors, latitude, longitude and the restored date. Preserve missing inputs for the benchmark pipeline; do not impute, smooth, interpolate, add neighboring target values or filter stations by model performance.
        - Retain small negative satellite NO2 retrievals: the linked Sentinel-5P product documentation attributes these to retrieval noise and advises keeping ordinary negatives. No observation is below its extreme-negative threshold of -0.001 mol/m2. The largest cloud fraction exceeds one by only 4.4e-8, a negligible precision artifact.
        - The source's leaderboard metric is RMSE on the original concentration scale. Each retained station-day is scored once per test fold; stations hold 298-1,093 labelled days, and how far counting each station once would move the model ranking is not yet measured. The source additionally described correlation and MAE for jury assessment; those do not replace its leaderboard metric.
        - The six unlabeled challenge stations have no station or coordinate overlap with the 79 training stations. Internal station-held-out folds reproduce that spatial-estimation question, but not the exact competition test locations. Overlapping dates are intentional; this does not evaluate future-year or distant-region transfer.
        - The six satellite columns are bands of one Sentinel-5P L3 NO2 overpass (early afternoon): NO2_trop is filtered at QA >= 0.75 (40.7% missing), the other five at QA >= 0.5 (14.8% missing). The TROPOMI NO2 processor changed within the period (v1.4 in December 2020, v2.2 in July 2021); both split sides share all dates, so the grouped split is unaffected. The source calls the land-surface temperature NOAA's, but the 13 values its README shows all lie on a 0.02 K grid, the scaling of MODIS and VIIRS land-surface temperature: the product is unconfirmed until DataDescription.pdf is read.
        - Accepted as implemented by Myunghwan on 2026-10-30: retain the source labels despite undocumented daily aggregation and quality control, with regional same-period station-transfer and uneven observed-label coverage limits. These remain documented uncertainties, not verified source procedures.
        - Split walk (the split decision tree, SPLIT-36, from the record's collection type Panel Data): [PAN.when] the model fills in daily NO2 at places without a monitor in the period the data covers: fill in → Fill-in step → [FILL.later] the labels arrive with their day, not later: no → [FILL.scattered] the places to fill are stations not in the network: whole units → [FILL.key] the station ID is a key: yes → leaf L-FILL.whole, Grouped · `RetrospectiveFillIn`, whole stations held out with all their days. The definition ships station groups, this leaf's split; time basis declared (`RetrospectiveFillIn`).
    """
    target = "GT_NO2"
    problem_type = "regression"
    metric = Metric.source("rmse", original="Root Mean Squared Error (RMSE)", reference=sources[0].url)
    grouping = Grouping(
        on="ID",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="One group is one ground monitoring station, identified by ID. Each station has a unique coordinate pair. All its dates stay on one side of a split, matching the challenge's estimation at withheld stations. A prediction is one day's concentration; no measured target from the new station is available.",
    )
    splits_comment = """
        Use the standard grouped protocol on station ID. Whole stations and all their dates stay together.
        Training uses the complete 2019-2021 archive at other stations; testing covers the same dates, as in the source challenge. This measures spatial
        estimation within the observed region and period; it does not estimate forecasting or geographic extrapolation performance.
        The split tree gives Grouped · RetrospectiveFillIn (whole units, areas or groups), L-FILL.whole.
    """
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        path = raw_dir / "original-zindi-20261030" / "Train.csv"
        expected = "fdee673ab76a4589cf118e10bcb6250ac6c58f132cec76d52ffc6f8b7d104446"
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("Train.csv differs from the preserved original Zindi release")
        return pd.read_csv(path)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.dropna(subset=[self.target]).drop(columns=["ID_Zindi"]).copy()
        # Train and Test have different date conventions; only Train enters this definition.
        slash = df["Date"].str.contains("/", regex=False)
        dates = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
        dates.loc[slash] = pd.to_datetime(df.loc[slash, "Date"], format="%d/%m/%y")
        dates.loc[~slash] = pd.to_datetime(df.loc[~slash, "Date"], format="%d-%m-%y")
        df["Date"] = dates
        assert not df.duplicated(["ID", "Date"]).any(), "Station-day keys must be unique"
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=("ID",), datetime=("Date",))
