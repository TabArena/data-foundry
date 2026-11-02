"""Curated dataset definition for `loan_default_prediction_imperial_college` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

# Running aggregates of a hidden per-period quantity x: f527 and f528, the forum's "golden features" (topic 7115),
# include the loan's own period and so record the period of the outcome (LEAK-10); f529-f531, f534, f535 and f537 go
# with them by the curator's call (CC 2026-11-01), and f533, which behaves like those six, goes with the block.
# `_decisions` shows the evidence.
CURRENT_PERIOD_AGGREGATES = ["f527", "f528", "f529", "f530", "f531", "f533", "f534", "f535", "f537"]
# Columns that give the entity's previous loan's loss as strongly when that loan was granted 1-10 loans earlier as
# when it lies far back, so they were filled in after the fact (LEAK-10; `_decisions`, the second table). Their exact
# copies f225-f227, f255-f257 and f265-f267 go as copies (CLEAN-5).
PREVIOUS_LOSS_HINDSIGHT = [
    "f211", "f212", "f214", "f215", "f216", "f217", "f221", "f222", "f224", "f251", "f252", "f254", "f261", "f262",
    "f264", "f271", "f272", "f273", "f274", "f275", "f277", "f278", "f538", "f539", "f568", "f569", "f577", "f578",
]  # fmt: skip
# Columns whose top values record a change of x in the loan's own period (LEAK-10; the notes give the test).
OWN_PERIOD_TAILS = ["f468", "f471", "f536"]
# Columns whose values pass the largest float32 (3.4e38); they ship as log10 (as rdkit_Ipc_log10, Lennart 2026-10-21).
BEYOND_FLOAT32 = ["f391", "f627"]


def _constant_and_copied_columns(df: pd.DataFrame, columns: list[str]) -> tuple[list[str], list[str]]:
    """The columns with at most one value besides missing, and every column that equals an earlier one in file order."""
    constant = [c for c in columns if df[c].nunique() <= 1]
    first_by_hash: dict[str, list[str]] = {}
    copies = []
    for c in columns:
        if c in constant:
            continue
        values = df[c].to_numpy(dtype="float64")
        key = hashlib.sha256(np.nan_to_num(values, nan=np.pi * 1e300).tobytes()).hexdigest()
        earlier = first_by_hash.setdefault(key, [])
        if any(np.array_equal(values, df[e].to_numpy(dtype="float64"), equal_nan=True) for e in earlier):
            copies.append(c)
        else:
            earlier.append(c)
    return constant, copies


def _period_links(raw: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Rows of one hidden entity one period apart, as (earlier row, row) positions: the unique matches of a row's
    f521 - 1 and f274 - f271 with the earlier row's f521 and f527.
    """
    n = len(raw)
    row = pd.DataFrame({"t": raw["f521"] - 1, "v": (raw["f274"] - raw["f271"]).round(1), "j": np.arange(n)})
    earlier = pd.DataFrame({"t": raw["f521"], "v": raw["f527"].round(1), "i": np.arange(n)})
    links = row.merge(earlier, on=["t", "v"])
    links = links[~links["j"].duplicated(keep=False) & ~links["i"].duplicated(keep=False)]
    return links["i"].to_numpy(), links["j"].to_numpy()


class LoanDefaultPredictionImperialCollege(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What share of a new loan's amount will the lender lose, 0 when the loan does not default or is fully "
            "recovered, from the anonymised information it has when the loan is granted?"
        ),
        use_case=(
            "For example, a lender or a loan investor ranks new loans by their expected loss when they are granted, "
            "to choose which enter a portfolio; the level of the loss, which a price needs, is set by a separate "
            'calibration. The competition\'s aim was "constructing an optimal portfolio of loans".'
        ),
        row=(
            "One loan of an unnamed lender, in the order the loans were recorded, old to new (105,471 loans; no dates "
            "given; that this is the order they were granted is our reading). Running aggregates link many loans into "
            "chains of one hidden entity; what the entity is is not stated."
        ),
        predicted=(
            "The loss given default as a percentage of the loan's amount, whole numbers from 0 to 100: 0 for 90.7% of "
            "the loans (no default, or a default fully recovered), median 5 among the others."
        ),
        known=(
            "Several hundred anonymised features of the borrower, the loan and the track record of the people "
            "involved, which the host calls ex-ante information; collateral, repayment type and region are named. "
            "Columns found to be filled in after the outcome are dropped."
        ),
        split=(
            "The newest loans are held out: 9 windows of 5,000 loans in the order the loans were recorded, each "
            "trained on the loans before a gap of 5,800 loans, so the test stands for loans granted after the model "
            "was fitted, at a time when the outcomes of the most recent loans were not yet known."
        ),
        changes=(
            "We drop f527 and f528, the forum's golden features, which include the loan's own period, with seven "
            "related aggregates; 28 columns that record the loss of the entity's previous loan after the fact; three "
            "columns whose top values record the loan's own period; and constant and copied columns. Two columns "
            "beyond the float32 range ship as log10."
        ),
        fit="approximate",
        fit_reason=(
            "The features are anonymised, so when each was recorded is inferred from the data: 33 columns found to be "
            "filled in after an outcome (the golden features, 28 with the previous loan's loss, three with the own "
            "period) are dropped, others may remain; the file order stands in for dates, and the gap of 5,800 loans "
            "is a guess at the time a loss takes to settle."
        ),
    )

    # Dataset
    unique_name = "loan_default_prediction_imperial_college"
    year = "2014"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/loan-default-prediction"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized",)
    download_description = """
        We use train_v2.csv from the Kaggle research competition loan-default-prediction ("Loan Default Prediction -
        Imperial College London", 2014), the only file with labels: the labels of test_v2.csv were never released.
        The _v2 files are the host's re-release without the 9 columns removed for leakage on 2014-01-29 (topic 6962).

        kaggle competitions download -c loan-default-prediction -f train_v2.csv.zip && unzip train_v2.csv.zip && rm train_v2.csv.zip
        mkdir -p local-data-warehouse/loan_default_prediction_imperial_college && mv train_v2.csv local-data-warehouse/loan_default_prediction_imperial_college/
    """
    bibtex = r"""
        @misc{ImperialCollegeLondon2014LoanDefaultPrediction,
          author = {{Imperial College London} and Kaggle},
          title  = {Loan Default Prediction - Imperial College London},
          year   = {2014},
          howpublished = {\url{https://www.kaggle.com/competitions/loan-default-prediction}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with train_v2.csv from the Kaggle research competition "Loan Default Prediction - Imperial College London" (2014-01-17 to 2014-03-14), data of an unnamed lender that the data page calls standardized, de-trended and anonymized (as read in screening).

        - Prediction point: when the loan is granted. The host: "each row containing the header fact corresponds to ex-ante information available on either the individual getting the loan, based on his personal features, on his history, etc or on the loan" (Arnaud de Servigny, topic 6862). The data contradict that label for three groups of columns, dropped below.
        - Target `loss`, as the source ships it: "loss = loss given default = scaled number between 0 and 100" (Will Cukierski, topic 6862), the share of a notional of 100 that was lost; "a few loans where there has been full recovery are with a zero loss" (topic 6862), so a 0 is either no default or a default fully recovered. 95,688 zeros (90.7%) and 9,783 losses of 1 to 100 (whole numbers, median 5); no missing values. The host: "There is no after and before. These transactions are all completed." (topic 6871), so no label is pending. Zero inflation is the task (Andrej, 2026-10-30: "We want to add any relevant predictive task, independent if it is zero inflated or not").
        - Dropped, LEAK-10 (an aggregate that may include the row's own outcome): f527 and f528, topic 7115's "golden features". Rows of one hidden entity link from period to period: f521 rises by 1 and the row's f274 - f271 equals the earlier row's f527 (73,319 links). f274 holds the entity's hidden value x of the previous period: the next row's f274 equals the earlier row's x (within 0.5) on 97.3% of the links. f527 averages in x of the loan's own period, in which x changes for 99.99% of the loans with a loss against 33.1% of the others; f528 moves with the own period's x too (Spearman 0.75 with its change, 0.44 with the previous period's). Their changes from the earlier row separate losses at ROC AUC 0.973 (f528) and 0.931 (f527). With them go, as one block, the six related aggregates the curator dropped (f529-f531, f534, f535, f537; Andrej, CC 2026-11-01) and f533, which behaves like them; two label-free tests do not show the seven carrying the own period (open question in REVIEW.md).
        - Dropped, LEAK-10 (filled in after the fact): f221 and 26 related columns (f211, f212, f214-f217, f222, f224, f251, f252, f254, f261, f262, f264, f271-f275, f277, f538, f539, f568, f569, f577, f578) and f278, which give away the loss of the entity's previous loan. A loan granted 1-10 loans earlier cannot have run its term, yet on those 8,083 links f221's level gives its loss at ROC AUC 0.993, as on links over 1,000 loans apart (0.998), and f278's change keeps 0.72-0.75 at short gaps (`_decisions`, second table). So they were filled in once the earlier loan's outcome was known, as `WheelType` in kick. Their copies f225-f227, f255-f257 and f265-f267 go as copies.
        - Dropped, LEAK-10: f468, f471 and f536, whose top values record the loan's own period. Among the loss-free linked rows in their top 0.1%, x changed in the own period in 31 of 36, 34 of 34 and 27 of 27 cases against 33.3% overall, while the previous period changed at its base rate; of 953 column tails under the same test only these and f13 stand out.
        - Potential leak, kept on purpose (LEAK-38, LEAK-32): f615 and f617 give the previous loan's loss at ROC AUC 0.65-0.68 when it was granted 1-10 loans earlier and 0.91-0.95 when over 1,000 loans earlier: the signal grows with distance, as history that arrives over time would, and the 0.65 at short gaps is the remaining risk. f13's low values go with a change of x in the own period (in 100%, 94%, 89%, 76%, 62% and 52% of the loss-free linked rows at f13 = 2 to 7, against 33%, in every quintile of the period counter f521, the link gap and the maturity f4), but as a smooth gradient: over all rows its label-free ROC AUC for an own-period change is 0.658, next to ordinary columns (f68 0.657, f596 0.650), and it does not scale with the size of the change (Spearman -0.09 in its low values, 0.59 in f536's top tail), so it reads as a predictor of the period's event, not a field written from it. The changes of f519, f520, f523 and f526 lean to the own period (label-free 0.613 against 0.532), and dropping them changes nothing. Revisit if the host's field list becomes public.
        - Not in the file: the host removed 9 columns that "consist of an aggregation of historical data that incorporate some ex-post information" (f11, f12, f462, f463, f473, f474, f602, f603, f605; Will Cukierski, topic 6962), and called any leakage left "fair game".
        - Dropped (CLEAN-5): 11 columns with at most one value besides missing (f33-f35, f37, f38, f678, f700-f702, f736, f764; f678 is 0 in every row but one, which is missing) and 81 exact copies of an earlier column (the first in file order kept; `_constant_and_copied_columns`). With the leak drops, 637 of the 769 feature columns remain, with `time_index`.
        - 19 columns hold integers too long for int64 (up to 9e41), which pandas reads as text; they are cast to float64 without loss, and f466, read as uint64, is cast too (its 14,405 distinct values kept). f391 and f627 pass the largest float32 (3.4e38) in 53,049 and 58,304 rows, so they ship as `f391_log10` and `f627_log10` (log10 of values that are all positive), as `rdkit_Ipc_log10` does for the same reason (Lennart, 2026-10-21); a tree model sees the same order.
        - `id` is the time order and ships as `time_index`: the data page says "the observations are still listed in order from old to new in the training set" (quoted in topic 6871), and the Kaggle admin "The train/test split is done by time. All of the test set loans occurred after all of the training set loans." (topic 6871). Along the 73,319 links of one entity's periods the id rises in 99.97% (22 fall back). That the order is the order of granting is our reading.
        - Dtypes: f776, f777 and f778 are categorical, the three factor columns the host names (collateral full or partial, gradual or bullet repayment, the region where the loan was granted; topic 6978, the forum's collection of host posts). f6, the host's "person instructing the loan has the historical relationship", is categorical too: 1,079 unordered codes (0 to 88,565), equal along entity links in 24.2% of the cases against 0.5% for random pairs (CLEAN-14). f2, f4 and f5, which the host says "can be seen as categorical" (a size cluster, maturity ranges, a ranking on ease of transaction), stay numeric: ordered ranges. Every other column stays as shipped, numeric (no semantic context).
        - Missing values stay missing (523 columns, up to 17.9% of the rows). -1 at the bottom of nine columns (f72, f586-f588, f648-f651, f763; 7-12% of the rows) is no missing code: those columns have missing values of their own and continuous values from -0.99 up, so -1 reads as a change of -100%. No two rows share a feature vector.
        - Note: the host says "Each observation is a single loan" (Will Cukierski, topic 6862), yet the links put 88% of the rows into 19,453 chains of one hidden entity (32,152 with the single rows); what the entity is is not stated (the host names the track record of the people involved in the lending). A loss does not end a chain: 70.3% of the loans with a loss have a later row, and a chain's last row has a loss as often as its other rows (9.42% against 9.38%), so the features do not summarise a window that ends at the outcome, as in iranian_churn (retired 2026-10-01).
        - Note: the data page's standardisation and de-trending, and the host's "Several of the factors displayed integrate some clustering of the corresponding features per range of maturity" (topic 6978), may be statistics over all rows of train and test; with anonymised fields this is the known risk of the `Anonymized` tag (LEAK-32), no action. Probe 16 finds no clear sign: 83 columns lie in [0, 1], but most hold many rows at both ends (a median of 138 rows at 1), like shares rather than min-max scaling, and one column (f775) has mean 0 and SD 1.
        - On the shipped columns no change from the entity's earlier row passes ROC AUC 0.595 for the row's own loss, and none of the 203,203 pairwise differences passes 0.647 (on 15,000 rows; the best single column 0.633).
        - Metric, the normalized Gini of the loss, declared from context in place of the competition's MAE (Kaggle API: "Mean Absolute Error"; MET-2, MET-4's overrule clause, MET-11; open question in REVIEW.md). The leaderboard was won with the golden features we drop, which give 9.6-11.3% of a window's loans a default probability above 1/2, so a loss is the median of their outcome, MAE's optimum. Without them 0-0.06% pass 1/2 and MAE's optimum is 0 for nearly every loan: on the 9 windows predicting 0 scores MAE 0.800, LightGBM with the MAE objective 0.800 (it predicts 0), a hurdle model P(loss) x E[loss | loss] 1.466, and the same model with the golden features 0.543. The Gini scores the ranking by expected loss that the portfolio choice acts on (the host: "You are indeed looking to flag the worst of the population", topic 6978): 0 for any constant, 0.196 (0.146 to 0.230) for the hurdle model, 0.132 for LightGBM on the loss, 0.978 with the golden features. RMSE, the fallback, scores the level too and separates the hurdle model from LightGBM on the loss at least as well as the Gini (paired bootstrap z 2.2-2.8 against 1.1-2.1 on 3 windows), but the largest 1% of the errors hold 71-82% of its sum of squares and the hurdle model's R^2 is 0.006 (-0.000 to 0.014; above the training mean on 8 of 9 windows). The Gini ignores the level of the loss, which a price needs; a separate calibration sets it. Untuned LightGBM, 400 trees.
        - Note: the task probes flag no_signal, drift_baseline and unstable, all on R^2 (untuned LightGBM -0.012, the best family, linear, -0.002, on 5 windows), which a few large losses drive. The zero-inflated check (task_probes.md, as for forest_fires) finds both stages learnable, unlike forest_fires: on the 9 windows a loss is ranked at ROC AUC 0.69-0.73 and its size among the loans with a loss at R^2 0.45-0.61 on log1p, and an oracle that knows which loans have a loss reaches R^2 0.30-0.40; the hurdle model's normalized Gini is above 0 on 9 of 9 windows (TP-2: a small but real signal, kept). Each window holds 461 to 527 losses, and the newest window's mean loss (0.813) is no lower than the others' (0.730-0.846), so no sign of losses still open.
    """

    # Task
    target = "loss"
    problem_type = "regression"
    metric = Metric.from_context(
        "normalized_gini",
        reason=(
            'The competition scored the MAE (mean absolute error) of the loss (Kaggle API: "Mean Absolute Error"), '
            "which loses its meaning once the golden features are dropped (MET-2, MET-4): without them 0-0.06% of a "
            "window's loans have a default probability above 1/2, so MAE's optimum is a loss of 0 for nearly every "
            "loan, and predicting 0 scores MAE 0.800 on the 9 windows against 1.466 for a hurdle model "
            "(0.543 with the golden features). The normalized Gini scores the ranking by expected loss that a "
            "lender acts on when it chooses which loans enter a portfolio, the competition's aim; credit and "
            "insurance practice compare risk models by this Gini. It is 0 for a constant and 0.196 (0.146 to 0.230) "
            "for the hurdle model. RMSE, the fallback, also scores the level of the loss and separates the hurdle "
            "model from LightGBM on the loss at least as well as the Gini (paired bootstrap z 2.2-2.8 against 1.1-2.1 "
            "on 3 windows), but the largest 1% of the errors hold 71-82% of its sum of squares and the hurdle model's "
            "R^2 is 0.006. The Gini ignores the level, which a price needs and a separate calibration sets."
        ),
    )

    # Splits
    temporal = Temporal(on="time_index", splits=TemporalSplits(window=5000, unit="rows", n_windows=9, gap=5800))
    splits_comment = """
        The loans are in time order (`time_index`, the source's id; the data page and the Kaggle admin, topic 6871), and the competition split by time too: its test file holds later loans, whose labels were never released. We hold out 9 windows of 5,000 loans, the newest first, each trained on the loans before a gap of 5,800 loans: the oldest window trains on 51.8% of the rows, the newest on 89.8% (SPLIT-11, SPLIT-14). Nine windows match the 3 x 3 splits a random split of this size gets; each holds 461 to 527 loans with a loss. The window is a count of loans because the file has no dates, so the time a window spans is unknown.
        Gap (SPLIT-10): a loan's loss is settled only after its term (the host: terms "vary by a factor from 1 to 3") and the workout, so a model refit at a window's start would not yet know the outcomes of the newest loans. Without dates the delay cannot be sized, and 5,800 loans is a guess; against training up to the window, the gap changes the hurdle model's Gini by -0.002 and its ROC AUC for a loss by -0.003 on average over the 9 windows (open question in REVIEW.md).
        Rows of one hidden entity recur from period to period: 68.0% to 72.4% of a window's loans have the entity's previous row, 61.2% to 63.5% inside the same window, 6.1% to 8.3% in the gap and 0.3% to 0.7% on the training side. None has the entity's next row on the training side, against 46.5% under a random 3-fold split.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "train_v2.csv", low_memory=False)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. Integers longer than int64 arrive as text: cast to float64, checking that no value is lost.
        text = [c for c in df.columns if df[c].dtype == object]
        missing_before = int(df[text].isna().sum().sum())
        df[text] = df[text].apply(pd.to_numeric, errors="coerce")
        assert int(df[text].isna().sum().sum()) == missing_before, "a text column held a non-number"
        # 2. The row id is the time order (the data page and the Kaggle admin, topic 6871).
        df = df.rename(columns={"id": "time_index"})
        # 3. Leak: running aggregates that include the loan's own period (LEAK-10).
        df = drop_columns(df, CURRENT_PERIOD_AGGREGATES)
        # 4. Constant columns and exact copies of an earlier column (CLEAN-5).
        features = [c for c in df.columns if c not in ("time_index", "loss")]
        constant, copies = _constant_and_copied_columns(df, features)
        assert (len(constant), len(copies)) == (11, 81), (len(constant), len(copies))  # the counts in the notes
        df = drop_columns(df, constant + copies)
        # 5. Leak: columns filled in after the previous loan's outcome, and own-period tails (LEAK-10). After step 4,
        # so the copies of f224, f254 and f264 are gone with them.
        df = drop_columns(df, PREVIOUS_LOSS_HINDSIGHT + OWN_PERIOD_TAILS)
        # 6. f466 is the one long-integer column read as uint64: float64 like the others, no value lost.
        assert df["f466"].astype("float64").nunique() == df["f466"].nunique()
        df["f466"] = df["f466"].astype("float64")
        # 7. Values beyond float32 as log10 (all positive; missing stays missing).
        for c in BEYOND_FLOAT32:
            assert (df[c].dropna() > 0).all(), c
            df[f"{c}_log10"] = np.log10(df[c])
        df = drop_columns(df, BEYOND_FLOAT32)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["f6", "f776", "f777", "f778"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        from scipy.stats import spearmanr
        from sklearn.metrics import roc_auc_score

        i, j = _period_links(raw)
        f274 = raw["f274"].to_numpy(dtype="float64")
        x = 2 * raw["f527"].to_numpy(dtype="float64") - (f274 - raw["f271"].to_numpy(dtype="float64"))
        own_change, previous_change = x[j] - f274[j], f274[j] - f274[i]
        loss = raw["loss"].to_numpy()[j] > 0
        rows = []
        for c in [*CURRENT_PERIOD_AGGREGATES, "f274"]:
            values = pd.to_numeric(raw[c], errors="coerce").to_numpy(dtype="float64")  # f534, f537 arrive as text
            change = values[j] - values[i]
            ok = ~np.isnan(change)
            auc = roc_auc_score(loss[ok], change[ok])
            rows.append(
                {
                    "column": c,
                    "Spearman with the own period's change of x": spearmanr(change[ok], own_change[ok])[0],
                    "Spearman with the previous period's change of x": spearmanr(change[ok], previous_change[ok])[0],
                    "ROC AUC of the change for a loss": max(auc, 1 - auc),
                }
            )
        table = pd.DataFrame(rows).set_index("column").round(3)

        # The previous loan's loss by how many loans earlier it was granted: a field filled in after the fact gives
        # it as well at short gaps as at long ones; history that arrives over time gives it better with distance.
        def auc_for_previous_loss(values: np.ndarray, rows_in: np.ndarray) -> float:
            ok = rows_in & ~np.isnan(values)
            auc = roc_auc_score(previous_loss[ok], values[ok])
            return max(auc, 1 - auc)

        previous_loss = raw["loss"].to_numpy()[i] > 0
        gap = j - i
        signals = {}
        for c in ["f221", "f278", "f615", "f617"]:
            values = pd.to_numeric(raw[c], errors="coerce").to_numpy(dtype="float64")
            signals[f"{c} level"] = values[j]
            signals[f"{c} change"] = values[j] - values[i]
        gap_rows = []
        for low, high in [(1, 10), (11, 100), (101, 1000), (1001, len(raw))]:
            rows_in = (gap >= low) & (gap <= high)
            gap_rows.append(
                {
                    "rows between the loans": f"{low:,}-{high:,}" if high < len(raw) else f"over {low - 1:,}",
                    "links": int(rows_in.sum()),
                    **{name: auc_for_previous_loss(values, rows_in) for name, values in signals.items()},
                }
            )
        gap_table = pd.DataFrame(gap_rows).set_index("rows between the loans").round(3)
        return [
            Decision(
                title="Running aggregates that include the loan's own period are dropped",
                why=(
                    f"On {len(j):,} links between a row and the same entity's row one period earlier, the change of "
                    "each column from the earlier row, against the change of the hidden value x in the row's own "
                    "period and in the previous one (f274 is x of the previous period, the lagged control). f527 and "
                    "f528 follow the own period and give the loss away. f529-f531, f534, f535 and f537 go by the "
                    "curator's call and f533 with them as one block, though their changes behave like those of the "
                    "shipped columns (which reach ROC AUC 0.595 at most for the row's own loss)."
                ),
                evidence=table,
            ),
            Decision(
                title="Columns filled in after the previous loan's outcome are dropped",
                why=(
                    "ROC AUC for the loss of the entity's previous loan, by how many loans earlier it was granted. "
                    "A loan granted 1-10 loans earlier cannot have run its term, yet f221's level gives its loss "
                    "away there as well as far back: f221 and 26 related columns, and f278 (whose change keeps its "
                    "signal at short gaps), were filled in after the fact and are dropped. f615 and f617 gain their "
                    "signal with distance, as history that arrives over time would, and stay with a note."
                ),
                evidence=gap_table,
            ),
        ]
