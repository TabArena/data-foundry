"""Curated dataset definition for `numerai_v5_2_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from data_foundry.v2 import AbstractCuratedDataset, Decision, TaskSummary, Temporal, TemporalSplits, drop_columns

FEATURE_SET = "medium"
"""Numerai's feature set in features.json: 780 basic features of the 2,748 in v5.2."""

LAST_ERA = 1235
"""The newest era whose target had resolved in the download of 2026-10-06; later downloads add newer eras."""

MISSING_BIN = 2
"""Numerai fills every stock of a feature-era without data with the middle bin."""


class NumeraiV521m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How will a stock's return over the next 20 market days rank against the other stocks of the same week?"
        ),
        use_case=(
            "Every Friday after the market close, a participant of the Numerai tournament scores each stock from its "
            "features as of that day and submits the scores, which Numerai combines for its trading."
        ),
        row=("One stock in one weekly era of Numerai's v5.2 tournament data; dates and stock names are hidden."),
        predicted=(
            "The stock's own return over the next 20 market days, ranked within the week and binned into five levels "
            "from 0 to 1; it is known about five weeks later."
        ),
        known=(
            "780 disguised features of the stock as of that Friday (Numerai's medium set), each binned into five "
            "levels within the week."
        ),
        split=(
            "Three test years of 52 weekly eras, the newest first. Training is a random 1M rows of the earlier eras, "
            "leaving out the last four before the test year, whose targets are not yet known."
        ),
        changes=(
            "We set the values Numerai fills in for a feature without data in a week to missing, and use the medium "
            "feature set (780 of 2,748)."
        ),
        fit="approximate",
        fit_reason=(
            "Numerai designed some features with the targets of the test years (75 released at era 1192). The "
            "score is the Pearson correlation over all test rows, which stands for Numerai's per-week correlation "
            "(within 0.0002 per model on the shipped windows). Everything else is known on the Friday."
        ),
    )

    # Dataset
    unique_name = "numerai_v5_2_1m"
    version_of = "numerai_v5_2"
    version_comment = """
        We sample per test window (v2 split protocol): each test window keeps at most 500k of its rows (all of them here: 327,025 to 361,712), and its train side is a random 1M of all earlier rows, drawn in one random order for all windows; the frame keeps only the rows a split uses. As in TabReD, the train data is sub-sampled at random rather than cut in time, so it keeps rows of every era. The full data has 6,881,281 rows (eras 1-1235); the frame has 2,025,745.
    """
    year = "2025"
    domain = "finance"
    source = "Other"
    source_url = "https://numer.ai/data/v5.2"
    license = (
        "Numerai Terms of Service (updated 2026-08-31), section 4.2: use solely to participate in Numerai tournaments; "
        "no commercial use outside its services, no redistribution, keep the data confidential"
    )
    data_tags = ("Anonymized",)
    download_description = """
        We download Numerai's v5.2 ("Faith2") tournament files with the numerapi client on 2026-10-06:

        mkdir -p local-data-warehouse/numerai_v5_2 && cd local-data-warehouse/numerai_v5_2
        uvx --from numerapi==3.1.1 python -c "from numerapi import NumerAPI; api = NumerAPI(); [api.download_dataset(f'v5.2/{f}', f) for f in ('features.json', 'train.parquet', 'validation.parquet')]"

        The API serves only the current weekly snapshot of each file, with no versioned URL. Ours came from the S3 folder 20261005: features.json (323,414 bytes), train.parquet (2,597,791,287 bytes, eras 1-574) and validation.parquet (4,417,740,944 bytes, eras 575-1240). Numerai adds new eras to validation.parquet as their targets resolve, so the definition keeps eras 1-1235; a later download gives the same rows as long as Numerai does not revise past eras. SHA-256 of our files:

        64cd254cba63c0966eeeb71c7c83c99cacb81d4acd8b36524195d20c92dd5c35  features.json
        73b41e084c91e50618227aca3759be46f59367a4506d0f3f43a5112fb83bbeca  train.parquet
        04f74ad99dd1afcee046a12c52d1a98b51dab4bf978fa042aa3f5fbaeb4601c0  validation.parquet
    """
    bibtex = r"""
        @misc{numerai2025v52,
          author = {{Numerai}},
          title = {Numerai Tournament Dataset v5.2 (Faith2)},
          year = {2025},
          howpublished = {\url{https://numer.ai/data/v5.2}},
          note = {Obfuscated global equity data, downloaded with numerapi; documentation at \url{https://docs.numer.ai/numerai-tournament/data}}
        }
    """
    curation_comments = """
        We start with train.parquet and validation.parquet of the Numerai tournament data v5.2 ("Faith2"), with the medium feature set of features.json.

        - Prediction point: every Friday after the market close (one era), a model scores each stock from its features as of that day; the target is the stock's return over the next 20 market days, known about 5 weeks later (at era T the newest resolved target is that of era T - 5).
        - Scope: a ranking of the stocks within each week, not forecasting of a series. `id` is unique across all 6.88M rows, so the data holds no series per stock, and a stock's newest known target (matched by its nearest neighbour on the 780 features five eras back) correlates 0.01, -0.00 and -0.01 with its target at three test eras. Whether some disguised features are trailing returns cannot be tested.
        - Target: `target_ender_20`, equal to the main target `target` of v5.2: a stock-specific return, ranked within each era and binned into 0, 0.25, 0.5, 0.75 and 1, so every era has a mean of 0.5. The other 40 target columns are future returns and are not read.
        - Features: the 780 features of Numerai's `medium` set, of the 2,748 in v5.2, each an integer bin 0-4 within its era with an obfuscated name; Numerai describes `medium` as features "each unique in some way". On the newest test window `medium` and `all` cannot be told apart: their order flips with the random 1M train sample (LightGBM per-era correlation 0.0006-0.0088 for `medium` over four samples, 0.0044-0.0060 for `all` over two). Whether the other 1,968 features are near-copies of the 780 is not measured.
        - Rows: we keep data_type `train` and `validation` up to era 1235 and drop data_type `test` (eras 1236-1240), whose targets had not resolved on 2026-10-06.
        - `era` (one per week; Numerai publishes no dates) becomes an integer and the time column. `id` is unique per stock per era (docs), so it identifies no stock and is not read.
        - Missing values: Numerai sets every value of a feature-era without data to 2 (hello_numerai.ipynb of v5.2); we set such feature-eras to missing (decision table). Elsewhere each bin holds 20% of an era's stocks, so no single stock is filled with 2. No duplicate rows.
        - Anomaly: the universe grows from 2,314 stocks in era 1 to 6,057-7,231 per era since era 1100.
        - Note: the task probes flag no_signal, drift_baseline and unstable. We keep the task (task_probes.md, rule 2, TP-2): on the shipped splits, LightGBM like Numerai's example model (600 trees) correlates with the target at 0.0071, 0.0142 and 0.0154 per era, newest window first (t = 3.3, 7.7 and 8.1). The newest window is fragile: one of five other random 1M train samples gives ridge a t of 0.8 there. Tuned results are pending; if tuned methods do not beat the constant 0.5 window by window under the metric that scores, the dataset goes to `TBD -> 2nd Tier` (as zillow_prize).
        - Metric: Numerai scores CORR, the mean over eras of the per-era correlation of the predictions with the target, which no listed metric names; we declare pooled `pearsonr`, which tracks CORR within 0.0002 per model here because every era's target mean is 0.5 (TP-6). RMSE, declared before, ranks the scale of the predictions, not the ranking of the stocks within each era. Over the constant 0.5, the train mean, ridge and LightGBM fits and copies of one LightGBM's predictions scaled by 0.3 and 3 (same ranking), RMSE's model ranking agrees with per-era CORR at Kendall tau -0.11, 0.11 and 0.39 in the three windows, pooled Pearson correlation at 0.89 to 0.93; the copy scaled by 3 loses to the constant in every window, and on the newest window the constant 0.5 beats ridge and LightGBM as fitted.
        - Potential leak, kept on purpose: Numerai designs features to predict the target and released the 75 `faith` features of `medium` at era 1192, so test eras 1080-1191 lie in their design period. On the shipped splits, ridge with them gains +0.0043 ± 0.0006 per-era correlation in 1080-1131 (about 28% of the signal there), +0.0013 ± 0.0007 in 1132-1183, +0.0056 ± 0.0018 in 1184-1191 and +0.0010 ± 0.0006 after the release. The 122 `midnight` features (released about era 1098) show no gain before their release (-0.0005 ± 0.0011 in 1080-1097). LEAK-31 says to remove a selection made with test labels when we can (dropping the 75 leaves 705); they stay for now as the source's own published inputs, and the curator decides. Revisit once v5.2 has a year of eras after the release.
        - History: each train side is a random 1M of all earlier eras (TabReD's convention); Numerai's example models train on all eras, so the whole history is what a participant trains on.
        - Note: feature neutralization post-processes predictions per era, so it belongs to a model or a scorer and is not applied.
        - Note: numerai28_6 (OpenML 23517), an older sample of this data, is not added separately.
    """

    # Task
    target = "target_ender_20"
    problem_type = "regression"
    metric = "pearsonr"  # stands for Numerai's per-era CORR (curation comments)

    # Splits: three windows of 52 weekly eras, 4 embargoed eras between train and test.
    temporal = Temporal(
        on="era",
        splits=TemporalSplits(window=52, unit="unique", n_windows=3, gap=4),
        horizon=52,
        horizon_unit="weeks",
        gap=4,
        gap_unit="weeks",
    )
    subsample_to_budget = True
    splits_comment = """
        Three test windows of 52 weekly eras (one year) each, newest first: eras 1184-1235, 1132-1183 and 1080-1131. Train is every era before the 4 eras that precede the window (train ends at era 1179 for the window starting at 1184). An era's 20-market-day target resolves about 5 weeks later: the download of 2026-10-06 has targets up to era 1235 and none for 1236-1240, so at era T the newest known target is that of era T - 5. Numerai's v5.2 notebook says to "embargo the first 4 eras following our last train era", but its code skips only 3 eras, so our gap is one era stricter. Numerai's example notebooks score a model on a long out-of-sample period (eras 575 onward); one year per window keeps 3 windows near the newest data and gives each window score 52 eras. Each test window keeps all its rows (327,025 to 361,712, under the 500k budget); each train side is a random 1M of all earlier rows (one random order for all windows); the frame keeps only the rows a split uses. Inner validation (tuning, early stopping) must be era-blocked with a 4-era gap as well: a stock's 20-day targets overlap for 3 eras, so on the newest train side a random hold-out gives LightGBM a per-era correlation of 0.040 (t 16.8), against 0.004 (t 1.1) on the last 52 train eras after a 4-era gap.
    """

    accepted_check_warnings = {
        "task_target_low_cardinality": "The target is a continuous return that Numerai ranks within each era and bins "
        "into 5 ordered levels (0 to 1); Numerai treats it as regression (its example models are regressors scored by "
        "correlation), and so do we.",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        features = json.loads((raw_dir / "features.json").read_text())["feature_sets"][FEATURE_SET]
        columns = ["era", "data_type", self.target, *features]
        tables = [pq.read_table(raw_dir / f"{name}.parquet", columns=columns) for name in ("train", "validation")]
        return pa.concat_tables(tables).to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. The era ("0001", ...) as an integer; keep the rows with a resolved target: data_type train and
        #    validation (not test), eras up to LAST_ERA (one row filter: the frame is several GB).
        era = raw["era"].astype("int32")
        keep = raw["data_type"].isin(["train", "validation"]) & (era <= LAST_ERA)
        df = drop_columns(raw.assign(era=era), ["data_type"])[keep]
        # 2. A feature-era in which every stock has the middle bin is missing data (Numerai's fill): set it to NaN.
        return _missing_feature_eras_to_nan(df)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        features = [c for c in df.columns if c.startswith("feature_")]
        eras = pd.cut(df["era"], [0, 574, 894, LAST_ERA], labels=["1-574", "575-894", "895-1235"]).rename("eras")
        missing = df[features].isna()
        table = pd.DataFrame(
            {
                "rows": eras.value_counts(sort=False),
                "share of feature values missing": missing.groupby(eras, observed=False).mean().mean(axis=1),
                "features with a missing era": missing.groupby(eras, observed=False).any().sum(axis=1),
            }
        )
        return [
            Decision(
                "Feature-eras filled with the middle bin are set to missing",
                "Numerai sets every stock of a feature-era without data to 2; an era in which a feature takes only "
                "that value is missing data, not a middle rank. It occurs only in the older eras (shares of the "
                "rows in this frame).",
                table,
            )
        ]


def _missing_feature_eras_to_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Set to NaN the values of every (feature, era) in which all stocks have MISSING_BIN; such features become
    float32, the others stay int8.
    """
    codes, _ = pd.factorize(df["era"], sort=True)
    n_eras = int(codes.max()) + 1
    columns = {}
    for col in df.columns:
        values = df[col].to_numpy()
        if col.startswith("feature_"):
            counts = np.bincount(codes * 5 + values, minlength=n_eras * 5).reshape(n_eras, 5)
            missing_era = (counts > 0).sum(axis=1) == 1
            missing_era &= counts[:, MISSING_BIN] > 0
            if missing_era.any():
                values = np.where(missing_era[codes], np.float32(np.nan), values.astype(np.float32))
        columns[col] = values
    return pd.DataFrame(columns, index=df.index)
