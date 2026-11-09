"""Curated dataset definition for `g_research_crypto_forecasting_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    ScoringColumn,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
)

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


def all_bars(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """The bars of train.csv followed by those of supplemental_train.csv, which continues it from 21 September 2021.

    A (timestamp, Asset_ID) pair that both files hold keeps the row of train.csv (the two share none in the release
    of 2022-01-26).
    """
    df = pd.concat([raw["train"], raw["supplemental"]], ignore_index=True)
    return df.drop_duplicates(["timestamp", "Asset_ID"]).reset_index(drop=True)


class GResearchCryptoForecasting1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("How will a cryptocurrency's price move over the next 15 minutes, compared with the market?"),
        use_case=(
            "At the close of each minute, a trading firm forecasts each coin's return over the next 15 minutes "
            "relative to the market, to decide its positions (the G-Research competition)."
        ),
        row="One coin at one minute: 14 cryptocurrencies, January 2018 to January 2022.",
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
            "Three test windows of 91 days: the newest (25 October 2021 to 23 January 2022), the bull run of early "
            "2021 and the quiet market of 2020 with its crash; training is all earlier history with a 15-minute gap, "
            "from which a benchmark draws about a million coin-minute rows as whole minutes (all coins of a minute) "
            "from the newest year."
        ),
        changes=(
            "We add the price-trend features of the third-place solution, as the minute itself carries no signal, and"
            " drop the minutes without a target."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is known at the minute and the target covers the next 15 minutes, as in "
            "trading. On the earlier windows to 20 September 2021, a 12-seed LightGBM ensemble scored +0.039, +0.033 "
            "and +0.021 by the weighted Pearson correlation and led the coin's mean in all three, clearly in two; it "
            "is to be measured again on the windows tested now."
        ),
    )

    # Dataset
    unique_name = "g_research_crypto_forecasting_1m"
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/g-research-crypto-forecasting",
            license="Kaggle Competition Rules (data access and use: competition use only)",
            year="2021",
            bibtex=r"""
                @misc{GResearchCryptoForecasting2021,
                  author = {Alessandro Ticchi and Andrew Scherer and Carla McIntyre and Carlos Stein N Brito and Derek Snow and Develra and dstern and James Colless and Kieran Garvey and Maggie and Maria Perez Ortiz and Ryan Lynch and Sohier Dane},
                  title = {G-Research Crypto Forecasting},
                  year = {2021},
                  howpublished = {\url{https://kaggle.com/competitions/g-research-crypto-forecasting}},
                  note = {Kaggle competition}
                }
            """,
        ),
    )
    download_description = """
        We download three files of the Kaggle competition (accept its rules on Kaggle first). The files were last updated on 2022-01-26; train.csv has 24,236,806 rows and supplemental_train.csv 2,518,278.

        kaggle competitions download -c g-research-crypto-forecasting -f train.csv -p local-data-warehouse/g_research_crypto_forecasting
        kaggle competitions download -c g-research-crypto-forecasting -f supplemental_train.csv -p local-data-warehouse/g_research_crypto_forecasting
        kaggle competitions download -c g-research-crypto-forecasting -f asset_details.csv -p local-data-warehouse/g_research_crypto_forecasting
        cd local-data-warehouse/g_research_crypto_forecasting && unzip train.csv.zip && unzip supplemental_train.csv.zip && rm train.csv.zip supplemental_train.csv.zip
    """
    curation_comments = """
        We start with train.csv (one row per asset and minute, 14 cryptocurrencies, 2018-01-01 to 2021-09-21), supplemental_train.csv (the same, 2021-09-21 00:01 to 2022-01-24) and asset_details.csv of the Kaggle competition.

        - The newer months (Lennart, 2026-11-11; Review issue 10): supplemental_train.csv continues train.csv minute by minute from 21 September 2021 00:01 to 24 January 2022 00:00 (2,518,278 rows, the same 14 assets and columns, no (timestamp, asset) pair in both; Bitcoin closes at 43,002.5 on the last minute of train.csv and at 42,947.1 on the first of the file). We append it: these are the release's newest months, the period closest to the competition's own scoring of the frozen models (2 February to 3 May 2022), and the newest test window stands for deployment. Together the files hold 26,755,084 rows. The history features are built on both files at once, so their look-back windows run across the seam. The release's other files are left out: example_test.csv and example_sample_submission.csv show the format of the live API (a few rows, no target), and gresearch_crypto/ is the API's code.
        - Prediction point: at the close of minute t we predict an asset's `Target`, its return from minute t+1 to t+16 minus its beta times the weighted mean return of the 14 assets (the organisers' tutorial notebook). Known then: every one-minute bar of the 14 assets up to and including minute t.
        - Scope: the target is the asset's own residualised forward return, and its signal is the asset's trailing return relative to the 14-asset mean. The bar alone, the asset's own lags alone and the market means alone carry none (LightGBM on each set, three test windows). The curator keeps it as a forecasting-like panel under the amended TP-10 (Lennart, 2026-10-22). Leg 1, measured by the declared metric: early-stopped LightGBM scores weighted Pearson +0.040, +0.052 and +0.045 in the three windows (95% day-block intervals [+0.023, +0.063], [+0.036, +0.070], [+0.027, +0.063]), and its lead over the asset's mean (the naive forecast: -0.002, +0.007, +0.008) excludes 0 in every window (random-row train sides, 1-day gap; superseded 2026-11-06: on the splits shipped then, train sides of 1M whole minutes from all history and a 15-minute gap, the 12-seed ensemble, which averages the 12 models' predictions and leaves out `timestamp`, scores +0.0388 [+0.0205, +0.0623], +0.0333 [+0.0103, +0.0585] and +0.0206 [-0.0050, +0.0496] (a single model +0.0368, +0.0294 and +0.0199), its lead over the coin's mean +0.0384 [+0.0182, +0.0631], +0.0418 [+0.0138, +0.0699] and +0.0231 [-0.0060, +0.0537], +0.034 pooled over the three windows (SE about 0.008), positive on 75, 75 and 77 of 91 days: the oldest window's lead no longer excludes 0). Leg 1 still holds (CC 2026-11-08, Lennart; Review issue 8): the model is ahead of the coin's mean in every window by its point estimate, and the interval is read pooled, as for ashrae_great_energy_predictor_iii and rain_in_australia. These figures come from the windows that ended on 20 September 2021, before the newer months were added (2026-11-11); they are to be measured again (the 12-seed ensemble against the coin's mean, day-block intervals) on the windows chosen in Review issue 9 on 2026-11-11, from 25 October 2021, 22 December 2020 and 28 February 2020, which has not been run yet. Leg 2: the top three solutions are LightGBM on point-in-time features (G-Research's wrap-up), and no feature is a lag of the `Target` column; the relative returns are built from Close and correlate 0.80-0.83 (median over the 14 assets) with sums of the asset's lagged `Target`.
        - History features (`history_features`): a row's own bar carries no signal for the next 15 minutes (a LightGBM prediction from the bar correlates -0.002, 0.005 and 0.010 with the target in the three test windows of train.csv, measured in October 2026), so we add the features of the 3rd-place solution: the public notebook "Training 3rd place solution" (sugghi), which Kaggle's write-up record for the 3rd place lists as sugghi's (sole author, team GABA); it uses Close only and trains from 12 January 2019. For 60, 300 and 900 minutes: the log of Close over its trailing mean and the log return, their mean over the assets (`market_*`) and the asset's difference from it (`*_minus_market`). With them the correlation is 0.026, 0.059 and 0.049.
        - The 18 features stay after a comparison with the other top solutions (CLEAN-19; Lennart, 2026-10-22): the 2nd place withholds its features (LightGBM on squared loss) and the 1st place has no write-up; lower places add a 15-minute look-back, volume and volatility, technical indicators, the hour, and other coins' returns. Added to the 18 (LightGBM, mean of 2 seeds, change in weighted Pearson in the three windows; random-row train sides, 1-day gap, 2026-10-22): a 15-minute look-back -0.001, -0.001, -0.002; volume and volatility +0.003, +0.004, -0.005; other coins' 15- and 60-minute returns -0.005, -0.013, -0.007; bar shape and time -0.007, -0.007, -0.004. None helps in all three windows.
        - We compute the features on the full minute grid before dropping rows. A missing minute takes the asset's last Close for at most 100 minutes (as in the notebook). A trailing mean reaching into a longer gap or before the asset's first minute is missing; a log return checks only its end point, so 193, 1,804 and 9,370 values (60, 300 and 900 minutes) span a longer gap, as in the notebook (all before the newer months, which add none).
        - We drop the 753,261 rows (2.8%) without a target, 750,338 of train.csv and 2,923 of supplemental_train.csv: Close(t+1) or Close(t+16) is missing (37% lack only Close(t+1)), and the competition does not score them. 308 of them have both closes and still no target in the file, 224 of these train.csv's last 16 minutes, whose Close(t+16) lay past its end; we do not recompute the host's target. Their bars still enter the history features.
        - We replace `Asset_ID` by the asset's name from asset_details.csv (`Asset_Name`, category); its `Weight` in asset_details.csv, the asset's weight in the metric, ships as a scoring column and is not a feature.
        - `VWAP` is a positive price and `Volume` a traded amount: we set the infinite and negative VWAP values (13 rows of the frame, 15 of the raw files, all Maker, June 2020) and the negative Volume values (2 rows of the frame, 3 raw, Maker) to missing; supplemental_train.csv has none of either.
        - We convert `timestamp` (Unix seconds) to a datetime.
        - Anomaly: 117 bars of the frame (119 raw) have a `Low` below half of their open and close and 3 raw bars a `High` above twice, and 271 targets exceed 0.2 in absolute value (mostly Bitcoin Cash around its November 2018 fork). In train.csv these are 16 bars of the frame (18 raw) and 266 targets, which we keep as unusual but real. The newer months add 101 of the low bars, 99 of them EOS.IO on 26-27 October 2021, where its Low sits near 1.09 against a price near 4.8 and its Close jumps between about 4.8 and 4.0 from minute to minute; EOS.IO holds 85 of the 126 targets above 0.1 in absolute value in the newest window, and these two days 3.7% of that window's weighted target variance. We keep them as the release gives them. No (timestamp, asset) pair repeats.
        - Temporal, not grouped by asset: the competition forecasts the same 14 assets on later data; a split by asset would only test a shift between 14 assets (decision table).
        - History: each train side is all earlier history back to 2018 (minus the 15-minute gap), and a benchmark sub-samples it to the 1M budget as whole minutes (every asset of a drawn minute kept, `sample_by="time"`), by default at random from the newest year before the window (`subsample_train`, issue #70); SPLIT-20 reason (Lennart, 2026-10-22): the target and the features are relative to the 14-asset market at each minute, and random rows left about 1.3 assets per minute. Measured at the 1M budget (weighted Pearson, mean of 3 seeds, windows 1, 2, 3; on 2026-10-22, on the test rows then shipped, drawn as random rows, with a 1-day gap): whole minutes over all history .041, .046, .045; random rows over all history .042, .045, .043; the newest 1M rows (50 days) .036, .045, .007; the newest year, now the default, is not among these runs. A recent cut swings by window and collapses in the third; the 2nd place found that longer history kept helping and trained on all of it. On the windows that ended on 20 September 2021, the two older test windows (2020-12-22 to 2021-06-21) fell in the 2021 high-volatility regime (median absolute 900-minute return 0.029-0.036, against 0.013-0.022 in every quarter of 2019-2020). With the newer months the test windows are the newest (25 October 2021 to 23 January 2022), the 2021 bull run (22 December 2020 to 22 March 2021) and the quiet market of 2020 with its crash (28 February to 28 May 2020), chosen by Lennart on 2026-11-11 (Review issue 9) in place of the three newest, of which the two older ones repeated the busy market of 2021.
        - Metric: the competition's weighted Pearson correlation, each row weighted by its asset's `Weight` (Bitcoin 6.78 ... IOTA and Maker 1.10). It replaces the pooled `pearsonr` declared before as its stand-in, which ranked seven predictions per window as the weighted correlation does (Kendall tau 1.0).
        - Training weight (MET-15, 2026-11-06): none. `Weight` is a function of `Asset_Name`, which the model sees, so MET-15 needs no sample weight: a weight that is a function of the features leaves the best squared-error prediction of each row unchanged. Fitting with it as the sample weight (and in the validation loss) moved the weighted Pearson by +0.0045, +0.0034 and +0.0001 in the three windows that ended on 20 September 2021 (mean of 12 seeds; better in 25 of 36 window-seed pairs; +0.0010 with a fixed 50 rounds instead of early stopping, every interval including 0), within the spread across windows (mean +0.0026, SD 0.0023, t about 1.96 on 2 df); only the newest window's interval excludes 0 (12-seed ensembles, +0.0050 [+0.0005, +0.0099], 95% day-block interval).
        - Note: the task probes flag no_signal, drift_baseline and unstable (untuned models, scored by R^2; by the declared weighted Pearson their LightGBM scores 0.028, the linear model 0.023 and the dummy 0, mean of the 3 splits that ended on 20 September 2021). LightGBM (learning rate 0.05, 31 leaves, at least 200 rows per leaf) early-stopped on the newest 10% of each train side reaches R^2 +0.0008, +0.0008 and -0.0023 on the splits shipped on 2026-11-06 (train sides of 1M whole minutes from all history; mean of 4 seeds; their ensemble +0.0010 [-0.0002, +0.0026], +0.0009 [+0.0001, +0.0017] and -0.0019 [-0.0046, +0.0011], 95% day-block intervals, only the middle window's excluding 0). Under the declared weighted Pearson the same signal is clear in the two newer windows and pooled over the three (Scope bullet); drift_baseline comes from a target centred on zero.
        - The row budget: each test window keeps at most 500k of its rows, drawn at random as whole minutes (every asset of a drawn minute kept), and each train side holds every earlier row (minus the 15-minute gap); the frame keeps every row a split uses. The 1M train budget is recorded, not applied: a benchmark sub-samples each train side to 1M rows before a fit with `subsample_train`, by default whole minutes drawn at random from the newest year before the window. The full frame has 26,001,823 rows (14 assets, one row per minute, 2018-01-01 to 2022-01-23 23:44; 23,486,468 of them from train.csv).
    """

    # Task
    accepted_check_warnings = {
        "task_metric_weight_without_sample_weight": (
            "The asset's Weight is a function of Asset_Name, a feature, so MET-15 needs no sample weight "
            "(2026-11-06). Training with it moved the weighted Pearson by +0.0026 on average, within the spread "
            "across the three windows that ended on 20 September 2021 (SD 0.0023, t about 1.96 on 2 df); only the "
            "newest window's interval excludes 0 (+0.0050 [+0.0005, +0.0099])."
        ),
        "splits_train_under_half": (
            "Signed off (Lennart, 2026-11-11, review issue 9, reply a): the window of the 2020 crash (from 28 February "
            "2020) trains on 48.25% of the rows, beside 93.0% and 69.2%; SPLIT-14's two tiers admit it."
        ),
    }
    target = "Target"
    problem_type = "regression"
    metric = Metric.source(
        "weighted_pearsonr",
        original="weighted version of the Pearson correlation coefficient",
        reference="https://www.kaggle.com/competitions/g-research-crypto-forecasting/overview/evaluation",
        inputs={"weight": "Weight"},
        definition="Pearson correlation of Target and the prediction over all test rows, each row weighted by its asset's Weight",
    )
    scoring_columns = (
        ScoringColumn(
            column="Weight",
            role="weight",
            used_by="weighted_pearsonr",
            description=(
                "the asset's weight from asset_details.csv (Bitcoin 6.78 ... IOTA and Maker 1.10), mapped from "
                "Asset_Name; each row is weighted by it in the Pearson correlation. Asset_Name stays a feature."
            ),
        ),
    )

    # Splits
    temporal = Temporal(
        on="timestamp",
        splits=TemporalSplits(
            window=91,
            unit="days",
            gap=15,
            gap_unit="minutes",
            sample_by="time",
            cutoffs=("2021-10-25", "2020-12-22", "2020-02-28"),
        ),
    )
    splits_comment = """
        The competition scored every submitted model, frozen after training, on the 3 months of live data after its submission deadline (2 February to 3 May 2022); no source gives a production refit cadence, so a window is those 91 days (the horizon checked by Lennart on 2026-11-11). We use three windows of 91 days as test windows and all earlier data as train data, with a 15-minute gap, the minimum and the target's own horizon: a row's target needs the Close 16 minutes later, so the newest training label is known at the close of the window's first minute, when the first test prediction is made (Lennart, 2026-10-22; against a 1-day gap the weighted Pearson moves by -0.0003 on average, inside the seed noise, on the windows of train.csv). The windows (Lennart, 2026-11-11; Review issue 9, reply a) test three markets a model that trades every minute has to hold in: the newest, 25 October 2021 to 23 January 2022, the falling market after Bitcoin's peak of 10 November 2021 and the deployment period (it holds the 99 EOS.IO bars of 26-27 October 2021 with a Low near 1.09 against a price near 4.8, kept as the release gives them, see the notes); the bull run of 22 December 2020 to 22 March 2021 (Bitcoin +138%), with the widest target spread; and the quiet market of 28 February to 28 May 2020 (59 trades a coin-minute at the median against 243 in the bull run), with the largest crash in the data, Bitcoin's -39% on 12 March 2020. The three newest windows tested before (from 25 October, 26 July and 26 April 2021) put two in the busy market of 2021 and none in a quiet one. They hold 1,830,834, 1,834,016 and 1,544,359 rows before the test sampling; their train sides hold 24,170,779, 17,985,995 and 12,545,715 rows (93.0%, 69.2% and 48.25% of the 26,001,823 rows of the frame), each ending at 23:44 the day before its window. The crash window trains on less than half the rows (48.25%), signed off by Lennart on 2026-11-11 beside the two on 69.2% and 93.0%. Each window keeps at most 500k of its rows, and each train side holds every earlier row, which a benchmark sub-samples to 1M before a fit, by default from the newest year before the window (`subsample_train`); both draw whole minutes at random (every asset of a drawn minute kept), as the target and the features are relative to the 14-asset market at each minute. Rows of one asset a few minutes apart share most of their 15-minute target window (per asset, targets 5 minutes apart correlate with a median of 0.57, range 0.25-0.66, in train.csv), so validation inside a train side has to split by time blocks, not rows: LightGBM early-stopped on random rows of the train side stops after 220-528 rounds and scores test R^2 -0.0049, -0.0043 and -0.0090, against +0.0006, +0.0013 and +0.0004 when it stops on the newest 10% (random-row train sides, 1-day gap).
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "train": pd.read_csv(raw_dir / "train.csv"),
            "supplemental": pd.read_csv(raw_dir / "supplemental_train.csv"),
            "assets": pd.read_csv(raw_dir / "asset_details.csv"),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, assets = all_bars(raw), raw["assets"]
        # The history features come from every bar of both files, before the rows without a target are dropped, so
        # the look-back windows run across the seam of 21 September 2021.
        df = pd.concat([df, history_features(df)], axis=1)
        df = df[df["Target"].notna()]
        # VWAP is a positive price: its infinite and negative values (Maker, June 2020) become missing.
        vwap = df["VWAP"].to_numpy()
        df.loc[~np.isfinite(vwap) | (vwap <= 0), "VWAP"] = np.nan
        # A traded volume cannot be negative (Maker): missing.
        df.loc[df["Volume"] < 0, "Volume"] = np.nan
        # The asset's name instead of its id (same position).
        df["Asset_ID"] = df["Asset_ID"].map(assets.set_index("Asset_ID")["Asset_Name"])
        # The asset's weight in the metric (asset_details.csv, exact values): a scoring column, not a feature.
        df["Weight"] = df["Asset_ID"].map(assets.set_index("Asset_Name")["Weight"])
        df = df.rename(columns={"Asset_ID": "Asset_Name"})
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        del df
        return FeatureTypes(categorical=["Asset_Name"], datetime=["timestamp"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        train, assets = all_bars(raw), raw["assets"]
        names = assets.set_index("Asset_ID")["Asset_Name"]
        coverage = train.groupby("Asset_ID").agg(
            first_minute=("timestamp", "min"),
            rows=("timestamp", "size"),
            share_without_target=("Target", lambda s: round(float(s.isna().mean()), 4)),
        )
        coverage["first_minute"] = pd.to_datetime(coverage["first_minute"], unit="s")
        coverage.index = coverage.index.map(names).rename("asset")
        numeric = [c for c in df.columns if c not in ("timestamp", "Asset_Name", "Weight", self.target)]
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
                "and a row has no target when the asset's Close one or 16 minutes later is missing (rows of the two "
                "raw files).",
                coverage,
            ),
            Decision(
                "History features from the 3rd-place solution carry the signal",
                "The bar of one minute says little about the next 15 minutes; the asset's recent returns relative to "
                "the market do (in ranks most clearly). Correlation of each feature with the target on the shipped frame.",
                correlation,
            ),
        ]
