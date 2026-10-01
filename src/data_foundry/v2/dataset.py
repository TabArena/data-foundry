"""The v2 dataset interface: one :class:`AbstractCuratedDataset` subclass per curated dataset.

A curated dataset is one ``dataset.py`` holding one subclass. Everything that describes the dataset is a
flat class attribute (metadata, task, preprocessing declarations, split declarations), and the code that
turns the raw download into the curated frame lives in a few hooks:

* :meth:`~AbstractCuratedDataset._load_raw` (required): read the raw files. Cached, so iterating on the
  cleaning never re-reads them.
* :meth:`~AbstractCuratedDataset._clean` (optional): turn the raw data into the curated frame.
* :meth:`~AbstractCuratedDataset._feature_types` (optional): the dtypes of the cleaned frame's columns
  (categorical / string / datetime), as a :class:`FeatureTypes`.
* :meth:`~AbstractCuratedDataset._make_splits` (optional): hand-built outer splits, for what the
  declarative ``temporal_splits`` and the recommended IID/grouped splits do not cover.
* :meth:`~AbstractCuratedDataset._prepare_raw_files` (optional): a heavy one-off step that writes
  intermediate files into the raw directory (listed in ``prepared_raw_files``).
* :meth:`~AbstractCuratedDataset._extra_checks` (optional): dataset-specific checks, such as a leak test.

The base class runs the rest the same way for every dataset: after ``_clean`` it casts the columns
``_feature_types`` names (and a classification target to ``category``), and fixes the row order (stable sort
by ``time_on`` for temporal tasks, else a shuffle with seed 42); then it builds the splits with the benchmark
seed, the container, the bundle checks and the report. The pattern follows
TabArena's model interface: declarative class attributes plus a small set of hooks.

From a notebook next to ``dataset.py``::

    from data_foundry.v2 import workbench

    ds = workbench()      # this folder's dataset; picks up edits to dataset.py automatically
    ds.df.head()          # the curated frame
    ds.check()            # the full pipeline and bundle checks, no save; writes README.md
"""

from __future__ import annotations

import contextlib
import datetime as dt
import inspect
import io
import re
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from data_foundry.bundle_checks import (
    SEVERITY_ORDER,
    TABARENA_DEFAULT_METRICS,
    BundleCheckReport,
    CheckResult,
    run_bundle_checks,
    verify_saved_container,
)
from data_foundry.curation_container import CuratedContainer
from data_foundry.dataset_checks import run_all_checks
from data_foundry.schema import (
    DatasetMetadata,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadata,
    resolve_warehouse_dir,
)
from data_foundry.v2 import splits as protocol
from data_foundry.v2.preprocessing import SHUFFLE_RANDOM_STATE, cast_dtypes, order_rows
from data_foundry.v2.splits import SPLIT_RANDOM_STATE, SplitPlan, Splits, TemporalSplits

DEFINITION_FILENAME = "dataset.py"
"""The file that holds a dataset's definition, one per dataset folder."""

REPORT_FILENAME = "README.md"
"""The generated report next to the definition file: the folder's README, which GitHub shows below its files."""

DEFAULT_SPLITS_COMMENT = "Default splits."
"""The splits comment of every dataset on the recommended IID or grouped splits."""


class _Auto:
    """Sentinel default of ``stratify_on``: the target for classification, nothing for regression."""

    def __repr__(self) -> str:
        return "AUTO"

    def __bool__(self) -> bool:
        return False


AUTO: Any = _Auto()
"""Sentinel default of ``stratify_on``: the target for classification, nothing for regression."""

REGIME_TAGS = ("IID", "Non-IID", "Temporal", "Grouped", "GroupedTemporal")

_UNSEEDED = re.compile(
    r"uuid\.uuid[14]\(|\bnp\.random\.(rand|randn|randint|choice|shuffle|permutation|random)\(|default_rng\(\)"
    r"|\brandom\.(random|choice|shuffle|sample|randint)\(|\.sample\((?![^)]*random_state)[^)]*\)"
)
"""Unseeded randomness in a definition: random ids, unseeded numpy/stdlib random, `sample` without a seed."""

_TEXT_FIELDS = ("download_description", "bibtex", "curation_comments", "version_comment", "splits_comment")
_BIBTEX_KEY = re.compile(r"@\w+\s*\{\s*([^,\s}]+)\s*,")


def clean_text(text: str | None) -> str | None:
    """Normalise a multi-line class attribute: dedent it and strip the blank first and last lines.

    Multi-line strings can then be indented like the code around them::

        download_description = \"\"\"
            mkdir -p local-data-warehouse/my_dataset
            wget ...
        \"\"\"
    """
    return None if text is None else inspect.cleandoc(text)


@dataclass(frozen=True)
class FeatureTypes:
    """The dtypes of the cleaned frame's columns, returned by :meth:`AbstractCuratedDataset._feature_types`.

    Attributes:
        categorical: Columns cast to ``category`` (fixed, finite value sets); unused categories are removed.
        string: Columns cast to ``string`` (free text, high-cardinality text).
        datetime: Columns parsed with ``pd.to_datetime``; a mapping gives a per-column format.
    """

    categorical: tuple[str, ...] | list[str] = ()
    string: tuple[str, ...] | list[str] = ()
    datetime: tuple[str, ...] | list[str] | dict[str, str | None] = ()

    @property
    def datetime_formats(self) -> dict[str, str | None]:
        """``datetime`` as a column -> format mapping."""
        return dict(self.datetime) if isinstance(self.datetime, dict) else dict.fromkeys(self.datetime)


@dataclass
class Decision:
    """One curation decision with the evidence behind it, rendered into the generated ``README.md``.

    Attributes:
        title: The decision, as a short statement ("Temporal split, not grouped by auction").
        why: The reasoning in one or two sentences.
        evidence: A table (DataFrame / Series), a matplotlib figure, a string, or None.
    """

    title: str
    why: str
    evidence: Any = None


@dataclass
class CurationResult:
    """The outcome of :meth:`AbstractCuratedDataset.check` or :meth:`AbstractCuratedDataset.build`.

    Attributes:
        dataset: The dataset definition that produced this result.
        container: The curated container (a fresh UUID unless it was saved).
        bundle_report: The bundle-check report, with the definition and extra checks merged in.
        data_checks: The tables of :func:`~data_foundry.dataset_checks.run_all_checks`, by name.
        saved_path: Where the container was saved, or None for a check without saving.
        created_at: When the result was produced (UTC).
    """

    dataset: AbstractCuratedDataset
    container: CuratedContainer
    bundle_report: BundleCheckReport
    data_checks: dict[str, pd.DataFrame] = field(default_factory=dict)
    decisions: list[Decision] = field(default_factory=list)
    saved_path: Path | None = None
    created_at: dt.datetime = field(default_factory=lambda: dt.datetime.now(dt.timezone.utc))

    @property
    def ok(self) -> bool:
        """Whether the bundle checks found no error."""
        return self.bundle_report.ok

    @property
    def saved(self) -> bool:
        """Whether the container was saved (only :meth:`AbstractCuratedDataset.build` saves)."""
        return self.saved_path is not None


class DatasetDefinitionError(TypeError):
    """A dataset class is missing a declaration or declares an inconsistent one."""


class AbstractCuratedDataset(ABC):
    """Base class of a curated dataset definition. Subclass it once per dataset, in ``dataset.py``.

    Multi-line text attributes may be indented like code; they are dedented (:func:`clean_text`). The class
    is validated when it is defined, so importing ``dataset.py`` already fails on a missing or inconsistent
    declaration. The metadata objects saved with the container are built from the attributes and are
    available as ``dataset_metadata`` and ``task_metadata``.
    """

    # --- dataset ------------------------------------------------------------------------------------
    unique_name: ClassVar[str]
    """Snake-case name; equal to the folder name. A version sub-sampled to the row budget ends in ``_1m``."""
    year: ClassVar[str]
    """Year the data was published."""
    domain: ClassVar[str]
    """One of :data:`data_foundry.schema.Domain`."""
    source: ClassVar[str]
    """Where the data first appeared: one of :data:`data_foundry.schema.DatasetSource`."""
    source_url: ClassVar[str]
    """Link to the original publication of the data."""
    download_description: ClassVar[str]
    """Commands (and notes) that recreate the raw files in ``local-data-warehouse/<unique_name>/``."""
    bibtex: ClassVar[str]
    """BibTeX of the work that published the data."""
    bibtex_key: ClassVar[str | None] = None
    """Citation key(s), comma-separated; parsed from ``bibtex`` when None."""
    license: ClassVar[str | None]
    """The license the source states."""
    data_tags: ClassVar[tuple[str, ...]] = ()
    """Context tags (``Spatial``, ``Anonymized``, ...). The regime tags (``IID`` or ``Non-IID`` plus
    ``Temporal``/``Grouped``) are added from the task unless one is listed here."""
    curation_comments: ClassVar[str] = ""
    """The audit trail: the starting artifact, then one bullet per non-obvious decision."""
    version_of: ClassVar[str | None] = None
    """For a ``_1m`` version (a frame above 1.5M rows, sub-sampled): the ``unique_name`` it was made from (its raw
    files are read)."""
    version_comment: ClassVar[str | None] = None
    """For a version: how it differs from the dataset it was made from."""
    raw_data_from: ClassVar[str | None] = None
    """Read the raw files of another dataset (for example an alternative-target ``<name>_clf`` of ``<name>``).
    Defaults to ``version_of``, then ``unique_name``."""

    # --- task ---------------------------------------------------------------------------------------
    target: ClassVar[str]
    """The target column."""
    problem_type: ClassVar[str]
    """``binary_classification``, ``multiclass_classification`` or ``regression``."""
    metric: ClassVar[str | None] = None
    """The objective metric; None is the default for the problem type (roc_auc / log_loss / rmse)."""
    stratify_on: ClassVar[Any] = AUTO
    """Column(s) to stratify on. Default: the target for classification, nothing for regression."""
    time_on: ClassVar[str | None] = None
    """The time column of a temporal task."""
    group_on: ClassVar[str | list[str] | None] = None
    """The group column(s) of a grouped task."""
    group_labels: ClassVar[str | None] = None
    """``per_group`` (one label per group) or ``per_sample`` (one label per row) for a grouped task."""
    group_time_on: ClassVar[str | None] = None
    """The time column inside groups, if any."""

    # --- row order ----------------------------------------------------------------------------------
    shuffle: ClassVar[bool] = True
    """Shuffle IID and grouped data (seed 42) as the last step. Temporal data is always sorted by time."""

    # --- splits -------------------------------------------------------------------------------------
    temporal_splits: ClassVar[TemporalSplits | None] = None
    """Declarative temporal splits; a temporal task sets this or implements `_make_splits`."""
    splits_comment: ClassVar[str | None] = None
    """What the splits simulate. None: the default comment for recommended or declarative splits."""
    time_horizon: ClassVar[int | None] = None
    """How far ahead a temporal task predicts (default: the window of a calendar `temporal_splits`)."""
    time_horizon_unit: ClassVar[str | None] = None
    """``days``, ``weeks``, ``months``, ``years`` or ``steps``."""
    subsample_to_budget: ClassVar[bool] = False
    """``True`` for a ``_1m`` version. IID / grouped: sub-sample a frame above 1.5M rows to 1.5M (whole groups,
    stratified) before splitting, so every fold trains on at most 1M and tests on at most 500k rows. Temporal: sample
    per window (each test window up to 500k rows, each train side a random 1M of all earlier rows) and keep only the
    rows a split uses (:mod:`data_foundry.v2.splits`)."""

    # --- checks and raw files ----------------------------------------------------------------------
    accepted_check_warnings: ClassVar[dict[str, str]] = {}
    """Bundle-check slugs accepted on purpose, each with the reason it is correct for this dataset."""
    prepared_raw_files: ClassVar[tuple[str, ...]] = ()
    """Files :meth:`_prepare_raw_files` writes into :attr:`raw_dir`; it runs when any is missing."""

    # --- fixed seeds (one per benchmark, never per dataset) ----------------------------------------
    SHUFFLE_RANDOM_STATE: ClassVar[int] = SHUFFLE_RANDOM_STATE
    SPLIT_RANDOM_STATE: ClassVar[int] = SPLIT_RANDOM_STATE

    # --- built from the attributes -----------------------------------------------------------------
    dataset_metadata: ClassVar[DatasetMetadata]
    task_metadata: ClassVar[PredictiveMLTaskMetadata]

    # --- hooks --------------------------------------------------------------------------------------
    @abstractmethod
    def _load_raw(self, raw_dir: Path) -> Any:
        """Read the raw files from ``raw_dir``: a frame, or a dict / tuple of frames for multi-table sources.

        Only reading belongs here (and a join that follows the source's own keys): the result is cached,
        so edits to :meth:`_clean` re-run without reading the files again. Files next to ``dataset.py``
        are reachable via :attr:`folder`.
        """

    def _clean(self, raw: Any) -> pd.DataFrame | tuple[pd.DataFrame, pd.DataFrame]:
        """Turn the raw data into the curated frame (default: the raw frame as it is).

        ``raw`` is a copy of the cached output of :meth:`_load_raw`, so it can be changed in place; it runs under
        pandas copy-on-write, so the copy costs memory only for the columns that change (write
        ``df.loc[mask, "a"] = x``, not the chained ``df["a"][mask] = x``, which does not write). All
        column work happens here: renames, derived columns, and drops (:func:`~data_foundry.v2.drop_columns`
        fails on a misspelled name). Leave the final dtypes to :meth:`_feature_types` (cast mid-way with
        :func:`~data_foundry.v2.cast_dtypes` only when a later step needs it) and do not shuffle or sort:
        the base class does both afterwards. Return a ``(dataset, test_dataset)`` pair when the source
        ships an unlabeled test set kept for inference.
        """
        if not isinstance(raw, pd.DataFrame):
            raise NotImplementedError(
                f"{type(self).__name__}: `_load_raw` returned several tables; implement `_clean`."
            )
        return raw

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        """Name the dtypes of the cleaned frame's columns (default: every column stays as it is).

        ``df`` is the output of :meth:`_clean`, so the lists can be computed from its final columns (for
        example ``[c for c in df if c.startswith("cat_")]``). Every column not named must be numeric or
        boolean. A classification target is cast to ``category`` without being listed.
        """
        del df
        return FeatureTypes()

    def _make_splits(self, df: pd.DataFrame) -> Splits | SplitPlan:
        """Build the outer splits for ``df`` (already in its final row order).

        The default is the v2 protocol (:mod:`data_foundry.v2.splits`): ``temporal_splits`` for a temporal
        task, else the recommended IID or grouped 3-fold cross-validation, on a frame sub-sampled to 1.5M rows
        for a ``_1m`` version. Override it only for a split none of these express, and return a
        :class:`SplitPlan` when the split step reduces the frame or computes its comment.
        """
        return self.default_splits(df)

    def _prepare_raw_files(self, raw_dir: Path) -> None:  # noqa: B027 - an optional hook, empty on purpose
        """Write the files listed in :attr:`prepared_raw_files` into ``raw_dir`` (optional, heavy, one-off)."""

    def _extra_checks(self, container: CuratedContainer) -> list[CheckResult]:
        """Return dataset-specific findings, for example a leak test (optional)."""
        del container
        return []

    def _decisions(self, raw: Any, df: pd.DataFrame) -> list[Decision]:
        """Return the curation decisions worth showing evidence for (optional).

        Each :class:`Decision` pairs a statement and its reasoning with a table or a figure computed from
        the data, and ``check`` renders them into the "Decisions" section of ``README.md`` (figures as PNGs
        under ``figures/``). Good candidates are the decisions a reviewer would question: why a column is a
        leak, why the split is temporal and not grouped, why duplicates are kept. ``raw`` is the cached
        output of ``_load_raw`` (do not change it), ``df`` the curated frame.
        """
        del raw, df
        return []

    # --- class set-up -------------------------------------------------------------------------------
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if inspect.isabstract(cls):
            return
        _validate_definition(cls)

    def __init__(self) -> None:
        """Create the dataset; nothing is read until :attr:`raw` or :attr:`df` is first used."""
        self._raw_cache: Any = None
        self._raw_loaded = False
        self._df_cache: tuple[pd.DataFrame, pd.DataFrame | None] | None = None
        self.auto_reload = False
        self._source_mtime = self._definition_mtime()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.unique_name!r} from {self.folder}>"

    @property
    def folder(self) -> Path:
        """The folder holding this dataset's ``dataset.py`` (and any sibling files it reads)."""
        return Path(inspect.getfile(type(self))).resolve().parent

    @property
    def raw_dir(self) -> Path:
        """Where the raw download lives: ``<warehouse>/<raw_data_from or version_of or unique_name>``."""
        return resolve_warehouse_dir() / (self.raw_data_from or self.version_of or self.unique_name)

    @property
    def report_path(self) -> Path:
        """The generated ``README.md`` next to ``dataset.py``."""
        return self.folder / REPORT_FILENAME

    # --- reloading ----------------------------------------------------------------------------------
    def _definition_mtime(self) -> float | None:
        try:
            return Path(inspect.getfile(type(self))).stat().st_mtime
        except (OSError, TypeError):
            return None

    def reload(self) -> AbstractCuratedDataset:
        """Re-import ``dataset.py`` in place. Returns ``self``.

        The cached raw data is kept when ``_load_raw`` and ``_prepare_raw_files`` are unchanged, so
        iterating on ``_clean`` or the declarations never re-reads the files.
        """
        from data_foundry.v2.registry import load_definition  # noqa: PLC0415 - the registry imports this module

        old = type(self)
        new = load_definition(inspect.getfile(old))
        keep_raw = all(_source(old, name) == _source(new, name) for name in ("_load_raw", "_prepare_raw_files"))
        self.__class__ = new
        if not keep_raw:
            self._raw_cache, self._raw_loaded = None, False
        self._df_cache = None
        self._source_mtime = self._definition_mtime()
        return self

    def _refresh(self) -> None:
        if self.auto_reload and self._definition_mtime() != self._source_mtime:
            self.reload()

    # --- data ---------------------------------------------------------------------------------------
    def prepare_raw_files(self, *, force: bool = False) -> None:
        """Run :meth:`_prepare_raw_files` when a file in :attr:`prepared_raw_files` is missing (or ``force``)."""
        missing = [name for name in self.prepared_raw_files if not (self.raw_dir / name).exists()]
        if force or missing:
            self._prepare_raw_files(self.raw_dir)

    @property
    def raw(self) -> Any:
        """The output of :meth:`_load_raw`, cached (kept across :meth:`reload` while its code is unchanged)."""
        self._refresh()
        if not self._raw_loaded:
            self.prepare_raw_files()
            with _copy_on_write():
                self._raw_cache = self._load_raw(self.raw_dir)
            self._raw_loaded = True
        return self._raw_cache

    def process(self) -> tuple[pd.DataFrame, pd.DataFrame | None]:
        """Run :meth:`_clean` on a copy of :attr:`raw`, then the standard steps. Returns (dataset, test_dataset)."""
        with _copy_on_write():
            cleaned = self._clean(_copy(self.raw))
            df, test = cleaned if isinstance(cleaned, tuple) else (cleaned, None)
            df = self._standardize(df)
            if test is not None:
                test = self._standardize(test, order=False)
        return df, test

    def _standardize(self, df: pd.DataFrame, *, order: bool = True) -> pd.DataFrame:
        types = self.feature_types(df)
        present = set(df.columns)
        df = cast_dtypes(
            df,
            categorical=[c for c in types.categorical if c in present or order],
            string=[c for c in types.string if c in present or order],
            datetime={c: f for c, f in types.datetime_formats.items() if c in present or order},
        )
        if not order:
            return df.reset_index(drop=True)
        return order_rows(df, time_on=self.time_on, shuffle=self.shuffle)

    def feature_types(self, df: pd.DataFrame | None = None) -> FeatureTypes:
        """:meth:`_feature_types` for ``df`` (default: the cleaned frame), with a classification target added."""
        if df is None:
            with _copy_on_write():
                cleaned = self._clean(_copy(self.raw))
            df = cleaned[0] if isinstance(cleaned, tuple) else cleaned
        types = self._feature_types(df)
        if not isinstance(types, FeatureTypes):
            msg = f"{type(self).__name__}: `_feature_types` must return a FeatureTypes."
            raise DatasetDefinitionError(msg)
        listed = {*types.categorical, *types.string, *types.datetime_formats}
        if self.problem_type != "regression" and self.target not in listed and self.target in df.columns:
            types = FeatureTypes(
                categorical=(*types.categorical, self.target), string=types.string, datetime=types.datetime
            )
        return types

    @property
    def df(self) -> pd.DataFrame:
        """The curated frame (after the standard steps), cached until the definition changes.

        Explore it freely: :meth:`check` and :meth:`build` rebuild the frame from the raw data and never
        use this cached copy.
        """
        self._refresh()
        if self._df_cache is None:
            self._df_cache = self.process()
        return self._df_cache[0]

    @property
    def test_df(self) -> pd.DataFrame | None:
        """The unlabeled test set, if `_clean` returned one."""
        _ = self.df
        return self._df_cache[1]

    def run_all_checks(self, df: pd.DataFrame | None = None) -> dict[str, pd.DataFrame]:
        """Run the exploratory :func:`~data_foundry.dataset_checks.run_all_checks` tables on ``df``."""
        df = self.df if df is None else df
        with _quiet():
            tables = run_all_checks(
                data=df,
                target_feature=self.target,
                problem_type=self.problem_type,
                print_report=False,
            )
        return dict(zip(("head", "summary", "numeric_stats", "cat_stats", "target"), tables, strict=True))

    # --- splits -------------------------------------------------------------------------------------
    def default_splits(self, df: pd.DataFrame) -> SplitPlan:
        """The default of :meth:`_make_splits`: the v2 split protocol (:mod:`data_foundry.v2.splits`).

        The splits are the declarative temporal windows, or the recommended IID / grouped 3-fold cross-validation,
        and no split trains on more than 1M or tests on more than 500k rows. A ``_1m`` version of IID or grouped
        data first sub-samples the frame to 1.5M rows (whole groups, stratified); a temporal ``_1m`` version samples
        per window instead (:func:`~data_foundry.v2.splits.sample_temporal_splits`) and keeps only the rows a split
        uses.
        """
        task = self.task_metadata
        temporal = task.time_on is not None
        frame_sampled = self.subsample_to_budget and not temporal
        if frame_sampled:
            if len(df) <= protocol.FRAME_ROW_BUDGET:
                msg = (
                    f"{type(self).__name__}: the frame has {len(df):,} rows, within the "
                    f"{protocol.FRAME_ROW_BUDGET:,}-row budget. Take the dataset fully: drop `subsample_to_budget` "
                    "and the `_1m` version."
                )
                raise DatasetDefinitionError(msg)
            df = protocol.subsample_frame(
                df, group_on=task.group_on, stratify_on=task.stratify_on, random_state=self.SPLIT_RANDOM_STATE
            )

        splits, comment = self._window_splits(df) if temporal else (self._cross_validation(df), DEFAULT_SPLITS_COMMENT)

        train_budget, test_budget = (
            protocol.rows_text(protocol.TRAIN_ROW_BUDGET),
            protocol.rows_text(protocol.TEST_ROW_BUDGET),
        )
        if self.subsample_to_budget and temporal:
            df, splits, trimmed = protocol.sample_temporal_splits(
                df, splits, stratify_on=task.stratify_on, random_state=self.SPLIT_RANDOM_STATE
            )
            if not trimmed:
                msg = (
                    f"{type(self).__name__}: no split side exceeds the row budget ({train_budget} train, {test_budget} "
                    "test rows). Take the dataset fully: drop `subsample_to_budget` and the `_1m` version."
                )
                raise DatasetDefinitionError(msg)
            comment += (
                f" Each test window keeps at most {test_budget} of its rows and each train side is a random "
                f"{train_budget} of all earlier rows (one random order for all windows); the frame keeps only the rows "
                "a split uses."
            )
            return SplitPlan(splits=splits, df=_drop_unused_categories(df), comment=comment)

        splits, capped = protocol.cap_splits(
            df,
            splits,
            group_on=task.group_on,
            stratify_on=task.stratify_on,
            random_state=self.SPLIT_RANDOM_STATE,
        )
        budget = f"every split trains on at most {train_budget} and tests on at most {test_budget} rows"
        if frame_sampled:
            whole = " (whole groups)" if task.group_on is not None else ""
            comment += (
                f" The frame is sub-sampled to {protocol.rows_text(protocol.FRAME_ROW_BUDGET)} rows{whole}; {budget}."
            )
            return SplitPlan(splits=splits, df=_drop_unused_categories(df), comment=comment)
        if capped:
            comment += f" Split sides over the row budget are trimmed: {budget}."
        return SplitPlan(splits=splits, comment=comment)

    def _window_splits(self, df: pd.DataFrame) -> tuple[Splits, str]:
        """The declarative temporal windows on ``df`` and their generated comment."""
        if self.temporal_splits is None:
            msg = f"{type(self).__name__}: a temporal task needs `temporal_splits` or `_make_splits`."
            raise DatasetDefinitionError(msg)
        time_on = self.task_metadata.time_on
        splits = self.temporal_splits.splits(df, time_on)
        derived = None
        if self.temporal_splits.window is None and self.temporal_splits.cutoffs is None:
            first_test = splits[0][0][1]
            derived = len(first_test) if self.temporal_splits.unit == "rows" else df[time_on].iloc[first_test].nunique()
        return splits, self.temporal_splits.describe(len(splits), derived_window=derived)

    def _cross_validation(self, df: pd.DataFrame) -> Splits:
        """The recommended IID or grouped 3-fold cross-validation on ``df``."""
        task = self.task_metadata
        n_repeats, n_folds = protocol.recommended_dimensions(df, group_on=task.group_on, group_labels=task.group_labels)
        if task.group_on is None:
            return protocol.iid_splits(
                df,
                n_repeats=n_repeats,
                n_folds=n_folds,
                stratify_on=task.stratify_on,
                random_state=self.SPLIT_RANDOM_STATE,
            )
        return protocol.grouped_splits(
            df,
            n_repeats=n_repeats,
            n_folds=n_folds,
            group_on=task.group_on,
            group_labels=task.group_labels,
            stratify_on=task.stratify_on,
            random_state=self.SPLIT_RANDOM_STATE,
        )

    def make_splits(self, df: pd.DataFrame | None = None) -> SplitPlan:
        """Run :meth:`_make_splits` on ``df`` (default: :attr:`df`) and normalise it to a SplitPlan."""
        df = self.df if df is None else df
        plan = self._make_splits(df)
        if not isinstance(plan, SplitPlan):
            plan = SplitPlan(splits=plan)
        if plan.df is None:
            plan.df = df
        if self.splits_comment is not None:
            plan.comment = self.splits_comment
        if not plan.comment:
            msg = f"{type(self).__name__}: custom splits need a `splits_comment` (or `SplitPlan(comment=...)`)."
            raise DatasetDefinitionError(msg)
        return plan

    def preview_splits(self, df: pd.DataFrame | None = None) -> pd.DataFrame:
        """One row per outer split with its train/test sizes, and time ranges for a temporal task."""
        plan = self.make_splits(df)
        return split_summary(plan.df, plan.splits, time_on=self.time_on)

    # --- pipeline -----------------------------------------------------------------------------------
    def to_container(self) -> CuratedContainer:
        """Rebuild the frame from the raw data, split it and attach the metadata. Nothing is saved."""
        df, test = self.process()
        plan = self.make_splits(df)
        horizon, unit = _horizon(type(self))
        splits_metadata = PredictiveMLSplitsMetadata(
            splits_comment=plan.comment,
            splits=plan.splits,
            split_random_state=self.SPLIT_RANDOM_STATE,
            time_horizon=horizon,
            time_horizon_unit=unit,
        )
        with _quiet():
            return CuratedContainer(
                dataset=plan.df,
                dataset_metadata=self.dataset_metadata,
                task_metadata=self.task_metadata,
                experiment_metadata=splits_metadata,
                test_dataset=test,
                version_comment=self.dataset_metadata.version_comment,
            )

    def check(self, *, write_report: bool = True, verbose: bool = True) -> CurationResult:
        """Run the full pipeline and the bundle checks without saving (no UUID is kept).

        Writes ``README.md`` unless ``write_report`` is False. The build record of an earlier
        :meth:`build` in the report is kept, and marked stale when the checksum no longer matches.
        """
        self._refresh()
        container = self.to_container()
        result = CurationResult(
            dataset=self,
            container=container,
            bundle_report=self._run_bundle_checks(container, verbose=verbose),
            data_checks=self.run_all_checks(container.dataset),
            decisions=list(self._decisions(self.raw, container.dataset)),
        )
        if write_report:
            self._write_report(result)
        return result

    def build(self, *, verbose: bool = True) -> CurationResult:
        """Run :meth:`check`, fail on bundle-check errors, save the container and verify the export.

        This is the only step that mints a UUID. The report records the UUID, checksum and provenance.
        """
        result = self.check(write_report=False, verbose=verbose)
        result.bundle_report.raise_if_errors()
        with _quiet():
            save_path = result.container.save(resolve_warehouse_dir())
        verify_saved_container(save_path, container=result.container, verbose=verbose).raise_if_errors()
        if verbose:
            print(f"Saved {self.unique_name} as {result.container.uuid} to {save_path}")
        result.saved_path = save_path
        self._write_report(result)
        return result

    def _run_bundle_checks(self, container: CuratedContainer, *, verbose: bool) -> BundleCheckReport:
        accepted = tuple(self.accepted_check_warnings)
        report = run_bundle_checks(container, ignore=accepted, verbose=False)
        # The shared checks judge the v1 split protocol; the v2 protocol checks replace those findings.
        kept = [r for r in report.results if r.slug not in protocol.REPLACED_V1_CHECKS]
        own = [*self._definition_checks(), *protocol.protocol_checks(container), *self._extra_checks(container)]
        extra = [r for r in own if r.slug not in accepted]
        if extra or len(kept) != len(report.results):
            report.results = sorted([*kept, *extra], key=lambda r: SEVERITY_ORDER[r.severity])
        if verbose:
            print(report.summary())
        return report

    def _definition_checks(self) -> list[CheckResult]:
        """Findings about ``dataset.py`` itself: scaffold markers left in the code."""
        source = Path(inspect.getfile(type(self))).read_text().splitlines()
        code = [(i, line.split("#", 1)[0]) for i, line in enumerate(source, start=1)]
        findings = []
        todo = [i for i, line in enumerate(source, start=1) if "TODO(verify)" in line]
        if todo:
            findings.append(
                CheckResult(
                    "definition_todo_left",
                    "error",
                    f"{DEFINITION_FILENAME} still has {len(todo)} `TODO(verify)` marker(s), on line(s) {todo[:20]}.",
                    hint="Resolve each marker (check the data, then write the step or delete the stub).",
                ),
            )
        random = [i for i, line in code if _UNSEEDED.search(line)]
        if random:
            findings.append(
                CheckResult(
                    "definition_nondeterministic",
                    "error",
                    f"{DEFINITION_FILENAME} uses unseeded randomness on line(s) {random[:20]}: "
                    "every run gives other data.",
                    hint="Use `anonymize_ids` for anonymous ids and a fixed `random_state=` / seed for sampling.",
                ),
            )
        return findings

    def _write_report(self, result: CurationResult) -> Path:
        from data_foundry.v2.report import write_report  # noqa: PLC0415 - report imports this module

        return write_report(result, self.report_path)


# --- helpers ------------------------------------------------------------------------------------------


@contextlib.contextmanager
def _quiet():
    """Silence the progress prints of the v1 helpers (checksum, data checks) inside the pipeline."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        yield


@contextlib.contextmanager
def _copy_on_write():
    """Run with pandas copy-on-write, so :func:`_copy` can hand `_clean` a shallow copy of the cached raw data.

    A shallow copy costs no memory up front; a column is copied only when `_clean` changes it, and the cached raw
    data never changes. (Under copy-on-write a chained assignment such as ``df["a"][mask] = x`` does not write;
    use ``df.loc[mask, "a"] = x``.)
    """
    with pd.option_context("mode.copy_on_write", True):  # noqa: FBT003 - pandas option API
        yield


def _copy(raw: Any) -> Any:
    """A shallow copy of the raw data (call under :func:`_copy_on_write`)."""
    if isinstance(raw, (pd.DataFrame, pd.Series)):
        return raw.copy(deep=False)
    if isinstance(raw, dict):
        return {k: _copy(v) for k, v in raw.items()}
    if isinstance(raw, tuple):
        return tuple(_copy(v) for v in raw)
    return raw


def _source(cls: type, name: str) -> str | None:
    try:
        return inspect.getsource(getattr(cls, name))
    except (OSError, TypeError):
        return None


def _drop_unused_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Drop category levels that no longer occur once a frame is sub-sampled (dtypes are set on the full data)."""
    df = df.copy()
    for col in df.columns:
        if isinstance(df[col].dtype, pd.CategoricalDtype):
            df[col] = df[col].cat.remove_unused_categories()
    return df


def _horizon(cls: type[AbstractCuratedDataset]) -> tuple[int | None, str | None]:
    if cls.time_horizon is not None or cls.time_horizon_unit is not None:
        return cls.time_horizon, cls.time_horizon_unit
    if cls.time_on is not None and cls.temporal_splits is not None and cls.temporal_splits.horizon:
        return cls.temporal_splits.horizon
    return None, None


def _regime_tags(cls: type[AbstractCuratedDataset]) -> list[str]:
    tags = list(dict.fromkeys(cls.data_tags))
    if any(tag in REGIME_TAGS for tag in tags):
        return tags
    if cls.time_on is not None:
        regime = ["Non-IID", "Temporal"]
    elif cls.group_on is not None:
        regime = ["Non-IID", "GroupedTemporal" if cls.group_time_on is not None else "Grouped"]
    else:
        regime = ["IID"]
    return regime + tags


def _build_metadata(cls: type[AbstractCuratedDataset]) -> tuple[DatasetMetadata, PredictiveMLTaskMetadata]:
    bibtex = clean_text(cls.bibtex) + "\n"
    key = cls.bibtex_key or ",".join(dict.fromkeys(_BIBTEX_KEY.findall(bibtex)))
    dataset = DatasetMetadata(
        unique_name=cls.unique_name,
        dataset_year=str(cls.year),
        domain_str=cls.domain,
        dataset_source=cls.source,
        original_dataset_source_download_link=cls.source_url,
        download_description=clean_text(cls.download_description),
        academic_reference_bibtex=bibtex,
        academic_reference_bibtex_key=key,
        license=cls.license,
        data_tags=_regime_tags(cls),
        curation_comments=clean_text(cls.curation_comments),
        version_from_unique_name=cls.version_of,
        version_comment=clean_text(cls.version_comment),
    )
    is_classification = cls.problem_type != "regression"
    stratify_on = (cls.target if is_classification else None) if cls.stratify_on is AUTO else cls.stratify_on
    task = PredictiveMLTaskMetadata(
        target_column_name=cls.target,
        problem_type=cls.problem_type,
        objective_metric_name=cls.metric or TABARENA_DEFAULT_METRICS.get(cls.problem_type, ""),
        stratify_on=stratify_on,
        time_on=cls.time_on,
        group_on=cls.group_on,
        group_labels=cls.group_labels,
        group_time_on=cls.group_time_on,
    )
    return dataset, task


_REQUIRED = (
    "unique_name",
    "year",
    "domain",
    "source",
    "source_url",
    "download_description",
    "bibtex",
    "license",
    "target",
    "problem_type",
)


def _validate_definition(cls: type[AbstractCuratedDataset]) -> None:  # noqa: C901, PLR0912 - a flat list of rules
    """Build the metadata of a concrete dataset class and raise :class:`DatasetDefinitionError` on a problem."""
    name = cls.__name__

    def fail(problem: str) -> None:
        raise DatasetDefinitionError(f"{name}: {problem}")

    if "dataset_metadata" in vars(cls) or "task_metadata" in vars(cls):
        fail("declare the metadata as flat attributes (`unique_name = ...`, `target = ...`), not metadata objects.")
    missing = [attr for attr in _REQUIRED if not hasattr(cls, attr)]
    if missing:
        fail(f"missing required attribute(s): {', '.join(missing)}.")
    for seed in ("SHUFFLE_RANDOM_STATE", "SPLIT_RANDOM_STATE"):
        if getattr(cls, seed) != getattr(AbstractCuratedDataset, seed):
            fail(f"`{seed}` is fixed for the whole benchmark; do not override it.")
    for attr in _TEXT_FIELDS:
        value = getattr(cls, attr, None)
        if value is not None and not isinstance(value, str):
            fail(f"`{attr}` must be a string.")
    if isinstance(cls.data_tags, str):
        fail("`data_tags` must be a tuple of tags, not one string.")
    moved = [
        a for a in ("drop_columns", "categorical_features", "string_features", "datetime_features") if a in vars(cls)
    ]
    if moved:
        fail(f"{', '.join(moved)}: drop columns in `_clean` and name dtypes in `_feature_types`.")

    try:
        cls.dataset_metadata, cls.task_metadata = _build_metadata(cls)
    except (ValueError, TypeError) as error:
        fail(f"invalid metadata: {error}")

    source = Path(inspect.getfile(cls))
    if source.name == DEFINITION_FILENAME and source.parent.name != cls.unique_name:
        fail(f"`unique_name={cls.unique_name!r}` must match its folder name {source.parent.name!r}.")

    for slug, reason in cls.accepted_check_warnings.items():
        if not str(reason).strip():
            fail(f"accepted check warning {slug!r} needs a reason.")

    custom_splits = cls._make_splits is not AbstractCuratedDataset._make_splits
    if cls.time_on is not None:
        if not custom_splits and cls.temporal_splits is None:
            fail("a temporal task (`time_on` set) needs `temporal_splits` or `_make_splits`.")
        if _horizon(cls) == (None, None):
            fail("a temporal task needs `time_horizon` and `time_horizon_unit` (or a calendar `temporal_splits`).")
    elif cls.temporal_splits is not None:
        fail("`temporal_splits` is set but `time_on` is not.")
    if (cls.time_horizon is None) != (cls.time_horizon_unit is None):
        fail("set `time_horizon` and `time_horizon_unit` together.")
    if cls.subsample_to_budget and cls.version_of is None:
        fail("`subsample_to_budget` makes a sub-sampled version: set `version_of` (and `version_comment`).")
    if cls.version_of is not None and not clean_text(cls.version_comment or ""):
        fail("a version (`version_of`) needs a `version_comment`.")
    if cls.prepared_raw_files and cls._prepare_raw_files is AbstractCuratedDataset._prepare_raw_files:
        fail("`prepared_raw_files` is set but `_prepare_raw_files` is not implemented.")


def split_summary(df: pd.DataFrame, splits: Splits, *, time_on: str | None = None) -> pd.DataFrame:
    """One row per outer split: repeat, fold, train/test sizes and, with ``time_on``, their time ranges."""
    rows = []
    for repeat, folds in splits.items():
        for fold, (train_idx, test_idx) in folds.items():
            row: dict[str, Any] = {"repeat": repeat, "fold": fold, "n_train": len(train_idx), "n_test": len(test_idx)}
            if time_on is not None:
                times = df[time_on]
                row["train_start"] = times.iloc[train_idx].min()
                row["train_end"] = times.iloc[train_idx].max()
                row["test_start"] = times.iloc[test_idx].min()
                row["test_end"] = times.iloc[test_idx].max()
            rows.append(row)
    return pd.DataFrame(rows)


def provenance(cwd: Path) -> dict[str, str | None]:
    """The data_foundry version and the git commit (with a dirty flag) of the working tree at ``cwd``."""
    try:
        package_version = version("data_foundry")
    except PackageNotFoundError:
        package_version = None

    def git(*args: str) -> str | None:
        try:
            out = subprocess.run(  # noqa: S603 - fixed git subcommands, no user input
                ["git", *args],  # noqa: S607 - git from PATH
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        return out.stdout.strip()

    sha = git("rev-parse", "HEAD")
    if sha is not None and git("status", "--porcelain", "--", ".") not in (None, ""):
        sha += "-dirty"
    return {"data_foundry_version": package_version, "git_sha": sha}
