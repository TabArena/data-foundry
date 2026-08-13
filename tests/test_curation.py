from __future__ import annotations

import json
from functools import partial
from pathlib import Path

import pytest
from data_foundry.curation import exporter, notebooks
from data_foundry.curation.app import _records_payload
from data_foundry.curation.notebooks import resolve_notebook, sync_notebook_paths
from data_foundry.curation.record import (
    FIELDS,
    CurationRecord,
    load_vocabularies,
    save_vocabularies,
)
from data_foundry.curation.site import build_site
from data_foundry.curation.store import (
    load_all,
    load_record,
    markdown_to_record,
    record_to_dict,
    record_to_markdown,
    save_record,
)


def _record(unique_name: str, **fields: object) -> CurationRecord:
    """A minimal record; ``fields`` sets whatever the test actually cares about."""
    return CurationRecord(unique_name=unique_name, name=unique_name, **fields)


@pytest.fixture
def sample_record() -> CurationRecord:
    return CurationRecord(
        unique_name="musk",
        name="musk",
        checked_by=["Lennart", "Andrej"],
        data_foundry_status=["DF: Yes", "BeyondArena"],
        decision_markers=["Duplicate", "Data Quality Issue"],
        tags=["Tiny Data", "Non-IID (Grouped)"],
        required_split=["Grouped (NON-IID)", "?"],
        problem_type="Binary Classification",
        year="1994",
        domain="chemistry & material science",
        source_links=["https://archive.ics.uci.edu/dataset/75", "10.24432/C51608"],
        comments="Line one.\n\nLine two with a colon: and symbols #@!.",
        reference="@article{x, title={Y}}",
        source_row=5,
    )


def test_markdown_roundtrip(sample_record: CurationRecord) -> None:
    parsed = markdown_to_record(record_to_markdown(sample_record))
    assert parsed == sample_record


def test_empty_fields_omitted_from_front_matter(sample_record: CurationRecord) -> None:
    md = record_to_markdown(sample_record)
    # collections is empty -> should not appear; required, present -> should.
    assert "collections:" not in md
    assert "required_split:" in md
    assert md.startswith("---\n")


def test_save_and_load(tmp_path, sample_record: CurationRecord) -> None:
    path = save_record(sample_record, tmp_path)
    assert path.name == "musk.md"
    assert load_record(path) == sample_record
    assert [r.unique_name for r in load_all(tmp_path)] == ["musk"]


def test_build_site(tmp_path, sample_record: CurationRecord) -> None:
    records = tmp_path / "records"
    save_record(sample_record, records)
    out = build_site(tmp_path / "site", records)

    # Read-only flag is injected; the live API endpoints are not hit by the build.
    index = (out / "index.html").read_text(encoding="utf-8")
    assert "window.DF_STATIC = true" in index

    # The two frozen read endpoints become sibling JSON files.
    schema = json.loads((out / "schema.json").read_text(encoding="utf-8"))
    assert set(schema) == {"fields", "vocabularies"}
    assert schema["fields"], "schema should list fields"

    records_json = json.loads((out / "records.json").read_text(encoding="utf-8"))
    assert [r["unique_name"] for r in records_json] == ["musk"]

    # Auxiliary static pages (e.g. guidelines.html) are copied alongside the grid.
    assert (out / "guidelines.html").exists()


def test_missing_front_matter_raises() -> None:
    with pytest.raises(ValueError, match="front-matter"):
        markdown_to_record("# just a body\n\nno front matter here")


def test_unknown_vocab_values(sample_record: CurationRecord) -> None:
    vocab = {"problem_type": ["Regression"], "domain": ["chemistry & material science"]}
    unknown = sample_record.unknown_vocab_values(vocab)
    assert unknown["problem_type"] == ["Binary Classification"]
    assert "domain" not in unknown  # this value is allowed


def test_repo_vocabularies_load() -> None:
    vocab = load_vocabularies()
    assert "data_foundry_status" in vocab
    assert "DF: Yes" in vocab["data_foundry_status"]


def test_vocab_save_load_roundtrip(tmp_path) -> None:
    path = tmp_path / "vocabularies.yaml"
    data = {"problem_type": ["Yes", "No", "?"], "domain": ["finance"]}
    save_vocabularies(data, path)
    assert load_vocabularies(path) == data  # bare 'Yes'/'No'/'?' survive YAML round-trip


def test_exporter_dataframe(tmp_path, sample_record: CurationRecord) -> None:
    save_record(sample_record, tmp_path)
    df = exporter.to_dataframe(directory=tmp_path)
    assert df.shape[0] == 1
    assert df.loc[0, "Checked by"] == "Lennart | Andrej"
    assert df.loc[0, "unique_name"] == "musk"


def _notebooks(*paths: Path) -> None:
    """Create each ``<dir>/<name>.ipynb`` (empty JSON) for a synthetic datasets tree."""
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}", encoding="utf-8")


def test_resolve_notebook_prefers_the_shipped_tree_over_scratch_copies(tmp_path) -> None:
    datasets = tmp_path / "datasets"
    _notebooks(
        datasets / "beyond_iid" / "new_iid" / "musk" / "musk.ipynb",
        datasets / "_dev" / "feature_selection" / "musk" / "musk.ipynb",
        datasets / "_maintenance" / "_old_collections" / "v0" / "musk" / "musk.ipynb",
        datasets / "_dev" / "feature_selection" / "only_in_dev" / "only_in_dev.ipynb",
        # A variant beside the shipped notebook loses to the plain name while nothing marks it
        # as the run that shipped -- and is never a dataset of its own.
        datasets / "beyond_iid" / "new_iid" / "musk" / "musk_clf.ipynb",
    )
    resolve = partial(resolve_notebook, datasets_dir=datasets)

    assert resolve(_record("musk")) == "datasets/beyond_iid/new_iid/musk/musk.ipynb"
    # A dataset that only ever lived in a scratch tree points at the copy that exists.
    assert resolve(_record("only_in_dev")) == "datasets/_dev/feature_selection/only_in_dev/only_in_dev.ipynb"
    assert resolve(_record("musk_clf")) is None


def test_resolve_notebook_keeps_a_shipped_dataset_out_of_dev(tmp_path) -> None:
    """``datasets/_dev/`` holds work in progress, so it never backs a shipped dataset."""
    # One tree per case: notebook_candidates() caches per datasets dir (the tree is static for
    # the lifetime of a serve/build), so a case must not mutate the tree another case resolved.
    dev_only = tmp_path / "dev-only" / "datasets"
    _notebooks(dev_only / "_dev" / "feature_selection" / "musk" / "musk.ipynb")
    shipped = _record("musk", data_foundry_status=["DF: Yes", "BeyondArena"])
    # Only a dev copy exists: better no pointer than one into the wrong tree (the integrity
    # tests then flag the shipped record as missing its notebook).
    assert resolve_notebook(shipped, dev_only) is None
    assert resolve_notebook(_record("musk"), dev_only) == "datasets/_dev/feature_selection/musk/musk.ipynb"

    both = tmp_path / "both" / "datasets"
    _notebooks(
        both / "_dev" / "feature_selection" / "musk" / "musk.ipynb",
        both / "beyond_iid" / "new_iid" / "musk" / "musk.ipynb",
    )
    assert resolve_notebook(shipped, both) == "datasets/beyond_iid/new_iid/musk/musk.ipynb"

    # TabArena v0.1 shipped from the archived tree, so that is where its notebook lives.
    archived = tmp_path / "archived" / "datasets"
    _notebooks(
        archived / "_dev" / "feature_selection" / "anneal" / "anneal.ipynb",
        archived / "_maintenance" / "_old_collections" / "tabarena-v0pt1" / "anneal" / "anneal.ipynb",
    )
    anneal = _record("anneal", data_foundry_status=["DF: Yes", "TabArena (v0.1)"])
    expected = "datasets/_maintenance/_old_collections/tabarena-v0pt1/anneal/anneal.ipynb"
    assert resolve_notebook(anneal, archived) == expected


def test_resolve_notebook_picks_the_variant_that_shipped(tmp_path, monkeypatch) -> None:
    uuid = "019d736f-26fd-73bd-8853-dc219e5f4ed5"
    dataset_dir = tmp_path / "datasets" / "beyond_iid" / "new_iid" / "musk"
    _notebooks(dataset_dir / "musk.ipynb")  # full-size run
    (dataset_dir / "musk_1m.ipynb").write_text(f'{{"out": "{uuid}"}}', encoding="utf-8")  # sub-sampled run
    monkeypatch.setattr(notebooks, "shipped_uuids", lambda: {"musk": uuid})

    resolved = resolve_notebook(_record("musk"), tmp_path / "datasets")
    assert resolved == "datasets/beyond_iid/new_iid/musk/musk_1m.ipynb"


def test_sync_notebook_paths_writes_the_pointer_into_the_record(tmp_path, sample_record: CurationRecord) -> None:
    records = tmp_path / "records"
    save_record(sample_record, records)
    dataset_dir = tmp_path / "datasets" / "beyond_iid" / "new_iid" / "musk"
    dataset_dir.mkdir(parents=True)
    (dataset_dir / "musk.ipynb").write_text("{}", encoding="utf-8")
    datasets = tmp_path / "datasets"

    changed = sync_notebook_paths(records, datasets, check=True)
    assert changed == {"musk": (None, "datasets/beyond_iid/new_iid/musk/musk.ipynb")}
    assert load_record(records / "musk.md").notebook_path is None, "--check must not write"

    assert sync_notebook_paths(records, datasets) == changed
    assert load_record(records / "musk.md").notebook_path == "datasets/beyond_iid/new_iid/musk/musk.ipynb"
    assert sync_notebook_paths(records, datasets, check=True) == {}, "second run is a no-op"


def test_records_payload_links_the_recorded_notebook(tmp_path, sample_record: CurationRecord) -> None:
    """The stored pointer is what gets linked -- no lookup in the datasets tree."""
    sample_record.notebook_path = "datasets/beyond_iid/new_iid/musk/musk_clf.ipynb"
    records = tmp_path / "records"
    save_record(sample_record, records)

    (row,) = _records_payload(records)
    assert row["notebook_path"] == "datasets/beyond_iid/new_iid/musk/musk_clf.ipynb"
    assert row["notebook_url"].endswith("/datasets/beyond_iid/new_iid/musk/musk_clf.ipynb")


def test_record_to_dict_has_all_fields(sample_record: CurationRecord) -> None:
    d = record_to_dict(sample_record)
    for f in FIELDS:
        assert f.name in d
    assert d["needs_review"] == []
