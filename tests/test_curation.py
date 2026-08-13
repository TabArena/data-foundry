from __future__ import annotations

import json

import pytest
from data_foundry.curation import exporter
from data_foundry.curation._paths import resolve_curation_root
from data_foundry.curation.app import _notebook_index
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


def test_notebook_index_prefers_shipped_over_scratch_copies(tmp_path) -> None:
    datasets = tmp_path / "datasets"
    for parent in [
        datasets / "beyond_iid" / "new_iid" / "musk",
        datasets / "_dev" / "feature_selection" / "musk",
        datasets / "_maintenance" / "_old_collections" / "v0" / "musk",
        datasets / "_dev" / "feature_selection" / "only_in_dev",
    ]:
        parent.mkdir(parents=True)
        (parent / f"{parent.name}.ipynb").write_text("{}", encoding="utf-8")
    # Not canonical (<name>/<name>.ipynb): a sibling variant next to the shipped notebook.
    (datasets / "beyond_iid" / "new_iid" / "musk" / "musk_clf.ipynb").write_text("{}", encoding="utf-8")

    index = _notebook_index(str(datasets))
    assert index["musk"] == "datasets/beyond_iid/new_iid/musk/musk.ipynb"
    # A dataset that only ever lived in a scratch tree still links to the copy that exists.
    assert index["only_in_dev"] == "datasets/_dev/feature_selection/only_in_dev/only_in_dev.ipynb"
    assert "musk_clf" not in index


def test_repo_notebook_links_point_at_the_shipped_collection() -> None:
    index = _notebook_index(str(resolve_curation_root().parent / "datasets"))
    shipped = {p.name for p in (resolve_curation_root().parent / "datasets" / "beyond_iid").rglob("*/*.ipynb")}
    for name, rel in index.items():
        if f"{name}.ipynb" in shipped:
            assert rel.startswith("datasets/beyond_iid/"), f"{name} links outside the shipped collection: {rel}"


def test_record_to_dict_has_all_fields(sample_record: CurationRecord) -> None:
    d = record_to_dict(sample_record)
    for f in FIELDS:
        assert f.name in d
    assert d["needs_review"] == []
