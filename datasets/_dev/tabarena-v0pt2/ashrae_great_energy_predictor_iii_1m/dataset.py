"""Curated dataset definition for `ashrae_great_energy_predictor_iii_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
    set_missing,
)

METER_TYPES = {0: "electricity", 1: "chilledwater", 2: "steam", 3: "hotwater"}
"""The meter codes of train.csv, as the competition's data page names them; BDG2 names its meter files the same."""

SITE_0_RECORDING_GAP_END = "2016-05-21"
"""Site 0's electricity meters read 0 until 2016-05-20 (344,577 of the 348,560 hours before this date)."""

OPERATING_MONTHS = {
    "chilledwater": (5, 6, 7, 8, 9, 10),
    "steam": (11, 12, 1, 2, 3, 4),
    "hotwater": (11, 12, 1, 2, 3, 4),
}
"""The months a cooling or heating plant runs: chilled water May-October, steam and hot water November-April."""

MIN_ZERO_RUN_HOURS = 48
"""A cooling or heating meter that reads 0 this many hours in a row in its operating months has stopped recording."""

MIN_STUCK_RUN_HOURS = 168
"""A meter that repeats one non-zero reading for a week has stopped recording."""

UNIT_ERROR_METER = (1099, "steam")
"""Building 1099's steam meter reads about 1,000 times its level in January-June 2016, in the competition data and
in BDG2's files alike."""

UNIT_ERROR_FACTOR = 10
"""A reading of that meter above this multiple of its median is the unit error."""

KAGGLE_UNITS = {1.0: "kWh", 3.41: "kBTU", 0.00341: "mmBTU", 0.284: "ton-hours", 3.28: "lb of steam"}
"""The competition's unit per Kaggle-to-kWh factor (3 significant digits), from BDG2's conversion table (paper, Table 5)."""

SITE_UTC_OFFSET_HOURS = {
    0: -5,
    1: 0,
    2: -7,
    3: -5,
    4: -8,
    5: 0,
    6: -5,
    7: -5,
    8: -5,
    9: -6,
    10: -7,
    11: -5,
    12: 0,
    13: -6,
    14: -5,
    15: -5,
}
"""Hours from UTC (the weather files) to the local standard time of the meter readings, per site: the offsets of the
1st place solution (`solutions/rank-1/scripts/02_preprocess_data.py` of
github.com/buds-lab/ashrae-great-energy-predictor-3-solution-analysis, the competition team's solution repository)."""


def recording_errors(df: pd.DataFrame) -> pd.DataFrame:
    """Flag the hours a meter did not record, one column per rule, in the row order of ``df``.

    ``df`` holds one row per meter and hour with ``building_id``, ``site_id``, ``meter`` (names), ``timestamp`` and
    ``reading_kwh``. A run is a stretch of consecutive hours of one meter with the same reading.
    """
    meters = df.sort_values(["building_id", "meter", "timestamp"], kind="stable")
    reading, meter, timestamp = meters["reading_kwh"], meters["meter"], meters["timestamp"]
    repeat = (
        meters["building_id"].eq(meters["building_id"].shift())
        & meter.eq(meter.shift())
        & reading.eq(reading.shift())
        & timestamp.diff().eq(pd.Timedelta(hours=1))
    )
    run = (~repeat).cumsum()
    run_hours = run.map(run.value_counts())
    zero = reading == 0
    electricity = meter == "electricity"
    in_season = pd.Series(False, index=meters.index)
    for name, months in OPERATING_MONTHS.items():
        in_season |= (meter == name) & timestamp.dt.month.isin(months)
    unit_error_meter = (meters["building_id"] == UNIT_ERROR_METER[0]) & (meter == UNIT_ERROR_METER[1])
    flags = pd.DataFrame(
        {
            "site_0_gap": (meters["site_id"] == 0) & electricity & (timestamp < SITE_0_RECORDING_GAP_END),
            "electricity_zero": electricity & zero,
            "plant_zero_in_season": in_season & zero & (run_hours >= MIN_ZERO_RUN_HOURS),
            "stuck_for_a_week": ~zero & repeat & (run_hours >= MIN_STUCK_RUN_HOURS),
            "unit_error": unit_error_meter & (reading > UNIT_ERROR_FACTOR * reading[unit_error_meter].median()),
        }
    )
    return flags.loc[df.index]


class AshraeGreatEnergyPredictorIii1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much energy would a building's meter have used in a given hour, given the building, the time and the"
            " weather?"
        ),
        use_case=(
            "After an energy-efficiency retrofit, an engineer or investor estimates what the building would have used"
            " without it, from a model fit on the readings before, and credits the difference as savings (the "
            "competition's purpose)."
        ),
        row=(
            "One hourly reading of one meter (electricity, chilled water, steam or hot water) of one building of the "
            "competition, 2016-2017; of the 39.1M readings, the splits use every one before September 2017 and "
            "500,000 of September-December 2017."
        ),
        predicted=(
            "The meter's reading in that hour in kWh (the heating and cooling meters converted to kWh by the "
            "competition's organisers), scored on a logarithmic scale as in the competition."
        ),
        known=(
            "The building (site, primary use, floor area, year built, floors), the meter type, the local date and "
            "hour, and the site's weather in that hour (temperature, dew point, cloud, rain, pressure, wind); no "
            "reading after the cutoff."
        ),
        split=(
            "Three four-month windows tile 2017, newest first, each trained on all earlier readings, of which a "
            "benchmark fits on a random million of the newest year. A savings baseline is fit once and used for a "
            "year or more without a refit, so the window is the longest that gives three windows inside 2017; the "
            "oldest trains on 2016 alone, just under half the readings."
        ),
        changes=(
            "We add the competition's 2017 readings, which its organisers released later with every meter in kWh, "
            "to split by time and to put all meters in one unit. Hours when a meter was not recording are dropped, as"
            " the top teams did: electricity at 0, a heating or cooling plant at 0 for two days in its season, a "
            "reading stuck for a week, and one steam meter's unit error."
        ),
        fit="direct",
        fit_reason=(
            "As in measuring retrofit savings, the model sees only the building, the time and the observed weather of"
            " each hour, never a later reading, and is fit on earlier readings. Hours when a meter did not record "
            "are dropped, as the savings would be measured on recorded hours only; the noise of real meters stays."
        ),
    )

    # Dataset
    unique_name = "ashrae_great_energy_predictor_iii_1m"
    domain = "environmental science & climate"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/ashrae-energy-prediction",
            license="Kaggle Competition Rules (7A: use for any purpose, commercial or non-commercial; 7B: no redistribution to "
            "anyone not participating in the competition); the 2017 readings and the readings in kWh from BDG2: MIT License at the pinned commit "
            "(2020), CC BY 4.0 on its Zenodo release v1.0 (doi 10.5281/zenodo.3887306), and a LICENSE headed "
            "'Attribution-ShareAlike 4.0 Unported' in the repository since 2023-10-14",
            year="2019",
            bibtex=r"""
                @misc{Howard2019ASHRAEGreatEnergyPredictorIII,
                  author = {Addison Howard and Chris Balbach and Clayton Miller and Jeff Haberl and Krishnan Gowri and Sohier Dane},
                  title = {ASHRAE - Great Energy Predictor III},
                  year = {2019},
                  howpublished = {\url{https://kaggle.com/competitions/ashrae-energy-prediction}},
                  note = {Kaggle competition}
                }
                @article{Miller2020GEPIII,
                  author = {Clayton Miller and Pandarasamy Arjunan and Anjukan Kathirgamanathan and Chun Fu and Jonathan Roth and June Young Park and Chris Balbach and Krishnan Gowri and Zoltan Nagy and Anthony D. Fontanini and Jeff Haberl},
                  title = {The {ASHRAE} Great Energy Predictor {III} competition: Overview and results},
                  journal = {Science and Technology for the Built Environment},
                  volume = {26},
                  number = {10},
                  pages = {1427--1447},
                  year = {2020},
                  doi = {10.1080/23744731.2020.1795514}
                }
                @article{Miller2020BDG2,
                  author = {Clayton Miller and Anjukan Kathirgamanathan and Bianca Picchetti and Pandarasamy Arjunan and June Young Park and Zoltan Nagy and Paul Raftery and Brodie W. Hobson and Zixiao Shi and Forrest Meggers},
                  title = {The Building Data Genome Project 2, energy meter data from the {ASHRAE} Great Energy Predictor {III} competition},
                  journal = {Scientific Data},
                  volume = {7},
                  pages = {368},
                  year = {2020},
                  doi = {10.1038/s41597-020-00712-x}
                }
            """,
        ),
    )
    download_description = """
        We download four files of the Kaggle competition (train.csv holds 2016) and, from the Building Data Genome
        Project 2 (BDG2) repository of the competition's technical team, the competition's 2017 readings
        (kaggle.csv, sha256 67e6d3e82cc737d28389845fc5e526711705fc264fd178a7a0b6f8f3d8d3c82e), the raw meter files
        with every reading in kWh (one per meter type) and the building metadata that maps BDG2's building names to
        the competition's building_id. The files are Git LFS objects, pinned to the commit that added kaggle.csv. The
        competition's 2018 readings (its private test year) are not public.

        mkdir -p local-data-warehouse/ashrae_great_energy_predictor_iii && cd local-data-warehouse/ashrae_great_energy_predictor_iii
        for f in train.csv weather_train.csv weather_test.csv building_metadata.csv; do kaggle competitions download -c ashrae-energy-prediction -f $f -p .; done
        unzip train.csv.zip && unzip weather_train.csv.zip && unzip weather_test.csv.zip && rm train.csv.zip weather_train.csv.zip weather_test.csv.zip
        BDG2=https://media.githubusercontent.com/media/buds-lab/building-data-genome-project-2/9581aafed95b28e3d5ac39929c15fbc0ba36af5b/data
        mkdir -p bdg2/raw && wget -O bdg2/kaggle.csv $BDG2/meters/kaggle/kaggle.csv && wget -O bdg2/metadata.csv $BDG2/metadata/metadata.csv
        for m in electricity chilledwater steam hotwater; do wget -O bdg2/raw/$m.csv $BDG2/meters/raw/$m.csv; done
    """
    curation_comments = """
        We start with the Kaggle competition's train.csv (2016), building_metadata.csv and weather files and, from the BDG2 repository of its technical team, the 2017 readings (kaggle.csv), the raw meter files in kWh and their building metadata.

        - Prediction point: after a cutoff, the model gives each known meter's reading for a later hour from the building's metadata, the meter type, the local time and the site's weather, as in the competition; no later reading is an input. The top five teams fit boosted trees and neural networks on these inputs, with no lagged readings (GEPIII overview, Table 2).
        - Not a naive forecast: each meter's hour-of-week profile from the same month a year earlier scores RMSE 1.393 / 1.273 / 1.372 on the three windows, LightGBM with 1,000 trees on a random 1M of all earlier rows per window 1.261 / 1.176 / 1.223. One model per site does no better than one large model (1.238 / 1.178 / 1.222), so meter types and sites stay one task.
        - We stack 2016 and 2017, the competition's public test year ("matches seamlessly with the training data", BDG2 paper, p. 8), keeping the hours with a reading; 2018 is not public.
        - Units: the competition kept each site's own unit (ton-hours, pounds of steam, mmBTU, kBTU; BDG2 paper, Table 4). We take the readings in kWh from BDG2's raw files, converted and corrected by the same team (p. 8); per meter they differ from Kaggle's by one constant factor in 99.9% of the hours (decision table).
        - The weather is in UTC and the readings in local time (p. 8): we shift it by the 1st place solution's offsets and join it on site and hour. Daylight saving time at 8 sites changed RMSE by -0.007 to +0.005 per window, so we keep standard time.
        - Recording errors, removed as all top five teams did: site 0's electricity before 2016-05-21, electricity at 0, chilled water at 0 for 48 hours or more in May-October and steam or hot water in November-April, readings stuck for a week or more (site 5's electricity, March-November 2017), and building 1099's steam unit error (above 10 times its median, January-June 2016). 1.70M hours (4.2%, decision table).
        - 94.5% of the 2016 hours we drop are on the 1st place team's hand-made list of bad readings, and they cover 64% of that list. Zeros of heating and cooling meters outside their season stay: a plant switched off, which a model can learn.
        - The target is log1p of kWh, in one unit for all meters; the metric is the competition's RMSLE on kWh, computed after the inverse (`target_transform="log1p"`).
        - building_id and site_id are categories: the test hours belong to meters seen in train, as in the competition.
        - precip_depth_1_hr = -1 stays: it codes a trace of rain in NOAA's ISD-Lite data (format note, field 11).
        - `cloud_coverage` is in oktas (0-8), and 9 means the sky is obscured (fog or precipitation), so the cloud
          amount cannot be estimated (ISD's code table): 9,905 rows, missing (CLEAN-10; the curator's marks of
          2026-10-31, as in rain_in_australia).
        - The row budget: The cleaned frame has 39.1M hourly readings, so the dataset ships only as this `_1m` version. Each test window keeps at most 500k of its rows, drawn at random within the window (v2 split protocol), and each train side holds every earlier reading, so the container holds every reading before September 2017 and 500k of September-December 2017. The container records the 1M train budget, and a benchmark sub-samples each train side to 1M rows before a fit (`subsample_train`; by default a random 1M of the newest year before the window). A year covers every season, so the default sample keeps all seasons.
    """

    # Task
    target = "log1p_meter_reading"
    problem_type = "regression"
    metric = Metric.source(
        "rmsle",
        original="RMSLE (Root Mean Squared Logarithmic Error)",
        reference="https://www.kaggle.com/competitions/ashrae-energy-prediction/overview/evaluation",
        definition=(
            "sqrt(mean((log1p(pred) - log1p(actual))^2)) of kWh over all meter-hours, computed after the inverse of "
            "our log1p_meter_reading target."
        ),
        target_transform="log1p",
    )

    # Splits: three 4-month windows tile 2017, the competition's public test year.
    temporal = Temporal(
        on="timestamp",
        splits=TemporalSplits(window=4, unit="months", cutoffs=("2017-01-01", "2017-05-01", "2017-09-01")),
    )
    accepted_check_warnings = {
        "splits_train_under_half": (
            "Signed off (Lennart, 2026-11-10, review issue 1, A): January-April 2017 trains on 49.47% of the "
            "readings, beside 66.0% and 83.0%; SPLIT-14's two tiers admit it."
        ),
    }
    splits_comment = """
        Three test windows of 4 months tile 2017, the competition's first test year: September-December, May-August and January-April 2017, newest first; train is all earlier hours. The newest window always stays, and at 4 months January-April and May-August are the only two windows that overlap neither it nor each other, so the three windows test each season once (kept by the curator on 2026-11-10).
        A window is the horizon: a savings baseline is fit once on the year before a retrofit and predicts the year or two after it without a refit (the competition trained on 2016 to predict 2017 and 2018, GEPIII overview, Miller et al. 2020, Sec. 2.2; CalTRACK, Sec. 3.1.3 and 3.6.1.1; LBNL's NMEC guidance v2.0, p. 10), so the window is the longest that gives three windows inside 2017: four months. Windows of 3 or 2 months would fit (9 and 10 candidates above the floor) but score a model refit more often, an easier task than the use case.
        The oldest window trains on 2016 alone: 50.07% of the hours (8,784 of 17,544) but 49.47% of the rows (19,325,311 of 39,062,170), as 2016 has more gaps and drops (site 0's recording gap). We keep it under the floor's amendment of 2026-11-08: the two newer windows train on 66.0% and 83.0% of the rows, and an older window may train on 40% or more when most test entities recur; here every test meter's building is in training, and folds by entity would test unseen buildings. LightGBM (one seed, default parameters with 1,000 trees and early stopping on the last 10% of each train sample in time order, fit on the default 1M sample of the newest year before each window, the date in the recommended encoding) scores RMSLE 1.212, 1.342 and 1.213, newest first: 1.277 on the two valid windows and 1.256 on all three. The oldest window scores like the newest and moves the mean by about 0.02; the direction comes from May-August, which the absolute date features (year, total seconds) make harder: without them the scores are 1.240, 1.176 and 1.247 (1.208 on the two valid windows, 1.221 on all three).
        Each test window keeps at most 500k of its rows, drawn at random; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows, by default a random 1M of the newest year before the window (`subsample_train`).
    """
    row_budget = RowBudget(train=1_000_000, test=500_000)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        read = {
            "dtype": {"building_id": "int16", "meter": "int8", "meter_reading": "float64"},
            "parse_dates": ["timestamp"],
            "date_format": "%Y-%m-%d %H:%M:%S",
        }
        readings = pd.concat(
            [
                pd.read_csv(raw_dir / "train.csv", **read),
                pd.read_csv(
                    raw_dir / "bdg2" / "kaggle.csv",
                    usecols=["building_id", "meter", "timestamp", "meter_reading"],
                    **read,
                ),
            ],
            ignore_index=True,
        )
        # BDG2's raw meter files: one column per building (BDG2's names), the readings in kWh.
        names = pd.read_csv(raw_dir / "bdg2" / "metadata.csv", usecols=["building_id", "building_id_kaggle"])
        names = names.dropna(subset=["building_id_kaggle"])
        kaggle_id = dict(zip(names["building_id"], names["building_id_kaggle"].astype("int16"), strict=True))
        kwh = []
        for code, meter in METER_TYPES.items():
            wide = pd.read_csv(
                raw_dir / "bdg2" / "raw" / f"{meter}.csv", parse_dates=["timestamp"], date_format="%Y-%m-%d %H:%M:%S"
            )
            wide = wide[["timestamp", *[name for name in wide.columns if name in kaggle_id]]]
            long = wide.melt(id_vars="timestamp", var_name="building_id", value_name="reading_kwh").dropna()
            kwh.append(long.assign(building_id=long["building_id"].map(kaggle_id), meter=np.int8(code)))
        weather = pd.concat(
            [pd.read_csv(raw_dir / "weather_train.csv"), pd.read_csv(raw_dir / "weather_test.csv")],
            ignore_index=True,
        )
        buildings = pd.read_csv(raw_dir / "building_metadata.csv")
        return {
            "readings": readings,
            "kwh": pd.concat(kwh, ignore_index=True),
            "weather": weather,
            "buildings": buildings,
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        readings, kwh, weather, buildings = raw["readings"], raw["kwh"], raw["weather"], raw["buildings"]
        # The competition's hours with a reading (2017 hours without one are gaps the competition did not score), with
        # the reading in kWh from BDG2's raw files: the competition team's own release with the units converted.
        df = readings.loc[readings["meter_reading"].notna(), ["building_id", "meter", "timestamp"]]
        df = df.merge(kwh, on=["building_id", "meter", "timestamp"], how="left", validate="one_to_one")
        df = df.merge(buildings, on="building_id", how="left", validate="many_to_one")
        df["timestamp"] = df["timestamp"].astype("datetime64[ns]")
        df["meter"] = df["meter"].map(METER_TYPES)

        # Hours a meter did not record (site 0's 2016 gap, electricity at 0, a plant at 0 in its season, a stuck
        # reading, building 1099's unit error).
        df = df[~recording_errors(df).any(axis=1)]

        # The weather is in UTC: move it to the sites' local standard time, then join it on site and hour.
        weather = weather.assign(
            timestamp=pd.to_datetime(weather["timestamp"], format="%Y-%m-%d %H:%M:%S").astype("datetime64[ns]")
            + pd.to_timedelta(weather["site_id"].map(SITE_UTC_OFFSET_HOURS), unit="h")
        )
        # cloud cover 9: the sky obscured, the cloud amount cannot be estimated (curation notes)
        weather = set_missing(weather, {"cloud_coverage": [9]})
        df = df.merge(weather, on=["site_id", "timestamp"], how="left", validate="many_to_one")

        df["log1p_meter_reading"] = np.log1p(df["reading_kwh"])
        return drop_columns(df, ["reading_kwh"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["building_id", "meter", "site_id", "primary_use"],
            datetime=["timestamp"],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        weather = raw["weather"]
        utc = pd.to_datetime(weather["timestamp"], format="%Y-%m-%d %H:%M:%S")
        local = utc + pd.to_timedelta(weather["site_id"].map(SITE_UTC_OFFSET_HOURS), unit="h")
        temperature = weather["air_temperature"]
        by_utc = temperature.groupby([weather["site_id"], utc.dt.hour]).mean().unstack()
        by_local = temperature.groupby([weather["site_id"], local.dt.hour]).mean().unstack()
        hours = pd.DataFrame(
            {
                "utc_offset_hours": pd.Series(SITE_UTC_OFFSET_HOURS),
                "warmest_hour_utc": by_utc.idxmax(axis=1),
                "warmest_hour_local": by_local.idxmax(axis=1),
                "coldest_hour_local": by_local.idxmin(axis=1),
            }
        ).rename_axis("site_id")

        readings = raw["readings"][raw["readings"]["meter_reading"].notna()]
        readings = readings.merge(raw["kwh"], on=["building_id", "meter", "timestamp"], how="left")
        readings = readings.merge(raw["buildings"][["building_id", "site_id"]], on="building_id", how="left")
        readings["meter"] = readings["meter"].map(METER_TYPES)
        positive = (readings["meter_reading"] > 0) & (readings["reading_kwh"] > 0)
        factor = (
            (readings["meter_reading"] / readings["reading_kwh"])[positive]
            .groupby([readings["building_id"], readings["meter"]])
            .median()
        )
        unit = factor.map(lambda f: KAGGLE_UNITS.get(float(f"{f:.3g}"), f"other: kWh x {f:,.4g}"))
        units = (
            unit.groupby(level="meter").value_counts().unstack(level="meter", fill_value=0)[list(METER_TYPES.values())]
        ).rename_axis(index="unit in the competition data", columns=None)

        flags = recording_errors(readings)
        dropped = pd.concat(
            [readings["meter"].value_counts().rename("hours_with_a_reading"), flags.groupby(readings["meter"]).sum()],
            axis=1,
        ).loc[list(METER_TYPES.values())]
        dropped["dropped"] = flags.any(axis=1).groupby(readings["meter"]).sum()
        dropped = dropped.rename_axis("meter")

        zero_share = (
            (df[self.target] == 0)
            .groupby([df["timestamp"].dt.month, df["meter"]], observed=True)
            .mean()
            .unstack()
            .round(3)
        ).rename_axis("month")
        return [
            Decision(
                "Weather shifted from UTC to the sites' local time",
                "The weather files are in UTC and the meter readings in local time (BDG2 paper, p. 8). With the 1st "
                "place solution's offsets the mean day peaks at 14:00-16:00 local time at every site.",
                hours,
            ),
            Decision(
                "Readings taken in kWh from BDG2",
                "The competition kept each site's own unit; BDG2's raw files hold the same readings converted to kWh "
                "(paper, Tables 4 and 5). Meters per meter type by the factor between the two, named by the unit it "
                "implies; the ratio is the same within 0.1% for 99.9% of a meter's hours.",
                units,
            ),
            Decision(
                "Hours a meter did not record dropped",
                "Hours with a reading per meter type and the hours each rule flags (a row can match several rules): "
                "site 0's 2016 gap, electricity at 0, a cooling or heating plant at 0 for 48 hours or more in its "
                "operating months, a reading repeated for a week or more, and building 1099's steam unit error.",
                dropped,
            ),
            Decision(
                "Zeros of the thermal meters outside their season kept",
                "Chilled-water zeros peak in winter and steam and hot-water zeros in summer: a plant switched off for "
                "the season, which a model can learn. Share of shipped rows with a reading of 0, by month and meter "
                "type.",
                zero_share,
            ),
        ]
