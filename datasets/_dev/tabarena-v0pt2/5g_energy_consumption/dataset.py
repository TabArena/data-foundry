"""Curated dataset definition for `5g_energy_consumption` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class Dataset5gEnergyConsumption(AbstractCuratedDataset):
    # Dataset
    unique_name = "5g_energy_consumption"
    year = "2023"
    domain = "technology & internet"
    source = "HuggingFace"
    source_url = "https://huggingface.co/datasets/netop/5G-Network-Energy-Consumption"
    license = "MIT"
    download_description = r"""
        We use the dataset version uploaded by a top solution from the Zindi challenge.

        mkdir -p local-data-warehouse/5g_energy_consumption/ \
        && wget https://github.com/ITU-AI-ML-in-5G-Challenge/5G-Energy-Consumption-Modelling-Solution-Team-Farzi-Data-Scientists/raw/refs/heads/main/ITU-5G-energy-Consumption-Dataset.zip \
        && unzip ITU-5G-energy-Consumption-Dataset.zip -d local-data-warehouse/5g_energy_consumption/ \
        && rm ITU-5G-energy-Consumption-Dataset.zip
    """
    bibtex = r"""
        @misc{huawei_netop_5g_energy_consumption,
          author       = {{HUAWEI Netop Team}},
          title        = {5G Network Energy Consumption Dataset},
          year         = {n.d.},
          howpublished = {\url{https://huggingface.co/datasets/netop/5G-Network-Energy-Consumption}},
          note         = {Dataset hosted on Hugging Face, accessed 2026-04-15}
        }
    """
    curation_comments = """
        - Note: The dataset was used in a Zindi challenge, but also uploaded to Huggingface under a MIT license by the company (Huawei).
        - The corresponding ITU/Zindi challenge explicitly emphasizes generalization to unseen base station products/configurations. We therefore split by base_station (BS).
        - With this setup, the task is development of predictive models for network optimization where models need to generalize to new unseen base station configurations and estimate their energy consumption under similar conditions (during the same time period).
        - For preprocessing, we orient on a top solution from the Zindi challenge: https://github.com/ITU-AI-ML-in-5G-Challenge/5G-Energy-Consumption-Modelling-Solution-Team-Farzi-Data-Scientists/tree/main.
        - Note that the competition also used mostly samples from the known BS as the test set, but weighted unknown base stations higher in evaluation.
        - The data itself is time-series. However, because we predict entirely unseen base stations in a per-sample fashion, the row-wise dependencies resulting from the temporal components cannot be used to improve performance unless the task is treated as transductive learning.
        - Following the Zindi solution, we merge the three given tables and use the Cell0 information only from the cell level table. In addition, we merge the Cell1 information since it contains information as well which might be useful in a grouped split setting.
        - Following the Zindi solution, we derive calendar features (`day`, `hour`, `weekday`) and drop the absolute timestamp.
        - We drop constant columns.
    """

    # Task
    target = "Energy"
    problem_type = "regression"
    metric = "mape"
    group_on = "BS"
    group_labels = "per_sample"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df_train = pd.read_csv(raw_dir / "ECdata.csv", parse_dates=["Time"])
        # df_test = pd.read_csv("/kaggle/input/ecm-itu-zindi-kp-data/imgs_202307101549519358.csv",parse_dates=['Time'])
        df_cell = pd.read_csv(raw_dir / "CLdata.csv", parse_dates=["Time"])
        df_bs = pd.read_csv(raw_dir / "BSinfo.csv")
        return {"df_train": df_train, "df_cell": df_cell, "df_bs": df_bs}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df_train, df_cell, df_bs = raw["df_train"], raw["df_cell"], raw["df_bs"]
        df_features = df_cell.merge(df_bs, on=["BS", "CellName"], how="outer")
        df_features = df_features[df_features["CellName"] == "Cell0"].reset_index(drop=True)
        df_total = df_train.merge(df_features, on=["BS", "Time"], how="left")
        cell1 = df_cell[df_cell["CellName"] == "Cell1"].rename(
            columns={col: col + "_Cell1" for col in df_cell.columns if col not in ["BS", "Time"]}
        )
        df = df_total.merge(cell1, on=["BS", "Time"], how="left")
        df["day"] = df["Time"].dt.day
        df["weekday_number"] = df["Time"].dt.weekday
        df["hour"] = df["Time"].dt.hour
        df = df.drop(columns=["Time"])
        # Drop constant columns that are not useful for modeling
        df = df.drop(columns=["CellName", "ESMode4", "CellName_Cell1", "ESMode4_Cell1", "ESMode5_Cell1"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "BS",
                "RUType",
                "Mode",
            ],
        )
