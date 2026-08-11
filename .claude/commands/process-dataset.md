Process a decided candidate into a curated dataset: scaffold its curation notebook for the
data-foundry project in the `datasets/beyond_iid/` folder.

The dataset should already have been triaged (`/triage-candidates`) and come out a `Yes`; to check
the notebook once it is filled in and run, use `/verify-dataset`.

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

## The one rule that governs everything below

**You have not seen the data.** At scaffold time the raw files are usually not even
downloaded. So: **pre-fill structure, never facts.**

* Anything you can derive from the spreadsheet row or from a convention → fill it in.
* Anything that needs a look at the data → emit it as an *ordered, commented step* with a
  `# TODO(verify): …` marker saying what to check, in the cell where it belongs.
* Never invent a column name, a class label, a leak, or a horizon. `"TODO"` as a value is
  correct and safe; a plausible-looking guess is not.

TODO markers are enforced, not decorative: the notebook's Bundle Checks cell fails with
`meta_placeholder_left` while any `TODO` / `FIXME` remains in the metadata, so a
half-filled scaffold cannot be exported. Say so in your report.

## Steps

Read the reference sections **§B–§E at the end of this file first** — they are distilled from the
~155 shipped notebooks and Step 3 fills the notebook from them.

### Step 1: Parse and map fields

**`unique_name`**: Convert "Name" (col 6) to snake_case — lowercase, replace spaces/hyphens/special chars with underscores, collapse multiple underscores, strip leading/trailing underscores. (Enforced: `DatasetMetadata` rejects anything else.)

**Determine target subfolder** from "New Tag" (col 5) + "Required split" (col 14):
- Contains "IID" or "Random" → `new_iid`
- Contains "Temporal" → `temporal`
- Contains "Grouped" → `grouped`
- Default → `new_iid`

**Map `domain_str`** (col 12) — must exactly match one of: `"education"`, `"environmental science & climate"`, `"biology & life sciences"`, `"handcrafted"`, `"chemistry & material science"`, `"industry & manufacturing"`, `"physics & astronomy"`, `"multimedia"`, `"medical & healthcare"`, `"technology & internet"`, `"finance"`, `"social science"`, `"business & marketing"`, `"insurance"`. If the input doesn't match, pick the closest match.

**Map `dataset_source`** (col 9) — must exactly match one of: `"Kaggle"`, `"Zindi"`, `"OpenML"`, `"GitHub"`, `"UCI"`, `"HuggingFace"`, `"GOV Website"`, `"Customer"`, `"Other"`, `"ASlib"`. This is where the data *first appeared*, which is often not the link you were given.

**Map `data_tags`** (col 5) — the regime tag must agree with the task fields you set, or the
bundle check `meta_tags_*` fires:
- IID → `["IID"]`
- Temporal → `["Non-IID", "Temporal"]`
- Grouped → `["Non-IID", "Grouped"]`
- Add `"Anonymized"` when feature names/values carry no semantics (common for Kaggle competition data).
- Add `"Spatial"` when the data holds geographic information (ZIP, lat/long, region, store location).
- Add `"ForcedIIDFromTemporal"` (with `IID`) when the task is temporal in nature but the
  time index was never shipped — do **not** just tag `IID` and move on.
- Only ever one of `Temporal` / `Grouped` / `GroupedTemporal`.

**Map `problem_type`** (col 15):
- "Regression" → `"regression"`
- "Binary Classification" → `"binary_classification"`
- "Multiclass Classification" or "Classification" → `"multiclass_classification"`

**Map `objective_metric_name`** from problem_type (these are the three the collection uses;
anything else is a deliberate custom metric that must be registered downstream):
- `"regression"` → `"rmse"`
- `"binary_classification"` → `"roc_auc"`
- `"multiclass_classification"` → `"log_loss"`

If the source is a competition with its own metric, keep our default and note the original
metric in `curation_comments` — do not silently invent a metric name.

**Generate `download_description`** from the URL (col 7):
- If Kaggle dataset URL (contains `kaggle.com/datasets/`): extract the slug (e.g., `ruchi798/housing-prices-in-metropolitan-areas-of-india`) and generate:
  ```
  We download the data from Kaggle.

  kaggle datasets download <slug> && unzip <slug-last-part>.zip && rm <slug-last-part>.zip
  mkdir -p local-data-warehouse/<unique_name> && mv *.csv local-data-warehouse/<unique_name>/
  ```
- If Kaggle competition URL (contains `kaggle.com/competitions/`): extract competition name and use `kaggle competitions download -c <name>`
- Otherwise: generate a placeholder with `wget <url>`

**Generate `academic_reference_bibtex`** — cite the work that *published the data* (paper,
competition, institution), not a paper that merely used it:
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
- **Balance every brace** and escape `&`, `%`, `#`, `_` in typeset fields (`\&`, …). Four shipped
  datasets have broken BibTeX — two that will not compile, two whose declared key does not match
  the entry; the bundle check now catches all four kinds.
- `academic_reference_bibtex_key` must list every entry key, comma-separated.

**Map task metadata fields** based on split type:
- IID: `stratify_on` = the same literal string as `target_column_name` for classification, `None` for regression; `time_on=None`; `group_on=None`
- Temporal: `time_on="TODO"`; `group_on=None`; **and** set `time_horizon` / `time_horizon_unit`
  on `PredictiveMLSplitsMetadata` — a temporal task without a declared horizon is a bundle-check error
- Grouped: `group_on="TODO"`; `group_labels="per_group"` if one label per group, `"per_sample"`
  if each row has its own label (see §C); never both `group_on` and `time_on`

**Seed `curation_comments`** in the house format — one opening line naming the exact starting
artifact, then `-` bullets. Pre-fill the bullets you know and leave TODO bullets for the rest:

```
We start with <file> from <source>.

- TODO(verify): what was dropped and why (identifiers, leaking features, constant columns).
- TODO(verify): dtype decisions (which columns are category / string / datetime).
- TODO(verify): duplicate-row decision (dropped as a collection artifact, or kept as natural).
- Anomaly: <anything odd that we deliberately did not fix>
- Note: <a decision a reviewer would otherwise question>
```

`Anomaly:` and `Note:` are established prefixes across the shipped notebooks — use them.
Comments are the audit trail: **every non-obvious line of preprocessing code needs a bullet,
and every bullet needs code.** `/verify-dataset` checks exactly that correspondence.

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

**Cell 4** (code): Data loading **plus the ordered preprocessing skeleton from §B**.
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
- Then the §B steps as commented stubs in order, each with its `# TODO(verify):` marker.
- Always end with `print("Loaded data shape:", df.shape)`

**Cell 5** (code): Display options + `df.head()` (identical to template)

**Cell 6** (markdown): `## Data Checks`

**Cell 7** (code): `run_all_checks()` call (identical to template)

**Cells 8-12** (code): Display check results — df_head, summary, numeric_stats, cat_stats, target_df (identical to template)

**Cell 13** (markdown): `## Task Curation`

**Cell 14** (code): `get_recommended_splits_dimensions()` call (identical to template). For a
temporal task, call it **without** `time_on` — passing it raises, since the horizon is a human
judgment (see §C) — and keep the result only as a reference for how many splits to aim for.

**Cell 15** (code): Splits creation — **only the relevant regime's recipe from §C**, with a
`splits_comment` that states what deployment scenario the split simulates.

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
- **Every `TODO(verify)` marker you left, grouped by cell**, so the curator has the work list
- Any mapping decisions that were ambiguous
- Which §D traps you flagged as plausible for *this* dataset, and why

### Step 5: Hand off to `/verify-dataset`

Close the report by telling the user what happens next, in this order:

1. fill in the TODOs and run the notebook — the **Bundle Checks** cell fails loudly on any
   mechanical problem (missing columns, non-positional split indices, temporal leakage, a
   temporal task without a `time_horizon`, unparseable BibTeX, leftover TODO markers, …);
2. once it runs clean, **run `/verify-dataset <path-to-notebook>`** for the second pass — the
   provenance / scope / split-regime / leakage-by-semantics judgment that the automated checks
   cannot make.

Say this explicitly, with the notebook path filled in, so the user can copy the command. Do **not**
run `/verify-dataset` yourself right after scaffolding: at that point the notebook is still full of
TODOs and there is no bundle to check. Its input is a *filled-in, executed* notebook.

---

# Reference: what the shipped notebooks do

Distilled from the ~155 curation notebooks under `datasets/beyond_iid/`. §B and §C are what to
*write*; §D is what to *flag*; §E maps each automated check to the action that pre-empts it.

## §B The preprocessing recipe

The order below is what the ~155 notebooks under `datasets/beyond_iid/` converge on. Emit the
steps that plausibly apply as commented stubs with TODO markers; drop the ones the source clearly
doesn't need.

```python
# 1. Load (+ merge multiple tables on their key, following the source's own joins).
# 2. Rename columns / the target to semantically meaningful names; fix typos and strip
#    special characters. Binary targets get readable labels:
#       df[target] = df[target].map({1: "Yes", 0: "No"})
# 3. TODO(verify): drop uninformative identifiers (ID, index, row id, booking_id, …).
#    Keep an identifier only if it carries real signal (a time index, a group id) — and then
#    process it into that meaning.
# 4. TODO(verify): reverse ordinal / one-hot encodings and restore the semantic labels
#    (very common for UCI releases: `df[col].map({...})`).
# 5. TODO(verify): convert proxy missing values to real NaN:
#       df = df.replace({"?": np.nan, " ": np.nan})     # UCI style
#       df[col] = df[col].replace(-1, np.nan)           # sentinel style (-1, -9, -999, 999999)
# 6. Set dtypes by meaning, not by convenience:
#       cat_features = [...]                            # fixed, finite value set
#       df[cat_features] = df[cat_features].astype("category")
#       df[text_features] = df[text_features].astype("string")   # free text / high cardinality
#       df[date_col] = pd.to_datetime(df[date_col])              # YYYY-MM-DD
#    Everything else numeric. No `object` columns may survive (bundle check + TabArena reject).
# 7. TODO(verify): drop constant columns, all-missing columns, and duplicated columns.
# 8. TODO(verify): drop leaking features — see §D.1. This is the single most common
#    preprocessing step in the collection.
# 9. TODO(verify): duplicate rows — decide and document (§D.4).
# 10. TODO(verify): target transform — log/log1p a skewed positive target (prices, durations,
#     counts): `df[target] = np.log(df[target])` / `np.log1p(...)`. Rename the column when you
#     do (e.g. `log_days_to_death`). Skip it if the source already log-scaled the target.
# 11. TODO(verify): drop implausible rows (data errors) and censored/capped target values.
# 12. Fix the row order:
#     IID + grouped: df = df.sample(frac=1, random_state=42).reset_index(drop=True)
#     temporal:      df = df.sort_values(time_on).reset_index(drop=True)
# 13. df = df.reset_index(drop=True)   # splits are positional — this must be the last word
```

After dropping rows, `category` columns keep their old levels — add
`df[col] = df[col].cat.remove_unused_categories()` (bundle check `dataset_unused_categories`).

Do **not**: geocode spatial columns, hand-engineer text features, one-hot encode, impute, or
scale features. Leave that to the pipeline. Feature engineering is only for *removing leaks*
with minimal information loss, or for reconstructing meaning the source destroyed.

## §C Split recipes

### IID
Template's `get_recommended_splits_dimensions` + `get_recommended_iid_splits`, with
`stratify_on` = the target for classification. `splits_comment="Default splits for IID data."`

### Grouped
Template's `get_recommended_grouped_splits` with `show_splits=True` and
`target_on=task_mold.target_column_name` — always keep the printed per-fold group/target
balance in the committed output; that table is what reviewers read.

`group_labels`: `"per_group"` when every row of a group shares one label (one label per
customer/patient/area), `"per_sample"` when each row has its own label (a per-timestep
measurement, a per-transaction outcome). Getting this wrong is a bundle-check error
(`task_group_labels_per_group_violated`), and it changes the recommended split sizes.

`splits_comment` should say what the split simulates and how big a test fold is in *groups*,
e.g. "We create stratified grouped 20-repeated 3-fold splits. This creates ca. 50 patients
(ca. 120-150 samples) per test set — simulating a model fit once and deployed for new patients."

### Temporal — the manual one
`get_recommended_splits_dimensions` **raises** when you pass `time_on`: the horizon is a human
judgment, not a row-count rule. Derive it from the source ("managers predict sales up to six
weeks in advance", "companies have 180 days to respond", the competition's own test window, the
refit cadence) and record that reasoning in `splits_comment`. Several temporal notebooks still
call the helper *without* `time_on`, purely to see how many splits an IID dataset of this size
would get — that is fine as a reference point.

The shipped convention:

* **one repeat per time window, always fold `0`** — `splits[window] = {0: (train_idx, test_idx)}`
  (checked: `splits_temporal_layout` reports any other layout)
* **split 0 is the most recent window**, the rest ordered by descending test time — most
  training data, most representative (checked: `splits_temporal_order`)
* **expanding train**: everything strictly before the test window, minus a planning gap if the
  application has one (checked: `splits_temporal_leakage`)
* keep **≥50% of rows (or dates) in the smallest split's train set** — stop walking back
  otherwise (not checked; your judgment)
* set `time_horizon` + `time_horizon_unit`; use `"steps"` when the time index is numeric
  rather than a date (checked: `meta_time_horizon_missing`, `meta_time_horizon_mismatch`)

```python
from data_foundry.schema import PredictiveMLSplitsMetadata

date_col = task_mold.time_on
target_col = task_mold.target_column_name
df = df.sort_values(by=date_col).reset_index(drop=True)

test_window = pd.DateOffset(days=7)   # TODO(verify): the horizon the application implies
planning_gap = pd.DateOffset(days=0)  # TODO(verify): lag between prediction point and test window
n_windows = 3                         # TODO(verify): as many as keep >=50% of data in train

splits = {}
used_in_train, used_in_test = set(), set()
# Half-open windows [test_start, test_end) so consecutive windows can never overlap;
# bump past the last observation so it is included.
test_end = df[date_col].max() + pd.Timedelta(days=1)

for window in range(n_windows):
    test_start = test_end - test_window
    pred_point = test_start - planning_gap

    train_idx = df.index[df[date_col] < pred_point].tolist()
    test_idx = df.index[(df[date_col] >= test_start) & (df[date_col] < test_end)].tolist()

    assert set(train_idx).isdisjoint(test_idx), "Train and test indices overlap!"
    assert df[date_col].iloc[train_idx].max() < df[date_col].iloc[test_idx].min(), "Temporal leak!"

    splits[window] = {0: (train_idx, test_idx)}
    used_in_train.update(train_idx)
    used_in_test.update(test_idx)

    print(f"\n=== Window {window} ===")
    print("Train size:", len(train_idx), "| Test size:", len(test_idx))
    print("Test range:", test_start, "->", test_end)
    print("Train target mean:", df.loc[train_idx, target_col].mean())
    print("Test target mean:", df.loc[test_idx, target_col].mean())

    test_end = test_start  # walk the window backwards

print(f"{len(used_in_train | used_in_test) / len(df):.4f} of the samples are used.")
print(f"{len(used_in_train) / len(df):.4f} in training, {len(used_in_test) / len(df):.4f} in testing.")

splits_mold = PredictiveMLSplitsMetadata(
    splits_comment="TODO(verify): what deployment scenario this simulates and why this horizon.",
    splits=splits,
    time_horizon=7,          # TODO(verify): must match the window above
    time_horizon_unit="days",
)
```

For a target-mean printout on a classification task use
`df.loc[idx, target_col].value_counts(normalize=True)` instead of `.mean()`.

Variants that are also in use: an explicit list of test months/years (when per-day data is too
sparse for a robust test set); `sklearn.model_selection.TimeSeriesSplit` when only a row-order
time index exists (`time_horizon_unit="steps"`); a sliding window with `step < window` when
data is scarce (consecutive test windows may then overlap — that is allowed *across* repeats).

### Datasets above ~1.25M rows
Ship a second, subsampled version as its own notebook: `unique_name="<name>_1m"`,
`version_from_unique_name="<name>"`, a `version_comment`, and a single train/test split. For
temporal data use `curation_recommendations.subsample_temporal(df=..., train_idx=..., test_idx=...,
stratify_on=...)` after computing the split; it returns a reduced frame with rebuilt indices
(and legitimately leaves the frame unsorted in time — the `task_time_on_not_sorted` warning is
expected there).

## §D Recurring traps — what to pre-flag

These are the mistakes the collection actually had to fix. Turn each applicable one into a
`# TODO(verify):` marker in the notebook, and a bullet in `curation_comments`.

**1. Target-component leakage.** A feature that is part of, derived from, or a consequence of
the target: sub-scores that add up to the target, an alternative encoding of the outcome,
weight/height when the target is body mass, grades G1/G2 when the target is the final grade,
a "current status" column, award notes inside a description field. Also: a feature that is the
output of a *supervised* transform fit on the whole dataset (discriminant score, target
encoding, a model's own prediction) — that leak is irreversible and excludes the dataset.
→ TODO marker: *"list every feature that is a component/consequence of the target and drop it."*

**2. Not available at prediction time.** Especially for temporal tasks: fields recorded after
the prediction point (call duration, reservation status, number of customers that day, post-outcome
scrape fields, post-election survey answers). Ask "would this value have existed at time *t*?"
→ TODO marker per suspicious column.

**3. Entity duplicates across splits.** The same patient / house / molecule / object appearing
in several rows leaks the target between train and test even when the rows differ. The shipped
fix is either "keep the first row per entity" or "make it a grouped task".
→ TODO marker: *"check for repeated entities (patient_nbr, address, obj_ID, hospital number)."*

**4. Duplicate rows — decide, don't ignore.** The rule the curators apply: many
degrees of freedom + exact match → a collection artifact, drop it (and say the %); few features
and plausible repeats → natural, keep it (and say so). Duplicates with *conflicting* targets are
usually dropped unless they represent genuine label ambiguity. Shipped datasets range from 0% to
98% duplicates, so this is always worth a bullet.

**5. Row order carries signal.** Data sorted by target, by price, by location, or by collection
batch produces a fake distribution shift and lets models exploit position. Always shuffle IID and
grouped data with a fixed seed; the bundle check `dataset_row_order_leaks_target` catches what you
forget.

**6. Censored / capped targets.** A target clipped at a maximum (house price 500001, a runtime
timeout) punishes extrapolation. Either drop the censored rows or document the censoring.

**7. Proxy missing values.** `"?"`, `" "`, `"na"`, `"NULL"`, `-1`, `-9`, `-999`, `999999`,
`365243` and friends. Convert them when the encoding can be inferred from the data description;
keep them (and say why) when they carry meaning, e.g. "not previously contacted".

**8. Rare classes.** Classes with <10 samples get dropped in the shipped notebooks — they break
stratification and leave folds whose test set holds an unseen class (`splits_test_class_unseen_in_train`).
Merging label groups into a coarser, meaningful taxonomy is also accepted; document the mapping.

**9. Trust the source's split protocol as a claim, not a fact.** Published splits are often
leaking (a random split on temporal data). Conversely, a benchmark's non-IID label may be wrong
for our framing. Decide from the *application*, and record the argument in `curation_comments` —
several shipped datasets deliberately diverge from TabRed/the original paper in both directions.

**10. Copy top solutions' preprocessing, not their exploits.** Kaggle write-ups are the best
source for what preprocessing is legitimate. Do not copy steps that exploit a test-set leak, a
metric quirk, or competition-specific hacking.

**11. Anonymized data.** When features have no semantics you cannot infer dtypes or missing-value
encodings — keep the data as-is, tag `Anonymized`, and say what you could not determine.

**12. Reconstruct destroyed meaning.** Ordinal-encoded categories, one-hot blocks, dates split
across three columns, IDs that encode a group and a session — the shipped notebooks reverse these.
It is the one kind of feature engineering that is always welcome.

## §E Bundle check → what to do in the scaffold

The notebook's Bundle Checks cell will run these. Pre-empt them:

| Check slug | Scaffold action |
|---|---|
| `dataset_index_range` | `reset_index(drop=True)` as the last preprocessing step, before building splits |
| `dataset_object_dtype` | cast every non-numeric column to `category` / `string` / datetime |
| `dataset_identifier_column` | drop uninformative identifiers (§B.3) |
| `dataset_constant_column`, `dataset_all_missing_column`, `dataset_duplicate_columns` | drop them (§B.7) |
| `dataset_feature_equals_target` | drop target components (§D.1) |
| `dataset_missing_value_sentinel`, `dataset_missing_value_label` | convert proxy missing values (§B.5) |
| `dataset_unused_categories` | `cat.remove_unused_categories()` after row filtering |
| `dataset_row_order_leaks_target` | shuffle IID/grouped data (§B.12) |
| `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` | decide + document (§D.4) |
| `task_target_dtype`, `task_target_class_count` | classification target must be `category` with the right class count |
| `task_target_missing_values` | drop rows with a missing target |
| `task_target_rare_class`, `splits_test_class_unseen_in_train` | drop/merge classes with <10 samples (§D.8) |
| `task_metric_empty`, `task_metric_problem_type_mismatch` | use the per-problem-type default metric |
| `task_stratify_*` | stratify on the target (classification) or a discrete feature |
| `task_time_on_dtype`, `task_time_on_missing_values`, `task_time_on_not_sorted` | datetime/numeric time column, no NaN, sorted ascending |
| `task_group_labels_per_group_violated`, `task_group_on_unique_per_row` | pick `per_group` vs `per_sample` correctly (§C) |
| `splits_temporal_leakage`, `splits_temporal_order` | expanding train, newest window first (§C) |
| `splits_rows_unused` | IID/grouped splits must cover every row |
| `meta_time_horizon_missing` | always set `time_horizon` + unit for temporal tasks |
| `meta_tags_*` | tags must agree with the split regime (Step 1) |
| `meta_bibtex_*` | balanced braces, keys defined, `&`/`%`/`_` escaped |
| `meta_placeholder_left` | every TODO must be resolved before export |
| `meta_license_unknown`, `meta_source_link`, `meta_splits_comment_empty` | fill license, a real URL/DOI, and a substantive splits comment |
