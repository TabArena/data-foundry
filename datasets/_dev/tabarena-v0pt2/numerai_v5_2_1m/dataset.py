"""Curated dataset definition for `numerai_v5_2_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

FEATURE_SET = "all"
"""Numerai's feature set in features.json: all 2,748 features of v5.2, less the EXCLUDED_FEATURE_SET."""

EXCLUDED_FEATURE_SET = "faith"
"""The 372 Faith features, which Numerai chose with the targets of the test eras and released at era 1192 (LEAK-31)."""

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
            "2,376 disguised features of the stock as of that Friday (Numerai's full set without its Faith family), "
            "each binned into five levels within the week."
        ),
        split=(
            "Three test years of 52 weekly eras, the newest first. Training is a random 1M rows of the earlier eras, "
            "leaving out the last four before the test year, whose targets are not yet known."
        ),
        changes=(
            "We set the values Numerai fills in for a feature without data in a week to missing, and use all "
            "features but the 372 that Numerai chose with the targets of our test years."
        ),
        fit="approximate",
        fit_reason=(
            "Numerai's features are designed to predict the target, and the set we use dates from July 2024, within "
            "the oldest test year. The "
            "score is Numerai's own: the per-week correlation, averaged over the weeks of the test window. "
            "Everything else is known on the Friday."
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

        Retired at the source: on 2026-10-16 Numerai released Classic v6.0 and retired the public v5.0-v5.3 training and validation downloads (docs; forum thread 8367: "The v5.x data is no longer available"), so the command above no longer serves train.parquet or validation.parquet. We keep v5.2 as a frozen release: our local files, pinned by the SHA-256 below, are the only exact copy. No community mirror matches them: the Hugging Face upload Mcdonald82/numerai-v5.2 (2026-02-23) holds the same train.parquet re-saved (same rows, schema and column statistics) but validation only to era 1206; Kaggle uploads are older snapshots or v5.3. Numerai's terms of service (4.2) forbid passing the data on, so no mirror is a sanctioned download route.

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
        We start with train.parquet and validation.parquet of the Numerai tournament data v5.2 ("Faith2"), with all features of features.json except the Faith family.

        - Prediction point: every Friday after the market close (one era), a model scores each stock from its features as of that day; the target is the stock's return over the next 20 market days, known about 5 weeks later (at era T the newest resolved target is that of era T - 5).
        - Scope: a ranking of the stocks within each week, not forecasting of a series. `id` is unique across all 6.88M rows, so the data holds no series per stock, and a stock's newest known target (matched by its nearest neighbour on the 780 `medium` features five eras back) correlates 0.01, -0.00 and -0.01 with its target at three test eras. Whether some disguised features are trailing returns cannot be tested.
        - Target: `target_ender_20`, equal to the main target `target` of v5.2: a stock-specific return, ranked within each era and binned into 0, 0.25, 0.5, 0.75 and 1, so every era has a mean of 0.5. The other 40 target columns are future returns and are not read.
        - Features: the 2,376 features of Numerai's `all` set without its 372 `faith` features (exactly v5.0's `all`, unchanged since July 2024), each an integer bin 0-4 within its era with an obfuscated name (CC 2026-10-26: "yes ship all"; CLEAN-22, no task reason leaves the other features out). With Numerai's own example and deep LightGBM settings, `medium` and `all` cannot be told apart on the test windows (the sign of the difference follows the training sample; on the full history they tie), and training on more rows helps more than either set.
        - Rows: we keep data_type `train` and `validation` up to era 1235 and drop data_type `test` (eras 1236-1240), whose targets had not resolved on 2026-10-06.
        - `era` (one per week; Numerai publishes no dates) becomes an integer and the time column. `id` is unique per stock per era (docs), so it identifies no stock and is not read.
        - Missing values: Numerai sets every value of a feature-era without data to 2 (hello_numerai.ipynb of v5.2); we set such feature-eras to missing (decision table). Elsewhere each bin holds 20% of an era's stocks, so no single stock is filled with 2. No duplicate rows.
        - Anomaly: the universe grows from 2,314 stocks in era 1 to 6,057-7,231 per era since era 1100.
        - Note: the task probes flag no_signal, drift_baseline and unstable. We keep the task (task_probes.md, rule 2, TP-2): on the shipped splits, with the 2,376 features, Numerai's example LightGBM (2,000 trees, learning rate 0.01, depth 5, column sample 0.1) correlates with the target at 0.0094 ± 0.0021, 0.0127 and 0.0127 per era, newest window first, and its deep benchmark settings at 0.0108 and 0.0173 (newest and oldest windows); the probes score R², under which no model beats the mean (2026-10-26). With the 780 `medium` features, before, a 600-tree LightGBM gave 0.0071, 0.0142 and 0.0154. The newest window is fragile: one of five other random 1M train samples gives ridge a t of 0.8 there. Tuned results are pending; if tuned methods do not beat the constant 0.5 window by window under the metric that scores, the dataset goes to `TBD -> 2nd Tier` (as zillow_prize).
        - Metric: Numerai's CORR, computed per era and averaged over the 52 eras of a test window (the spec). Pooled `pearsonr`, declared before, tracked it within 0.0002 per model because every era's target mean is 0.5. RMSE, declared before that, ranks the scale of the predictions, not the ranking of the stocks within each era: its model ranking agreed with per-era CORR at Kendall tau -0.11, 0.11 and 0.39 in the three windows, and a copy of one LightGBM's predictions scaled by 3 lost to the constant 0.5 in every window.
        - We drop the 372 `faith` features (LEAK-31, CC 2026-10-26): Numerai engineers features "to be predictive of the target" and released the Faith family at era 1192 (Faith I) and about era 1198 (Faith II) because they predicted the target over past eras, our test eras 1080-1191 among them. Every value may be point-in-time, but the choice of features was made with our test labels. On the shipped splits, ridge with the 75 Faith features of `medium` gained +0.0043 ± 0.0006 per-era correlation in 1080-1131 (about 28% of the signal there), +0.0013 ± 0.0007 in 1132-1183, +0.0056 ± 0.0018 in 1184-1191 and +0.0010 ± 0.0006 after the release. The `midnight` features (244 in `all`, released about era 1098) stay: the 122 of them in `medium` showed no gain before their release (-0.0005 ± 0.0011 in 1080-1097). Note: Numerai's v5.0 rebuild (July 2024, about era 1125) also falls within the oldest test window; not measured.
        - History: each train side is a random 1M of all earlier eras (TabReD's convention); Numerai's example models train on all eras, so the whole history is what a participant trains on.
        - Note: feature neutralization post-processes predictions per era, so it belongs to a model or a scorer and is not applied.
        - Note: numerai28_6 (OpenML 23517), an older sample of this data, is not added separately.
    """

    # Task
    target = "target_ender_20"
    problem_type = "regression"
    metric = Metric.source(
        "mean_group_pearsonr",
        original="CORR (numerai_corr), the per-era correlation averaged over eras",
        reference="https://docs.numer.ai/numerai-tournament/scoring/correlation-corr",
        params={"method": "numerai_corr"},
        inputs={"group": "era"},
        definition=(
            "per era: rank-gaussianize the predictions, signed power 1.5; centre the target, signed power 1.5; "
            "Pearson correlation; mean over eras (numerai_tools numerai_corr)"
        ),
    )

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
        sets = json.loads((raw_dir / "features.json").read_text())["feature_sets"]
        excluded = set(sets[EXCLUDED_FEATURE_SET])
        features = [f for f in sets[FEATURE_SET] if f not in excluded]
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
