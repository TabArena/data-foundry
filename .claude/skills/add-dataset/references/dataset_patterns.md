# Dataset patterns for the `add-dataset` skill

Reference for writing a v2 `dataset.py`, distilled from the ~155 curation notebooks shipped under
`datasets/beyond_iid/` (formerly the reference sections of `/process-dataset`). §A maps the curation record to
the attributes; §B and §C are what to *write*; §D is what to *flag*; §E maps each automated check to the action
that pre-empts it; §F shows how to record decisions with their evidence.

Coming from a v1 notebook: `dataset_mold` / `task_mold` fields are flat class attributes (inside methods,
`self.dataset_metadata` / `self.task_metadata` hold the built objects), `dataset_mold.path` is the `raw_dir`
argument, the preprocessing cell is `_load_raw` (reading) + `_clean` (the rest, including column drops), the
dtype casts are `_feature_types`, the final shuffle is the base class's, the split cell is `temporal_splits` or `_make_splits`, and `ignore=[...]`
is `accepted_check_warnings`.

## The definition file

```python
"""Curated dataset definition for `<unique_name>` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TemporalSplits, drop_columns


class MyDataset(AbstractCuratedDataset):
    # Dataset (§A)
    unique_name = "my_dataset"
    year = "2024"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://..."
    license = "CC BY 4.0"
    data_tags = ("Spatial",)            # context tags only; regime tags are added from the task
    download_description = """
        kaggle datasets download ... && unzip ...
    """                                  # indented like code: dedented by the base class
    bibtex = """
        @misc{key2024,
          ...
        }
    """                                  # the key is parsed from the entry
    curation_comments = """
        We start with <file> from <source>.

        - ...
    """

    # Task
    target = "y"
    problem_type = "binary_classification"   # metric -> roc_auc, stratify_on -> target by default
    time_on = "date"                          # temporal only

    # Splits (§C)
    temporal_splits = TemporalSplits(window=7, unit="days", n_windows=3)
    splits_comment = """
        A model refit weekly ...
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:      # required: reading only, cached
        return pd.read_csv(raw_dir / "data.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:      # optional: §B
        df = raw
        ...
        return drop_columns(df, ["id"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:  # dtypes of the cleaned frame
        return FeatureTypes(
            categorical=["colour"],                # the classification target is added automatically
            string=["description"],
            datetime={"date": "%Y-%m-%d"},         # or a list of names (format inferred)
        )

    def _decisions(self, raw, df) -> list[Decision]:           # optional: §F
        ...
```

Other hooks: `_make_splits(df)` for splits the declarations cannot express (return a `SplitPlan`),
`_prepare_raw_files(raw_dir)` with `prepared_raw_files = (...)` for a heavy one-off step that writes intermediate
files into the raw directory, `_extra_checks(container)` for dataset-specific bundle checks (for example a leak test
from an audit).

The class is validated when `dataset.py` is imported: the required attributes are present and the metadata
validates, `unique_name` equals the folder name, every accepted warning has a reason, a temporal task has
`temporal_splits` or `_make_splits` and a horizon, `subsample_to_budget` needs `version_of`, a version needs a
`version_comment`, `prepared_raw_files` needs `_prepare_raw_files`, and the benchmark seeds are not overridden.

Keep `print` diagnostics out of the definition: `report.md` already records split sizes and time ranges, and
`explore.ipynb` or `_decisions` is the place for evidence. Keep `assert`s that guard custom logic. Run
`ruff check --fix` and `ruff format` on the file: they fix quoting (always double quotes) and import order.

## §A Field mapping (curation record → metadata)

**`unique_name`**: Convert "Name" (the record's `name`) to snake_case — lowercase, replace spaces/hyphens/special chars with underscores, collapse multiple underscores, strip leading/trailing underscores. (Enforced: `DatasetMetadata` rejects anything else.)


**Map `domain`** (record `domain`) — must exactly match one of: `"education"`, `"environmental science & climate"`, `"biology & life sciences"`, `"handcrafted"`, `"chemistry & material science"`, `"industry & manufacturing"`, `"physics & astronomy"`, `"multimedia"`, `"medical & healthcare"`, `"technology & internet"`, `"finance"`, `"social science"`, `"business & marketing"`, `"insurance"`. If the input doesn't match, pick the closest match.

**Map `source`** (record `original_source`) — must exactly match one of: `"Kaggle"`, `"Zindi"`, `"OpenML"`, `"GitHub"`, `"UCI"`, `"HuggingFace"`, `"GOV Website"`, `"Customer"`, `"Other"`, `"ASlib"`. This is where the data *first appeared*, which is often not the link you were given.

**Map `data_tags`** (record `required_split` / tags) — the regime tag must agree with the task fields you set, or the
bundle check `meta_tags_*` fires:
- IID → `["IID"]`
- Temporal → `["Non-IID", "Temporal"]`
- Grouped → `["Non-IID", "Grouped"]`
- Add `"Anonymized"` when feature names/values carry no semantics (common for Kaggle competition data).
- Add `"Spatial"` when the data holds geographic information (ZIP, lat/long, region, store location).
- Add `"ForcedIIDFromTemporal"` (with `IID`) when the task is temporal in nature but the
  time index was never shipped — do **not** just tag `IID` and move on.
- Only ever one of `Temporal` / `Grouped` / `GroupedTemporal`.

**Map `problem_type`** (record `problem_type`):
- "Regression" → `"regression"`
- "Binary Classification" → `"binary_classification"`
- "Multiclass Classification" or "Classification" → `"multiclass_classification"`

Some candidates carry *two possible* problem types — the same table supports either a
regression target or a classification one, and taking one means dropping the other as a
leaking feature. `pva_revenue_prediction_kddcup98` is the example: `TARGET_D` (donation
amount) and `TARGET_B` (did they donate at all) are two framings of one signal, so the
regression run drops `TARGET_B` and the classification run drops `TARGET_D`. The problem type
is then a property of the task we choose, not of the dataset, so the record's `problem_type`
cannot be read off the row: pick one target per dataset folder, and make the record match
whichever run ends up shipping. This is **not** `Multi-target` — that tag is for targets
predicted at once (distinct quantities modelled jointly). The second framing is its own folder
and class, `<unique_name>_clf/` (or `_reg/`), with its own `unique_name`.

**`metric`** defaults from `problem_type`; leave it unset for these three (the collection's standard).
Anything else is a deliberate custom metric that must be registered downstream; use the canonical short
spelling (`mae`, `rmsle`, `mape`, ...), the bundle check `task_metric_not_canonical` rejects aliases:
- `"regression"` → `"rmse"`
- `"binary_classification"` → `"roc_auc"`
- `"multiclass_classification"` → `"log_loss"`

If the source is a competition with its own metric, keep our default and note the original
metric in `curation_comments` — do not silently invent a metric name.

**Generate `download_description`** from the URL (the record's first `source_links` entry):
- If Kaggle dataset URL (contains `kaggle.com/datasets/`): extract the slug (e.g., `ruchi798/housing-prices-in-metropolitan-areas-of-india`) and generate:
  ```
  We download the data from Kaggle.

  kaggle datasets download <slug> && unzip <slug-last-part>.zip && rm <slug-last-part>.zip
  mkdir -p local-data-warehouse/<unique_name> && mv *.csv local-data-warehouse/<unique_name>/
  ```
- If Kaggle competition URL (contains `kaggle.com/competitions/`): extract competition name and use `kaggle competitions download -c <name>`
- Otherwise: generate a placeholder with `wget <url>`

**Generate `bibtex`** — cite the work that *published the data* (paper,
competition, institution), not a paper that merely used it:
- If Reference (record `reference`) is "Kaggle" or dataset_source is "Kaggle", generate a `@misc` template:
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
- The key is parsed from the entry; set `bibtex_key` only when it must differ.

**Map the task attributes** by split type:
- IID: nothing beyond `target` and `problem_type` (stratifying on a classification target is the default; set
  `stratify_on = None` to switch it off, with a reason).
- Temporal: `time_on = "TODO"` and `temporal_splits` (§C). A calendar window gives the horizon; otherwise set
  `time_horizon` / `time_horizon_unit`. A temporal task without a horizon does not import.
- Grouped: `group_on = "TODO"`; `group_labels = "per_group"` if one label per group, `"per_sample"` if each row
  has its own label (see §C); never both `group_on` and `time_on`.

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

## §B The preprocessing recipe (the body of `_clean`)

The order below is what the ~155 notebooks under `datasets/beyond_iid/` converge on. Emit the
steps that plausibly apply as commented stubs with TODO markers; drop the ones the source clearly
doesn't need.

```python
# 1. Load (+ merge multiple tables on their key, following the source's own joins).
# 2. Rename columns / the target to semantically meaningful names; fix typos and strip
#    special characters. Binary targets get readable labels:
#       df[target] = df[target].map({1: "Yes", 0: "No"})
# 3. TODO(verify): drop uninformative identifiers (ID, index, row id, booking_id, …). To keep an id but hide
#    its names (a group id), use `anonymize_ids(df[col])`, never random ids: `uuid4()` changes the data on
#    every run (`definition_nondeterministic`).
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
# 12. The row order and the index are the base class's job: a stable sort by `time_on` for temporal
#     tasks, else a shuffle with seed 42, then `reset_index`. Do not shuffle or sort in `_clean`.
```

After dropping rows, `category` columns keep their old levels — add
`df[col] = df[col].cat.remove_unused_categories()` (bundle check `dataset_unused_categories`).

Do **not**: geocode spatial columns, hand-engineer text features, one-hot encode, impute, or
scale features. Leave that to the pipeline. Feature engineering is only for *removing leaks*
with minimal information loss, or for reconstructing meaning the source destroyed.

## §C Split recipes

### IID and grouped
Keep the default: no split attributes at all. The base class calls `get_recommended_splits_dimensions` and
`get_recommended_iid_splits` / `get_recommended_grouped_splits` with the benchmark seed, and the comment is
"Default splits.". Set `splits_comment` only when there is something to say (a split that deliberately differs
from the source's protocol, what a grouped test fold holds).

`group_labels`: `"per_group"` when every row of a group shares one label (one label per customer/patient/area),
`"per_sample"` when each row has its own label (a per-timestep measurement, a per-transaction outcome). Getting this
wrong is a bundle-check error (`task_group_labels_per_group_violated`), and it changes the recommended split sizes.

### Temporal: `TemporalSplits`
The horizon is a human judgment, not a row-count rule. Derive it from the source ("managers predict sales up to six
weeks in advance", the competition's own test window, the refit cadence) and write the reasoning in
`splits_comment`. The data arrives sorted by `time_on` (stable), and `TemporalSplits` builds the collection's
convention, which the bundle checks verify:

* one repeat per time window, always fold `0` (`splits_temporal_layout`);
* split 0 is the newest window, the rest walk back in time (`splits_temporal_order`);
* expanding train: everything strictly before the window, minus `gap` (`splits_temporal_leakage`).

| Pattern in the collection | Declaration |
|---|---|
| The last N windows of fixed length (acquire: 5 x 5 days; rossmann: 3 x 42 days with a 1-day planning gap) | `TemporalSplits(window=5, unit="days", n_windows=5)`, `TemporalSplits(window=42, unit="days", n_windows=3, gap=1)` |
| Calendar months or years (coffee: 5 x 6 months; ieee: 3 months, 1-month gap) | `TemporalSplits(window=6, unit="months", n_windows=5)`, `TemporalSplits(window=1, unit="months", n_windows=3, gap=1)` |
| Explicit test periods (kickstarter, sf_permit: calendar years; lending_club: 2016) | `TemporalSplits(window=1, unit="years", cutoffs=(2023, 2024, 2025))` |
| One final period to the end of the data (consumer_complaints, home_credit) | `TemporalSplits(window=None, unit="days", cutoffs=("2025-09-01",))` |
| N windows of distinct time values (anes: election years; garments: dates; kick: derived size) | `TemporalSplits(window=1, unit="unique", n_windows=9)`, `TemporalSplits(window=None, unit="unique", n_windows=9, min_train_fraction=0.5)` |
| Only a row order (california, mercedes: `TimeSeriesSplit`) | `TemporalSplits(window=..., unit="rows", n_windows=3)` with `time_horizon_unit="steps"` |
| Overlapping windows (ghana: 3 days moving by 2) | `TemporalSplits(window=3, unit="days", step=2, min_train_fraction=0.5)` |

Calendar windows end on unit boundaries (day, month start, year start); `min_train_fraction` stops before a window
whose train side is smaller than that share (of the distinct values for `"unique"`, of the rows otherwise) and, with
`window=None` and `unit="unique"`, sizes the windows so they cover the newest `1 - min_train_fraction` of the
values. Only a split that also filters rows by an as-of date (hotel_booking_demand) needs `_make_splits`.

### Datasets above ~1.25M rows: the `_1m` version
The sub-sampled version is its own folder and class, `<unique_name>_1m/dataset.py`, with
`unique_name = "<name>_1m"`, `version_of = "<name>"` and a `version_comment`. It reads the raw files of `<name>`.
Set `subsample_to_budget = True`: the base class caps the single train/test split to 1M train / 250k test rows with
`subsample_split_to_budget` (IID / grouped, whole groups kept) or `subsample_temporal` (temporal, which needs a
single window, for example `cutoffs=("2016",)`); the sub-sampled frame is sorted by time again.

## §D Recurring traps — what to pre-flag

These are the mistakes the collection actually had to fix. Turn each applicable one into a
`# TODO(verify):` marker in `dataset.py`, and a bullet in `curation_comments`.

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

`dataset check` runs these (and `dataset build` refuses to save on an error). Pre-empt them:

| Check slug | Scaffold action |
|---|---|
| `dataset_index_range` | handled by the base class (`reset_index` after the row order) |
| `dataset_object_dtype` | name every non-numeric column in `_feature_types` |
| `dataset_identifier_column` | drop uninformative identifiers (§B.3) |
| `dataset_constant_column`, `dataset_all_missing_column`, `dataset_duplicate_columns` | drop them (§B.7) |
| `dataset_feature_equals_target` | drop target components (§D.1) |
| `dataset_missing_value_sentinel`, `dataset_missing_value_label` | convert proxy missing values (§B.5) |
| `dataset_unused_categories` | handled by the base class (the category cast removes unused categories) |
| `dataset_row_order_leaks_target` | handled by the base class (shuffle); check `shuffle = False` is justified |
| `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` | decide + document (§D.4) |
| `task_target_dtype`, `task_target_class_count` | classification target must be `category` with the right class count |
| `task_target_missing_values` | drop rows with a missing target |
| `task_target_rare_class`, `splits_test_class_unseen_in_train` | drop/merge classes with <10 samples (§D.8) |
| `task_metric_empty`, `task_metric_problem_type_mismatch`, `task_metric_not_canonical` | leave `metric` unset (the default), or use the canonical short name |
| `task_stratify_*` | stratify on the target (classification) or a discrete feature |
| `task_time_on_dtype`, `task_time_on_missing_values`, `task_time_on_not_sorted` | a datetime (`_feature_types`) or numeric time column without NaN; the base class sorts |
| `task_group_labels_per_group_violated`, `task_group_on_unique_per_row` | pick `per_group` vs `per_sample` correctly (§C) |
| `splits_temporal_leakage`, `splits_temporal_order` | expanding train, newest window first (§C) |
| `splits_rows_unused` | IID/grouped splits must cover every row |
| `splits_train_over_budget`, `splits_test_over_budget` | more than 1M train / 250k test rows in a split: make a `_1m` version (§C) |
| `meta_time_horizon_missing` | a calendar `temporal_splits` window, or `time_horizon` + `time_horizon_unit` |
| `meta_tags_*` | tags must agree with the split regime (Step 1) |
| `meta_bibtex_*` | balanced braces, keys defined, `&`/`%`/`_` escaped |
| `meta_placeholder_left`, `definition_todo_left` | every TODO in the metadata and every `TODO(verify)` in `dataset.py` must be resolved before `build` |
| `meta_license_unknown`, `meta_source_link`, `meta_splits_comment_empty` | fill license, a real URL/DOI, and a substantive splits comment |

A warning that is correct for the dataset goes into `accepted_check_warnings` with its reason; `report.md` lists
it under "Accepted on purpose".

## §F Decisions: evidence for the calls a reviewer would question

`_decisions(self, raw, df)` returns `Decision(title, why, evidence)` objects; `dataset check` renders them into the
"Decisions" section of `report.md` (titles also go into the frontmatter). `evidence` is a DataFrame or Series
(rendered as a table), a matplotlib figure (saved as `report/decision_<n>_<title>.png`, linked from the report), a
string, or None. Compute evidence from `raw` (do not change it) and `df`, keep it small, and import matplotlib
inside the hook. Typical decisions, with examples from the collection:

| Decision | Evidence |
|---|---|
| A column leaks the target and is dropped (sub-scores that add up to the target, a post-outcome field) | a table of the column's correlation with / single-feature AUC for the target |
| The split regime (kick: temporal, not grouped by auction location) | a table of how many groups recur over time; a histogram of time points per group |
| Duplicate rows are kept or dropped (§D.4) | the duplicate share and how many conflict in the target |
| Rare classes are merged or dropped (§D.8) | the class counts before and after |
| A proxy missing value is converted (§B.5) | the value counts of the sentinel |

`kick/dataset.py` is the worked example (a table and a figure).

