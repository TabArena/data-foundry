# Review file format

The open review issues live in git, next to what they are about:

| Where | What |
|---|---|
| `datasets/_dev/tabarena-v0pt2/<folder>/REVIEW.md` | the open issues of one dataset of the working copy |
| an `**Open issues (AI, <date>):**` block in a record's `## Comments` | the open issues of a record without a folder (not added) |
| `datasets/_dev/tabarena-v0pt2/REVIEW.md` (optional) | items that span datasets |

`scripts/collect_reviews.py` reads all three and writes one report; `scripts/build_review_page.py` turns that
report into the review page. When a file breaks a rule below, the collector stops and names the file and the line.
Fix the file, not the scripts.

A review file holds only what is still open. When the curator settles an issue, the decision goes to the definition
and the record, and the issue leaves the file; a REVIEW.md without issues and field rows is deleted. How to write an
issue (evidence, links, what is no evidence) is in
[`../../knowledge-curation/references/writing.md`](../../knowledge-curation/references/writing.md); the
REVIEW.md convention of the working copy in
[`../../knowledge-data-foundry/references/working_copy.md`](../../knowledge-data-foundry/references/working_copy.md).

## REVIEW.md of a dataset

The title is the record's `unique_name` (`curation/records/<unique_name>.md`). The folder can differ, such as a
`_1m` version; the record's `v2_path` names it. Then come these blocks, each opened by its bold label at the start
of a line, in this order:

| Label | Required | Content |
|---|---|---|
| `**Outcome:**` | yes | One short paragraph: what was added and what the AI recommends. |
| `**Main points:**` | yes | One line: what the curator decides. |
| `**Record fields that disagree with the definition:**` | no | One item per field, see below. |
| `**Record judgment:**` | no | The AI's judgment of the record, in a few lines. |
| `**Issues for <curator>:**` | no | The numbered issues. |

The first sentence of the outcome is the record's outcome on the page and sets its category:

| First sentence | Category on the page |
|---|---|
| `added` | To ship |
| `added as `<folder>`` (required when the folder is not the unique name) | To ship |
| `added; recommended `No` (<markers>)`, or another text with `recommended` | Rec. not to ship |

Leave out what the generated README or the run's log holds: data, definition and checksum, checks, probes and
verification rounds. The run's process log stays in its local run folder `local-data-warehouse/_runs/<run>/`, and
no local path goes into a review file. A statement that the current `dataset.py` contradicts is removed.

### Issues

Each issue starts with `N. ` at the start of a line; its other lines are indented by three spaces (or blank). The
title is the bold text at the start (`1. **Keep the target in decibels?** The source ...`), or else the first
sentence. An issue keeps its `Implemented:` and `Alternative:` parts, their numbers and the public links to its
evidence. An answer to the curator's question goes into the issue as `**Answer (AI, <date>):**`; it does not close
the issue.

The number is the key of the curator's mark (`items.<N>` on the page). Numbers are unique in the file and never
change; gaps are fine. A new issue takes the next number after the highest the file has had, so an old mark never
lands on it.

The collector stops on:

* an issue with a `**Resolved (...)**` or `**Deferred (...)**` label, or a title that starts with either word:
  settled issues leave the file;
* a line inside an issue that starts with a block label of the report (`**Data:**`, `**Split:**`, `**Task:**`,
  `**Verification:**`, ...): the page would read it as a new block;
* a number used twice.

### Record fields

One item per field, the field name in backticks, the bullet ending with a period:

```text
- `problem_type`: record `Regression`, definition `Binary Classification`.
- `original_source`: record `Kaggle`, definition `GOV Website`.
```

Field names are lower case with `_`: `problem_type`, `required_split`, `original_source`, `domain`, `year`, `tag`
(a `Non-IID` tag that names another regime). The record values `Website` and `Company` count as the schema's
`Other`. The curator marks each row "take the definition's value" (`update`) or "keep the record's value" (`keep`),
stored under the field name, so a field appears once per file. Record fields go only here, never into a numbered
issue: an issue's marks do not say which value the record takes (Lennart, 2026-10-15, breast_cancer_prediction).
Record changes that are not a disagreement (a dead link, a missing `v2_path`) need no mark: Claude makes them.

## Open issues of a record without a folder

A record that was not added has no folder for a REVIEW.md. Its open issues are one block in the record's
`## Comments`, written through the store API:

```markdown
**Open issues (AI, 2026-10-01):** not added; duplicate. The files are the 2,000 rows of `churn_telco_south_asia`
with renamed values.

1. **Leave it out as a duplicate?** Every row matches a row of `churn_telco_south_asia` once the values are
   renamed.
```

The lead after the label must start with `not added`. Its first sentence is the outcome on the page (category "Not
added"), the rest is the main points. The issues follow the rules above. The block ends at the first line that is
neither blank, nor indented, nor the start of an issue, such as the next `CC (...)` comment. A record has one such
block at most, and none when its folder exists: then the issues belong in the folder's REVIEW.md.

## Items across datasets

The working copy's own `REVIEW.md` holds the items that span datasets:

```markdown
# Across datasets

### Framework (`src/data_foundry/v2/`)

- **`dataset new` leaves `domain` as `"TODO"`.** A fresh scaffold then fails to import. Proposal: fill it from the
  record.
```

After the title come only `### <section>` headings, each with items written as top-level `- ` bullets. An item runs
from its bullet to the next one; its title is its bold lead or its first sentence. The page stores the curator's
mark under the id `x<section>-<item>`, both counted from 0 in file order. So while a page is in use, close a settled
item with a `**Resolved (<date>):**` label (the page hides it) instead of deleting it, and add new items at the end
of a section and new sections at the end. Closed items are deleted when the next page starts.

## The collected report

```bash
.venv/bin/python .claude/skills/review-added-datasets/scripts/collect_reviews.py --root datasets/_dev/tabarena-v0pt2 \
    --out local-data-warehouse/_runs/<date>_review/review_report.md [--names a,b] [--title <text>] [--date <YYYY-MM-DD>]
```

The report is generated: never edit or commit it. `build_review_page.py` parses it as follows; the collector
checks that every issue it read arrives there.

```text
# <title> (<YYYY-MM-DD>)
<header>
## Summary per record                                   one row per record: | [`name`](#name) | outcome | points |
## Record fields that disagree with the definition      one bullet per record: - `name`: field `x`, definition `y`; ...
## Across datasets                                      the working copy's REVIEW.md
## Per dataset                                          one `### <unique_name>` section per record
```

* The first date in the title is the date of the page ("run of <date>"). The header, up to the first `##`, is shown
  in the Summary view under "About this run".
* The `##` sections are recognised by how their heading starts (`## Summary`, `## Record fields`,
  `## Across datasets`); every other `##` section holds `### <unique_name>` sections.
* The outcome cell sets the category: starting with `not added`, Not added (no folder); containing `recommended`,
  Rec. not to ship; otherwise To ship. `added as `<folder>`` names the folder. A folder gone from the working copy is
  shown from the last commit that still had its `dataset.py`, marked retired. A record whose `suggestion` starts
  with `No` is shown as "Decided: verify" whatever the outcome says.
* In a record section, a bold label at the start of a line opens a block: `**Outcome:**`, `**Record judgment:**`,
  `**Issues for <anyone>:**` (or `**Issues:**`, `**Open questions:**`), and the run-log labels the builder still
  reads (`**Data:**`, `**Definition:**`, `**Checks:**`, `**Probes:**`, `**Verification:**`, `**Fix round:**`,
  `**Recommendation:**`, `**Task:**`, `**Split:**`, `**Source and licence:**`, `**Final critic:**`). A label may
  carry a tail in parentheses. Any other bold text at the start of a line is text of the current block.
* An issue or cross-dataset item with a `Resolved` or `Deferred` label, or whose title starts with either word, is
  closed: the page hides it behind a toggle.
* The builder also reads two things the collector does not write: a `(late)` tag after the record link, and shared
  notes, a `###` section with a heading in words that covers the records its first line `` Records: `a`, `b` ``
  names.

## Where the parts appear on the page

The rail lists the records in the order of the summary table. A record's view starts with its category, the split,
problem type, rows and build state, its name and its links, then (for a record decided in triage) the triage box.
Its tabs, in this order:

1. Use case: the definition's `task_summary` (or a `--tldr` entry).
2. Decisions: the numbered issues and the record-field table, with their marks.
3. Details: the outcome and the record judgment.
4. `dataset.py`, 5. `README.md`, 6. Curation record: the files as of the build.

The verdict box follows the tabs. The Across datasets view holds the cross-dataset items, and the Summary view all
verdicts, the report's header, and the decisions as text or JSON.

## Example

The test fixtures in `tests/fixtures/review_files/` are a complete example: one REVIEW.md
(`working_copy/airfoil_self_noise/REVIEW.md`), the working copy's REVIEW.md (`working_copy/REVIEW.md`, the
cross-dataset item above) and a record with an open-issues block (`records/churn_telco_south_asia_duplicate.md`,
the block above). The REVIEW.md reads:

```markdown
# airfoil_self_noise

**Outcome:** added. NASA's wind-tunnel table as published; the AI recommends shipping it.

**Main points:** The target is in decibels; keep it?

**Record fields that disagree with the definition:**

- `year`: record `2014`, definition `1989`.

**Record judgment:** valid. NASA wind-tunnel measurements of airfoil noise.

**Issues for the curator:**

1. **Keep the target in decibels?** The source reports the scaled sound pressure level in dB; a log scale is the
   alternative.
```

Collected with `--title "Added datasets: issues" --date 2026-10-01`, the three give
`tests/fixtures/review_page_report.md`, the report the page tests build from.
