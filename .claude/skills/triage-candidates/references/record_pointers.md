# The definition pointers (`notebook_path`, `v2_path`)

A record points at two definitions. `v2_path` is its `dataset.py` in the TabArena v0.2 working copy
(`datasets/_dev/tabarena-v0pt2/<name>/`, or the `<name>_*/` folder whose class declares `version_of = "<name>"`);
it points into `_dev` by design until v0.2 ships. `notebook_path` is the v1 notebook a dataset was curated in:
for a shipped dataset the BeyondArena or TabArena v0.1 notebook that produced the container, otherwise an older one
under `_maintenance/` or `_dev/` (the rules below). A new dataset only ever gets a `v2_path`; nobody writes a v1
notebook any more (`DATA_FOUNDRY_V1.md`). `sync-notebooks` fills and
checks both, and the dashboard links them as 📓 and 🧩.

A curated dataset comes from exactly one notebook, and the record stores which one:

```yaml
notebook_path: datasets/beyond_iid/new_iid/student_portuguese_performance/student_portuguese_performance.ipynb
```

It lives in the record, not in a lookup, so the record names its notebook on its own — readable in
the file, in a PR diff, and by anything that never runs the dashboard — and so a later
reorganisation of `datasets/` is a path edit instead of a change to resolution rules. The
dashboard's 📓 button reads it directly, and only falls back to searching the tree for a record
that has no pointer yet.

**Which tree it must point into.** A dataset we *ship* is curated in its collection's tree, and
its pointer has to name that copy:

| The record ships in | Its notebook lives under |
|---|---|
| `BeyondArena` | `datasets/beyond_iid/{new_iid,old_iid,temporal,grouped}/` |
| `TabArena (v0.1)` only | `datasets/_maintenance/_old_collections/tabarena-v0pt1/` |
| nothing (a candidate) | `datasets/_dev/` while in progress, or `datasets/_maintenance/` once deprecated / suspended / out of scope |

**`datasets/_dev/` never backs a shipped dataset.** It holds work in progress *and* older copies of
notebooks that have since shipped from `beyond_iid` — most `_dev/feature_selection/<name>.ipynb`
files are exactly that. Pointing a shipped record there sends every reader to preprocessing that
produced no released data. For an unshipped candidate the reverse holds: `_dev` or `_maintenance` is
the right and only answer (`datasets/_maintenance/_deprecated/chronic_kidney_disease/…` is a correct
pointer). `sync-notebooks` enforces this — it resolves a shipped dataset only within its collection
tree, and leaves the pointer empty rather than naming a `_dev` copy, which the integrity tests then
report as a shipped record missing its notebook.

**Set it when:**

* a v2 `dataset.py` is created — `/add-dataset` does this as its own step;
* a notebook is renamed, moved between trees (`_dev/` → `beyond_iid/`, or into `_maintenance/`
  when a dataset is retired), or a dataset directory is renamed;
* the run that ships changes — a `<name>_1m.ipynb` sub-sample or a `<name>_clf.ipynb` alternative
  target supersedes the full-size run. Point at the run that shipped and say why in `## Comments`;
  a reader following the wrong sibling reads preprocessing that produced no shipped data.

**Check it when:**

* you are about to open a PR that touches `datasets/` or the records — `.venv/bin/python -m
  data_foundry.curation.cli sync-notebooks --check` prints every drifted record and exits non-zero, and plain
  `sync-notebooks` writes the fixes;
* a 📓 link opens something unexpected (the wrong tree, the wrong variant, a 404);
* you are verifying a dataset — `/verify-dataset` carries this as a rubric item: the pointer must
  name the notebook whose output holds the UUID the collection pins.

`tests/test_records_integrity.py` fails on a pointer that is missing on a shipped dataset, does not
exist, is not a `.ipynb`, sits outside its dataset's directory, has drifted from the tree, or names
a sibling run that did not ship. So it is enforced, not merely conventional — but the enforcement
compares against the tree, so a *deliberate* pointer to something the resolver would not pick needs
its reason in `## Comments` (and will still fail the sync check).

**Do not** hand-write a pointer you have not verified exists, and do not point a shipped dataset at
a working copy under `datasets/_dev/`: the shipped notebook is the one that produced the data.

