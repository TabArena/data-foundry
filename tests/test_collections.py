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
    clear_cache,
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

    def fetch(self, entry: CollectionEntry, cache_dir: Path, *, force_download: bool = False) -> Path:
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


def test_dataset_collection_rejects_duplicate_unique_names():
    with pytest.raises(ValueError, match="Duplicate `unique_name` 'a'"):
        DatasetCollection.from_relative_paths(
            name="dup",
            description="x",
            relative_paths=["a/uuid-1", "a/versions/uuid-2"],
        )


def test_beyond_arena_has_unique_names():
    names = BEYOND_ARENA.unique_names
    assert len(set(names)) == len(names), "duplicate unique_names in BEYOND_ARENA"


# --- HuggingFaceSource caching ---
def _make_hf_snapshot(cache_dir: Path, repo_id: str, sha: str, relative: str, *, ref: str | None = None) -> Path:
    """Build a fake HF-style snapshot tree and return the container directory."""
    repo_folder = cache_dir / f"datasets--{repo_id.replace('/', '--')}"
    snapshot_dir = repo_folder / "snapshots" / sha / relative
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "container_metadata.json").write_text("{}")
    if ref is not None:
        refs_dir = repo_folder / "refs"
        refs_dir.mkdir(parents=True, exist_ok=True)
        (refs_dir / ref).write_text(sha)
    return snapshot_dir


def test_find_cached_returns_none_when_cache_empty(tmp_path):
    src = HuggingFaceSource(repo_id="org/repo")
    assert src._find_cached(tmp_path, "name/uuid") is None


def test_find_cached_picks_any_snapshot_when_no_revision(tmp_path):
    expected = _make_hf_snapshot(tmp_path, "org/repo", sha="abc123", relative="name/uuid")
    src = HuggingFaceSource(repo_id="org/repo")
    assert src._find_cached(tmp_path, "name/uuid") == expected


def test_find_cached_skips_snapshots_missing_the_entry(tmp_path):
    _make_hf_snapshot(tmp_path, "org/repo", sha="abc123", relative="other/uuid")
    expected = _make_hf_snapshot(tmp_path, "org/repo", sha="def456", relative="name/uuid")
    src = HuggingFaceSource(repo_id="org/repo")
    assert src._find_cached(tmp_path, "name/uuid") == expected


def test_find_cached_uses_pinned_commit_revision(tmp_path):
    _make_hf_snapshot(tmp_path, "org/repo", sha="stale1", relative="name/uuid")
    expected = _make_hf_snapshot(tmp_path, "org/repo", sha="pinned", relative="name/uuid")
    src = HuggingFaceSource(repo_id="org/repo", revision="pinned")
    assert src._find_cached(tmp_path, "name/uuid") == expected


def test_find_cached_resolves_revision_through_refs(tmp_path):
    expected = _make_hf_snapshot(
        tmp_path, "org/repo", sha="abc123", relative="name/uuid", ref="main",
    )
    src = HuggingFaceSource(repo_id="org/repo", revision="main")
    assert src._find_cached(tmp_path, "name/uuid") == expected


def test_find_cached_returns_none_when_pinned_revision_missing(tmp_path):
    # Snapshot exists but under a different sha; pinned revision does not resolve.
    _make_hf_snapshot(tmp_path, "org/repo", sha="abc123", relative="name/uuid")
    src = HuggingFaceSource(repo_id="org/repo", revision="not-cached")
    assert src._find_cached(tmp_path, "name/uuid") is None


def test_find_cached_repo_type_changes_folder_prefix(tmp_path):
    repo_folder = tmp_path / "models--org--repo"
    snapshot_dir = repo_folder / "snapshots" / "abc" / "name/uuid"
    snapshot_dir.mkdir(parents=True)
    src = HuggingFaceSource(repo_id="org/repo", repo_type="model")
    assert src._find_cached(tmp_path, "name/uuid") == snapshot_dir


def test_fetch_uses_cache_without_importing_huggingface_hub(tmp_path, monkeypatch):
    """When the container is already on disk, fetch must not require huggingface_hub."""
    expected = _make_hf_snapshot(tmp_path, "org/repo", sha="abc123", relative="name/uuid")

    # Block the import so any attempt to reach the HF code path would fail loudly.
    import builtins
    real_import = builtins.__import__

    def blocked_import(name, *args, **kwargs):
        if name == "huggingface_hub" or name.startswith("huggingface_hub."):
            raise AssertionError(f"huggingface_hub should not be imported on cache hit (got {name!r})")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)

    entry = CollectionEntry(unique_name="name", uuid="uuid")
    src = HuggingFaceSource(repo_id="org/repo")
    assert src.fetch(entry, tmp_path) == expected


def test_fetch_raises_import_error_on_cache_miss_without_hf(tmp_path, monkeypatch):
    """Cache miss must surface the ImportError, not a confusing inner failure."""
    import builtins
    real_import = builtins.__import__

    def blocked_import(name, *args, **kwargs):
        if name == "huggingface_hub" or name.startswith("huggingface_hub."):
            raise ImportError("simulated missing huggingface_hub")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    # Also drop any already-imported copy so the import statement re-runs.
    monkeypatch.delitem(__import__("sys").modules, "huggingface_hub", raising=False)

    entry = CollectionEntry(unique_name="name", uuid="uuid")
    src = HuggingFaceSource(repo_id="org/repo")
    with pytest.raises(ImportError, match="huggingface_hub"):
        src.fetch(entry, tmp_path)


def test_fetch_all_uses_cache_without_importing_huggingface_hub(tmp_path, monkeypatch):
    """Batch path must short-circuit when every entry is already cached."""
    expected_a = _make_hf_snapshot(tmp_path, "org/repo", sha="abc", relative="a/uuid-a")
    expected_b = _make_hf_snapshot(tmp_path, "org/repo", sha="abc", relative="b/versions/uuid-b")

    import builtins
    real_import = builtins.__import__

    def blocked_import(name, *args, **kwargs):
        if name == "huggingface_hub" or name.startswith("huggingface_hub."):
            raise AssertionError(f"huggingface_hub should not be imported when fully cached (got {name!r})")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)

    entries = [
        CollectionEntry(unique_name="a", uuid="uuid-a"),
        CollectionEntry(unique_name="b", uuid="uuid-b", is_versioned=True),
    ]
    src = HuggingFaceSource(repo_id="org/repo")
    assert src.fetch_all(entries, tmp_path) == [expected_a, expected_b]


def test_fetch_all_batches_into_single_snapshot_download(tmp_path, monkeypatch):
    """On any cache miss, fetch_all must issue exactly one HF call with all patterns."""
    # Only one of the two entries is cached — still a miss for the batch.
    _make_hf_snapshot(tmp_path, "org/repo", sha="abc", relative="a/uuid-a")

    import huggingface_hub

    snapshot_root = tmp_path / "downloaded"
    (snapshot_root / "a" / "uuid-a").mkdir(parents=True)
    (snapshot_root / "b" / "versions" / "uuid-b").mkdir(parents=True)
    calls: list[dict] = []

    def fake_snapshot_download(**kwargs):
        calls.append(kwargs)
        return str(snapshot_root)

    monkeypatch.setattr(huggingface_hub, "snapshot_download", fake_snapshot_download)

    entries = [
        CollectionEntry(unique_name="a", uuid="uuid-a"),
        CollectionEntry(unique_name="b", uuid="uuid-b", is_versioned=True),
    ]
    src = HuggingFaceSource(repo_id="org/repo")
    paths = src.fetch_all(entries, tmp_path)

    assert paths == [
        snapshot_root / "a" / "uuid-a",
        snapshot_root / "b" / "versions" / "uuid-b",
    ]
    assert len(calls) == 1, "fetch_all must batch into a single snapshot_download call"
    assert calls[0]["allow_patterns"] == ["a/uuid-a/*", "b/versions/uuid-b/*"]
    assert calls[0]["force_download"] is False


def test_fetch_all_force_download_bypasses_cache(tmp_path, monkeypatch):
    """`force_download=True` must skip the all-cached short-circuit."""
    _make_hf_snapshot(tmp_path, "org/repo", sha="abc", relative="a/uuid-a")

    import huggingface_hub

    snapshot_root = tmp_path / "fresh"
    (snapshot_root / "a" / "uuid-a").mkdir(parents=True)
    calls: list[dict] = []

    def fake_snapshot_download(**kwargs):
        calls.append(kwargs)
        return str(snapshot_root)

    monkeypatch.setattr(huggingface_hub, "snapshot_download", fake_snapshot_download)

    src = HuggingFaceSource(repo_id="org/repo")
    paths = src.fetch_all(
        [CollectionEntry(unique_name="a", uuid="uuid-a")],
        tmp_path,
        force_download=True,
    )
    assert paths == [snapshot_root / "a" / "uuid-a"]
    assert calls[0]["force_download"] is True


def test_fetch_force_download_skips_cache_and_passes_flag(tmp_path, monkeypatch):
    """`force_download=True` must bypass the local cache hit and forward the flag to HF."""
    _make_hf_snapshot(tmp_path, "org/repo", sha="abc123", relative="name/uuid")

    import huggingface_hub

    fresh_dir = tmp_path / "fresh" / "name" / "uuid"
    fresh_dir.mkdir(parents=True)
    calls: list[dict] = []

    def fake_snapshot_download(**kwargs):
        calls.append(kwargs)
        return str(tmp_path / "fresh")

    monkeypatch.setattr(huggingface_hub, "snapshot_download", fake_snapshot_download)

    entry = CollectionEntry(unique_name="name", uuid="uuid")
    src = HuggingFaceSource(repo_id="org/repo")
    result = src.fetch(entry, tmp_path, force_download=True)

    assert result == fresh_dir
    assert len(calls) == 1
    assert calls[0]["force_download"] is True


def test_prefetch_calls_source_for_each_entry(tmp_path):
    from data_foundry.examples import get_toy_container_path

    src = _RecordingSource(container_dir=get_toy_container_path())
    coll = DatasetCollection.from_relative_paths(
        name="prefetch-test",
        description="x",
        relative_paths=["a/uuid-a", "b/versions/uuid-b"],
        source=src,
    )

    paths = coll.prefetch(cache_dir=tmp_path)

    # Default `fetch_all` loops `fetch`, so each entry shows up in `calls`.
    assert paths == [src.container_dir, src.container_dir]
    assert [entry.unique_name for entry, _ in src.calls] == ["a", "b"]
    # All calls share the per-collection cache subdir.
    assert {cache for _, cache in src.calls} == {tmp_path / "prefetch-test"}


def test_prefetch_uses_source_fetch_all(tmp_path):
    """`prefetch` must delegate to `source.fetch_all` so batched sources are honored."""
    captured: dict[str, object] = {}

    class _BatchSource(DataSource):
        def fetch(self, entry, cache_dir, *, force_download=False):
            raise AssertionError("prefetch should call fetch_all, not fetch")

        def fetch_all(self, entries, cache_dir, *, force_download=False):
            captured["entries"] = list(entries)
            captured["cache_dir"] = cache_dir
            captured["force_download"] = force_download
            return [cache_dir / e.uuid for e in entries]

    coll = DatasetCollection.from_relative_paths(
        name="batch",
        description="x",
        relative_paths=["a/uuid-a", "b/uuid-b"],
        source=_BatchSource(),
    )
    paths = coll.prefetch(cache_dir=tmp_path, force_download=True)

    assert captured["force_download"] is True
    assert captured["cache_dir"] == tmp_path / "batch"
    assert [e.unique_name for e in captured["entries"]] == ["a", "b"]
    assert paths == [tmp_path / "batch" / "uuid-a", tmp_path / "batch" / "uuid-b"]


def test_prefetch_without_source_raises():
    coll = DatasetCollection.from_relative_paths(
        name="no-src", description="x", relative_paths=["a/uuid-a"],
    )
    with pytest.raises(RuntimeError, match="nothing to prefetch"):
        coll.prefetch()


def test_prefetch_forwards_force_download(tmp_path):
    received: list[bool] = []

    class _FlagCapturingSource(DataSource):
        def fetch(self, entry, cache_dir, *, force_download=False):
            received.append(force_download)
            return tmp_path / entry.uuid

    coll = DatasetCollection.from_relative_paths(
        name="ff-test",
        description="x",
        relative_paths=["a/uuid-a", "b/uuid-b"],
        source=_FlagCapturingSource(),
    )
    coll.prefetch(cache_dir=tmp_path, force_download=True)
    assert received == [True, True]


def test_get_dataset_forwards_force_download_to_source(tmp_path):
    from data_foundry.examples import get_toy_container_path

    received: list[bool] = []

    class _FlagCapturingSource(DataSource):
        def fetch(self, entry, cache_dir, *, force_download=False):
            received.append(force_download)
            return get_toy_container_path()

    coll = DatasetCollection.from_relative_paths(
        name="forward-test",
        description="x",
        relative_paths=["a/uuid-a"],
        source=_FlagCapturingSource(),
    )
    coll.get_dataset("a", cache_dir=tmp_path, force_download=True)
    assert received == [True]


def test_fetch_falls_back_to_download_on_cache_miss(tmp_path, monkeypatch):
    """When nothing is cached, fetch should call snapshot_download and return its path."""
    import huggingface_hub

    target = tmp_path / "downloaded" / "name" / "uuid"
    target.mkdir(parents=True)
    snapshot_root = tmp_path / "downloaded"
    calls: list[dict] = []

    def fake_snapshot_download(**kwargs):
        calls.append(kwargs)
        return str(snapshot_root)

    monkeypatch.setattr(huggingface_hub, "snapshot_download", fake_snapshot_download)

    entry = CollectionEntry(unique_name="name", uuid="uuid")
    src = HuggingFaceSource(repo_id="org/repo", revision="v1")
    result = src.fetch(entry, tmp_path)

    assert result == target
    assert len(calls) == 1
    assert calls[0]["repo_id"] == "org/repo"
    assert calls[0]["revision"] == "v1"
    assert calls[0]["allow_patterns"] == ["name/uuid/*"]
    assert calls[0]["force_download"] is False


# --- clear_cache helper ---
def test_clear_cache_removes_collection_subdir(tmp_path):
    target = tmp_path / "BeyondArena"
    target.mkdir()
    (target / "junk.bin").write_bytes(b"x")
    sibling = tmp_path / "OtherCollection"
    sibling.mkdir()
    (sibling / "keep.bin").write_bytes(b"y")

    removed = clear_cache(tmp_path, collection_name="BeyondArena")

    assert removed == target
    assert not target.exists()
    assert sibling.exists(), "sibling collection cache should be untouched"


def test_clear_cache_removes_entire_cache_root(tmp_path):
    (tmp_path / "BeyondArena").mkdir()
    (tmp_path / "OtherCollection").mkdir()

    removed = clear_cache(tmp_path)

    assert removed == tmp_path
    assert not tmp_path.exists()


def test_clear_cache_missing_path_is_noop(tmp_path):
    missing = tmp_path / "never-existed"
    # Should not raise; returns the resolved path.
    assert clear_cache(missing) == missing


def test_clear_cache_uses_env_when_no_explicit_dir(tmp_path, monkeypatch):
    monkeypatch.setenv(DATA_FOUNDRY_CACHE_ENV, str(tmp_path / "env-cache"))
    (tmp_path / "env-cache" / "C").mkdir(parents=True)

    removed = clear_cache(collection_name="C")
    assert removed == tmp_path / "env-cache" / "C"
    assert not removed.exists()


def test_dataset_collection_clear_cache_targets_own_subdir(tmp_path):
    coll = DatasetCollection.from_relative_paths(
        name="my-coll", description="x", relative_paths=["a/uuid-a"],
    )
    target = tmp_path / "my-coll"
    target.mkdir()
    (target / "junk").write_text("x")

    removed = coll.clear_cache(cache_dir=tmp_path)
    assert removed == target
    assert not target.exists()
