"""A v2 dataset as the plain inputs of the probe library: the Data Foundry side of the probe scripts.

The probes in ``.claude/skills/knowledge-curation/scripts/curation_probes/`` take a pandas frame, its target and
problem type, the group and time columns and the splits; this module reads them from a v2 definition under a root
folder: from the definition's own frame and split plan (rebuilt from the raw files), or from a container (the built
one recorded in the definition's ``README.md``, or one rebuilt from the definition).
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
    """

    df: pd.DataFrame
    target: str
    problem_type: str
    regime: str
    splits: dict[Any, dict[Any, tuple]]
    grouping: Grouping | None
    time_on: str | None
    origin: str

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


def from_definition(ds: AbstractCuratedDataset) -> ProbeInput:
    """The definition's frame and split plan, rebuilt from the raw files (no container)."""
    plan = ds.make_splits()
    task = ds.task_metadata
    return ProbeInput(
        df=plan.df,
        target=task.target_column_name,
        problem_type=task.problem_type,
        regime=task.split_regime,
        splits=plan.splits,
        grouping=task.grouping,
        time_on=task.time_on,
        origin="definition",
    )


def from_container(container: CuratedContainer, origin: str) -> ProbeInput:
    """A container's frame, task and shipped splits."""
    task = container.task_metadata
    return ProbeInput(
        df=container.dataset,
        target=task.target_column_name,
        problem_type=task.problem_type,
        regime=task.split_regime,
        splits=container.experiment_metadata.splits,
        grouping=container.grouping,  # raises for a format-1 container
        time_on=task.time_on,
        origin=origin,
    )


def load(name: str, root: Path | str, *, built: bool) -> ProbeInput:
    """The container of ``name``: with ``built``, the one recorded in its ``README.md``'s build record (when there is
    one), else rebuilt from the definition.
    """
    if built:
        build = (read_report(Path(root) / name / "README.md") or {}).get("build") or {}
        if build.get("path"):
            return from_container(CuratedContainer.load(resolve_warehouse_dir() / build["path"]), "built")
    return from_container(definition(name, root).to_container(), "rebuilt")
