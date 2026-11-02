"""A v2 dataset as the plain inputs of the probe library: the Data Foundry side of the probe scripts.

The probes in ``.claude/skills/knowledge-curation/scripts/curation_probes/`` take a pandas frame, its target and
problem type, the group and time columns and the splits; this module reads them from a v2 definition under a root
folder: from the definition's own frame and split plan (rebuilt from the raw files), or from a container (the built
one recorded in the definition's ``README.md``, or one rebuilt from the definition).

The scoring columns (``task.scoring_columns``: the inputs of the metric, such as Numerai's ``era``) are never model
inputs, so they are dropped from the frame the probes see, unless one is also the target, a group column or the time
column, which the probes take by name. ``ProbeInput.scoring_cols`` lists the ones dropped.

A SMILES column (``task.semantic_columns`` of type ``smiles``) enters the probes in the recommended encoding
(``data_foundry.v2.chemistry.encode_smiles``: RDKit's 2D descriptors, the MACCS keys and the ECFP4 counts, columns
``<column>__rdkit_<name>``, ``<column>__maccs_<i>`` and ``<column>__ecfp4_<i>``), as a benchmark would give it to a model, not as text.
``encode_smiles=False`` keeps the string (the blind reviewer's clean room). ``ProbeInput.smiles_cols`` lists them.

A spectrum (``task.feature_groups`` of type ``spectrum``) enters the probes in its recommended encoding
(``data_foundry.v2.spectra.encode_spectrum``: a raw mass spectrum through MALDIquant's steps, any other as it is), the
same columns with new values, as a benchmark would give it to a model. ``encode_spectra=False`` keeps the values as
shipped (the clean room). ``ProbeInput.spectra`` lists the spectra by name.
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
        smiles_cols: The SMILES columns of the task, encoded in ``df`` unless loaded with ``encode_smiles=False``.
        spectra: The spectra of the task by name, encoded in ``df`` unless loaded with ``encode_spectra=False``.
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
    smiles_cols: tuple[str, ...] = ()
    spectra: tuple[str, ...] = ()

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


def _with_encoded_smiles(df: pd.DataFrame, task: Any, *, encode: bool) -> tuple[pd.DataFrame, tuple[str, ...]]:
    """``df`` with each SMILES column replaced by its recommended encoding (in place of the column), and their names."""
    smiles = tuple(
        c.column
        for c in getattr(task, "semantic_columns", None) or ()
        if c.semantic_type == "smiles" and c.column in df.columns
    )
    if not encode or not smiles:
        return df, smiles
    import pandas as pd  # noqa: PLC0415
    from data_foundry.v2.chemistry import encode_smiles  # noqa: PLC0415 - RDKit only for datasets with SMILES

    parts = []
    for column in df.columns:
        parts.append(encode_smiles(df[column], prefix=f"{column}__") if column in smiles else df[[column]])
    return pd.concat(parts, axis=1), smiles


def _with_encoded_spectra(df: pd.DataFrame, task: Any, *, encode: bool) -> tuple[pd.DataFrame, tuple[str, ...]]:
    """``df`` with each spectrum's columns in its recommended encoding (same columns), and the spectra's names."""
    groups = [g for g in getattr(task, "feature_groups", None) or () if g.semantic_type == "spectrum"]
    if not encode or not groups:
        return df, tuple(g.name for g in groups)
    from data_foundry.v2.spectra import encode_spectrum  # noqa: PLC0415

    df = df.copy()
    for g in groups:
        df[g.columns] = encode_spectrum(df[g.columns], g.axis, g.recommended_encoding)
    return df, tuple(g.name for g in groups)


def from_definition(
    ds: AbstractCuratedDataset, *, encode_smiles: bool = True, encode_spectra: bool = True
) -> ProbeInput:
    """The definition's frame and split plan, rebuilt from the raw files (no container)."""
    plan = ds.make_splits()
    task = ds.task_metadata_for(plan.df)
    df, scoring = _without_scoring_columns(plan.df, task)
    df, smiles = _with_encoded_smiles(df, task, encode=encode_smiles)
    df, spectra = _with_encoded_spectra(df, task, encode=encode_spectra)
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
        smiles_cols=smiles,
        spectra=spectra,
    )


def from_container(
    container: CuratedContainer, origin: str, *, encode_smiles: bool = True, encode_spectra: bool = True
) -> ProbeInput:
    """A container's frame, task and shipped splits."""
    task = container.task_metadata
    df, scoring = _without_scoring_columns(container.dataset, task)
    df, smiles = _with_encoded_smiles(df, task, encode=encode_smiles)
    df, spectra = _with_encoded_spectra(df, task, encode=encode_spectra)
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
        smiles_cols=smiles,
        spectra=spectra,
    )


def load(
    name: str, root: Path | str, *, built: bool, encode_smiles: bool = True, encode_spectra: bool = True
) -> ProbeInput:
    """The container of ``name``: with ``built``, the one recorded in its ``README.md``'s build record (when there is
    one), else rebuilt from the definition.
    """
    if built:
        build = (read_report(Path(root) / name / "README.md") or {}).get("build") or {}
        if build.get("path"):
            container = CuratedContainer.load(resolve_warehouse_dir() / build["path"])
            return from_container(container, "built", encode_smiles=encode_smiles, encode_spectra=encode_spectra)
    container = definition(name, root).to_container()
    return from_container(container, "rebuilt", encode_smiles=encode_smiles, encode_spectra=encode_spectra)
