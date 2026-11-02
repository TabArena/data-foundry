# The curation dashboard

The dashboard is a local web page over the curation records ([records.md](records.md)): a filterable table that edits
the markdown files in place, plus the knowledge pages (the two knowledge skills rendered from their .md files, after a
"Start here" page).

## Running it

```bash
.venv/bin/python -m data_foundry.curation.cli serve            # http://127.0.0.1:8765
```

Use the repository's `.venv` (or `PYTHONPATH=src` with another Python): its editable install resolves both the code
and `curation/` to this checkout. The `data-foundry-curation` entry point of a non-editable install resolves the
curation root inside site-packages; set `DATA_FOUNDRY_CURATION_DIR=<repo>/curation` there. Start the server in the
background and point the curator at the URL (a hard refresh once if the tab was already open). The page polls the
server's change token every 2 s and patches its table in place, so records saved through the store API show up within
seconds, without losing scroll, filters or pins.

The server does not reload its own code: after an edit under `src/data_foundry/curation/` (Python or `static/`), stop
it and start it again. Stop it by its process id; never `pkill -f <pattern>` from an agent shell, whose own command
line contains the pattern (it killed the agent's shell twice on 2026-09-21):

```bash
for pid in $(ps -eo pid=,comm=,args= | awk '$2 ~ /^python/' | grep "curation.cli ser""ve" | awk '{print $1}'); do kill $pid; done
```

`.venv/bin/python -m data_foundry.curation.cli build-site <out>` writes a read-only static copy (published on GitHub
Pages from `main`); `export` writes a flat CSV, Parquet or XLSX snapshot. The dashboard runs locally per curator (edit,
commit, PR) and is not hardened for multi-user or public use.

## Features to point curators at

* Leftmost **status** cell encodes priority (⚡ disagreement = purple, ✓ in Data Foundry
  = green, 🤖 AI-reviewed-but-unverified = cyan, ✗ suggestion No = red, ★ accepted-not-yet-in-DF
  = blue, ⚠ needs review / untriaged = orange, • other = yellow; first match wins, so 🤖 shows
  even when the AI already filled a Yes/No suggestion, and a `DF: Yes` row shows ✓ whatever its
  verdict). Click the column to sort by it, or the funnel in its header to filter: each status
  cycles **✓ require, ✕ exclude, off**, so "hide everything rejected" is one click. A claimed row's
  status tooltip ends with "claimed by <name> (<stage>, until <date>)" and the claim's note.
* **Priority** (next to *Suggestion*) is the record's `priority`, 1 to 5 as a chip (the darker, the sooner a curator
  should act on the record: verify the screening, or review what `/add-dataset` added), set by `/screen-candidates`
  and again by `/add-dataset`; pick another value
  or *(none)* from the cell's list. Click the header to sort: records without a priority sort last in both directions.
  Its filter popover lists 1 to 5 and *(empty)*, so `#hf.priority=+5|+4` shows the two top priorities.
* **Claimed by** (next to *Data Foundry*) shows the live claims board ([claims.md](claims.md)), which the server
  fetches every 20 s; the 🔒 count in the bar says when, and the error if the fetch failed. Pick your own name in a
  cell to claim the dataset, empty the cell to release it (both push to the board and update the record). Its filter
  on *(empty)* (`#hf.claimed_by=+∅`) shows the datasets nobody works on; add your name for "free or mine"
  (`#hf.claimed_by=+∅|+<name>`). The server needs your name: `git config data-foundry.curator <Name>`.
* **Column filters combine with AND and NOT.** Every dropdown column's header has a filter
  button opening a popover that lists all its values (vocabulary ∪ values actually present ∪
  **(empty)**, each with a count; ⚠ marks a value missing from `vocabularies.yaml`). Clicking a
  value cycles **✓ require, ✕ exclude, off**. Multi-value columns carry a **match ALL ✓ /
  match ANY ✓** switch at the top of the popover: set it before (or after) ticking values, it
  persists per column for the session; ALL is the default, so `tags` ✓Non-IID (Temporal)
  ✓Review Prio 1 means both. On single-value columns ✓ values read as "any of". Different
  columns always AND together, so e.g. `BeyondArena` ✓ + `DF: Yes` ✕ is expressible.
  Free-text column filters and the top **search** box take the same query syntax: several
  terms must all match, `!word` excludes, `"quoted phrase"` keeps spaces.
* An amber **filter strip** under the top bar spells out every constraint in effect in words
  (`Tags: A AND B · NOT C`), with a ✕ per constraint and a ✕ Clear-all: read it instead of
  guessing why rows are missing.
* Top **pills** (Data Foundry / TabArena v0.1 / BeyondArena | Review / Screening / ⚡ Disagreement) are
  exclusive filters (clicking one resets the others) but layer on top of the status funnel , 
  pick a pill, then narrow by status. All three of **Data Foundry** / **TabArena v0.1** /
  **BeyondArena** read the merged `data_foundry_status` field: **Data Foundry** counts collection
  membership (TabArena ∪ BeyondArena = 144 shipped datasets), **TabArena v0.1** / **BeyondArena**
  the respective tag. **Review** surfaces *everything a curator still owns*: untriaged rows (⚠)
  **and** AI-reviewed-but-unverified rows (🤖); use the status funnel to see one group at a time.
  **Screening** is the queue `/screen-candidates` leaves for the curator: records with `AI (UNVERIFIED)` in
  `checked_by` and a suggestion that does not start with `No`. Switching it on sorts the table by priority, highest
  first (`#pill=scr`); switching it off restores the status order unless you re-sorted in between.
  The **search** box deliberately spans all datasets, overriding the pills / status / column
  filters while a term is present (the filter strip labels it *(all datasets)*).
* **📌 pin** (far-left column) keeps a row visible through any filter and sticks it to
  the top while scrolling. The same column links every row's **curation record (📄)** , 
  its `curation/records/<name>.md` on GitHub: and, for curated datasets, the
  **curation notebook (📓)** and the **v0.2 definition (🧩)**, read straight from the record's `notebook_path` and `v2_path`; on 🤖 rows it also
  holds the ✓ verify action.
* **🔗 Copy link** (appears next to **✕ Clear filters** whenever the view is filtered or sorted
  differently from the status order) copies a URL that reopens the exact current view: active pill,
  status constraints, search term, every column filter and the sort are encoded in the hash
  (`#pill=bey&status=+in-df|-no&hf.tags=mode=any|+New IID|-Tiny Data`,
  `#pill=scr&hf.priority=+5|+4&sort=priority:desc`). `sort=` takes any sortable column as `field:asc` or
  `field:desc` (several comma-separated); without it a link opens in the status order, or in its pill's order
  (`#pill=scr` sorts by priority). Opening such a link restores the view; this works on the live dashboard and
  the static GitHub Pages build alike (live-only states like the Review and Screening pills are ignored there), and
  links made before include/exclude existed still work (a bare value means "require"; a `+` typed by hand works too).
* Dropdown columns show a **▾** on hover and a **＋** in the header to add a new option;
  the **Optional Tags** column opens a panel for the less-common fields.
* **📖 Guidelines** opens the knowledge pages. The first entry, **Start here**, renders the map of the skills
  ([.claude/skills/README.md](../../README.md), served as `/docs/start/README.md`, copied by `build-site` to
  `docs/start/README.md`); without that file the entry is hidden. Its links to the knowledge skills open in the viewer,
  links to workflow skills and agents open on GitHub.

