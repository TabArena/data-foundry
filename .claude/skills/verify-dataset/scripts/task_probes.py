"""Task probes for v2 datasets: is the task worth benchmarking, or empty, solved, or the same for every model?

Usage::

    python .claude/skills/verify-dataset/scripts/task_probes.py <unique_name> [<unique_name> ...]
        [--root datasets/_dev/tabarena-v0pt2]
    python .claude/skills/verify-dataset/scripts/task_probes.py --all [--built] [--jobs 8] [--out DIR]

On the shipped splits (IID folds, grouped folds or the newest temporal windows, so the probe follows the task's
regime): every split up to 30 for a dataset of at most 5,000 scored units (rows, or groups for a task scored per
group), else the first 5 (``--splits`` overrides both),
with untuned models:

* baselines: a dummy that predicts the train side's class shares (classification) or mean (regression); for a
  temporal task also a drift baseline, the same from the newest rows of the train side (as many as the test window
  holds, at most a fifth of the train side);
* three model families: a regularised linear model, a random forest and LightGBM (regression predictions are clipped
  to the train side's target range);
* the best single feature, chosen on each split's training side: of the five features LightGBM uses most there, the
  one that scores best alone on an inner hold-out of the train side (whole groups for a grouped task, the newest rows
  for a temporal one); it is then refitted on the train side and scored on the test side;
* the scores: ROC AUC (binary), macro ROC AUC and log loss (multiclass), R^2 and RMSE (regression), per row and,
  for a task scored per group (``Grouping(prediction_unit="group")`` with ``mean``, ``any`` or ``last``), per group;
* the smallest class of each test fold, in rows (or in groups for a task scored per group).

Every score is also a skill against the dummy, 0 for the dummy and 1 for a perfect model: ``2 AUC - 1`` (binary),
``1 - log loss / dummy log loss`` (multiclass), ``1 - MSE / dummy MSE`` (regression). The flags are questions for the
curator, not verdicts; how to answer each one: ``.claude/skills/verify-dataset/references/task_probes.md``.

* ``no_signal``: the best family's mean skill is not above twice its standard error (nor above 0.02);
* ``solved``: ROC AUC, macro ROC AUC or R^2 of at least 0.995;
* ``no_spread``: the best and the worst family differ by less than twice the standard error of their per-split
  difference (paired by split), or by less than 0.01;
* ``one_feature``: the single feature reaches 95% of the best family's skill, and leaves at most 1.25 times its
  remaining error (``1 - skill``): the models remove less than a fifth of what that feature leaves;
* ``drift_baseline``: for a temporal task, the drift baseline's loss (log loss, or squared error) is within 2% of
  the best family's;
* ``unstable``: the best family beats the dummy on fewer than 80% of the splits, or the standard error of its mean
  skill is above 0.05;
* ``few_minority``: for a binary task, a test fold holds fewer than 5 rows (or groups) of a class (a rare class of a
  multiclass task is the bundle check ``splits_test_minority_few``).

Group and target columns are not features. Text (string) columns enter as 16 TF-IDF + SVD components each, fitted on
the train side (``--no-text`` leaves them out); categoricals enter as codes and datetimes as numbers. Train and test
sides are capped at ``--max-rows`` random rows (whole groups for a task scored per group). ``--built`` reads the
container recorded in each ``README.md``'s build record instead of rebuilding the frame from the raw files. The
numbers are indicative (untuned models); a flag is checked against tuned methods before anyone acts on it
(``tuned_results.py``).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")

import lightgbm as lgb
import numpy as np
import pandas as pd
from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import as_column_list, resolve_warehouse_dir
from data_foundry.v2 import discover_datasets, read_report
from joblib import Parallel, delayed
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SOLVED = 0.995
"""ROC AUC, macro ROC AUC or R^2 from which a task counts as solved."""
MIN_SKILL = 0.02
"""A skill below this is no signal, whatever the noise."""
MIN_SPREAD = 0.01
"""A skill spread between the model families below this is no spread, whatever the noise."""
ONE_FEATURE_SHARE = 0.95
"""One feature carries the task when it reaches this share of the best family's skill ..."""
ONE_FEATURE_ROOM = 1.25
"""... and its remaining error is at most this multiple of the best family's."""
UNSTABLE_SHARE = 0.8
"""The best family has to beat the dummy on at least this share of the splits."""
UNSTABLE_SE = 0.05
"""A standard error of the best family's mean skill above this makes the comparison unstable."""
DRIFT_MARGIN = 1.02
"""The drift baseline is as good as the models when its loss is within this factor of the best family's."""
FEW_MINORITY = 5
"""A test fold with fewer rows (or groups) of a class than this cannot score that class."""
SMALL_UNITS = 5_000
"""Up to this many scored units (rows, or groups), every shipped split is probed (at most ``SMALL_SPLITS``)."""
SMALL_SPLITS = 30
DEFAULT_SPLITS = 5
N_SINGLE = 5
"""Single-feature candidates per split: the features LightGBM uses most on its train side."""
TEXT_COMPONENTS = 16
MAX_TEXT_COLUMNS = 30


def load(name: str, root: Path, *, built: bool) -> tuple[CuratedContainer, str]:
    """The container of ``name`` (the built one, or rebuilt from the definition) and where it came from."""
    if built:
        build = (read_report(root / name / "README.md") or {}).get("build") or {}
        if build.get("path"):
            return CuratedContainer.load(resolve_warehouse_dir() / build["path"]), "built"
    return discover_datasets(root)[name]().to_container(), "rebuilt"


def features(df: pd.DataFrame, drop: list[str]) -> tuple[pd.DataFrame, list[str], list[str]]:
    """Numeric model inputs (columns ``f0``, ``f1``, ...), their original names, and the text columns."""
    X = df.drop(columns=[c for c in drop if c in df.columns])
    text = list(X.select_dtypes(include=["string", "object"]).columns)
    X = X.drop(columns=text)
    for col in X.columns:
        if isinstance(X[col].dtype, pd.CategoricalDtype):
            X[col] = X[col].cat.codes.replace(-1, np.nan)
        elif pd.api.types.is_datetime64_any_dtype(X[col]):
            X[col] = X[col].astype("int64") // 10**9
        elif isinstance(X[col].dtype, pd.PeriodDtype):
            X[col] = X[col].dt.to_timestamp().astype("int64") // 10**9
    X = X.astype(float)
    names = list(X.columns)
    X = X.fillna(X.median()).fillna(0.0)
    X.columns = [f"f{i}" for i in range(X.shape[1])]
    return X, names, text


def encode_text(
    df: pd.DataFrame, text: list[str], train: np.ndarray, test: np.ndarray
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, list[str]]]:
    """Each text column as TF-IDF + SVD components fitted on the train rows; the column blocks by source column."""
    tr_parts, te_parts, blocks = [], [], {}
    for k, col in enumerate(text[:MAX_TEXT_COLUMNS]):
        values = df[col].astype("string").fillna("").to_numpy(dtype=object)
        try:
            vectorizer = TfidfVectorizer(max_features=20_000, min_df=2, sublinear_tf=True, dtype=np.float32)
            a_train = vectorizer.fit_transform(values[train])
        except ValueError:  # no term occurs twice: nothing to encode
            continue
        n = min(TEXT_COMPONENTS, a_train.shape[1] - 1)
        if n < 1:
            continue
        svd = TruncatedSVD(n_components=n, random_state=0)
        cols = [f"t{k}_{j}" for j in range(n)]
        tr_parts.append(pd.DataFrame(svd.fit_transform(a_train), columns=cols))
        te_parts.append(pd.DataFrame(svd.transform(vectorizer.transform(values[test])), columns=cols))
        blocks[col] = cols
    if not tr_parts:
        return pd.DataFrame(index=range(len(train))), pd.DataFrame(index=range(len(test))), {}
    return pd.concat(tr_parts, axis=1), pd.concat(te_parts, axis=1), blocks


def models(*, regression: bool, n_jobs: int) -> dict:
    """The three untuned model families."""
    if regression:
        return {
            "linear": lambda: make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
            "random_forest": lambda: RandomForestRegressor(
                n_estimators=200, min_samples_leaf=2, max_features="sqrt", n_jobs=n_jobs, random_state=0
            ),
            "lightgbm": lambda: lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, verbose=-1, n_jobs=n_jobs),
        }
    return {
        "linear": lambda: make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000)),
        "random_forest": lambda: RandomForestClassifier(
            n_estimators=200, min_samples_leaf=2, n_jobs=n_jobs, random_state=0
        ),
        "lightgbm": lambda: lgb.LGBMClassifier(n_estimators=300, learning_rate=0.05, verbose=-1, n_jobs=n_jobs),
    }


def predict(model, X_test: pd.DataFrame, n_classes: int) -> np.ndarray:
    """Class probabilities aligned to all classes, or values (``n_classes=0``)."""
    if not n_classes:
        return model.predict(X_test)
    out = np.zeros((len(X_test), n_classes))
    out[:, model.classes_] = model.predict_proba(X_test)
    return out


def scores(y: np.ndarray, pred: np.ndarray, reference: np.ndarray, n_classes: int) -> dict[str, float]:
    """The scores of ``pred`` and its skill against the constant ``reference`` (the dummy's prediction)."""
    if not n_classes:
        mse, dummy = float(np.mean((y - pred) ** 2)), float(np.mean((y - reference) ** 2))
        total = float(np.mean((y - y.mean()) ** 2))
        return {
            "rmse": mse**0.5,
            "r2": 1 - mse / total if total else float("nan"),
            "skill": 1 - mse / dummy if dummy else float("nan"),
        }
    labels = list(range(n_classes))
    p = np.clip(pred, 1e-12, 1)
    p = np.round(p / p.sum(axis=1, keepdims=True), 12)  # a constant averaged per group stays a constant
    q = np.clip(np.broadcast_to(reference, p.shape), 1e-12, 1)
    q = q / q.sum(axis=1, keepdims=True)
    present = np.unique(y)
    if n_classes == 2:  # binary
        auc = float(roc_auc_score(y, p[:, 1])) if len(present) == 2 else float("nan")
        return {"auc": auc, "log_loss": float(log_loss(y, p, labels=labels)), "skill": 2 * auc - 1}
    ll, ll_dummy = float(log_loss(y, p, labels=labels)), float(log_loss(y, q, labels=labels))
    auc = float("nan")
    if len(present) > 2:
        sub = p[:, present] / p[:, present].sum(axis=1, keepdims=True)
        auc = float(roc_auc_score(y, sub, multi_class="ovr", labels=list(present)))
    return {"macro_auc": auc, "log_loss": ll, "skill": 1 - ll / ll_dummy if ll_dummy else float("nan")}


def by_group(frame: pd.DataFrame, aggregation: str, n_classes: int) -> tuple[np.ndarray, np.ndarray]:
    """Group-level predictions and labels from row-level ones (``frame``: predictions, ``_y``, ``_g``, ``_t``)."""
    cols = [c for c in frame.columns if not str(c).startswith("_")]
    if aggregation == "last":
        last = frame.sort_values("_t", kind="stable").groupby("_g", sort=True).tail(1).sort_values("_g")
        return last[cols].to_numpy(), last["_y"].to_numpy()
    grouped = frame.groupby("_g", sort=True)
    if aggregation == "any":
        pred = grouped[cols].max().to_numpy()
        if n_classes == 2:  # P(negative) as the complement of the max P(positive)
            pred[:, 0] = 1 - pred[:, 1]
        return pred, grouped["_y"].max().to_numpy()
    return grouped[cols].mean().to_numpy(), grouped["_y"].first().to_numpy()


def inner_holdout(train: np.ndarray, groups: np.ndarray | None, times: np.ndarray | None, seed: int) -> tuple:
    """Positions (within ``train``) of an inner train and validation part: whole groups, the newest rows, or random."""
    n = len(train)
    if groups is not None:
        unique = np.unique(groups[train])
        held = np.random.default_rng(seed).permutation(unique)[: max(1, len(unique) // 4)]
        val = np.isin(groups[train], held)
    elif times is not None:
        val = np.zeros(n, dtype=bool)
        val[np.argsort(times[train], kind="stable")[-max(1, n // 4) :]] = True
    else:
        val = np.zeros(n, dtype=bool)
        val[np.random.default_rng(seed).permutation(n)[: max(1, n // 4)]] = True
    return np.flatnonzero(~val), np.flatnonzero(val)


def probe(name: str, root: Path, *, built: bool, n_splits: int | None, max_rows: int, n_jobs: int, text: bool) -> dict:  # noqa: C901, PLR0912
    """Run the probes of the module docstring on one dataset and return the numbers and flags."""
    started = time.time()
    container, origin = load(name, root, built=built)
    task, grouping = container.task_metadata, container.grouping
    df = container.dataset
    regression = task.problem_type == "regression"
    group_cols = as_column_list(grouping.on) if grouping is not None else []
    X, names, text_cols = features(df, [task.target_column_name, *group_cols])
    if not text:
        text_cols = []
    target = df[task.target_column_name]
    if regression:
        y, n_classes = target.to_numpy(dtype=float), 0
    else:
        y, classes = pd.factorize(target, sort=True)
        n_classes = len(classes)
    unit = "row"
    aggregation = None
    if grouping is not None and grouping.prediction_unit == "group":
        aggregation = grouping.aggregation
        unit = "group" if aggregation in ("mean", "any", "last") else "row"
    groups = df.groupby(group_cols, sort=False, observed=True).ngroup().to_numpy() if group_cols else None
    order = df[grouping.time_on].to_numpy() if aggregation == "last" else None
    time_on = task.time_on
    times = df[time_on].to_numpy() if time_on is not None else None

    flat = [(tr, te) for folds in container.experiment_metadata.splits.values() for tr, te in folds.values()]
    if n_splits is None:
        units = len(np.unique(groups)) if unit == "group" else len(df)
        n_splits = min(len(flat), SMALL_SPLITS) if units <= SMALL_UNITS else DEFAULT_SPLITS
    rng = np.random.default_rng(0)
    pairs = []
    for split_train, split_test in flat[:n_splits]:
        full_train, test = np.asarray(split_train), np.asarray(split_test)
        train = full_train
        if len(train) > max_rows:
            train = np.sort(rng.choice(train, max_rows, replace=False))
        if len(test) > max_rows and unit == "group":
            chosen = rng.permutation(np.unique(groups[test]))
            sizes = pd.Series(groups[test]).value_counts().reindex(chosen).to_numpy()
            test = test[np.isin(groups[test], chosen[: max(1, np.searchsorted(np.cumsum(sizes), max_rows))])]
        elif len(test) > max_rows:
            test = np.sort(rng.choice(test, max_rows, replace=False))
        pairs.append((train, test, full_train))

    results: dict[str, list[dict]] = {}
    candidates = models(regression=regression, n_jobs=n_jobs)
    chosen_single: list[str] = []
    minority: list[int] = []
    numeric_blocks = {names[i]: [f"f{i}"] for i in range(len(names))}

    def reference_of(rows: np.ndarray) -> np.ndarray:
        if regression:
            return np.array([y[rows].mean()])
        return (np.bincount(y[rows], minlength=n_classes) / len(rows))[None, :]

    def record(key: str, y_te: np.ndarray, pred: np.ndarray, ref: np.ndarray, test: np.ndarray) -> None:
        if unit == "group":
            frame = pd.DataFrame(pred if n_classes else pred[:, None]).assign(_y=y_te, _g=groups[test])
            if order is not None:
                frame["_t"] = order[test]
            refs = np.broadcast_to(ref, (len(test), max(n_classes, 1)))
            gp, gy = by_group(frame, aggregation, n_classes)
            ref_frame = pd.DataFrame(refs.copy()).assign(_y=y_te, _g=groups[test])
            if order is not None:
                ref_frame["_t"] = order[test]
            gref, _ = by_group(ref_frame, aggregation, n_classes)
            pred, y_te, ref = (gp if n_classes else gp[:, 0]), gy, (gref if n_classes else gref[:, 0])
        results.setdefault(key, []).append(scores(y_te, pred, ref, n_classes))

    def make_single() -> lgb.LGBMModel:
        return (lgb.LGBMRegressor if regression else lgb.LGBMClassifier)(n_estimators=200, verbose=-1, n_jobs=n_jobs)

    for i, (train, test, full_train) in enumerate(pairs):
        ref = reference_of(train)
        y_tr, y_te = y[train], y[test]
        X_tr, X_te = X.iloc[train].reset_index(drop=True), X.iloc[test].reset_index(drop=True)
        text_blocks: dict[str, list[str]] = {}
        if text_cols:
            t_tr, t_te, text_blocks = encode_text(df, text_cols, train, test)
            X_tr, X_te = pd.concat([X_tr, t_tr], axis=1), pd.concat([X_te, t_te], axis=1)
        blocks = numeric_blocks | text_blocks
        if n_classes:
            if unit == "group":
                labels = pd.Series(y_te).groupby(groups[test]).max() if aggregation == "any" else None
                if labels is None:
                    frame = pd.DataFrame({"_y": y_te, "_g": groups[test]})
                    labels = frame.groupby("_g")["_y"].first()
                minority.append(int(np.bincount(labels.to_numpy(), minlength=n_classes).min()))
            else:
                minority.append(int(np.bincount(y_te, minlength=n_classes).min()))
        dummy_pred = np.broadcast_to(ref, (len(test), max(n_classes, 1))).copy()
        record("dummy", y_te, dummy_pred if n_classes else dummy_pred[:, 0], ref, test)
        if times is not None:
            by_time = full_train[np.argsort(times[full_train], kind="stable")]
            newest = by_time[-max(1, min(len(test), len(by_time) // 5)) :]
            drift = np.broadcast_to(reference_of(newest), (len(test), max(n_classes, 1))).copy()
            record("drift", y_te, drift if n_classes else drift[:, 0], ref, test)
        lightgbm = None
        for key, make in candidates.items():
            model = make().fit(X_tr, y_tr)
            pred = predict(model, X_te, n_classes)
            if regression:
                pred = np.clip(pred, y_tr.min(), y_tr.max())
            record(key, y_te, pred, ref, test)
            if key == "lightgbm":
                lightgbm = model

        # The single feature: chosen on this split's training side only.
        if lightgbm is not None and len(blocks) > 1:
            gain = pd.Series(lightgbm.booster_.feature_importance(importance_type="gain"), index=X_tr.columns)
            ranked = sorted(blocks, key=lambda b: -float(gain[blocks[b]].sum()))[:N_SINGLE]
            inner_tr, inner_va = inner_holdout(train, groups, times, seed=i)
            best_block, best_inner = ranked[0], -np.inf
            if len(inner_tr) and len(inner_va):
                inner_ref = reference_of(train[inner_tr])
                for block in ranked:
                    cols = blocks[block]
                    model = make_single().fit(X_tr.iloc[inner_tr][cols], y_tr[inner_tr])
                    inner = scores(
                        y_tr[inner_va], predict(model, X_tr.iloc[inner_va][cols], n_classes), inner_ref, n_classes
                    )
                    if np.isfinite(inner["skill"]) and inner["skill"] > best_inner:
                        best_block, best_inner = block, inner["skill"]
            cols = blocks[best_block]
            model = make_single().fit(X_tr[cols], y_tr)
            record("single_feature", y_te, predict(model, X_te[cols], n_classes), ref, test)
            chosen_single.append(best_block)

    def summary(key: str) -> dict[str, float]:
        frame = pd.DataFrame(results[key])
        out = {f"{k}_mean": float(frame[k].mean()) for k in frame.columns}
        out |= {f"{k}_std": float(frame[k].std(ddof=0)) for k in frame.columns}
        return out

    table = {key: summary(key) for key in results}
    family = [k for k in candidates if k in table]
    best = max(family, key=lambda k: np.nan_to_num(table[k]["skill_mean"], nan=-np.inf))
    best_skill = pd.Series([r["skill"] for r in results[best]])
    se = float(best_skill.std(ddof=1) / np.sqrt(len(best_skill))) if len(best_skill) > 1 else 0.0
    above = float((best_skill > 0).mean())
    flags = []
    if not best_skill.mean() > max(2 * se, MIN_SKILL):
        flags.append("no_signal")
    solved_key = "r2" if regression else ("auc" if n_classes == 2 else "macro_auc")
    if table[best].get(f"{solved_key}_mean", 0) >= SOLVED:
        flags.append("solved")
    if "no_signal" not in flags:
        skills = pd.DataFrame({k: [r["skill"] for r in results[k]] for k in family})
        top, bottom = skills.mean().idxmax(), skills.mean().idxmin()
        diff = skills[top] - skills[bottom]
        paired_se = float(diff.std(ddof=1) / np.sqrt(len(diff))) if len(diff) > 1 else 0.0
        spread = float(diff.mean())
        if not spread > max(2 * paired_se, MIN_SPREAD):
            flags.append("no_spread")
        table["spread"] = {"best_minus_worst": spread, "paired_se": paired_se, "best": top, "worst": bottom}
    single_skill = table.get("single_feature", {}).get("skill_mean")
    if (
        single_skill is not None
        and best_skill.mean() >= 0.1
        and single_skill >= ONE_FEATURE_SHARE * best_skill.mean()
        and (1 - single_skill) <= ONE_FEATURE_ROOM * (1 - best_skill.mean())
    ):
        flags.append("one_feature")
    if "drift" in table:
        loss = "log_loss" if n_classes else "rmse"
        best_loss = min(table[k][f"{loss}_mean"] for k in family)
        drift_loss = table["drift"][f"{loss}_mean"]
        if not n_classes:  # compare squared errors
            best_loss, drift_loss = best_loss**2, drift_loss**2
        if drift_loss <= DRIFT_MARGIN * best_loss:
            flags.append("drift_baseline")
    if above < UNSTABLE_SHARE or se > UNSTABLE_SE:
        flags.append("unstable")
    if n_classes == 2 and minority and min(minority) < FEW_MINORITY:
        flags.append("few_minority")
    counts = pd.Series(chosen_single).value_counts()
    return {
        "name": name,
        "origin": origin,
        "regime": task.split_regime,
        "problem_type": task.problem_type,
        "unit": unit if aggregation is None else f"{unit} ({aggregation})",
        "rows": len(df),
        "features": X.shape[1],
        "text_columns": len(text_cols),
        "splits_probed": len(pairs),
        "splits_shipped": len(flat),
        "scores": table,
        "best": best,
        "best_skill_se": se,
        "best_beats_dummy_share": above,
        "single_feature": {"skill": single_skill, "chosen": {str(k): int(v) for k, v in counts.items()}},
        "smallest_class_per_test_fold": min(minority) if minority else None,
        "flags": flags,
        "seconds": round(time.time() - started),
    }


def render(result: dict) -> str:
    """A short text report of one dataset's probes."""
    if "error" in result:
        return f"{result['name']}: CRASH {result['error']}"
    t = result["scores"]
    keys = [k for k in ("auc", "macro_auc", "log_loss", "r2", "rmse") if f"{k}_mean" in t["dummy"]]
    head = (
        f"{result['name']} ({result['regime']}, {result['problem_type']}, unit {result['unit']}, {result['origin']}): "
        f"{result['rows']:,} rows, {result['features']} features"
        + (f" + {result['text_columns']} text columns" if result["text_columns"] else "")
        + f", {result['splits_probed']} of {result['splits_shipped']} splits, {result['seconds']} s"
    )
    lines = [head]
    for key in ["dummy", "drift", "linear", "random_forest", "lightgbm", "single_feature"]:
        if key in t:
            cells = ", ".join(f"{k} {t[key][f'{k}_mean']:.3f}" for k in keys)
            lines.append(f"  {key:>14}: skill {t[key]['skill_mean']:+.3f} +- {t[key]['skill_std']:.3f} | {cells}")
    lines.append(
        f"  best family {result['best']}: beats the dummy on {result['best_beats_dummy_share']:.0%} of the splits, "
        f"standard error of its mean skill {result['best_skill_se']:.3f}"
    )
    if "spread" in t:
        s = t["spread"]
        lines.append(
            f"  spread {s['best']} - {s['worst']}: {s['best_minus_worst']:+.3f} (paired SE {s['paired_se']:.3f})"
        )
    if result["single_feature"]["chosen"]:
        chosen = ", ".join(f"{k!r} {v}x" for k, v in result["single_feature"]["chosen"].items())
        lines.append(f"  single feature chosen per split: {chosen}")
    if result["smallest_class_per_test_fold"] is not None:
        what = "groups" if result["unit"].startswith("group") else "rows"
        lines.append(f"  smallest class in a test fold: {result['smallest_class_per_test_fold']} {what}")
    lines.append(f"  flags: {', '.join(result['flags']) or 'none'}")
    return "\n".join(lines)


def _safe_probe(name: str, root: Path, **kwargs) -> dict:
    try:
        return probe(name, root, **kwargs)
    except Exception as error:  # noqa: BLE001 - one crash must not stop a sweep
        return {"name": name, "error": f"{type(error).__name__}: {error}", "traceback": traceback.format_exc()}


def main(argv: list[str] | None = None) -> int:
    """Probe the datasets; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--all", action="store_true", help="Probe every definition under --root.")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--built", action="store_true", help="Read the built containers (README build record).")
    parser.add_argument("--splits", type=int, help="Splits to probe (default: up to 30 for small data, else 5).")
    parser.add_argument("--max-rows", type=int, default=50_000)
    parser.add_argument("--no-text", action="store_true", help="Leave text columns out instead of encoding them.")
    parser.add_argument("--n-jobs", type=int, default=8, help="Threads per model.")
    parser.add_argument("--jobs", type=int, default=1, help="Datasets probed in parallel.")
    parser.add_argument("--out", type=Path, help="Write one JSON per dataset and summary.md here.")
    args = parser.parse_args(argv)

    names = sorted(discover_datasets(args.root)) if args.all else args.names
    if not names:
        parser.error("name at least one dataset, or pass --all")
    kwargs = {
        "built": args.built,
        "n_splits": args.splits,
        "max_rows": args.max_rows,
        "n_jobs": args.n_jobs,
        "text": not args.no_text,
    }
    results = Parallel(n_jobs=args.jobs)(delayed(_safe_probe)(n, args.root, **kwargs) for n in names)
    for result in results:
        print(render(result))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for result in results:
            (args.out / f"{result['name']}.json").write_text(json.dumps(result, indent=1, default=str))
        rows = [
            f"| `{r['name']}` | {r.get('regime', '')} | {r.get('unit', '')} | {r.get('best', '')} | "
            + (
                f"{r['scores'][r['best']]['skill_mean']:+.3f} | {', '.join(r['flags']) or ''} |"
                if "error" not in r
                else f" | CRASH: {r['error'][:80]} |"
            )
            for r in results
        ]
        header = "| dataset | regime | unit | best model | best skill | flags |\n|---|---|---|---|---|---|\n"
        (args.out / "summary.md").write_text(header + "\n".join(rows) + "\n")
    return 1 if any("error" in r for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
