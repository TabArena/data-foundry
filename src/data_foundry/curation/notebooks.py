"""Resolve and record the one curation notebook behind each dataset.

A dataset maps to exactly one curation notebook, and that pointer is stored *in* its
record (``notebook_path``) rather than rediscovered on every read: a record then names its
notebook on its own, and the link survives the ``datasets/`` tree being reorganised.

This module is what puts the pointer there. :func:`notebook_index` discovers the mapping
from the tree — including which sibling run shipped, where a dataset has more than one —
and :func:`sync_notebook_paths` writes it into the records (or, with ``check=True``, only
reports the drift). The dashboard falls back to :func:`notebook_index` for a record that
carries no pointer yet, so a freshly curated dataset still links before it is synced.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from pathlib import Path

from data_foundry.collections import get_collection, list_collections
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.store import load_all, save_record


@lru_cache(maxsize=1)
def shipped_uuids() -> dict[str, str]:
    """Map a dataset ``unique_name`` -> the UUID of the curated container that shipped."""
    return {e.unique_name: e.uuid for c in list_collections() for e in get_collection(c).entries}


def _tree_rank(rel: Path) -> int:
    """How far a notebook sits from the shipped collection (lower is closer).

    The same ``<name>/<name>.ipynb`` often exists several times: once in the shipped
    collection (``datasets/beyond_iid/...``) and once more in a working or retired tree
    (``datasets/_dev/...``, ``datasets/_maintenance/...``). Underscore-prefixed directories
    mark those non-shipped trees, so counting them separates the two.
    """
    return sum(p.startswith("_") for p in rel.parts[:-1])


def _pick_notebook(repo_root: Path, unique_name: str, candidates: list[Path]) -> Path:
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
def notebook_index(datasets_dir: str) -> dict[str, str]:
    """Map a dataset ``unique_name`` -> its repo-relative curation-notebook path.

    A notebook counts when it sits in the dataset's own directory and is named after it:
    ``datasets/**/<name>/<name>.ipynb`` (the layout ``/process-dataset`` scaffolds) or a
    variant of it such as ``<name>_1m.ipynb`` / ``<name>_clf.ipynb``. Where a name has more
    than one, :func:`_pick_notebook` resolves which one shipped. Cached because the datasets
    tree is large and static for the lifetime of a serve/build.
    """
    base = Path(datasets_dir)
    if not base.exists():
        return {}
    repo_root = base.parent
    candidates: dict[str, list[Path]] = defaultdict(list)
    for nb in base.rglob("*.ipynb"):
        name = nb.parent.name
        if nb.stem == name or nb.stem.startswith(f"{name}_"):
            candidates[name].append(nb.relative_to(repo_root))
    return {name: _pick_notebook(repo_root, name, rels).as_posix() for name, rels in candidates.items()}


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
        from what the tree says — empty when the records are in sync. A record with no
        notebook in the tree is left alone: nothing was found to point at.
    """
    root = resolve_curation_root().parent
    index = notebook_index(str(Path(datasets_dir) if datasets_dir is not None else root / "datasets"))
    changed: dict[str, tuple[str | None, str]] = {}
    for record in load_all(directory):
        resolved = index.get(record.unique_name)
        if resolved is None or record.notebook_path == resolved:
            continue
        changed[record.unique_name] = (record.notebook_path, resolved)
        if not check:
            record.notebook_path = resolved
            save_record(record, directory if directory is not None else records_dir())
    return changed
