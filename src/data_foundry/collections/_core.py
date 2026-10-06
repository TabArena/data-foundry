"""Core abstractions for official curated dataset collections."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from data_foundry.collections._sources import (
    DataSource,
    clear_cache as _clear_cache,
    resolve_cache_dir,
)
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
    name: str | None = None
    """The dataset's own ``unique_name`` when it differs from the folder :attr:`unique_name`: a version such as
    ``mercari_price_suggestion_1m`` lives under ``mercari_price_suggestion/versions/``."""

    @property
    def dataset_name(self) -> str:
        """The dataset's own ``unique_name`` (:attr:`name`, else the folder name)."""
        return self.name or self.unique_name

    @classmethod
    def from_relative_path(cls, relative_path: str, *, name: str | None = None) -> CollectionEntry:
        """Parse a warehouse-relative path like ``name/uuid`` or ``name/versions/uuid``.

        ``name`` is the dataset's own name for a version (see :attr:`name`).
        """
        parts = relative_path.strip("/").split("/")
        if len(parts) == 2:
            return cls(unique_name=parts[0], uuid=parts[1], is_versioned=False, name=name)
        if len(parts) == 3 and parts[1] == "versions":
            return cls(unique_name=parts[0], uuid=parts[2], is_versioned=True, name=name)
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

    def __post_init__(self) -> None:
        seen: dict[str, str] = {}
        for entry in self.entries:
            for label in dict.fromkeys((entry.unique_name, entry.dataset_name)):
                if label in seen:
                    raise ValueError(
                        f"Duplicate `unique_name` {label!r} in collection "
                        f"{self.name!r}: uuids {seen[label]!r} and "
                        f"{entry.uuid!r} both map to the same name.",
                    )
                seen[label] = entry.uuid

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self) -> Iterator[CollectionEntry]:
        return iter(self.entries)

    @property
    def unique_names(self) -> list[str]:
        """The warehouse folder name of each entry, in collection order (a version's folder is its base dataset's
        name; :attr:`dataset_names` has the versions' own names).
        """
        return [e.unique_name for e in self.entries]

    @property
    def dataset_names(self) -> list[str]:
        """Each entry's own dataset name (``<name>_1m`` for a version), in collection order."""
        return [e.dataset_name for e in self.entries]

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
        force_download: bool = False,
        verify: bool = False,
    ) -> Iterator[CuratedContainer]:
        """Yield each :class:`CuratedContainer` in the collection.

        Pass ``base_dir`` to load from a pre-populated local warehouse, or
        leave it ``None`` to fetch via :attr:`source` (using ``cache_dir`` /
        ``$DATA_FOUNDRY_CACHE``). ``force_download`` is only meaningful when
        loading via :attr:`source` — it bypasses the cache for every entry.
        ``verify`` checks each container against its checksum (see :meth:`get_dataset`).
        """
        for entry in self.entries:
            if base_dir is not None:
                container = entry.load(
                    base_dir,
                    load_dataset=load_dataset,
                    load_test_data=load_test_data,
                )
                yield _verified(container, entry) if verify else container
            else:
                yield self.get_dataset(
                    entry.uuid,
                    cache_dir=cache_dir,
                    load_dataset=load_dataset,
                    load_test_data=load_test_data,
                    force_download=force_download,
                    verify=verify,
                )

    def find_entry(self, name_or_uuid: str) -> CollectionEntry:
        """Look up an entry by its ``uuid``, its own dataset name (``<name>_1m`` for a version) or its folder name."""
        for entry in self.entries:
            if name_or_uuid in (entry.unique_name, entry.dataset_name, entry.uuid):
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
        force_download: bool = False,
        verify: bool = False,
    ) -> CuratedContainer:
        """Download (if needed) and load one container from this collection.

        Args:
            name_or_uuid: The dataset's ``unique_name`` (a version's own, such as ``cooking_time_1m``, or its
                folder name) or its container UUID.
            cache_dir: Override the cache root. Precedence is
                ``cache_dir`` > ``$DATA_FOUNDRY_CACHE`` > ``~/.cache/data_foundry``.
                A per-collection subdirectory (``<cache>/<collection.name>``)
                is created automatically.
            load_dataset: See :meth:`CuratedContainer.load`.
            load_test_data: See :meth:`CuratedContainer.load`.
            force_download: When ``True``, bypass any cached copy and re-fetch
                from :attr:`source`. Use this to invalidate stale data — e.g.
                after a known upstream revision change.
            verify: When ``True``, recompute the checksum (and the test set's, when loaded) and raise if the
                files do not match it. Needs ``load_dataset=True``.

        Raises:
            ValueError: ``verify`` and the container does not match its checksum.
        """
        if self.source is None:
            raise RuntimeError(
                f"Collection {self.name!r} has no `source` configured — pass "
                "a local `base_dir` to `entry.load(...)` instead.",
            )
        entry = self.find_entry(name_or_uuid)
        cache_root = resolve_cache_dir(cache_dir, collection_name=self.name)
        container_path = self.source.fetch(entry, cache_root, force_download=force_download)
        container = CuratedContainer.load(
            container_path,
            load_dataset=load_dataset,
            load_test_data=load_test_data,
        )
        return _verified(container, entry) if verify else container

    def prefetch(
        self,
        cache_dir: Path | str | None = None,
        *,
        force_download: bool = False,
    ) -> list[Path]:
        """Download every container in the collection without loading it.

        Walks :attr:`entries` and asks :attr:`source` to materialize each
        container on disk, returning the resolved paths in collection order.
        Use this to warm the cache up front — e.g. before an offline benchmark
        run — so later :meth:`iter_containers` calls hit the cache instead of
        reaching out to the source.

        Args:
            cache_dir: Override the cache root (same precedence as
                :meth:`get_dataset`).
            force_download: When ``True``, re-fetch every container even if
                cached.
        """
        if self.source is None:
            raise RuntimeError(
                f"Collection {self.name!r} has no `source` configured — nothing to prefetch.",
            )
        cache_root = resolve_cache_dir(cache_dir, collection_name=self.name)
        return self.source.fetch_all(
            self.entries,
            cache_root,
            force_download=force_download,
        )

    def clear_cache(self, cache_dir: Path | str | None = None) -> Path:
        """Delete this collection's cache subdirectory and return its path.

        Resolves the cache root the same way as :meth:`get_dataset`, so the
        same ``cache_dir`` / ``$DATA_FOUNDRY_CACHE`` precedence applies. A
        missing path is a no-op (still returned for logging).
        """
        return _clear_cache(cache_dir, collection_name=self.name)

    @classmethod
    def from_relative_paths(
        cls,
        name: str,
        description: str,
        relative_paths: Sequence[str],
        *,
        source: DataSource | None = None,
        names: Mapping[str, str] | None = None,
    ) -> DatasetCollection:
        """Build a collection from an iterable of ``<unique_name>/[versions/]<uuid>`` strings.

        ``names`` maps a version's UUID to its own dataset name (see :attr:`CollectionEntry.name`).
        """
        names = names or {}
        entries = []
        for p in relative_paths:
            entry = CollectionEntry.from_relative_path(p)
            entries.append(dataclasses.replace(entry, name=names.get(entry.uuid)))
        return cls(
            name=name,
            description=description,
            entries=tuple(entries),
            source=source,
        )


def _verified(container: CuratedContainer, entry: CollectionEntry) -> CuratedContainer:
    """``container`` when it matches its checksum, else a ValueError naming the entry."""
    if container.dataset is None:
        raise ValueError("verify=True needs load_dataset=True: the checksum covers the data.")
    if not container.verify():
        raise ValueError(
            f"{entry.relative_path.as_posix()}: the files do not match the container's checksum; "
            "fetch it again with force_download=True.",
        )
    return container
