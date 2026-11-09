"""A v2 dataset as the plain inputs of the probe library: the Data Foundry side of the probe scripts.

The probes in ``.claude/skills/knowledge-curation/scripts/curation_probes/`` take a pandas frame, its target and
problem type, the group and time columns and the splits; this module reads them from a v2 definition under a root
folder: from the definition's own frame and split plan (rebuilt from the raw files), or from a container (the built
one recorded in the definition's ``README.md``, or one rebuilt from the definition).

The scoring columns (``task.scoring_columns``: the inputs of the metric, such as Numerai's ``era``) are never model
inputs, so they are dropped from the frame the probes see, unless one is also the target, a group column or the time
column, which the probes take by name. ``ProbeInput.scoring_cols`` lists the ones dropped.

The task's training weight (``sample_weight``: a scoring column of role ``weight``, such as the years insured of a
claims-per-year target) leaves ``df`` with them; ``ProbeInput.weights`` holds its values, row by row of ``df``, so the
probes fit every model with it, and ``ProbeInput.weight_column`` names it. ``ProbeInput.metric`` is the declared
metric (the spec), and ``ProbeInput.scoring`` the values of every scoring column, row by row of ``df``:
``metric_inputs(rows)`` gives the metric's inputs by role (``data_foundry.v2.metrics.score(spec, y, p, **inputs)``),
and ``declared_metric()`` the metric as the probe library takes it (``curation_probes.weights``), scored as the
benchmark scores it.

A special feature (``task.special_features``) enters the probes in its recommended encoding
(``data_foundry.v2.special.encode_special_feature``), as a benchmark would give it to a model: a SMILES column as its
descriptor and fingerprint columns (``<column>__rdkit_<name>``, ``<column>__maccs_<i>``, ``<column>__ecfp4_<i>``),
never as text; a spectrum's columns with the encoded values. ``encode_special=False`` keeps the values as shipped (the
blind reviewer's clean room). ``ProbeInput.special_features`` lists them by name.

With ``raw=True``, ``from_definition`` also gives the raw state: ``ProbeInput.raw``, the table ``_load_raw`` returns
(in source order, before ``_clean``), and ``ProbeInput.raw_rows``, the raw position of each row of ``df`` (the lineage
of ``process(lineage=True)``), or None when the rows cannot be traced (``ProbeInput.raw_note`` says why). The probes of
the raw state (``leak_probes.py --raw``) read row order, the rows ``_clean`` removed, the columns it dropped and the
copies before deduplication from them.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd
from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import as_column_list, resolve_warehouse_dir
from data_foundry.v2 import discover_datasets, load_definition, read_report
from data_foundry.v2.metrics import row_weight_column, scorer

if TYPE_CHECKING:
    from data_foundry.schema import Grouping
    from data_foundry.v2 import AbstractCuratedDataset


@dataclass
class ProbeInput:
    """One dataset as the probes take it.

    Attributes:
        df: The rows, with the target, group and time columns.
        target: The target column.
        problem_type: ``regression``, ``binary_classification`` or ``multiclass_classification``.
        regime: The task's split regime (``iid``, ``grouped_non_iid`` or ``temporal_non_iid``).
        splits: The shipped splits, ``{repeat: {fold: (train_idx, test_idx)}}``.
        grouping: The task's grouping, or None for an IID or temporal task.
        time_on: The time column of a temporal task.
        origin: ``built`` (the container of the README build record), ``rebuilt`` (a container rebuilt from the
            definition) or ``definition`` (the definition's frame and split plan, no container).
        scoring_cols: The scoring columns dropped from ``df`` (metric inputs, never features).
        special_features: The task's special features by name, encoded in ``df`` unless loaded with
            ``encode_special=False``.
        feature_cols: The exact model inputs (after special-feature encoding): no target, group or scoring
            column, even when a scoring column stays in ``df`` as the time key.
            None for manually constructed legacy inputs.
        raw: With ``from_definition(..., raw=True)``: the raw table in source order (``_load_raw``), or None when the
            raw data is not one table.
        raw_rows: The raw position of each row of ``df``, or None when the rows cannot be traced.
        raw_note: How the rows were traced, or why not.
        weights: The task's training weight, one value per row of ``df``, or None: every model is fitted with it as
            the row weight. Its column is a scoring column, never in ``df``.
        weight_column: The training weight's column, or None.
        metric: The declared metric (the ``objective_metric`` spec), or None (a format-1 container).
        scoring: The values of every scoring column, row by row of ``df`` (index 0 to n - 1), or None.
    """

    df: pd.DataFrame
    target: str
    problem_type: str
    regime: str
    splits: dict[Any, dict[Any, tuple]]
    grouping: Grouping | None
    time_on: str | None
    origin: str
    scoring_cols: tuple[str, ...] = ()
    special_features: tuple[str, ...] = ()
    feature_cols: tuple[str, ...] | None = None
    raw: pd.DataFrame | None = None
    raw_rows: np.ndarray | None = None
    raw_note: str = ""
    weights: np.ndarray | None = None
    weight_column: str | None = None
    metric: Any = None
    scoring: pd.DataFrame | None = None

    @property
    def group_cols(self) -> list[str]:
        """The group columns (none for an IID or temporal task)."""
        return as_column_list(self.grouping.on) if self.grouping is not None else []

    def flat_splits(self) -> list[tuple]:
        """Every split as ``(train_idx, test_idx)``, repeat by repeat."""
        return [(tr, te) for folds in self.splits.values() for tr, te in folds.values()]

    def repeats(self) -> list[list[tuple]]:
        """The ``(train_idx, test_idx)`` folds of each repeat, by repeat number."""
        return [list(self.splits[r].values()) for r in sorted(self.splits)]

    def metric_inputs(self, rows: Any) -> dict[str, np.ndarray]:
        """The declared metric's input values on ``rows`` (positions into ``df``), by role:
        ``data_foundry.v2.metrics.score(data.metric, y, p, **data.metric_inputs(rows))``.
        """
        rows = np.asarray(rows)
        out = {}
        for role, column in (_spec_fields(self.metric).get("inputs") or {}).items():
            source = self.scoring if self.scoring is not None and column in self.scoring.columns else self.df
            out[role] = source[column].to_numpy()[rows]
        return out

    def declared_metric(self) -> dict | None:
        """The declared metric as the probe library takes it (``curation_probes.weights``), scored as the benchmark
        scores it (``data_foundry.v2.metrics.scorer``: a group's rows aggregated, the input columns read by row), or
        None: a format-1 container, or a metric whose code only the definition holds (``kind="local"``).
        """
        fields = _spec_fields(self.metric)
        if not fields or fields.get("kind") == "local":
            return None
        frame = self.df.reset_index(drop=True)
        if self.scoring is not None:
            frame = frame.join(self.scoring[[c for c in self.scoring.columns if c not in frame.columns]])
        task = SimpleNamespace(target_column_name=self.target, objective_metric=self.metric, grouping=self.grouping)
        score_rows = scorer(SimpleNamespace(dataset=frame, task_metadata=task))

        def score(y_true: Any, y_pred: Any, rows: Any) -> float:
            # probabilities come as a table named by the classes: matched by name, in the sorted order of the classes
            labels = sorted(y_pred.columns) if isinstance(y_pred, pd.DataFrame) else None
            return score_rows(y_true, y_pred, rows, labels=labels)

        floor = (fields.get("params") or {}).get("min_prediction")
        if floor is not None:  # on the scale the target ships on, where the probes predict
            floor = float(_TO_SHIPPED[fields.get("target_transform") or "identity"](float(floor)))
        return {
            "name": fields["name"],
            "greater_is_better": bool(fields["greater_is_better"]),
            "prediction": fields["prediction"],
            "score": score,
            "floor": floor,
            "gini": "gini" in fields["name"],
            "row_weight": row_weight_column(self.metric),
            "params": dict(fields.get("params") or {}),
            "transform": fields.get("target_transform") or "identity",
        }


_TO_SHIPPED = {"identity": float, "log": np.log, "log1p": np.log1p, "log10": np.log10}
"""Each ``target_transform`` a spec may declare: a value on the original scale moved to the scale the target ships."""


def _spec_fields(spec: Any) -> dict:
    """A metric spec (a ``MetricSpec``, or the dict of the JSON file) as a dict; empty for None."""
    if spec is None:
        return {}
    return dataclasses.asdict(spec) if dataclasses.is_dataclass(spec) else dict(spec)


def dataset_names(root: Path | str) -> list[str]:
    """The unique names of the definitions under ``root``, sorted (``--all``)."""
    return sorted(discover_datasets(root, strict=False))


def definition(name: str, root: Path | str) -> AbstractCuratedDataset:
    """The v2 definition of ``name`` under ``root``."""
    return load_definition(Path(root) / name / "dataset.py")()  # this folder only


def _unit_weight_columns(task: Any) -> list[str]:
    """The unit weight's columns (``task.unit_weight``: the weight and the unit it counts once), never model inputs."""
    unit_weight = getattr(task, "unit_weight", None)
    return [unit_weight.column, unit_weight.unit] if unit_weight is not None else []


def _without_scoring_columns(df: pd.DataFrame, task: Any) -> tuple[pd.DataFrame, tuple[str, ...]]:
    """``df`` without the task's scoring columns (metric inputs) and the unit weight's columns, keeping the target,
    group and time columns.
    """
    keep = {task.target_column_name, *as_column_list(task.group_on), task.time_on}
    candidates = [c.column for c in getattr(task, "scoring_columns", None) or ()] + _unit_weight_columns(task)
    drop = tuple(dict.fromkeys(c for c in candidates if c in df.columns and c not in keep))
    return (df.drop(columns=list(drop)) if drop else df), drop


def _excluded_columns(task: Any) -> set[str]:
    """The columns that are never model inputs: the target, the group column(s), the scoring columns, the training
    weight (a scoring column too) and the unit weight's weight and unit, as ``feature_columns`` leaves them out.
    """
    return {
        task.target_column_name,
        *as_column_list(task.group_on),
        *(c.column for c in getattr(task, "scoring_columns", None) or ()),
        *as_column_list(getattr(task, "sample_weight", None)),
        *_unit_weight_columns(task),
    }


def _weight_and_metric(frame: pd.DataFrame, task: Any) -> dict[str, Any]:
    """The ``ProbeInput`` fields of the training weight, the declared metric and the scoring columns' values, from
    ``frame`` before the scoring columns are dropped.
    """
    column = getattr(task, "sample_weight", None)
    scoring = [c.column for c in getattr(task, "scoring_columns", None) or () if c.column in frame.columns]
    return {
        "weights": frame[column].to_numpy(dtype=float) if column else None,
        "weight_column": column,
        "metric": getattr(task, "objective_metric", None),
        "scoring": frame[scoring].reset_index(drop=True) if scoring else None,
    }


def _with_encoded_special_features(
    df: pd.DataFrame, task: Any, *, encode: bool
) -> tuple[pd.DataFrame, tuple[str, ...]]:
    """``df`` with each special feature in its recommended encoding (in place of its columns), and their names."""
    features = [f for f in getattr(task, "special_features", None) or () if all(c in df.columns for c in f.columns)]
    names = tuple(f.name for f in features)
    if not encode or not features:
        return df, names
    from data_foundry.v2.special import encode_special_feature  # noqa: PLC0415 - RDKit only for SMILES datasets

    for feature in features:
        df = encode_special_feature(df, feature)
    return df, names


def from_definition(
    ds: AbstractCuratedDataset, plan: Any = None, *, encode_special: bool = True, raw: bool = False
) -> ProbeInput:
    """The definition's frame and split plan, rebuilt from the raw files (no container); ``plan``: one already made.

    ``raw`` adds the raw state (``ProbeInput.raw``, ``raw_rows``, ``raw_note``; see the module docstring). The
    training weight is the definition's ``sample_weight``, read from the task metadata it builds.
    """
    plan = plan if plan is not None else ds.make_splits()
    task = ds.task_metadata_for(plan.df)
    df, scoring = _without_scoring_columns(plan.df, task)
    df, special = _with_encoded_special_features(df, task, encode=encode_special)
    excluded = _excluded_columns(task)
    table, rows, note = _raw_state(ds, plan.df) if raw else (None, None, "")
    return ProbeInput(
        df=df,
        target=task.target_column_name,
        problem_type=task.problem_type,
        regime=task.split_regime,
        splits=plan.splits,
        grouping=task.grouping,
        time_on=task.time_on,
        origin="definition",
        scoring_cols=scoring,
        special_features=special,
        feature_cols=tuple(c for c in df.columns if c not in excluded),
        raw=table,
        raw_rows=rows,
        raw_note=note,
        **_weight_and_metric(plan.df, task),
    )


def _raw_state(ds: AbstractCuratedDataset, frame: pd.DataFrame) -> tuple[pd.DataFrame | None, np.ndarray | None, str]:
    """The raw table, the raw position of each row of ``frame`` (the split plan's frame) and how it was traced."""
    table = ds.raw
    if not isinstance(table, pd.DataFrame):
        return None, None, "the raw data is not one table"
    processed, _test, lineage = ds.process(lineage=True)
    if lineage.rows is None:
        return table, None, lineage.note
    at = _row_positions(frame, processed)
    if at is None:
        return table, None, f"{lineage.note}, but the split step reorders the rows it keeps"
    return table, lineage.rows[at], lineage.note


def _row_positions(frame: pd.DataFrame, processed: pd.DataFrame) -> np.ndarray | None:
    """The position in ``processed`` of each row of ``frame``: the same frame, or one the split step sub-sampled
    keeping the row order (``subsample_frame``); None when the rows of ``frame`` are not in ``processed``'s order.
    """
    if len(frame) == len(processed) and frame.equals(processed):
        return np.arange(len(processed))
    want = pd.util.hash_pandas_object(frame, index=False).to_numpy()
    have = pd.util.hash_pandas_object(processed[frame.columns], index=False).to_numpy()
    out, j = np.empty(len(want), dtype=np.int64), 0
    for i, value in enumerate(want):  # both in the same order: a two-pointer merge
        while j < len(have) and have[j] != value:
            j += 1
        if j == len(have):
            return None
        out[i], j = j, j + 1
    return out


def from_container(container: CuratedContainer, origin: str, *, encode_special: bool = True) -> ProbeInput:
    """A container's frame, task and shipped splits; the training weight is its ``task_metadata.sample_weight``."""
    task = container.task_metadata
    df, scoring = _without_scoring_columns(container.dataset, task)
    df, special = _with_encoded_special_features(df, task, encode=encode_special)
    return ProbeInput(
        df=df,
        target=task.target_column_name,
        problem_type=task.problem_type,
        regime=task.split_regime,
        splits=container.experiment_metadata.splits,
        grouping=container.grouping,  # raises for a format-1 container
        time_on=task.time_on,
        origin=origin,
        scoring_cols=scoring,
        special_features=special,
        feature_cols=tuple(c for c in df.columns if c not in _excluded_columns(task)),
        **_weight_and_metric(container.dataset, task),
    )


def load(name: str, root: Path | str, *, built: bool, encode_special: bool = True) -> ProbeInput:
    """The container of ``name``: with ``built``, the one recorded in its ``README.md``'s build record (when there is
    one), else rebuilt from the definition.
    """
    if built:
        build = (read_report(Path(root) / name / "README.md") or {}).get("build") or {}
        if build.get("path"):
            container = CuratedContainer.load(resolve_warehouse_dir() / build["path"])
            return from_container(container, "built", encode_special=encode_special)
    return from_container(definition(name, root).to_container(), "rebuilt", encode_special=encode_special)
