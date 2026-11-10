"""Train a model on a Data Foundry v2 container across every outer split, scored by the container's metric spec.

A v2 container (``format_version == 2``: the TabArena v0.2 collection, or one built locally from a ``dataset.py``)
says everything a benchmark needs:

* the splits, ``experiment_metadata.splits`` as ``{repeat: {fold: (train_idx, test_idx)}}``: never re-split or
  shuffle, they encode the regime (IID, temporal, grouped);
* the train budget, ``experiment_metadata.row_budget`` (a ``_1m`` version): its train sides keep every row they may
  use, all history of a temporal one, and ``subsample_train(container, repeat, fold)`` draws the rows a model fits
  on, at most ``row_budget.train`` of them, by the default sampler the container records
  (``experiment_metadata.train_sampling``: a random sample of the newest year of a temporal side, whole groups of a
  grouped one); without a budget it returns the train side whole;
* the features, ``feature_columns(container)``: no target, no group column, no scoring column (a metric input such
  as an era, never a feature);
* the training weight, ``sample_weight(container)`` (or ``None``): a scoring column every model is fitted with as each
  row's weight, never a feature, such as the years insured of a claims-per-year target; the metric weights the test
  rows by it too;
* the metric, ``task_metadata.objective_metric`` (its name, what it takes, its origin and reference), scored by
  ``scorer(container)``, which looks up the scoring columns' values by the test rows' index and reads class
  probabilities in the sorted order of the classes (scikit-learn's ``classes_``), or by name from a table whose
  columns are the class names; an ordered target's order is type information, never the column order;
* the feature types, from the dtypes: numeric, categorical, ordinal (an ordered categorical), ``datetime`` and
  ``string`` (free text), and the special features (``special_features(container)``: a molecule's SMILES column, a
  spectrum's group of columns).

Each type enters the model in the encoding the package recommends (``data_foundry.v2.encodings``): a special feature
by ``encode_special_feature`` (a SMILES as RDKit's descriptors and fingerprints, never as text; a spectrum by its
technique and state), a date by skrub's ``DatetimeEncoder`` (seconds since 1970 when skrub is not installed), text by
TF-IDF and a truncated SVD fitted on each split's training rows, an ordinal by its order. The model is scikit-learn's
histogram gradient boosting, which takes the unordered categoricals as they are. Swap in your own model and encodings;
keep the splits, the features and the scorer.

For the BeyondArena collection (format 1), see ``benchmark_on_beyond_arena.py``.

Run::

    python examples/benchmark_container.py <container folder>

Requires ``scikit-learn>=1.4``; RDKit (the ``build`` extra) for a SMILES feature, skrub (the ``encodings`` extra) for
the recommended date encoding.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.curation_container import CuratedContainer, feature_columns, sample_weight, special_features
from data_foundry.v2.encodings import encode_text_tfidf
from data_foundry.v2.metrics import scorer
from data_foundry.v2.splits import subsample_train
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor

MAX_CATEGORIES = 255
"""Histogram gradient boosting takes at most this many levels in a categorical; a wider one enters as its codes."""


def main(container_path: Path) -> list[float]:
    """Benchmark the v2 container at ``container_path``; return the score of every split."""
    container = CuratedContainer.load(container_path)
    if container.format_version < 2:
        msg = f"{container_path} is a format-{container.format_version} container; use benchmark_on_beyond_arena.py."
        raise SystemExit(msg)
    print(container.describe())
    print()
    return benchmark(container)


def benchmark(container: CuratedContainer) -> list[float]:
    """Every split of ``container``: fit on its training rows, score its test rows by the metric spec."""
    task = container.task_metadata
    spec = task.objective_metric
    target = task.target_column_name
    df, features = encoded_frame(container)
    text = [c for c in features if pd.api.types.is_string_dtype(df[c]) and not _categorical(df[c])]
    score = scorer(container)  # score(y_true, y_pred, row_index)
    classes = list(df[target].cat.categories) if task.problem_type != "regression" else None
    scoring = ", ".join(f"`{c.column}` ({c.role})" for c in task.scoring_columns) or "none"
    weight = sample_weight(container)  # the training weight, or None
    print(f"Metric: {spec.name} ({spec.origin}; takes {spec.prediction}; ", end="")
    print(f"{'higher' if spec.greater_is_better else 'lower'} is better); scoring columns: {scoring}")
    print(f"{len(features)} model inputs, {len(text)} text columns encoded per split", end="")
    print(f"; every model fitted with `{weight}` as the row weight\n" if weight else "\n")
    budget = container.experiment_metadata.row_budget
    if budget is not None:
        sampling = container.experiment_metadata.train_sampling
        print(f"Train budget: at most {budget.train:,} rows per fit, ", end="")
        print(f"sampled by `{sampling.default}` in units of {sampling.unit}\n")

    scores: list[float] = []
    for repeat_id, folds in container.experiment_metadata.splits.items():
        for fold_id, (train_idx, test_idx) in folds.items():
            train_idx = subsample_train(container, repeat_id, fold_id)  # noqa: PLW2901 - the train side within the budget
            x_train, x_test = df.iloc[train_idx][features], df.iloc[test_idx][features]
            x_train, x_test = _encode_text(x_train, x_test, text)
            y_train, y_test = df[target].iloc[train_idx], df[target].iloc[test_idx]
            if classes is None:
                model = HistGradientBoostingRegressor(categorical_features="from_dtype", random_state=42)
            else:
                model = HistGradientBoostingClassifier(categorical_features="from_dtype", random_state=42)
            # the training weight is the metric's row weight: a model fitted without it targets another quantity
            model.fit(x_train, y_train, sample_weight=None if weight is None else df[weight].iloc[train_idx])
            if spec.prediction == "proba":
                # A table with a column per class, named by the class: the scorer matches the columns by name, and
                # a fold whose training rows lack a class gets 0 for it. A plain array is read in the sorted order of
                # the classes (scikit-learn's `classes_`), also for an ordered target.
                y_pred = pd.DataFrame(model.predict_proba(x_test), columns=model.classes_)
                y_pred = y_pred.reindex(columns=classes, fill_value=0.0)
            else:
                y_pred = model.predict(x_test)
            value = score(y_test.to_numpy(), y_pred, test_idx)
            scores.append(value)
            print(f"  repeat {repeat_id}  fold {fold_id}:  {spec.name}={value:.4f}")
    print(f"\nMean {spec.name} over {len(scores)} splits: {np.mean(scores):.4f}  (std {np.std(scores):.4f})")
    return scores


def encoded_frame(container: CuratedContainer) -> tuple[pd.DataFrame, list[str]]:
    """The dataset with every feature in a form the model takes, and the names of the model's inputs.

    The encodings that need no fit (special features, dates, ordinals, wide categoricals) apply to all rows here;
    text is left as it is and encoded per split on its training rows (:func:`_encode_text`).
    """
    df = container.dataset.copy()
    features = feature_columns(container)
    special = special_features(container)
    if special:  # each in its recommended encoding, in place of its columns
        from data_foundry.v2.special import encode_special_feature  # noqa: PLC0415 - RDKit or scipy by kind

        before = list(df.columns)
        for feature in special:
            df = encode_special_feature(df, feature)
        replaced = {c for f in special for c in f.columns} - set(df.columns)
        features = [c for c in features if c not in replaced] + [c for c in df.columns if c not in before]
    out: list[str] = []
    for column in features:
        values = df[column]
        if isinstance(values.dtype, pd.CategoricalDtype) and (values.cat.ordered or _wide(values)):
            # an ordinal by its order; a categorical too wide for the model by its codes (missing stays missing)
            df[column] = values.cat.codes.astype(float).where(values.notna())
            out.append(column)
        elif pd.api.types.is_datetime64_any_dtype(values) or isinstance(values.dtype, pd.PeriodDtype):
            encoded = _encode_datetime(values)
            df = pd.concat([df.drop(columns=column), encoded], axis=1)
            out.extend(encoded.columns)
        elif pd.api.types.is_bool_dtype(values):
            df[column] = values.astype(float)
            out.append(column)
        elif pd.api.types.is_numeric_dtype(values) or _categorical(values) or pd.api.types.is_string_dtype(values):
            out.append(column)
        else:
            print(f"left out `{column}`: dtype {values.dtype} has no encoding here")
    return df, out


def _encode_datetime(values: pd.Series) -> pd.DataFrame:
    """Skrub's encoding of a date (the recommended one), or seconds since 1970 without skrub."""
    if isinstance(values.dtype, pd.PeriodDtype):
        values = values.dt.to_timestamp()
    try:
        from data_foundry.v2.encodings import encode_datetime  # noqa: PLC0415 - skrub is optional

        return encode_datetime(values, prefix=f"{values.name}_")
    except ImportError:
        if values.dt.tz is not None:
            values = values.dt.tz_convert("UTC").dt.tz_localize(None)
        seconds = (values - pd.Timestamp("1970-01-01")) / pd.Timedelta(seconds=1)
        return seconds.rename(f"{values.name}_seconds").to_frame()


def _encode_text(x_train: pd.DataFrame, x_test: pd.DataFrame, text: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Each text column as TF-IDF components fitted on this split's training rows, in place of the column."""
    for column in text:
        train, test = encode_text_tfidf(x_train[column], x_test[column], prefix=f"{column}_tfidf_")
        x_train = pd.concat([x_train.drop(columns=column), train], axis=1)
        x_test = pd.concat([x_test.drop(columns=column), test], axis=1)
    return x_train, x_test


def _categorical(values: pd.Series) -> bool:
    return isinstance(values.dtype, pd.CategoricalDtype)


def _wide(values: pd.Series) -> bool:
    return len(values.cat.categories) > MAX_CATEGORIES


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("container", type=Path, help="The container folder (format 2).")
    args = parser.parse_args()
    main(args.container)
