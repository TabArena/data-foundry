from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal

import pydantic

MultilineStr = Annotated[str, "multiline"]

DEFAULT_LOCAL_DATA_DIR = str(Path(__file__).parent.parent.parent / "local-data-warehouse")

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

        return "\n".join([
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
        ])


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
            regime_desc = (
                f"grouped non-IID (group column: `{self.group_on}`, "
                f"labels={self.group_labels})"
            )
        else:
            regime_desc = "IID"

        return "\n".join([
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
        ])


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

    type_adapter_id: str = "predictive-ml-splits-mold-v1"
    """Identifier for name of the type adapter used to serialize/deserialize."""

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
            per_repeat_desc = ", ".join(
                f"r{r}={n}" for r, n in splits_per_repeat.items()
            ) or "(no splits)"

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
                    f"    r{repeat_id}/f{fold_id}:  "
                    f"train={len(train_idx):>{train_w}}  "
                    f"test={len(test_idx):>{test_w}}",
                )
            if len(flat) > preview_limit:
                lines.append(f"    … ({len(flat) - preview_limit} more)")
        else:
            lines.append("  splits shape:        (no splits)")

        return "\n".join(lines)
