"""Sources that resolve a :class:`CollectionEntry` to a local directory of files.

A :class:`DataSource` is the place a collection's containers actually live —
e.g. a Hugging Face dataset repo, an S3 bucket, or a directory you already
have on disk. The collection asks the source to ``fetch`` an entry; the source
returns a local path that :meth:`CuratedContainer.load` can read.

Two sources ship with the package: :class:`HuggingFaceSource` (download from
a Hub dataset repo) and :class:`LocalWarehouseSource` (point at a directory
that already mirrors the warehouse layout). The abstraction is designed so
additional sources (URL/S3/etc.) can slot in without touching the rest of
the package.
"""

from __future__ import annotations

import os
import shutil
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_foundry.collections._core import CollectionEntry

DATA_FOUNDRY_CACHE_ENV = "DATA_FOUNDRY_CACHE"
"""Environment variable users can set to override the default cache directory."""

DEFAULT_CACHE_DIR = Path.home() / ".cache" / "data_foundry"
"""Default cache directory (used when no env var or explicit ``cache_dir`` is given)."""


def _resolve_base_cache_dir(cache_dir: Path | str | None) -> Path:
    """Resolve the cache root without creating it (no per-collection suffix)."""
    if cache_dir is None:
        env_value = os.environ.get(DATA_FOUNDRY_CACHE_ENV)
        cache_dir = Path(env_value) if env_value else DEFAULT_CACHE_DIR
    return Path(cache_dir).expanduser()


def resolve_cache_dir(
    cache_dir: Path | str | None,
    *,
    collection_name: str | None = None,
) -> Path:
    """Resolve the cache directory for a fetch.

    Precedence: explicit ``cache_dir`` argument > ``$DATA_FOUNDRY_CACHE``
    > :data:`DEFAULT_CACHE_DIR`. When ``collection_name`` is given, a
    per-collection subdirectory is appended so different collections don't
    share an HF snapshot cache.
    """
    cache_dir = _resolve_base_cache_dir(cache_dir)
    if collection_name is not None:
        cache_dir = cache_dir / collection_name
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def clear_cache(
    cache_dir: Path | str | None = None,
    *,
    collection_name: str | None = None,
) -> Path:
    """Delete the data_foundry cache directory.

    Resolves the cache root the same way as :func:`resolve_cache_dir`. When
    ``collection_name`` is given, only that collection's subdirectory is
    removed; otherwise the entire cache root is removed. Missing paths are a
    no-op (the path is still returned so callers can log it).
    """
    base = _resolve_base_cache_dir(cache_dir)
    target = base / collection_name if collection_name is not None else base
    if target.exists():
        shutil.rmtree(target)
    return target


class DataSource:
    """Base class for collection data sources.

    A source knows where a collection's containers physically live and how to
    materialize one of them on the local filesystem (downloading on first
    access, returning the cached copy on subsequent calls).

    Subclasses must implement :meth:`fetch`.
    """

    def fetch(
        self,
        entry: CollectionEntry,
        cache_dir: Path,
        *,
        force_download: bool = False,
    ) -> Path:
        """Return a local directory holding the curated container files for ``entry``.

        Implementations are expected to be idempotent — repeated calls with the
        same ``entry`` and ``cache_dir`` should reuse cached files. When
        ``force_download`` is ``True``, cached files must be bypassed and the
        source re-fetched from its origin.
        """
        raise NotImplementedError

    def fetch_all(
        self,
        entries: Sequence[CollectionEntry],
        cache_dir: Path,
        *,
        force_download: bool = False,
    ) -> list[Path]:
        """Materialize many entries and return their paths in input order.

        Default implementation loops :meth:`fetch`. Subclasses can override to
        batch the underlying transport (e.g. a single ``snapshot_download``
        call covering every entry) when their backend supports it.
        """
        return [self.fetch(e, cache_dir, force_download=force_download) for e in entries]


@dataclass(frozen=True)
class LocalWarehouseSource(DataSource):
    """Source backed by a pre-populated local warehouse directory.

    Use this when the curated containers already live on disk in the standard
    warehouse layout (``<base_dir>/<unique_name>/[versions/]<uuid>/``) and no
    download is required — e.g. a shared filesystem on a compute cluster, or a
    locally-curated set of containers that has not been published to the Hub.

    ``fetch`` is a no-op pointer lookup: it returns the entry's path under
    ``base_dir`` (and validates that the directory exists). ``cache_dir`` and
    ``force_download`` are ignored because nothing is cached or downloaded.
    """

    base_dir: Path
    """Root of the local warehouse — the directory that contains
    ``<unique_name>/`` subfolders."""

    def fetch(
        self,
        entry: CollectionEntry,
        cache_dir: Path,  # noqa: ARG002 — kept to match DataSource interface
        *,
        force_download: bool = False,  # noqa: ARG002 — same reason
    ) -> Path:
        """Return the on-disk path for ``entry`` under :attr:`base_dir`.

        Raises ``FileNotFoundError`` if the container directory is missing.
        ``cache_dir`` and ``force_download`` are ignored.
        """
        path = entry.local_path(self.base_dir)
        if not path.is_dir():
            raise FileNotFoundError(
                f"No curated container at {path}. Expected a directory "
                f"matching entry {entry.relative_path.as_posix()!r} under the "
                f"local warehouse {self.base_dir!s}.",
            )
        return path


@dataclass(frozen=True)
class HuggingFaceSource(DataSource):
    """Source backed by a Hugging Face Hub dataset repository.

    The repo is expected to mirror the on-disk warehouse layout, i.e. each
    container lives at ``<unique_name>/<uuid>/`` or
    ``<unique_name>/versions/<uuid>/`` from the repo root.

    Requires the optional :mod:`huggingface_hub` dependency.
    """

    repo_id: str
    """Hub repository ID, e.g. ``"TabArena/BeyondArena"``."""
    revision: str | None = None
    """Optional pinned revision (branch, tag, or commit) of the dataset repo."""
    repo_type: str = "dataset"
    """The HF repo type; almost always ``"dataset"``."""

    def fetch(
        self,
        entry: CollectionEntry,
        cache_dir: Path,
        *,
        force_download: bool = False,
    ) -> Path:
        """Download only the files for ``entry`` (if not already cached) and return its directory.

        Checks the local HF cache first and returns the existing path without
        importing :mod:`huggingface_hub` when the files are already present.
        The dependency is only required on a cache miss. Pass
        ``force_download=True`` to skip the cache and re-fetch from the Hub.
        """
        relative = entry.relative_path.as_posix()

        if not force_download:
            cached = self._find_cached(cache_dir, relative)
            if cached is not None:
                return cached

        try:
            from huggingface_hub import snapshot_download
        except ImportError as exc:
            raise ImportError(
                "HuggingFaceSource requires the `huggingface_hub` package. "
                "Install with: pip install huggingface_hub",
            ) from exc

        snapshot_path = snapshot_download(
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            revision=self.revision,
            cache_dir=str(cache_dir),
            allow_patterns=[f"{relative}/*"],
            force_download=force_download,
        )
        return Path(snapshot_path) / relative

    def fetch_all(
        self,
        entries: Sequence[CollectionEntry],
        cache_dir: Path,
        *,
        force_download: bool = False,
    ) -> list[Path]:
        """Batch-download every entry with a single ``snapshot_download`` call.

        Short-circuits without importing :mod:`huggingface_hub` when every
        entry is already cached and ``force_download`` is ``False``. On any
        miss, issues one HF call with ``allow_patterns`` covering each entry —
        much faster than per-entry calls because the Hub indices are fetched
        only once.
        """
        relatives = [e.relative_path.as_posix() for e in entries]

        if not force_download:
            cached = [self._find_cached(cache_dir, r) for r in relatives]
            if all(c is not None for c in cached):
                return [c for c in cached if c is not None]

        try:
            from huggingface_hub import snapshot_download
        except ImportError as exc:
            raise ImportError(
                "HuggingFaceSource requires the `huggingface_hub` package. "
                "Install with: pip install huggingface_hub",
            ) from exc

        snapshot_path = snapshot_download(
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            revision=self.revision,
            cache_dir=str(cache_dir),
            allow_patterns=[f"{r}/*" for r in relatives],
            force_download=force_download,
        )
        return [Path(snapshot_path) / r for r in relatives]

    def _find_cached(self, cache_dir: Path, relative: str) -> Path | None:
        """Return the cached container directory if present, else ``None``.

        Mirrors the on-disk layout used by ``huggingface_hub``:
        ``<cache_dir>/<repo_type>s--<org>--<name>/snapshots/<sha>/<relative>``,
        with branch/tag names resolved via the sibling ``refs/`` directory.
        """
        repo_folder = f"{self.repo_type}s--{self.repo_id.replace('/', '--')}"
        repo_root = Path(cache_dir) / repo_folder
        snapshots_dir = repo_root / "snapshots"
        if not snapshots_dir.is_dir():
            return None

        if self.revision is not None:
            direct = snapshots_dir / self.revision / relative
            if direct.is_dir():
                return direct
            ref_file = repo_root / "refs" / self.revision
            if ref_file.is_file():
                sha = ref_file.read_text().strip()
                candidate = snapshots_dir / sha / relative
                if candidate.is_dir():
                    return candidate
            return None

        for snapshot in snapshots_dir.iterdir():
            candidate = snapshot / relative
            if candidate.is_dir():
                return candidate
        return None
