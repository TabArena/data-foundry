# Verifying a v1 dataset (a shipped BeyondArena container)

The shipped BeyondArena containers are format 1 (`container.format_version == 1`), built by the curation notebooks
under `datasets/beyond_iid/`. Use this file for Steps 0 and 1 of `/verify-dataset`, and for the v1 halves of rubric
items 14 and 15, when the question is about a shipped container. For anything that ships in TabArena v0.2, verify
the dataset's v2 folder instead (the skill's own Steps 0 and 1).

## Step 0 — Locate the inputs

1. **The notebook** — the record's `notebook_path`, the notebook that produced the shipped container. It is the
   record's own pointer to the one notebook behind this dataset, so use it rather than assuming
   `datasets/**/<unique_name>/<unique_name>.ipynb`. That matters where a dataset has sibling runs: a sub-sampled
   `<unique_name>_1m.ipynb` or an alternative target `<unique_name>_clf.ipynb` may be the run that shipped, and
   verifying the other one verifies a dataset nobody uses. If the record has no pointer yet, resolve it with
   `.venv/bin/python -m data_foundry.curation.cli sync-notebooks` (or list `<unique_name>*.ipynb` in the dataset
   directory and match the UUID as in item 14). Read it in full: the metadata cell, every preprocessing step, the
   split construction, and the committed cell *outputs* (the `run_all_checks` tables are evidence you should use, not
   re-run).
2. **The container** — `BEYOND_ARENA.get_dataset("<unique_name>")`, or `CuratedContainer.load(path)` for a copy in
   the warehouse (`<unique_name>/<uuid>/`, or `<version_of>/versions/<uuid>/` for a `_1m` version).
3. **The backlog record** and 4. **the upstream source**, as in the skill.

If the container has not been saved yet, run the notebook's Bundle + Bundle Checks cells' logic yourself (construct
the container in a scratch script). **Do not re-run the notebook end to end and re-save**: `save()` mints a new UUID,
and for a shipped dataset that breaks the collection pin.

## Step 1 — Run the automated checks

```python
from data_foundry.bundle_checks import run_bundle_checks
from data_foundry.collections import BEYOND_ARENA          # or CuratedContainer.load(path)

container = BEYOND_ARENA.get_dataset("<unique_name>")
report = run_bundle_checks(container)                       # prints the report
```

For a whole collection: `.venv/bin/python .claude/skills/verify-dataset/scripts/check_collection_bundles.py --examples 5`.

A format-1 container is judged by the v1 split protocol (`curation_recommendations`): repeats by train size
(`get_recommended_splits_dimensions`), at most 1M train and 250k test rows per split, and a frame of 1.25M rows or
more as a single holdout split in a `_1m` version. A warning the curator accepts belongs in the notebook's
`ignore=[...]` **with the reason**; report errors and warnings as the skill's Step 1 says.

The leak probes, task probes and group probes (`.claude/skills/verify-dataset/scripts/*_probes.py`) run on v2 definitions. For a shipped
container, run the same probes by hand on its splits (see
[`../../check-candidate/references/leak_checks.md`](../../check-candidate/references/leak_checks.md)), or run the
scripts on the dataset's v2 folder when its splits match the shipped ones.

## Rubric items 14 and 15, the v1 halves

| # | Item | What to actually check |
|---|---|---|
| 14 | **Record pointer** | Does the record's `notebook_path` name *this* notebook, is it under the tree the dataset ships from (`datasets/beyond_iid/` for BeyondArena — never `datasets/_dev/`, which holds work in progress and superseded copies), and does this notebook's saved output carry the UUID the collection pins (`BEYOND_ARENA` entry / `datasets/beyond_iid/final_uuid_list.py`)? A mismatch means the record points at the wrong run, or the notebook was re-run after the collection was pinned — say which. `.venv/bin/python -m data_foundry.curation.cli sync-notebooks --check` must be clean; evidence is the UUID string itself. |
| 15 | **Template conformance** | Does the notebook follow the *current* [`datasets/_template/_template.ipynb`](../../../../datasets/_template/_template.ipynb)? Open the template and compare section by section, not from memory, since it changes. Today that means the headings *Dataset and Task Metadata → Preprocessing → Data Checks → Task Curation → Bundle → Bundle Checks → Export* in that order; `run_all_checks(..., problem_type=task_mold.problem_type)` (not the old `classification=`); a *Bundle Checks* cell with `run_bundle_checks(curated_data, ignore=[...]).raise_if_errors()` before `save()`, where every `ignore` entry carries its reason; and `verify_saved_container(...)` after `save()`. Any other deviation from the template needs a reason in `curation_comments` or a cell comment. Report each drift as a concrete edit; restructuring an old notebook must not change its preprocessing or split logic. |

## Rules for notebooks

* **Do not edit committed notebook outputs.** They are the evidence trail.
* **A notebook that moves or gets superseded needs its record updated.** If the run that ships changes (a `_1m`
  sub-sample replaces the full-size run, a notebook is renamed or relocated), set the record's `notebook_path` to the
  new one (or run `.venv/bin/python -m data_foundry.curation.cli sync-notebooks`) in the same change.
