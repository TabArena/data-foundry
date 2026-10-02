"""Task probes for v2 datasets: is the task worth benchmarking, or empty, solved, or the same for every model?

Usage::

    python .claude/skills/verify-dataset/scripts/task_probes.py <unique_name> [<unique_name> ...] [--root datasets/_dev/tabarena-v0pt2]
    python .claude/skills/verify-dataset/scripts/task_probes.py --all [--built] [--jobs 8] [--out DIR]

For each dataset, on its first ``--splits`` shipped splits (IID folds, grouped folds or the newest temporal windows,
so the probe follows the task's regime) and with untuned models:

* baselines: a dummy that predicts the train side's class shares (classification) or mean (regression); for a
  temporal regression or multiclass task also a drift baseline, the same from the newest fifth of the train side
  (a constant cannot rank the rows of a binary task, so it has no drift baseline);
* three model families: a regularised linear model, a random forest and LightGBM (regression predictions are clipped
  to the train side's target range);
* the best single feature: LightGBM on each of the five features LightGBM uses most, alone;
* the scores: ROC AUC (binary), macro ROC AUC and log loss (multiclass), R^2 and RMSE (regression), per row and,
  for a task scored per group (``Grouping(prediction_unit="group")`` with ``mean``, ``any`` or ``last``), per group.

Every score is also a skill against the dummy, 0 for the dummy and 1 for a perfect model: ``2 AUC - 1`` (binary),
``1 - log loss / dummy log loss`` (multiclass), ``1 - MSE / dummy MSE`` (regression). The flags, for the curator to
resolve with criterion 4C of the curation guidelines (``Trivial``):

* ``no_signal``: no model beats the dummy by more than the noise over the splits;
* ``solved``: a model is near perfect (ROC AUC, macro ROC AUC or R^2 at least 0.995): no room to rank methods;
* ``no_spread``: the mean skills of the three model families lie within twice their typical standard error (the
  median over the families) or within 0.01;
* ``one_feature``: one feature alone reaches at least 95% of the best model's skill (a leak or a lookup? run
  ``.claude/skills/verify-dataset/scripts/leak_probes.py``);
* ``drift_baseline``: for a temporal task, the drift baseline is as good as the best model;
* ``unstable``: the best model's skill varies by more than 0.1 (standard deviation) over the splits.

Group, target and string columns are not features (the report counts the string columns left out); categoricals
enter as codes and datetimes as numbers. Train and test sides are capped at ``--max-rows`` random rows (whole groups
for a task scored per group). ``--built`` reads the container recorded in each ``README.md``'s build record instead
of rebuilding the frame from the raw files. The numbers are indicative (untuned models, a few splits); the curator
decides.
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
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
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
"""One feature with this share of the best model's skill carries the task."""
UNSTABLE_STD = 0.1
"""A standard deviation of the best skill over the splits above this makes the comparison unstable."""
DRIFT_SHARE = 0.2
"""The drift baseline uses the newest fifth of the train side."""
N_SINGLE = 5
"""Single features probed: the ones LightGBM uses most on the first split."""


def load(name: str, root: Path, *, built: bool) -> tuple[CuratedContainer, str]:
    """The container of ``name`` (the built one, or rebuilt from the definition) and where it came from."""
    if built:
        build = (read_report(root / name / "README.md") or {}).get("build") or {}
        if build.get("path"):
            return CuratedContainer.load(resolve_warehouse_dir() / build["path"]), "built"
    return discover_datasets(root)[name]().to_container(), "rebuilt"


def features(df: pd.DataFrame, drop: list[str]) -> tuple[pd.DataFrame, list[str], int]:
    """Numeric model inputs, their original names, and the number of string columns left out."""
    X = df.drop(columns=[c for c in drop if c in df.columns])
    strings = X.select_dtypes(include=["string", "object"]).shape[1]
    X = X.select_dtypes(exclude=["string", "object"])
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
    return X, names, strings


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


def probe(name: str, root: Path, *, built: bool, n_splits: int, max_rows: int, n_jobs: int) -> dict:  # noqa: C901, PLR0912
    """Run the probes of the module docstring on one dataset and return the numbers and flags."""
    started = time.time()
    container, origin = load(name, root, built=built)
    task, grouping = container.task_metadata, container.grouping
    df = container.dataset
    regression = task.problem_type == "regression"
    group_cols = as_column_list(grouping.on) if grouping is not None else []
    X, names, n_strings = features(df, [task.target_column_name, *group_cols])
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

    rng = np.random.default_rng(0)
    flat = [(tr, te) for folds in container.experiment_metadata.splits.values() for tr, te in folds.values()]
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
    first_importance = None
    candidates = models(regression=regression, n_jobs=n_jobs)

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

    for i, (train, test, full_train) in enumerate(pairs):
        ref = reference_of(train)
        y_te = y[test]
        dummy_pred = np.broadcast_to(ref, (len(test), max(n_classes, 1))).copy()
        record("dummy", y_te, dummy_pred if n_classes else dummy_pred[:, 0], ref, test)
        if time_on is not None and n_classes != 2:
            by_time = full_train[np.argsort(df[time_on].to_numpy()[full_train], kind="stable")]
            newest = by_time[int(len(by_time) * (1 - DRIFT_SHARE)) :]
            drift = np.broadcast_to(reference_of(newest), (len(test), max(n_classes, 1))).copy()
            record("drift", y_te, drift if n_classes else drift[:, 0], ref, test)
        for key, make in candidates.items():
            model = make().fit(X.iloc[train], y[train])
            pred = predict(model, X.iloc[test], n_classes)
            if regression:
                pred = np.clip(pred, y[train].min(), y[train].max())
            record(key, y_te, pred, ref, test)
            if key == "lightgbm" and i == 0:
                first_importance = model.booster_.feature_importance(importance_type="gain")

    single: dict[str, float] = {}
    if first_importance is not None and X.shape[1] > 1:
        top = np.argsort(first_importance)[::-1][: min(N_SINGLE, X.shape[1])]
        for j in top:
            col = X.columns[j]
            skills = []
            for train, test, _full in pairs:
                model = (lgb.LGBMRegressor if regression else lgb.LGBMClassifier)(
                    n_estimators=200, verbose=-1, n_jobs=n_jobs
                ).fit(X.iloc[train][[col]], y[train])
                ref = reference_of(train)
                pred = predict(model, X.iloc[test][[col]], n_classes)
                before = len(results.get("_single", []))
                record("_single", y[test], pred, ref, test)
                skills.append(results["_single"].pop(before)["skill"])
            single[names[j]] = float(np.nanmean(skills))
        results.pop("_single", None)

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
    flags = []
    if not best_skill.mean() > max(2 * se, MIN_SKILL):
        flags.append("no_signal")
    solved_key = "r2" if regression else ("auc" if n_classes == 2 else "macro_auc")
    if table[best].get(f"{solved_key}_mean", 0) >= SOLVED:
        flags.append("solved")
    if "no_signal" not in flags:
        skills = pd.DataFrame({k: [r["skill"] for r in results[k]] for k in family})
        means = skills.mean()
        typical_se = float((skills.std(ddof=1) / np.sqrt(len(skills))).median()) if len(skills) > 1 else 0.0
        spread = float(means.max() - means.min())
        if not spread > max(2 * typical_se, MIN_SPREAD):
            flags.append("no_spread")
        table["spread"] = {"best_minus_worst": spread, "typical_se": typical_se}
    if single and best_skill.mean() >= 0.1 and max(single.values()) >= ONE_FEATURE_SHARE * best_skill.mean():
        flags.append("one_feature")
    if "drift" in table and table["drift"]["skill_mean"] >= best_skill.mean() - 2 * se:
        flags.append("drift_baseline")
    if float(best_skill.std(ddof=0)) > UNSTABLE_STD:
        flags.append("unstable")
    return {
        "name": name,
        "origin": origin,
        "regime": task.split_regime,
        "problem_type": task.problem_type,
        "unit": unit if aggregation is None else f"{unit} ({aggregation})",
        "rows": len(df),
        "features": X.shape[1],
        "string_columns_left_out": n_strings,
        "splits_probed": len(pairs),
        "scores": table,
        "best": best,
        "best_single_features": dict(sorted(single.items(), key=lambda kv: -kv[1])),
        "flags": flags,
        "seconds": round(time.time() - started),
    }


def render(result: dict) -> str:
    """A short text report of one dataset's probes."""
    if "error" in result:
        return f"{result['name']}: CRASH {result['error']}"
    t = result["scores"]
    keys = [k for k in ("auc", "macro_auc", "log_loss", "r2", "rmse") if f"{k}_mean" in t["dummy"]]
    lines = [
        f"{result['name']} ({result['regime']}, {result['problem_type']}, unit {result['unit']}, {result['origin']}): "
        f"{result['rows']:,} rows, {result['features']} features"
        + (
            f" (+{result['string_columns_left_out']} string columns left out)"
            if result["string_columns_left_out"]
            else ""
        )
        + f", {result['splits_probed']} splits, {result['seconds']} s"
    ]
    for key in ["dummy", "drift", "linear", "random_forest", "lightgbm"]:
        if key in t:
            cells = ", ".join(f"{k} {t[key][f'{k}_mean']:.3f}" for k in keys)
            lines.append(f"  {key:>13}: skill {t[key]['skill_mean']:+.3f} +- {t[key]['skill_std']:.3f} | {cells}")
    if result["best_single_features"]:
        col, skill = next(iter(result["best_single_features"].items()))
        lines.append(f"  best single feature: {col!r} skill {skill:+.3f}")
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
    parser.add_argument("--splits", type=int, default=5)
    parser.add_argument("--max-rows", type=int, default=50_000)
    parser.add_argument("--n-jobs", type=int, default=8, help="Threads per model.")
    parser.add_argument("--jobs", type=int, default=1, help="Datasets probed in parallel.")
    parser.add_argument("--out", type=Path, help="Write one JSON per dataset and summary.md here.")
    args = parser.parse_args(argv)

    names = sorted(discover_datasets(args.root)) if args.all else args.names
    if not names:
        parser.error("name at least one dataset, or pass --all")
    kwargs = {"built": args.built, "n_splits": args.splits, "max_rows": args.max_rows, "n_jobs": args.n_jobs}
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
