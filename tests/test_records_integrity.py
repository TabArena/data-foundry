"""Data-integrity checks over the real curation records (``curation/records/*.md``).

These run against the committed records (not synthetic fixtures) to catch obvious
mistakes: malformed files, filename/``unique_name`` drift, duplicate names, typo'd
dropdown values, and collection-membership inconsistencies vs. the shipped
``datasets/`` tree (e.g. the TabArena / BeyondArena tag counts).
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.notebooks import required_tree, shipped_uuids, sync_notebook_paths
from data_foundry.curation.record import (
    ACCEPTED_SUGGESTIONS,
    AI_FILLED_TAG,
    AI_REVIEWER,
    COLLECTION_TAGS,
    RETIRED_SUGGESTION,
    load_vocabularies,
)
from data_foundry.curation.store import load_all, markdown_to_record

RECDIR = records_dir()
DATASETS = resolve_curation_root().parent / "datasets"
TAB_LABEL, BEY_LABEL, DF_YES = "TabArena (v0.1)", "BeyondArena", "DF: Yes"


def _record_files() -> list[Path]:
    """All record files (``*.md`` minus the ``_``-prefixed template/scaffolding)."""
    return [p for p in sorted(RECDIR.glob("*.md")) if not p.name.startswith("_")]


@pytest.fixture(scope="module")
def records():
    """Every curation record, loaded once for the module."""
    return load_all(RECDIR)


@pytest.fixture(scope="module")
def vocab():
    """The editable dropdown vocabularies."""
    return load_vocabularies()


def _shipped() -> dict[str, set[str]]:
    """Map each shipped dataset folder name -> the collection labels it ships in."""
    members: dict[str, set[str]] = {}

    def add(directory: Path, label: str) -> None:
        if not directory.exists():
            return
        for child in directory.iterdir():
            if child.name.startswith("_") or child.name == "__pycache__":
                continue
            if child.is_dir() or child.suffix == ".ipynb":
                members.setdefault(child.name.replace(".ipynb", ""), set()).add(label)

    add(DATASETS / "_maintenance" / "_old_collections" / "tabarena-v0pt1", TAB_LABEL)
    for sub in ("grouped", "new_iid", "old_iid", "temporal"):
        add(DATASETS / "beyond_iid" / sub, BEY_LABEL)
    return members


_HAS_DATASETS = (DATASETS / "beyond_iid").exists()
_needs_datasets = pytest.mark.skipif(not _HAS_DATASETS, reason="shipped datasets/ tree not available")


# --------------------------------------------------------------------- structure
def test_records_dir_is_populated():
    """Sanity: the records directory exists and has records."""
    assert _record_files(), f"no record files found under {RECDIR}"


def test_every_record_parses_and_filename_matches():
    """Every file parses, and its ``unique_name`` equals its filename stem."""
    drift = []
    for path in _record_files():
        record = markdown_to_record(path.read_text())  # raises on malformed front-matter
        if record.unique_name != path.stem:
            drift.append((path.name, record.unique_name))
    assert not drift, f"unique_name != filename stem: {drift}"


def test_unique_names_are_unique(records):
    """No two records share a ``unique_name``."""
    dups = [n for n, c in Counter(r.unique_name for r in records).items() if c > 1]
    assert not dups, f"duplicate unique_name(s): {dups}"


def test_every_record_has_a_name(records):
    """Every record has a non-empty ``name``."""
    missing = [r.unique_name for r in records if not (r.name or "").strip()]
    assert not missing, f"records missing a name: {missing}"


def test_type_adapter_id_is_current(records):
    """All records use the expected serialization id."""
    bad = [r.unique_name for r in records if r.type_adapter_id != "curation-record-v1"]
    assert not bad, f"unexpected type_adapter_id: {bad}"


# ------------------------------------------------------------------ vocab / review
def test_dropdown_values_in_vocabulary(records, vocab):
    """Every dropdown value is in vocabularies.yaml (catches typos / stray values)."""
    offenders = {r.unique_name: r.unknown_vocab_values(vocab) for r in records}
    offenders = {k: v for k, v in offenders.items() if v}
    assert not offenders, f"out-of-vocabulary dropdown values: {offenders}"


def test_needs_review_is_consistent(records, vocab):
    """Stored ``needs_review`` matches what the record content implies (not stale)."""
    stale = [r.unique_name for r in records if list(r.needs_review or []) != r.review_reasons(vocab)]
    assert not stale, f"stale needs_review (re-save to fix): {stale}"


# ------------------------------------------------------------- collection invariants
def test_benchmark_tag_implies_in_data_foundry(records):
    """A record tagged with a shipped collection must also carry ``DF: Yes``."""
    bad = [
        r.unique_name
        for r in records
        if any(b in (r.data_foundry_status or []) for b in (TAB_LABEL, BEY_LABEL))
        and DF_YES not in (r.data_foundry_status or [])
    ]
    assert not bad, f"collection tag without '{DF_YES}': {bad}"


def test_duplicate_records_follow_convention(records):
    """``*_duplicate`` records carry the Duplicate marker and are not suggested 'Yes'."""
    bad = []
    for r in records:
        if not r.unique_name.endswith("_duplicate"):
            continue
        if "Duplicate" not in (r.decision_markers or []):
            bad.append((r.unique_name, "missing Duplicate marker"))
        if r.suggestion == "Yes":
            bad.append((r.unique_name, "suggestion == 'Yes'"))
    assert not bad, f"_duplicate convention violations: {bad}"


def test_no_ship_conflict(records):
    """A dataset shipped in a collection must carry an accepted verdict — or be marked retired.

    Accepted = ``Yes`` or ``Yes (Disagreement)`` (the latter = shipped on purpose but with an
    open disagreement to re-evaluate). ``No`` / ``TBD`` / plain ``Disagreement`` on a shipped
    dataset is a contradiction — **unless** the suggestion is ``No (Retired)``, which records
    that the verdict changed *after* the dataset shipped (e.g. later found trivial or
    ethically problematic); those keep their collection tag but are legitimately non-accepted.
    """
    bad = [
        (r.unique_name, r.suggestion)
        for r in records
        if any(t in (r.data_foundry_status or []) for t in COLLECTION_TAGS)
        and r.suggestion
        and r.suggestion not in (*ACCEPTED_SUGGESTIONS, RETIRED_SUGGESTION)
    ]
    assert not bad, f"shipped in a collection but suggestion not accepted (and not retired): {bad}"


def test_collection_records_have_a_suggestion(records):
    """Every dataset we ship in a collection must carry a (non-empty) suggestion."""
    bad = [
        r.unique_name
        for r in records
        if any(t in (r.data_foundry_status or []) for t in COLLECTION_TAGS) and not r.suggestion
    ]
    assert not bad, f"shipped in a collection but no suggestion: {bad}"


def test_ai_reviewed_records_follow_convention(records):
    """Records triaged by the AI pass carry the full, honestly-labelled convention.

    ``AI (UNVERIFIED)`` in ``checked_by`` must coincide with: the ``AI-Filled (Verify)``
    tag, an actual suggestion (the AI leaves a verdict), the ``ai_unverified`` review
    reason (so they stay in the human review queue), and the UNVERIFIED disclaimer in
    the comments (so no one mistakes an AI draft for a human decision).
    """
    bad = []
    for r in records:
        if AI_REVIEWER not in (r.checked_by or []):
            continue
        if AI_FILLED_TAG not in (r.tags or []):
            bad.append((r.unique_name, f"missing {AI_FILLED_TAG!r} tag"))
        if not r.suggestion:
            bad.append((r.unique_name, "no suggestion"))
        if "ai_unverified" not in (r.needs_review or []):
            bad.append((r.unique_name, "missing 'ai_unverified' in needs_review"))
        if "AI-FILLED" not in (r.comments or ""):
            bad.append((r.unique_name, "comments missing the UNVERIFIED disclaimer"))
    assert not bad, f"AI-review convention violations: {bad}"


def test_tabarena_records_checked_by_lennart_and_andrej(records):
    """Every TabArena (v0.1) record records review by both Lennart and Andrej."""
    bad = [
        r.unique_name
        for r in records
        if TAB_LABEL in (r.data_foundry_status or []) and not {"Lennart", "Andrej"} <= set(r.checked_by or [])
    ]
    assert not bad, f"TabArena records missing Lennart/Andrej in checked_by: {bad}"


@_needs_datasets
def test_collection_tag_counts_match_shipped(records):
    """The TabArena / BeyondArena tag counts equal the shipped dataset counts."""
    shipped = _shipped()
    exp_tab = sum(1 for labels in shipped.values() if TAB_LABEL in labels)
    exp_bey = sum(1 for labels in shipped.values() if BEY_LABEL in labels)
    got_tab = sum(1 for r in records if TAB_LABEL in (r.data_foundry_status or []))
    got_bey = sum(1 for r in records if BEY_LABEL in (r.data_foundry_status or []))
    got_union = sum(1 for r in records if any(b in (r.data_foundry_status or []) for b in (TAB_LABEL, BEY_LABEL)))
    assert got_tab == exp_tab, f"TabArena tags={got_tab}, shipped={exp_tab}"
    assert got_bey == exp_bey, f"BeyondArena tags={got_bey}, shipped={exp_bey}"
    assert got_union == len(shipped), f"DF-collection union={got_union}, shipped folders={len(shipped)}"


@_needs_datasets
def test_collection_members_align_with_shipped_folders(records):
    """Each shipped folder has a same-named record carrying its label, and no record
    carries a benchmark tag without a matching shipped folder.
    """
    shipped = _shipped()
    by_name = {r.unique_name: r for r in records}
    problems = []
    for folder, labels in shipped.items():
        record = by_name.get(folder)
        if record is None:
            problems.append((folder, "no record with this unique_name"))
            continue
        for label in labels:
            if label not in (record.data_foundry_status or []):
                problems.append((folder, f"record missing {label!r}"))
    assert not problems, f"shipped datasets not reflected in records: {problems}"

    extra = [
        r.unique_name
        for r in records
        if any(b in (r.data_foundry_status or []) for b in (TAB_LABEL, BEY_LABEL)) and r.unique_name not in shipped
    ]
    assert not extra, f"records carry a benchmark tag but are not a shipped folder: {extra}"


# ------------------------------------------------------------------- notebook pointers
@_needs_datasets
def test_notebook_path_points_at_an_existing_notebook(records):
    """Every recorded ``notebook_path`` resolves to a notebook in the dataset's own directory."""
    repo_root = resolve_curation_root().parent
    problems = []
    for r in records:
        if not r.notebook_path:
            continue
        path = repo_root / r.notebook_path
        if not path.is_file():
            problems.append((r.unique_name, f"missing file: {r.notebook_path}"))
        elif path.suffix != ".ipynb":
            problems.append((r.unique_name, f"not a notebook: {r.notebook_path}"))
        elif path.parent.name != r.unique_name:
            problems.append((r.unique_name, f"notebook outside the dataset's directory: {r.notebook_path}"))
    assert not problems, f"broken notebook_path pointers (run sync-notebooks): {problems}"


@_needs_datasets
def test_shipped_notebook_paths_live_in_their_collection_tree(records):
    """A shipped dataset's notebook comes from its collection's tree, never from ``_dev``.

    ``datasets/_dev/`` is work in progress — including older copies of notebooks that have since
    shipped from ``datasets/beyond_iid/`` — so a shipped dataset pointing there sends readers to
    preprocessing that produced no released data. Unshipped candidates are the other way round:
    ``_dev`` (in progress) and ``_maintenance`` (deprecated / suspended / out of scope) are
    exactly where their notebooks belong.
    """
    problems = [
        (r.unique_name, r.notebook_path, tree)
        for r in records
        if r.notebook_path and (tree := required_tree(r)) and not r.notebook_path.startswith(tree)
    ]
    assert not problems, f"shipped dataset curated outside its collection tree (name, path, expected): {problems}"


@_needs_datasets
def test_curated_records_have_a_notebook_path(records):
    """Every dataset shipped in a collection names the notebook it came from."""
    missing = [
        r.unique_name
        for r in records
        if any(t in (r.data_foundry_status or []) for t in COLLECTION_TAGS) and not r.notebook_path
    ]
    assert not missing, f"shipped in a collection but no notebook_path: {missing}"


@_needs_datasets
def test_notebook_paths_are_in_sync_with_the_datasets_tree():
    """The recorded pointers match what the tree holds — nothing moved or was re-run since."""
    drift = sync_notebook_paths(RECDIR, DATASETS, check=True)
    assert not drift, f"notebook_path drift (run `data-foundry-curation sync-notebooks`): {drift}"


@_needs_datasets
def test_notebook_path_names_the_run_that_shipped(records):
    """Where a dataset has sibling runs, the pointer is the one whose output carries the
    shipped container's UUID -- a ``_1m`` sub-sample or a ``_clf`` alternative target, not
    whichever notebook happens to match the directory name.
    """
    repo_root = resolve_curation_root().parent
    uuids = shipped_uuids()
    problems, checked = [], 0
    for r in records:
        uuid = uuids.get(r.unique_name)
        if not (uuid and r.notebook_path):
            continue
        notebook = repo_root / r.notebook_path
        if len(list(notebook.parent.glob(f"{r.unique_name}*.ipynb"))) < 2:  # nothing to disambiguate
            continue
        checked += 1
        if uuid not in notebook.read_text(encoding="utf-8"):
            problems.append((r.unique_name, r.notebook_path))
    assert not problems, f"notebook_path names a run that did not ship: {problems}"
    # 10 datasets ship a _1m sub-sample, pva_revenue_prediction_kddcup98 ships _clf; guards
    # against this check going vacuous if the layout changes.
    assert checked >= 11, f"expected at least 11 datasets with sibling notebooks, found {checked}"
