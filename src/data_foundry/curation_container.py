from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import pandas as pd
from pydantic import TypeAdapter
from uuid6 import uuid7

from data_foundry.schema import (
    DatasetMetadata,
    Grouping,
    MultilineStr,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadata,
    PredictiveMLTaskMetadataV2,
    resolve_warehouse_dir,
)
from data_foundry.utils.checksum import (
    CHECKSUM_VERSION,
    categorical_details,
    checksum_version,
    encode_dataset,
    encode_dataset_v2,
    encode_pydantic_metadata,
    omit_unset_fields,
)
from data_foundry.utils.dtypes import is_str_dtype

logger = logging.getLogger(__name__)

MetadataRegistry = {
    DatasetMetadata.type_adapter_id: DatasetMetadata,
    PredictiveMLTaskMetadata.type_adapter_id: PredictiveMLTaskMetadata,
    PredictiveMLTaskMetadataV2.type_adapter_id: PredictiveMLTaskMetadataV2,
    PredictiveMLSplitsMetadata.type_adapter_id: PredictiveMLSplitsMetadata,
}
FORMAT_VERSIONS = {
    PredictiveMLTaskMetadata.type_adapter_id: 1,
    PredictiveMLTaskMetadataV2.type_adapter_id: 2,
}
"""The container format of each task metadata class: 1 for the v1 notebooks (and the shipped BeyondArena
containers), 2 for the v2 definitions (:mod:`data_foundry.v2`)."""
NoIndentMetadata = [
    PredictiveMLSplitsMetadata.type_adapter_id,
]


@dataclass
class CuratedContainer:
    """Schema for a collection of curated items, ready to be used by others."""

    _RESERVED_EXTRA_FILENAMES: ClassVar[frozenset[str]] = frozenset(
        {
            "dataset.parquet",
            "dtypes.json",
            "categories.json",
            "test_dataset.parquet",
            "test_dtypes.json",
            "test_categories.json",
            "container_metadata.json",
        }
    )
    _REQUIRED_METADATA: ClassVar[tuple[str, ...]] = ("dataset_metadata", "task_metadata", "experiment_metadata")

    dataset: pd.DataFrame
    """The curated dataset as a pandas DataFrame."""
    dataset_metadata: DatasetMetadata
    """Metadata about the dataset."""
    task_metadata: PredictiveMLTaskMetadata | PredictiveMLTaskMetadataV2
    """Metadata about the task for the dataset; its class sets the container format (:attr:`format_version`)."""
    experiment_metadata: PredictiveMLSplitsMetadata
    """Metadata about the experiments for the task."""

    # Special cases
    test_dataset: pd.DataFrame | None = None
    """An optional test dataset. Used for inference/deployment evaluation."""

    # Container Metadata
    version_comment: MultilineStr | None = None
    """A comment about the version of the curated data collection. If no changes
    compared to the first version, set to None."""
    uuid: str | None = None
    """A unique identifier for the curated data collection."""
    checksum: str | None = None
    """A checksum for the curated data collection to verify integrity (see :data:`CHECKSUM_VERSION`): the frame,
    the metadata and, from version 2 on, the test set's checksum. Check it with :meth:`verify`."""
    test_dataset_checksum: str | None = None
    """The checksum of :attr:`test_dataset` (version 2 on, when there is a test set). The container checksum
    includes it, so a container verifies without loading its test set."""

    # Cache meta-data
    loaded_from_path: Path | None = None
    """The path from which the curated container was loaded, if applicable. Used for caching purposes."""

    def __post_init__(self):
        """Text categories as ``object`` under any pandas version, then the UUID and, for a new container, the frame
        checks and the checksums.

        Raises:
            ValueError: A new container's frame has a column name that is not a string, or an index other than
                ``0..n-1`` (the files keep neither, so the checksum would not verify after a save).
        """
        if self.dataset is not None:
            self.dataset = self._text_categories_as_object(self.dataset)
        if self.test_dataset is not None:
            self.test_dataset = self._text_categories_as_object(self.test_dataset)
        if self.uuid is None:
            self.uuid = self._create_uuid()
        if self.checksum is None:
            for label, frame in (("dataset", self.dataset), ("test_dataset", self.test_dataset)):
                if frame is not None:
                    self._check_new_frame(frame, label)
            if self.test_dataset is not None:
                self.test_dataset_checksum = self._create_test_checksum()
            self.checksum = self._create_checksum(CHECKSUM_VERSION)

    @staticmethod
    def _check_new_frame(df: pd.DataFrame, label: str) -> None:
        """Refuse what a save would not keep: non-string column names and an index other than ``0..n-1``."""
        not_str = [c for c in df.columns if not isinstance(c, str)]
        if not_str:
            raise ValueError(f"`{label}` has column names that are not strings: {not_str[:5]}.")
        index = df.index
        if not (isinstance(index, pd.RangeIndex) and index.start == 0 and index.step == 1):
            raise ValueError(
                f"`{label}` needs the index 0..n-1 (a RangeIndex); the files do not keep the index. "
                "Call `df.reset_index(drop=True)` first.",
            )

    @property
    def unique_name(self) -> str:
        """Return a unique name for the container."""
        return f"{self.dataset_metadata.unique_name}/{self.uuid}"

    @property
    def format_version(self) -> int:
        """The container format: 1 for a v1 notebook (every shipped BeyondArena container), 2 for a v2 definition.

        Set by the class of :attr:`task_metadata`; a format-2 container also writes it to ``container_metadata.json``.
        """
        return FORMAT_VERSIONS[self.task_metadata.type_adapter_id]

    @property
    def grouping(self) -> Grouping | None:
        """How a grouped task is used (:class:`~data_foundry.schema.Grouping`), or None for an IID or temporal task.

        Format 2 only. A format-1 container records just ``group_on`` / ``group_labels`` / ``group_time_on``, not the
        prediction unit, the aggregation or the context, so asking it for a grouping raises.
        """
        if self.format_version < 2:
            raise NotImplementedError(
                f"{self.dataset_metadata.unique_name}: a format-{self.format_version} container has no grouping "
                "block (only task_metadata.group_on / group_labels / group_time_on); rebuild it from its v2 "
                "definition, or check `container.format_version >= 2` first.",
            )
        return self.task_metadata.grouping

    @property
    def container_metadata(self) -> dict[str, str | int | None]:
        """Return a dictionary of the container's metadata."""
        assert self.uuid is not None, "UUID must be set."
        assert self.checksum is not None, "Checksum must be set."

        metadata = {
            "uuid": self.uuid,
            "checksum": self.checksum,
            "version_comment": self.version_comment,
        }
        if self.format_version >= 2:  # format 1 keeps the file its readers know
            metadata["format_version"] = self.format_version
        if self.test_dataset_checksum is not None:
            metadata["test_dataset_checksum"] = self.test_dataset_checksum
        return metadata

    @staticmethod
    def _create_uuid() -> str:
        """Create a new unique identifier for the curated data collection."""
        return str(uuid7())

    def _create_checksum(self, version: int | None = None) -> str:
        """The checksum of the frame and the metadata, by ``version`` (default: the version of :attr:`checksum`, or
        :data:`CHECKSUM_VERSION` for a container without one). Version 2 also covers the categories and, through
        :attr:`test_dataset_checksum`, the test set.
        """
        # Ensure container is fully loaded before calculating checksum
        if self.dataset is None:
            raise ValueError("Dataset must be loaded to calculate checksum.")
        if version is None:
            version = checksum_version(self.checksum) if self.checksum else CHECKSUM_VERSION

        print("Calculating checksum for curated container...")
        h = hashlib.blake2b(digest_size=32)
        h.update(b"\0")
        h.update(b"dataset\0")
        h.update(encode_dataset(self.dataset) if version == 1 else encode_dataset_v2(self.dataset))
        h.update(b"dataset_metadata\0")
        h.update(encode_pydantic_metadata(self.dataset_metadata))
        h.update(b"task_metadata\0")
        h.update(encode_pydantic_metadata(self.task_metadata))
        h.update(b"experiment_metadata\0")
        h.update(encode_pydantic_metadata(self.experiment_metadata))
        if version == 1:
            return h.hexdigest()
        if version != 2:
            raise ValueError(f"Unknown checksum version {version}.")
        if self.test_dataset_checksum is not None:
            h.update(b"test_dataset\0")
            h.update(self.test_dataset_checksum.encode())
        return f"v{version}:{h.hexdigest()}"

    def _create_test_checksum(self) -> str:
        """The version-2 checksum of :attr:`test_dataset` (its frame alone)."""
        if self.test_dataset is None:
            raise ValueError("The test dataset must be loaded to calculate its checksum.")
        return f"v2:{hashlib.blake2b(encode_dataset_v2(self.test_dataset), digest_size=32).hexdigest()}"

    def verify(self) -> bool:
        """Whether the stored checksums match the data: the container's, and the test set's when it is loaded.

        Works for every checksum version; a container whose test set is not loaded is checked against the stored
        test-set checksum.
        """
        if self.checksum != self._create_checksum():
            return False
        if self.test_dataset is not None and self.test_dataset_checksum is not None:
            return self.test_dataset_checksum == self._create_test_checksum()
        return True

    def _feature_dtype_counts(self) -> dict[str, int]:
        """Count feature-column dtypes.

        Excludes the target column and any ``group_on`` columns. Binary
        columns (exactly two distinct non-null values, regardless of dtype)
        are counted only in the ``binary`` bucket — the ``numeric``,
        ``categorical``, ``datetime``, and ``text`` buckets all exclude
        binary columns, so the four buckets plus ``binary`` partition
        ``n_features``.
        """
        excluded: set[str] = {self.task_metadata.target_column_name}
        group_on = self.task_metadata.group_on
        if isinstance(group_on, list):
            excluded.update(group_on)
        elif isinstance(group_on, str):
            excluded.add(group_on)

        feature_df = self.dataset.drop(
            columns=[c for c in excluded if c in self.dataset.columns],
        )
        binary_cols = {c for c in feature_df.columns if feature_df[c].nunique(dropna=True) == 2}
        numeric_cols = feature_df.select_dtypes(include=["number"], exclude=["bool"]).columns
        categorical_cols = feature_df.select_dtypes(include=["category", "bool"]).columns
        datetime_cols = list(feature_df.select_dtypes(include=["datetime", "datetimetz"]).columns)
        datetime_cols += [c for c in feature_df.columns if isinstance(feature_df[c].dtype, pd.PeriodDtype)]
        text_cols = feature_df.select_dtypes(include=["string"]).columns

        return {
            "numeric": sum(c not in binary_cols for c in numeric_cols),
            "categorical": sum(c not in binary_cols for c in categorical_cols),
            "datetime": sum(c not in binary_cols for c in datetime_cols),
            "text": sum(c not in binary_cols for c in text_cols),
            "binary": len(binary_cols),
            "n_features": feature_df.shape[1],
        }

    def describe_container(self) -> str:
        """Return the container-level identity: ``unique_name``, ``uuid``, ``checksum``.

        These are *container* attributes (not dataset/task/experiment
        metadata). UUID and checksum are truncated so the summary stays on
        one line each.
        """
        uuid_short = (self.uuid or "")[:18] + "…" if self.uuid and len(self.uuid) > 18 else self.uuid
        checksum_short = (
            (self.checksum or "")[:16] + "…" if self.checksum and len(self.checksum) > 16 else self.checksum
        )
        return "\n".join(
            [
                "CuratedContainer:",
                f"  unique_name:   {self.dataset_metadata.unique_name}",
                f"  uuid:          {uuid_short}",
                f"  checksum:      {checksum_short}",
            ]
        )

    def describe_dataset(self) -> str:
        """Return the DataFrame summary: shape and feature-dtype counts.

        Covers only the loaded :attr:`dataset` — see
        :meth:`describe_container` for the container's identity and
        :meth:`DatasetMetadata.describe` for the dataset-level metadata.
        """
        if self.dataset is None:
            raise ValueError("Dataset must be loaded before calling describe_dataset().")

        counts = self._feature_dtype_counts()
        target = self.task_metadata.target_column_name
        return "\n".join(
            [
                "Dataset:",
                f"  shape:         {self.dataset.shape}",
                f"  feature dtypes ({counts['n_features']} features, excluding target `{target}`):",
                f"    numeric:     {counts['numeric']}",
                f"    categorical: {counts['categorical']}",
                f"    datetime:    {counts['datetime']}",
                f"    text:        {counts['text']}",
                f"    binary:      {counts['binary']}",
            ]
        )

    def describe(self) -> str:
        """Return a high-level summary of the container.

        Composes :meth:`describe_container` (identity), :meth:`describe_dataset`
        (shape + dtype counts), and the per-section :meth:`describe` outputs
        of the dataset, task, and experiment metadata objects.
        """
        return "\n".join(
            [
                self.describe_container(),
                "",
                self.describe_dataset(),
                "",
                self.dataset_metadata.describe(),
                "",
                self.task_metadata.describe(),
                "",
                self.experiment_metadata.describe(),
            ]
        )

    @staticmethod
    def _save_dtypes(df: pd.DataFrame, path: Path) -> None:
        """Save DataFrame column dtypes to a JSON file."""
        dtypes = {str(col): str(dtype) for col, dtype in df.dtypes.items()}
        with path.open("w") as f:
            json.dump(dtypes, f, indent=2)

    @staticmethod
    def _save_categories(df: pd.DataFrame, path: Path) -> None:
        """Save each categorical column's categories (in order), their dtype and ``ordered``; ``dtypes.json`` only
        says ``category``. Not written when the frame has no categorical column.
        """
        details = categorical_details(df)
        if details:
            with path.open("w") as f:
                json.dump(details, f, indent=1, default=str)

    @staticmethod
    def _restore_categories(df: pd.DataFrame, path: Path) -> pd.DataFrame:
        """Give the categorical columns the categories, order and ``ordered`` that :meth:`_save_categories` wrote.

        Parquet alone can return integer categories with missing values as floats, and re-sort a custom order.
        Containers saved before the file existed are left as they load.
        """
        if not path.exists():
            return df
        with path.open("r") as f:
            details = json.load(f)
        for col, detail in details.items():
            if col not in df.columns:
                logger.warning("Column '%s' from %s not found in DataFrame — skipping.", col, path.name)
                continue
            categories = pd.Index(detail["categories"], dtype=detail["categories_dtype"])
            dtype = pd.CategoricalDtype(categories, ordered=detail["ordered"])
            if df[col].dtype != dtype or list(df[col].cat.categories) != list(categories):
                df[col] = df[col].astype(dtype)
        return df

    @staticmethod
    def _restore_dtypes(df: pd.DataFrame, path: Path) -> pd.DataFrame:
        """Restore DataFrame column dtypes from a JSON file.

        If the file does not exist, logs a warning and returns the DataFrame with only its text categories fixed.
        If a column cast fails, logs a warning for that column and skips it. Text categories come back as
        ``object``, as pandas 2 reads them (pandas 3 reads them as ``str``), so both load the same frame.
        """
        if not path.exists():
            logger.warning("dtype file %s not found — skipping dtype restoration (backward compatibility).", path)
            return CuratedContainer._text_categories_as_object(df)

        with path.open("r") as f:
            dtypes = json.load(f)

        for col, dtype_str in dtypes.items():
            if col not in df.columns:
                logger.warning("Column '%s' from dtype file not found in DataFrame — skipping.", col)
                continue
            if str(df[col].dtype) == dtype_str:
                continue
            try:
                df[col] = df[col].astype(dtype_str)
            except (ValueError, TypeError) as e:
                logger.warning("Failed to cast column '%s' to %s: %s — skipping.", col, dtype_str, e)
        return CuratedContainer._text_categories_as_object(df)

    @staticmethod
    def _text_categories_as_object(df: pd.DataFrame) -> pd.DataFrame:
        """Give categorical columns with pandas 3 ``str`` categories ``object`` categories, as pandas 2 makes them.

        Returns ``df`` itself when there is nothing to change, else a shallow copy. The checksum hashes both alike.
        """
        out = df
        for col in df.columns:
            dtype = df[col].dtype
            if isinstance(dtype, pd.CategoricalDtype) and is_str_dtype(dtype.categories.dtype):
                out = df.copy(deep=False) if out is df else out
                out[col] = df[col].cat.rename_categories(dtype.categories.astype(object))
        return out

    def _save_path(self, save_dir: Path) -> Path:
        """Resolve the on-disk save directory for this container under ``save_dir``."""
        meta = self.dataset_metadata
        path_name = meta.version_from_unique_name or meta.unique_name
        base = save_dir / path_name
        if meta.version_from_unique_name is not None:
            base = base / "versions"
        return base / self.uuid

    def save(self, save_dir: Path | str | None = None) -> Path:
        """Save the curated data collection under ``save_dir`` (default: the warehouse,
        ``$DATA_FOUNDRY_WAREHOUSE`` or ``local-data-warehouse/``).

        The container is written to
        ``<save_dir>/<unique_name>/<uuid>/`` (or
        ``<save_dir>/<version_from_unique_name>/versions/<uuid>/`` for
        versioned datasets).
        """
        save_dir = resolve_warehouse_dir() if save_dir is None else Path(save_dir)
        final_path = self._save_path(save_dir)
        final_path.parent.mkdir(parents=True, exist_ok=True)
        warehouse_path = final_path.relative_to(save_dir)
        print(f"Saving curated container to {warehouse_path}")
        # write into a temporary folder next to the target and rename it at the end, so an interrupted save never
        # leaves a half-written container under the UUID
        save_path = final_path.parent / f".{final_path.name}.saving-{os.getpid()}"
        if save_path.exists():
            shutil.rmtree(save_path)
        save_path.mkdir()

        # Save dataset
        dataset_path = save_path / "dataset.parquet"
        self.dataset.to_parquet(dataset_path, index=False)
        self._save_dtypes(self.dataset, save_path / "dtypes.json")
        self._save_categories(self.dataset, save_path / "categories.json")

        if self.test_dataset is not None:
            test_dataset_path = save_path / "test_dataset.parquet"
            self.test_dataset.to_parquet(test_dataset_path, index=False)
            self._save_dtypes(self.test_dataset, save_path / "test_dtypes.json")
            self._save_categories(self.test_dataset, save_path / "test_categories.json")

        # Save metadata
        for meta_name, meta_obj in [
            ("dataset_metadata", self.dataset_metadata),
            ("task_metadata", self.task_metadata),
            ("experiment_metadata", self.experiment_metadata),
        ]:
            assert "." not in meta_name, "Meta names cannot contain dots!"
            adapter = TypeAdapter(MetadataRegistry[meta_obj.type_adapter_id])
            meta_path = save_path / f"{meta_name}.{meta_obj.type_adapter_id}.json"
            indent = None if meta_obj.type_adapter_id in NoIndentMetadata else 2
            with meta_path.open("w") as f:
                json.dump(omit_unset_fields(meta_obj, adapter.dump_python(meta_obj, mode="json")), f, indent=indent)

        with (save_path / "container_metadata.json").open("w") as f:
            json.dump(self.container_metadata, f, indent=2)

        if final_path.exists():  # saving the same UUID again replaces it
            shutil.rmtree(final_path)
        save_path.rename(final_path)
        return final_path

    def load_test_dataset(self, path: Path | str | None = None) -> pd.DataFrame:
        """Load the test dataset if it exists."""
        if self.test_dataset is not None:
            return self.test_dataset

        if path is None:
            if self.loaded_from_path is not None:
                path = self.loaded_from_path
            else:
                raise ValueError("Path must be provided to load test dataset if not already loaded.")

        self.test_dataset = self._load_test_dataset(path=path)

        if self.test_dataset is None:
            raise ValueError("Curation container path does not include a test dataset!")

        return self.test_dataset

    @staticmethod
    def _load_test_dataset(path: Path) -> pd.DataFrame | None:
        """Load the test dataset if it exists."""
        test_dataset_path = path / "test_dataset.parquet"
        if test_dataset_path.exists():
            df = pd.read_parquet(test_dataset_path)
            df = CuratedContainer._restore_dtypes(df, path / "test_dtypes.json")
            return CuratedContainer._restore_categories(df, path / "test_categories.json")
        return None

    @staticmethod
    def _load_metadata(path: Path) -> dict:
        """The dataset, task and experiment metadata of a saved container; other ``a.b.json`` files are skipped."""
        metadata_objs = {}
        for meta_file in sorted(path.glob("*.*.json")):
            meta_name, type_adapter_id = meta_file.name.rsplit(".", 2)[:2]
            if meta_name not in CuratedContainer._REQUIRED_METADATA:
                logger.warning("%s: not a metadata file of the container — skipping.", meta_file.name)
                continue
            if type_adapter_id not in MetadataRegistry:
                raise ValueError(
                    f"{meta_file.name}: unknown metadata type {type_adapter_id!r}; the container was probably written "
                    "by a newer data_foundry (a newer container format). Upgrade data_foundry to read it.",
                )
            adapter = TypeAdapter(MetadataRegistry[type_adapter_id])
            with meta_file.open("r") as f:
                meta_data = json.load(f)

            # backward compatibility for typo (FIXME: remove in the future)
            if "licence" in meta_data:
                meta_data["license"] = meta_data.pop("licence")

            # backward compatibility
            meta_data.pop("local_data_directory_base", None)

            # forward compatibility: a container saved by a newer version may carry fields this version lacks
            known = {f.name for f in dataclasses.fields(MetadataRegistry[type_adapter_id])}
            unknown = sorted(set(meta_data) - known)
            if unknown:
                logger.warning("%s: ignoring fields this version does not know: %s.", meta_file.name, unknown)
                meta_data = {k: v for k, v in meta_data.items() if k in known}

            metadata_objs[meta_name] = adapter.validate_python(meta_data)

        return metadata_objs

    @staticmethod
    def load(path: Path | str, *, load_dataset: bool = True, load_test_data: bool = False) -> CuratedContainer:
        """Load a curated data collection from a path directory."""
        if isinstance(path, str):
            path = Path(path)

        # Load dataset
        if load_dataset:
            dataset_path = path / "dataset.parquet"
            dataset = pd.read_parquet(dataset_path)
            dataset = CuratedContainer._restore_dtypes(dataset, path / "dtypes.json")
            dataset = CuratedContainer._restore_categories(dataset, path / "categories.json")
        else:
            dataset = None
        test_dataset = CuratedContainer._load_test_dataset(path=path) if load_test_data else None

        metadata_objs = CuratedContainer._load_metadata(path)

        # Load container metadata
        container_metadata_path = path / "container_metadata.json"
        with container_metadata_path.open("r") as f:
            container_metadata = json.load(f)
        stated_format = container_metadata.pop("format_version", 1)
        known = {"uuid", "checksum", "version_comment", "test_dataset_checksum"}
        unknown = sorted(set(container_metadata) - known)
        if unknown:
            logger.warning("%s: ignoring fields this version does not know: %s.", container_metadata_path.name, unknown)
            container_metadata = {k: v for k, v in container_metadata.items() if k in known}
        missing = [m for m in CuratedContainer._REQUIRED_METADATA if m not in metadata_objs]
        if missing:
            raise ValueError(f"{path}: no metadata file for {missing}.")
        actual_format = FORMAT_VERSIONS[metadata_objs["task_metadata"].type_adapter_id]
        if stated_format != actual_format:
            raise ValueError(
                f"{container_metadata_path} states format {stated_format}, but its task metadata is format "
                f"{actual_format} ({metadata_objs['task_metadata'].type_adapter_id}).",
            )

        return CuratedContainer(
            dataset=dataset,
            test_dataset=test_dataset,
            dataset_metadata=metadata_objs["dataset_metadata"],
            task_metadata=metadata_objs["task_metadata"],
            experiment_metadata=metadata_objs["experiment_metadata"],
            loaded_from_path=path,
            **container_metadata,
        )

    # --- Extra (non-core) artifacts ---------------------------------------------------
    def _resolve_extras_dir(self, path: Path | str | None) -> Path:
        """Return the directory to look for extra artifacts in.

        Falls back to ``loaded_from_path`` if ``path`` is omitted.
        """
        if path is not None:
            return Path(path)
        if self.loaded_from_path is not None:
            return self.loaded_from_path
        raise ValueError(
            "Container has no `loaded_from_path` — pass `path=...` to locate extra files.",
        )

    def extra_file_path(self, filename: str, *, path: Path | str | None = None) -> Path:
        """Resolve the path of an extra artifact alongside the container.

        Extra artifacts are any files a producer ships in the container directory beyond
        the six core files (``dataset.parquet``, ``dtypes.json``, ``container_metadata.json``
        and the three ``*.{type_id}.json`` metadata files) and the optional test-dataset pair.
        Data Foundry does not interpret their contents — it only resolves the path so callers
        can load them however they need (e.g. ``pd.read_parquet``, ``json.load``, ``np.load``).

        The returned path is not guaranteed to exist — use :meth:`has_extra_file` first.
        ``filename`` must be a bare file name (no directory separators).
        """
        if not filename or "/" in filename or "\\" in filename or filename in {".", ".."}:
            raise ValueError(f"Extra filename must be a bare file name, got {filename!r}.")
        if filename in self._RESERVED_EXTRA_FILENAMES:
            raise ValueError(
                f"{filename!r} is a core container file; use the dedicated load API instead "
                "(e.g. `CuratedContainer.load(...)` or `load_test_dataset()`).",
            )
        return self._resolve_extras_dir(path) / filename

    def has_extra_file(self, filename: str, *, path: Path | str | None = None) -> bool:
        """Return whether an extra artifact named ``filename`` exists next to the container."""
        try:
            return self.extra_file_path(filename, path=path).is_file()
        except ValueError:
            return False

    def list_extra_files(self, *, path: Path | str | None = None) -> list[str]:
        """Return the sorted list of extra-artifact file names present next to the container.

        Excludes the core six files and the optional test-dataset pair. Metadata JSON files
        (``<name>.<type_id>.json`` — two dots before ``.json``) are also excluded.
        Returns ``[]`` if the directory does not exist or holds no extras.
        """
        try:
            base = self._resolve_extras_dir(path)
        except ValueError:
            return []
        if not base.is_dir():
            return []
        extras: list[str] = []
        for entry in sorted(base.iterdir()):
            if not entry.is_file():
                continue
            name = entry.name
            if name in self._RESERVED_EXTRA_FILENAMES:
                continue
            if name.endswith(".json") and name.count(".") >= 2:
                continue
            extras.append(name)
        return extras
