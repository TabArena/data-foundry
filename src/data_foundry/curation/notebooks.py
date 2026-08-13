"""Resolve and record the one curation notebook behind each dataset.

A dataset maps to exactly one curation notebook, and that pointer is stored *in* its
record (``notebook_path``) rather than rediscovered on every read: a record then names its
notebook on its own, and the link survives the ``datasets/`` tree being reorganised.

This module is what puts the pointer there. :func:`resolve_notebook` works out which notebook
a record should point at — which tree it must come from, and which sibling run shipped where a
dataset has more than one — and :func:`sync_notebook_paths` writes that into the records (or,
with ``check=True``, only reports the drift). The dashboard falls back to
:func:`resolve_notebook` for a record that carries no pointer yet, so a freshly curated dataset
still links before it is synced.

**Where a shipped dataset's notebook may live.** A dataset we ship comes from its collection's
tree — ``datasets/beyond_iid/`` for BeyondArena, ``datasets/_maintenance/_old_collections/``
for TabArena v0.1 — never from ``datasets/_dev/``, which holds work in progress and older
copies of notebooks that have since shipped elsewhere. Datasets we do *not* ship are the other
way round: their notebook legitimately lives under ``datasets/_dev/`` (still being worked on)
or ``datasets/_maintenance/`` (deprecated, suspended, out of scope), and pointing there is
correct.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

from data_foundry.collections import get_collection, list_collections
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.store import load_all, save_record

if TYPE_CHECKING:
    from collections.abc import Sequence

    from data_foundry.curation.record import CurationRecord

# The tree each shipped collection's notebooks live in, most specific first: a dataset in
# BeyondArena is curated under datasets/beyond_iid/ even if it also shipped in TabArena v0.1,
# whose own (older) notebooks were archived under _maintenance/_old_collections/.
COLLECTION_TREES: tuple[tuple[str, str], ...] = (
    ("BeyondArena", "datasets/beyond_iid/"),
    ("TabArena (v0.1)", "datasets/_maintenance/_old_collections/"),
)


@lru_cache(maxsize=1)
def shipped_uuids() -> dict[str, str]:
    """Map a dataset ``unique_name`` -> the UUID of the curated container that shipped."""
    return {e.unique_name: e.uuid for c in list_collections() for e in get_collection(c).entries}


def required_tree(record: CurationRecord) -> str | None:
    """The tree this record's notebook must live in, or ``None`` if it ships nowhere.

    See :data:`COLLECTION_TREES`. A record with no collection tag is unconstrained: its
    notebook may sit anywhere, including ``datasets/_dev/`` or ``datasets/_maintenance/``.
    """
    status = record.data_foundry_status or []
    return next((tree for label, tree in COLLECTION_TREES if label in status), None)


def _tree_rank(rel: Path) -> int:
    """How far a notebook sits from the shipped collection (lower is closer).

    The same ``<name>/<name>.ipynb`` often exists several times: once in the shipped
    collection (``datasets/beyond_iid/...``) and once more in a working or retired tree
    (``datasets/_dev/...``, ``datasets/_maintenance/...``). Underscore-prefixed directories
    mark those non-shipped trees, so counting them separates the two.
    """
    return sum(p.startswith("_") for p in rel.parts[:-1])


def _pick_notebook(repo_root: Path, unique_name: str, candidates: Sequence[Path]) -> Path:
    """Choose the notebook that produced this dataset's shipped container.

    A dataset directory can hold more than one notebook: a sub-sampled ``<name>_1m.ipynb``
    next to the full-size run, or an alternative target such as ``<name>_clf.ipynb``. The
    notebook that shipped is the one whose saved output carries the UUID the collection
    registry points at, so that decides it — falling back to the plain ``<name>.ipynb`` for
    datasets that never shipped. Ties break on the path so the result does not depend on
    filesystem walk order.
    """
    best_tree = min(_tree_rank(c) for c in candidates)
    shortlist = sorted(c for c in candidates if _tree_rank(c) == best_tree)
    if len(shortlist) == 1:  # the common case: no notebook to read
        return shortlist[0]
    uuid = shipped_uuids().get(unique_name)
    return min(
        shortlist,
        key=lambda c: (
            not (uuid and uuid in (repo_root / c).read_text(encoding="utf-8")),
            c.stem != unique_name,
            c.as_posix(),
        ),
    )


@lru_cache(maxsize=8)
def notebook_candidates(datasets_dir: str) -> dict[str, tuple[Path, ...]]:
    """Map a dataset ``unique_name`` -> every repo-relative notebook that could be its own.

    A notebook counts when it sits in the dataset's own directory and is named after it:
    ``datasets/**/<name>/<name>.ipynb`` (the layout ``/process-dataset`` scaffolds) or a
    variant of it such as ``<name>_1m.ipynb`` / ``<name>_clf.ipynb``. Cached because the
    datasets tree is large and static for the lifetime of a serve/build.
    """
    base = Path(datasets_dir)
    if not base.exists():
        return {}
    repo_root = base.parent
    found: dict[str, list[Path]] = defaultdict(list)
    for nb in base.rglob("*.ipynb"):
        name = nb.parent.name
        if nb.stem == name or nb.stem.startswith(f"{name}_"):
            found[name].append(nb.relative_to(repo_root))
    return {name: tuple(sorted(paths)) for name, paths in found.items()}


def resolve_notebook(record: CurationRecord, datasets_dir: str | Path | None = None) -> str | None:
    """Repo-relative path of the notebook ``record`` should point at, or ``None`` if there is none.

    A dataset shipped in a collection is resolved *within that collection's tree*
    (:func:`required_tree`), so a stale copy under ``datasets/_dev/`` can never win — and a
    shipped dataset with no notebook in its own tree resolves to ``None`` rather than to the
    wrong file, which the record-integrity tests then flag. Unshipped datasets are resolved
    across the whole tree, where ``_dev`` / ``_maintenance`` is the right answer.
    """
    root = resolve_curation_root().parent
    base = Path(datasets_dir) if datasets_dir is not None else root / "datasets"
    candidates = notebook_candidates(str(base)).get(record.unique_name, ())
    tree = required_tree(record)
    if tree:
        candidates = tuple(c for c in candidates if c.as_posix().startswith(tree))
    if not candidates:
        return None
    return _pick_notebook(base.parent, record.unique_name, candidates).as_posix()


def sync_notebook_paths(
    directory: str | Path | None = None,
    datasets_dir: str | Path | None = None,
    *,
    check: bool = False,
) -> dict[str, tuple[str | None, str]]:
    """Fill each record's ``notebook_path`` from the datasets tree.

    Args:
        directory: Records directory (defaults to the standard one).
        datasets_dir: Datasets tree to resolve against (defaults to ``<repo>/datasets``).
        check: Report what would change without writing anything.

    Returns:
        ``unique_name -> (stored, resolved)`` for every record whose stored pointer differs
        from what the tree says — empty when the records are in sync. A record that resolves to
        nothing is left alone: there is no notebook to point at (an unprocessed candidate), or
        the only ones are outside the collection tree the dataset ships from, which is a
        curation problem to fix in the tree rather than to record here.
    """
    changed: dict[str, tuple[str | None, str]] = {}
    for record in load_all(directory):
        resolved = resolve_notebook(record, datasets_dir)
        if resolved is None or record.notebook_path == resolved:
            continue
        changed[record.unique_name] = (record.notebook_path, resolved)
        if not check:
            record.notebook_path = resolved
            save_record(record, directory if directory is not None else records_dir())
    return changed
