# Review format

A dataset's review lives in the `## Review` section of its curation record (`curation/records/<unique_name>.md`,
between `## Comments` and `## Reference`), the one source of its curation (Lennart, 2026-11-11): the review of an added
dataset, or of a record without a folder (not added). A point that spans datasets has no review file: a standing rule
goes into the knowledge skills as a draft for the curator to confirm, open work becomes a GitHub issue (Lennart,
2026-11-25).

`data_foundry.curation.review` (`src/data_foundry/curation/review.py`) is the one parser of this format: the review
page (`scripts/review_page.py`), the decision register and the priority factors read reviews through it. The page
stays in the local run folder and is never committed; it is built from the records, with no file in between. When a
review breaks a rule below, the parser stops and names the record and the line, counted in that file. Fix the record,
not the parser. It also stops on a `REVIEW.md` anywhere in the working copy and on an `**Open issues (AI, <date>):**`
block in a record's `## Comments`, both retired on 2026-11-11; either is moved by hand into the record's `## Review`,
in the format below. `scripts/review_page.py check` runs the parser over the records and prints its warnings.

A record's review keeps every issue, so the page shows how each dataset was decided. When the curator settles an
issue, the decision goes to the definition and to the record's `## Comments` (a `CC` line), and the issue stays in the
review with the curator's turn and a closing `**Resolved (<date>, <who>):**` turn that states the decision; the page
hides it behind "Show resolved issues". A review is never deleted, so a decided dataset's decisions stay in its record
(Andrej, 2026-11-02); the page leaves a record with nothing left to decide off, unless `--keep-settled`
(Lennart, 2026-11-08). A settled record-field row leaves the review. A review with a `**Review panel:**` block may
have no issue and no field row: the panel found nothing for the curator, who only sets the verdict; without a panel
(or a `**Horizon:**` block, itself a decision) such a review is an error. How to write an issue (evidence, links, what
is no evidence) is in
[`../../knowledge-curation/references/writing.md`](../../knowledge-curation/references/writing.md); the record's
sections in [`../../knowledge-data-foundry/references/records.md`](../../knowledge-data-foundry/references/records.md),
and the working copy in
[`../../knowledge-data-foundry/references/working_copy.md`](../../knowledge-data-foundry/references/working_copy.md).

## Editing a record's review

Edit the `## Review` section in place, with an exact-string edit of the current record file (the Edit tool), or
through the store API (`record.review`, after a fresh `load_record`, then `save_record`); never by saving a record
loaded earlier, which would overwrite what the dashboard or another session wrote since. This is the one exception to
"records only through the store API": a review is long markdown that an exact edit changes safely while the dashboard
edits the front matter. The `CC` and `Assessment` lines go into `## Comments` through the store API as before. The
section holds no `## ` heading (the next one ends it) and no `#` heading at all. A relative link in it resolves from
`curation/records/`: the definition is `../../datasets/_dev/tabarena-v0pt2/<folder>/dataset.py`.

## The review of an added dataset

The section opens with its `## Review` heading and has no title line of its own: the record's `unique_name` names
the dataset. The folder can differ from the unique name, such as a `_1m` version; the record's `v2_path` names it.
Then come these blocks, each opened by its bold label at the start of a line, in this order:

| Label | Required | Content |
|---|---|---|
| `**Outcome:**` | yes | One short paragraph: what was added and what the AI recommends. |
| `**Main points:**` | yes | One line: what the curator decides. |
| `**Record fields that disagree with the definition:**` | no | One item per field, see below. |
| `**Record judgment:**` | no | The AI's judgment of the record, in a few lines. |
| `**Horizon:**` | for a new temporal dataset | The argument for its horizon and time frame, which the curator signs off as the issue "H": in the issue shape, with the label alone on its line, then `* **Verdict:**` (one sentence: keep or change, and the confidence), `* **Length:**`, `* **Gap:**`, `* **Time frame:**` (the sources, what is ours), `* **Options:**` with the table `| | Option | What it does | Test windows | Pro | Con |` (the test windows: how many, and the rows of each, in a `_1m` version also how many are tested after the 500k cap; Lennart, 2026-11-11), today's length as the row marked `(implemented)`, and `* **Recommendation:**` ending in `**Decision:**`; footnotes, notes for the AI and turns as in an issue. The parser warns when a part is missing. |
| `**Issues for <curator>:**` | no | The numbered issues, 0 to N: a review that leaves nothing to decide has none. |
| `**Review panel:**` | no | The review panel of `/add-dataset`: its summary, then one section per role, see below. |

The first sentence of the outcome is the record's outcome on the page and sets its category:

| First sentence | Category on the page |
|---|---|
| `added` | To ship |
| `added as `<folder>`` (required when the folder is not the unique name) | To ship |
| `added; recommended `No` (<markers>)`, or another text with `recommended` | Rec. not to ship |

Leave out what the generated README or the run's log holds: data, definition and checksum, checks, probes and
verification rounds. The run's process log stays in its local run folder `local-data-warehouse/_runs/<run>/`, and
no local path goes into a review (nor into any committed file: the house rules of
[knowledge-data-foundry](../../knowledge-data-foundry/SKILL.md)). A statement that the current `dataset.py`
contradicts is removed.

### Issues

Each issue starts with `N. ` at the start of a line; its other lines are indented by three spaces (or blank). The
title is the bold question at the start (`1. **Keep the target in decibels?**`), alone on its line. An issue asks
one decision: a second one is an issue of its own, and a change proposed for a dataset is an issue in the review of
that dataset's own record, never only a line in another dataset's issue or answer. Then come, in this order:

1. The bullets of [writing.md](../../knowledge-curation/references/writing.md) ("Questions and issues for the
   curator"), each opened by its bold lead: `**Problem:**` (at most three sub-bullets of one sentence each), the
   optional `**Background:**`, `**Effect on the task:**`,
   `**Experiments:**`, `**Consistency:**`, `**Panel:**`, `**Unknown:**` (and any other bold lead that helps), then
   `**Options:**` with its table and `**Recommendation:**`, which ends with `**Decision:**` and the question. No
   paragraph of prose outside a bullet.
2. Optionally `**Notes for the AI:**` at the start of a line: what Claude needs to apply a decision (the code, the
   exact record or exception text, the probes to re-run). It runs to the footnotes or the end of the issue's text.
3. The footnotes, `[^key]: <text>` at the start of a line (continuation lines indented), referenced as `[^key]` in
   the text: every rule ID, rule wording and quoted earlier call. The page numbers them by first reference.

The options table has the columns `| | Option | What it does | Pro | Con |`, one row per option, a letter in the
first column, `(implemented)` on the row the definition has now (the page names it on the "As implemented" button
and highlights it when that mark is set). Every issue has two rows or more. Several points in
one cell are separated by `; `: the page shows them as bullets (green for Pro, red for Con) and tags the implemented
row and the row the `**Recommendation:**` names by its letter. A rule ID belongs in
a footnote or the notes for the AI, never in the bullets or the title. The page shows the problem, then every other
bullet before the options in a closed box "Details" (its summary lists their leads), then the options and the
recommendation. It shows the footnotes in a closed box "Rules and references" (a click on a reference opens it) and the
notes in a closed box "Notes for the AI". The same holds for the review of a record without a folder. The parser
warns (and the page is still built) for an open issue without the three required bullets or the table, with a table
that has no `(implemented)` row, with a problem of more than three bullets or a bullet of more than one sentence, or
with a rule ID in its text.

An issue keeps the public links to its evidence. An answer to the curator's question goes into the issue as
`**Answer (AI, <date>):**`; it does not close the issue. Write the curator's note that prompted it just before, at the
start of a line, as `**Lennart (<date>, <mark>):** <the note, in their words>`. The page shows an issue as a
conversation: the original text, then one box per turn, each starting at a line that opens
with one of these labels:
`**Answer (AI, <date>):**`, `**Consistency check (AI, <date>):**`, `**<curator> (<date>[, <mark>]):**`,
`**Resolved (<date>[, <who>]):**` or `**Deferred (<date>):**`. An open item whose last turn is the AI's is marked
"Your turn". An AI turn that asks the curator to choose (a consistency check, an answer that asks for a confirmation)
takes the issue's shape: the question in one sentence on the label line, `**Problem:**` bullets (and `**Background:**`
where needed), an options table `| | Option | What it does | Pro | Con |` with lowercase letters a, b, c,
`**Recommendation:**` and `**Decision:**`, the rule IDs in footnotes. The page renders it like an issue and shows the
table's rows as answer buttons under the turn (a turn without a table gets Agree / Disagree; lettered bullets
`- (a) ...` still work); a click writes `Reply (a): ...` (or `Agree.`) as the first line of the issue's note and
highlights the row. An answer that only reports findings keeps bullets, with its rule IDs in footnotes too. In an
issue and in every turn, measured results stand in tables, not in sentences
([writing.md](../../knowledge-curation/references/writing.md), "Results go in tables"). A table inside an issue or
a turn needs a blank line before and after it; without one, the lines around it render as table rows.

The number is the key of the curator's mark (`items.<N>` on the page). Numbers are unique in the review and never
change; gaps are fine. A new issue takes the next number after the highest the review has had, so an old mark never
lands on it.

The parser stops on text before the first issue, a heading inside the issues and a number used twice. A bold label
that is not one of the review's blocks (`**Split:**` at the start of a line) is text of the issue it stands in, and
an issue ends only at the next `N. ` line or the next block label of the table above. An issue with a bold
`Resolved` or `Deferred` label in its text, or a title that starts with either word, is closed: deferred when its last
closing turn (or its title) says `Deferred`, else resolved; any other issue is open. The page hides the closed ones, a
deferred one keeps its record on the page, and the decision register reads the state.

### Record fields

One item per field, the field name in backticks, the bullet ending with a period:

```text
- `problem_type`: record `Regression`, definition `Binary Classification`.
- `original_source`: record `Kaggle`, definition `GOV Website`.
```

Field names are lower case with `_`: `problem_type`, `required_split`, `original_source`, `domain`, `year`, `tag`
(a `Non-IID` tag that names another regime). The record values `Website` and `Company` count as the schema's
`Other`. The curator marks each row "take the definition's value" (`update`) or "keep the record's value" (`keep`),
stored under the field name, so a field appears once per review. Record fields go only here, never into a numbered
issue: an issue's marks do not say which value the record takes (Lennart, 2026-10-15, breast_cancer_prediction).
Record changes that are not a disagreement (a dead link, a missing `v2_path`) need no mark: Claude makes them.

### Review panel

The review panel of `/add-dataset` (claim auditor, column auditor, split auditor, domain practitioner, blind
reviewer, precedent checker, advocate, critic, mediator, review editor) leaves one optional block, the last of the
review, after the issues:

```markdown
**Review panel:** ship after changes (mediator). Claim audit: 14 claims, 12 hold, 1 refuted (fixed), 1 untested.
Blind review: would benchmark; main concern the year column. Debate: agreed on the split; disputed: keep `region`
(issue 3).

<details><summary>Claim audit</summary>

| Claim | Source | Test | Result | Rule |
|---|---|---|---|---|
| ... | ... | ... | holds | LEAK-2 |

</details>

<details><summary>Mediator</summary>

...markdown...

</details>
```

* The summary is the first paragraph, starting on the label's line. Its first sentence, up to the first full stop,
  is the panel's recommendation (`ship after changes (mediator)`), shown next to the curator's verdict box.
* Then come only `<details><summary>Role</summary>` ... `</details>` sections, one per role, with markdown inside
  (tables, lists, fenced code). The `<details>` line and the `</details>` line stand alone, and sections do not
  nest. No `#` heading anywhere, as in the rest of the review: use bold text.
* The panel holds no marks and no numbers: what the curator decides stays in the issues, which name the panel where
  it matters ("the critic disputes this"). No issue holds a line that starts with `**Review panel:**`: that line
  opens the panel and ends the issues.
* The panel stays as the run wrote it, also once every issue is resolved.
* The review of a record without a folder has no panel: the panel runs on a definition.

The parser stops on a second panel, a block label after the panel, a panel without its summary, text between the
sections, a `<details>` without its `</details>` (or with a fenced block left open), a `</details>` without its
`<details>`, or an empty section.

## A record without a folder

A record that was not added keeps its issues in the same `## Review` section, in the same format:

```markdown
## Review

**Outcome:** not added; duplicate. The files are the 2,000 rows of `churn_telco_south_asia` with renamed values.

**Main points:** Leave it out as a duplicate?

**Issues for the curator:**

1. **Leave it out as a duplicate?**

   * **Problem:** Every row matches a row of `churn_telco_south_asia` once the values are renamed[^1].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave out (implemented) | the record gets `No` | no copy in the benchmark | none found |
     | B | Add it | a second folder | none found | the same rows twice |

   * **Recommendation:** A. **Decision:** A or B?

   [^1]: **PROV-3** (Must): the data is real, not a real table someone reworked (relabelled, columns renamed).
```

The outcome starts with `not added`, and its first sentence is the outcome on the page (category "Not added"). The
parser tells the two kinds of review apart by the record: one whose `v2_path` names a folder starts its outcome with
`added`, one without starts with `not added`. A retired dataset, whose `v2_path` was cleared, keeps the `added` (or
``added as `<folder>` ``) its review had, and the page shows its definition from the last commit that still had it.
The other blocks and the issues follow the rules above.

The `**Open issues (AI, <date>):**` block that a record without a folder kept in its `## Comments` until 2026-11-11 is
retired. Move one by hand: its lead becomes the `**Outcome:**` (the first sentence, starting `not added`) and the
`**Main points:**` (the rest, or the question the issues put), its issues go under `**Issues for <curator>:**`, and
the block leaves `## Comments`.

## How the page reads a review

```bash
.venv/bin/python .claude/skills/review-added-datasets/scripts/review_page.py build \
    --out local-data-warehouse/_runs/<date>_review/review_page [--names a,b] [--metric-marks a,b|all] \
    [--horizon-marks a,b|all] [--split-marks a,b|all] [--keep-settled] [--title <text>] [--date <YYYY-MM-DD>]
```

* The page's date is `--date` (today by default). The Summary view's "About this page" names the counts, the records
  whose declared metric the page shows and marks (`--metric-marks`; without it the page shows no metric), the same
  for the horizon and test windows of a temporal task (`--horizon-marks`) and for the declared split
  (`--split-marks`), and the settled records left out.
* The outcome's first sentence sets the category: starting with `not added`, Not added (no folder); containing
  `recommended`, Rec. not to ship; otherwise To ship. The folder is the record's `v2_path` folder, or for a retired
  dataset the one the outcome names. A folder gone from the working copy is shown from the last commit that still
  had its `dataset.py`, marked retired; its review is in the record, so a retired dataset stays on the page while
  something on it is open. A record whose `suggestion` starts with `No` is shown as "Decided: verify" whatever the
  outcome says.
* The panel's `<details>` sections are read by the parser, so their markdown renders with raw HTML off; a line inside
  the panel that looks like another block label stays in the panel.

## Where the parts appear on the page

The rail lists the records by the record's `priority` (5 first, each under its heading; records without one last),
and within one priority the fewest open decisions (open issues and record-field rows) first; the page's
`review_order` sets it. A record's view starts with its priority and category, the split, problem type, rows and build
state, its name and its links, then (for a record decided in triage) the triage box. Its tabs, in this order:

1. Use case: the definition's `task_summary` (or a `--tldr` entry), then, for a record `--metric-marks` names, its
   metric: name, origin, original, reference, definition, reason, params, inputs and scoring columns, from `metric`
   in `dataset.py` (for a retired definition: name and origin from the README frontmatter).
2. Decisions: for a record `--horizon-marks` names, its `**Horizon:**` block as issue "H" first (the declared windows
   from `temporal` added to its Details box), then the numbered issues and the record-field table, with their marks.
3. Panel: the review panel's recommendation and summary, then one collapsible section per role, closed except the
   Mediator's ("No review panel" for a record without one).
4. Details: the outcome and the record judgment.
5. `dataset.py`, 6. `README.md`, 7. Curation record: the files as of the build.

The verdict box follows the tabs; for a record with a panel, a line "Panel: <recommendation>" stands under its
heading. The Summary view holds all verdicts, "About this page", and the decisions as text or JSON.

## Example

The test fixtures in `tests/fixtures/review_files/` are a complete example: a record whose review has a review panel
(`tests/fixtures/review_files/records/airfoil_self_noise.md`) and a record without a folder
(`tests/fixtures/review_files/records/churn_telco_south_asia_duplicate.md`, the review above). The first record's
review reads:

```markdown
## Review

**Outcome:** added. NASA's wind-tunnel table as published; the AI recommends shipping it.

**Main points:** The target is in decibels; keep it?

**Record fields that disagree with the definition:**

- `year`: record `2014`, definition `1989`.

**Record judgment:** valid. NASA wind-tunnel measurements of airfoil noise.

**Issues for the curator:**

1. **Keep the target in decibels?**

   * **Problem:**
     - The target is the sound pressure level in decibels, as NASA reports it.
     - Should it get a further log?
   * **Background:** Decibels are already a log scale, so a further log changes how errors on loud and quiet
     airfoils are weighed[^1].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Decibels (implemented) | target as published | the unit engineers use | none found |
     | B | Log of decibels | target transformed | none found | a log of a log scale |

   * **Recommendation:** A, the source's unit. **Decision:** A or B?

   **Notes for the AI:** on B, set `target_transform` in `dataset.py` and re-run `dataset check`.

   [^1]: **MET-3** (Must): the score is on the scale the task means, the source's; the target may ship on the
     scale a practitioner models it on.

**Review panel:** ship (mediator). Claim audit: 2 claims, 2 hold. Blind review: would benchmark; main concern the
decibel scale. Debate: agreed on the random split; disputed: the target scale (issue 1).

<details><summary>Claim audit</summary>

| Claim | Source | Test | Result | Rule |
|---|---|---|---|---|
| 1,503 rows | UCI page | row count | holds | |
| target in dB | NASA report, p. 3 | column range | holds | |

</details>

<details><summary>Mediator</summary>

Ship. The advocate and the critic agree on the split; the target scale stays open as issue 1.

</details>
```

The page tests build from these two records (`tests/test_review_page.py`).
