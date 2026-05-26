from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from pydantic import TypeAdapter
from uuid6 import uuid7

logger = logging.getLogger(__name__)

from data_foundry.schema import (
    DEFAULT_LOCAL_DATA_DIR,
    DatasetMetadata,
    MultilineStr,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadata,
)
from data_foundry.utils.checksum import encode_dataset, encode_pydantic_metadata

MetadataRegistry = {
    DatasetMetadata.type_adapter_id: DatasetMetadata,
    PredictiveMLTaskMetadata.type_adapter_id: PredictiveMLTaskMetadata,
    PredictiveMLSplitsMetadata.type_adapter_id: PredictiveMLSplitsMetadata,
}
NoIndentMetadata = [
    PredictiveMLSplitsMetadata.type_adapter_id,
]


@dataclass
class CuratedContainer:
    """Schema for a collection of curated items, ready to be used by others."""

    dataset: pd.DataFrame
    """The curated dataset as a pandas DataFrame."""
    dataset_metadata: DatasetMetadata
    """Metadata about the dataset."""
    task_metadata: PredictiveMLTaskMetadata
    """Metadata about the task for the dataset."""
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
    """A checksum for the curated data collection to verify integrity."""

    # Cache meta-data
    loaded_from_path: Path | None = None
    """The path from which the curated container was loaded, if applicable. Used for caching purposes."""

    def __post_init__(self):
        """Post-initialization to set the UUID if not provided."""
        if self.uuid is None:
            self.uuid = self._create_uuid()
        if self.checksum is None:
            self.checksum = self._create_checksum()

    @property
    def unique_name(self) -> str:
        """Return a unique name for the container."""
        return f"{self.dataset_metadata.unique_name}/{self.uuid}"

    @property
    def container_metadata(self) -> dict[str, str | None]:
        """Return a dictionary of the container's metadata."""
        assert self.uuid is not None, "UUID must be set."
        assert self.checksum is not None, "Checksum must be set."

        return {
            "uuid": self.uuid,
            "checksum": self.checksum,
            "version_comment": self.version_comment,
        }

    @staticmethod
    def _create_uuid() -> str:
        """Create a new unique identifier for the curated data collection."""
        return str(uuid7())

    def _create_checksum(self) -> str:
        """Hex digest checksum across dataframe + all metadata, using pydantic dumping."""

        # Ensure container is fully loaded before calculating checksum
        if self.dataset is None:
            raise ValueError("Dataset must be loaded to calculate checksum.")

        print("Calculating checksum for curated container...")
        h = hashlib.blake2b(digest_size=32)
        h.update(b"\0")
        h.update(b"dataset\0")
        h.update(encode_dataset(self.dataset))
        h.update(b"dataset_metadata\0")
        h.update(encode_pydantic_metadata(self.dataset_metadata))
        h.update(b"task_metadata\0")
        h.update(encode_pydantic_metadata(self.task_metadata))
        h.update(b"experiment_metadata\0")
        h.update(encode_pydantic_metadata(self.experiment_metadata))
        return h.hexdigest()

    @staticmethod
    def _save_dtypes(df: pd.DataFrame, path: Path) -> None:
        """Save DataFrame column dtypes to a JSON file."""
        dtypes = {str(col): str(dtype) for col, dtype in df.dtypes.items()}
        with path.open("w") as f:
            json.dump(dtypes, f, indent=2)

    @staticmethod
    def _restore_dtypes(df: pd.DataFrame, path: Path) -> pd.DataFrame:
        """Restore DataFrame column dtypes from a JSON file.

        If the file does not exist, logs a warning and returns the DataFrame unchanged.
        If a column cast fails, logs a warning for that column and skips it.
        """
        if not path.exists():
            logger.warning("dtype file %s not found — skipping dtype restoration (backward compatibility).", path)
            return df

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
        return df

    def _save_path(self, save_dir: Path) -> Path:
        """Resolve the on-disk save directory for this container under ``save_dir``."""
        meta = self.dataset_metadata
        path_name = meta.version_from_unique_name or meta.unique_name
        base = save_dir / path_name
        if meta.version_from_unique_name is not None:
            base = base / "versions"
        return base / self.uuid

    def save(self, save_dir: Path | str = DEFAULT_LOCAL_DATA_DIR) -> Path:
        """Save the curated data collection under ``save_dir``.

        The container is written to
        ``<save_dir>/<unique_name>/<uuid>/`` (or
        ``<save_dir>/<version_from_unique_name>/versions/<uuid>/`` for
        versioned datasets).
        """
        save_dir = Path(save_dir)
        save_path = self._save_path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)
        warehouse_path = save_path.relative_to(save_dir)
        print(f"Saving curated container to {warehouse_path}")

        # Save dataset
        dataset_path = save_path / "dataset.parquet"
        self.dataset.to_parquet(dataset_path, index=False)
        self._save_dtypes(self.dataset, save_path / "dtypes.json")

        if self.test_dataset is not None:
            test_dataset_path = save_path / "test_dataset.parquet"
            self.test_dataset.to_parquet(test_dataset_path)
            self._save_dtypes(self.test_dataset, save_path / "test_dtypes.json")

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
                json.dump(adapter.dump_python(meta_obj, mode="json"), f, indent=indent)

        with (save_path / "container_metadata.json").open("w") as f:
            json.dump(self.container_metadata, f, indent=2)

        return save_path

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
            return CuratedContainer._restore_dtypes(df, path / "test_dtypes.json")
        return None

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
        else:
            dataset = None
        test_dataset = CuratedContainer._load_test_dataset(path=path) if load_test_data else None

        # Load metadata
        metadata_objs = {}
        for meta_file in path.glob("*.*.json"):
            meta_name, type_adapter_id = meta_file.name.rsplit(".", 2)[:2]
            adapter = TypeAdapter(MetadataRegistry[type_adapter_id])
            with meta_file.open("r") as f:
                meta_data = json.load(f)

            # backward compatibility for typo (FIXME: remove in the future)
            if "licence" in meta_data:
                meta_data["license"] = meta_data.pop("licence")

            # backward compatibility
            meta_data.pop("local_data_directory_base", None)

            metadata_objs[meta_name] = adapter.validate_python(meta_data)

        # Load container metadata
        container_metadata_path = path / "container_metadata.json"
        with container_metadata_path.open("r") as f:
            container_metadata = json.load(f)

        return CuratedContainer(
            dataset=dataset,
            test_dataset=test_dataset,
            dataset_metadata=metadata_objs["dataset_metadata"],
            task_metadata=metadata_objs["task_metadata"],
            experiment_metadata=metadata_objs["experiment_metadata"],
            loaded_from_path=path,
            **container_metadata,
        )
