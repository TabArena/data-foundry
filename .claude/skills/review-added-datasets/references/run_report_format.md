# Run report format

A batch run of `/add-dataset` writes one markdown report. `scripts/build_review_page.py` turns it into the review
page; this file is the format that script reads. When the report breaks a rule below, the script stops and names
the line and the section. Fix the report, not the parser. `NEW_DATASETS_ISSUES.md` of the TabArena v0.2 working
copy follows this format, and the example at the end is the test fixture `tests/fixtures/review_page_report.md`.

## Structure

```text
# <title> (<YYYY-MM-DD>)
<header>
## Summary per record                                   required
## Record fields that disagree with the definition      optional
## Across datasets                                      optional
## Per dataset                                          one or more sections like this one
```

The first line is the title. The first date in it is the run's date (the page subtitle says "run of <date>"; without
a date it says when the page was built). The header, everything up to the first `##`, is shown in the Summary view
under "About this run".

The script recognises three `##` sections by how their heading starts: `## Summary`, `## Record fields` and
`## Across datasets`. Each may appear once. Every other `##` section holds record sections (`### <unique_name>`), so
a report can split its records over several, such as `## Per dataset` and `## Records added late`. Text between such
a `##` heading and its first `###` is not shown. The order of the `##` sections does not matter, and headings inside
fenced code blocks are ignored.

## Summary per record

A table: a header row, the separator row, then one row per record with three cells.

```text
| Record | Outcome | Main points |
|---|---|---|
| [`<unique_name>`](#<unique_name>) | added | ... |
```

The rows give the records and their order on the page. A unique name appears in one row only. Write a `|` inside a
cell as `\|`. A `(late)` after the link marks a record that joined the run late; the page tags it "Late" and offers
a filter for it.

The page does not show the outcome and points cells at present, but the outcome decides the record's category:

| Outcome cell | Category on the page | Verdicts |
|---|---|---|
| starts with `not added` | Not added; no folder | leave out, add it, discuss |
| contains `recommended` (`added; recommended No (...)`) | Rec. not to ship | ship, ship after changes, don't ship, discuss |
| anything else (`added`, `added as ...`) | To ship | the same |

`added as `<folder>`` names the folder when it differs from the unique name (`added as `aeolus_1m``). Otherwise the
folder is `<root>/<unique_name>/`. When the folder is gone from the working copy, the page shows the definition from
the last commit that still had its `dataset.py` and marks it retired. A record whose curation record has a
`suggestion` starting with `No` is shown as "Decided: verify" whatever the outcome says: triage already decided, and
the curator only checks that the record says so.

## Record sections

Each summary row needs exactly one `### <unique_name>` section, under any `##` section that is not one of the three
fixed ones. A `###` heading that looks like a unique name (lower case, digits, `_`) but has no summary row stops the
script; notes for several records take a heading in words (see shared notes below).

Inside a record section, a bold label at the start of a line opens a block. The blocks appear in the Details tab, in
the order of the report. The rest of the label's line is the block's first line, text before the first label belongs
to Outcome, and a label used twice adds to the same block.

| Label | Block |
|---|---|
| `**Outcome:**` | Outcome |
| `**Record judgment:**` | Record judgment |
| `**Data:**` | Data |
| `**Definition:**` | Definition |
| `**Checks:**` | Checks |
| `**Probes:**` | Probes |
| `**Verification:**`, `**Fix round:**`, or a `#### Verification ...` heading | Verification |
| `**Recommendation:**` | Recommendation |
| `**Task:**` | Task |
| `**Split:**` | Split |
| `**Source and licence:**` | Source and licence |
| `**Final critic:**` | Final critic, remaining points |
| `**Issues for <anyone>:**`, `**Issues:**`, `**Open questions:**` | the numbered issues (Decisions tab) |

A label may carry a tail in parentheses, which starts the block's text: `**Verification (fix round, 2026-10-07):**`.
Any other bold text at the start of a line is ordinary text of the current block.

### Numbered issues

The issues block holds what the curator decides on. Text before the first issue is shown above the issues. Each issue
starts with `N. ` at the start of a line; the indented and blank lines after it belong to it, up to the next issue or
the next label. A paragraph that is not indented after the last issue also belongs to that issue, so close the block
with the next label.

An issue is a decision for the curator, with the evidence from our own splits, probes and sources. Scores that
other benchmarks published for the dataset (TALENT, leaderboards) are no issue and no evidence: their random splits
are wrong for most of our tasks (Lennart, 2026-10-15). The same holds for another collection's version of the data
(TabSTAR's column choices, an OpenML copy's target): do not over-index on it, and name it only where it identifies
the source, a duplicate or the record's name.
Nor is a model's limit (a feature cap such as Mitra's, a runtime): the table keeps every relevant feature however
wide it is, so its width is no issue and a narrower version no alternative (Lennart, 2026-10-15,
coad_colon_adenocarcinoma).

The title is the bold text at the start of the issue (`1. **Keep the target in decibels?** The source ...`), or else
the first sentence. The number is the key under which the curator's mark is stored (`items.<N>`): numbers are unique
within a record, and a published page's issues are never renumbered.

An issue with a bold label that starts with `Resolved` or `Deferred` (`**Resolved (2026-10-12):** kept.`), or whose
title starts with one of the two words, is closed: the page hides it behind a toggle and counts it among the marks
only once the curator marked it.

### Shared notes

A `###` section with a heading in words, between the record sections, holds notes on several records. It appears in
the Details tab of each record it covers:

1. A first line `` Records: `a`, `b` `` names them. Use this in new reports.
2. Without that line, a heading with "the two" to "the ten" (or "the 3") covers that many records directly before
   the section (`### Across the three`).
3. Otherwise it covers the records since the previous shared section of the same `##` section. When there is none,
   the script stops and asks for a `Records:` line.

## Record fields that disagree with the definition

One bullet per record, each disagreement as `` <field> `<record value>`, definition `<definition value>` ``, several
separated by `; `, the bullet ending with a period:

```text
- `lgd`: problem_type `Binary Classification`, definition `Regression`; required_split `Random (IID)`, definition `Grouped (NON-IID)`.
- `house_sales`: original_source `Kaggle`, definition source `Other`.
```

Field names are lower case with `_` (`problem_type`, `required_split`, `original_source`, `domain`, `year`, `tag`).
The curator marks each one "take definition's value" (stored as `update`) or "keep record's value" (`keep`), under
the field name, so a field appears once per record. A bullet can wrap onto indented lines; lines that are not
bullets (an intro) are not shown.

Record fields go only here, never into a numbered issue: an issue's marks (as implemented / change / discuss) do not
say which value the record takes, and the curator found such issues confusing (Lennart, 2026-10-15,
breast_cancer_prediction). Record changes that are not a disagreement with the definition (a dead source link, a
missing `v2_path`) need no mark: Claude makes them when it applies the verdict and says so in the outcome.

## Across datasets

`###` sections, each with items written as top-level `- ` bullets. An item runs from its bullet to the next one; its
title is its bold lead or its first sentence. The section's heading is shown above its items. There is no text
between `## Across datasets` and the first `###`, nor before a section's first bullet, and every section has an item.

Each item's id is `x<section>-<item>`, both counted from 0 in the order of the report (`x0-0`, `x0-1`, `x1-0`). The
curator's marks are stored under these ids, so once the page is published, add new items at the end of a section and
new sections at the end, and close an item with a `Resolved` or `Deferred` label instead of deleting it. Closed items
are hidden behind a toggle, as issues are.

Items that are not in the report, such as the state of the repository after the run, can be added with
`--extra-crosscut <yaml>`, each with a fixed id of its own.

## Where the parts appear on the page

The rail lists the records in the order of the summary table. A record's view starts with its category, the split,
problem type, rows and build state, its name and its links, then (for a record decided in triage) the triage box.
Its tabs, in this order:

1. Use case: the definition's `task_summary` (or a `--tldr` entry).
2. Decisions: the numbered issues and the record-field table, with their marks.
3. Details: the run's report, the blocks of the record section and its shared notes.
4. `dataset.py`, 5. `README.md`, 6. Curation record: the files as of the build.

The verdict box follows the tabs. The Across datasets view holds the cross-dataset items, and the Summary view all
verdicts, the report's header, and the decisions as text or JSON.

## Example

A complete report with two records and one cross-dataset item:

```markdown
# Added datasets: issues (2026-10-01)

A test run of `/add-dataset` on two records: one added, one left out.

**Counts:** 1 added, 1 not added.

## Summary per record

| Record | Outcome | Main points for the curator |
|---|---|---|
| [`airfoil_self_noise`](#airfoil_self_noise) | added | The target is in decibels; keep it? |
| [`churn_telco_south_asia_duplicate`](#churn_telco_south_asia_duplicate) | not added; duplicate | The rows of `churn_telco_south_asia` with renamed values. |

## Record fields that disagree with the definition

- `airfoil_self_noise`: year `2014`, definition `1989`.

## Across datasets

### Framework (`src/data_foundry/v2/`)

- **`dataset new` leaves `domain` as `"TODO"`.** A fresh scaffold then fails to import. Proposal: fill it from the
  record.

## Per dataset

### airfoil_self_noise

**Outcome:** added and checked.

**Record judgment:** valid. NASA wind-tunnel measurements of airfoil noise.

**Issues for the curator:**

1. **Keep the target in decibels?** The source reports the scaled sound pressure level in dB; a log scale is the
   alternative.

### churn_telco_south_asia_duplicate

**Outcome:** not added. The files are the 2,000 rows of `churn_telco_south_asia` with renamed values.
```
