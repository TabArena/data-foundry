from __future__ import annotations

from pathlib import Path

import pytest
from data_foundry.collections import (
    BEYOND_ARENA,
    DATA_FOUNDRY_CACHE_ENV,
    DEFAULT_CACHE_DIR,
    CollectionEntry,
    DataSource,
    DatasetCollection,
    HuggingFaceSource,
    get_collection,
    list_collections,
    resolve_cache_dir,
)


# --- CollectionEntry parsing ---
def test_collection_entry_parses_simple_relative_path():
    entry = CollectionEntry.from_relative_path("foo/019d7366-4673-7d9a-9821-35604af616f6")
    assert entry.unique_name == "foo"
    assert entry.uuid == "019d7366-4673-7d9a-9821-35604af616f6"
    assert entry.is_versioned is False
    assert entry.relative_path == Path("foo/019d7366-4673-7d9a-9821-35604af616f6")


def test_collection_entry_parses_versioned_relative_path():
    entry = CollectionEntry.from_relative_path("foo/versions/019d7366-4673-7d9a-9821-35604af616f6")
    assert entry.unique_name == "foo"
    assert entry.uuid == "019d7366-4673-7d9a-9821-35604af616f6"
    assert entry.is_versioned is True
    assert entry.relative_path == Path("foo/versions/019d7366-4673-7d9a-9821-35604af616f6")


def test_collection_entry_rejects_bad_path():
    with pytest.raises(ValueError, match="Cannot parse"):
        CollectionEntry.from_relative_path("just-one-segment")
    with pytest.raises(ValueError, match="Cannot parse"):
        CollectionEntry.from_relative_path("foo/bar/baz/qux")


def test_collection_entry_local_path():
    entry = CollectionEntry(unique_name="foo", uuid="uuid-x", is_versioned=False)
    assert entry.local_path("/data") == Path("/data/foo/uuid-x")
    versioned = CollectionEntry(unique_name="foo", uuid="uuid-x", is_versioned=True)
    assert versioned.local_path("/data") == Path("/data/foo/versions/uuid-x")


# --- DatasetCollection convenience ---
def test_dataset_collection_basic_accessors():
    coll = DatasetCollection.from_relative_paths(
        name="tiny",
        description="x",
        relative_paths=["a/uuid-a", "b/versions/uuid-b"],
    )
    assert len(coll) == 2
    assert list(coll) == list(coll.entries)
    assert coll.unique_names == ["a", "b"]
    assert coll.uuids == ["uuid-a", "uuid-b"]
    assert coll.local_paths("/w") == [Path("/w/a/uuid-a"), Path("/w/b/versions/uuid-b")]


def test_find_entry_by_unique_name_and_uuid():
    coll = DatasetCollection.from_relative_paths(
        name="tiny", description="x", relative_paths=["a/uuid-a", "b/versions/uuid-b"],
    )
    assert coll.find_entry("a").uuid == "uuid-a"
    assert coll.find_entry("uuid-b").unique_name == "b"
    with pytest.raises(KeyError, match="No entry matching"):
        coll.find_entry("nope")


def test_get_dataset_without_source_raises():
    coll = DatasetCollection.from_relative_paths(
        name="tiny", description="x", relative_paths=["a/uuid-a"],
    )
    with pytest.raises(RuntimeError, match="has no `source`"):
        coll.get_dataset("a")


# --- Source dispatch + caching ---
class _RecordingSource(DataSource):
    def __init__(self, container_dir: Path):
        self.container_dir = container_dir
        self.calls: list[tuple[CollectionEntry, Path]] = []

    def fetch(self, entry: CollectionEntry, cache_dir: Path) -> Path:
        self.calls.append((entry, cache_dir))
        return self.container_dir


def test_get_dataset_routes_through_source(tmp_path):
    # Build a real on-disk container via the toy builder + reuse its path.
    from data_foundry.examples import get_toy_container_path
    src = _RecordingSource(container_dir=get_toy_container_path())
    coll = DatasetCollection.from_relative_paths(
        name="route-test",
        description="x",
        relative_paths=["a/uuid-a"],
        source=src,
    )

    container = coll.get_dataset("a", cache_dir=tmp_path)

    assert container.dataset is not None
    assert len(src.calls) == 1
    fetched_entry, used_cache = src.calls[0]
    assert fetched_entry.unique_name == "a"
    # Per-collection subdir was created under the override.
    assert used_cache == tmp_path / "route-test"
    assert used_cache.is_dir()


# --- resolve_cache_dir precedence ---
def test_resolve_cache_dir_explicit_wins(tmp_path, monkeypatch):
    monkeypatch.setenv(DATA_FOUNDRY_CACHE_ENV, str(tmp_path / "env-cache"))
    out = resolve_cache_dir(tmp_path / "explicit", collection_name="c")
    assert out == tmp_path / "explicit" / "c"
    assert out.is_dir()


def test_resolve_cache_dir_env_var(tmp_path, monkeypatch):
    monkeypatch.setenv(DATA_FOUNDRY_CACHE_ENV, str(tmp_path / "env-cache"))
    out = resolve_cache_dir(None, collection_name="c")
    assert out == tmp_path / "env-cache" / "c"


def test_resolve_cache_dir_default(monkeypatch):
    monkeypatch.delenv(DATA_FOUNDRY_CACHE_ENV, raising=False)
    out = resolve_cache_dir(None)
    assert out == DEFAULT_CACHE_DIR


# --- Registry contents ---
def test_only_beyond_arena_is_registered():
    assert list_collections() == ["BeyondArena"]


def test_get_collection_returns_beyond_arena():
    assert get_collection("BeyondArena") is BEYOND_ARENA


def test_get_collection_unknown_name():
    with pytest.raises(KeyError, match="Unknown collection"):
        get_collection("does-not-exist")


def test_beyond_arena_has_hf_source():
    assert isinstance(BEYOND_ARENA.source, HuggingFaceSource)
    assert BEYOND_ARENA.source.repo_id == "TabArena/BeyondArena"


def test_beyond_arena_has_unique_uuids():
    uuids = BEYOND_ARENA.uuids
    assert len(set(uuids)) == len(uuids), "duplicate UUIDs in BEYOND_ARENA"


def test_beyond_arena_has_versioned_entries():
    versioned = [e for e in BEYOND_ARENA if e.is_versioned]
    assert versioned, "expected at least one versioned entry in BEYOND_ARENA"
