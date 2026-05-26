"""Sources that resolve a :class:`CollectionEntry` to a local directory of files.

A :class:`DataSource` is the place a collection's containers actually live —
e.g. a Hugging Face dataset repo, an S3 bucket, or a directory you already
have on disk. The collection asks the source to ``fetch`` an entry; the source
returns a local path that :meth:`CuratedContainer.load` can read.

Currently only :class:`HuggingFaceSource` is implemented, but the abstraction
is designed so additional sources (URL/S3/local) can slot in without touching
the rest of the package.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_foundry.collections._core import CollectionEntry

DATA_FOUNDRY_CACHE_ENV = "DATA_FOUNDRY_CACHE"
"""Environment variable users can set to override the default cache directory."""

DEFAULT_CACHE_DIR = Path.home() / ".cache" / "data_foundry"
"""Default cache directory (used when no env var or explicit ``cache_dir`` is given)."""


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
    if cache_dir is None:
        env_value = os.environ.get(DATA_FOUNDRY_CACHE_ENV)
        cache_dir = Path(env_value) if env_value else DEFAULT_CACHE_DIR
    cache_dir = Path(cache_dir).expanduser()
    if collection_name is not None:
        cache_dir = cache_dir / collection_name
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


class DataSource:
    """Base class for collection data sources.

    A source knows where a collection's containers physically live and how to
    materialize one of them on the local filesystem (downloading on first
    access, returning the cached copy on subsequent calls).

    Subclasses must implement :meth:`fetch`.
    """

    def fetch(self, entry: CollectionEntry, cache_dir: Path) -> Path:
        """Return a local directory holding the curated container files for ``entry``.

        Implementations are expected to be idempotent — repeated calls with the
        same ``entry`` and ``cache_dir`` should reuse cached files.
        """
        raise NotImplementedError


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

    def fetch(self, entry: CollectionEntry, cache_dir: Path) -> Path:
        """Download only the files for ``entry`` (if not already cached) and return its directory.

        Checks the local HF cache first and returns the existing path without
        importing :mod:`huggingface_hub` when the files are already present.
        The dependency is only required on a cache miss.
        """
        relative = entry.relative_path.as_posix()

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
        )
        return Path(snapshot_path) / relative

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
