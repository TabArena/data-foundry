"""The shipped BeyondArena containers against this checkout, without downloading them.

TabArena loads the 142 containers of the collection with whatever ``data_foundry`` it installs, so a change to the
loader or the task view can break shipped data that no test container resembles: a stricter loader refusing a field
they carry, or ``container.task()`` failing on a metric name only they use (five did, 2026-11-27).
``tests/data/beyondarena_tasks.json`` records what the code reads of each container (its task metadata, the fields
of each metadata file, its columns), and these tests run that through the current code.

* Regenerate the snapshot after the collection changes: ``python -m tests.test_shipped_collection`` with the
  collection in the local cache (``BEYOND_ARENA.prefetch()``); ``HF_HUB_OFFLINE=1`` keeps it from downloading.
* ``DATA_FOUNDRY_TEST_SHIPPED=1 pytest tests/test_shipped_collection.py`` also loads every cached container: verify,
  task view, a fold, the inputs and a score of a constant prediction (minutes, and only where the cache holds them).
"""

from __future__ import annotations

import dataclasses
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from data_foundry.collections import get_collection
from data_foundry.curation_container import CuratedContainer, MetadataRegistry
from data_foundry.metrics import METRICS
from data_foundry.task import FORMAT_1_METRICS, _format_1_spec

SNAPSHOT = Path(__file__).parent / "data" / "beyondarena_tasks.json"
COLLECTION = "BeyondArena"


def _snapshot() -> list[dict]:
    return json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else []  # the coverage test then fails


def _ids(entries: list[dict]) -> list[str]:
    return [e["unique_name"] for e in entries]


def test_the_snapshot_covers_the_collection() -> None:
    """Every container the collection ships is recorded, so a new one cannot slip past these tests."""
    shipped = sorted(get_collection(COLLECTION).unique_names)
    assert sorted(_ids(_snapshot())) == shipped, "regenerate tests/data/beyondarena_tasks.json (module docstring)"


@pytest.mark.parametrize("entry", _snapshot(), ids=_ids(_snapshot()))
def test_the_loader_accepts_every_shipped_metadata_field(entry: dict) -> None:
    """The loader refuses a task or split field it does not know (a newer container); every field a shipped
    container carries must be one it knows.
    """
    for meta_name, (type_adapter_id, keys) in entry["metadata_fields"].items():
        if meta_name == "dataset_metadata":
            continue  # unknown descriptive fields are dropped with a warning, never refused
        meta_class = MetadataRegistry.get(type_adapter_id)
        assert meta_class is not None, f"{meta_name}: unknown metadata type {type_adapter_id!r}"
        known = {f.name for f in dataclasses.fields(meta_class)}
        assert set(keys) <= known | {"licence", "local_data_directory_base"}, (meta_name, set(keys) - known)


@pytest.mark.parametrize("entry", _snapshot(), ids=_ids(_snapshot()))
def test_the_task_view_resolves_every_shipped_metric(entry: dict) -> None:
    """``container.task()`` turns a format-1 metric name into a registry spec whose input columns the container has
    (BeyondArena's own names: ``MAPE``, ``amex_metric``, an empty name; ``data_foundry.task.FORMAT_1_METRICS``).
    """
    task = entry["task"]
    if entry["format_version"] >= 2:
        pytest.skip("a format-2 container stores its metric spec")
    spec = _format_1_spec(SimpleNamespace(**task))
    assert spec.name in METRICS
    assert task["problem_type"] in METRICS[spec.name].problem_types
    missing = set(spec.inputs.values()) - set(entry["columns"])
    hint = (
        "" if entry["columns_complete"] else " (a wide container records only named columns: regenerate the snapshot)"
    )
    assert not missing, f"the metric reads {sorted(missing)}, which the container lacks{hint}"
    for column in ("target_column_name", "group_on", "time_on"):
        name = task.get(column)
        assert name is None or name in entry["columns"], (column, name)


def _cached_names() -> list[str]:
    if os.environ.get("DATA_FOUNDRY_TEST_SHIPPED") != "1":
        return []
    return _ids(_snapshot())


@pytest.mark.skipif(os.environ.get("DATA_FOUNDRY_TEST_SHIPPED") != "1", reason="set DATA_FOUNDRY_TEST_SHIPPED=1")
@pytest.mark.parametrize("name", _cached_names() or ["-"])
def test_every_cached_shipped_container_loads_and_scores(name: str) -> None:
    """Load a cached container as TabArena does, with its checksum verified, and use its task view end to end."""
    collection = get_collection(COLLECTION)
    try:
        container = collection.get_dataset(name, verify=True)
    except FileNotFoundError:
        pytest.skip(f"{name} is not in the local cache")
    task = container.task()
    fold = next(iter(task.folds()))
    train, test = fold.train_side[:500], fold.test[:500]
    assert len(task.X(train).columns) > 0
    y_train, y_test = task.y(train), task.y(test)
    if task.classes is not None:
        shares = y_train.value_counts(normalize=True).reindex(task.classes, fill_value=0).to_numpy()
        prediction = np.tile(shares, (len(test), 1))
        prediction = prediction[:, 1] if len(task.classes) == 2 else prediction
    else:
        prediction = np.full(len(test), float(np.mean(y_train)))
    score = task.score(y_test, prediction, test)
    assert np.isfinite(score) or task.metric.name in ("roc_auc", "average_precision")  # one class: undefined


FULL_COLUMNS = 300
"""Containers with more columns record only the columns the task names and every metric alias reads."""


def _columns(columns: list[str], task: dict) -> dict:
    """The container's columns for the snapshot: all of them up to :data:`FULL_COLUMNS`, else the named ones."""
    if len(columns) <= FULL_COLUMNS:
        return {"columns": columns, "columns_complete": True}
    named = {task.get(k) for k in ("target_column_name", "group_on", "time_on")}
    named |= {c for alias in FORMAT_1_METRICS.values() for c in alias.get("inputs", {}).values()}
    return {"columns": sorted(c for c in columns if c in named), "columns_complete": False, "n_columns": len(columns)}


def build_snapshot() -> list[dict]:
    """What the tests above read of every container of the collection, from the local cache (no download)."""
    from data_foundry.collections import resolve_cache_dir  # only when regenerating

    collection = get_collection(COLLECTION)
    cache_root = resolve_cache_dir(None, collection_name=collection.name)
    out = []
    for entry in collection:
        path = collection.source.fetch(entry, cache_root)
        metadata = {}
        for meta_file in sorted(path.glob("*.*.json")):
            meta_name, type_adapter_id = meta_file.name.rsplit(".", 2)[:2]
            if meta_name in CuratedContainer._REQUIRED_METADATA:
                metadata[meta_name] = (type_adapter_id, sorted(json.loads(meta_file.read_text())))
        task_file = next(path.glob("task_metadata.*.json"))
        task = json.loads(task_file.read_text())
        fields = {"objective_metric_name", "problem_type", "target_column_name", "group_on", "time_on"}
        out.append(
            {
                "unique_name": entry.unique_name,
                "relative_path": entry.relative_path.as_posix(),
                "format_version": 2 if "objective_metric" in task else 1,
                "task": {k: task.get(k) for k in sorted(fields)},
                "metadata_fields": metadata,
                **_columns(sorted(json.loads((path / "dtypes.json").read_text())), task),
            }
        )
    return sorted(out, key=lambda e: e["unique_name"])


if __name__ == "__main__":  # python -m tests.test_shipped_collection
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    SNAPSHOT.parent.mkdir(exist_ok=True)
    SNAPSHOT.write_text(json.dumps(build_snapshot(), indent=1) + "\n")
    print(f"wrote {SNAPSHOT} ({SNAPSHOT.stat().st_size / 1e3:.0f} KB)", file=sys.stderr)
