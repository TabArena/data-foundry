# Dashboard features

What to point curators at in the dashboard.

* Leftmost **status** cell encodes priority (⚡ disagreement = purple, ✓ in Data Foundry
  = green, 🤖 AI-reviewed-but-unverified = cyan, ✗ suggestion No = red, ★ accepted-not-yet-in-DF
  = blue, ⚠ needs review / untriaged = orange, • other = yellow; first match wins, so 🤖 shows
  even when the AI already filled a Yes/No suggestion, and a `DF: Yes` row shows ✓ whatever its
  verdict). Click the column to sort by it, or the funnel in its header to filter: each status
  cycles **✓ require → ✕ exclude → off**, so "hide everything rejected" is one click.
* **Column filters combine with AND and NOT.** Every dropdown column's header has a filter
  button opening a popover that lists all its values (vocabulary ∪ values actually present ∪
  **(empty)**, each with a count; ⚠ marks a value missing from `vocabularies.yaml`). Clicking a
  value cycles **✓ require → ✕ exclude → off**. Multi-value columns carry a **match ALL ✓ /
  match ANY ✓** switch at the top of the popover — set it before (or after) ticking values, it
  persists per column for the session; ALL is the default, so `tags` ✓Non-IID (Temporal)
  ✓Review Prio 1 means both. On single-value columns ✓ values read as "any of". Different
  columns always AND together, so e.g. `BeyondArena` ✓ + `DF: Yes` ✕ is expressible.
  Free-text column filters and the top **search** box take the same query syntax: several
  terms must all match, `!word` excludes, `"quoted phrase"` keeps spaces.
* An amber **filter strip** under the top bar spells out every constraint in effect in words
  (`Tags: A AND B · NOT C`), with a ✕ per constraint and a ✕ Clear-all — read it instead of
  guessing why rows are missing.
* Top **pills** (Data Foundry / TabArena v0.1 / BeyondArena | Review / ⚡ Disagreement) are
  exclusive filters (clicking one resets the others) but layer on top of the status funnel —
  pick a pill, then narrow by status. All three of **Data Foundry** / **TabArena v0.1** /
  **BeyondArena** read the merged `data_foundry_status` field: **Data Foundry** counts collection
  membership (TabArena ∪ BeyondArena = 144 shipped datasets), **TabArena v0.1** / **BeyondArena**
  the respective tag. **Review** surfaces *everything a curator still owns* — untriaged rows (⚠)
  **and** AI-reviewed-but-unverified rows (🤖); use the status funnel to see one group at a time.
  The **search** box deliberately spans all datasets, overriding the pills / status / column
  filters while a term is present (the filter strip labels it *(all datasets)*).
* **📌 pin** (far-left column) keeps a row visible through any filter and sticks it to
  the top while scrolling. The same column links every row's **curation record (📄)** —
  its `curation/records/<name>.md` on GitHub — and, for curated datasets, the
  **curation notebook (📓)** and the **v0.2 definition (🧩)**, read straight from the record's `notebook_path` and `v2_path`; on 🤖 rows it also
  holds the ✓ verify action.
* **🔗 Copy link** (appears next to **✕ Clear filters** whenever the view is filtered)
  copies a URL that reopens the exact current view — active pill, status constraints, search
  term, and every column filter are encoded in the hash
  (`#pill=bey&status=+in-df|-no&hf.tags=mode=any|+New IID|-Tiny Data`). Opening such a link
  restores the view; this works on the live dashboard and the static GitHub Pages build alike
  (live-only states like the Review pill are ignored there), and links made before
  include/exclude existed still work (a bare value means "require").
* Dropdown columns show a **▾** on hover and a **＋** in the header to add a new option;
  the **Optional Tags** column opens a panel for the less-common fields.

