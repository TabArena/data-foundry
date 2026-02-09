from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal

import pydantic

MultilineStr = Annotated[str, "multiline"]

DEFAULT_LOCAL_DATA_DIR = str(
    Path(__file__).parent.parent.parent / "local-data-warehouse"
)

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
    "OpenML",
    "GitHub",
    "UCI",
    "HuggingFace",
    "GOV Website",
    "Customer",
    "Other",
]
DataTags = Literal[
    # Important tags for the task
    "IID",
    "Non-IID",
    "Temporal",
    "Grouped",
    # Other context tags (not statistical information!)
    "Spatial",  # data that contains spatial/geographical information
    "Anonymized",  # data that has no semantic meaning anymore on purpose
    # data that is IID by construction of the data.
    #   - e.g. temporal data that is missing the timestamp
    "ForcedIIDFromTemporal",
]
ProblemType = Literal[
    "binary_classification", "multiclass_classification", "regression"
]
ProblemTypeClassification = [
    "binary_classification",
    "multiclass_classification",
]


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
    licence: str | None
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

    local_data_directory_base: str = DEFAULT_LOCAL_DATA_DIR
    """Link to a directory that contains the all data related files."""
    type_adapter_id: str = "dataset-mold-v1"
    """Identifier for name of the type adapter used to serialize/deserialize."""

    @property
    def path(self) -> Path:
        """Get the full local path to the dataset directory."""
        return Path(self.local_data_directory_base) / self.unique_name


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
    group_on: str | list[str] | None = None
    """The name of the column used for grouping during splitting."""
    time_on: str | None = None
    """The name of the column used for temporal splitting."""

    type_adapter_id: str = "predictive-ml-task-mold-v1"
    """Identifier for name of the type adapter used to serialize/deserialize."""

    @property
    def is_classification(self) -> bool:
        """Check if the task is a classification task."""
        return self.problem_type in ProblemTypeClassification


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

    type_adapter_id: str = "predictive-ml-splits-mold-v1"
    """Identifier for name of the type adapter used to serialize/deserialize."""
