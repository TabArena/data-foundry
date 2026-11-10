from __future__ import annotations

import dataclasses
import os
import re
from pathlib import Path
from typing import Annotated, Any, ClassVar, Literal

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
    # a task temporal by its use case, split grouped because it has too few periods for three test windows
    "ForcedGroupedFromTemporal",
    # Retired (2026-10-21): kept readable for containers that carry it; new definitions refuse it (RETIRED_DATA_TAGS).
    "2ndTierData",
    "WrongDomain",  # Task that was transformed to another domain (like audio) to tabular.
]
RETIRED_DATA_TAGS = ("2ndTierData",)
"""Tags old containers may carry and loading accepts, but a new definition may not set."""
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


MetricKind = Literal["standard", "custom", "local"]
MetricPrediction = Literal["proba", "label", "value"]
MetricOrigin = Literal["source", "stand_in", "context", "fallback"]
TargetTransform = Literal["identity", "log", "log1p", "log10"]


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class MetricSpec:
    """The metric that scores a task, as data: a reader without Data Foundry can implement it from these fields.

    Stored as :attr:`PredictiveMLTaskMetadataV2.objective_metric` (container format 2). The reference
    implementations of every ``standard`` and ``custom`` name are in :mod:`data_foundry.v2.metrics`
    (:func:`~data_foundry.v2.metrics.score`), a module that depends only on numpy, pandas, scikit-learn and scipy.
    """

    name: str
    """A standard name for a standard metric (``rmse``, ``roc_auc``, ``log_loss``, ``f1_weighted``, ...), a general
    one for a custom metric (``cost_matrix``, ``mean_group_pearsonr``); never a dataset's name."""
    kind: MetricKind
    """``standard`` (the name maps to a scikit-learn / scipy function), ``custom`` (Data Foundry ships the
    implementation) or ``local`` (code only the definition holds: never in a shipped container)."""
    prediction: MetricPrediction
    """What the scorer takes: ``proba`` (class probabilities), ``label`` (predicted classes) or ``value``."""
    greater_is_better: bool
    """Whether a higher score is better."""
    origin: MetricOrigin
    """``source`` (what the competition or paper scored), ``stand_in`` (the closest computable metric to an original
    that cannot be computed, named in ``original``), ``context`` (the source defines no metric, but the task makes one
    obvious, e.g. a relative error for a price; why in ``reason``) or ``fallback`` (the source defines no metric the
    task would use in practice, and none is obvious: roc_auc / log_loss / rmse by problem type, the reason in
    ``reason``)."""
    params: dict[str, Any] = dataclasses.field(default_factory=dict)
    """JSON values only: a cost matrix, ``k``, the shape of a transform."""
    inputs: dict[str, str] = dataclasses.field(default_factory=dict)
    """Each role the scorer needs (``group``, ``weight``, ``order``) mapped to a column of the frame. Such a column is
    a :class:`ScoringColumn` (never a feature), except the task's group or time column, which the metric reads where
    it is; a feature the metric also needs ships a copy as a scoring column (MET-2)."""
    original: str | None = None
    """The original metric as the source names it (``"RMSE"``, ``"per-era CORR"``)."""
    reference: str | None = None
    """Where the source defines the metric: a link to the evaluation page or the paper."""
    definition: str | None = None
    """The metric as a one-line formula."""
    reason: str | None = None
    """Why the metric is a fallback (the source defines none) or a stand-in (why the original cannot be computed)."""
    target_transform: TargetTransform = "identity"
    """Regression only: the scale the target ships on. The target ships transformed for modelling (``log`` for a
    price, ``log1p`` for a count); the metric is computed after the inverse (``exp``, ``expm1``, ``10**``) of both the
    true values and the predictions, so the declared metric is the one on the original scale."""

    def __post_init__(self):
        if not (self.name or "").strip():
            raise ValueError("MetricSpec.name must name the metric.")
        if self.target_transform != "identity" and self.prediction != "value":
            raise ValueError(
                f"MetricSpec.target_transform={self.target_transform!r} is for a regression metric (prediction "
                f"'value'), not one that takes {self.prediction!r}."
            )

    def describe_lines(self, indent: str = "  ") -> list[str]:
        """The spec as ``describe()`` lines: name, kind, origin, original, reference, definition, reason."""
        head = f"{self.name} ({self.kind}, {self.prediction}, {'higher' if self.greater_is_better else 'lower'} is "
        lines = [f"{indent}objective_metric:      {head}better; origin: {self.origin})"]
        for label, value in (
            ("original", self.original),
            ("reference", self.reference),
            ("definition", self.definition),
            ("reason", self.reason),
            ("params", self.params or None),
            ("inputs", self.inputs or None),
            ("target_transform", self.target_transform if self.target_transform != "identity" else None),
        ):
            if value:
                lines.append(f"{indent}  {label + ':':20s} {value}")
        if self.target_transform != "identity":
            lines[-1] += f" (the target ships on the {self.target_transform} scale; scored after the inverse)"
        return lines


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class ScoringColumn:
    """A column the metric needs to score a prediction (Numerai's ``era``, an asset weight): kept in the frame, never
    a model feature.

    Drop the scoring columns from the model's inputs (:func:`~data_foundry.curation_container.feature_columns`), then
    pass the test rows' values to the scorer (:func:`data_foundry.v2.metrics.scorer` looks them up by row index).
    """

    column: str
    """The column of the frame."""
    role: str
    """The role it plays for the metric: a key of :attr:`MetricSpec.inputs` (``group``, ``weight``, ``order``)."""
    used_by: str
    """The name of the metric that uses it."""
    description: str
    """What the column is and how the metric uses it, e.g. "the week a row belongs to; the metric is the mean of the
    per-era correlations"."""


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class UnitWeight:
    """A score that counts each unit once (MET-17): the metric's row weight is 1 over the rows of the row's unit, so
    the weights of each unit sum to 1 (each quadrat of a plot, each bleed of a mouse, each visit of a person).

    It is for scoring only, never a training weight (MET-15). A model that picks its settings on a validation split
    weights the validation loss by :attr:`column` too, so that it optimises what the test score counts
    (:func:`~data_foundry.curation_container.validation_weight`), and keeps a unit's rows on one side of that split.
    """

    column: str
    """The weight scoring column the metric reads (role ``weight``): 1 over the unit's number of rows."""
    unit: str
    """The column that names each row's unit (the task's group column, or a column kept for it): metadata, never a
    model feature."""


SpecialFeatureKind = Literal["smiles", "spectrum"]
"""What a :class:`SpecialFeature` holds: ``smiles``, a molecule's structure as a SMILES string (one column), or
``spectrum``, one spectrum per row (a group of columns, one per position on its axis)."""

SpecialFeatureLayout = Literal["column", "group"]
"""How a :class:`SpecialFeature` is stored: in one ``column``, or in a ``group`` of columns, in a fixed order, that
hold one object together and are encoded together."""

SpectrumTechnique = Literal["mass_spectrometry", "raman", "infrared", "near_infrared"]
"""How a spectrum was measured: by mass spectrometry (an m/z axis) or a vibrational spectroscopy (Raman, infrared,
near-infrared: a wavenumber or wavelength axis)."""

SpectrumState = Literal["raw", "processed", "peaks"]
"""What the source did to a spectrum before publishing it: nothing (``raw``, the instrument's intensities with their
baseline and scale), a correction or normalisation (``processed``), or a peak list on fixed bins (``peaks``)."""


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class SpectrumDetails:
    """What a ``spectrum`` special feature adds to its columns: where each sits on the axis and how it was measured."""

    axis: list[float]
    """The position of each column on the axis, strictly increasing (an m/z, a wavenumber, a bin number)."""
    axis_unit: str
    """The unit of :attr:`axis`: ``m/z``, ``cm-1``, ``nm``, or ``bin`` when the source does not give the positions."""
    technique: SpectrumTechnique
    """How the spectrum was measured."""
    state: SpectrumState
    """What the source did to the spectrum before publishing it."""

    def __post_init__(self):
        """The axis is strictly increasing."""
        if any(b <= a for a, b in zip(self.axis, self.axis[1:], strict=False)):
            raise ValueError("A spectrum's axis is not strictly increasing.")


SPECIAL_FEATURE_LAYOUTS: dict[str, str] = {"smiles": "column", "spectrum": "group"}
"""The layout of each kind: a SMILES is one column, a spectrum a group of columns."""


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class SpecialFeature:
    """A model input that needs handling beyond its dtype: one column (a SMILES) or a group of columns that hold one
    object together (a spectrum), recorded like the target and the scoring columns are.

    The columns stay in the frame and stay features (:func:`~data_foundry.curation_container.feature_columns`). A
    benchmark encodes a special feature by its :attr:`kind`, with the :attr:`recommended_encoding` or its own
    (:func:`~data_foundry.curation_container.special_features` lists them;
    :func:`data_foundry.v2.special.encode_special_feature` encodes one). Where :attr:`encoding_required` is true the
    raw values are no model input (a SMILES read as text adds nothing): encode the feature or leave it out. A
    definition declares its special features in ``special_features``.
    """

    name: str
    """The special feature's name: its column for a ``column`` layout, e.g. ``SMILES``; a name such as ``serum_ms``
    for a ``group``."""
    kind: SpecialFeatureKind
    """What it holds (``smiles``, ``spectrum``)."""
    layout: SpecialFeatureLayout
    """``column`` (one column) or ``group`` (several columns, in order, encoded together); fixed by the kind."""
    columns: list[str]
    """Its columns in the frame: one for a ``column`` layout, two or more in order (a spectrum's axis order) for a
    ``group``."""
    description: str
    """What it is: the form of the values, the instrument, what the source did to them."""
    encoding_required: bool
    """Whether the raw values are unusable as model inputs (a SMILES string) rather than usable numbers (a spectrum's
    intensities)."""
    recommended_encoding: str | None = None
    """The spec id of the encoding Data Foundry recommends, e.g. ``rdkit2d-maccs-ecfp4-rdkit2026.03.6-r1``."""
    details: SpectrumDetails | None = None
    """What the kind adds: :class:`SpectrumDetails` for a ``spectrum``, nothing for a ``smiles``."""

    def __post_init__(self):
        """The layout matches the kind and the number of columns, and the details match the kind."""
        if self.layout != SPECIAL_FEATURE_LAYOUTS[self.kind]:
            raise ValueError(f"A {self.kind} special feature has the {SPECIAL_FEATURE_LAYOUTS[self.kind]!r} layout.")
        if len(set(self.columns)) != len(self.columns):
            raise ValueError(f"Special feature {self.name!r} lists a column twice.")
        if self.layout == "column" and len(self.columns) != 1:
            raise ValueError(f"Special feature {self.name!r} is one column; got {len(self.columns)}.")
        if self.layout == "group" and len(self.columns) < 2:
            raise ValueError(f"Special feature {self.name!r} is a group and needs two columns or more.")
        if self.kind == "spectrum":
            if self.details is None:
                raise ValueError(f"Spectrum {self.name!r} needs its details (axis, unit, technique, state).")
            if len(self.details.axis) != len(self.columns):
                raise ValueError(
                    f"Spectrum {self.name!r} has {len(self.columns)} columns but {len(self.details.axis)} axis "
                    "positions."
                )
        elif self.details is not None:
            raise ValueError(f"A {self.kind} special feature takes no details.")


SourceRole = Literal["publication", "part", "copy"]
"""What a :class:`Source` is to its dataset: ``publication``, where the data were first published (the dataset's
year and citation are this source's); ``part``, a piece the dataset is assembled from (one of several survey waves, a
second table joined in); ``copy``, a later copy of the data, such as the re-upload we download (Kaggle, UCI)."""

_BIBTEX_KEY = re.compile(r"@\w+\s*\{\s*([^,\s}]+)\s*,")


def bibtex_keys(bibtex: str | None) -> list[str]:
    """The citation keys of the entries of ``bibtex``, in order."""
    return list(dict.fromkeys(_BIBTEX_KEY.findall(bibtex or "")))


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class Source:
    """One source of a dataset's data: where it was first published, a part it is assembled from, or a copy.

    A v2 definition lists its sources in ``sources``, the publication first::

        sources = (
            Source(role="publication", platform="UCI", url="https://doi.org/10.24432/C5...", license="CC BY 4.0",
                   year="2014", bibtex="@misc{...}"),
            Source(role="copy", platform="Kaggle", url="https://www.kaggle.com/...", license="CC0 1.0"),
        )

    Exactly one source is the publication; it needs a year and a BibTeX entry.
    """

    role: SourceRole
    """What the source is to the dataset (:data:`SourceRole`)."""
    platform: DatasetSource
    """Where the source is published: one of :data:`DatasetSource` ("Other" when none fits)."""
    url: str
    """A link to the source: its DOI where it has one, else the page that holds the data."""
    license: str | None
    """The license the source states, e.g. "CC BY 4.0"; None when it states none."""
    year: str | None = None
    """The year the source was first published (the publication's is the dataset's year)."""
    bibtex: MultilineStr | None = None
    """BibTeX of the work that published the source; required for the publication."""
    bibtex_key: str | None = None
    """The citation key(s) of :attr:`bibtex`, comma-separated; read from it when None."""
    name: str | None = None
    """A short label that tells sources apart, e.g. "the 2019 survey wave"."""
    files: list[str] = pydantic.Field(default_factory=list)
    """The raw files that come from this source: paths or glob patterns under the raw folder."""

    def __post_init__(self):
        """A link, a parsed citation key, and a year and BibTeX for the publication."""
        if not (self.url or "").strip():
            raise ValueError(f"A {self.role} source needs a `url`.")
        if self.role == "publication":
            if not str(self.year or "").strip():
                raise ValueError("The publication source needs its `year`.")
            if not (self.bibtex or "").strip():
                raise ValueError("The publication source needs its `bibtex`.")
        if self.bibtex_key is None and self.bibtex:
            self.bibtex_key = ",".join(bibtex_keys(self.bibtex)) or None
        bad = [f for f in self.files if not f or f.startswith("/") or ".." in Path(f).parts]
        if bad:
            raise ValueError(f"Source files are paths under the raw folder; got {bad}.")

    def label(self) -> str:
        """A short name for messages and tables: the name, else the platform and role."""
        return self.name or f"{self.platform} {self.role}"


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
class DatasetMetadataV2:
    """The dataset-level metadata of a format-2 container, built from a v2 definition.

    The provenance is a list of :class:`Source` (the publication first, then the parts it is assembled from and the
    copies); the dataset's year and citation are its publication's. A definition derived from another one (a family's
    child) names its parent in :attr:`derived_from` and says how it differs in :attr:`derivation`.
    """

    unique_name: str
    """The dataset's name, snake_case; equal to its definition's folder."""
    domain: Domain
    """The real-world application domain (one of :data:`Domain`), chosen by the context of the data."""
    sources: list[Source]
    """Where the data comes from: the publication first, then parts and copies."""
    download_description: MultilineStr
    """Commands (and notes) that recreate the raw files in the local data warehouse."""
    data_tags: list[DataTags]
    """Context tags and the split-regime tags (:data:`DataTags`)."""
    curation_comments: MultilineStr | None = None
    """The audit trail of the curation: the starting artifact, then one bullet per non-obvious decision."""
    derived_from: str | None = None
    """The ``unique_name`` of the definition this one derives from (its parent in a family), else None."""
    derivation: MultilineStr | None = None
    """How this dataset differs from :attr:`derived_from`; set exactly when it is."""

    type_adapter_id: str = "dataset-mold-v2"
    """Identifier for name of the type adapter used to serialize/deserialize."""

    def __post_init__(self):
        """A snake_case name, exactly one publication (listed first), and a derivation exactly with a parent."""
        if not SNAKE_CASE_PATTERN.fullmatch(self.unique_name or ""):
            raise ValueError(f"unique_name must be non-empty snake_case ([a-z0-9_]), got {self.unique_name!r}.")
        roles = [s.role for s in self.sources]
        if roles.count("publication") != 1 or roles[0] != "publication":
            raise ValueError(f"`sources` lists exactly one publication, first; got the roles {roles}.")
        if self.derived_from is not None and self.derived_from == self.unique_name:
            raise ValueError(f"derived_from equals unique_name ({self.unique_name!r}).")
        if (self.derived_from is None) != (not (self.derivation or "").strip()):
            raise ValueError("`derivation` says how the dataset differs from `derived_from`: set both or neither.")

    @property
    def publication(self) -> Source:
        """The source where the data were first published."""
        return self.sources[0]

    @property
    def path(self) -> Path:
        """``<warehouse>/<unique_name>/``, where this dataset's containers are saved."""
        return resolve_warehouse_dir() / self.unique_name

    def describe(self) -> str:
        """A human-readable summary of the dataset-level fields, long text cut to one line."""

        def one_line(value: str | None, limit: int = 80) -> str:
            first = (value or "").strip().splitlines()[0] if (value or "").strip() else ""
            return first if len(first) <= limit else first[: limit - 1] + "…"

        lines = [
            "DatasetMetadataV2:",
            f"  unique_name:          {self.unique_name}",
            f"  domain:               {self.domain}",
            f"  data_tags:            {self.data_tags}",
        ]
        for source in self.sources:
            year = f" ({source.year})" if source.year else ""
            lines.append(f"  {source.role + ':':21s} {source.platform}{year} {source.url}  license: {source.license}")
        lines += [
            f"  download_description: {one_line(self.download_description)}",
            f"  curation_comments:    {one_line(self.curation_comments)}",
        ]
        if self.derived_from is not None:
            lines.append(f"  derived_from:         {self.derived_from}: {one_line(self.derivation)}")
        return "\n".join(lines)


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
    objective_metric: MetricSpec
    """The metric that scores the task (:class:`MetricSpec`): the source's metric when it defines one, else the
    declared fallback. Replaces format 1's ``objective_metric_name``; the name is ``objective_metric.name``."""
    stratify_on: str | None = None
    """The column the IID or grouped splits are stratified on (the target of a classification task by default)."""
    time_on: str | None = None
    """The time column of a temporal task: every test row comes after every training row."""
    grouping: Grouping | None = None
    """How a grouped task is used (:class:`Grouping`): the group column, the labels, the order inside a group, the
    prediction unit, the aggregation and the context. The group column is metadata, never a model feature."""
    scoring_columns: list[ScoringColumn] = dataclasses.field(default_factory=list)
    """The columns the metric needs (:class:`ScoringColumn`): kept in the frame, never model features."""
    special_features: list[SpecialFeature] = dataclasses.field(default_factory=list)
    """Model inputs that need handling beyond their dtype (:class:`SpecialFeature`): one column (a SMILES) or a group
    of columns (a spectrum), each encoded by its kind."""
    sample_weight: str | None = None
    """The training weight: a scoring column that every model is fitted with as each row's weight, never a feature.
    It is the metric's row weight (a rate's realized denominator such as the years insured, MET-15), so training and
    scoring weight the rows alike. ``None``: models train unweighted."""
    unit_weight: UnitWeight | None = None
    """A score that counts each unit once (:class:`UnitWeight`, MET-17): the metric's row weight column and the column
    of the unit whose rows it splits 1 among. For scoring and validation only, never a training weight. ``None``: no
    unit weight (a row weight the metric reads is then an amount or a function of the features)."""

    type_adapter_id: str = "predictive-ml-task-mold-v2"
    """Identifies container format 2."""

    _OMIT_WHEN_UNSET: ClassVar[tuple[str, ...]] = ("sample_weight", "unit_weight")
    """Fields added after containers shipped: dropped from the checksum and the saved JSON while ``None``, so a
    container saved before they existed keeps verifying."""

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
        scoring = [c.column for c in self.scoring_columns]
        if len(set(scoring)) != len(scoring):
            raise ValueError(f"scoring_columns lists a column twice: {scoring}.")
        if self.target_column_name in scoring:
            raise ValueError(f"The target column ({self.target_column_name!r}) cannot be a scoring column.")
        self._check_sample_weight()
        self._check_unit_weight()
        self._check_special_features(scoring)
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

    def _check_sample_weight(self) -> None:
        """The training weight is a scoring column of role ``weight``, never a column models use."""
        if self.sample_weight is None:
            return
        weight = {c.column: c for c in self.scoring_columns}.get(self.sample_weight)
        if weight is None or weight.role != "weight":
            raise ValueError(
                f"sample_weight={self.sample_weight!r} names no scoring column of role 'weight': the training weight "
                "ships as the metric's weight column (a ScoringColumn with role='weight').",
            )
        used = {self.time_on, self.group_time_on, *as_column_list(self.group_on), *as_column_list(self.stratify_on)}
        if self.sample_weight in used:
            raise ValueError(f"sample_weight={self.sample_weight!r} is a time, group or stratification column.")

    def _check_unit_weight(self) -> None:
        """The unit weight is a weight scoring column the metric reads, for scoring only, and its unit is no column
        with another role (the target, a scoring column, a special feature).
        """
        if self.unit_weight is None:
            return
        column, unit = self.unit_weight.column, self.unit_weight.unit
        weight = {c.column: c for c in self.scoring_columns}.get(column)
        if weight is None or weight.role != "weight":
            raise ValueError(f"unit_weight.column={column!r} names no scoring column of role 'weight'.")
        if self.objective_metric.inputs.get("weight") != column:
            raise ValueError(
                f"unit_weight.column={column!r} is not the metric's weight input: map it with inputs={{'weight': "
                f"{column!r}}}."
            )
        if self.sample_weight == column:
            raise ValueError(
                f"unit_weight.column={column!r} is also the sample_weight: a unit weight is for scoring and "
                "validation only, never a training weight (MET-15, MET-17)."
            )
        if unit in (self.target_column_name, column) or unit in {c.column for c in self.scoring_columns}:
            raise ValueError(f"unit_weight.unit={unit!r} is the target or a scoring column.")
        if unit in {c for f in self.special_features for c in f.columns}:
            raise ValueError(f"unit_weight.unit={unit!r} is a column of a special feature.")

    def _check_special_features(self, scoring: list[str]) -> None:
        """Special features have distinct names and hold features only, each column in one special feature at most."""
        names = [f.name for f in self.special_features]
        if len(set(names)) != len(names):
            raise ValueError(f"special_features uses a name twice: {names}.")
        columns = [c for f in self.special_features for c in f.columns]
        if len(set(columns)) != len(columns):
            raise ValueError("A column is in two special features.")
        not_features = {self.target_column_name, self.time_on, *as_column_list(self.group_on), *scoring} - {None}
        if not_features & set(columns):
            raise ValueError(
                f"A special feature is a feature; {sorted(not_features & set(columns))[:5]} is the target, the time, a "
                "group or a scoring column.",
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
            *self.objective_metric.describe_lines(),
            f"  stratify_on:           {self.stratify_on}",
            f"  time_on:               {self.time_on}",
        ]
        for scoring in self.scoring_columns:
            use = "never a feature"
            if scoring.role == "weight":
                use += "; test-row values for the scorer only, never read when predicting a test row"
            lines.append(
                f"  scoring column:        {scoring.column} (role {scoring.role}, used by {scoring.used_by}; {use}): "
                f"{scoring.description}"
            )
        if self.sample_weight is not None:
            lines.append(
                f"  sample weight:         {self.sample_weight} (fit every model with it as the row weight; never a "
                "feature)"
            )
        if self.unit_weight is not None:
            lines.append(
                f"  unit weight:           {self.unit_weight.column} (each {self.unit_weight.unit} counts once in "
                "the score: weight a validation loss by it too; never a training weight or a feature)"
            )
        for feature in self.special_features:
            spectrum = feature.details
            where = (
                f"; {spectrum.technique}, {spectrum.state}, {spectrum.axis_unit} {spectrum.axis[0]:g} to "
                f"{spectrum.axis[-1]:g}"
                if spectrum is not None
                else ""
            )
            lines.append(
                f"  special feature:       {feature.name} ({feature.kind}, {feature.layout} of "
                f"{len(feature.columns):,}{where}; recommended encoding {feature.recommended_encoding})"
            )
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


def rows_text(n: int) -> str:
    """A row count for comments and names: 1,500,000 -> "1.5M", 500,000 -> "500k"."""
    return f"{n / 1e6:g}M" if n >= 1_000_000 else f"{n / 1e3:g}k"


@pydantic.dataclasses.dataclass(frozen=True, config=pydantic.ConfigDict(extra="forbid"))
class RowBudget:
    """The most rows any outer split trains and tests on, for data sub-sampled to a budget.

    Data Foundry sets no budget by default: the splits use the full frame. A v2 definition that declares one
    (``row_budget = RowBudget(train=..., test=...)``) is a sub-sampled version named after its train budget
    (:attr:`suffix`), and the container records the budget in
    :attr:`PredictiveMLSplitsMetadata.row_budget`. TabArena v0.2 sub-samples its larger datasets to
    ``RowBudget(train=1_000_000, test=500_000)`` (its ``_1m`` versions).

    Attributes:
        train: No split trains on more rows than this.
        test: No split tests on more rows than this.
    """

    train: pydantic.PositiveInt
    test: pydantic.PositiveInt

    @property
    def suffix(self) -> str:
        """The name suffix of a version sampled to this budget, from its train budget.

        10M -> ``"10m"``, 2.5M -> ``"2p5m"``, 300k -> ``"300k"``.
        """
        return rows_text(self.train).lower().replace(".", "p")

    def describe(self) -> str:
        """``"at most 1M train / 500k test rows per split"``."""
        return f"at most {rows_text(self.train)} train / {rows_text(self.test)} test rows per split"


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
    Defines the amount of time between the training and test splits for temporal splits: a positive number of
    ``time_horizon_unit`` (a few shipped containers store it as text, such as ``"1"``).
    """
    time_horizon_unit: Literal["steps", "days", "weeks", "months", "years"] | None = None
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

    time_gap: int | float | None = None
    """The gap between the end of each training side and the start of its test window, for temporal splits: a
    positive number of ``time_gap_unit``. No row of that span is in either side, usually because its labels were not
    known yet when the model is refit (a completion rate published six years after entry). ``None`` when the splits
    leave no gap, and for splits recorded before this field existed.
    """
    time_gap_unit: Literal["steps", "minutes", "hours", "days", "weeks", "months", "years"] | None = None
    """The unit of ``time_gap``, read as ``time_horizon_unit`` is; a gap can also be in ``"minutes"`` or ``"hours"``
    (a label known minutes after its row)."""

    row_budget: RowBudget | None = None
    """The budget the data was sub-sampled to: no split trains on more than ``row_budget.train`` or tests on more
    than ``row_budget.test`` rows, and the split checks hold the container to it. ``None``: no budget, the splits use
    the full frame (and splits recorded before this field existed)."""

    type_adapter_id: str = "predictive-ml-splits-mold-v1"
    """Identifier for name of the type adapter used to serialize/deserialize."""

    _OMIT_WHEN_UNSET: ClassVar[tuple[str, ...]] = ("split_random_state", "time_gap", "time_gap_unit", "row_budget")
    """Fields added after containers shipped: dropped from the checksum and the saved JSON while ``None``, so a
    container saved before they existed keeps verifying."""

    def __post_init__(self):
        """Validate the shape of the splits container and the horizon fields.

        Deliberately cheap: only checks that need neither the dataset nor the task
        metadata, so loading a container stays O(#folds) here. Everything that needs
        the data (index bounds, train/test overlap, leakage, coverage) is checked by
        :mod:`data_foundry.bundle_checks`.
        """
        if not self.splits:
            raise ValueError("splits must contain at least one repeat with one train/test split.")

        self._check_split_ids()
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
                raise ValueError(
                    f"time_horizon must be a number of {self.time_horizon_unit}, got {self.time_horizon!r}.",
                ) from None
            if horizon <= 0:
                raise ValueError(f"time_horizon must be positive, got {self.time_horizon!r}.")
        if (self.time_gap is None) != (self.time_gap_unit is None):
            raise ValueError(
                f"time_gap ({self.time_gap!r}) and time_gap_unit ({self.time_gap_unit!r}) must be set together.",
            )
        if self.time_gap is not None and self.time_gap <= 0:
            raise ValueError(f"time_gap must be positive (None for no gap), got {self.time_gap!r}.")

    def _check_split_ids(self) -> None:
        """Repeat ids ``0..R-1``, and fold ids ``0..F-1`` in every repeat (consumers index them by position)."""
        repeat_ids = sorted(self.splits)
        if repeat_ids != list(range(len(repeat_ids))):
            raise ValueError(f"Repeat ids must be 0..{len(repeat_ids) - 1}, got {repeat_ids[:10]}.")
        for repeat_id, folds in self.splits.items():
            fold_ids = sorted(folds)
            if fold_ids != list(range(len(fold_ids))):
                raise ValueError(f"Fold ids of repeat {repeat_id} must be 0..{len(fold_ids) - 1}, got {fold_ids[:10]}.")

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
            f"  time_gap:            {self.time_gap} {self.time_gap_unit or ''}".rstrip(),
            f"  splits_comment:      {self.splits_comment}",
        ]
        if self.row_budget is not None:
            lines.insert(-1, f"  row_budget:          {self.row_budget.describe()}")

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
