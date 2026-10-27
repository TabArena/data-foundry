"""Curated dataset definition for `numerai28_6` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, Metric, TaskSummary

N_ORDER_BLOCKS = 10
"""File-order blocks for the decision table on hidden weeks (the raw file's row order)."""


class Numerai286(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a stock end up in the positive class of Numerai's binary target, from 21 disguised features?",
        use_case=(
            "Numerai, a hedge fund, collects probability estimates from tournament participants for each stock and "
            "combines them to rank stocks for its next trading period; the 2016 tournament ranked participants by log "
            "loss."
        ),
        row=(
            "One stock at one undisclosed date of Numerai's 2016 training data (a 96,320-row sample Numerai put on "
            "Kaggle); the stock, the date and the week are not given."
        ),
        predicted=(
            "Numerai's binary target, an undisclosed outcome of the stock's later return; the horizon and the "
            "definition were never published."
        ),
        known="21 encrypted, regularized numbers per stock, each in [0, 1]; what they measure is hidden.",
        split="Random rows; the week of a row is unknown.",
        changes="",
        fit="approximate",
        fit_reason=(
            "The task is real (Numerai traded on these predictions), but the features are encrypted and the release "
            "has no date or week, so the test data cannot stand for later weeks as in the tournament."
        ),
    )

    # Dataset
    unique_name = "numerai28_6"
    year = "2016"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/numerai/encrypted-stock-market-data-from-numerai"
    license = "CC0: Public Domain"
    data_tags = ("ForcedIIDFromTemporal", "Anonymized")
    download_description = """
        kaggle datasets download numerai/encrypted-stock-market-data-from-numerai --unzip -p numerai_download && mkdir -p local-data-warehouse/numerai28_6 && mv numerai_download/numerai_training_data.csv local-data-warehouse/numerai28_6/ && rm -r numerai_download
    """
    bibtex = r"""
        @misc{Numerai2016EncryptedStockMarketData,
          author = {{Numerai}},
          title  = {Encrypted Stock Market Data from Numerai},
          year   = {2016},
          howpublished = {\url{https://www.kaggle.com/datasets/numerai/encrypted-stock-market-data-from-numerai}},
          note   = {Kaggle dataset}
        }
    """
    curation_comments = """
        We start with numerai_training_data.csv from Numerai's own Kaggle dataset (owner `numerai`, CC0, "a sample of the training data used in the Numerai machine learning competition"; version 1, last updated 2016-12-02).

        - Prediction point: a tournament round, when Numerai asks for a probability per stock. The 2016 rules page states neither the round's cadence nor the target's return window; weekly rounds are Numerai's later design (USE-1, assumed).
        - No change to the file: 21 features, the binary target as 0/1, no missing values, no duplicate rows (96,320 rows; 48,658 of class 1, 47,662 of class 0).
        - The split is forced (ForcedIIDFromTemporal, SPLIT-8): Numerai trains on past weeks and scores the next one, but this release has no era, date or id column. A dated split would test a model on later weeks' market states; a random split mixes stocks of the same unknown weeks, which share the weekly market state. That cost cannot be measured here, but its main source in numerai_v5_2 is absent: there, IID splits recognised the same stock one week back with an overlapping label (1-NN target agreement 0.618), while here 1-NN agreement is 0.501 and the closest pairs agree below chance (0.433 for the closest 0.1%). What remains is drift in the weekly feature-target relation, which v5.2's dated windows show can take the out-of-time signal to about 0; read the IID ROC AUC of 0.524-0.531 as an upper bound and model rankings as fragile. Recover the eras and split by them if a dated release of the 2016 data turns up.
        - Hidden weeks, checked (2026-10-22): the file order is shuffled (target mean of 20 file-order blocks 0.494-0.521, lag-1 autocorrelation of every feature at most 0.007 in absolute value, a row's file-order block predicted at chance, 0.1005 against 0.10); 1-NN target agreement 0.501 against 0.502 for a random neighbour (numerai_v5_2, with its weeks, 0.618); the hidden-group probe finds no entity-like column, composite key or near-copy cluster; holding out k-means clusters as stand-in weeks moves LightGBM's ROC AUC by at most 0.0055 (0.526 random, 0.520-0.524 grouped). The target rate differs across those clusters more than binomial noise (SD 0.0185 against 0.0051 for 10 clusters), but targets simulated from out-of-fold logistic-regression probabilities reproduce it (0.0216 against 0.0219 observed), and after LightGBM the residual spread is binomial (0.0046 against 0.0053): the features' signal, not a week.
        - The signal is small: ROC AUC 0.531 (logistic regression) and 0.524 (LightGBM) on 5 random folds (fold SD about 0.003), the same on file-order blocks. Expected for stock returns, and the reason models sit close together: under log loss the dummy scores 0.6931 and logistic regression 0.6912-0.6921 per fold, a spread of about 0.0015, and untuned LightGBM and random forest score worse than the dummy.
        - Metric: Numerai's 2016 rules rank models "by accuracy (logloss)" on uploaded probabilities (numer.ai/rules, archived 2016-08-30), so log loss is the source's metric. Numerai later moved to per-era correlation, which needs the eras this release lacks.
        - Distinct from numerai_v5_2 (PROV-7, not a PROV-6 duplicate): a different release of a different design, not a cut of the same table. Here 21 continuous features and a binary target; v5.2 has 2,748 five-level features, a 20-day return ranked within each week and binned into five levels, and weekly eras. No row can be matched between them, so each gives its own task from one source.
        - Not OpenML 23517 (numerai28.6), although the record carries that name: OpenML's file holds 72,404 rows (36,605 / 35,798) of the same 21-feature design and shares no feature row with the Kaggle file, so it is another 2016 training sample. We use the data owner's Kaggle upload.
        - Anomaly: every feature uses one global set of 1,000 values, each used by 73-118 rows, unevenly spaced over [0, 1], plus an exact 0.0 held by one row in 17 features; Numerai's encryption quantised them. One global set means the values carry no week fingerprint. The target rate per value varies by SD 0.051-0.058 against 0.051 binomial, the excess explained by the features' own monotone signal.
        - Potential leak, kept on purpose (LEAK-30): the values are equal-frequency quantile bins fitted on a larger population that holds our test rows. The counts per value are far more even than sampling would give (variance over mean 0.29-0.37 on all 21 features, against 1.0), which fits bins built over about 140,000 rows of which this file is a sample (OpenML 23517's 72,404 disjoint rows give the same estimate). No raw values exist, so the transform cannot be refitted per fold; a bin edge carries almost no information about one row's label, and we do not rescale.
    """

    # Task
    target = "target"
    problem_type = "binary_classification"
    metric = Metric.source(
        "log_loss",
        original="logloss (Numerai tournament, 2016: models are ranked by accuracy (logloss) as well as originality)",
        reference="http://web.archive.org/web/20160830071822/https://numer.ai/rules",
        definition="Mean binary log loss of the uploaded probability that a row is of class 1",
    )
    splits_comment = """
        Default splits (random rows, stratified on the target). Forced IID from temporal (SPLIT-8): the release has no era or date, so the weekly splits of Numerai's tournament cannot be rebuilt; see the curation notes for the hidden-week checks.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "numerai_training_data.csv")

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        features = [c for c in raw.columns if c != "target"]
        block = np.arange(len(raw)) * N_ORDER_BLOCKS // len(raw)
        lag1 = raw[features].apply(lambda s: s.autocorr(lag=1))
        table = pd.DataFrame(
            {
                "rows": raw.groupby(block).size(),
                "target_mean": raw.groupby(block)["target"].mean().round(4),
            }
        )
        table.index.name = "file_order_block"
        return [
            Decision(
                title="IID split, forced from temporal",
                why=(
                    "The release has no era or date. Blocks of the raw file order carry no week structure: the "
                    f"target mean stays near the base rate in every block, and the largest lag-1 autocorrelation of a "
                    f"feature is {lag1.abs().max():.4f}."
                ),
                evidence=table,
            )
        ]
