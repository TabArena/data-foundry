# Writing a dataset definition (v2)

How a dataset is written down in Data Foundry v2: the folder, the `dataset.py` class, what the base class does, the
field mapping from the record, the preprocessing recipe, the split declarations, the bundle checks and how decisions
are recorded. What to decide (which split, which columns, which cleaning) is in the general knowledge skill; this file
says how to express it. Read the class docstrings of `data_foundry.v2.AbstractCuratedDataset`
(`src/data_foundry/v2/dataset.py`) before writing.

## The folder

Every dataset lives in one folder, `datasets/_dev/tabarena-v0pt2/<unique_name>/` for now (the TabArena v0.2 working
copy, [working_copy.md](working_copy.md)):

| File | Written by | Role |
|---|---|---|
| `dataset.py` | the curator or the agent | The only definition: one `AbstractCuratedDataset` subclass. Flat class attributes declare the metadata, the task, the standard preprocessing and the splits; a few hooks hold the code. |
| `explore.ipynb` | the template, then whoever explores | The workbench: `ds = workbench()` loads this folder's dataset and picks up every edit to `dataset.py`. Committed without outputs. |
| `README.md` (+ `figures/*.png`) | `dataset check` / `dataset build` | The dataset card and evidence: YAML front matter (build record, data and split shape, bundle-check slugs, decision titles), then the files of the folder, links, how to rebuild, the dataset and task, the curation notes, the splits, the decisions with their tables and figures, the check results and the build record. Never edited by hand. |
| `REVIEW.md` | the agent, while issues are open | The open issues for the curator ([working_copy.md](working_copy.md)); deleted once they are settled. |

Discovery is `data_foundry.v2.discover_datasets(root)`, and `tests/test_v2_datasets.py` tests every discovered folder
(each import in its own test), so there is no per-dataset test file and no registry to edit.

## The definition file

```python
"""Curated dataset definition for `<unique_name>` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, Temporal, TemporalSplits, drop_columns


class MyDataset(AbstractCuratedDataset):
    task_summary = TaskSummary(...)       # first attribute ("In brief")

    # Dataset (field mapping)
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

    # Splits: a temporal task; a grouped one declares `grouping = Grouping(...)` instead, an IID one neither
    temporal = Temporal(on="date", splits=TemporalSplits(window=7, unit="days", n_windows=3))
    splits_comment = """
        A model refit weekly ...
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:      # required: reading only, cached
        return pd.read_csv(raw_dir / "data.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:      # optional: the preprocessing recipe
        df = raw
        ...
        return drop_columns(df, ["id"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:  # dtypes of the cleaned frame
        return FeatureTypes(
            categorical=["colour"],                # the classification target is added automatically
            string=["description"],
            datetime={"date": "%Y-%m-%d"},         # or a list of names (format inferred)
        )

    def _decisions(self, raw, df) -> list[Decision]:           # optional: Decisions
        ...
```

Other hooks: `_make_splits(df)` for splits the declarations cannot express (return a `SplitPlan`);
`_prepare_raw_files(raw_dir)` with `prepared_raw_files = (...)` for a heavy one-off step that writes intermediate
files into the raw directory (it runs again when a file is missing or when the method, a helper of `dataset.py` it
calls, or a module constant it reads changed; the hash sits in `.prepared_raw_files.json` next to the files);
`_extra_checks(container)` for a dataset-specific bundle check (a leak test from an audit). Sibling files of the
definition (a lookup table such as `sat_concordance.csv`) are under `self.folder`.

The class is validated when `dataset.py` is imported: the required attributes are present and the metadata
validates, `unique_name` equals the folder name, every accepted warning has a reason, the regime is one `Grouping` or
`Temporal` (the flat `time_on`, `group_on`, `group_labels`, `group_time_on`, `temporal_splits`, `time_horizon`,
`time_horizon_unit` attributes are refused), a grouping has a `definition`, a temporal task has windows or
`_make_splits` and a horizon, `subsample_to_budget` needs `version_of` and a `_1m` name, a version needs a
`version_comment`, `prepared_raw_files` needs `_prepare_raw_files`, a multi-column `stratify_on` is refused (build one
key in `_clean`), `Temporal(splits=...)` or `subsample_to_budget` together with a custom `_make_splits` is refused, and
`TemporalSplits` needs `n_windows`, `cutoffs` or `min_train_fraction`. After `_clean`, a declared column that is missing,
or a group or time column with missing values, stops the run with the attribute's name.

Keep `print` diagnostics out of the definition: `README.md` records split sizes and time ranges, and `explore.ipynb`
or `_decisions` is the place for evidence. Keep the `assert`s that guard custom logic. Run `ruff check --fix` and
`ruff format` on the file (double quotes, import order), then `dataset check` again: a fix can change behaviour (rule
C416 once rewrote a dict comprehension and broke a repair; it is now in ruff's ignore list).

## What the base class does

Do not re-implement any of this.

* Metadata: it builds `DatasetMetadata` / `PredictiveMLTaskMetadataV2` (container format 2) from the attributes. Multi-line
  text (`download_description`, `bibtex`, `curation_comments`, `version_comment`, `splits_comment`) is indented like
  code and dedented for you. The BibTeX key is parsed from `bibtex` (set `bibtex_key` only when it must differ). The
  regime tags (`IID`, or `Non-IID` with `Temporal`, `Grouped` or `GroupedTemporal`) are added from the task.
* Defaults: `metric` is the one for the problem type (`roc_auc`, `log_loss`, `rmse`); `stratify_on` is the target for
  classification. Set them only to deviate.
* After `_clean`: it casts the columns `_feature_types` names (a dict gives datetime formats; unused categories are
  removed; a classification target becomes a category without being listed), then fixes the row order: the rows in
  the order of their content (a hash of each row, so the order `_clean` returns does not matter), then a stable sort by
  the time column for a temporal task, otherwise a shuffle with seed 42 (`shuffle = False` keeps the order of `_clean`,
  with a reason in `curation_comments`), then `reset_index`. Never shuffle, sort or `reset_index` yourself, and never
  shuffle the columns (the benchmark permutes them).
* Seeds: one shuffle seed (42) and one split seed (4267) for the whole benchmark.
* The same data on every run and machine: sorts take `kind="stable"`, file listings are `sorted(...)`, a polars
  `group_by` keeps `maintain_order=True`, and a polars join's output is sorted before it is written
  (`definition_nondeterministic` checks the first three). The order `_clean` returns matters only where it changes
  values (`drop_duplicates(keep="first")`, an id numbered by consecutive blocks). Only the last bit of a numpy `log` or
  `exp` can differ between CPUs, so a rebuild elsewhere may give another checksum for a log-scaled target.
* Splits: the v2 split protocol (`src/data_foundry/v2/splits.py`), below.

## In brief: `task_summary`

The first attribute of the class and the first section of the README: what the dataset simulates, then our judgement
of how closely it does (USE-1, USE-8 in [use_case.md](../../knowledge-curation/references/use_case.md); style in
[writing.md](../../knowledge-curation/references/writing.md)). It is not stored in the container, so it never changes a
checksum. `dataset check` reports `definition_summary_missing` (error) without it, `definition_no_use_case` (error)
for `fit="none"`, and `definition_summary_long` (warning) for a field over 70 words.

```python
task_summary = TaskSummary(
    question="How loud is an airfoil's own noise at a given sound frequency, for a wind-tunnel setting that was not measured?",
    use_case="An aerodynamics engineer estimates the noise spectrum of an airfoil configuration (size, angle, wind speed) before, or instead of, measuring it in a wind tunnel.",
    row="One frequency band of one wind-tunnel run, that is one airfoil size at one angle and one wind speed (106 runs of 8 to 19 bands, NASA 1989).",
    predicted="The sound pressure level in that band, in decibels.",
    known="The band's frequency and the run's settings (chord length, angle of attack, wind speed) plus a boundary-layer thickness computed from them.",
    split="Whole runs are held out, so the test data stands for configurations never measured; runs with the same size, angle or speed in other combinations can be in training.",
    changes="We added the run as a group column and split by it; with random rows, models filled gaps in spectra they had already seen.",
    fit="direct",
    fit_reason="The features are the settings an engineer chooses, and a held-out run is an unmeasured configuration. The task is narrow (one airfoil shape, one wind tunnel) but real.",
)
```

(Written with implicit string concatenation in the file, so no line passes 120 characters.) The fields: `use_case`
(settled first), `question`, `row`, `predicted`, `known` (in plain words, never column names), `split` (what the test
data stands for), `changes` (only our changes that alter the task for a reader; empty when none), `fit`
(`"direct"`, `"approximate"`, `"none"`) and `fit_reason`.

## Field mapping (record to definition)

* `unique_name`: the record's name in snake_case (lowercase, special characters to underscores, no repeated or edge
  underscores); `DatasetMetadata` rejects anything else. It equals the folder name.
* `domain`: exactly one of `"education"`, `"environmental science & climate"`, `"biology & life sciences"`,
  `"handcrafted"`, `"chemistry & material science"`, `"industry & manufacturing"`, `"physics & astronomy"`,
  `"multimedia"`, `"medical & healthcare"`, `"technology & internet"`, `"finance"`, `"social science"`,
  `"business & marketing"`, `"insurance"`; the closest match when the record's value differs.
* `source`: exactly one of `"Kaggle"`, `"Zindi"`, `"OpenML"`, `"GitHub"`, `"UCI"`, `"HuggingFace"`, `"GOV Website"`,
  `"Customer"`, `"Other"`, `"ASlib"`: where the data was first published, with `source_url` pointing there
  (PROV-8 in [provenance.md](../../knowledge-curation/references/provenance.md)). `download_description` says where
  the files are downloaded from and names the original when the download is a copy.
* `year`: the year of that first publication (PROV-9 in
  [provenance.md](../../knowledge-curation/references/provenance.md)).
* `data_tags`: context tags only, since listing a regime tag yourself switches the automatic ones off. `"Anonymized"`
  when feature names or values carry no semantics or are masked (common for competition data); `"Spatial"` when the
  data holds geographic information (ZIP, latitude and longitude, region, store location); `"ForcedIIDFromTemporal"`
  when the task is temporal in nature but the release has no time index (SPLIT-8 in
  [splits.md](../../knowledge-curation/references/splits.md)).
* `problem_type`: "Regression" to `"regression"`, "Binary Classification" to `"binary_classification"`,
  "Multiclass Classification" or "Classification" to `"multiclass_classification"`. A table that supports a regression
  or a classification target, where taking one means dropping the other, gets one folder per framing: the second is
  `<unique_name>_clf/` (or `_reg/`) with its own `unique_name`, and the record's `problem_type` follows the one that
  ships.
* `metric`: leave it unset for the three defaults (`rmse`, `roc_auc`, `log_loss`). Another metric is a deliberate
  custom one that must be registered downstream, in its canonical short spelling (`mae`, `rmsle`, `mape`;
  `task_metric_not_canonical` rejects aliases). A competition with its own metric keeps our default, and the notes name
  the original metric.
* `download_description`: for a Kaggle dataset `kaggle datasets download <slug> && unzip ... && rm ...`, then the move
  into `local-data-warehouse/<unique_name>/`; for a competition `kaggle competitions download -c <name>`; otherwise
  `wget <url>`. Pin a DOI or an archived release where one exists.
* `bibtex`: the work that published the data. For a Kaggle dataset a `@misc` entry with `howpublished = {\url{...}}`
  and `note = {Kaggle dataset}`. Balance every brace and escape `&`, `%`, `#`, `_` in typeset fields; the bundle checks
  catch broken entries and a key that does not match.
* The task attributes: IID needs nothing beyond `target` and `problem_type` (set `stratify_on = None` only with a
  reason). Temporal: `temporal = Temporal(on=..., splits=TemporalSplits(...))`. Grouped: `grouping = Grouping(...)`.
  A task is grouped or temporal, never both; an order inside groups is `Grouping(time_on=...)`.

### `curation_comments`

The house format: one opening line naming the exact starting artefact, then `-` bullets
([writing.md](../../knowledge-curation/references/writing.md) for the length and what goes in). Pre-fill the bullets
you know and leave TODO bullets for the rest:

```
We start with <file> from <source>.

- TODO(verify): what was dropped and why (identifiers, leaking features, constant columns).
- TODO(verify): dtype decisions (which columns are category / string / datetime).
- TODO(verify): duplicate-row decision (dropped as a collection artefact, or kept as natural).
- Anomaly: <anything odd that we deliberately did not fix>
- Note: <a decision a reviewer would otherwise question>
```

The prefixes in use: `Anomaly:`, `Note:`, `History:` (the training history and why), `Potential leak, kept on
purpose:` (the mechanism, the numbers, why it stays, when to revisit; homesite_quote_conversion, kick, and the datasets
scaled over all rows). Every non-obvious line of preprocessing code has a bullet, and every bullet has code.

## The preprocessing recipe (`_clean`)

The order the collection's definitions converge on. Emit the steps that plausibly apply as commented stubs with
`TODO(verify)` markers; drop the ones the source clearly does not need. What each step decides is in
[cleaning_features.md](../../knowledge-curation/references/cleaning_features.md).

```python
# 1. Load (+ merge multiple tables on their key, following the source's own joins).
# 2. Rename columns and the target to meaningful names; fix typos, strip special characters. Binary targets get
#    readable labels: df[target] = df[target].map({1: "Yes", 0: "No"})
# 3. TODO(verify): drop uninformative identifiers. To keep an id but hide its names (a group id), use
#    `anonymize_ids(df[col])`, never random ids: `uuid4()` changes the data on every run.
# 4. TODO(verify): reverse ordinal codes and true one-hot blocks, restore the labels (`df[col].map({...})`); yes/no
#    flags that can be set together stay separate columns.
# 5. TODO(verify): proxy missing values and impossible values to NaN, keeping the rows:
#       df = df.replace({"?": np.nan, " ": np.nan})     # UCI style
#       df[col] = df[col].replace(-1, np.nan)           # sentinel style (-1, -9, -999, 999999)
# 6. Dtypes by meaning, named in `_feature_types` (not cast here); no `object` column survives. Cast mid-way with
#    `cast_dtypes` only when a later step needs the dtype. A SMILES column becomes RDKit descriptors and is dropped:
#       df = pd.concat([df, rdkit_descriptors(df["SMILES"])], axis=1)   # `rdkit_*` columns
#    then check for rows that are now copies (stereoisomers).
# 7. TODO(verify): drop constant, all-missing and duplicated columns.
# 8. TODO(verify): drop leaking features (the traps below; leak_checks.md). The most common step in the collection.
# 9. TODO(verify): duplicate rows: decide and document (leak_checks.md, Copies across the split (LEAK-16 to LEAK-21)).
# 10. TODO(verify): target transform: `np.log` / `np.log1p` a skewed positive target and rename the column; skip it
#     when the source already logged it.
# 11. TODO(verify): censored or capped target values (drop the capped rows or document the cap).
# 12. TODO(verify): rows the use case never sees (a row without the input the prediction acts on; bias_correction's
#     days without an LDAPS run).
# 13. TODO(verify): recording errors cleaned to the state an expert would ship (the top solutions' and data owners'
#     rules that hold for train and test alike); one unit and one scale per column (college_scorecard's SAT tables).
# 14. Features a data scientist would build where the raw data cannot be used as it is (aggregates of a history), from
#     the top solutions; never from labels, embeddings, model scores or statistics over all rows.
# 15. The row order and the index are the base class's job.
```

Our own `_clean` never computes a feature value from a statistic over all rows: take it from the history before the
oldest test window, or drop it (LEAK-29; sf_permit_time counts standard phrases before 2020, the start of its oldest
test window; home_credit_default_risk dropped `NEW_INC_BY_ORG` and a mean fill). Check that the source did not scale
over all rows: every column of a block with mean 0 and SD 1, or min 0 and max 1, is the sign (LEAK-30 and probe 16 in
[leak_checks.md](../../knowledge-curation/references/leak_checks.md)).

### pandas 2 and 3 build the same container

pandas 3 reads text as the `str` dtype (missing values stay NaN) and parses dates to `us` or `s`. The base class stores
dates in nanoseconds and `str` text as `object`, so a definition only has to avoid code whose result depends on the
version (all found in the v0.2 copy, 2026-10-06):

* `astype(str)` to build a key or a label: pandas 2 writes a missing value as `"nan"`, pandas 3 keeps it missing. Fill
  first: `df[cols].astype("string").fillna("nan")`.
* Writing a number into a text column (`fillna(0)`, `df.loc[mask, col] = n`): pandas 3 refuses. Cast the column to
  `object` first, or test `notna()` instead of filling.
* `df.select_dtypes(include="object")`: use `object_columns(df)` from `data_foundry.v2`, which counts `str` too.
* `DataFrame.applymap`: removed in pandas 3; use `DataFrame.map`.

## Splits

### IID and grouped

Keep the default: no split attributes. The base class runs the v2 split protocol (`src/data_foundry/v2/splits.py`):
always 3-fold cross-validation, with 20, 10, 3 or 1 repeats by the size of the train side (`recommended_dimensions`),
built by `iid_splits` / `grouped_splits` with the benchmark seed, and every split capped to 1M train and 500k test rows
(`cap_splits`). The comment is "Default splits."; set `splits_comment` only when there is something to say (a split
that deliberately differs from the source's protocol, what a grouped test fold holds).

### Grouped: `Grouping`

```python
grouping = Grouping(
    on="molecule_name",          # the group column(s): split and scoring metadata, never a model feature
    labels="per_group",          # a property of the data
    prediction_unit="group",     # from the use case: "row" (default) or "group"
    aggregation="any",           # with "group" only: "mean", "any", "last", "select_min", "select_max"
    context="all_rows",          # what a model may know about the group: "none" (default), "all_rows", "past_rows"
    definition="""
        One group is a molecule; ... The use case is ... (source, with the quote that says so).
    """,
)
```

It is stored in the container (`task_metadata.grouping`, read with `container.grouping`; `group_on`, `group_labels`,
`group_time_on` are read-only views of it).

* `labels`: `"per_group"` when every row of a group shares one label, `"per_sample"` when each row has its own.
  Getting it wrong is a bundle-check error (`task_group_labels_per_group_violated`), and it changes the split sizes. It
  does not decide the unit: micro_mass has one species per strain, yet identifies the species from one spectrum.
* `prediction_unit` and `aggregation` come from what one real-world prediction is in the source: `mean` for replicate
  measurements of one label, `any` for multiple-instance data (musk: a molecule is a musk if any conformation is),
  `last` when the latest row carries the label (amex; needs `time_on`), `select_min` / `select_max` when one row is
  chosen by its prediction and scored by its true value (sat11: run the algorithm predicted fastest). Everything else
  is `row`.
* `context`: `all_rows` when all rows of a new group are known when predicting, `past_rows` when only its earlier rows
  are (needs `time_on`), `none` when each row stands alone.
* `definition` is required: what one group is, why groups are held out (the use case), and the source with a quote.
  Say when the grouped split is stricter than the source's protocol. It is rendered in the README's "Group structure"
  section with the group statistics, which give four findings (few test groups per fold, one group over 20% of the
  rows, `per_sample` labels nearly one per group, groups not clustered). For the model-based questions run
  `group_probes.py` ([checks_and_probes.md](checks_and_probes.md)); accept `groups_test_groups_few` only with that
  evidence. A group id built from the data: `df.groupby(columns).ngroup()` over the defining columns.

### Temporal: `Temporal` and `TemporalSplits`

Declare `temporal = Temporal(on="date", splits=TemporalSplits(...))`: the time column and the test windows in one
place. The horizon is a human judgment (SPLIT-12 in [splits.md](../../knowledge-curation/references/splits.md));
write the reasoning in `splits_comment`, which replaces the generated text, so restate the windows (and any
sub-sampling or trimming) in it. A window of fixed length is the horizon (`window` `unit` for a calendar unit, `window`
steps for `unit="rows"`), and declaring it again is an error. Add `horizon=..., horizon_unit=...` only when the windows
do not fix it: `unit="unique"` (anes counts election years, garments days), `window=None` (california, kick), or
`_make_splits` (hotel).

The gap between train and test is stored next to the horizon (`time_gap`, `time_gap_unit` in the split metadata, left
out of the checksum while unset): the `gap` of a calendar or row window states it, while a gap of distinct time values
(`unit="unique"`: college_scorecard's cohorts, numerai's weekly eras) or one built in `_make_splits`
(brazilian_ecommerce, sf_permit_time) is declared as `Temporal(..., gap=..., gap_unit=...)`. A `unique` window with a
gap and no declared unit does not import, nor does a declared gap the windows already state or do not leave
(Lennart, 2026-10-16).

The data arrives sorted by the time column, and `TemporalSplits` builds the convention the bundle checks verify: one
repeat per time window, always fold `0` (`splits_temporal_layout`); split 0 is the newest window, the rest walk back
(`splits_temporal_order`); an expanding train side, everything strictly before the window minus the gap
(`splits_temporal_leakage`).

| Pattern in the collection | Declaration |
|---|---|
| The last N windows of fixed length (acquire: 5 x 5 days; rossmann: 3 x 42 days with a 1-day planning gap) | `TemporalSplits(window=5, unit="days", n_windows=5)`, `TemporalSplits(window=42, unit="days", n_windows=3, gap=1)` |
| Calendar months or years (sberbank: 5 x 6 months; lending_club: 3 quarters; ieee: 3 months, 1-month gap) | `TemporalSplits(window=6, unit="months", n_windows=5)`, `TemporalSplits(window=3, unit="months", n_windows=3)`, `TemporalSplits(window=1, unit="months", n_windows=3, gap=1)` |
| Explicit test periods (kickstarter: calendar years) | `TemporalSplits(window=1, unit="years", cutoffs=(2023, 2024, 2025))` |
| Windows down to a train share (coffee: 2 months; sf_permit: 6 months; both keep at least half for training) | `TemporalSplits(window=2, unit="months", min_train_fraction=0.5)` |
| Explicit periods of several months (consumer_complaints: 3 quarters of 2025; home_credit: 3 x 2 months) | `TemporalSplits(window=3, unit="months", cutoffs=("2025-04-01", "2025-07-01", "2025-10-01"))` |
| N windows of distinct time values (anes: election years; garments: dates; kick: derived size) | `TemporalSplits(window=1, unit="unique", n_windows=9)`, `TemporalSplits(window=None, unit="unique", n_windows=9, min_train_fraction=0.5)` |
| Only a row order (california, mercedes) | `TemporalSplits(window=320, unit="rows", n_windows=9)` (horizon: 320 steps); `window=None` needs `Temporal(horizon=..., horizon_unit="steps")` |
| Overlapping windows (ghana, now retired: 3 days moving by 2) | `TemporalSplits(window=3, unit="days", step=2, min_train_fraction=0.5)` |

The number of windows follows `recommended_dimensions` (20, 10, 3 or 1 times 3), never fewer than 3 (`splits_too_few`)
and never a train side below half the data (`min_train_fraction=0.5`); then widen windows of fewer than about 50 test
rows (SPLIT-17 in [splits.md](../../knowledge-curation/references/splits.md)). Calendar windows end on unit boundaries;
`min_train_fraction` stops before a window whose train side is smaller than that share (of the distinct values for
`"unique"`, of the rows otherwise) and, with `window=None` and `unit="unique"`, sizes the windows so they cover the
newest `1 - min_train_fraction` of the values.

Labels that arrive late and training rows whose label is not yet known need `_make_splits`: train on the rows whose
outcome is known by each window's start, with the gap declared on `Temporal` (brazilian_ecommerce, sf_permit_time,
hotel_booking_demand). The training history the use case calls for is set in `_load_raw` or `_clean`, with a
`History:` bullet (aeolus_1m: flights from 2023 on).

### Larger than the row budget: the `_1m` version

The v2 protocol keeps every split at 3 folds (or at least 3 temporal windows) and at most 1M train / 500k test rows. A
dataset that does not fit gets a sub-sampled version, its own folder and class, `<unique_name>_1m/dataset.py`, with
`unique_name = "<name>_1m"`, `version_of = "<name>"` and a `version_comment`. It reads the raw files of `<name>`. Set
`subsample_to_budget = True`:

* IID or grouped data: a frame of up to 1.5M rows is taken fully (3 folds of 2/3 train). A larger frame is sub-sampled
  to 1.5M rows before splitting (`subsample_frame`: rows stratified on the target, or whole groups), then the usual
  splits are built and each side capped (`cap_splits`). `subsample_to_budget` on a frame that already fits is an error.
* Temporal data: the frame is not sampled. The windows (at least 3) are built on the full data, then
  `sample_temporal_splits` keeps at most 500k rows of each test window and a random 1M of all earlier rows for each
  train side, drawn in one random order so the train sides overlap; the frame keeps only the rows a split uses. A
  temporal `_1m` version whose windows all fit is an error.

A dataset that sets `splits_comment` itself states the sub-sampling there.

## Traps to flag at scaffold time

Turn each one that plausibly applies into a `# TODO(verify):` marker in `dataset.py` and a bullet in
`curation_comments`. What each means and the precedents: [leak_checks.md](../../knowledge-curation/references/leak_checks.md)
and [cleaning_features.md](../../knowledge-curation/references/cleaning_features.md).

* A part, consequence or encoding of the target among the features: "list every feature that is a component or a
  consequence of the target and drop it."
* A value not known at the prediction point, per suspicious column; missingness caused by the outcome; a codebook
  marker for post-outcome items.
* Repeated entities across the split: "check for repeated entities (patient_nbr, address, obj_ID, hospital number)";
  parse ids as strings.
* Duplicate rows: decide and say the share.
* Row order that carries signal (the base class shuffles; a temporal row order needs a check against the date).
* Censored or capped targets; the newest periods losing their slow cases.
* Proxy and impossible values.
* Rare classes and merged labels.
* The source's split protocol, taken as a claim.
* Top solutions' preprocessing without their exploits.
* Anonymized data: keep it as it is, tag `Anonymized`, and say what could not be determined.
* Destroyed meaning to reconstruct.
* Classes recorded differently: "check number formats and missingness per class; do two same-label subgroups
  separate?"
* Cohort and selection, right truncation.
* A label read off a later stage.
* Definition bugs the audit found in shipped datasets: a numeric column listed as categorical (a 125k-level category in
  give_me_some_credit); a target stored as `log1p` with metric `rmsle`, which logs it again
  (santander_transaction_value); BibTeX citing a different competition (sberbank_housing_market_forecasting); a tag in
  `license` (cirrhosis: `"IID"`). Read the class attributes once more for these before handing off.

## Bundle checks and what to do at scaffold time

`dataset check` runs them (and `dataset build` refuses to save on an error). Pre-empt them:

| Check slug | Scaffold action |
|---|---|
| `dataset_index_range` | handled by the base class |
| `dataset_object_dtype` | name every non-numeric column in `_feature_types` |
| `dataset_identifier_column` | drop uninformative identifiers (recipe step 3) |
| `dataset_constant_column`, `dataset_all_missing_column`, `dataset_duplicate_columns` | drop them (step 7) |
| `dataset_feature_equals_target` | drop target components |
| `dataset_pure_feature_value` | a value (100 rows or more), or present against missing, that holds one class only: look the column up in the source's documentation; drop it if derived from or recorded after the outcome, else accept with the reason. On a target with a 94-98% base rate it is usually an ordinary category effect |
| `dataset_missing_value_sentinel`, `dataset_missing_value_label` | convert proxy missing values (step 5) |
| `dataset_unused_categories` | handled by the base class |
| `dataset_row_order_leaks_target` | handled by the base class (shuffle); check that `shuffle = False` is justified |
| `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` | decide and document |
| `task_target_dtype`, `task_target_class_count` | a classification target is a `category` with the right class count |
| `task_target_missing_values` | drop rows with a missing target |
| `task_target_rare_class`, `splits_test_class_unseen_in_train` | a class too rare to stratify: keep a rare class of the source's labels when its rows carry about their share of the score, merge only by a convention of the field, and accept with the counts ([task_probes.md](../../knowledge-curation/references/task_probes.md), TP-7 and TP-8) |
| `task_metric_empty`, `task_metric_problem_type_mismatch`, `task_metric_not_canonical` | leave `metric` unset, or use the canonical short name |
| `task_stratify_*` | stratify on the target (classification) or a discrete feature |
| `task_time_on_dtype`, `task_time_on_missing_values`, `task_time_on_not_sorted` | a datetime (`_feature_types`) or numeric time column without NaN; the base class sorts |
| `task_group_labels_per_group_violated`, `task_group_on_unique_per_row` | pick `per_group` or `per_sample` correctly |
| `splits_temporal_leakage`, `splits_temporal_order` | expanding train, newest window first |
| `splits_rows_unused` | IID and grouped splits cover every row |
| `splits_train_over_budget`, `splits_test_over_budget` | more than 1M train / 500k test rows in a split: a `_1m` version for a frame above 1.5M rows, otherwise narrower windows |
| `splits_too_few` | a temporal task with fewer than 3 test windows: declare at least 3 |
| `meta_time_horizon_missing` | a fixed-length window in `Temporal(splits=...)`, or `Temporal(horizon=..., horizon_unit=...)` |
| `meta_time_gap_without_time_on` | a gap belongs to a temporal task |
| `groups_test_groups_few` | fewer than 20 test groups in a fold: keep only with real signal across groups (`group_probes.py`) and more than a handful of groups of each class per fold (else `Too Small`), and accept with that evidence |
| `groups_largest_share_high` | one group over 20% of the rows: check it is one entity, not a catch-all value |
| `groups_labels_constant` | `per_sample` with at least 95% single-label groups: `per_group` if one label by construction, else accept with the count of mixed groups |
| `groups_not_clustered` (info) | rows no closer to their group than chance: compare IID and grouped scores before keeping the grouping |
| `splits_test_single_class`, `splits_test_target_constant` | a test fold whose metric is undefined: fewer, larger folds or windows, or the task is too small |
| `splits_test_minority_few`, `splits_test_class_missing` | test folds with under 10 rows of the rarer class, or without some class: widen the windows, merge by convention, or accept with the counts |
| `task_target_value_dominant` | one value holds half of a regression target: name the cap, placeholder or zero inflation in `curation_comments`, drop censored rows, or accept with the reason |
| `meta_tags_*` | tags agree with the split regime |
| `meta_bibtex_*` | balanced braces, keys defined, `&`, `%`, `_` escaped |
| `meta_placeholder_left`, `definition_todo_left`, `definition_license_placeholder` | every TODO in the metadata (the licence included) and every `TODO(verify)` in `dataset.py` is resolved before `build` |
| `definition_nondeterministic` | seed every random step, sort with `kind="stable"`, wrap `glob` / `iterdir` / `listdir` in `sorted(...)`, use `maintain_order=True` in a polars `group_by` (and sort what a polars join returns before writing it) |
| `definition_summary_missing`, `definition_no_use_case`, `definition_summary_long` | the `task_summary` (In brief) |
| `accepted_check_warnings_unused` (info) | an accepted slug that no longer fires: remove the entry, or fix the misspelled slug |
| `check_crashed` | a check raised; the message names it. Fix the definition or report the check |
| `meta_license_unknown`, `meta_source_link`, `meta_splits_comment_empty` | a licence, a real URL or DOI, and a substantive splits comment |

A warning that is correct for the dataset goes into `accepted_check_warnings` with its reason (one per slug, filled by
the curator once they have seen the warnings); `README.md` lists it under "Accepted on purpose".

## Decisions: evidence for the calls a reviewer would question

`_decisions(self, raw, df)` returns `Decision(title, why, evidence)` objects; `dataset check` renders them into the
README's "Decisions" section (titles also go into the front matter). `evidence` is a DataFrame or Series (a table), a
matplotlib figure (saved as `figures/decision_<n>_<title>.png`), a string, or None. Compute it from `raw` (do not
change it) and `df`, keep it small, and import matplotlib inside the hook.

| Decision | Evidence |
|---|---|
| A column is dropped for what it is: recorded after the prediction point, an outcome, a model output or estimate fit with the label, a field the source says not to use | no numbers: the reason (the source's words) in `curation_comments`, and no decision unless a reviewer could question the call |
| A column is dropped for what its values show, and the context does not settle it (sub-scores that add up to the target, a column tied to the label's time window, a block with no signal) | the comparison that shows it (its correlation with or ROC AUC alone for the target against a reference), with `roc_auc_score` and pandas `corr`, not a hand-written helper; how much the drop matters comes from `leak_probes.py` |
| The split regime (kick: temporal, not grouped by auction location) | a table of how many groups recur over time; a histogram of time points per group |
| A suspected leak kept on purpose (kick `WheelType`, homesite) | the target rate by value or by missingness, and the score with and without the column |
| Duplicate rows kept or dropped | the duplicate share and how many conflict in the target |
| Rare classes merged or dropped | the class counts before and after, and the smallest class per test fold |
| A proxy missing value converted | the value counts of the sentinel |

`kick/dataset.py` is the worked example (a table and a figure). Show a number only where it decides the call
([writing.md](../../knowledge-curation/references/writing.md)); `rain_in_australia` shows a case where it does (each
column's ROC AUC for the rain before 9 am on day D against the label's window).

## Recording decisions

* `curation_comments`: one bullet per drop, filter or kept suspect, with the mechanism, the number that decides it,
  and the location in the paper for any claim taken from it. Longer evidence goes into the record as an
  `**Assessment (AI, ...)**` or into a `_decisions` table.
* A suspect kept on purpose: `Potential leak, kept on purpose:` with the mechanism, the numbers, why it stays and when
  to revisit.
* The record: the curator's decision as a dated `CC` line with the same substance, and a revisit condition when the
  call is provisional (ghana "retired for now", sf_permit_time "re-download in 1-2 years", homesite "if the fields are
  documented"); planned outreach to authors goes into the record ([records.md](records.md)).
* A retirement: `No (Retired)` with its markers, the folder removed from the working copy, `v2_path` cleared and a
  CHANGELOG entry ([working_copy.md](working_copy.md)).
* An accepted bundle-check warning keeps its reason in `accepted_check_warnings` (emscad accepts
  `dataset_pure_feature_value` for large legitimate clients).

## Reference definitions

Read the closest one in full before writing (paths under `datasets/_dev/tabarena-v0pt2/`):

| Regime | Reference | What it shows |
|---|---|---|
| IID | `tour_travels_churn/dataset.py`, `forensic_glass_identification/dataset.py` | The minimal definition: attributes, `_load_raw`, a short `_clean`. |
| Grouped | `airfoil_self_noise/dataset.py`, `early_learning_predictors/dataset.py`, `musk/dataset.py`, `emscad/dataset.py` | `Grouping` with a `definition` citing the source (airfoil: a wind-tunnel run built from three columns; musk: one prediction per molecule, `aggregation="any"`), rule-based leak drops in `_clean`, long feature lists (early_learning), a group id built from the data and an accepted group finding (emscad). |
| Temporal | `kick/dataset.py` | `TemporalSplits(window=None, unit="unique", n_windows=9, min_train_fraction=0.5)`, a datetime in `_feature_types`, and `_decisions` with a table and a figure. |
| Temporal with late labels | `brazilian_ecommerce/dataset.py`, `sf_permit_time/dataset.py` | `_make_splits` training on rows whose label had arrived, with the gap on `Temporal`. |
| Sub-sampled `_1m` | `sepsis_prediction_1m/dataset.py` (grouped), `delivery_eta_1m/dataset.py` (temporal) | `version_of`, `version_comment`, `subsample_to_budget`, grouped labels per sample; 3 weekly `TemporalSplits` with a `splits_comment` that states the sub-sampling. |
| Heavy raw data | `acquire_valued_shoppers_challenge/dataset.py` | `prepared_raw_files` + `_prepare_raw_files` (a polars join run once), fixed calendar windows. |

## What the benchmark harness does with a definition

* v0.2 runs a new default pipeline like BeyondArena's, which keeps the hour of a datetime (skrub's `DatetimeEncoder`);
  only the v0.1 pipeline dropped it (Lennart, 2026-10-12). Do not add hour columns to work around it.
* A group column is split and scoring metadata, never a feature; the harness drops it before fitting
  (`datasets/_dev/tabarena-v0pt2/BENCHMARK_CHANGES_TODO.md` lists what the harness still needs, such as per-group
  scoring and custom metrics).
* String columns are embedded by the pipeline, so a definition ships text as `string`, and molecules as RDKit
  descriptors.
