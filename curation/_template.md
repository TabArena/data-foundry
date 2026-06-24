---
unique_name: _template
name: 'TEMPLATE — copy this file to <unique_name>.md and fill it in'
checked_by: []
data_foundry_status: []
suggestion:
decision_markers: []
tags: []
collections: []
original_source:
year:
domain:
required_split: []
problem_type:
original_data_state:
source_links: []
type_adapter_id: curation-record-v1
---

## Comments

How to fill a curation record. Copy this file to `curation/records/<unique_name>.md`
(snake_case, no leading underscore — files starting with `_` are ignored), set
`unique_name` + `name`, then fill the front-matter fields below. Empty fields are simply
omitted on save. Dropdown fields accept any value, but values outside the vocabulary
(`curation/vocabularies.yaml`) get flagged via `needs_review` — add new options through the
dashboard's ＋ header buttons rather than free-typing. Most curators edit records in the
dashboard (`data-foundry-curation serve`); this file is the by-hand reference.

Field-by-field:

- **unique_name** — stable id and file stem; `snake_case`, globally unique. This is the
  dataset's canonical name (prefer the shipped dataset/notebook name where one exists).
- **name** — human-readable name(s) the dataset is published under (join aliases with ` / `).
  This is the *single source of truth* for the name; the body has no `# title` heading.
- **checked_by** — people who reviewed it: `Lennart`, `Andrej`, `Mustafa`, `Alex`, `Gioia`,
  `AI (UNVERIFIED)`.
- **data_foundry_status** — the merged Data Foundry field. A multi-tag list combining
  *integration status* and *benchmark-collection membership*:
  - integration: `DF: Yes` (in Data Foundry), `DF: WIP`, `DF: Much work`, `DF: Suspended`.
  - collection: `TabArena (v0.1)`, `BeyondArena` — every shipped dataset carries its
    collection tag(s) **and** `DF: Yes`. Example: `[DF: Yes, BeyondArena]`.
  - `DF: …` with **no** collection tag is valid and intentional: the dataset is in Data Foundry
    but not in a shipped collection (it lives under `datasets/_maintenance/` — deprecated /
    suspended / out-of-scope — or `datasets/_dev/`). Don't add a collection tag to "fix" it.
    See `datasets/_maintenance/_deprecated/README.md`.
- **suggestion** — whether we'd include it: `Yes`, `No`, `TBD -> Yes`, `TBD -> 2nd Tier`,
  `Disagreement`, `Yes (Disagreement)`. (This is the one field that, left empty, flags the record
  for review.) `Yes (Disagreement)` = *shipped on purpose, but with an unresolved disagreement to
  re-evaluate* — it counts as accepted but shows under the ⚡ Disagreement filter. A dataset shipped
  in a collection must be `Yes` or `Yes (Disagreement)` (anything else is a `ship_conflict`).
- **decision_markers** — why / decision flags, e.g. `Duplicate`, `Trivial`, `Image`,
  `NLP (Text)`, `Out-of-scope Task (CTR/RecSys/Ranking)`, `Ethical Issue`, `Too Small`,
  `Data Quality Issue`, `Not Representative`, `TBD` (see vocab for the full list).
- **tags** — priority / shape tags, e.g. `New IID`, `Non-IID (Temporal)`,
  `Non-IID (Grouped)`, `Larger IID Data`, `Tiny Data`, `Many features`, `Multi-target`.
- **collections** — *external* benchmarks/collections the dataset appears in (NOT our own):
  `TabSTAR`, `CARTE/TARTE`, `TabRed`, `TableShift`, `TexTabBench`, `New (BeyondArena)`,
  `TabArena Reject`, … (our own membership lives in `data_foundry_status`).
- **original_source** — where the data was first shared: `OpenML`, `UCI`, `Kaggle`, `Zindi`,
  `GOV Website`, `Github`, `Company`, `Website`, `Other`, `?`.
- **year** — publication / collection year (free text; e.g. `2014` or `? (2014)`).
- **domain** — real-world application domain, e.g. `medical & healthcare`, `finance`,
  `business & marketing`, `industry & manufacturing`, `environmental science & climate`.
- **required_split** — appropriate evaluation protocol: `Random (IID)`, `Temporal (NON-IID)`,
  `Grouped (NON-IID)`, `Custom`, `?` (the split decides whether the task is IID or non-IID).
- **problem_type** — `Binary Classification`, `Multiclass Classification`, `Regression`,
  `Other`, `TBD`.
- **original_data_state** — shape of the raw data: `One Table`,
  `Database (or multiple to-be-joined tables)`, `Other`.
- **source_links** — download links / DOIs, one per line (OpenML id URL, Kaggle, DOI, UCI…).
  These double as the dataset's identity for de-duplication, so include the canonical ones.

Replace this section with the actual curation discussion: the reasoning behind the
suggestion and decision markers (curation is manual and human-verified).

## Reference

Academic reference / citation for the dataset (often BibTeX). Example:

@article{author2014dataset, title={...}, author={...}, year={2014}}
