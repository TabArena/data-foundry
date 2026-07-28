Create a new dataset curation notebook for the data-foundry project in the `datasets/beyond_iid/` folder.

## Input

The user has pasted tab-separated metadata from a spreadsheet. Parse the following columns (in order, separated by tabs — some fields may be empty):

1. **Checked by** — who reviewed it (ignore)
2. **Data Foundry** — internal flag (ignore)
3. **Suggestion** — yes/no (ignore)
4. **Decision Markers** — internal (ignore)
5. **New Tag** — e.g. "New IID", "Temporal", "Grouped"
6. **Name** — dataset name (human-readable)
7. **Source (and Link to download)** — URL to download the dataset
8. **Free Comments** — curation notes, may be multiline and quoted
9. **Original Source (Website)** — e.g. "Kaggle", "UCI", "OpenML"
10. **Source (Benchmark / Collection)** — e.g. "New - IST"
11. **Year** — publication year
12. **Context Domain** — e.g. "business & marketing", "medical & healthcare"
13. **Reference** — citation source or "Kaggle"
14. **Required split** — e.g. "Random (IID)", "Temporal", "Grouped"
15. **Problem Type** — e.g. "Regression", "Binary Classification", "Multiclass Classification"
16. **Usable Task Type** — (ignore)
17. **Given Task Type** — (ignore)
18. **Data Domain** — (ignore)
19. **Original Data State** — e.g. "One Table", "Multiple Tables"

**Metadata to parse:**

$ARGUMENTS

## Steps

### Step 1: Parse and map fields

**`unique_name`**: Convert "Name" (col 6) to snake_case — lowercase, replace spaces/hyphens/special chars with underscores, collapse multiple underscores, strip leading/trailing underscores.

**Determine target subfolder** from "New Tag" (col 5) + "Required split" (col 14):
- Contains "IID" or "Random" → `new_iid`
- Contains "Temporal" → `temporal`
- Contains "Grouped" → `grouped`
- Default → `new_iid`

**Map `domain_str`** (col 12) — must exactly match one of: `"education"`, `"environmental science & climate"`, `"biology & life sciences"`, `"handcrafted"`, `"chemistry & material science"`, `"industry & manufacturing"`, `"physics & astronomy"`, `"multimedia"`, `"medical & healthcare"`, `"technology & internet"`, `"finance"`, `"social science"`, `"business & marketing"`, `"insurance"`. If the input doesn't match, pick the closest match.

**Map `dataset_source`** (col 9) — must exactly match one of: `"Kaggle"`, `"OpenML"`, `"GitHub"`, `"UCI"`, `"HuggingFace"`, `"GOV Website"`, `"Customer"`, `"Other"`, `"ASlib"`.

**Map `data_tags`** (col 5):
- "New IID" or "IID" → `["IID"]`
- "Temporal" → `["Temporal"]`
- "Grouped" → `["Grouped"]`
- Otherwise → `["IID"]` (default)

**Map `problem_type`** (col 15):
- "Regression" → `"regression"`
- "Binary Classification" → `"binary_classification"`
- "Multiclass Classification" or "Classification" → `"multiclass_classification"`

**Map `objective_metric_name`** from problem_type:
- `"regression"` → `"rmse"`
- `"binary_classification"` → `"roc_auc"`
- `"multiclass_classification"` → `"log_loss"`

**Generate `download_description`** from the URL (col 7):
- If Kaggle dataset URL (contains `kaggle.com/datasets/`): extract the slug (e.g., `ruchi798/housing-prices-in-metropolitan-areas-of-india`) and generate:
  ```
  We download the data from Kaggle.

  kaggle datasets download <slug> && unzip <slug-last-part>.zip && rm <slug-last-part>.zip
  mkdir -p local-data-warehouse/<unique_name> && mv *.csv local-data-warehouse/<unique_name>/
  ```
- If Kaggle competition URL (contains `kaggle.com/competitions/`): extract competition name and use `kaggle competitions download -c <name>`
- Otherwise: generate a placeholder with `wget <url>`

**Generate `academic_reference_bibtex`**:
- If Reference (col 13) is "Kaggle" or dataset_source is "Kaggle", generate a `@misc` template:
  ```
  @misc{<bibtex_key>,
    author = {TODO},
    title = {<Name>},
    year = {<Year>},
    howpublished = {\url{<URL>}},
    note = {Kaggle dataset}
  }
  ```
  where `<bibtex_key>` is `Author<Year><FirstWordOfName>` format (use "TODO" for author part → `TODO<Year><word>`)
- Otherwise: leave as placeholder `@\n`

**Map task metadata fields** based on split type:
- IID: `stratify_on="TODO"` if classification else `None`; `time_on=None`; `group_on=None`
- Temporal: `time_on="TODO"`; `group_on=None`; and set `time_horizon` / `time_horizon_unit`
  on the `PredictiveMLSplitsMetadata` — a temporal task without a declared horizon is a
  bundle-check error
- Grouped: `group_on="TODO"`; `group_labels="per_group"`

### Step 2: Create the folder

Create directory: `datasets/beyond_iid/<subfolder>/<unique_name>/`

### Step 3: Write the notebook

Write a valid Jupyter notebook (nbformat 4, nbformat_minor 5) as `<unique_name>.ipynb` in the folder created above.

The notebook MUST be valid JSON with this exact structure. Use the template at `datasets/_template/_template.ipynb` as the base — read it first to get the exact JSON structure.

**Cell 1** (markdown): `### Dataset and Task Metadata`

**Cell 2** (code): The metadata definition cell. Populate ALL fields from the parsed metadata. For the `PredictiveMLTaskMetadata`:
- `target_column_name="TODO"`
- Only include the relevant optional fields (drop the `# For classification`, `# For time`, `# For grouped data` comment blocks that don't apply). For IID regression, the task_mold should be minimal like existing examples (just target, problem_type, objective_metric_name).

**Cell 3** (markdown): `## Preprocessing`

**Cell 4** (code): Data loading cell.
- Default: `df = pd.read_csv(dataset_mold.path / "TODO.csv")`
- If Free Comments mentions multiple specific CSV files (like `Bangalore.csv`, `Chennai.csv`, etc.), add a comment listing them and a TODO about merging:
  ```python
  # TODO: Dataset contains multiple files that should be merged:
  # Bangalore.csv, Chennai.csv, Delhi.csv, etc.
  # See curation_comments for details.
  dfs = []
  for f in ["Bangalore.csv", "Chennai.csv", ...]:  # TODO: verify filenames after download
      dfs.append(pd.read_csv(dataset_mold.path / f))
  df = pd.concat(dfs, ignore_index=True)
  ```
- Always end with `print("Loaded data shape:", df.shape)`

**Cell 5** (code): Display options + `df.head()` (identical to template)

**Cell 6** (markdown): `## Data Checks`

**Cell 7** (code): `run_all_checks()` call (identical to template)

**Cells 8-12** (code): Display check results — df_head, summary, numeric_stats, cat_stats, target_df (identical to template)

**Cell 13** (markdown): `## Task Curation`

**Cell 14** (code): `get_recommended_splits_dimensions()` call (identical to template)

**Cell 15** (code): Splits creation — **only include the relevant split type**:
- For IID: only the `get_recommended_iid_splits` call, with `splits_comment="Default splits for IID data."`
- For Grouped: only the `get_recommended_grouped_splits` call, with `show_splits=True` and `target_on=task_mold.target_column_name`, with `splits_comment="Default splits for grouped data."`
- For Temporal: only the manual splits dict placeholder with TODO comment, with `splits_comment="Default splits for temporal data."`

**Cell 16** (markdown): `## Bundle` (identical to template)

**Cell 17** (code): `CuratedContainer` construction + `describe()` (identical to template — do **not** save here)

**Cell 18** (markdown): `## Bundle Checks` (identical to template)

**Cell 19** (code): `run_bundle_checks(...)` + `report.raise_if_errors()` (identical to template).
Leave `ignore=[]` empty — the curator fills it in, with a reason per entry, once they have
seen which warnings apply.

**Cell 20** (markdown): `## Export` (identical to template)

**Cell 21** (code): `save()` + `verify_saved_container(...)` (identical to template)

### Step 4: Verify the scaffold

After writing the notebook, read it back and verify it is valid JSON by checking:
- All required cells are present (21 cells)
- The metadata fields are populated correctly
- The file path is correct

Report to the user:
- The path of the created notebook
- A summary of the populated metadata fields
- Any fields left as TODO that the user needs to fill in manually
- Any mapping decisions that were ambiguous

### Step 5: Hand off to `/verify-dataset`

Close the report by telling the user what happens next, in this order:

1. fill in the TODOs and run the notebook — the **Bundle Checks** cell fails loudly on any
   mechanical problem (missing columns, non-positional split indices, temporal leakage, a
   temporal task without a `time_horizon`, unparseable BibTeX, …);
2. once it runs clean, **run `/verify-dataset <path-to-notebook>`** for the second pass — the
   provenance / scope / split-regime / leakage-by-semantics judgment that the automated checks
   cannot make.

Say this explicitly, with the notebook path filled in, so the user can copy the command. Do **not**
run `/verify-dataset` yourself right after scaffolding: at that point the notebook is still full of
TODOs and there is no bundle to check. Its input is a *filled-in, executed* notebook.
