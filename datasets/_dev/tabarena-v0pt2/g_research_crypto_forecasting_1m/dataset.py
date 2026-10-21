"""Curated dataset definition for `g_research_crypto_forecasting_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, Temporal, TemporalSplits

LAGS = (60, 300, 900)
"""The look-back windows (minutes) of the 3rd-place solution's features."""

FFILL_LIMIT = 100
"""A missing minute takes the asset's last Close for at most this many minutes (as in the 3rd-place solution)."""


def history_features(df: pd.DataFrame) -> pd.DataFrame:
    """The features of the 3rd-place solution for every row, from the Close prices up to and including its minute.

    The Close prices go on the full minute grid (one column per asset); a missing minute takes the asset's last Close
    for at most :data:`FFILL_LIMIT` minutes. For each look-back window in :data:`LAGS`: the log of Close over its
    trailing mean (the window ends at the row's minute) and the log return over the window, the mean of each over the
    assets that have a value at that minute (`market_*`), and the asset's value minus that mean (`*_minus_market`).
    Every value uses only minutes up to the row's own, so it is known when the prediction is made. `shift` checks
    only the window's end point, so a log return can span a gap longer than :data:`FFILL_LIMIT` minutes (as in the
    solution's code).
    """
    minute = ((df["timestamp"] - df["timestamp"].min()) // 60).to_numpy()
    assets = np.sort(df["Asset_ID"].unique())
    column = np.searchsorted(assets, df["Asset_ID"].to_numpy())
    grid = np.full((int(minute.max()) + 1, len(assets)), np.nan)
    grid[minute, column] = df["Close"].to_numpy()
    close = pd.DataFrame(grid).ffill(limit=FFILL_LIMIT)

    own = {}
    for lag in LAGS:
        own[f"log_close_to_mean_{lag}"] = np.log(close / close.rolling(lag).mean()).to_numpy()
        own[f"log_return_{lag}"] = np.log(close / close.shift(lag)).to_numpy()
    features = {}
    for name, wide in own.items():
        present = ~np.isnan(wide)
        n_present = present.sum(axis=1)
        market = np.where(present, wide, 0.0).sum(axis=1) / np.maximum(n_present, 1)
        market[n_present == 0] = np.nan
        features[name] = wide[minute, column]
        features[f"market_{name}"] = market[minute]
        features[f"{name}_minus_market"] = (wide - market[:, None])[minute, column]
    return pd.DataFrame(features, index=df.index)


class GResearchCryptoForecasting1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("How will a cryptocurrency's price move over the next 15 minutes, compared with the market?"),
        use_case=(
            "At the close of each minute, a trading firm forecasts each coin's return over the next 15 minutes "
            "relative to the market, to decide its positions (the G-Research competition)."
        ),
        row="One coin at one minute: 14 cryptocurrencies, January 2018 to September 2021.",
        predicted=(
            "The coin's return from one to 16 minutes ahead, minus the part that follows the market's return (a "
            "weighted mean of the 14 coins); values sit close to zero."
        ),
        known=(
            "The coin and the minute, the minute's trading summary (open, high, low and close prices, volume, average"
            " price, number of trades) and the price trends of the past hour, 5 hours and 15 hours, for the coin and "
            "for the market."
        ),
        split=(
            "Each test window is 91 days at the end of the period, newest first; training is a random million earlier"
            " coin-minute rows, with a one-day gap."
        ),
        changes=(
            "We add the price-trend features of the third-place solution, as the minute itself carries no signal, and"
            " drop the minutes without a target."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is known at the minute and the target covers the next 15 minutes, as in "
            "trading. The signal is tiny: one LightGBM configuration reaches R² +0.0006, +0.0013 and +0.0004 in the "
            "three windows, none outside the day-to-day noise, while its daily correlation with the target is "
            "positive on 70-74 of 91 days. The declared metric is Pearson correlation, for the competition's weighted correlation."
        ),
    )

    # Dataset
    unique_name = "g_research_crypto_forecasting_1m"
    version_of = "g_research_crypto_forecasting"
    version_comment = """
        We sample per test window (v2 split protocol): each window keeps at most 500k of its rows, and its train side is a random 1M of all earlier rows, drawn in one random order for all windows; the frame keeps only the rows a split uses. The full frame has 23,486,468 rows (14 assets, one row per minute, 2018-01-01 to 2021-09-20). We follow TabReD and sample the train data at random, so the train sides cover the whole history.
    """
    year = "2021"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/g-research-crypto-forecasting"
    license = "Kaggle Competition Rules (data access and use: competition use only)"
    download_description = """
        We download two files of the Kaggle competition (accept its rules on Kaggle first). The files were last updated on 2022-01-26; train.csv has 24,236,806 rows.

        kaggle competitions download -c g-research-crypto-forecasting -f train.csv -p local-data-warehouse/g_research_crypto_forecasting
        kaggle competitions download -c g-research-crypto-forecasting -f asset_details.csv -p local-data-warehouse/g_research_crypto_forecasting
        cd local-data-warehouse/g_research_crypto_forecasting && unzip train.csv.zip && rm train.csv.zip
    """
    bibtex = r"""
        @misc{GResearchCryptoForecasting2021,
          author = {Alessandro Ticchi and Andrew Scherer and Carla McIntyre and Carlos Stein N Brito and Derek Snow and Develra and dstern and James Colless and Kieran Garvey and Maggie and Maria Perez Ortiz and Ryan Lynch and Sohier Dane},
          title = {G-Research Crypto Forecasting},
          year = {2021},
          howpublished = {\url{https://kaggle.com/competitions/g-research-crypto-forecasting}},
          note = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with train.csv (one row per asset and minute, 14 cryptocurrencies, 2018-01-01 to 2021-09-21) and asset_details.csv of the Kaggle competition.

        - Prediction point: at the close of minute t we predict an asset's `Target`, its return from minute t+1 to t+16 minus its beta times the weighted mean return of the 14 assets (the organisers' tutorial notebook). Known then: every one-minute bar of the 14 assets up to and including minute t.
        - Scope: the target is the asset's own residualised forward return, and its signal is the asset's trailing return relative to the 14-asset mean. The bar alone, the asset's own lags alone and the market means alone carry none (LightGBM on each set, three test windows). The relative returns correlate 0.80-0.83 (median over the 14 assets) with sums of the asset's own lagged `Target`, so by the curation guidelines (SEL-10, TP-10) this is time-series forecasting. The record carries an imported, unattributed note "Forecasting-as-tabular task" (sheet import, 2026-06-23) that predates TP-10; no curator decision accepts the case. The scope call stays with the curator.
        - History features (`history_features`): a row's own bar carries no signal for the next 15 minutes (a LightGBM prediction from the bar correlates -0.002, 0.005 and 0.010 with the target in the three test windows), so we add the features of the public notebook "Training 3rd place solution" (sugghi) cited in the record. For 60, 300 and 900 minutes: the log of Close over its trailing mean and the log return, their mean over the assets (`market_*`) and the asset's difference from it (`*_minus_market`). With them the correlation is 0.026, 0.059 and 0.049. The features come from this one notebook; that it is the 3rd-place team's code is not verified, and no other solution was compared.
        - We compute the features on the full minute grid before dropping rows. A missing minute takes the asset's last Close for at most 100 minutes (as in the notebook). A trailing mean reaching into a longer gap or before the asset's first minute is missing; a log return checks only its end point, so 193, 1,804 and 9,370 values (60, 300 and 900 minutes) span a longer gap, as in the notebook.
        - We drop the 750,338 rows (3.1%) without a target: Close(t+1) or Close(t+16) is missing (37% lack only Close(t+1)), and the competition does not score them. Their bars still enter the history features.
        - We replace `Asset_ID` by the asset's name from asset_details.csv (`Asset_Name`, category); its `Weight`, the asset's weight in the metric, is not a feature.
        - `VWAP` is a positive price and `Volume` a traded amount: we set the infinite and negative VWAP values (13 rows of the frame, 15 of the raw file, all Maker, June 2020) and the negative Volume values (2 rows of the frame, 3 raw, Maker) to missing.
        - We convert `timestamp` (Unix seconds) to a datetime.
        - Anomaly: 16 bars of the frame (18 raw) have a `Low` below half of their open and close and 3 raw bars a `High` above twice, and 266 targets exceed 0.2 in absolute value (mostly Bitcoin Cash around its November 2018 fork). We keep them as unusual but real. No (timestamp, asset) pair repeats.
        - Temporal, not grouped by asset: the competition forecasts the same 14 assets on later data; a split by asset would only test a shift between 14 assets (decision table).
        - History: each train side is a random 1M of all earlier rows back to 2018, TabReD's convention; no use-case reason is recorded for the whole history against a recent one. The test windows from 2020-12-22 to 2021-06-21 fall in the 2021 high-volatility regime (median absolute 900-minute return 0.029-0.036, against 0.013-0.022 in every quarter of 2019-2020).
        - Metric: the competition scored a weighted Pearson correlation over all test rows, each row weighted by its asset's `Weight` in asset_details.csv (Bitcoin 6.78, Ethereum 5.89, Cardano 4.41, Binance Coin 4.30, Dogecoin 3.56, Bitcoin Cash and Litecoin 2.40, Ethereum Classic and Stellar 2.08, TRON 1.79, Monero 1.61, EOS.IO 1.39, IOTA and Maker 1.10). No listed metric weighs rows, so we declare pooled `pearsonr` (TP-6): over seven predictions per window (ridge with two penalties, four LightGBM sizes, one raw feature), it ranks them as the weighted correlation does in all three windows (Kendall tau 1.0), within 0.008 of it. RMSE, declared before, ranks mostly how close predictions stay to the mean.
        - Note: the task probes flag no_signal, drift_baseline and unstable (untuned models). LightGBM (learning rate 0.05, 31 leaves, at least 200 rows per leaf) early-stopped on the newest 10% of each train side reaches R^2 +0.0006, +0.0013 and +0.0004 in one refit (+0.0007, +0.0012 and -0.0003 in an earlier run, so the sign of the third window is unstable); no window's 95% day-block interval excludes 0. Its daily correlation with the target is positive on 71, 70 and 74 of 91 days. The signal is small and real under correlation and not separable from the noise under RMSE; drift_baseline comes from a target centred on zero.
    """

    # Task
    target = "Target"
    problem_type = "regression"
    metric = "pearsonr"  # stands for the competition's asset-weighted correlation (curation comments)

    # Splits
    temporal = Temporal(
        on="timestamp",
        splits=TemporalSplits(window=91, unit="days", n_windows=3, gap=1),
    )
    splits_comment = """
        The competition scored the submitted models on the 3 months of live data after its submission deadline. We use each of the last 3 windows of 91 days (newest first) as a test window and all earlier data as train data, with a 1-day gap: a row's target needs the prices of the next 16 minutes, so every training label is known when the window starts. Each window keeps at most 500k of its rows; each train side is a random 1M of all earlier rows (one random order for all windows). Rows of one asset a few minutes apart share most of their 15-minute target window (per asset, targets 5 minutes apart correlate with a median of 0.57, range 0.25-0.66), so validation inside a train side has to split by time blocks, not rows: LightGBM early-stopped on random rows of the train side stops after 220-528 rounds and scores test R^2 -0.0049, -0.0043 and -0.0090, against +0.0006, +0.0013 and +0.0004 when it stops on the newest 10%.
    """
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "train": pd.read_csv(raw_dir / "train.csv"),
            "assets": pd.read_csv(raw_dir / "asset_details.csv"),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, assets = raw["train"], raw["assets"]
        # The history features come from every bar, before the rows without a target are dropped.
        df = pd.concat([df, history_features(df)], axis=1)
        df = df[df["Target"].notna()]
        # VWAP is a positive price: its infinite and negative values (Maker, June 2020) become missing.
        vwap = df["VWAP"].to_numpy()
        df.loc[~np.isfinite(vwap) | (vwap <= 0), "VWAP"] = np.nan
        # A traded volume cannot be negative (Maker): missing.
        df.loc[df["Volume"] < 0, "Volume"] = np.nan
        # The asset's name instead of its id (same position).
        df["Asset_ID"] = df["Asset_ID"].map(assets.set_index("Asset_ID")["Asset_Name"])
        df = df.rename(columns={"Asset_ID": "Asset_Name"})
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        del df
        return FeatureTypes(categorical=["Asset_Name"], datetime=["timestamp"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        train, assets = raw["train"], raw["assets"]
        names = assets.set_index("Asset_ID")["Asset_Name"]
        coverage = train.groupby("Asset_ID").agg(
            first_minute=("timestamp", "min"),
            rows=("timestamp", "size"),
            share_without_target=("Target", lambda s: round(float(s.isna().mean()), 4)),
        )
        coverage["first_minute"] = pd.to_datetime(coverage["first_minute"], unit="s")
        coverage.index = coverage.index.map(names).rename("asset")
        numeric = [c for c in df.columns if c not in ("timestamp", "Asset_Name", self.target)]
        correlation = pd.DataFrame(
            {
                "pearson_r_with_target": df[numeric].corrwith(df[self.target]),
                "spearman_r_with_target": df[numeric].corrwith(df[self.target], method="spearman"),
            }
        ).round(4)
        correlation.index.name = "feature"
        return [
            Decision(
                "Temporal split over the same 14 assets, not grouped by asset",
                "The competition forecasts the 14 assets on later data. The assets enter the data at different times, "
                "and a row has no target when the asset's Close one or 16 minutes later is missing (rows of the raw file).",
                coverage,
            ),
            Decision(
                "History features from the 3rd-place solution carry the signal",
                "The bar of one minute says little about the next 15 minutes; the asset's recent returns relative to "
                "the market do (in ranks most clearly). Correlation of each feature with the target on the shipped frame.",
                correlation,
            ),
        ]
