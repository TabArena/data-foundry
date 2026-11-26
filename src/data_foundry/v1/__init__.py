"""Data Foundry v1: the format-1 metadata of the shipped BeyondArena containers.

v1 was the notebook flow behind BeyondArena (``DATA_FOUNDRY_V1.md``), retired for new datasets. This module keeps the
two format-1 metadata classes so that the pinned containers keep loading, describing and verifying: their checksums
encode exactly these fields. A new dataset is a definition that writes format 2
(:class:`~data_foundry.schema.DatasetMetadataV2`, :class:`~data_foundry.schema.PredictiveMLTaskMetadataV2`).
"""

from __future__ import annotations

from pathlib import Path

import pydantic

from data_foundry.schema import (
    SNAKE_CASE_PATTERN,
    DatasetSource,
    DataTags,
    Domain,
    GroupLabelTypes,
    MultilineStr,
    ProblemType,
    ProblemTypeClassification,
    Source,
    as_column_list,
    resolve_warehouse_dir,
)

__all__ = ["DatasetMetadata", "PredictiveMLTaskMetadata"]


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class DatasetMetadata:
    """Schema for metadata about a dataset (format 1, the v1 notebooks and BeyondArena).

    A v2 definition writes :class:`DatasetMetadataV2`. The properties :attr:`domain`, :attr:`publication`,
    :attr:`sources`, :attr:`derived_from` and :attr:`derivation` read both the same way.
    """

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

    # --- the v2 names, so readers handle both formats the same way ------------------------------------------------
    @property
    def domain(self) -> str:
        """:attr:`domain_str`."""
        return self.domain_str

    @property
    def publication(self) -> Source:
        """The flat source fields as the publication :class:`Source`."""
        return Source(
            role="publication",
            platform=self.dataset_source,
            url=self.original_dataset_source_download_link,
            license=self.license,
            year=self.dataset_year,
            bibtex=self.academic_reference_bibtex,
            bibtex_key=self.academic_reference_bibtex_key,
        )

    @property
    def sources(self) -> list[Source]:
        """[:attr:`publication`]: a format-1 dataset names one source."""
        return [self.publication]

    @property
    def derived_from(self) -> str | None:
        """:attr:`version_from_unique_name`."""
        return self.version_from_unique_name

    @property
    def derivation(self) -> str | None:
        """:attr:`version_comment`."""
        return self.version_comment


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

    def __post_init__(self):  # noqa: C901 - one validation rule after another
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
