"""A v2 dataset as the plain inputs of the probe library: the Data Foundry side of the probe scripts.

The probes in ``.claude/skills/knowledge-curation/scripts/curation_probes/`` take a pandas frame, its target and
problem type, the group and time columns and the splits; this module reads them from a v2 definition under a root
folder: from the definition's own frame and split plan (rebuilt from the raw files), or from a container (the built
one recorded in the definition's ``README.md``, or one rebuilt from the definition).

The scoring columns (``task.scoring_columns``: the inputs of the metric, such as Numerai's ``era``) are never model
inputs, so they are dropped from the frame the probes see, unless one is also the target, a group column or the time
column, which the probes take by name. ``ProbeInput.scoring_cols`` lists the ones dropped.

A special feature (``task.special_features``) enters the probes in its recommended encoding
(``data_foundry.v2.special.encode_special_feature``), as a benchmark would give it to a model: a SMILES column as its
descriptor and fingerprint columns (``<column>__rdkit_<name>``, ``<column>__maccs_<i>``, ``<column>__ecfp4_<i>``),
never as text; a spectrum's columns with the encoded values. ``encode_special=False`` keeps the values as shipped (the
blind reviewer's clean room). ``ProbeInput.special_features`` lists them by name.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import as_column_list, resolve_warehouse_dir
from data_foundry.v2 import discover_datasets, load_definition, read_report

if TYPE_CHECKING:
    import pandas as pd
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


def dataset_names(root: Path | str) -> list[str]:
    """The unique names of the definitions under ``root``, sorted (``--all``)."""
    return sorted(discover_datasets(root, strict=False))


def definition(name: str, root: Path | str) -> AbstractCuratedDataset:
    """The v2 definition of ``name`` under ``root``."""
    return load_definition(Path(root) / name / "dataset.py")()  # this folder only


def _without_scoring_columns(df: pd.DataFrame, task: Any) -> tuple[pd.DataFrame, tuple[str, ...]]:
    """``df`` without the task's scoring columns (metric inputs), keeping the target, group and time columns."""
    keep = {task.target_column_name, *as_column_list(task.group_on), task.time_on}
    drop = tuple(
        c.column
        for c in getattr(task, "scoring_columns", None) or ()
        if c.column in df.columns and c.column not in keep
    )
    return (df.drop(columns=list(drop)) if drop else df), drop


def _excluded_columns(task: Any) -> set[str]:
    """The columns that are never model inputs: the target, the group column(s) and the scoring columns."""
    return {
        task.target_column_name,
        *as_column_list(task.group_on),
        *(c.column for c in getattr(task, "scoring_columns", None) or ()),
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


def from_definition(ds: AbstractCuratedDataset, plan: Any = None, *, encode_special: bool = True) -> ProbeInput:
    """The definition's frame and split plan, rebuilt from the raw files (no container); ``plan``: one already made."""
    plan = plan if plan is not None else ds.make_splits()
    task = ds.task_metadata_for(plan.df)
    df, scoring = _without_scoring_columns(plan.df, task)
    df, special = _with_encoded_special_features(df, task, encode=encode_special)
    excluded = _excluded_columns(task)
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
    )


def from_container(container: CuratedContainer, origin: str, *, encode_special: bool = True) -> ProbeInput:
    """A container's frame, task and shipped splits."""
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
