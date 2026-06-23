from __future__ import annotations

import csv

import pytest
from data_foundry.curation import exporter
from data_foundry.curation.importer import (
    import_sheet,
    paren_aware_split,
    parse_name,
    split_links,
    to_snake,
)
from data_foundry.curation.record import (
    FIELDS,
    CurationRecord,
    load_vocabularies,
    save_vocabularies,
)
from data_foundry.curation.store import (
    load_all,
    load_record,
    markdown_to_record,
    record_to_dict,
    record_to_markdown,
    save_record,
)

SHEET_HEADER = [
    "Checked by",
    "Data Foundry",
    "Suggestion",
    "Decision Markers",
    "New Tag",
    "Name",
    "Source (and Link to download)",
    "Free Comments",
    "Original Source (Website)",
    "Source (Benchmark / Collection)",
    "Year",
    "Context Domain",
    "Reference",
    "Required split",
    "Problem Type",
    "Usable Task Type",
    "Given Task Type",
    "Data Domain",
    "Original Data State",
]


@pytest.fixture
def sample_record() -> CurationRecord:
    return CurationRecord(
        unique_name="musk",
        name="musk",
        checked_by=["Lennart", "Andrej"],
        data_foundry_status="Yes",
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
    assert "Yes" in vocab["data_foundry_status"]


def test_vocab_save_load_roundtrip(tmp_path) -> None:
    path = tmp_path / "vocabularies.yaml"
    data = {"problem_type": ["Yes", "No", "?"], "domain": ["finance"]}
    save_vocabularies(data, path)
    assert load_vocabularies(path) == data  # bare 'Yes'/'No'/'?' survive YAML round-trip


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Random (IID), Grouped (NON-IID)", ["Random (IID)", "Grouped (NON-IID)"]),
        ("Lennart, Andrej", ["Lennart", "Andrej"]),
        (
            "Wrong Domain / Source Modality, Time-series (Classification)",
            ["Wrong Domain / Source Modality", "Time-series (Classification)"],
        ),
        ("", []),
    ],
)
def test_paren_aware_split(value: str, expected: list[str]) -> None:
    assert paren_aware_split(value) == expected


def test_to_snake() -> None:
    assert to_snake("PhiUSIIL Phishing URL (Website)") == "phiusiil_phishing_url_website"
    assert to_snake("Real-Estate  Valuation!") == "real_estate_valuation"


def test_parse_name_extracts_snake_hint() -> None:
    display, hint = parse_name("PhiUSIIL Phishing URL (Website)\n(phiusiil_phishing)")
    assert hint == "phiusiil_phishing"
    assert display == "PhiUSIIL Phishing URL (Website)"


def test_split_links() -> None:
    assert split_links("https://a.com\n\n10.123/x\n") == ["https://a.com", "10.123/x"]


def _write_sheet(path, rows: list[dict]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SHEET_HEADER)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in SHEET_HEADER})


def test_import_sheet(tmp_path) -> None:
    sheet = tmp_path / "sheet.csv"
    out = tmp_path / "records"
    _write_sheet(
        sheet,
        [
            {
                "Name": "Foo Bar (foo_bar)",
                "Checked by": "Lennart",
                "Data Foundry": "Yes",
                "New Tag": "Tiny Data",
                "Required split": "Random (IID)",
                "Problem Type": "Regression",
                "Free Comments": "multi\nline\ncomment",
                "Source (and Link to download)": "https://x.com\n10.1/y",
            },
            {"Name": "Foo Bar", "Checked by": "Andrej"},  # collides with foo_bar
            {"Name": "", "Free Comments": "nameless but not empty"},  # no name -> row_N fallback
        ],
    )
    records, report = import_sheet(sheet, out, vocab={}, write=True)
    assert report.n_written == 3
    by_name = {r.unique_name: r for r in records}
    assert "foo_bar" in by_name
    assert "foo_bar_2" in by_name  # collision resolved
    assert any(name.startswith("row_") for name in by_name)  # nameless row fallback
    foo = by_name["foo_bar"]
    assert foo.checked_by == ["Lennart"]
    assert foo.data_foundry_status == "Yes"
    assert foo.problem_type == "Regression"
    assert foo.source_links == ["https://x.com", "10.1/y"]
    assert foo.comments == "multi\nline\ncomment"
    assert (out / "foo_bar.md").exists()
    # empty vocab => every set dropdown value flagged for review
    assert "problem_type" in foo.needs_review


def test_exporter_dataframe(tmp_path, sample_record: CurationRecord) -> None:
    save_record(sample_record, tmp_path)
    df = exporter.to_dataframe(directory=tmp_path)
    assert df.shape[0] == 1
    assert df.loc[0, "Checked by"] == "Lennart | Andrej"
    assert df.loc[0, "unique_name"] == "musk"


def test_record_to_dict_has_all_fields(sample_record: CurationRecord) -> None:
    d = record_to_dict(sample_record)
    for f in FIELDS:
        assert f.name in d
    assert d["needs_review"] == []
