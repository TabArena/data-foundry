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
  declarative windows of ``temporal`` and the recommended IID/grouped splits do not cover.
* :meth:`~AbstractCuratedDataset._prepare_raw_files` (optional): a heavy one-off step that writes
  intermediate files into the raw directory (listed in ``prepared_raw_files``).
* :meth:`~AbstractCuratedDataset._extra_checks` (optional): dataset-specific checks, such as a leak test.

The base class runs the rest the same way for every dataset: after ``_clean`` it casts the columns
``_feature_types`` names (and a classification target to ``category``), and fixes the row order (the rows in the
order of their content, then a stable sort by the time column for temporal tasks, else a shuffle with seed 42);
then it builds the splits with the benchmark seed, the container, the bundle checks and the report. The pattern
follows TabArena's model interface: declarative class attributes plus a small set of hooks.

Several tasks on the same data form a family: a parent definition (no ``target``; a :class:`DataSummary` instead of a
:class:`TaskSummary`) holds the shared metadata and code, and each task subclasses it in its own folder::

    ExamScores = import_definition("exam_scores")      # the sibling folder's class


    class ExamScoresMath(ExamScores):
        unique_name = "exam_scores_math"               # <parent>_<variant>
        derivation = "The math score as the target."   # how it differs from its parent
        target = "math_score"
        ...

A child may override any hook and call ``super()``; it reads its family's raw files and records its parent in the
container (``derived_from``). A parent is checked as data (:meth:`AbstractCuratedDataset.check_parent`), never built.

From a notebook next to ``dataset.py``::

    from data_foundry.v2 import workbench

    ds = workbench()      # this folder's dataset; picks up edits to dataset.py automatically
    ds.df.head()          # the curated frame
    ds.check()            # the full pipeline and bundle checks, no save; writes README.md
"""

from __future__ import annotations

import ast
import contextlib
import dataclasses
import datetime as dt
import functools
import hashlib
import inspect
import io
import json
import re
import shutil
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import numpy as np
import pandas as pd

from data_foundry.bundle_checks import (
    SEVERITY_ORDER,
    BundleCheckReport,
    CheckResult,
    metric_computes_findings,
    run_bundle_checks,
    verify_saved_container,
)
from data_foundry.curation_container import CuratedContainer
from data_foundry.dataset_checks import run_all_checks
from data_foundry.schema import (
    RETIRED_DATA_TAGS,
    DatasetMetadataV2,
    Grouping,
    MetricSpec,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadataV2,
    RawFile,
    RowBudget,
    ScoringColumn,
    Source,
    TrainSampling,
    UnitWeight,
    as_column_list,
    resolve_warehouse_dir,
    rows_text,
)
from data_foundry.utils.checksum import encode_dataset_v2
from data_foundry.v2 import (
    group_checks,
    splits as protocol,
    task_checks,
)
from data_foundry.v2.metrics import Metric
from data_foundry.v2.preprocessing import (
    PANDAS_3,
    SHUFFLE_RANDOM_STATE,
    canonical_dtypes,
    canonical_nans,
    cast_dtypes,
    content_order,
    order_positions,
    order_rows,
)
from data_foundry.v2.splits import SPLIT_RANDOM_STATE, SplitPlan, Splits, Temporal, TemporalSplits
from data_foundry.v2.windows import Window, candidate_windows, window_stats

if TYPE_CHECKING:
    from data_foundry.schema import SpecialFeature
    from data_foundry.v2.special import SpecialFeatureSpec

DEFINITION_FILENAME = "dataset.py"
"""The file that holds a dataset's definition, one per dataset folder."""

REPORT_FILENAME = "README.md"
"""The generated report next to the definition file: the folder's README, which GitHub shows below its files."""

CLI_COMMAND = ".venv/bin/python -m data_foundry.curation.cli"
"""How the generated pages and messages spell the curation CLI: the repository's own environment, never an install
that happens to be first on PATH."""

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

LINEAGE_COLUMN = "__raw_row__"
"""The column :meth:`AbstractCuratedDataset.process` adds to a one-table raw frame to trace its rows (lineage)."""
_LINEAGE_OFFSET = 7_000_000_000_000
"""The index start of the second lineage try: a reset or rebuilt index falls below it and shows the trace is lost."""


@dataclass(frozen=True)
class RawLineage:
    """Where each row of the curated frame comes from in the raw table: :meth:`AbstractCuratedDataset.process`
    with ``lineage=True``.

    Attributes:
        rows: The raw position (row number in ``raw``, from 0) of each row of the curated frame, in its order; None
            when the rows cannot be traced.
        note: How the rows were traced, or why they could not be.
    """

    rows: np.ndarray | None
    note: str


_TEXT_FIELDS = ("download_description", "curation_comments", "splits_comment", "derivation")


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
        ordinal: Columns cast to an ordered ``category``, as a mapping column -> its levels, lowest first (an ordinal
            scale: a grade, a rating, a stage, bands, a count with an open end). Every value must be one of the
            levels or missing (`set_missing` turns the codes outside the scale into missing values); unused levels
            are removed. A column listed here is ordinal even when ``categorical`` lists it too, which is handy when
            ``categorical`` is computed.
    """

    categorical: tuple[str, ...] | list[str] = ()
    string: tuple[str, ...] | list[str] = ()
    datetime: tuple[str, ...] | list[str] | dict[str, str | None] = ()
    ordinal: dict[str, tuple | list] = field(default_factory=dict)

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


USE_CASE_FITS = ("direct", "approximate", "none")
"""How closely a dataset simulates its use case (:attr:`TaskSummary.fit`)."""

OPTIONAL_SUMMARY_FIELDS = ("changes", "known_at_scoring")
"""The :class:`TaskSummary` fields that may stay empty."""

SUMMARY_MAX_WORDS = 70
"""A field of :class:`TaskSummary` above this many words is flagged (`definition_summary_long`)."""


@dataclass(frozen=True)
class TaskSummary:
    """What the dataset simulates, in plain words, for a reader who has not seen the source.

    Shown first in the generated ``README.md`` ("In brief"): the description, then the judgement of the use case.
    Not stored in the container. The house format and examples are in the knowledge-data-foundry skill
    (``references/definitions.md``, "In brief").

    Attributes:
        question: The prediction as a one-line question ("Will this loan default within a year of its issue?").
        use_case: Who uses the prediction, when, and the decision it informs.
        row: What one row is.
        predicted: The target in plain words: what, by when after the prediction point, its classes or unit.
        known: What the model knows at the prediction point, in plain words (no column names).
        split: What the test data stands for (new customers, the next two weeks, unseen patients) and how it is
            drawn.
        fit: The judgement: ``"direct"`` (rows, features and split mirror the use case), ``"approximate"`` (a
            stand-in with a known gap) or ``"none"`` (no decision fits; such a dataset is retired, not shipped).
        fit_reason: Why, in one or two sentences: the gap for ``"approximate"``, what is missing for ``"none"``.
        changes: Our changes to the source a reader needs to know, in plain words ("" when there are none).
        known_at_scoring: What the scorer knows that the model does not, in plain words ("" when it knows only the
            target): a metric input recorded with the outcome, such as the time on risk a rate is weighted by, read
            with the test rows' labels and never when predicting (MET-15).
    """

    question: str
    use_case: str
    row: str
    predicted: str
    known: str
    split: str
    fit: str
    fit_reason: str
    changes: str = ""
    known_at_scoring: str = ""

    def fields(self) -> dict[str, str]:
        """The text fields, dedented, in display order."""
        names = (
            "question",
            "use_case",
            "row",
            "predicted",
            "known",
            "known_at_scoring",
            "split",
            "changes",
            "fit_reason",
        )
        return {name: clean_text(getattr(self, name)) or "" for name in names}


@dataclass(frozen=True)
class DataSummary:
    """What the data is, in plain words and independent of one task: the summary of a parent definition.

    A parent (a definition without a ``target``) declares it; its children inherit it, and their ``README.md`` shows
    it above their own :class:`TaskSummary`. Not stored in the container.

    Attributes:
        data: What was measured or recorded, by whom, where and when.
        row: What one row is.
        goals: The use cases the data serves, independent of one task: who would predict what from it, and why.
        limits: Known gaps and biases a task built on it inherits ("" when there are none).
    """

    data: str
    row: str
    goals: str
    limits: str = ""

    def fields(self) -> dict[str, str]:
        """The text fields, dedented, in display order."""
        return {name: clean_text(getattr(self, name)) or "" for name in ("data", "row", "goals", "limits")}


NON_FEATURE_REASONS = ("outcome", "provenance", "identifier", "other")
"""Why a column is kept but never a feature (:class:`NonFeature`)."""


@dataclass(frozen=True)
class NonFeature:
    """A column a definition keeps in its frame but no task may use as a feature, with the reason.

    A parent declares them in ``non_features``; its children inherit the declarations, and every task drops the
    declared columns after ``_clean`` unless it gives one a role (its target, its group key, a scoring or weight
    column). A child may extend the declarations, never remove one.

    Attributes:
        column: The column of the frame.
        reason: ``"outcome"`` (a result measured with or after the target: a sibling target), ``"provenance"`` (where
            the row comes from: a file, a row number, an id; :func:`~data_foundry.v2.preprocessing.provenance_columns`),
            ``"identifier"`` (a key with no meaning as an input, sequential ids among them) or ``"other"``.
        description: What the column is and why it is no feature; required for ``"other"``.
    """

    column: str
    reason: str
    description: str = ""


@dataclass
class CurationResult:
    """The outcome of :meth:`AbstractCuratedDataset.check` or :meth:`AbstractCuratedDataset.build`.

    Attributes:
        dataset: The dataset definition that produced this result.
        container: The curated container (a fresh UUID unless it was saved).
        bundle_report: The bundle-check report, with the definition and extra checks merged in.
        data_checks: The tables of :func:`~data_foundry.dataset_checks.run_all_checks`, by name.
        decisions: The curation decisions of :meth:`AbstractCuratedDataset._decisions`, with their evidence.
        group_stats: The group statistics of a grouped task (:mod:`data_foundry.v2.group_checks`), else None.
        saved_path: Where the container was saved, or None for a check without saving.
        created_at: When the result was produced (UTC).
    """

    dataset: AbstractCuratedDataset
    container: CuratedContainer
    bundle_report: BundleCheckReport
    data_checks: dict[str, pd.DataFrame] = field(default_factory=dict)
    decisions: list[Decision] = field(default_factory=list)
    group_stats: group_checks.GroupStats | None = None
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


@dataclass
class ParentCheckResult:
    """The outcome of :meth:`AbstractCuratedDataset.check_parent`: a parent checked as data.

    Attributes:
        dataset: The parent definition.
        frame: Its frame, in content order.
        data_checksum: :func:`data_checksum` of the frame.
        findings: The definition findings (markers, nondeterminism, summary, a parent without children).
        children: The ``unique_name`` of each definition that derives from it directly, found next to it.
        raw_files: The raw-file manifest of its sources (:meth:`AbstractCuratedDataset.raw_manifest`).
        created_at: When the result was produced (UTC).
    """

    dataset: AbstractCuratedDataset
    frame: pd.DataFrame
    data_checksum: str
    findings: list[CheckResult] = field(default_factory=list)
    children: list[str] = field(default_factory=list)
    raw_files: list[RawFile] = field(default_factory=list)
    created_at: dt.datetime = field(default_factory=lambda: dt.datetime.now(dt.timezone.utc))

    @property
    def ok(self) -> bool:
        """Whether no finding is an error."""
        return not any(f.severity == "error" for f in self.findings)


class DatasetDefinitionError(TypeError):
    """A dataset class is missing a declaration or declares an inconsistent one."""


class AbstractCuratedDataset(ABC):
    """Base class of a curated dataset definition. Subclass it once per dataset, in ``dataset.py``.

    Multi-line text attributes may be indented like code; they are dedented (:func:`clean_text`). The class
    is validated when it is defined, so importing ``dataset.py`` already fails on a missing or inconsistent
    declaration. The metadata objects saved with the container are built from the attributes and are
    available as ``dataset_metadata`` and ``task_metadata``.
    """

    # --- in brief ---------------------------------------------------------------------------------
    task_summary: ClassVar[TaskSummary | None] = None
    """What the dataset simulates, in plain words, and how closely (:class:`TaskSummary`); first in the README."""
    data_summary: ClassVar[DataSummary | None] = None
    """What the data is, independent of one task (:class:`DataSummary`): required on a parent (a definition without
    a ``target``), inherited by its children."""

    # --- family -------------------------------------------------------------------------------------
    non_features: ClassVar[tuple[NonFeature, ...]] = ()
    """Columns kept in the frame that no task may use as a feature (:class:`NonFeature`): the outcomes a task does not
    predict, provenance, identifiers. Inherited; every task drops them after ``_clean`` unless it gives one a role (its
    target, group key, scoring or weight column)."""
    derivation: ClassVar[str | None] = None
    """For a child (a class derived from another definition, ``class Math(import_definition("exam_scores"))``): how it
    differs from its parent, in one or two sentences (another target, split or preprocessing). Required on a child,
    refused on a definition without a parent."""

    # --- dataset ------------------------------------------------------------------------------------
    unique_name: ClassVar[str]
    """Snake-case name; equal to the folder name. A version sub-sampled to a :attr:`row_budget` is named
    ``<name>_<suffix>`` after its train budget (``_1m``, ``_10m``) and reads the raw files of ``<name>``."""
    domain: ClassVar[str]
    """One of :data:`data_foundry.schema.Domain`."""
    sources: ClassVar[tuple[Source, ...]]
    """Where the data comes from (:class:`~data_foundry.schema.Source`), the publication first::

        sources = (
            Source(role="publication", platform="UCI", url="https://doi.org/...", license="CC BY 4.0", year="2014",
                   bibtex=\"\"\"@misc{...}\"\"\"),
            Source(role="copy", platform="Kaggle", url="https://www.kaggle.com/...", license="CC0 1.0"),
        )

    The publication is where the data were first published, not a later re-upload; its ``year`` (a competition's
    launch, a dataset's release or donation, the online date of the paper or supplement that holds the rows, not the
    year of collection) and ``bibtex`` are the dataset's. A ``part`` is a piece the dataset is assembled from (each
    with its own license), a ``copy`` a later copy of the data, such as the one we download."""
    download_description: ClassVar[str]
    """Commands (and notes) that recreate the raw files in ``local-data-warehouse/<unique_name>/``."""
    data_tags: ClassVar[tuple[str, ...]] = ()
    """Context tags (``Spatial``, ``Anonymized``, ...). The regime tags (``IID`` or ``Non-IID`` plus
    ``Temporal``/``Grouped``) are added from the task unless one is listed here."""
    curation_comments: ClassVar[str] = ""
    """The audit trail: the starting artifact, then one bullet per non-obvious decision."""

    # --- task ---------------------------------------------------------------------------------------
    target: ClassVar[str]
    """The target column."""
    problem_type: ClassVar[str]
    """``binary_classification``, ``multiclass_classification`` or ``regression``."""
    metric: ClassVar[Metric]
    """Required: the metric that scores the task (:class:`~data_foundry.v2.metrics.Metric`). The source's metric
    when it defines one (``Metric.source("rmse", original="RMSE", reference=...)``), the closest computable one to an
    original that cannot be computed (``Metric.stand_in(...)``), else ``Metric.fallback(reason=...)`` (roc_auc /
    log_loss / rmse by problem type, and where we looked)."""
    scoring_columns: ClassVar[tuple[ScoringColumn, ...]] = ()
    """The columns the metric needs (``ScoringColumn(column=..., role=..., used_by=..., description=...)``, e.g.
    Numerai's ``era`` as the ``group`` of a per-era correlation): kept in the frame, never model features. Each one is
    an input of the metric (``Metric.source(..., inputs={"group": "era"})``)."""
    sample_weight: ClassVar[str | None] = None
    """The training weight, a scoring column every model is fitted with as each row's weight, never a feature: the
    metric's row weight (``inputs={"weight": col}``). Declare it when the weight is a realized amount at risk, the
    denominator of a rate target (the years insured of a claims-per-year target, MET-15); a weight that is a function
    of the features (a sum insured) needs none. ``None``: models train unweighted."""
    unit_weight: ClassVar[UnitWeight | None] = None
    """A score that counts each unit once (MET-17): ``UnitWeight(column="plot_weight", unit="plot")``, the metric's
    weight scoring column (1 over the unit's rows, ``inputs={"weight": column}``) and the column naming the unit, kept
    in the frame as metadata, never a feature. For scoring and validation only, never a ``sample_weight``; the check
    tests that each unit's weights sum to 1. Downstream tools read it to weight their validation loss alike."""
    special_features: ClassVar[tuple[SpecialFeatureSpec, ...]] = ()
    """Model inputs that need handling beyond their dtype, declared like the target. Each entry is one special
    feature, in one of two layouts (:mod:`data_foundry.v2.special`):

    * one column (:class:`~data_foundry.v2.special.SpecialColumn`): ``Smiles(column="SMILES")``, a molecule's
      structure (CLEAN-24), cast to ``string``; ship the form :func:`~data_foundry.v2.chemistry.canonical_smiles`
      gives;
    * a group of columns that hold one object together (:class:`~data_foundry.v2.special.SpecialColumnGroup`):
      ``Spectrum(name="serum_ms", prefix="M/Z:", unit="m/z", technique=..., state=..., description=...)``, one column
      per position on a spectrum's axis, named ``<prefix><position>`` (CLEAN-26); never process them in ``_clean``.

    The container records each as a :class:`~data_foundry.schema.SpecialFeature` (kind, layout, columns, the
    recommended encoding), so a benchmark encodes it by its kind. Leave the columns out of :meth:`_feature_types`."""
    stratify_on: ClassVar[Any] = AUTO
    """Column(s) to stratify on. Default: the target for classification, nothing for regression."""
    grouping: ClassVar[Grouping | None] = None
    """A grouped task: ``Grouping(on=..., labels=..., definition=..., prediction_unit=..., aggregation=...,
    context=..., time_on=...)`` (:class:`~data_foundry.schema.Grouping`). The ``definition`` (what a group is, why
    it is held out, the use case with its source) is required and may be indented like code. Stored in the container."""
    temporal: ClassVar[Temporal | None] = None
    """A temporal task: ``Temporal(on=..., splits=TemporalSplits(...))`` (:class:`~data_foundry.v2.splits.Temporal`),
    plus ``horizon=..., horizon_unit=...`` when the windows do not fix the horizon. Neither ``grouping`` nor
    ``temporal``: an IID task."""

    # --- row order ----------------------------------------------------------------------------------
    shuffle: ClassVar[bool] = True
    """Put the rows in the order of their content, then shuffle IID and grouped data (seed 42) as the last step;
    temporal data is sorted by time, ties in content order. False keeps the order ``_clean`` returns."""

    # --- splits -------------------------------------------------------------------------------------
    splits_comment: ClassVar[str | None] = None
    """What the splits simulate. None: the default comment for recommended or declarative splits."""
    row_budget: ClassVar[RowBudget | None] = None
    """The benchmark's row budget, for data larger than it. None (the default): no budget, the splits use the full
    frame and no side is capped.

    ``RowBudget(train=..., test=...)`` makes a version named ``<name>_<suffix>`` after its train budget
    (:attr:`~data_foundry.schema.RowBudget.suffix`), and the container records the budget
    (``experiment_metadata.row_budget``) with how to sub-sample to it (``experiment_metadata.train_sampling``,
    :meth:`train_sampling`). Only the test sides are sampled in the container: each temporal test window, or each
    IID / grouped fold's test third, keeps at most ``test`` rows (whole groups, stratified; whole time values with
    ``TemporalSplits(sample_by="time")``). The train sides keep every row available to them, all history before a
    window, and a benchmark sub-samples them to ``train`` rows before a fit
    (:func:`~data_foundry.v2.splits.subsample_train`: the newest year at random for temporal data). TabArena v0.2 uses
    ``RowBudget(train=1_000_000, test=500_000)``; a budget that changes nothing (no test side over ``test`` and no
    train side over ``train``) is refused (take the dataset fully)."""

    # --- checks and raw files ----------------------------------------------------------------------
    accepted_check_warnings: ClassVar[dict[str, str]] = {}
    """Bundle-check slugs accepted on purpose, each with the reason it is correct for this dataset."""
    prepared_raw_files: ClassVar[tuple[str, ...]] = ()
    """Files :meth:`_prepare_raw_files` writes into :attr:`raw_dir`; it runs when any is missing or when its code
    (the method and the helpers of ``dataset.py`` it calls) changed since they were written."""

    # --- fixed seeds (one per benchmark, never per dataset) ----------------------------------------
    SHUFFLE_RANDOM_STATE: ClassVar[int] = SHUFFLE_RANDOM_STATE
    SPLIT_RANDOM_STATE: ClassVar[int] = SPLIT_RANDOM_STATE

    # --- built from the attributes -----------------------------------------------------------------
    dataset_metadata: ClassVar[DatasetMetadataV2]
    task_metadata: ClassVar[PredictiveMLTaskMetadataV2]

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

        The default is the v2 protocol (:mod:`data_foundry.v2.splits`): the windows of ``temporal.splits`` for a
        temporal task, else the recommended IID or grouped 3-fold cross-validation, both fitted to the
        :attr:`row_budget` of a sub-sampled version. Override it only for a split none of these express, and return a
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
        if "unique_name" not in vars(cls) and inspect.isabstract(cls):
            return  # a helper base class, not a definition
        _validate_definition(cls)
        # the source as loaded: `reload` compares against it (the file may already hold the edited text)
        cls._loaded_sources = {name: _source(cls, name) for name in ("_load_raw", "_prepare_raw_files")}

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
    def is_task(self) -> bool:
        """Whether this definition is a task (it declares a ``target``), not a parent of tasks."""
        return is_task(type(self))

    @property
    def folder(self) -> Path | None:
        """The folder holding this dataset's ``dataset.py`` (and any sibling files it reads); None for a class defined
        elsewhere (a notebook, a script). A parent's hooks that read a file next to the parent's own ``dataset.py``
        use ``Path(__file__).parent``, since ``folder`` is the folder of the class that runs them.
        """
        file = definition_file(type(self))
        return None if file is None else file.parent

    @property
    def raw_dir(self) -> Path:
        """Where the raw download lives: ``<warehouse>/<raw_name>`` (:func:`raw_name`)."""
        return resolve_warehouse_dir() / raw_name(type(self))

    @property
    def report_path(self) -> Path | None:
        """The generated ``README.md`` next to ``dataset.py`` (None for a class defined in a notebook)."""
        return None if self.folder is None else self.folder / REPORT_FILENAME

    # --- reloading ----------------------------------------------------------------------------------
    def _definition_mtime(self) -> tuple[float, ...] | None:
        """The modification times of the definition files of the class and its parents (:func:`definition_files`)."""
        try:
            return tuple(file.stat().st_mtime for file in definition_files(type(self)))
        except OSError:
            return None

    def reload(self) -> AbstractCuratedDataset:
        """Re-import ``dataset.py`` in place. Returns ``self``.

        The cached raw data is kept when ``_load_raw`` and ``_prepare_raw_files`` are unchanged, so
        iterating on ``_clean`` or the declarations never re-reads the files.
        """
        from data_foundry.v2.registry import load_definition  # noqa: PLC0415 - the registry imports this module

        old = type(self)
        file = definition_file(old)
        if file is None:  # a class defined in a notebook: re-run its cell instead
            return self
        new = load_definition(file)  # imports the parents again too (`import_definition`)
        loaded = getattr(old, "_loaded_sources", {})
        keep_raw = all(loaded.get(name) == new._loaded_sources[name] for name in new._loaded_sources)
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
        """Run :meth:`_prepare_raw_files` when a file in :attr:`prepared_raw_files` is missing, when its code changed
        since the files were written, or with ``force``.

        The hash of the code is kept in :data:`PREPARED_MARKER` next to the files; files without one (written before
        2026-10-06) count as written by other code, so the step runs once more.
        """
        if not self.prepared_raw_files:
            return
        marker = self.raw_dir / PREPARED_MARKER
        code = _prepare_code_hash(type(self))
        missing = [name for name in self.prepared_raw_files if not (self.raw_dir / name).exists()]
        written_by = json.loads(marker.read_text()).get("code_hash") if marker.exists() else None
        if force or missing or written_by != code:
            if not missing and not force:
                print(
                    f"{self.unique_name}: `_prepare_raw_files` changed since its files were written; running it again."
                )
            self._prepare_raw_files(self.raw_dir)
            marker.write_text(json.dumps({"code_hash": code, "files": list(self.prepared_raw_files)}, indent=1))

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

    def process(self, *, lineage: bool = False) -> tuple:
        """Run :meth:`_clean` on a copy of :attr:`raw`, then the standard steps. Returns (dataset, test_dataset).

        With ``lineage``, returns (dataset, test_dataset, :class:`RawLineage`): the raw position of every row of
        the dataset. It traces a one-table raw frame through ``_clean`` by a column (:data:`LINEAGE_COLUMN`), or,
        when ``_clean`` drops that column (it selects columns), by the index; the standard steps' row order is then
        applied to the positions. A trace counts only when the traced run gives the same dataset as :attr:`df`, so
        a ``_clean`` that reads the extra column or the index (``drop_duplicates()`` over all columns, an aligned
        assignment) gives no lineage rather than wrong lineage. A raw dict or tuple of tables gives none either.
        """
        if lineage:
            return self._process_with_lineage()
        with _copy_on_write():
            cleaned = self._clean(_copy(self.raw))
            df, test = cleaned if isinstance(cleaned, tuple) else (cleaned, None)
            df, test = self._drop_non_features(df, test)
            self._check_declared_columns(df)
            df = self._standardize(df)
            if test is not None:
                test = _categories_like(self._standardize(test, order=False), df)
        return df, test

    def _process_with_lineage(self) -> tuple[pd.DataFrame, pd.DataFrame | None, RawLineage]:
        raw = self.raw
        if not isinstance(raw, pd.DataFrame):
            df, test = self.process()
            return df, test, RawLineage(None, "the raw data is not one table")
        reference = self.df
        tried = []
        for how in ("column", "index"):
            try:
                traced = self._clean_traced(raw, how)
            except Exception as err:  # noqa: BLE001 - a `_clean` check of the source's shape fails on the tagged frame
                # a real error of the definition is raised again by the untraced `process()` below
                tried.append(f"`_clean` fails on the frame tagged by the {how} ({type(err).__name__})")
                continue
            if traced is None:
                tried.append(f"the {how} does not survive `_clean`")
                continue
            df, test, rows = traced
            if df.equals(reference):
                return df, test, RawLineage(rows, f"traced by the {how}")
            tried.append(f"tracing by the {how} changes what `_clean` returns")
        df, test = self.process()
        return df, test, RawLineage(None, "; ".join(tried))

    def _clean_traced(self, raw: pd.DataFrame, how: str) -> tuple[pd.DataFrame, pd.DataFrame | None, np.ndarray] | None:
        """:meth:`process` on ``raw`` tagged by a lineage column or index; None when ``_clean`` drops the tag."""
        n = len(raw)
        with _copy_on_write():
            tagged = _copy(raw)
            if how == "column":
                if LINEAGE_COLUMN in tagged.columns:
                    return None
                tagged[LINEAGE_COLUMN] = np.arange(n)
            else:
                tagged.index = pd.RangeIndex(_LINEAGE_OFFSET, _LINEAGE_OFFSET + n)
            cleaned = self._clean(tagged)
            df, test = cleaned if isinstance(cleaned, tuple) else (cleaned, None)
            if how == "column":
                if LINEAGE_COLUMN not in df.columns:
                    return None
                rows = pd.to_numeric(df.pop(LINEAGE_COLUMN), errors="coerce").to_numpy(dtype=float)
                if test is not None and LINEAGE_COLUMN in test.columns:
                    test = test.drop(columns=[LINEAGE_COLUMN])
            else:
                if not pd.api.types.is_integer_dtype(df.index):
                    return None
                rows = df.index.to_numpy(dtype=float) - _LINEAGE_OFFSET
                df = df.reset_index(drop=True)
            if not len(rows) or np.isnan(rows).any() or rows.min() < 0 or rows.max() >= n:
                return None
            df, test = self._drop_non_features(df, test)
            self._check_declared_columns(df)
            df, positions = self._standardize(df, positions=True)
            if test is not None:
                test = _categories_like(self._standardize(test, order=False), df)
        return df, test, rows.astype(np.int64)[positions]

    def _drop_non_features(
        self, df: pd.DataFrame, test: pd.DataFrame | None
    ) -> tuple[pd.DataFrame, pd.DataFrame | None]:
        """Check the columns this class declares as non-features, count the rows per raw file, and for a task drop
        every declared non-feature it gives no role (:attr:`non_features`).
        """
        own = vars(type(self)).get("non_features", ())
        inherited = {nf.column for k in type(self).__mro__[1:] for nf in vars(k).get("non_features", ())}
        missing = [nf.column for nf in own if nf.column not in inherited and nf.column not in df.columns]
        if missing:
            msg = f"{type(self).__name__}: `non_features` names {missing}, which `_clean` does not return."
            raise DatasetDefinitionError(msg)
        if "source_file" in df.columns:  # the rows each raw file gave, for the manifest
            self._rows_per_file = {str(k): int(v) for k, v in df["source_file"].value_counts(sort=False).items()}
        if not self.is_task:
            return df, test
        roles = self._column_roles()
        dropped = [nf for nf in self.non_features if nf.column in df.columns and nf.column not in roles]
        self._dropped_non_features = dropped
        columns = [nf.column for nf in dropped]
        if test is not None:
            test = test.drop(columns=[c for c in columns if c in test.columns])
        return df.drop(columns=columns), test

    @property
    def dropped_non_features(self) -> list[NonFeature]:
        """The declared non-features the last run of :meth:`process` dropped (a task's; a parent drops none)."""
        return list(getattr(self, "_dropped_non_features", ()))

    def _column_roles(self) -> set[str]:
        """The columns a task uses other than as features: target, split keys, scoring and weight columns."""
        task = self.task_metadata
        roles = {task.target_column_name, *as_column_list(task.group_on), *as_column_list(task.group_time_on)}
        roles |= {task.time_on} - {None}
        roles |= {c.column for c in task.scoring_columns}
        roles |= {task.sample_weight} - {None}
        if task.unit_weight is not None:
            roles |= {task.unit_weight.column, task.unit_weight.unit}
        return roles

    def _check_declared_columns(self, df: pd.DataFrame) -> None:
        """Fail with the attribute's name when a declared column is missing, or a split key has missing values."""
        if not self.is_task:  # a parent declares no task columns
            self.special_feature_records(df)
            return
        task = self.task_metadata
        declared = {"target": [task.target_column_name], "stratify_on": as_column_list(task.stratify_on)}
        if self.temporal is not None:
            declared["temporal.on"] = [self.temporal.on]
        if self.grouping is not None:
            declared["grouping.on"] = as_column_list(self.grouping.on)
            declared["grouping.time_on"] = as_column_list(self.grouping.time_on)
        declared["scoring_columns"] = [c.column for c in task.scoring_columns]
        declared["sample_weight"] = as_column_list(task.sample_weight)
        if task.unit_weight is not None:
            declared["unit_weight"] = [task.unit_weight.column, task.unit_weight.unit]
        self.special_feature_records(df)  # every declared special feature finds its columns
        declared["metric inputs"] = list(task.objective_metric.inputs.values())
        for attribute, columns in declared.items():
            missing = [c for c in columns if c not in df.columns]
            if missing:
                msg = f"{type(self).__name__}: `{attribute}` names {missing}, which `_clean` does not return."
                raise DatasetDefinitionError(msg)
        for attribute in ("temporal.on", "grouping.on"):
            empty = [c for c in declared.get(attribute, []) if df[c].isna().any()]
            if empty:
                msg = (
                    f"{type(self).__name__}: the split key `{attribute}` = {empty} has missing values "
                    f"({int(df[empty].isna().any(axis=1).sum()):,} rows); drop or fill them in `_clean`."
                )
                raise DatasetDefinitionError(msg)

    def _standardize(self, df: pd.DataFrame, *, order: bool = True, positions: bool = False) -> Any:
        """The standard steps: dtypes, canonical missing values, then (``order``) the row order of :func:`order_rows`.

        With ``positions``, returns (frame, positions): the frame's rows are the input's rows at those positions.
        """
        types = self.feature_types(df)
        if order:  # the full cleaned frame, before its dtypes are cast; the README lists these types
            self._applied_feature_types = types
        present = set(df.columns)
        # a name that is not in the frame is a misspelling and fails the cast; the non-features a task dropped are not
        dropped = {nf.column for nf in getattr(self, "_dropped_non_features", ())} - present

        def keep(c: str) -> bool:
            return c in present or (order and c not in dropped)

        df = cast_dtypes(
            df,
            categorical=[c for c in types.categorical if keep(c)],
            ordinal={c: levels for c, levels in types.ordinal.items() if keep(c)},
            string=[c for c in (*types.string, *self._special_columns(df, "string")) if keep(c)],
            datetime={c: f for c, f in types.datetime_formats.items() if keep(c)},
        )
        df = canonical_nans(canonical_dtypes(df))
        if not order:
            return df.reset_index(drop=True)
        if not self.is_task:  # a parent's frame: in the order of its content, which no task order depends on
            at = content_order(df)
            return (df.iloc[at].reset_index(drop=True), at) if positions else df.iloc[at].reset_index(drop=True)
        if positions:
            at = order_positions(df, time_on=self.task_metadata.time_on, shuffle=self.shuffle)
            return df.iloc[at].reset_index(drop=True), at
        return order_rows(df, time_on=self.task_metadata.time_on, shuffle=self.shuffle)

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
        if types.ordinal:  # an ordinal column may also be named among the categorical ones; it is ordinal
            types = FeatureTypes(
                categorical=[c for c in types.categorical if c not in types.ordinal],
                string=types.string,
                datetime=types.datetime,
                ordinal=types.ordinal,
            )
        listed = {*types.categorical, *types.string, *types.datetime_formats, *types.ordinal}
        special = set(self._special_columns(df))
        if listed & special:
            msg = (
                f"{type(self).__name__}: {sorted(listed & special)[:5]} is a column of a special feature "
                "(`special_features`), which types it; leave it out of `_feature_types`."
            )
            raise DatasetDefinitionError(msg)
        if (
            self.is_task
            and self.problem_type != "regression"
            and self.target not in listed
            and self.target in df.columns
        ):
            types = FeatureTypes(
                categorical=(*types.categorical, self.target),
                string=types.string,
                datetime=types.datetime,
                ordinal=types.ordinal,
            )
        return types

    def special_feature_records(self, df: pd.DataFrame) -> list[SpecialFeature]:
        """The container's records of the definition's ``special_features`` for the columns of ``df``, in order.

        Raises:
            DatasetDefinitionError: A special feature does not find its columns in ``df``.
        """
        from data_foundry.v2.special import SpecialFeatureError  # noqa: PLC0415 - special imports this module's users

        try:
            return [spec.record(df.columns) for spec in self.special_features]
        except SpecialFeatureError as error:
            raise DatasetDefinitionError(f"{type(self).__name__}: {error}") from error

    def _special_columns(self, df: pd.DataFrame, dtype: str | None = None) -> list[str]:
        """The columns of the special features in ``df`` (only those whose kind casts to ``dtype``, when given)."""
        specs = [s for s in self.special_features if dtype is None or s.dtype == dtype]
        names = list(df.columns)
        return [c for spec in specs for c in self._resolve(spec, names)]

    def _resolve(self, spec: SpecialFeatureSpec, names: list[str]) -> list[str]:
        from data_foundry.v2.special import SpecialFeatureError  # noqa: PLC0415

        try:
            return spec.resolve(names)[0]
        except SpecialFeatureError as error:
            raise DatasetDefinitionError(f"{type(self).__name__}: {error}") from error

    def task_metadata_for(self, df: pd.DataFrame) -> PredictiveMLTaskMetadataV2:
        """:attr:`task_metadata` with the special features of ``df`` (a group's columns depend on the frame)."""
        if not self.special_features:
            return self.task_metadata
        return dataclasses.replace(self.task_metadata, special_features=self.special_feature_records(df))

    @property
    def df(self) -> pd.DataFrame:
        """The curated frame (after the standard steps), cached until the definition changes.

        Explore it freely: it is a copy that shares no memory with the cached raw data, and :meth:`check` and
        :meth:`build` rebuild the frame from the raw data and never use this cached copy.
        """
        self._refresh()
        if self._df_cache is None:
            df, test = self.process()
            self._df_cache = (df.copy(deep=True), None if test is None else test.copy(deep=True))
        return self._df_cache[0]

    @property
    def test_df(self) -> pd.DataFrame | None:
        """The unlabeled test set, if `_clean` returned one."""
        _ = self.df
        return self._df_cache[1]

    def run_all_checks(self, df: pd.DataFrame | None = None) -> dict[str, pd.DataFrame]:
        """Run the exploratory :func:`~data_foundry.dataset_checks.run_all_checks` tables on ``df``."""
        df = self.df if df is None else df
        options = ("display.max_rows", "display.max_columns", "display.width", "display.max_colwidth")
        restore = [x for name in options for x in (name, pd.get_option(name))]
        try:
            with _quiet(), pd.option_context(*restore):  # run_all_checks sets the display options globally
                tables = run_all_checks(
                    data=df,
                    target_feature=self.target,
                    problem_type=self.problem_type,
                    print_report=False,
                )
        except (TypeError, ValueError) as error:  # an object column or a wrong class count: the bundle checks say so
            return {"error": pd.DataFrame({"data checks not run": [f"{type(error).__name__}: {error}"]})}
        return dict(zip(("head", "summary", "numeric_stats", "cat_stats", "target"), tables, strict=True))

    # --- splits -------------------------------------------------------------------------------------
    def default_splits(self, df: pd.DataFrame) -> SplitPlan:
        """The default of :meth:`_make_splits`: the v2 split protocol (:mod:`data_foundry.v2.splits`).

        The splits are the declarative temporal windows, or the recommended IID / grouped 3-fold cross-validation, on
        the full frame. A version with a :attr:`row_budget` samples only its test sides to ``row_budget.test``: a
        temporal version each test window (:func:`~data_foundry.v2.splits.sample_temporal_splits`, the frame keeps the
        rows a split uses), an IID or grouped one each fold's test third, whose left-out rows train in that fold
        (:func:`~data_foundry.v2.splits.fit_splits_to_budget`). The train sides keep every row available to them; a
        benchmark sub-samples them to ``row_budget.train`` (:func:`~data_foundry.v2.splits.subsample_train`).
        """
        task = self.task_metadata
        temporal = task.time_on is not None
        budget = self.row_budget
        if budget is None:
            if temporal:
                splits, comment = self._window_splits(df)
                return SplitPlan(splits=splits, comment=comment)
            return SplitPlan(splits=self._cross_validation(df), comment=DEFAULT_SPLITS_COMMENT)

        train_budget, test_budget = rows_text(budget.train), rows_text(budget.test)
        sampled_by = self._train_sampling_text(df)
        if temporal:
            splits, comment = self._window_splits(df)
            by_time = self.temporal.splits.sample_by == "time"
            df, splits, trimmed = protocol.sample_temporal_splits(
                df,
                splits,
                budget,
                stratify_on=None if by_time else task.stratify_on,
                whole_values_of=task.time_on if by_time else None,
                random_state=self.SPLIT_RANDOM_STATE,
            )
            drawn = f", drawn as whole values of `{task.time_on}`" if by_time else ", drawn at random"
            comment += (
                f" Each test window keeps at most {test_budget} of its rows{drawn}; each train side holds every "
                f"earlier row, and a benchmark sub-samples it to {train_budget} rows ({sampled_by})."
            )
            df = _drop_unused_categories(df)
        else:
            splits, trimmed = protocol.fit_splits_to_budget(
                df,
                self._cross_validation(df),
                budget,
                group_on=task.group_on,
                stratify_on=task.stratify_on,
                random_state=self.SPLIT_RANDOM_STATE,
            )
            whole = " (whole groups)" if task.group_on is not None else ""
            comment = (
                f"{DEFAULT_SPLITS_COMMENT} Each fold tests on at most {test_budget} rows of its third{whole} and "
                f"trains on every other row; a benchmark sub-samples the train side to {train_budget} rows "
                f"({sampled_by})."
            )
        longest_train = max(len(train) for folds in splits.values() for train, _test in folds.values())
        if not trimmed and longest_train <= budget.train:
            msg = (
                f"{type(self).__name__}: the frame has {len(df):,} rows and no split side exceeds the row budget "
                f"({train_budget} train, {test_budget} test rows). Take the dataset fully: drop `row_budget` and the "
                f"`_{budget.suffix}` version."
            )
            raise DatasetDefinitionError(msg)
        return SplitPlan(splits=splits, df=df, comment=comment)

    def train_sampling(self, df: pd.DataFrame | None = None) -> TrainSampling | None:
        """How a benchmark sub-samples this dataset's train sides to ``row_budget.train`` (None without a budget).

        A temporal task: the newest year, extended back in time until it holds ``row_budget.train`` rows, and a random
        sample of those (the year of a numeric time column from ``Temporal(time_unit=...)``). IID and grouped tasks: at
        random. Whole groups for a grouped task, whole time values with ``TemporalSplits(sample_by="time")``;
        stratified like the splits.
        """
        if self.row_budget is None:
            return None
        task = self.task_metadata
        by_time = self._samples_by_time()
        if task.time_on is not None:
            self._check_time_unit((self.df if df is None else df)[task.time_on])
        unit = "time_values" if by_time else ("groups" if task.group_on is not None else "rows")
        return TrainSampling(
            default="newest_year" if task.time_on is not None else "random",
            unit=unit,
            stratify_on=None if by_time else task.stratify_on,
        )

    def _samples_by_time(self) -> bool:
        """Whether the splits sample whole values of the time column (``TemporalSplits(sample_by="time")``)."""
        windows = self.temporal.splits if self.temporal is not None else None
        return windows is not None and windows.sample_by == "time"

    def _train_sampling_text(self, df: pd.DataFrame) -> str:
        """How the default sampler (:meth:`train_sampling`) draws a train side of ``df``, for the splits comment."""
        sampling = self.train_sampling(df)
        unit = {"rows": "rows", "groups": "whole groups", "time_values": "whole values of the time column"}
        where = ""
        if sampling.default == "newest_year":
            where = " from the newest year before each window, extended back in time until it holds that many rows"
        return f"by default {unit[sampling.unit]} drawn at random{where}, `subsample_train`"

    def _window_splits(self, df: pd.DataFrame) -> tuple[Splits, str]:
        """The declarative temporal windows on ``df`` and their generated comment."""
        windows = self.temporal.splits if self.temporal is not None else None
        if windows is None:
            msg = f"{type(self).__name__}: a temporal task needs `Temporal(splits=...)` or `_make_splits`."
            raise DatasetDefinitionError(msg)
        time_on = self.task_metadata.time_on
        splits = windows.splits(df, time_on)
        derived = None
        if windows.window is None and windows.cutoffs is None:
            first_test = splits[0][0][1]
            derived = len(first_test) if windows.unit == "rows" else df[time_on].iloc[first_test].nunique()
        return splits, windows.describe(len(splits), derived_window=derived)

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
        """Run :meth:`_make_splits` on ``df`` (default: :attr:`df`) and normalise it to a SplitPlan.

        Every split side comes in row order: a side is a set of rows, and the container's row table stores it so.
        """
        df = self.df if df is None else df
        if self.temporal is not None:
            self._check_time_unit(df[self.temporal.on])
        plan = self._make_splits(df)
        if not isinstance(plan, SplitPlan):
            plan = SplitPlan(splits=plan)
        plan.splits = _in_row_order(plan.splits)
        if plan.df is None:
            plan.df = df
        elif plan.df is not df and self._make_splits is not AbstractCuratedDataset._make_splits:
            plan.df = _drop_unused_categories(plan.df)  # a custom split step that drops rows keeps old levels
            self._time_changed_in_split = _time_values_changed(df, plan.df, self.task_metadata.time_on)
        if self.splits_comment is not None:
            plan.comment = clean_text(self.splits_comment)
        if not plan.comment:
            msg = f"{type(self).__name__}: custom splits need a `splits_comment` (or `SplitPlan(comment=...)`)."
            raise DatasetDefinitionError(msg)
        return plan

    def _check_time_unit(self, times: pd.Series) -> None:
        """Check the time column's calendar against ``Temporal(time_unit=...)``.

        A date has its own calendar; a numeric time column says what a step counts when the train sampler needs it.
        """
        unit, name = self.temporal.time_unit, type(self).__name__
        dated = pd.api.types.is_datetime64_any_dtype(times)
        if unit is not None and dated:
            msg = f"{name}: `{times.name}` is a date, whose calendar is its own: drop `Temporal(time_unit=...)`."
            raise DatasetDefinitionError(msg)
        if unit is not None and not pd.api.types.is_numeric_dtype(times):
            msg = f"{name}: `time_unit` counts steps of a numeric time column; `{times.name}` is {times.dtype}."
            raise DatasetDefinitionError(msg)
        if unit is None and not dated and self.row_budget is not None:
            msg = (
                f"{name}: a benchmark samples the train sides of a version with a `row_budget` from their newest year, "
                f"and `{times.name}` is no date: declare what one step of it counts, `Temporal(..., time_unit=...)` "
                "(numerai's weekly eras: `time_unit='weeks'`)."
            )
            raise DatasetDefinitionError(msg)

    def window_stats(
        self,
        *,
        window: int | None = None,
        unit: str | None = None,
        gap: int | None = None,
        gap_unit: str | None = None,
        step: int | None = None,
        min_train_fraction: float = 0.3,
        n_rows: int = 100_000,
    ) -> pd.DataFrame:
        """The candidate test windows of this temporal task and their statistics, for choosing its windows (SPLIT-15).

        The candidates have the length, gap and step of the declared windows (``temporal.splits``) unless given here,
        walking back from the newest data while every train side keeps ``min_train_fraction`` of the rows. The
        definition's own windows are marked ``chosen``; one that no candidate matches (a cutoff on another date) is
        listed as a row of its own. Statistics of the data only, never of a model
        (:func:`~data_foundry.v2.windows.window_stats`): the dates and months, the sizes and train share, the target,
        and the drift of the features from the train side. ``dataset windows <name>`` prints the table.
        """
        if self.temporal is None:
            msg = f"{type(self).__name__}: window statistics are for a temporal task (`temporal = Temporal(...)`)."
            raise DatasetDefinitionError(msg)
        declared, on = self.temporal.splits, self.temporal.on
        if declared is None and (window is None or unit is None):
            msg = (
                f"{type(self).__name__}: the splits are custom (`_make_splits`); give the candidates' window and unit."
            )
            raise DatasetDefinitionError(msg)
        candidates = TemporalSplits(
            window=window if window is not None else declared.window,
            unit=unit if unit is not None else declared.unit,
            gap=gap if gap is not None else (declared.gap if declared is not None else 0),
            gap_unit=gap_unit if gap_unit is not None else (declared.gap_unit if declared is not None else None),
            step=step if step is not None else (declared.step if declared is not None else None),
            min_train_fraction=min_train_fraction,
        )
        df = self.df
        task = self.task_metadata
        # The features a model reads (as `feature_columns` of a container): no target, group, scoring column, training
        # weight or unit of a unit weight (noaa_storm_events_damage's `cell` would read as all-new categories).
        drop = {task.target_column_name, on, *as_column_list(task.group_on), *(c.column for c in task.scoring_columns)}
        drop.update(as_column_list(task.sample_weight))
        if task.unit_weight is not None:
            drop.add(task.unit_weight.unit)
        stats = functools.partial(
            window_stats,
            time_on=on,
            target=task.target_column_name,
            problem_type=task.problem_type,
            features=[c for c in df.columns if c not in drop],
            time_unit=self.temporal.time_unit,
            n_rows=n_rows,
            random_state=self.SPLIT_RANDOM_STATE,
        )
        if declared is None:  # custom splits: their own positions, on the frame they return
            plan = self.make_splits(df)
            own = [(train, test) for folds in plan.splits.values() for train, test in folds.values()]
        else:  # the declared windows as position ranges: no index lists, however long the history
            plan = SplitPlan(splits={}, df=df)
            own = [
                (range(b.train_stop), range(b.test_start, b.test_stop))
                for b in protocol.window_bounds(
                    df,
                    time_on=on,
                    window=declared.window,
                    unit=declared.unit,
                    n_windows=declared.n_windows,
                    step=declared.step,
                    gap=declared.gap,
                    gap_unit=declared.gap_unit,
                    cutoffs=list(declared.cutoffs) if declared.cutoffs is not None else None,
                    min_train_fraction=declared.min_train_fraction,
                )
            ]
        own_tests = {(test[0], test[-1]) for _train, test in own}
        windows = [
            dataclasses.replace(w, chosen=(w.test[0], w.test[-1]) in own_tests)
            for w in candidate_windows(df, on, candidates, min_train_fraction=min_train_fraction)
        ]
        matched = {(w.test[0], w.test[-1]) for w in windows if w.chosen}
        extra = [
            Window(train=train, test=test, chosen=True) for train, test in own if (test[0], test[-1]) not in matched
        ]
        table = stats(df, windows)
        if extra:  # a custom split's frame may leave out columns (hotel_booking_demand drops the outcome columns)
            features = [c for c in df.columns if c not in drop and c in plan.df.columns]
            table = pd.concat([table, stats(plan.df, extra, features=features)], ignore_index=True)
        table = table.sort_values("test_start", ascending=False, kind="stable").reset_index(drop=True)
        table["window"] = range(len(table))
        return table

    def preview_splits(self, df: pd.DataFrame | None = None) -> pd.DataFrame:
        """One row per outer split with its train/test sizes, and time ranges for a temporal task."""
        plan = self.make_splits(df)
        return split_summary(plan.df, plan.splits, time_on=self.task_metadata.time_on)

    # --- pipeline -----------------------------------------------------------------------------------
    def to_container(self) -> CuratedContainer:
        """Rebuild the frame from the raw data, split it and attach the metadata. Nothing is saved."""
        df, test = self.process()
        plan = self.make_splits(df)
        horizon, unit = _horizon(type(self))
        gap, gap_unit = _gap(type(self))
        splits_metadata = PredictiveMLSplitsMetadata(
            splits_comment=plan.comment,
            splits=plan.splits,
            split_random_state=self.SPLIT_RANDOM_STATE,
            time_horizon=horizon,
            time_horizon_unit=unit,
            time_gap=gap,
            time_gap_unit=gap_unit,
            row_budget=self.row_budget,
            train_sampling=self.train_sampling(plan.df),
        )
        manifest = self.raw_manifest(getattr(self, "_rows_per_file", None))
        metadata = dataclasses.replace(self.dataset_metadata, raw_files=manifest) if manifest else self.dataset_metadata
        with _quiet():
            return CuratedContainer(
                dataset=plan.df,
                dataset_metadata=metadata,
                task_metadata=self.task_metadata_for(plan.df),
                experiment_metadata=splits_metadata,
                test_dataset=test,
            )

    def check(self, *, write_report: bool = True, verbose: bool = True) -> CurationResult | ParentCheckResult:
        """Run the full pipeline and the bundle checks without saving (no UUID is kept).

        Writes ``README.md`` unless ``write_report`` is False (or the class is defined in a notebook). The build record
        of an earlier :meth:`build` in the report is kept, and marked stale when the checksum no longer matches. A
        parent (no ``target``) is checked as data only: :meth:`check_parent`.
        """
        self._refresh()
        if not self.is_task:
            return self.check_parent(write_report=write_report, verbose=verbose)
        with _copy_on_write():  # a hook that writes in place must not reach the cached raw data
            container = self.to_container()
            stats = group_checks.group_stats(container)
            result = CurationResult(
                dataset=self,
                container=container,
                bundle_report=self._run_bundle_checks(container, verbose=verbose, group_stats=stats),
                data_checks=self.run_all_checks(container.dataset),
                decisions=list(self._decisions(self.raw, container.dataset)),
                group_stats=stats,
            )
        if write_report and self.report_path is not None:
            self._write_report(result)
        return result

    def check_parent(self, *, write_report: bool = True, verbose: bool = True) -> ParentCheckResult:
        """Check a parent (a definition without a ``target``) as data: its frame, its checksum and its definition.

        A parent is never built. Its ``README.md`` describes the data its children start from: the data summary, the
        sources, the columns, a checksum of the frame (in content order) and the children found next to it.

        Raises:
            DatasetDefinitionError: The parent is partial (no ``_load_raw`` or a missing declaration), or a task.
        """
        name = type(self).__name__
        if self.is_task:
            raise DatasetDefinitionError(f"{name} declares a `target`: a task, checked with `check()`.")
        missing = [a for a in _REQUIRED_DATA if not hasattr(self, a)]
        if inspect.isabstract(type(self)):
            missing.append("_load_raw")
        if missing:
            msg = (
                f"{name} is a partial parent, which shares code only; its data cannot be checked without "
                f"{', '.join(missing)}."
            )
            raise DatasetDefinitionError(msg)
        with _copy_on_write():
            frame, _ = self.process()
        children = family_children(type(self))
        manifest = self.raw_manifest(getattr(self, "_rows_per_file", None))
        findings = self._definition_checks() + self._raw_file_findings(manifest)
        if not children:
            findings.append(
                CheckResult(
                    "parent_without_children",
                    "warning",
                    f"`{self.unique_name}` declares no `target`, so it is a parent, but no definition derives from it.",
                    hint="Declare the task (`target`, `problem_type`, `metric`), or add a child: `class "
                    f'X(import_definition("{self.unique_name}"))` in `{self.unique_name}_<variant>/dataset.py`.',
                ),
            )
        result = ParentCheckResult(
            dataset=self,
            frame=frame,
            data_checksum=data_checksum(frame),
            findings=sorted(findings, key=lambda r: SEVERITY_ORDER[r.severity]),
            children=children,
            raw_files=manifest,
        )
        if verbose:
            print(
                f"{self.unique_name}: a parent of {len(children)} definition(s); data checksum {result.data_checksum}"
            )
            for finding in result.findings:
                print(f"  {finding.severity}: {finding.slug}: {finding.message}")
        if write_report and self.report_path is not None:
            from data_foundry.v2.report import write_parent_report  # noqa: PLC0415 - report imports this module

            write_parent_report(result, self.report_path)
        return result

    def build(self, *, verbose: bool = True, allow_local_metric: bool = False) -> CurationResult:
        """Run :meth:`check`, fail on bundle-check errors, save the container and verify the export.

        This is the only step that mints a UUID. The report records the UUID, checksum and provenance. A local
        metric (``Metric.local``: code only this definition holds) is refused unless ``allow_local_metric`` is True,
        which only a user's own, never shipped, dataset should pass: a reader of the container could not compute it.
        """
        from data_foundry.v2.report import read_report  # noqa: PLC0415 - report imports this module

        name = type(self).__name__
        if not self.is_task:
            msg = f"{name} is a parent (no `target`): it is never built; build its children (`dataset list`)."
            raise DatasetDefinitionError(msg)
        if self.folder is None:
            msg = f"{name} is defined outside a `{DEFINITION_FILENAME}`: write it into one to build it."
            raise DatasetDefinitionError(msg)
        if _declared_metric(type(self)).is_local and not allow_local_metric:
            msg = (
                f"{type(self).__name__}: the metric is local (`Metric.local`), so a reader of the container cannot "
                "compute it. A shipped dataset adds its metric to data_foundry.v2.metrics under a general name; for "
                "your own unshipped dataset, pass `build(allow_local_metric=True)`."
            )
            raise DatasetDefinitionError(msg)
        result = self.check(write_report=False, verbose=verbose)
        result.bundle_report.raise_if_errors()
        reviewed = read_report(self.report_path).get("checksum")
        if reviewed and reviewed != result.container.checksum:
            print(
                f"Note: {self.unique_name} builds checksum {result.container.checksum}, not the {reviewed} of its "
                f"{REPORT_FILENAME}: the definition, the raw files or the library changed since the last check.",
            )
        with _quiet():
            save_path = result.container.save(resolve_warehouse_dir())
        try:
            verify_saved_container(save_path, container=result.container, verbose=verbose).raise_if_errors()
        except Exception:
            shutil.rmtree(save_path, ignore_errors=True)  # no container in the warehouse without its record
            raise
        if verbose:
            print(f"Saved {self.unique_name} as {result.container.uuid} to {save_path}")
        result.saved_path = save_path
        self._write_report(result)
        return result

    def _run_bundle_checks(
        self,
        container: CuratedContainer,
        *,
        verbose: bool,
        group_stats: group_checks.GroupStats | None = None,
    ) -> BundleCheckReport:
        accepted = tuple(self.accepted_check_warnings)
        report = run_bundle_checks(container, verbose=False)  # a format-2 container: the v2 protocol checks included
        shared = report.results
        own: list[CheckResult] = []
        metric = _declared_metric(type(self))
        for name, run in (
            ("definition", self._definition_checks),
            ("metric", lambda: metric_computes_findings(container, metric) if metric.is_local else []),
            ("group", lambda: group_checks.group_findings(container, group_stats)),
            ("task", lambda: task_checks.task_findings(container)),
            ("extra", lambda: self._extra_checks(container)),
            ("raw files", lambda: self._raw_file_findings(container.dataset_metadata.raw_files)),
        ):
            try:
                own += run()
            except Exception as error:  # noqa: BLE001 - a broken check is a finding, not a crash
                own.append(
                    CheckResult("check_crashed", "error", f"the {name} checks crashed: {type(error).__name__}: {error}")
                )
        found = [*shared, *own]
        unused = [slug for slug in accepted if slug not in {r.slug for r in found}]
        if unused:
            found.append(
                CheckResult(
                    "accepted_check_warnings_unused",
                    "info",
                    f"Accepted on purpose but not found: {unused}.",
                    hint="Remove the entries that no longer apply, or fix a misspelled slug.",
                ),
            )
        report.results = sorted([r for r in found if r.slug not in accepted], key=lambda r: SEVERITY_ORDER[r.severity])
        report.ignored = accepted
        if verbose:
            print("\n".join(["Metric:", *container.task_metadata.objective_metric.describe_lines()]))
            print(report.summary())
        return report

    def _summary_checks(self) -> list[CheckResult]:
        """Findings about :attr:`task_summary`: missing, no use case, or too long to read at a glance."""
        summary = self.task_summary
        if summary is None:
            return [
                CheckResult(
                    "definition_summary_missing",
                    "error",
                    "`task_summary` is not set: the README has no plain-language summary of the task.",
                    hint="Add `task_summary = TaskSummary(...)` at the top of the class (knowledge-data-foundry "
                    'definitions.md, "In brief").',
                ),
            ]
        findings = []
        if summary.fit == "none":
            findings.append(
                CheckResult(
                    "definition_no_use_case",
                    "error",
                    f"`TaskSummary(fit='none')`: {clean_text(summary.fit_reason)}",
                    hint="A dataset that simulates no decision is retired (`No Good Target / Scientific Discovery`), "
                    "not shipped.",
                ),
            )
        long = {
            name: len(text.split()) for name, text in summary.fields().items() if len(text.split()) > SUMMARY_MAX_WORDS
        }
        if long:
            findings.append(
                CheckResult(
                    "definition_summary_long",
                    "warning",
                    f"`task_summary` field(s) over {SUMMARY_MAX_WORDS} words: {long}.",
                    hint="Keep each field to one or two plain sentences; the evidence belongs in `curation_comments`.",
                ),
            )
        return findings

    def _data_summary_checks(self) -> list[CheckResult]:
        """Findings about :attr:`data_summary`: a field too long to read at a glance."""
        if self.data_summary is None:
            return []
        long = {
            name: len(text.split())
            for name, text in self.data_summary.fields().items()
            if len(text.split()) > SUMMARY_MAX_WORDS
        }
        if not long:
            return []
        return [
            CheckResult(
                "definition_summary_long",
                "warning",
                f"`data_summary` field(s) over {SUMMARY_MAX_WORDS} words: {long}.",
                hint="Keep each field to one or two plain sentences; the evidence belongs in `curation_comments`.",
            ),
        ]

    def _definition_checks(self) -> list[CheckResult]:
        """Findings about the definition files (this class's and its parents'): scaffold markers, a placeholder
        license, nondeterministic code, and the summaries.
        """
        findings = []
        for file in definition_files(type(self)):
            label = _file_label(file, definition_file(type(self)))
            text = file.read_text()
            todo = [i for i, line in enumerate(text.splitlines(), start=1) if "TODO(verify)" in line]
            if todo:
                findings.append(
                    CheckResult(
                        "definition_todo_left",
                        "error",
                        f"{label} still has {len(todo)} `TODO(verify)` marker(s), on line(s) {todo[:20]}.",
                        hint="Resolve each marker (check the data, then write the step or delete the stub).",
                    ),
                )
            unstable = nondeterministic_calls(ast.parse(text))
            if unstable:
                listed = "; ".join(f"line {line}: {why}" for line, why in unstable[:10])
                findings.append(
                    CheckResult(
                        "definition_nondeterministic",
                        "error",
                        f"{label} has {len(unstable)} call(s) whose result can change between runs or machines: "
                        f"{listed}.",
                        hint="Seed every random step (`random_state=`, a seeded `default_rng`, `anonymize_ids` for "
                        'ids), sort with `kind="stable"`, wrap file listings in `sorted(...)`, and use '
                        "`maintain_order=True` in a polars `group_by`.",
                    ),
                )
        findings += self._summary_checks() if self.is_task else self._data_summary_checks()
        changed = getattr(self, "_time_changed_in_split", 0)
        if changed:
            time_on = self.task_metadata.time_on
            findings.append(
                CheckResult(
                    "definition_time_changed_in_split",
                    "warning",
                    f"`_make_splits` changes the time column `{time_on}` on {changed:,} rows. The rows were ordered "
                    "by its values before that step, so within a coarsened period they keep the order of the finer "
                    "time (the minute of chicago_traffic_crashes, 2026-11-04).",
                    hint=f"Coarsen `{time_on}` in `_clean`; within a period the rows then follow the content order.",
                ),
            )
        placeholders = [s.license for s in getattr(self, "sources", ()) if re.search(r"\bTODO\b", str(s.license))]
        if placeholders:
            findings.append(
                CheckResult(
                    "definition_license_placeholder",
                    "error",
                    f"`Source(license={placeholders[0]!r})` is a placeholder.",
                    hint="Write the license the source states, or None when it states none.",
                ),
            )
        return findings

    def raw_manifest(self, rows_per_file: dict[str, int] | None = None) -> list[RawFile]:
        """The raw files the sources name (``Source(files=...)``, globs under :attr:`raw_dir`), with their hashes.

        Hashes are cached in :data:`RAW_MANIFEST_CACHE` in the raw folder, by size and modification time, so a large
        file is read once. ``rows_per_file`` gives each file's rows (from the ``source_file`` column). A pattern that
        matches no file is reported by the checks (``raw_files_missing``).
        """
        raw_dir = self.raw_dir
        cache_path = raw_dir / RAW_MANIFEST_CACHE
        try:
            cache = json.loads(cache_path.read_text()) if cache_path.is_file() else {}
        except (OSError, ValueError):
            cache = {}
        manifest: dict[str, RawFile] = {}
        unmatched = []
        for source in getattr(self, "sources", ()):
            for pattern in source.files:
                paths = sorted(p for p in raw_dir.glob(pattern) if p.is_file() and not p.name.startswith("."))
                if not paths:
                    unmatched.append(pattern)
                for path in paths:
                    rel = path.relative_to(raw_dir).as_posix()
                    if rel in manifest:
                        continue
                    stat = path.stat()
                    entry = cache.get(rel, {})
                    if entry.get("size") != stat.st_size or entry.get("mtime_ns") != stat.st_mtime_ns:
                        entry = {"size": stat.st_size, "mtime_ns": stat.st_mtime_ns, "sha256": _sha256(path)}
                        cache[rel] = entry
                    rows = (rows_per_file or {}).get(rel)
                    manifest[rel] = RawFile(
                        path=rel, sha256=entry["sha256"], size=stat.st_size, source=source.label(), rows=rows
                    )
        self._unmatched_raw_files = unmatched
        if manifest:
            with contextlib.suppress(OSError):  # a read-only warehouse hashes again next time
                cache_path.write_text(json.dumps(cache, indent=1, sort_keys=True))
        return list(manifest.values())

    def _raw_file_findings(self, manifest: list[RawFile]) -> list[CheckResult]:
        """A source's file pattern that matches nothing, and raw files changed since the README was written."""
        from data_foundry.v2.report import read_report  # noqa: PLC0415 - report imports this module

        findings = []
        unmatched = getattr(self, "_unmatched_raw_files", [])
        if unmatched:
            findings.append(
                CheckResult(
                    "raw_files_missing",
                    "error",
                    f"`Source(files=...)` names {unmatched}, which match no file under {self.raw_dir}.",
                    hint="Download the files (`download_description`), or fix the pattern.",
                ),
            )
        before = read_report(self.report_path).get("raw_files") if self.report_path is not None else None
        if before:
            now = {f.path: f.sha256 for f in manifest}
            changed = sorted(p for p in now if p in before and before[p] != now[p])
            added, removed = sorted(set(now) - set(before)), sorted(set(before) - set(now))
            if changed or added or removed:
                parts = [
                    f"{label}: {paths[:10]}"
                    for label, paths in (("changed", changed), ("new", added), ("gone", removed))
                    if paths
                ]
                findings.append(
                    CheckResult(
                        "raw_files_changed",
                        "warning",
                        f"The raw files differ from those {REPORT_FILENAME} was written from; {'; '.join(parts)}.",
                        hint="A source may have published a new version: check what changed before writing the "
                        "README again.",
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
    use ``df.loc[mask, "a"] = x``.) pandas 3 always copies on write and deprecates the option.
    """
    if PANDAS_3:
        yield
        return
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


_SORTS = ("sort_values", "sort_index", "argsort")
_LISTINGS = ("glob", "rglob", "iterdir", "listdir", "scandir")
_STDLIB_RANDOM = ("random", "choice", "choices", "shuffle", "sample", "randint", "uniform", "gauss")


def nondeterministic_calls(tree: ast.AST) -> list[tuple[int, str]]:  # noqa: C901 - a flat list of rules
    """Calls in a definition whose result can change between runs or machines, as ``(line, reason)``.

    Unseeded randomness (``sample`` or ``train_test_split`` without ``random_state``, ``np.random.*``, an unseeded
    generator, the ``random`` module, ``uuid1`` / ``uuid4``); a pandas or numpy sort without ``kind="stable"`` (the
    default quicksort breaks ties differently with and without AVX512); a polars ``group_by`` without
    ``maintain_order=True`` (its row order changes between runs); and a file listing not wrapped in ``sorted``.
    """
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}

    def wrapped_in_sorted(node: ast.AST) -> bool:
        for _ in range(3):  # sorted(x.glob()), sorted(list(x.glob())), sorted(map(str, x.glob()))
            node = parents.get(node)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "sorted":
                return True
        return False

    def constant(value: ast.AST | None) -> object:
        return value.value if isinstance(value, ast.Constant) else None

    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else (func.id if isinstance(func, ast.Name) else "")
        owner = ast.unparse(func.value) if isinstance(func, ast.Attribute) else ""
        keywords = {k.arg: k.value for k in node.keywords if k.arg}
        if name in _SORTS and constant(keywords.get("kind")) not in ("stable", "mergesort"):
            found.append((node.lineno, f'`{name}` without kind="stable"'))
        elif name == "group_by" and constant(keywords.get("maintain_order")) is not True:
            found.append((node.lineno, "`group_by` without maintain_order=True"))
        elif name in _LISTINGS and not wrapped_in_sorted(node):
            found.append((node.lineno, f"`{name}` not wrapped in sorted()"))
        elif name in ("sample", "train_test_split") and owner != "random" and "random_state" not in keywords:
            found.append((node.lineno, f"`{name}` without random_state"))
        elif owner in ("np.random", "numpy.random") and name not in ("default_rng", "RandomState"):
            found.append((node.lineno, f"unseeded `{owner}.{name}`"))
        elif name in ("default_rng", "RandomState") and not node.args and "seed" not in keywords:
            found.append((node.lineno, f"`{name}()` without a seed"))
        elif (owner == "random" and name in _STDLIB_RANDOM) or (owner == "uuid" and name in ("uuid1", "uuid4")):
            found.append((node.lineno, f"unseeded `{owner}.{name}`"))
    return sorted(found)


RAW_MANIFEST_CACHE = ".raw_manifest.json"
"""The file in a raw folder that caches the hashes of its raw files, by size and modification time."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


PREPARED_MARKER = ".prepared_raw_files.json"
"""The file next to the prepared raw files that records the hash of the code that wrote them."""


def _prepare_code_hash(cls: type) -> str:
    """A hash of ``_prepare_raw_files`` and of the functions, classes and methods of its module it calls, directly
    or through each other, and of the module-level assignments they read (an edit of a helper or of a constant such
    as a list of files makes the prepared files stale too). Constants are hashed as written, not by their value, so
    module state that changes at run time does not count.
    """
    owner = next((k for k in cls.__mro__ if "_prepare_raw_files" in vars(k)), cls)  # the family root, if inherited
    cls = owner
    module = inspect.getmodule(cls)
    assignments = _module_assignments(module)
    sources: dict[str, str] = {}
    constants: dict[str, str] = {}
    pending = [("_prepare_raw_files", cls._prepare_raw_files)]
    while pending:
        name, obj = pending.pop()
        if name in sources:
            continue
        try:
            sources[name] = inspect.getsource(obj)
        except (OSError, TypeError):
            continue
        code = getattr(obj, "__code__", None)
        for used in _names_used(code) if code is not None else ():
            target = getattr(module, used, None) or getattr(cls, used, None)
            if callable(target) and inspect.getmodule(target) is module and used not in sources:
                pending.append((used, target))
            elif used in assignments:
                _add_constant(used, assignments, constants)
    text = "\n".join(f"{name}\n{source}" for name, source in sorted(sources.items()))
    if constants:  # appended only when there are any, so the hash of code without constants does not change
        text += "\n" + "\n".join(source for _, source in sorted(constants.items()))
    return hashlib.sha256(text.encode()).hexdigest()


def _module_assignments(module: Any) -> dict[str, tuple[str, set[str]]]:
    """The module-level assignments of ``module``: name -> (the statement as written, the names its value reads)."""
    try:
        source = inspect.getsource(module)
    except (OSError, TypeError):
        return {}
    out: dict[str, tuple[str, set[str]]] = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        else:
            continue
        reads = {n.id for n in ast.walk(value) if isinstance(n, ast.Name)}
        for target in targets:
            if isinstance(target, ast.Name):
                out[target.id] = (ast.get_source_segment(source, node) or "", reads)
    return out


def _add_constant(name: str, assignments: dict[str, tuple[str, set[str]]], constants: dict[str, str]) -> None:
    """Add the assignment of ``name`` and of the module-level names its value reads (a constant built from others)."""
    if name in constants or name not in assignments:
        return
    statement, reads = assignments[name]
    constants[name] = statement
    for read in reads:
        _add_constant(read, assignments, constants)


def _names_used(code: Any) -> set[str]:
    """The global and attribute names a code object (and the code nested in it) refers to."""
    names = set(code.co_names)
    for const in code.co_consts:
        if inspect.iscode(const):
            names |= _names_used(const)
    return names


def _categories_like(test: pd.DataFrame, train: pd.DataFrame) -> pd.DataFrame:
    """Give the test set's categorical columns the training frame's categories first, in their order, and the
    values only the test set has after them, so a value has the same code in both frames.
    """
    for col in test.columns:
        if col in train.columns and isinstance(train[col].dtype, pd.CategoricalDtype):
            if not isinstance(test[col].dtype, pd.CategoricalDtype):
                continue
            known = list(train[col].cat.categories)
            new = [c for c in test[col].cat.categories if c not in set(known)]
            test[col] = test[col].cat.set_categories(known + new)
    return test


def _source(cls: type, name: str) -> str | None:
    try:
        return inspect.getsource(getattr(cls, name))
    except (OSError, TypeError):
        return None


def _time_values_changed(before: pd.DataFrame, after: pd.DataFrame, time_on: str | None) -> int:
    """How many rows a custom split step changed the time column on (0 when it kept it, or has no such column).

    The rows are ordered by the time column before ``_make_splits`` runs (:func:`order_rows`), so a split step that
    floors the time leaves each period in the order of the finer values it meant to hide.
    """
    if time_on is None or time_on not in before.columns or time_on not in after.columns or len(before) != len(after):
        return 0
    old, new = before[time_on].reset_index(drop=True), after[time_on].reset_index(drop=True)
    return int((old.ne(new) & old.notna()).sum())


def _in_row_order(splits: Splits) -> Splits:
    """``splits`` with every side in row order; a side already in order is kept as it is."""

    def ordered(side: list[int]) -> list[int]:
        positions = np.asarray(side)
        return side if bool(np.all(positions[1:] >= positions[:-1])) else np.sort(positions).tolist()

    return {
        r: {f: (ordered(train), ordered(test)) for f, (train, test) in folds.items()} for r, folds in splits.items()
    }


def _drop_unused_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Drop category levels that no longer occur once a frame is sub-sampled (dtypes are set on the full data)."""
    df = df.copy(deep=False)  # only the categorical columns are replaced, not written into
    for col in df.columns:
        if isinstance(df[col].dtype, pd.CategoricalDtype):
            df[col] = df[col].cat.remove_unused_categories()
    return df


def _horizon(cls: type[AbstractCuratedDataset]) -> tuple[int | None, str | None]:
    return cls.temporal.resolved_horizon if cls.temporal is not None else (None, None)


def _gap(cls: type[AbstractCuratedDataset]) -> tuple[int | None, str | None]:
    return cls.temporal.resolved_gap if cls.temporal is not None else (None, None)


def _regime_tags(cls: type[AbstractCuratedDataset]) -> list[str]:
    tags = list(dict.fromkeys(cls.data_tags))
    if not is_task(cls) or any(tag in REGIME_TAGS for tag in tags):  # a parent has no split, so no regime
        return tags
    if cls.temporal is not None:
        regime = ["Non-IID", "Temporal"]
    elif cls.grouping is not None:
        regime = ["Non-IID", "GroupedTemporal" if cls.grouping.time_on is not None else "Grouped"]
    else:
        regime = ["IID"]
    return regime + tags


def is_task(cls: type) -> bool:
    """Whether a definition class is a task (it declares a ``target``, itself or through a parent), not a parent."""
    return hasattr(cls, "target")


def lineage(cls: type) -> list[type[AbstractCuratedDataset]]:
    """``cls`` and the definitions it derives from, nearest first: the classes of its MRO that declare their own
    ``unique_name`` (a helper base class without one is no definition).
    """
    return [
        k
        for k in cls.__mro__
        if k is not AbstractCuratedDataset and issubclass(k, AbstractCuratedDataset) and "unique_name" in vars(k)
    ]


def parent_definition(cls: type) -> type[AbstractCuratedDataset] | None:
    """The definition ``cls`` derives from directly (its parent in a family), or None."""
    return next((k for k in lineage(cls) if k is not cls), None)


def definition_file(cls: type) -> Path | None:
    """The ``dataset.py`` that defines ``cls``, or None for a class defined elsewhere (a notebook, a script, a test).

    Such a class has no folder of its own: it writes no ``README.md`` and cannot be built.
    """
    try:
        file = Path(inspect.getfile(cls)).resolve()
    except (TypeError, OSError):
        return None
    return file if file.name == DEFINITION_FILENAME else None


def definition_files(cls: type) -> list[Path]:
    """The files of ``cls`` and of the definitions it derives from, nearest first (each once)."""
    files = (definition_file(k) for k in [cls, *lineage(cls)])
    return list(dict.fromkeys(f for f in files if f is not None))


def _file_label(file: Path, own: Path | None) -> str:
    """How a finding names a definition file: ``dataset.py`` for the class's own, ``../<parent>/dataset.py`` else."""
    return DEFINITION_FILENAME if file == own else f"../{file.parent.name}/{file.name}"


def family_children(cls: type[AbstractCuratedDataset]) -> list[str]:
    """The definitions next to ``cls`` that derive from it directly: ``<unique_name>_<variant>/dataset.py`` folders
    whose class's parent is ``cls`` (by name). Folders that do not import are skipped.
    """
    from data_foundry.v2.registry import load_definition  # noqa: PLC0415 - the registry imports this module

    file = definition_file(cls)
    if file is None:
        return []
    children = []
    for definition in sorted(file.parent.parent.glob(f"{cls.unique_name}_*/{DEFINITION_FILENAME}")):
        try:
            child = load_definition(definition)
        except Exception:  # noqa: BLE001, S112 - a broken sibling is reported by its own check
            continue
        parent = parent_definition(child)
        if parent is not None and parent.unique_name == cls.unique_name:
            children.append(child.unique_name)
    return children


def data_checksum(frame: pd.DataFrame) -> str:
    """A checksum of a frame alone (shape, columns, dtypes, categories, values), as the container checksum hashes it:
    the identity of a parent's data.
    """
    return "v2:" + hashlib.blake2b(encode_dataset_v2(frame), digest_size=32).hexdigest()


def raw_owner(cls: type[AbstractCuratedDataset]) -> type[AbstractCuratedDataset]:
    """The definition whose raw files ``cls`` reads: the topmost one in its family that says how to download them
    (``download_description``); the family root when it does, a child of a code-only parent when that child does.
    """
    chain = lineage(cls) or [cls]
    return next((k for k in reversed(chain) if "download_description" in vars(k)), chain[-1])


def raw_name(cls: type[AbstractCuratedDataset]) -> str:
    """The warehouse folder of a definition's raw files.

    The ``unique_name`` of its :func:`raw_owner` (the family root, or itself), without the suffix of that
    definition's :attr:`~AbstractCuratedDataset.row_budget` (``cooking_time_1m`` reads ``cooking_time``).
    """
    root = raw_owner(cls)
    budget = root.row_budget
    suffix = f"_{budget.suffix}" if budget is not None else ""
    if suffix and root.unique_name.endswith(suffix):
        return root.unique_name[: -len(suffix)]
    return root.unique_name


def _clean_source(source: Source) -> Source:
    """``source`` with its BibTeX dedented, ending in one newline (its citation key is read when it is built)."""
    return dataclasses.replace(source, bibtex=clean_text(source.bibtex) + "\n") if source.bibtex else source


def _build_dataset_metadata(cls: type[AbstractCuratedDataset]) -> DatasetMetadataV2:
    parent = parent_definition(cls)
    return DatasetMetadataV2(
        unique_name=cls.unique_name,
        domain=cls.domain,
        sources=[_clean_source(source) for source in cls.sources],
        download_description=clean_text(cls.download_description),
        data_tags=_regime_tags(cls),
        curation_comments=clean_text(cls.curation_comments),
        derived_from=None if parent is None else parent.unique_name,
        derivation=None if parent is None else clean_text(cls.derivation),
    )


def _build_metadata(cls: type[AbstractCuratedDataset]) -> tuple[DatasetMetadataV2, PredictiveMLTaskMetadataV2]:
    dataset = _build_dataset_metadata(cls)
    is_classification = cls.problem_type != "regression"
    stratify_on = (cls.target if is_classification else None) if cls.stratify_on is AUTO else cls.stratify_on
    grouping = None
    if cls.grouping is not None:
        grouping = dataclasses.replace(cls.grouping, definition=clean_text(cls.grouping.definition))
    task = PredictiveMLTaskMetadataV2(
        target_column_name=cls.target,
        problem_type=cls.problem_type,
        objective_metric=metric_spec(_declared_metric(cls), cls.problem_type),
        stratify_on=stratify_on,
        time_on=cls.temporal.on if cls.temporal is not None else None,
        time_unit=cls.temporal.time_unit if cls.temporal is not None else None,
        grouping=grouping,
        scoring_columns=[dataclasses.replace(c, description=clean_text(c.description)) for c in cls.scoring_columns],
        sample_weight=cls.sample_weight,
        unit_weight=cls.unit_weight,
    )
    return dataset, task


def metric_spec(metric: Metric, problem_type: str) -> MetricSpec:
    """The container's spec of ``metric`` for ``problem_type`` (a fallback resolved to roc_auc / log_loss / rmse)."""
    spec = metric.spec(problem_type)
    for key in ("original", "reference", "definition", "reason"):
        spec[key] = clean_text(spec[key]) if spec[key] else spec[key]
    return MetricSpec(**spec)


def _declared_metric(cls: type[AbstractCuratedDataset]) -> Metric:
    """The definition's ``metric`` (required; :func:`_validate_definition` checks it is a :class:`Metric`)."""
    return cls.metric


_FLAT_REGIME_ATTRIBUTES = (
    "time_on",
    "group_on",
    "group_labels",
    "group_time_on",
    "temporal_splits",
    "time_horizon",
    "time_horizon_unit",
)
"""The flat regime attributes of earlier v2 definitions, now declared as `grouping` / `temporal`."""

_REMOVED = {
    **dict.fromkeys(
        ("year", "source", "source_url", "license", "bibtex", "bibtex_key"),
        'declare the provenance as `sources = (Source(role="publication", platform=..., url=..., license=..., '
        "year=..., bibtex=...),)` (`from data_foundry.v2 import Source`)",
    ),
    "version_of": "a version sub-sampled to its `row_budget` is named `<name>_<suffix>` and reads the raw files of "
    "`<name>`; drop `version_of`",
    "version_comment": "say how a sub-sampled version differs in `curation_comments`",
    "raw_data_from": "a definition reads the raw files of its own name (without a row-budget suffix)",
}
"""Attributes of earlier v2 definitions, with what replaced them."""

_REQUIRED_DATA = ("unique_name", "domain", "sources", "download_description", "data_summary")
"""What a parent needs before its data can be checked (a partial parent may lack all but its name and summary)."""

_REQUIRED = (
    "unique_name",
    "domain",
    "sources",
    "download_description",
    "target",
    "problem_type",
    "metric",
)
"""The attributes a definition must declare."""


def _validate_definition(cls: type[AbstractCuratedDataset]) -> None:  # noqa: C901, PLR0912 - a flat list of rules
    """Build the metadata of a concrete dataset class and raise :class:`DatasetDefinitionError` on a problem."""
    name = cls.__name__

    def fail(problem: str) -> None:
        raise DatasetDefinitionError(f"{name}: {problem}")

    removed = [attr for attr in _REMOVED if hasattr(cls, attr)]
    if removed:
        fail("; ".join(f"`{attr}` is gone: {_REMOVED[attr]}" for attr in removed) + ".")
    parent = parent_definition(cls)
    if "unique_name" not in vars(cls) and parent is not None:
        fail(
            f"a child declares its own `unique_name` (`{parent.unique_name}_<variant>`); it inherits "
            f"`{parent.unique_name}`."
        )
    if "dataset_metadata" in vars(cls) or "task_metadata" in vars(cls):
        fail("declare the metadata as flat attributes (`unique_name = ...`, `target = ...`), not metadata objects.")
    task = is_task(cls)
    missing = [attr for attr in (_REQUIRED if task else ("unique_name", "data_summary")) if not hasattr(cls, attr)]
    if missing:
        what = "" if task else " (a parent: no `target`)"
        fail(f"missing required attribute(s){what}: {', '.join(missing)}.")
    for seed in ("SHUFFLE_RANDOM_STATE", "SPLIT_RANDOM_STATE"):
        if getattr(cls, seed) != getattr(AbstractCuratedDataset, seed):
            fail(f"`{seed}` is fixed for the whole benchmark; do not override it.")
    for attr in _TEXT_FIELDS:
        value = getattr(cls, attr, None)
        if value is not None and not isinstance(value, str):
            fail(f"`{attr}` must be a string.")
    sources = getattr(cls, "sources", ())
    if not isinstance(sources, tuple) or not all(isinstance(s, Source) for s in sources):
        fail("`sources` must be a tuple of `Source(...)`, the publication first.")
    if isinstance(cls.data_tags, str):
        fail("`data_tags` must be a tuple of tags, not one string.")
    retired = [tag for tag in cls.data_tags if tag in RETIRED_DATA_TAGS]
    if retired:
        fail(
            f"`data_tags` {retired}: retired, kept only so that old containers load. Write the dataset's doubts as a "
            "finding and its fit as `approximate` instead."
        )
    if not task and set(cls.data_tags) & {*REGIME_TAGS, "ForcedGroupedFromTemporal", "ForcedIIDFromTemporal"}:
        fail("a parent (no `target`) has no split, so no regime tag; its children get theirs from their task.")
    if task and "ForcedGroupedFromTemporal" in cls.data_tags and cls.grouping is None:
        fail("`ForcedGroupedFromTemporal` marks a grouped split; declare `grouping = Grouping(...)` or drop the tag.")
    if task and "ForcedIIDFromTemporal" in cls.data_tags and (cls.grouping is not None or cls.temporal is not None):
        fail("`ForcedIIDFromTemporal` marks an IID split; drop the tag or the `grouping`/`temporal` declaration.")
    moved = [
        a for a in ("drop_columns", "categorical_features", "string_features", "datetime_features") if a in vars(cls)
    ]
    if moved:
        fail(f"{', '.join(moved)}: drop columns in `_clean` and name dtypes in `_feature_types`.")
    flat = [a for a in _FLAT_REGIME_ATTRIBUTES if hasattr(cls, a)]
    if flat:
        fail(
            f"{', '.join(flat)}: declare the regime as one object, `grouping = Grouping(on=..., labels=..., "
            "definition=...)` or `temporal = Temporal(on=..., splits=TemporalSplits(...))`."
        )
    if cls.grouping is not None and not isinstance(cls.grouping, Grouping):
        fail("`grouping` must be a `Grouping(...)`.")
    metric = getattr(cls, "metric", None)
    if metric is not None and not isinstance(metric, Metric):
        fail("`metric` must be a `Metric` (`Metric.source(...)`, `Metric.stand_in(...)` or `Metric.fallback(...)`).")
    if isinstance(cls.scoring_columns, ScoringColumn) or not all(
        isinstance(c, ScoringColumn) for c in cls.scoring_columns
    ):
        fail("`scoring_columns` must be a tuple of `ScoringColumn(...)`.")
    if cls.sample_weight is not None and not isinstance(cls.sample_weight, str):
        fail("`sample_weight` names one scoring column (a string), or is None.")
    if cls.unit_weight is not None and not isinstance(cls.unit_weight, UnitWeight):
        fail("`unit_weight` is a `UnitWeight(column=..., unit=...)`, or None.")
    from data_foundry.v2.special import SpecialFeatureSpec  # noqa: PLC0415 - the kinds import this module

    moved = [a for a in ("smiles_columns", "spectra") if a in vars(cls)]
    if moved:
        fail(f"{', '.join(moved)}: declare it in `special_features` (`Smiles(column=...)`, `Spectrum(...)`).")
    specs = cls.special_features
    if not isinstance(specs, tuple) or not all(isinstance(s, SpecialFeatureSpec) for s in specs):
        fail("`special_features` must be a tuple of special features (`Smiles(column=...)`, `Spectrum(...)`).")
    if len({s.feature_name for s in specs}) != len(specs):
        fail("two `special_features` share a name.")
    if cls.temporal is not None and not isinstance(cls.temporal, Temporal):
        fail("`temporal` must be a `Temporal(...)`.")
    if cls.grouping is not None and cls.temporal is not None:
        fail(
            "a task is grouped or temporal, not both. For grouped data ordered in time, record the order as "
            "`Grouping(time_on=...)`; for a temporal split, the test rows are future rows whatever their group."
        )
    if isinstance(cls.stratify_on, (list, tuple)) and len(cls.stratify_on) > 1:
        fail("`stratify_on` takes one column: build a single stratification key in `_clean`.")
    if cls.grouping is not None and not clean_text(cls.grouping.definition or ""):
        fail(
            "`Grouping(definition=...)` is required: what one group is, why groups are held out, and the use case "
            "with its source."
        )
    _validate_summary(cls, fail)
    _validate_non_features(cls, fail)
    _validate_family(cls, parent, fail)
    file = definition_file(cls)
    if file is not None and file.name == DEFINITION_FILENAME and file.parent.name != cls.unique_name:
        fail(f"`unique_name={cls.unique_name!r}` must match its folder name {file.parent.name!r}.")
    for slug, reason in cls.accepted_check_warnings.items():
        if not str(reason).strip():
            fail(f"accepted check warning {slug!r} needs a reason.")

    if not task:
        _validate_parent(cls, fail)
        return
    try:
        cls.dataset_metadata, cls.task_metadata = _build_metadata(cls)
    except (ValueError, TypeError) as error:
        fail(f"invalid metadata: {error}")
    _validate_year(cls, fail)

    if cls.task_summary is not None:
        if not isinstance(cls.task_summary, TaskSummary):
            fail("`task_summary` must be a `TaskSummary(...)`.")
        if cls.task_summary.fit not in USE_CASE_FITS:
            fail(f"`TaskSummary(fit=...)` is one of {', '.join(USE_CASE_FITS)}, not {cls.task_summary.fit!r}.")
        empty = [
            name for name, text in cls.task_summary.fields().items() if name not in OPTIONAL_SUMMARY_FIELDS and not text
        ]
        if empty:
            fail(f"`TaskSummary` needs text in: {', '.join(empty)}.")

    custom_splits = cls._make_splits is not AbstractCuratedDataset._make_splits
    if cls.temporal is not None:
        if not custom_splits and cls.temporal.splits is None:
            fail("a temporal task needs `Temporal(splits=TemporalSplits(...))` or `_make_splits`.")
        if _horizon(cls) == (None, None):
            fail(
                "these windows do not fix the prediction horizon (unit='unique', window=None, or `_make_splits`): "
                "declare it as `Temporal(horizon=..., horizon_unit=...)`.",
            )
    if custom_splits and cls.temporal is not None and cls.temporal.splits is not None:
        fail("`Temporal(splits=...)` is ignored when the class implements `_make_splits`; declare one of them.")
    if "subsample_to_budget" in vars(cls):
        fail(
            "`subsample_to_budget` is replaced by the budget itself: `row_budget = RowBudget(train=1_000_000, "
            "test=500_000)` for a `_1m` version (`from data_foundry.v2 import RowBudget`)."
        )
    budget = cls.row_budget
    if budget is not None and not isinstance(budget, RowBudget):
        fail("`row_budget` must be a `RowBudget(train=..., test=...)`.")
    if (
        cls.temporal is not None
        and cls.temporal.splits is not None
        and cls.temporal.splits.sample_by != "rows"
        and budget is None
    ):
        fail("`TemporalSplits(sample_by=...)` sets how a version samples to its budget; it needs a `row_budget`.")
    if budget is not None:
        if custom_splits:
            fail("`row_budget` is ignored when the class implements `_make_splits`; sample there instead.")
        if not cls.unique_name.endswith(f"_{budget.suffix}"):
            fail(
                f"a version sub-sampled to `row_budget` is named `<name>_{budget.suffix}` and reads the raw files of "
                "`<name>`."
            )
    if cls.prepared_raw_files and cls._prepare_raw_files is AbstractCuratedDataset._prepare_raw_files:
        fail("`prepared_raw_files` is set but `_prepare_raw_files` is not implemented.")


def _validate_year(cls: type[AbstractCuratedDataset], fail: Any) -> None:
    year = cls.dataset_metadata.publication.year
    if not re.fullmatch(r"(19|20)\d{2}", str(year).strip()):
        fail(
            f"the publication's `year={year!r}` is not a year. Give the best guess of the first publication (PROV-9) "
            "and say in `curation_comments` that it is a guess, and why."
        )


def _validate_summary(cls: type[AbstractCuratedDataset], fail: Any) -> None:
    """A :class:`DataSummary` with text in its required fields, when one is declared."""
    summary = cls.data_summary
    if summary is None:
        return
    if not isinstance(summary, DataSummary):
        fail("`data_summary` must be a `DataSummary(data=..., row=..., goals=..., limits=...)`.")
    empty = [name for name, text in summary.fields().items() if name != "limits" and not text]
    if empty:
        fail(f"`DataSummary` needs text in: {', '.join(empty)}.")


def _validate_non_features(cls: type[AbstractCuratedDataset], fail: Any) -> None:
    """Valid :class:`NonFeature` declarations, each column once, and a child that keeps every inherited one."""
    declared = cls.non_features
    if not isinstance(declared, tuple) or not all(isinstance(nf, NonFeature) for nf in declared):
        fail("`non_features` must be a tuple of `NonFeature(column, reason, description)`.")
    other = [nf.column for nf in declared if nf.reason not in NON_FEATURE_REASONS]
    if other:
        fail(f"`NonFeature(reason=...)` is one of {', '.join(NON_FEATURE_REASONS)}; {other} have another.")
    columns = [nf.column for nf in declared]
    twice = sorted({c for c in columns if columns.count(c) > 1})
    if twice:
        fail(f"`non_features` declares {twice} twice.")
    undescribed = [nf.column for nf in declared if nf.reason == "other" and not nf.description.strip()]
    if undescribed:
        fail(f"a `NonFeature(reason='other')` says why in its `description`: {undescribed}.")
    if "non_features" in vars(cls):
        base = next((k for k in cls.__mro__[1:] if "non_features" in vars(k)), None)
        left_out = [nf.column for nf in getattr(base, "non_features", ()) if nf.column not in set(columns)]
        if left_out:
            fail(
                f"a child keeps every non-feature it inherits and may add more (`non_features = "
                f"(*{base.__name__}.non_features, NonFeature(...))`); it leaves out {left_out}."
            )


def _validate_family(cls: type[AbstractCuratedDataset], parent: type | None, fail: Any) -> None:  # noqa: C901
    """The rules of a child (a class derived from another definition), and no `derivation` without a parent."""
    if parent is None:
        if cls.derivation is not None:
            fail("`derivation` says how a definition differs from its parent; this one derives from no definition.")
        return
    if not cls.unique_name.startswith(f"{parent.unique_name}_"):
        fail(
            f"a child of `{parent.unique_name}` is named `{parent.unique_name}_<variant>` after what differs "
            f"(`_cop`, `_grouped`, `_clf`; a row budget's suffix last), not {cls.unique_name!r}."
        )
    if "derivation" not in vars(cls) or not clean_text(cls.derivation or ""):
        fail(f"a child declares `derivation`: how it differs from `{parent.unique_name}`, in a sentence or two.")
    ancestors = lineage(cls)[1:]
    owned = [
        a
        for a in ("download_description", "_prepare_raw_files", "prepared_raw_files")
        if a in vars(cls) and any(a in vars(k) for k in ancestors)
    ]
    if owned:
        root = raw_owner(parent).unique_name
        fail(
            f"{', '.join(f'`{a}`' for a in owned)}: the raw files belong to `{root}`, which says how to download "
            "them and whose files every member of the family reads; change them there."
        )
    if not is_task(cls):
        return
    for attr in ("task_summary", "splits_comment"):
        if attr in vars(cls):
            continue
        owner = next((k for k in cls.__mro__ if attr in vars(k)), AbstractCuratedDataset)
        if owner is AbstractCuratedDataset or getattr(owner, attr) is None:
            continue
        differs = [
            a
            for a in ("target", "problem_type", "grouping", "temporal")
            if _task_value(owner, a) != _task_value(cls, a)
        ]
        if differs:
            fail(
                f"`{attr}` is inherited from `{owner.unique_name}`, whose task differs ({', '.join(differs)}); declare "
                f"this task's own (`dataclasses.replace({owner.__name__}.{attr}, ...)` changes single fields)."
            )


def _task_value(cls: type, attr: str) -> Any:
    return getattr(cls, attr, None)


def _validate_parent(cls: type[AbstractCuratedDataset], fail: Any) -> None:
    """A parent declares no task of its own; when its data is described in full, its metadata is built."""
    declared = [a for a in ("row_budget", "task_summary", "splits_comment") if getattr(cls, a, None) is not None]
    if declared:
        fail(
            f"{', '.join(f'`{a}`' for a in declared)}: a parent (no `target`) has no task; declare them on its "
            "children."
        )
    if cls.data_summary is None:
        fail(
            "declares no `target`, so it is a parent of tasks, and a parent declares `data_summary = DataSummary(...)`"
            " (what the data is, independent of one task). For a task, declare `target`, `problem_type` and `metric`."
        )
    if all(hasattr(cls, a) for a in _REQUIRED_DATA):
        try:
            cls.dataset_metadata = _build_dataset_metadata(cls)
        except (ValueError, TypeError) as error:
            fail(f"invalid metadata: {error}")
        _validate_year(cls, fail)


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
    root = git("rev-parse", "--show-toplevel")
    package = Path(__file__).resolve().parents[1]  # src/data_foundry: the code that builds the container
    paths = ["."] + ([str(package)] if root and package.is_relative_to(Path(root).resolve()) else [])
    if sha is not None and git("status", "--porcelain", "--", *paths) not in (None, ""):
        sha += "-dirty"
    return {"data_foundry_version": package_version, "git_sha": sha, "libraries": _library_versions()}


def _library_versions() -> dict[str, str]:
    """The versions of the libraries the data, the splits and the checksum depend on."""
    import platform  # noqa: PLC0415

    out = {"python": platform.python_version()}
    for name in ("pandas", "numpy", "pyarrow", "scikit-learn", "polars"):
        try:
            out[name] = version(name)
        except PackageNotFoundError:
            continue
    return out
