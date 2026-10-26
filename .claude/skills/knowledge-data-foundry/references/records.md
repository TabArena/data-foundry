# Curation records

The curation log is one markdown record per candidate dataset, `curation/records/<unique_name>.md`: YAML front matter
for the structured fields, then `## Comments` and `## Reference`. The records are the source of truth for every
verdict; the dashboard ([dashboard.md](dashboard.md)) edits the same files in place, so every change is a reviewable
diff. The schema is `CurationRecord` in `src/data_foundry/curation/record.py`; `curation/_template.md` is a copy-me
skeleton (files starting with `_` are skipped by the loader). What a verdict means is in the general
[selection.md](../../knowledge-curation/references/selection.md).

## Editing a record

Always through the store API, as one short step, right after reloading the record from disk: the curator edits the
same files in the dashboard while you work, so a copy read earlier is stale.

```python
from data_foundry.curation.record import load_vocabularies
from data_foundry.curation.store import load_record, save_record

rec = load_record("curation/records/<unique_name>.md")   # the path, not the bare name
rec.comments += "\n\n**Assessment (AI, 2026-10-19):** ..."
rec.needs_review = rec.review_reasons(load_vocabularies())
save_record(rec)
```

If the file changed between your read and your write, re-read it and redo the edit on the new content. The same holds
for `curation/vocabularies.yaml` and every other file under `curation/`. Afterwards run
`.venv/bin/python -m data_foundry.curation.cli validate`.

Every new file under `curation/` (a record, a changed vocabulary) is staged with `git add` as soon as it exists; an
untracked record is invisible to PRs and to other curators. Staging is not committing: before the session ends, name
every uncommitted curation change and offer the commit.

## Who wrote a comment line

* `CC (YYYY-MM-DD, Name):` is the curator's decision, with its reasoning. Only for decisions the curator made (in the
  dashboard, in chat, on a review page), and then the fields change with it.
* `**Assessment (AI, YYYY-MM-DD):**` is the AI's evidence and recommendation ("recommend ...; the curator has the
  call"). The verdict and markers stay as they are.
* `**Counter-argument (AI):**` is a disagreement with a documented decision, argued from the data
  ([principles.md](../../knowledge-curation/references/principles.md), "Arguing a call"). The fields stay as they are.
* `**Screening (AI, YYYY-MM-DD):**` is the dossier `/screen-candidates` writes: the verdict and priority in its first
  line, then the source, the use case, siblings and duplicates, papers, the risks for adding and the priority factors
  (the format is in [the skill](../../screen-candidates/SKILL.md), step 6). It sits right under the AI disclaimer.
* `**Exception to <ID> (YYYY-MM-DD, Name):**` is a curator's decision to depart from a rule for this dataset: the fact
  that sets the case apart, then `Serves P<k>: <why>.` The rule does not change; the dataset's notes and the Cases
  table of the rule's file get the same exception
  ([principles.md](../../knowledge-curation/references/principles.md), "Exceptions and amendments").
  `test_records_integrity.py` checks that the ID exists and the reason is given.
* `**Consistency check (AI, YYYY-MM-DD):**` is the AI's question to the curator when a decision departs from a rule
  without a fact that sets it apart, contradicts a similar precedent, drifts from the curator's earlier calls, or is
  the third exception of its kind ([principles.md](../../knowledge-curation/references/principles.md), "Consistent
  judgement"). The curator's answer follows as a `CC` line; the check stays as the record of the question.
* `**Open issues (AI, YYYY-MM-DD):**` followed by numbered issues: the open questions of a record that has no dataset
  folder, until the curator settles them (a folder keeps them in its `REVIEW.md`, [working_copy.md](working_copy.md)).
* A field edit alone gets no comment: git records who changed what.

Never delete existing comments. Never name company code repositories in a record (house rules in the
[skill index](../SKILL.md)).

## AI screening of untriaged records (`AI (UNVERIFIED)`)

The AI may draft a provisional screening for a record without a verdict (`/screen-candidates`), honestly labelled
until a curator verifies it:

1. set a `suggestion` (`TBD -> Yes`, `TBD -> 2nd Tier` or `No`, never a plain `Yes`), any justified
   `decision_markers`, and a `priority` from 1 to 5 unless the verdict is `No`;
2. fill empty metadata (`problem_type`, `required_split`, `domain`, `year`, `original_data_state`) only where it can
   be inferred with confidence, never overwriting a value;
3. add `AI (UNVERIFIED)` to `checked_by` and `AI-Filled (Verify)` to `tags`;
4. put the "AI-FILLED, UNVERIFIED" disclaimer at the top of `## Comments`, then the screening block, keeping every
   existing note below it.

`AI (UNVERIFIED)` in `checked_by` puts the record in the review queue (status 🤖) until a curator verifies it (the ✓
action replaces the AI with their name). `test_ai_reviewed_records_follow_convention` enforces the convention. A
record that already has a verdict gets an `**Assessment (AI)**` instead.

## The fields

| Field | Meaning |
|---|---|
| `unique_name` | Stable id and file stem, snake_case, globally unique; the dataset's canonical name. Renaming breaks links and review marks, so names stay (a duplicate keeps its name when links to it must stay valid: the indabax records, 2026-10-12). |
| `name` | The names the dataset is published under, joined with ` / `. The body has no title heading. |
| `checked_by` | The curators who reviewed it, or `AI (UNVERIFIED)`. |
| `data_foundry_status` | Work state and collection membership in one list (below). |
| `claimed_by` | The curator holding the claim, mirrored from the claims board ([claims.md](claims.md)); one name, never the AI. |
| `suggestion` | The verdict; the one required field. |
| `priority` | 1-5: how urgently a curator should act on the record at its stage (5 first): verify the screening and send it to `/add-dataset`, then review what `/add-dataset` added. Set by `/screen-candidates`, set again by `/add-dataset` from what it measured, changed by the curator; none on a rejected record. The factors are in [selection.md](../../knowledge-curation/references/selection.md), "Priority". |
| `decision_markers` | Issue flags (`Duplicate`, `Trivial`, `Image`, `Too Small`, `Data Quality Issue`, ...); a clean dataset has none. |
| `tags` | Priority and shape tags (`New IID`, `Non-IID (Temporal)`, `Non-IID (Grouped)`, `Tiny Data`, `Many features`, `Multi-target`, `Better Data Available`). Remove a tag that does not apply. |
| `collections` | External benchmarks the dataset appears in (TabSTAR, CARTE/TARTE, TabRed, TableShift, ...), never our own. |
| `original_source` | Where the data was first published ([provenance.md](../../knowledge-curation/references/provenance.md)): `OpenML`, `UCI`, `Kaggle`, `Zindi`, `GOV Website`, `Github`, `Company`, `Website`, `Other`, `?`. This is the record's vocabulary; the definition's `source` uses the schema's values (`GitHub`, `HuggingFace`, `Customer`, `ASlib`, ...), and `dataset new` maps one to the other. |
| `year` | The year the data was first published (free text: `2014`, `? (2014)`). |
| `domain` | The application domain (`medical & healthcare`, `finance`, ...). |
| `required_split` | `Random (IID)`, `Temporal (NON-IID)`, `Grouped (NON-IID)`; `Custom` and `?` exist in the vocabulary, but a task is IID, grouped or temporal ([splits.md](../../knowledge-curation/references/splits.md)). Once a definition exists, the field holds its regime, one value, and the regime tags (`Non-IID (Grouped)`, `Non-IID (Temporal)`) agree with it (aligned for 34 records on 2026-10-19). |
| `problem_type` | `Binary Classification`, `Multiclass Classification`, `Regression`, `Other`, `TBD`: the task we ship. |
| `original_data_state` | `One Table`, `Database (or multiple to-be-joined tables)`, `Other`. |
| `source_links` | The dataset's own download links and DOIs, one per entry; they double as its identity for de-duplication. A line starting with `#` is a note on the next link. Related work goes into the comments, not here. |
| `v2_path`, `notebook_path` | The definition pointers (below). |

Optional fields left empty are fine ([selection.md](../../knowledge-curation/references/selection.md), "Reading
decision markers"). A record whose definition is not finished or built may keep an empty `year`, `domain` or
`required_split`; they are filled when the dataset is built (Lennart, 2026-10-19: zillow_prize,
distribution_transformers_at_cauca_department). Dropdown values outside `curation/vocabularies.yaml` put the record in the review queue: add a new
option through the dashboard's ＋ header button or `save_vocabularies`.

### `data_foundry_status`

* The work state: `DF: Yes` (in Data Foundry), `WIP (Triage)` (the verdict is open and someone is settling it),
  `WIP (DF)` (the verdict is a final `Yes` and the definition is in progress; never without a final `Yes`),
  `DF: Much work`, `DF: Suspended`.
* Collection membership: `TabArena (v0.1)`, `BeyondArena`. Every shipped dataset carries its collection tags and
  `DF: Yes` (51 TabArena v0.1 and 142 BeyondArena datasets, 144 in their union). A `DF: ...` value without a
  collection tag is valid: the dataset is in Data Foundry but in no shipped collection (`datasets/_maintenance/`,
  `datasets/_dev/`). Do not add a collection tag to "fix" it.
* A shipped dataset's verdict is `Yes`, `Yes (Disagreement)` or `No (Retired)`; anything else is a `ship_conflict`.
* `Disagreement` together with `DF: Yes` is valid and can happen: the dataset is in Data Foundry while curators still
  disagree about it (infrared_thermography_temperature, phiusil_phishing; Lennart, 2026-10-19). Do not flag it.

### Claims

Who works on which dataset lives on the claims board, a branch every curator pushes to directly
([claims.md](claims.md)): `claims claim <names>` before the work, `claims release <names>` when it reaches `main` or is
dropped. Leave a dataset another curator holds alone (no triage, no edits, only a note to the curator). The record
mirrors the claim: `claimed_by` names the holder and a WIP value says the stage, both written by the `claims` commands
and carried to `main` by the work's own PR, which sets the final state. `claims sync` repairs a record that drifted
from the board.

### Duplicates and retirements

* A redundant copy is `No` + `Duplicate`, named `<canonical>_duplicate` when it is created; an existing record keeps
  its name when links to it must stay valid. Every `*_duplicate` record carries the marker and no `Yes`
  (`test_duplicate_records_follow_convention`).
* A retired dataset is `No (Retired)` with its markers, its folder is removed from the working copy and its `v2_path`
  cleared in the same change, with a CHANGELOG entry ([working_copy.md](working_copy.md)). A dataset to be rebuilt
  from other sources gets a new record that names the sources and the plan (tcga_coad_molecular_subtype,
  corporate_issuer_credit_rating).

## The review queue

`needs_review` is derived, never set by hand: `CurationRecord.review_reasons()` recomputes it on every save. Today it
holds `suggestion` (no verdict), a dropdown value outside the vocabulary, `ai_unverified`, `ship_conflict`,
`wip_unclaimed`, `claim_without_wip` and `better_data_review` (tagged `Better Data Available`: a larger or newer
dataset for the same task has its own record, and a curator must decide whether this one's verdict holds). A new
automated check goes into `review_reasons()` with a matching assertion in `tests/test_records_integrity.py`.

## The definition pointers (`v2_path`, `notebook_path`)

`v2_path` is the record's v2 `dataset.py` in the TabArena v0.2 working copy (`datasets/_dev/tabarena-v0pt2/<name>/`,
or the `<name>_*/` folder whose class declares `version_of = "<name>"`); it points into `_dev` until v0.2 ships.
`notebook_path` is the v1 notebook a dataset was curated in; a new dataset only ever gets a `v2_path`
([DATA_FOUNDRY_V1.md](../../../../DATA_FOUNDRY_V1.md)). The pointers live in the record, so it names its definition on
its own (in the file, in a PR diff), and a reorganisation of `datasets/` is a path edit. The dashboard links them as 📓
and 🧩.

A shipped dataset's notebook lives in its collection's tree:

| The record ships in | Its notebook lives under |
|---|---|
| `BeyondArena` | `datasets/beyond_iid/{new_iid,old_iid,temporal,grouped}/` |
| `TabArena (v0.1)` only | `datasets/_maintenance/_old_collections/tabarena-v0pt1/` |
| nothing (a candidate) | `datasets/_dev/` while in progress, `datasets/_maintenance/` once deprecated, suspended or out of scope |

`datasets/_dev/` never backs a shipped dataset: it holds work in progress and older copies of notebooks that have since
shipped. `sync-notebooks` resolves a shipped dataset only within its collection tree.

Set the pointers when a v2 `dataset.py` is created (`/add-dataset` does it), when a dataset is retired (clear
`v2_path`), when a folder or notebook moves, and when the definition that ships changes (a `_1m` version or a `_clf`
target supersedes the full run; say why in the comments). Check them before a PR that touches `datasets/` or the
records: `.venv/bin/python -m data_foundry.curation.cli sync-notebooks --check` prints every drifted record and exits
non-zero; plain `sync-notebooks` writes the fixes. `tests/test_records_integrity.py` fails on a pointer that is
missing on a shipped dataset, does not exist, sits outside its dataset's directory or has drifted from the tree. Never
hand-write a pointer you have not checked.
