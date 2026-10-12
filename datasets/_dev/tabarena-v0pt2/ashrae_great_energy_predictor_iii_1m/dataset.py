"""Curated dataset definition for `ashrae_great_energy_predictor_iii_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Temporal, TemporalSplits, drop_columns

METER_TYPES = {0: "electricity", 1: "chilledwater", 2: "steam", 3: "hotwater"}
"""The meter codes of train.csv, as the competition's data page names them."""

KBTU_TO_KWH = 0.2931
"""The host's factor for site 0's electricity readings, which are in kBTU (Kaggle discussion 119261)."""

SITE_0_RECORDING_GAP_END = "2016-05-21"
"""Site 0's electricity meters read 0 until 2016-05-20 (344,577 of the 348,560 hours before this date)."""

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


class AshraeGreatEnergyPredictorIii1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "ashrae_great_energy_predictor_iii_1m"
    version_of = "ashrae_great_energy_predictor_iii"
    version_comment = """
        The cleaned frame has 40.1M hourly readings, so the dataset ships only as this `_1m` version. We sample per
        test window (v2 split protocol): each window keeps at most 500k of its rows, and its train side is a random 1M
        of all earlier rows, drawn in one random order for all windows; the frame keeps only the rows a split uses. As
        in TabReD, the train side is a random sample of the whole history rather than its newest part, so every
        window trains on all seasons seen so far.
    """
    year = "2019"
    domain = "environmental science & climate"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/ashrae-energy-prediction"
    license = (
        "Kaggle Competition Rules (7A: use for any purpose, commercial or non-commercial; 7B: no redistribution to "
        "anyone not participating in the competition); the 2017 readings from BDG2: MIT License at the pinned commit "
        "(2020), CC BY 4.0 on its Zenodo release v1.0 (doi 10.5281/zenodo.3887306), and a LICENSE headed "
        "'Attribution-ShareAlike 4.0 Unported' in the repository since 2023-10-14"
    )
    download_description = """
        We download four files of the Kaggle competition (train.csv holds 2016) and the competition's 2017 readings,
        which its technical team released in the Building Data Genome Project 2 (BDG2) repository (a Git LFS file,
        pinned to the commit that added it; sha256 67e6d3e82cc737d28389845fc5e526711705fc264fd178a7a0b6f8f3d8d3c82e).
        The competition's 2018 readings (its private test year) are not public.

        mkdir -p local-data-warehouse/ashrae_great_energy_predictor_iii && cd local-data-warehouse/ashrae_great_energy_predictor_iii
        for f in train.csv weather_train.csv weather_test.csv building_metadata.csv; do kaggle competitions download -c ashrae-energy-prediction -f $f -p .; done
        unzip train.csv.zip && unzip weather_train.csv.zip && unzip weather_test.csv.zip && rm train.csv.zip weather_train.csv.zip weather_test.csv.zip
        mkdir -p bdg2 && wget -O bdg2/kaggle.csv https://media.githubusercontent.com/media/buds-lab/building-data-genome-project-2/9581aafed95b28e3d5ac39929c15fbc0ba36af5b/data/meters/kaggle/kaggle.csv
    """
    bibtex = r"""
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
    """
    curation_comments = """
        We start with train.csv (2016), building_metadata.csv, weather_train.csv and weather_test.csv of the Kaggle competition and the competition's 2017 readings (data/meters/kaggle/kaggle.csv of the BDG2 repository).

        - Prediction point: after a cutoff, for every later hour of a meter we already know, the model gives the reading the building would have had, from the building's metadata, the meter type, the local time and the site's weather in that hour, as in the competition. No reading after the cutoff is an input, so this is a regression on exogenous inputs with a temporal split, not forecasting.
        - We stack 2016 and 2017, the competition's public test year, which its technical team released in BDG2 ("matches seamlessly with the training data", BDG2 paper, p. 8); 2018 is not public. The 2017 file keeps the competition's units: site 0's median electricity reading is 193.8 in the last week of 2016 and 202.5 in the first week of 2017.
        - We drop the hours of 2017 without a reading (gaps the competition did not score).
        - Site 0's electricity readings are in kBTU. We multiply them by 0.2931, the host's factor (discussion 119261).
        - The weather timestamps are UTC and the meter timestamps local time (BDG2 paper, p. 8). We shift each site's weather by the 1st place solution's offsets (standard time) and join it on site and hour, so the mean day peaks at 14:00-16:00 at every site (decision table). The meters of 8 sites follow daylight saving time, but a join with it changed LightGBM's RMSE by -0.007 to +0.005 per window, no consistent gain, so we keep the standard offsets.
        - We drop site 0's electricity before 2016-05-21, a recording gap (its meters read 0 in 344,577 of these 348,560 hours), and every other electricity reading of 0: a whole-building electricity meter that reads 0 has not recorded (BDG2's cleaned data removes these readings too, p. 7).
        - Zero readings of the chilled-water, steam and hot-water meters stay: they follow the seasons (decision table), so a model can learn when a plant is off. BDG2's cleaned data removes zero runs of more than 24 hours; we keep them because most are seasonal.
        - Anomaly: other recording errors stay as the competition shipped them ("real data with measurement error", data page), such as building 1099's steam meter at about 1,000 times its usual level in March-June 2016. BDG2 fixed such unit errors, which were "left as-is in the Kaggle data set" (p. 8).
        - The target is log1p of the reading (kWh, or kWh equivalent for the thermal meters), so RMSE on it is the competition's metric, RMSLE.
        - The meter codes get the data page's names. building_id and site_id stay as categories: the test hours belong to meters with earlier readings in train, as in the competition.
        - precip_depth_1_hr = -1 stays: in the NOAA ISD-Lite data the weather comes from, -1 codes a trace of precipitation (ISD-Lite format note, field 11).
    """

    # Task
    target = "log1p_meter_reading"
    problem_type = "regression"

    # Splits: three 4-month windows tile 2017, the competition's public test year.
    temporal = Temporal(
        on="timestamp",
        splits=TemporalSplits(window=4, unit="months", cutoffs=("2017-01-01", "2017-05-01", "2017-09-01")),
    )
    splits_comment = """
        Three test windows of 4 months tile 2017, the competition's first test year: September-December, May-August and January-April 2017, newest first; train is all earlier hours. The oldest window is the competition's own setting: train on the year 2016 and predict the first months of 2017. 2016 holds 50.07% of the hours (8,784 of 17,544) but 49.12% of the rows, as it has more gaps and drops (site 0's recording gap); we keep the window because it is the competition's setting. A window is the horizon: the competition asked for the two years after its training year, and 4 months is the longest window that gives three windows inside 2017. Each test window keeps at most 500k of its rows and each train side is a random 1M of all earlier rows (one random order for all windows); the frame keeps only the rows a split uses.
    """
    subsample_to_budget = True

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
        weather = pd.concat(
            [pd.read_csv(raw_dir / "weather_train.csv"), pd.read_csv(raw_dir / "weather_test.csv")],
            ignore_index=True,
        )
        buildings = pd.read_csv(raw_dir / "building_metadata.csv")
        return {"readings": readings, "weather": weather, "buildings": buildings}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        readings, weather, buildings = raw["readings"], raw["weather"], raw["buildings"]
        # 2017 hours without a reading (gaps the competition did not score)
        df = readings[readings["meter_reading"].notna()]
        df = df.merge(buildings, on="building_id", how="left", validate="many_to_one")
        df["timestamp"] = df["timestamp"].astype("datetime64[ns]")

        # Site 0's electricity is in kBTU: convert it to kWh like the other sites (the host's factor).
        site_0_electricity = (df["site_id"] == 0) & (df["meter"] == 0)
        df.loc[site_0_electricity, "meter_reading"] = df.loc[site_0_electricity, "meter_reading"] * KBTU_TO_KWH
        # Site 0's 2016 recording gap and electricity readings of 0 (not recorded).
        recording_gap = site_0_electricity & (df["timestamp"] < SITE_0_RECORDING_GAP_END)
        electricity_zero = (df["meter"] == 0) & (df["meter_reading"] == 0)
        df = df[~(recording_gap | electricity_zero)]

        # The weather is in UTC: move it to the sites' local standard time, then join it on site and hour.
        weather = weather.assign(
            timestamp=pd.to_datetime(weather["timestamp"], format="%Y-%m-%d %H:%M:%S").astype("datetime64[ns]")
            + pd.to_timedelta(weather["site_id"].map(SITE_UTC_OFFSET_HOURS), unit="h")
        )
        df = df.merge(weather, on=["site_id", "timestamp"], how="left", validate="many_to_one")

        df["meter"] = df["meter"].map(METER_TYPES)
        df["log1p_meter_reading"] = np.log1p(df["meter_reading"])
        return drop_columns(df, ["meter_reading"])

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

        readings = raw["readings"].merge(raw["buildings"][["building_id", "site_id"]], on="building_id", how="left")
        labelled = readings["meter_reading"].notna()
        site_0_gap = (
            (readings["site_id"] == 0) & (readings["meter"] == 0) & (readings["timestamp"] < SITE_0_RECORDING_GAP_END)
        )
        zero = readings["meter_reading"] == 0
        dropped = (
            pd.DataFrame(
                {
                    "hours_with_a_reading": labelled.groupby(readings["meter"]).sum(),
                    "zero_share": zero[labelled].groupby(readings["meter"][labelled]).mean().round(4),
                    "dropped_site_0_gap": (labelled & site_0_gap).groupby(readings["meter"]).sum(),
                    "dropped_zero": (labelled & zero & ~site_0_gap & (readings["meter"] == 0))
                    .groupby(readings["meter"])
                    .sum(),
                }
            )
            .rename(index=METER_TYPES)
            .rename_axis("meter")
        )

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
                "Electricity zeros and site 0's 2016 recording gap dropped",
                "A whole-building electricity meter that reads 0 has not recorded (BDG2's cleaned data drops these "
                "readings). Site 0's electricity reads 0 until 2016-05-20. Rows of the raw files per meter type.",
                dropped,
            ),
            Decision(
                "Zeros of the thermal meters kept",
                "Chilled-water zeros peak in winter and steam and hot-water zeros in summer: a plant that is off, which "
                "a model can learn. Share of shipped rows with a reading of 0, by month and meter type.",
                zero_share,
            ),
        ]
