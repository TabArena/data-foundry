"""Core abstractions for official curated dataset collections."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

from data_foundry.collections._sources import DataSource, resolve_cache_dir
from data_foundry.curation_container import CuratedContainer


@dataclass(frozen=True)
class CollectionEntry:
    """A pointer to a single curated container in the local data warehouse.

    Each entry uniquely identifies one curated container as
    ``<unique_name>/[versions/]<uuid>``, mirroring the on-disk layout written
    by :meth:`data_foundry.curation_container.CuratedContainer.save`.
    """

    unique_name: str
    """The dataset's ``unique_name`` (top-level warehouse directory)."""
    uuid: str
    """The container's UUID (final path segment)."""
    is_versioned: bool = False
    """True if the container was saved under a ``versions/`` subdirectory
    (i.e. the dataset has ``version_from_unique_name`` set in its metadata).
    """

    @classmethod
    def from_relative_path(cls, relative_path: str) -> CollectionEntry:
        """Parse a warehouse-relative path like ``name/uuid`` or ``name/versions/uuid``."""
        parts = relative_path.strip("/").split("/")
        if len(parts) == 2:
            return cls(unique_name=parts[0], uuid=parts[1], is_versioned=False)
        if len(parts) == 3 and parts[1] == "versions":
            return cls(unique_name=parts[0], uuid=parts[2], is_versioned=True)
        raise ValueError(
            f"Cannot parse collection entry from {relative_path!r}; "
            "expected '<unique_name>/<uuid>' or '<unique_name>/versions/<uuid>'.",
        )

    @property
    def relative_path(self) -> Path:
        """The container's path relative to the warehouse base directory."""
        if self.is_versioned:
            return Path(self.unique_name) / "versions" / self.uuid
        return Path(self.unique_name) / self.uuid

    def local_path(self, base_dir: Path | str) -> Path:
        """The container's absolute path, given the warehouse ``base_dir``."""
        return Path(base_dir) / self.relative_path

    def load(
        self,
        base_dir: Path | str,
        *,
        load_dataset: bool = True,
        load_test_data: bool = False,
    ) -> CuratedContainer:
        """Load the :class:`CuratedContainer` for this entry from ``base_dir``."""
        return CuratedContainer.load(
            self.local_path(base_dir),
            load_dataset=load_dataset,
            load_test_data=load_test_data,
        )


@dataclass(frozen=True)
class DatasetCollection:
    """A named, immutable list of curated containers that together form an
    "official" benchmarking collection (e.g. ``BeyondArena``).

    A collection is a stable set of ``(unique_name, uuid)`` pointers — the
    UUIDs are pinned in code so downstream users always get exactly the same
    containers when they resolve a collection against a local warehouse.
    """

    name: str
    """Stable identifier for this collection (used as the registry key)."""
    description: str
    """Short human-readable summary of what this collection contains."""
    entries: tuple[CollectionEntry, ...]
    """The container entries in this collection."""
    source: DataSource | None = None
    """Optional data source backing this collection (e.g. a Hugging Face repo).
    When set, :meth:`get_dataset` and :meth:`iter_containers` can fetch and
    cache containers automatically; otherwise callers must supply a local
    warehouse ``base_dir``.
    """

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self) -> Iterator[CollectionEntry]:
        return iter(self.entries)

    @property
    def unique_names(self) -> list[str]:
        """The dataset ``unique_name`` for each entry, in collection order."""
        return [e.unique_name for e in self.entries]

    @property
    def uuids(self) -> list[str]:
        """The container UUID for each entry, in collection order."""
        return [e.uuid for e in self.entries]

    @property
    def relative_paths(self) -> list[Path]:
        """Warehouse-relative paths for each entry, in collection order."""
        return [e.relative_path for e in self.entries]

    def local_paths(self, base_dir: Path | str) -> list[Path]:
        """Absolute on-disk paths for each entry, given the warehouse ``base_dir``."""
        return [e.local_path(base_dir) for e in self.entries]

    def iter_containers(
        self,
        base_dir: Path | str | None = None,
        *,
        cache_dir: Path | str | None = None,
        load_dataset: bool = True,
        load_test_data: bool = False,
    ) -> Iterator[CuratedContainer]:
        """Yield each :class:`CuratedContainer` in the collection.

        Pass ``base_dir`` to load from a pre-populated local warehouse, or
        leave it ``None`` to fetch via :attr:`source` (using ``cache_dir`` /
        ``$DATA_FOUNDRY_CACHE``).
        """
        for entry in self.entries:
            if base_dir is not None:
                yield entry.load(
                    base_dir,
                    load_dataset=load_dataset,
                    load_test_data=load_test_data,
                )
            else:
                yield self.get_dataset(
                    entry.uuid,
                    cache_dir=cache_dir,
                    load_dataset=load_dataset,
                    load_test_data=load_test_data,
                )

    def find_entry(self, name_or_uuid: str) -> CollectionEntry:
        """Look up an entry by its ``unique_name`` or ``uuid``."""
        for entry in self.entries:
            if name_or_uuid in (entry.unique_name, entry.uuid):
                return entry
        raise KeyError(
            f"No entry matching {name_or_uuid!r} in collection {self.name!r}.",
        )

    def get_dataset(
        self,
        name_or_uuid: str,
        *,
        cache_dir: Path | str | None = None,
        load_dataset: bool = True,
        load_test_data: bool = False,
    ) -> CuratedContainer:
        """Download (if needed) and load one container from this collection.

        Args:
            name_or_uuid: The dataset's ``unique_name`` or its container UUID.
            cache_dir: Override the cache root. Precedence is
                ``cache_dir`` > ``$DATA_FOUNDRY_CACHE`` > ``~/.cache/data_foundry``.
                A per-collection subdirectory (``<cache>/<collection.name>``)
                is created automatically.
            load_dataset: See :meth:`CuratedContainer.load`.
            load_test_data: See :meth:`CuratedContainer.load`.
        """
        if self.source is None:
            raise RuntimeError(
                f"Collection {self.name!r} has no `source` configured — pass "
                "a local `base_dir` to `entry.load(...)` instead.",
            )
        entry = self.find_entry(name_or_uuid)
        cache_root = resolve_cache_dir(cache_dir, collection_name=self.name)
        container_path = self.source.fetch(entry, cache_root)
        return CuratedContainer.load(
            container_path,
            load_dataset=load_dataset,
            load_test_data=load_test_data,
        )

    @classmethod
    def from_relative_paths(
        cls,
        name: str,
        description: str,
        relative_paths: Sequence[str],
        *,
        source: DataSource | None = None,
    ) -> DatasetCollection:
        """Build a collection from an iterable of ``<unique_name>/[versions/]<uuid>`` strings."""
        return cls(
            name=name,
            description=description,
            entries=tuple(CollectionEntry.from_relative_path(p) for p in relative_paths),
            source=source,
        )
