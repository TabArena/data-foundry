"""Tests of the curation backlog: records, vocabularies, exports, the dashboard server and the static site."""

from __future__ import annotations

import http.client
import json
import os
import threading
from collections.abc import Iterator
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path

import pandas as pd
import pydantic
import pytest
from data_foundry.curation import exporter, notebooks
from data_foundry.curation._paths import DATA_FOUNDRY_CURATION_ENV
from data_foundry.curation.app import (
    GUIDELINE_SKILLS,
    START_DOC,
    START_REPO_PATH,
    START_SECTION,
    CurationHandler,
    _docs_payload,
    _records_payload,
    _schema_payload,
    _version_payload,
)
from data_foundry.curation.notebooks import resolve_notebook, sync_notebook_paths
from data_foundry.curation.record import (
    BETTER_DATA_TAG,
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
    record_from_dict,
    record_to_dict,
    record_to_markdown,
    save_record,
)


def _record(unique_name: str, **fields: object) -> CurationRecord:
    """A minimal record; ``fields`` sets whatever the test actually cares about."""
    return CurationRecord(unique_name=unique_name, name=unique_name, **fields)


@pytest.fixture
def sample_record() -> CurationRecord:
    """A record with every kind of field filled in."""
    return CurationRecord(
        unique_name="musk",
        name="musk",
        checked_by=["Lennart", "Andrej"],
        data_foundry_status=["DF: Yes", "BeyondArena"],
        suggestion="Yes",
        priority=4,
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
    """A record survives markdown serialisation unchanged."""
    parsed = markdown_to_record(record_to_markdown(sample_record))
    assert parsed == sample_record
    assert parsed.priority == 4


def test_dict_roundtrip(sample_record: CurationRecord) -> None:
    """``record_to_dict`` and ``record_from_dict`` (the dashboard's JSON path) keep every field, priority included."""
    data = record_to_dict(sample_record)
    assert data["priority"] == 4
    assert record_from_dict(data) == sample_record
    assert record_from_dict({**data, "priority": None}).priority is None


def test_priority_sits_after_the_suggestion() -> None:
    """``priority`` follows ``suggestion`` in the schema and in the front matter, written as a plain integer."""
    names = [f.name for f in FIELDS]
    assert names[names.index("suggestion") + 1] == "priority"
    assert next(f for f in FIELDS if f.name == "priority").kind == "number"

    text = record_to_markdown(_record("a", suggestion="Yes", priority=5, decision_markers=["TBD"]))
    assert text.index("suggestion:") < text.index("priority: 5\n") < text.index("decision_markers:")
    assert "priority:" not in record_to_markdown(_record("b", suggestion="No")), "an empty priority is omitted"


@pytest.mark.parametrize("value", [0, 6, -1, "high"])
def test_an_out_of_range_priority_fails_to_parse(value: object) -> None:
    """A priority is an integer from 1 to 5; anything else is not a record."""
    text = record_to_markdown(_record("a")).replace("name: a\n", f"name: a\npriority: {value}\n")
    assert f"priority: {value}" in text
    with pytest.raises(pydantic.ValidationError):
        markdown_to_record(text)
    with pytest.raises(pydantic.ValidationError):
        _record("a", priority=value)


def test_describe_shows_the_priority(sample_record: CurationRecord) -> None:
    """The one-record summary lists the priority under its label."""
    line = next(ln for ln in sample_record.describe().splitlines() if ln.strip().startswith("Priority:"))
    assert line.split()[-1] == "4"
    assert next(ln for ln in _record("a").describe().splitlines() if "Priority:" in ln).split()[-1] == "None"


def test_schema_payload_has_the_number_field() -> None:
    """The dashboard learns from the schema that ``priority`` is a number column, with its help text."""
    fields = {f["name"]: f for f in _schema_payload()["fields"]}
    assert fields["priority"]["kind"] == "number"
    assert fields["priority"]["label"] == "Priority"
    assert fields["priority"]["vocab"] is None
    assert "/screen-candidates" in fields["priority"]["help"]


def test_empty_fields_omitted_from_front_matter(sample_record: CurationRecord) -> None:
    """Empty fields stay out of the front matter; filled ones are written."""
    md = record_to_markdown(sample_record)
    # collections is empty -> should not appear; required, present -> should.
    assert "collections:" not in md
    assert "required_split:" in md
    assert md.startswith("---\n")


def test_save_and_load(tmp_path, sample_record: CurationRecord) -> None:
    """A saved record is one ``<unique_name>.md`` file that loads back equal."""
    path = save_record(sample_record, tmp_path)
    assert path.name == "musk.md"
    assert load_record(path) == sample_record
    assert [r.unique_name for r in load_all(tmp_path)] == ["musk"]


def test_build_site(tmp_path, sample_record: CurationRecord) -> None:
    """The static site has the grid, its frozen JSON, and the Guidelines page with its docs."""
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

    # The Guidelines page is the markdown viewer, also in read-only mode, with its frozen manifest; every
    # file the manifest lists is copied next to it (this reads the repo's own skills, whatever they hold).
    guidelines = (out / "guidelines.html").read_text(encoding="utf-8")
    assert "window.DF_STATIC = true" in guidelines
    assert "markdown-it@14.1.0" in guidelines
    manifest = json.loads((out / "docs" / "manifest.json").read_text(encoding="utf-8"))
    # The Start here page leads when the repo has a .claude/skills/README.md.
    assert [s["skill"] for s in manifest["sections"] if s["skill"] != START_SECTION] == list(GUIDELINE_SKILLS)
    for doc in manifest["docs"]:
        assert (out / "docs" / doc["skill"] / doc["path"]).is_file(), doc


def test_missing_front_matter_raises() -> None:
    """A markdown file without front matter is not a record."""
    with pytest.raises(ValueError, match="front-matter"):
        markdown_to_record("# just a body\n\nno front matter here")


def test_unknown_vocab_values(sample_record: CurationRecord) -> None:
    """Values outside the vocabulary are reported per field."""
    vocab = {"problem_type": ["Regression"], "domain": ["chemistry & material science"]}
    unknown = sample_record.unknown_vocab_values(vocab)
    assert unknown["problem_type"] == ["Binary Classification"]
    assert "domain" not in unknown  # this value is allowed


def test_a_wip_state_and_its_claim_go_together() -> None:
    """A WIP state without a claim, or a claim without a WIP state, puts the record in the Review queue."""
    vocab = {"claimed_by": ["Lennart"], "data_foundry_status": ["WIP (DF)"], "suggestion": ["Yes"]}
    claimed = _record("a", suggestion="Yes", data_foundry_status=["WIP (DF)"], claimed_by="Lennart")
    unclaimed = _record("b", suggestion="Yes", data_foundry_status=["WIP (DF)"])
    left_behind = _record("c", suggestion="Yes", claimed_by="Lennart")

    assert claimed.review_reasons(vocab) == []
    assert unclaimed.review_reasons(vocab) == ["wip_unclaimed"]
    assert left_behind.review_reasons(vocab) == ["claim_without_wip"]


def test_better_data_tag_puts_the_record_in_review() -> None:
    """A record flagged with a better dataset for its task waits in the Review queue until the tag is removed."""
    vocab = {"suggestion": ["Yes"], "tags": [BETTER_DATA_TAG]}
    assert _record("a", suggestion="Yes", tags=[BETTER_DATA_TAG]).review_reasons(vocab) == ["better_data_review"]
    assert _record("b", suggestion="Yes").review_reasons(vocab) == []


def test_claimed_by_sits_next_to_the_wip_state_in_the_front_matter() -> None:
    """The claim is written right after the Data Foundry state and survives a round trip."""
    record = _record("a", suggestion="Yes", data_foundry_status=["WIP (DF)"], claimed_by="Lennart")
    text = record_to_markdown(record)

    assert text.index("data_foundry_status:") < text.index("claimed_by: Lennart") < text.index("suggestion:")
    assert markdown_to_record(text).claimed_by == "Lennart"


def test_repo_vocabularies_load() -> None:
    """The repo's ``vocabularies.yaml`` loads and has the Data Foundry states."""
    vocab = load_vocabularies()
    assert "data_foundry_status" in vocab
    assert "DF: Yes" in vocab["data_foundry_status"]


def test_vocab_save_load_roundtrip(tmp_path) -> None:
    """Bare ``Yes`` / ``No`` / ``?`` values survive a YAML round trip as strings."""
    path = tmp_path / "vocabularies.yaml"
    data = {"problem_type": ["Yes", "No", "?"], "domain": ["finance"]}
    save_vocabularies(data, path)
    assert load_vocabularies(path) == data  # bare 'Yes'/'No'/'?' survive YAML round-trip


def test_exporter_dataframe(tmp_path, sample_record: CurationRecord) -> None:
    """The flat export joins list fields with `` | ``."""
    save_record(sample_record, tmp_path)
    df = exporter.to_dataframe(directory=tmp_path)
    assert df.shape[0] == 1
    assert df.loc[0, "Checked by"] == "Lennart | Andrej"
    assert df.loc[0, "unique_name"] == "musk"
    assert df.loc[0, "Priority"] == 4


def test_exporter_keeps_priority_an_integer_column(tmp_path, sample_record: CurationRecord) -> None:
    """Priority and Source Row stay nullable integers: empty where unset, and the Parquet export still writes."""
    records = tmp_path / "records"
    save_record(sample_record, records)
    save_record(_record("unscreened"), records)
    df = exporter.to_dataframe(directory=records)
    assert str(df["Priority"].dtype) == "Int64"
    assert str(df["Source Row"].dtype) == "Int64"
    priority = df.set_index("unique_name")["Priority"]
    assert priority["musk"] == 4
    assert pd.isna(priority["unscreened"])

    csv = exporter.export_csv(tmp_path / "out.csv", records).read_text(encoding="utf-8").splitlines()
    header = csv[0].split(",")
    assert csv[1].split(",")[header.index("Priority")] == "4"
    pytest.importorskip("pyarrow")
    back = pd.read_parquet(exporter.export_parquet(tmp_path / "out.parquet", records))
    assert back.set_index("unique_name").loc["musk", "Priority"] == 4


def _notebooks(*paths: Path) -> None:
    """Create each ``<dir>/<name>.ipynb`` (empty JSON) for a synthetic datasets tree."""
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}", encoding="utf-8")


def test_resolve_notebook_prefers_the_shipped_tree_over_scratch_copies(tmp_path) -> None:
    """The shipped tree wins over ``_dev`` and archived copies of the same notebook."""
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
    """Of several notebook variants, the one whose output carries the shipped UUID wins."""
    uuid = "019d736f-26fd-73bd-8853-dc219e5f4ed5"
    dataset_dir = tmp_path / "datasets" / "beyond_iid" / "new_iid" / "musk"
    _notebooks(dataset_dir / "musk.ipynb")  # full-size run
    (dataset_dir / "musk_1m.ipynb").write_text(f'{{"out": "{uuid}"}}', encoding="utf-8")  # sub-sampled run
    monkeypatch.setattr(notebooks, "shipped_uuids", lambda: {"musk": uuid})

    resolved = resolve_notebook(_record("musk"), tmp_path / "datasets")
    assert resolved == "datasets/beyond_iid/new_iid/musk/musk_1m.ipynb"


def test_sync_notebook_paths_writes_the_pointer_into_the_record(tmp_path, sample_record: CurationRecord) -> None:
    """``sync_notebook_paths`` reports with ``check`` and writes without it, once."""
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


def test_version_payload_moves_when_a_record_is_written(tmp_path, sample_record: CurationRecord) -> None:
    """The dashboard polls this token to refresh itself: any write or delete must move it."""
    records = tmp_path / "records"
    path = save_record(sample_record, records)
    (records / "_template.md").write_text("scaffolding, not a record", encoding="utf-8")
    first = _version_payload(records)
    assert first["records"] == 1, "files starting with '_' are not records"

    os.utime(path, ns=(path.stat().st_atime_ns, path.stat().st_mtime_ns + 1_000_000))  # a later write
    second = _version_payload(records)
    assert second["version"] != first["version"]

    path.unlink()
    third = _version_payload(records)
    assert third["records"] == 0
    assert third["version"] != second["version"], "a deletion moves the token even with nothing newer"


def test_record_to_dict_has_all_fields(sample_record: CurationRecord) -> None:
    """``record_to_dict`` carries every schema field."""
    d = record_to_dict(sample_record)
    for f in FIELDS:
        assert f.name in d
    assert d["needs_review"] == []


# -- the Guidelines page: the knowledge skills' markdown, served and frozen ------------------------------------

_SKILL_INDEX = """---
name: knowledge-curation
description: "Reference knowledge"
---

# Curation knowledge

Read [the second](references/b_second.md) before [the first](./references/a_first.md#leak-checks).
"""

_LEAK_CHECKS = """---
# a YAML comment, not a heading
title: x
---

# Leak checks `probe`

## A section
"""

_NO_HEADING = """```text
# inside a code fence, not a heading
```

Some text.
"""


@pytest.fixture
def guideline_repo(tmp_path, monkeypatch) -> Path:
    """A repo root with small guideline skills, made the curation root's parent via the environment.

    Beside the two rendered skills it holds files the server must never hand out: another skill, a
    non-markdown file, a hidden file, and the repo's ``pyproject.toml``.
    """
    curation = tmp_path / "curation"
    (curation / "records").mkdir(parents=True)
    monkeypatch.setenv(DATA_FOUNDRY_CURATION_ENV, str(curation))
    skills = tmp_path / ".claude" / "skills"
    files = {
        "knowledge-curation/SKILL.md": _SKILL_INDEX,
        "knowledge-curation/references/a_first.md": _LEAK_CHECKS,
        "knowledge-curation/references/b_second.md": _NO_HEADING,
        "knowledge-curation/references/c_unlisted.md": "# Unlisted\n",
        "knowledge-curation/references/notes.txt": "not markdown",
        "knowledge-curation/.hidden.md": "# Hidden\n",
        "knowledge-data-foundry/SKILL.md": "# Data Foundry knowledge\n",
        "screen-candidates/SKILL.md": "# Another skill\n",
    }
    for rel, text in files.items():
        (skills / rel).parent.mkdir(parents=True, exist_ok=True)
        (skills / rel).write_text(text, encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'secret'\n", encoding="utf-8")
    return tmp_path


@pytest.mark.usefixtures("guideline_repo")
def test_docs_manifest_lists_both_skills_in_index_order() -> None:
    """SKILL.md comes first as Overview, then the files in the order SKILL.md names them, then the rest."""
    payload = _docs_payload()
    assert payload["sections"] == [{"skill": s, "title": t} for s, t in GUIDELINE_SKILLS.items()]
    rows = [(d["skill"], d["path"], d["title"]) for d in payload["docs"]]
    assert rows == [
        ("knowledge-curation", "SKILL.md", "Overview"),
        ("knowledge-curation", "references/b_second.md", "b_second"),  # no heading outside the fence
        ("knowledge-curation", "references/a_first.md", "Leak checks probe"),  # front matter skipped
        ("knowledge-curation", "references/c_unlisted.md", "Unlisted"),
        ("knowledge-data-foundry", "SKILL.md", "Overview"),
    ]
    first = payload["docs"][0]
    assert first["repo_path"] == ".claude/skills/knowledge-curation/SKILL.md"
    assert first["heading"] == "Curation knowledge"
    assert payload["github_blob_base"].startswith("https://")


def test_docs_manifest_is_empty_without_the_skill_folders(tmp_path, monkeypatch) -> None:
    """A curation root whose parent has no ``.claude/skills`` (a non-editable install) lists no docs."""
    monkeypatch.setenv(DATA_FOUNDRY_CURATION_ENV, str(tmp_path / "curation"))
    assert _docs_payload()["docs"] == []
    out = build_site(tmp_path / "site", tmp_path / "curation" / "records")
    manifest = json.loads((out / "docs" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["docs"] == []


_START_README = """# Skills

Start with [the curation knowledge](knowledge-curation/SKILL.md), then [screening](screen-candidates/SKILL.md).
"""


def test_build_site_has_the_start_here_page_when_a_readme_is_given(guideline_repo: Path) -> None:
    """A given README becomes the first section and page, "Start here", copied to ``docs/start/README.md``."""
    readme = guideline_repo / "elsewhere" / "README.md"
    readme.parent.mkdir()
    readme.write_text(_START_README, encoding="utf-8")
    out = build_site(guideline_repo / "site", guideline_repo / "curation" / "records", start_readme=readme)

    manifest = json.loads((out / "docs" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["sections"][0] == {"skill": START_SECTION, "title": "Start here"}
    assert [s["skill"] for s in manifest["sections"][1:]] == list(GUIDELINE_SKILLS)
    first = manifest["docs"][0]
    assert first == {
        "skill": START_SECTION,
        "path": "README.md",
        "repo_path": START_REPO_PATH,
        "title": "Start here",
        "heading": "Skills",
    }
    assert f"{first['skill']}/{first['path']}" == START_DOC
    assert (out / "docs" / START_DOC).read_text(encoding="utf-8") == _START_README
    assert [d["skill"] for d in manifest["docs"]].count(START_SECTION) == 1

    # Without the README (none in the fixture's .claude/skills/) the page is left out.
    plain = build_site(guideline_repo / "plain", guideline_repo / "curation" / "records")
    assert not (plain / "docs" / START_SECTION).exists()
    assert START_SECTION not in [s["skill"] for s in _docs_payload()["sections"]]


def test_build_site_copies_the_guideline_docs(guideline_repo: Path) -> None:
    """The static build freezes the manifest and copies exactly the files it lists."""
    out = build_site(guideline_repo / "site", guideline_repo / "curation" / "records")
    docs = out / "docs"
    manifest = json.loads((docs / "manifest.json").read_text(encoding="utf-8"))
    assert manifest == _docs_payload()
    copied = sorted(p.relative_to(docs).as_posix() for p in docs.rglob("*") if p.is_file())
    assert copied == sorted(["manifest.json", *(f"{d['skill']}/{d['path']}" for d in manifest["docs"])])
    assert "# Leak checks `probe`" in (docs / "knowledge-curation/references/a_first.md").read_text(encoding="utf-8")


@pytest.fixture
def server(guideline_repo: Path) -> Iterator[int]:
    """The dashboard server on a free local port, over the fixture repo; yields the port."""
    handler = partial(CurationHandler, directory=guideline_repo / "curation" / "records")
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=httpd.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    thread.start()
    try:
        yield httpd.server_address[1]
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join()


def _put(port: int, path: str, payload: dict[str, object]) -> tuple[int, dict[str, object]]:
    """PUT ``payload`` as JSON to ``path``; return status and the decoded JSON answer."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request("PUT", path, body=json.dumps(payload), headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        return resp.status, json.loads(resp.read().decode("utf-8"))
    finally:
        conn.close()


def _get(port: int, path: str) -> tuple[int, str, str]:
    """GET ``path`` exactly as written (no client-side normalisation); return status, content type, body."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request("GET", path)
        resp = conn.getresponse()
        return resp.status, resp.getheader("Content-Type", ""), resp.read().decode("utf-8")
    finally:
        conn.close()


def test_server_serves_the_viewer_and_the_docs(server: int, guideline_repo: Path) -> None:
    """``/guidelines.html``, ``/api/docs`` and ``/docs/<skill>/<path>.md`` answer, and an edit shows at once."""
    status, ctype, body = _get(server, "/guidelines.html")
    assert (status, ctype) == (200, "text/html; charset=utf-8")
    assert "<df-docs-core>" in body

    status, ctype, body = _get(server, "/api/docs")
    assert status == 200
    assert ctype.startswith("application/json")
    assert json.loads(body) == _docs_payload()

    path = guideline_repo / ".claude/skills/knowledge-curation/references/a_first.md"
    status, ctype, body = _get(server, "/docs/knowledge-curation/references/a_first.md")
    assert (status, ctype, body) == (200, "text/markdown; charset=utf-8", _LEAK_CHECKS)

    path.write_text("# Leak checks, edited\n", encoding="utf-8")  # read on every request: no restart needed
    assert _get(server, "/docs/knowledge-curation/references/a_first.md?x=1")[2] == "# Leak checks, edited\n"
    assert _get(server, "/docs/knowledge-data-foundry/SKILL.md")[0] == 200


def test_server_serves_the_start_here_page_first(server: int, guideline_repo: Path) -> None:
    """Given ``.claude/skills/README.md``, ``/api/docs`` lists Start here first and ``/docs/start/`` serves it."""
    assert START_SECTION not in [s["skill"] for s in json.loads(_get(server, "/api/docs")[2])["sections"]]
    (guideline_repo / ".claude" / "skills" / "README.md").write_text(_START_README, encoding="utf-8")

    listing = json.loads(_get(server, "/api/docs")[2])
    assert listing["sections"][0] == {"skill": START_SECTION, "title": "Start here"}
    assert listing["docs"][0]["repo_path"] == START_REPO_PATH
    assert _get(server, f"/docs/{START_DOC}") == (200, "text/markdown; charset=utf-8", _START_README)
    assert _get(server, "/docs/start/SKILL.md")[0] == 404


def test_server_saves_a_priority(server: int, guideline_repo: Path, sample_record: CurationRecord) -> None:
    """A PUT of a priority rewrites the record; an out-of-range one is refused and leaves the file as it was."""
    path = save_record(sample_record, guideline_repo / "curation" / "records")
    status, body = _put(server, "/api/records/musk", {"priority": 5})
    assert (status, body["priority"]) == (200, 5)
    assert "priority: 5\n" in path.read_text(encoding="utf-8")

    before = path.read_text(encoding="utf-8")
    status, body = _put(server, "/api/records/musk", {"priority": 9})
    assert status == 500
    assert "priority" in body["error"]
    assert path.read_text(encoding="utf-8") == before

    assert _put(server, "/api/records/musk", {"priority": None})[0] == 200
    assert "priority:" not in path.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "path",
    [
        "/docs/../../pyproject.toml",
        "/docs/knowledge-curation/../../../pyproject.toml",
        "/docs/%2e%2e/%2e%2e/pyproject.toml",
        "/docs/knowledge-curation/%2e%2e%2f%2e%2e%2f%2e%2e%2fpyproject.toml",
        "/docs/knowledge-curation/..%2F..%2F..%2Fpyproject.toml",
        "/docs/%252e%252e/%252e%252e/pyproject.toml",
        "/docs/knowledge-curation/references/../SKILL.md",
        "/docs/%2Fetc%2Fpasswd",
        "/docs//knowledge-curation/SKILL.md",
        "/docs/knowledge-curation/references/notes.txt",
        "/docs/knowledge-curation/.hidden.md",
        "/docs/screen-candidates/SKILL.md",
        "/docs/knowledge-curation/references/missing.md",
        "/docs/",
    ],
)
def test_server_refuses_anything_but_a_guideline_doc(server: int, path: str) -> None:
    """Path traversal (plain or encoded), other skills, non-markdown and hidden files are all a 404."""
    status, _, body = _get(server, path)
    assert status == 404
    assert "secret" not in body
