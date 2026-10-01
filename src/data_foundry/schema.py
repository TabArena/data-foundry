from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Annotated, ClassVar, Literal

import pydantic

MultilineStr = Annotated[str, "multiline"]

SNAKE_CASE_PATTERN = re.compile(r"[a-z0-9]+(_[a-z0-9]+)*")
"""Naming convention for ``unique_name`` (curation guidelines: standardize to snake_case)."""


def as_column_list(value: str | list[str] | None) -> list[str]:
    """Normalize a metadata field that holds one column name, several, or none."""
    if value is None:
        return []
    return list(value) if isinstance(value, list) else [value]


DEFAULT_LOCAL_DATA_DIR = str(Path(__file__).parent.parent.parent / "local-data-warehouse")
"""Default local data warehouse directory (used when no env var override is set).

Resolves to ``<data-foundry-root>/local-data-warehouse`` for editable installs.
For pip installs you almost certainly want to override via the
:data:`DATA_FOUNDRY_WAREHOUSE_ENV` environment variable instead, since the
default would otherwise land inside ``site-packages``.
"""

DATA_FOUNDRY_WAREHOUSE_ENV = "DATA_FOUNDRY_WAREHOUSE"
"""Environment variable that overrides :data:`DEFAULT_LOCAL_DATA_DIR`.

Set this when your raw downloads + saved containers do not live next to the
data-foundry source tree (e.g. on a pip-installed deployment, or in a shared
team warehouse).
"""


def resolve_warehouse_dir() -> Path:
    """Resolve the local data warehouse root.

    Precedence: ``$DATA_FOUNDRY_WAREHOUSE`` > :data:`DEFAULT_LOCAL_DATA_DIR`.
    The path is **not** created — callers (curation notebooks, ``save``) are
    responsible for ensuring it exists when they need to write.
    """
    return Path(os.environ.get(DATA_FOUNDRY_WAREHOUSE_ENV) or DEFAULT_LOCAL_DATA_DIR).expanduser()


# TODO: converge on set of domains we want to check
Domain = Literal[
    "education",
    "environmental science & climate",
    "biology & life sciences",
    "handcrafted",
    "chemistry & material science",
    "industry & manufacturing",
    "physics & astronomy",
    "multimedia",
    "medical & healthcare",
    "technology & internet",
    "finance",
    "social science",
    "business & marketing",
    # Newer domain strings
    "insurance",
]
DatasetSource = Literal[
    "Kaggle",
    "Zindi",
    "OpenML",
    "GitHub",
    "UCI",
    "HuggingFace",
    "GOV Website",
    "Customer",
    "Other",
    "ASlib",
]
DataTags = Literal[
    # Important tags for the task, feel free to add more that seem reasonable!
    "IID",
    "Non-IID",
    # What kind of non-iid task (i.e., split) the data represents
    #   - Only set Grouped XOR Temporal. PredictiveMLTaskMetadata has more details on the difference for splits.
    "Temporal",  # Split on temporal information (e.g. timestamp) to predict on the future.
    "Grouped",  # Split on groups (e.g. customers) to predict on unseen groups.
    "GroupedTemporal",  # Data that is split using grouped and temporal information - unsure if this exists.
    # Other context tags (not statistical information!)
    "Spatial",  # data that contains spatial/geographical information
    "Anonymized",  # data that has no semantic meaning anymore on purpose
    # data that is IID by construction of the data.
    #   - e.g. temporal data that is missing the timestamp
    "ForcedIIDFromTemporal",
    "2ndTierData",  # Data that is not of the highest quality but still a reasonable task
    "WrongDomain",  # Task that was transformed to another domain (like audio) to tabular.
]
ProblemType = Literal["binary_classification", "multiclass_classification", "regression"]
ProblemTypeClassification = [
    "binary_classification",
    "multiclass_classification",
]
GroupLabelTypes = Literal["per_group", "per_sample"]
PredictionUnit = Literal["row", "group"]
GroupAggregation = Literal["mean", "any", "last", "select_min", "select_max"]
GroupContext = Literal["none", "all_rows", "past_rows"]


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class Grouping:
    """How a grouped task is used: what one group is, what one prediction is, and what a model may know.

    Stored as :attr:`PredictiveMLTaskMetadataV2.grouping` (container format 2), the only place such a container
    records its group fields; ``prediction_unit``, ``aggregation`` and ``context`` come from the use case of the data's
    source. The group column is metadata for splitting and scoring, never a model feature.

    How a benchmark is expected to score the fields (a recommendation; the harness decides):

    * ``prediction_unit="row"``: every row is one prediction and counts once.
    * ``prediction_unit="group"``: one prediction per group, and every group counts once. ``aggregation`` combines
      the row predictions of a group: ``mean`` (replicate measurements, one shared label), ``any`` (multiple-instance:
      the group is positive if any row is; the max of the rows' probabilities), ``last`` (the row latest in
      ``time_on`` carries the label and the prediction), ``select_min`` / ``select_max`` (choose the row with the
      lowest / highest prediction and score the true value of that row, as in algorithm selection). A method may
      return its own group prediction instead and is scored on the same unit.
    * ``context``: what a model may use about the group when predicting: ``none`` (the row only), ``all_rows`` (all
      rows of the group, as for a molecule whose conformations are all known), ``past_rows`` (the rows before it in
      ``time_on``).
    """

    on: str | list[str]
    """The group column(s)."""
    labels: GroupLabelTypes
    """``per_group`` (one label per group) or ``per_sample`` (labels may differ within a group)."""
    time_on: str | None = None
    """The order of the rows inside a group; never used for splitting."""
    definition: MultilineStr | None = None
    """What one group is, why groups are held out, and the use case with its source."""
    prediction_unit: PredictionUnit = "row"
    """``row`` (default) or ``group``: what one real-world prediction is."""
    aggregation: GroupAggregation | None = None
    """How the rows' predictions become one group prediction; set exactly when ``prediction_unit`` is ``group``."""
    context: GroupContext = "none"
    """What a model may use about the group at prediction time: ``none`` (default), ``all_rows`` or ``past_rows``."""

    def __post_init__(self):
        """Validate the rules between the fields that need no other metadata.

        The rules that need the target type are checked by :class:`PredictiveMLTaskMetadataV2`.
        """
        columns = as_column_list(self.on)
        if not columns or any(not str(c).strip() for c in columns):
            raise ValueError("Grouping.on must name the group column(s).")
        if len(set(columns)) != len(columns):
            raise ValueError(f"Grouping.on contains duplicate column names: {self.on!r}.")
        if self.prediction_unit == "group" and self.aggregation is None:
            raise ValueError(
                "prediction_unit='group' needs an aggregation (mean, any, last, select_min or select_max): how the "
                "rows' predictions become one prediction per group.",
            )
        if self.prediction_unit == "row" and self.aggregation is not None:
            raise ValueError(
                f"aggregation={self.aggregation!r} is set but prediction_unit is 'row'; an aggregation only applies "
                "when one prediction is made per group.",
            )
        if self.aggregation == "mean" and self.labels != "per_group":
            raise ValueError("aggregation='mean' averages replicates of one label: it needs labels='per_group'.")
        if self.aggregation in ("select_min", "select_max") and self.labels != "per_sample":
            raise ValueError(
                f"aggregation={self.aggregation!r} selects one row by its prediction and scores that row's true "
                "value: it needs labels='per_sample'.",
            )
        if self.aggregation == "last" and self.time_on is None:
            raise ValueError("aggregation='last' needs time_on: the order that defines a group's latest row.")
        if self.context == "past_rows" and self.time_on is None:
            raise ValueError("context='past_rows' needs time_on: the order that defines a row's earlier rows.")
        if self.time_on is not None and self.time_on in columns:
            raise ValueError(f"Grouping.time_on={self.time_on!r} is also a group column.")


# TODO: fields that might be cool to add in the future
#   - derived_from (to check for duplicates)
#   - dataset_version (unlikely, we track versions of these files in code repos?)
@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class DatasetMetadata:
    """Schema for metadata about a dataset."""

    unique_name: str
    """A unique name for the dataset."""

    dataset_year: str
    """The year when the data was collected/created.
    If unknown, the date when it was published. Specific the year from the original
    source or academic reference. Otherwise, provide an estimate.
    This is used to determine the age of the dataset.
    """
    domain_str: Domain
    """The real-world application domain of the dataset.
    Select one of the categories from the `Domain` type.

    How the domain of a dataset is defined is very subjective.
    Try to select such that it represents the context of the dataset.
    For example, if it is a insurance dataset about laptops, then
    the domain is "finance" rather than "technology & internet".
    """

    dataset_source: DatasetSource
    """The source from which the dataset was obtained.
    Select one of the options from the `DatasetSource` type.
    If none of the options fit, select "Other" or add to the `DatasetSource` type.

    Select the source of the original data were it was shared for the first time.
    The `original_dataset_source_download_link` below can point to a different source.
    """
    original_dataset_source_download_link: str
    """Link to the original dataset source.
    The DOI. Otherwise, URL to Kaggle, OpenML, etc.
    """
    download_description: MultilineStr
    """Code/CLI snippet or description that describes how the the dataset was
    downloaded from the original source and added to the local data warehouse.
    This is mostly needed for reproducibility purposes, not to automatically
    re-download the data.
    """

    academic_reference_bibtex: MultilineStr
    """Academic reference or a please-cite-request for the dataset.
    Bibtex, include DOI if possible."""
    academic_reference_bibtex_key: str
    """The Bibtex citation key for the entry from `academic_reference_bibtex`."""
    license: str | None
    """License under which the data is made available.
    E.g. "CC BY 4.0", "MIT, "GPL-3.0", "Public Domain".
    Set to None if license is unknown or missing.
    """

    data_tags: list[DataTags]
    """Tags that describe the context-depended data characteristics.
    Select one or more options from the `DataTags` type.

    Feel free to add new tags. Note, these tags shall describe things we
    cannot easily test for based on dataset characteristics. So do
    not tag things such as "high-dimensional" or "imbalanced".
    """
    curation_comments: MultilineStr | None
    """Notes from us about the dataset curation.

    This is a free text field that can include any relevant information
    about the dataset curation process, such as descriptions of any custom
    or special preprocessing steps you applied, or any oddities, anomalies,
    or manual fixes you encountered.

    Set to None, if there are no comments (e.g., you only had to load a CSV file).
    """

    version_from_unique_name: str | None = None
    """Indicates if the datasets is a version of another dataset.
    If the dataset is a version of another dataset, provide the unique_name of that dataset here.

    This name will be used to group them together in the data warehouse and to keep a
    linage of the dataset versions.
    """
    version_comment: MultilineStr | None = None
    """Comment about the dataset version and how it differs from the original dataset."""

    type_adapter_id: str = "dataset-mold-v1"
    """Identifier for name of the type adapter used to serialize/deserialize."""

    def __post_init__(self):
        """Validate what is checkable from this object alone.

        Cross-object and data-dependent checks (does the BibTeX compile, do the tags
        match the split regime, ...) live in :mod:`data_foundry.bundle_checks`.
        """
        if not SNAKE_CASE_PATTERN.fullmatch(self.unique_name or ""):
            raise ValueError(
                f"unique_name must be non-empty snake_case ([a-z0-9_]), got {self.unique_name!r}.",
            )
        if self.version_from_unique_name is not None:
            if self.version_from_unique_name == self.unique_name:
                raise ValueError(
                    f"version_from_unique_name equals unique_name ({self.unique_name!r}); a dataset cannot be a "
                    "version of itself. Give the version a distinct unique_name (e.g. `<name>_1m`).",
                )
            if not (self.version_comment or "").strip():
                raise ValueError(
                    "version_comment must describe how this version differs when version_from_unique_name is set.",
                )

    @property
    def path(self) -> Path:
        """Local directory where this dataset's raw downloads live.

        Resolves to ``<warehouse>/<unique_name>/`` where ``<warehouse>`` is
        the result of :func:`resolve_warehouse_dir` (i.e. respects the
        ``$DATA_FOUNDRY_WAREHOUSE`` env var, falling back to the editable
        install's ``local-data-warehouse/``).

        This is the directory the curation notebook's ``download_description``
        is expected to populate, and the directory the preprocessing cell
        reads from (e.g. ``pd.read_csv(dataset_mold.path / "raw.csv")``).
        The directory is **not** created here — call ``path.mkdir(parents=True,
        exist_ok=True)`` yourself if you need it materialized before download.

        Note: ``CuratedContainer.save`` writes containers under
        ``<warehouse>/<unique_name>/<uuid>/`` (or
        ``<warehouse>/<version_from_unique_name>/versions/<uuid>/`` for
        versioned datasets), so curated artifacts and raw downloads share the
        ``<unique_name>`` parent directory by design.
        """
        return resolve_warehouse_dir() / self.unique_name

    def describe(self) -> str:
        """Return a human-readable summary of every dataset-level field.

        Long multi-line fields (download description, BibTeX, curation
        comments) are truncated to one line so the summary stays scannable.
        """

        def _one_line(value: str | None, limit: int = 80) -> str:
            if value is None:
                return "None"
            first = value.strip().splitlines()[0] if value.strip() else ""
            return first if len(first) <= limit else first[: limit - 1] + "…"

        return "\n".join(
            [
                "DatasetMetadata:",
                f"  unique_name:                          {self.unique_name}",
                f"  dataset_year:                         {self.dataset_year}",
                f"  domain_str:                           {self.domain_str}",
                f"  dataset_source:                       {self.dataset_source}",
                f"  original_dataset_source_download_link: {self.original_dataset_source_download_link}",
                f"  download_description:                 {_one_line(self.download_description)}",
                f"  academic_reference_bibtex_key:        {self.academic_reference_bibtex_key}",
                f"  academic_reference_bibtex:            {_one_line(self.academic_reference_bibtex)}",
                f"  license:                              {self.license}",
                f"  data_tags:                            {self.data_tags}",
                f"  curation_comments:                    {_one_line(self.curation_comments)}",
                f"  version_from_unique_name:             {self.version_from_unique_name}",
                f"  version_comment:                      {_one_line(self.version_comment)}",
            ]
        )


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class PredictiveMLTaskMetadata:
    """Schema for metadata about a tabular predictive ML tasks."""

    target_column_name: str
    """The name of the target column in the dataset file."""
    problem_type: ProblemType
    """The type of predictive problem."""

    # TODO: figure out how to register custom metrics in a clean way somewhere.
    #    e.g. https://github.com/autogluon/tabarena/blob/main/tabarena/tabarena/metrics/custom_metrics.py
    objective_metric_name: str
    """The name of the objective metric used to evaluate model performance.
    Ideally, this define a custom metric for the task. If not, default to some
    reasonable metric (e.g. ROC AUC for binary classification, log loss for
    multiclass, RMSE for regression); use sklearn names where possible.
    """
    stratify_on: str | list[str] | None = None
    """The name of the column used for stratification during splitting."""
    time_on: str | None = None
    """The name of the column used for temporal splitting.

    Note, if you have temporal-grouped data and want to split the data such that you
    only predict on future groups, then do not set the group_on column. Since any temporal split
    would automatically ensure that the test groups are all from the future.

    In the cases where you do a grouped split and each group has rows ordered by a time index (e.g. a timestamp),
    we wont use that for splitting as a grouped split will ensure that all rows from a group are in the same split,
    so there is no risk of data leakage. We still want to keep this metadata as pipelines might need it.
    Thus, ensure to set `group_time_on` in that case.
    """
    group_on: str | list[str] | None = None
    """The name of the column used for grouping during splitting."""
    group_labels: GroupLabelTypes | None = None
    """Whether the group labels are per group or per sample.
        - If "per_group", then the group_on column contains one label per group,
            and all samples in the same group have the same label.
        - If "per_sample", then the group_on column contains a label for each sample,
            and samples in the same group can have different labels.
    """
    group_time_on: str | None = None
    """The name of the column that contains the time information for each group in case of grouped data.

    This column name is not used for splitting!

    Ensure to set this value if you have, for example, data about customers (group_on = "customer_id") and each row
    has a timestamp (group_time_on = "timestamp"), then we can read this metadata as "grouped data where the
    groups are ordered in time based on the group_time_on column".
    Moreover, the could include cases where different groups are not on the same time scale, but the model shall
    predict for a group based on the time information of that group. Thus, the pipeline needs to know this column
    to be able to normalize the time per group and globally correctly.
    """

    type_adapter_id: str = "predictive-ml-task-mold-v1"
    """Identifier for name of the type adapter used to serialize/deserialize."""

    def __post_init__(self):
        """Validate that the split configuration is internally coherent.

        Only checks that need no dataset and no other metadata object — whether the
        columns named here exist, have the right dtype, or match the splits is checked
        by :mod:`data_foundry.bundle_checks` once the bundle is assembled.
        """
        if not (self.target_column_name or "").strip():
            raise ValueError("target_column_name must name the target column.")

        # either group_on or time_on can be set, but not both
        if (self.group_on is not None) and (self.time_on is not None):
            raise ValueError(
                "group_on and time_on cannot both be set for the same task.Did you want to set `group_time_on`?"
            )
        if (self.group_on is not None) and (self.group_labels is None):
            raise ValueError(
                "If group_on is set, then group_labels must also be set to indicate whether "
                "the group labels are per group or per sample."
            )
        if (self.group_on is None) and (self.group_labels is not None):
            raise ValueError(
                f"group_labels={self.group_labels!r} is set but group_on is None; group labels only describe a "
                "grouped task.",
            )
        if (self.group_on is None) and (self.group_time_on is not None):
            raise ValueError(
                f"group_time_on={self.group_time_on!r} is set but group_on is None. Use `time_on` for the time "
                "column of a temporal split; `group_time_on` only records the time ordering *within* groups.",
            )

        group_columns = as_column_list(self.group_on)
        if len(set(group_columns)) != len(group_columns):
            raise ValueError(f"group_on contains duplicate column names: {self.group_on!r}.")

        for field_name in ("time_on", "group_time_on"):
            if getattr(self, field_name) == self.target_column_name:
                raise ValueError(
                    f"{field_name} cannot be the target column ({self.target_column_name!r}).",
                )
        if self.target_column_name in group_columns:
            raise ValueError(
                f"group_on cannot contain the target column ({self.target_column_name!r}).",
            )

        if (self.target_column_name in as_column_list(self.stratify_on)) and not self.is_classification:
            raise ValueError(
                f"stratify_on names the target column ({self.target_column_name!r}) but problem_type is "
                f"{self.problem_type!r}. A continuous target cannot be stratified on — drop stratify_on, or "
                "stratify on a discrete feature instead.",
            )

    @property
    def is_classification(self) -> bool:
        """Check if the task is a classification task."""
        return self.problem_type in ProblemTypeClassification

    @property
    def split_regime(self) -> str:
        """Classify the task's split regime based on which columns are set.

        Returns one of:

        * ``"temporal_non_iid"`` — ``time_on`` is set; rows are ordered in time
          and future rows must not leak into the training fold.
        * ``"grouped_non_iid"`` — ``group_on`` is set; all rows of a group stay
          together (``group_time_on`` may carry ordering info that is *not*
          used for splitting).
        * ``"iid"`` — neither is set; standard random / stratified splitting
          applies.

        ``time_on`` and ``group_on`` are mutually exclusive — see
        :meth:`__post_init__`.
        """
        if self.time_on is not None:
            return "temporal_non_iid"
        if self.group_on is not None:
            return "grouped_non_iid"
        return "iid"

    def describe(self) -> str:
        """Return a human-readable summary of every field plus the split regime.

        Use ``print(task.describe())`` to inspect a task at a glance — useful
        for example scripts and notebooks. See :attr:`split_regime` for the
        IID / temporal / grouped classification logic.
        """
        regime = self.split_regime
        if regime == "temporal_non_iid":
            regime_desc = f"temporal non-IID (time column: `{self.time_on}`)"
        elif regime == "grouped_non_iid":
            regime_desc = f"grouped non-IID (group column: `{self.group_on}`, labels={self.group_labels})"
        else:
            regime_desc = "IID"

        return "\n".join(
            [
                "PredictiveMLTaskMetadata:",
                f"  target_column_name:    {self.target_column_name}",
                f"  problem_type:          {self.problem_type}",
                f"  objective_metric_name: {self.objective_metric_name}",
                f"  stratify_on:           {self.stratify_on}",
                f"  time_on:               {self.time_on}",
                f"  group_on:              {self.group_on}",
                f"  group_labels:          {self.group_labels}",
                f"  group_time_on:         {self.group_time_on}",
                f"  is_classification:     {self.is_classification}",
                f"  → split regime:        {regime_desc}",
            ]
        )


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class PredictiveMLTaskMetadataV2:
    """The task metadata of a container built by a v2 definition (:mod:`data_foundry.v2`): container format 2.

    The regime is ``time_on`` for a temporal task (its horizon is in the splits metadata), ``grouping``
    (:class:`Grouping`) for a grouped task, and neither for an IID task. Unlike :class:`PredictiveMLTaskMetadata`
    (format 1: the v1 notebooks and the shipped BeyondArena containers), the group fields are stored once, in
    ``grouping``; ``group_on``, ``group_labels`` and ``group_time_on`` are read-only views of it, so code that reads
    both formats (the bundle checks, a benchmark harness) reads them the same way. The ``type_adapter_id`` marks the
    format (:attr:`~data_foundry.curation_container.CuratedContainer.format_version`).
    """

    target_column_name: str
    """The name of the target column in the dataset file."""
    problem_type: ProblemType
    """The type of predictive problem."""
    objective_metric_name: str
    """The metric that scores the task: sklearn names where possible, the problem type's default otherwise."""
    stratify_on: str | None = None
    """The column the IID or grouped splits are stratified on (the target of a classification task by default)."""
    time_on: str | None = None
    """The time column of a temporal task: every test row comes after every training row."""
    grouping: Grouping | None = None
    """How a grouped task is used (:class:`Grouping`): the group column, the labels, the order inside a group, the
    prediction unit, the aggregation and the context. The group column is metadata, never a model feature."""

    type_adapter_id: str = "predictive-ml-task-mold-v2"
    """Identifies container format 2."""

    def __post_init__(self):
        """Validate the regime, and the rules between the grouping and the target."""
        if not (self.target_column_name or "").strip():
            raise ValueError("target_column_name must name the target column.")
        if self.time_on is not None and self.grouping is not None:
            raise ValueError(
                "A task is temporal (time_on) or grouped (grouping), not both; record the order inside a group as "
                "grouping.time_on.",
            )
        if self.target_column_name in (self.time_on, self.group_time_on, *as_column_list(self.group_on)):
            raise ValueError(f"The target column ({self.target_column_name!r}) cannot be a time or group column.")
        if self.stratify_on == self.target_column_name and not self.is_classification:
            raise ValueError(
                f"stratify_on names the target column ({self.target_column_name!r}) but problem_type is "
                f"{self.problem_type!r}: a continuous target cannot be stratified on.",
            )
        aggregation = self.grouping.aggregation if self.grouping is not None else None
        if aggregation == "any" and self.problem_type != "binary_classification":
            raise ValueError(
                f"aggregation='any' (positive if any row is) needs a binary target, got {self.problem_type!r}.",
            )
        if aggregation in ("select_min", "select_max") and self.problem_type != "regression":
            raise ValueError(
                f"aggregation={aggregation!r} selects the row with the lowest / highest predicted value: it needs a "
                f"regression target, got {self.problem_type!r}.",
            )

    @property
    def group_on(self) -> str | list[str] | None:
        """The group column(s): ``grouping.on``."""
        return self.grouping.on if self.grouping is not None else None

    @property
    def group_labels(self) -> GroupLabelTypes | None:
        """``per_group`` or ``per_sample``: ``grouping.labels``."""
        return self.grouping.labels if self.grouping is not None else None

    @property
    def group_time_on(self) -> str | None:
        """The order of the rows inside a group: ``grouping.time_on``."""
        return self.grouping.time_on if self.grouping is not None else None

    @property
    def is_classification(self) -> bool:
        """Check if the task is a classification task."""
        return self.problem_type in ProblemTypeClassification

    @property
    def split_regime(self) -> str:
        """``temporal_non_iid`` (``time_on`` set), ``grouped_non_iid`` (``grouping`` set) or ``iid``."""
        if self.time_on is not None:
            return "temporal_non_iid"
        if self.grouping is not None:
            return "grouped_non_iid"
        return "iid"

    def describe(self) -> str:
        """Return a human-readable summary of every field plus the split regime."""
        lines = [
            "PredictiveMLTaskMetadataV2:",
            f"  target_column_name:    {self.target_column_name}",
            f"  problem_type:          {self.problem_type}",
            f"  objective_metric_name: {self.objective_metric_name}",
            f"  stratify_on:           {self.stratify_on}",
            f"  time_on:               {self.time_on}",
        ]
        grouping = self.grouping
        if grouping is not None:
            unit = grouping.prediction_unit + (f" ({grouping.aggregation})" if grouping.aggregation else "")
            lines += [
                f"  grouping.on:           {grouping.on}",
                f"  grouping.labels:       {grouping.labels}",
                f"  grouping.time_on:      {grouping.time_on}",
                f"  grouping.unit:         {unit}",
                f"  grouping.context:      {grouping.context}",
            ]
        lines += [f"  is_classification:     {self.is_classification}", f"  → split regime:        {self.split_regime}"]
        return "\n".join(lines)


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class PredictiveMLSplitsMetadata:
    """Schema for the outer data splits for training and testing of predictive ML."""

    splits_comment: str | MultilineStr
    """Comment about the splits and how they were created."""
    splits: dict[int, dict[int, tuple[list[int], list[int]]]]
    """The data splits for training and testing.

    A dictionary of train-tests splits per repeat and split/fold.

    These splits represent the outer splits that are used to evaluate models,
    and not the inner splits used for tuning/validation/HPO.

    The way we save the splits is similar to how OpenML does it:
    {
        repeat_id: {
            split_id: {
                (train_indices, test_indices)
            }
            ...
        }
        ...
    }
    where train_indices and test_indices are lists of indices, starting from 0.

    Note, this part of the code does not validate the splits or enforce any schema.
    It is up to the user to ensure that the splits are valid and make sense for the
    task at hand. Moreover, code that ingests these splits should also validate them
    for their specific purpose.
    """

    time_horizon: str | int | float | None = None
    """The time horizon for the splits for temporal splits.
    Defines the amount of time between the training and test splits for temporal splits.
    """
    time_horizon_unit: Literal["steps", "days", "weeks", "months", "years"] | str | None = None
    """The unit for the time_horizon.

        - If "steps", then the time_horizon is interpreted as a number of steps (e.g. rows) of time points in
            the test data. Use this if the time information is time index and not a timestamp.
        - If "months" or "years", then the time_horizon is interpreted as the number of calender months.
            This ignores that months vary in size!
        - If "days" or "weeks", then the time_horizon is interpreted as unit of 1 or 7 days, respectively.
    """

    split_random_state: int | None = None
    """The seed the splits were generated with (``random_state`` of the split builders in
    ``curation_recommendations``, :data:`~data_foundry.curation_recommendations.SPLIT_RANDOM_STATE` unless a
    caller chose another). Lets downstream code seed an aligned split, e.g. an inner validation split, without
    copying the number. ``None`` for splits recorded before this field existed (those k-fold and grouped k-fold
    splits were built with the default seed) and for splits not produced by those builders.
    """

    type_adapter_id: str = "predictive-ml-splits-mold-v1"
    """Identifier for name of the type adapter used to serialize/deserialize."""

    _OMIT_WHEN_UNSET: ClassVar[tuple[str, ...]] = ("split_random_state",)
    """Fields added after containers shipped: dropped from the checksum and the saved JSON while ``None``, so a
    container saved before ``split_random_state`` existed keeps verifying."""

    def __post_init__(self):
        """Validate the shape of the splits container and the horizon fields.

        Deliberately cheap: only checks that need neither the dataset nor the task
        metadata, so loading a container stays O(#folds) here. Everything that needs
        the data (index bounds, train/test overlap, leakage, coverage) is checked by
        :mod:`data_foundry.bundle_checks`.
        """
        if not self.splits:
            raise ValueError("splits must contain at least one repeat with one train/test split.")

        folds_per_repeat = {repeat_id: len(folds) for repeat_id, folds in self.splits.items()}
        empty_repeats = [repeat_id for repeat_id, n_folds in folds_per_repeat.items() if n_folds == 0]
        if empty_repeats:
            raise ValueError(f"Repeats {empty_repeats} contain no splits.")
        if len(set(folds_per_repeat.values())) > 1:
            raise ValueError(
                f"Every repeat must hold the same number of splits, got {folds_per_repeat}. Consumers assume a "
                "rectangular (repeat x fold) grid.",
            )
        for repeat_id, folds in self.splits.items():
            for fold_id, (train_indices, test_indices) in folds.items():
                if not train_indices or not test_indices:
                    raise ValueError(
                        f"Split (repeat={repeat_id}, fold={fold_id}) has an empty "
                        f"{'train' if not train_indices else 'test'} set.",
                    )

        if (self.time_horizon is None) != (self.time_horizon_unit is None):
            raise ValueError(
                f"time_horizon ({self.time_horizon!r}) and time_horizon_unit ({self.time_horizon_unit!r}) must be "
                "set together — a horizon without a unit is ambiguous.",
            )
        if self.time_horizon is not None:
            try:
                horizon = float(self.time_horizon)
            except (TypeError, ValueError):
                horizon = None
            if horizon is not None and horizon <= 0:
                raise ValueError(f"time_horizon must be positive, got {self.time_horizon!r}.")

    def describe(self) -> str:
        """Return a human-readable summary of the outer splits and split metadata.

        Reports the number of repeats, how many splits each repeat contains
        (collapsed to a single number when uniform; listed per-repeat
        otherwise), the total split count, the temporal-split metadata
        fields, and — at the end — a per-(repeat, fold) overview of the
        train/test sizes. Pair with :meth:`PredictiveMLTaskMetadata.describe`
        for the full task picture.
        """
        splits_per_repeat = {r: len(folds) for r, folds in self.splits.items()}
        total_splits = sum(splits_per_repeat.values())
        if splits_per_repeat and len(set(splits_per_repeat.values())) == 1:
            per_repeat_desc = f"{next(iter(splits_per_repeat.values()))} per repeat"
        else:
            per_repeat_desc = ", ".join(f"r{r}={n}" for r, n in splits_per_repeat.items()) or "(no splits)"

        lines = [
            "PredictiveMLSplitsMetadata:",
            f"  # repeats:           {len(self.splits)}",
            f"  splits/repeat:       {per_repeat_desc}",
            f"  total splits:        {total_splits}",
            f"  time_horizon:        {self.time_horizon}",
            f"  time_horizon_unit:   {self.time_horizon_unit}",
            f"  splits_comment:      {self.splits_comment}",
        ]

        if self.splits:
            preview_limit = 3
            flat = [
                (r, f, train_idx, test_idx)
                for r, folds in self.splits.items()
                for f, (train_idx, test_idx) in folds.items()
            ]
            preview = flat[:preview_limit]
            train_w = max(len(str(len(t))) for _, _, t, _ in preview)
            test_w = max(len(str(len(t))) for _, _, _, t in preview)
            header = "  splits shape (train / test sizes"
            if len(flat) > preview_limit:
                header += f", first {preview_limit} of {len(flat)}"
            header += "):"
            lines.append(header)
            for repeat_id, fold_id, train_idx, test_idx in preview:
                lines.append(
                    f"    r{repeat_id}/f{fold_id}:  train={len(train_idx):>{train_w}}  test={len(test_idx):>{test_w}}",
                )
            if len(flat) > preview_limit:
                lines.append(f"    … ({len(flat) - preview_limit} more)")
        else:
            lines.append("  splits shape:        (no splits)")

        return "\n".join(lines)
