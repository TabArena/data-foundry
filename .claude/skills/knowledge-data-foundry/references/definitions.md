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
| `README.md` (+ `figures/*.png`) | `dataset check` / `dataset build` | The dataset card and evidence: YAML front matter (build record, data and split shape, bundle-check slugs, decision titles), then the files of the folder, links, how to rebuild, the dataset and task, the curation notes, the splits, the decisions with their tables and figures, the check results and the build record. Never edited by hand. |
| `REVIEW.md` | the agent, while issues are open | The open issues for the curator ([working_copy.md](working_copy.md)); deleted once they are settled. |

Discovery is `data_foundry.v2.discover_datasets(root)` (the tasks; `discover_definitions` adds the parents of a family,
"Families" below), and `tests/test_v2_datasets.py` tests every discovered folder (each import in its own test), so there
is no per-dataset test file and no registry to edit.

## The definition file

```python
"""Curated dataset definition for `<unique_name>` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset, Decision, FeatureTypes, Metric, Source, TaskSummary, Temporal, TemporalSplits, drop_columns,
)


class MyDataset(AbstractCuratedDataset):
    task_summary = TaskSummary(...)       # first attribute ("In brief")

    # Dataset (field mapping)
    unique_name = "my_dataset"
    domain = "finance"
    sources = (                         # the publication first; its year and BibTeX are the dataset's
        Source(
            role="publication",
            platform="Kaggle",
            url="https://...",
            license="CC BY 4.0",
            year="2024",
            bibtex="""
                @misc{key2024,
                  ...
                }
            """,                         # the key is parsed from the entry
        ),
    )
    data_tags = ("Spatial",)            # context tags only; regime tags are added from the task
    download_description = """
        kaggle datasets download ... && unzip ...
    """                                  # indented like code: dedented by the base class
    curation_comments = """
        We start with <file> from <source>.

        - ...
    """

    # Task
    target = "y"
    problem_type = "binary_classification"   # stratify_on -> target by default
    metric = Metric.source("roc_auc", original="AUC", reference="https://...")  # required (metrics.md)

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
            ordinal={"condition": ["poor", "fair", "good"]},  # an ordinal scale, lowest level first (CLEAN-14)
        )

    def _decisions(self, raw, df) -> list[Decision]:           # optional: Decisions
        ...
```

A time column a model sees coarser than recorded (crash times to the hour) is coarsened in `_clean`, never in
`_make_splits`: the rows are ordered by the time column before the split step runs, so a split step that floors it
leaves each period in the order of the finer values (chicago_traffic_crashes, 2026-11-04); `dataset check` warns
(`definition_time_changed_in_split`).

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
`_make_splits` and a horizon, `sources` is a tuple of `Source` with exactly one publication (listed first, with a
four-digit `year` and a `bibtex`), a `row_budget` needs the name `<name>_<suffix>` (`_1m`), the removed `year`,
`source`, `source_url`, `license`, `bibtex`, `bibtex_key`, `version_of`, `version_comment` and `raw_data_from` are
refused with what replaced them, `prepared_raw_files` needs `_prepare_raw_files`, a multi-column `stratify_on` is
refused (build one key in `_clean`), `Temporal(splits=...)` or `row_budget` together with a custom `_make_splits` is
refused, the old `subsample_to_budget` is refused with a pointer to `row_budget`, and
`TemporalSplits` needs `n_windows`, `cutoffs` or `min_train_fraction`. After `_clean`, a declared column that is
missing, or a group or time column with missing values, stops the run with the attribute's name.

Keep `print` diagnostics out of the definition: `README.md` records split sizes and time ranges, and `_decisions`
(or `ds = workbench()` in an uncommitted scratch notebook) is the place for evidence. Keep the `assert`s that guard
custom logic. Run `ruff check --fix` and `ruff format` on the file (double quotes, import order), then `dataset check`
again: a fix can change behaviour (rule C416 once rewrote a dict comprehension and broke a repair; it is now in ruff's
ignore list).

## What the base class does

Do not re-implement any of this.

*  Metadata: it builds `DatasetMetadataV2` / `PredictiveMLTaskMetadataV2` (container format 2) from the attributes.
  Multi-line text (`download_description`, a source's `bibtex`, `curation_comments`, `splits_comment`) is indented
  like code and dedented for you. A source's BibTeX key is parsed from its `bibtex` (set `Source(bibtex_key=...)` only
  when it must differ). The regime tags (`IID`, or `Non-IID` with `Temporal`, `Grouped` or `GroupedTemporal`) are
  added from the task.
* Defaults: `stratify_on` is the target for classification; set it only to deviate. `metric` has no default: it is
  required, and `Metric.fallback(reason=...)` resolves to the problem type's `roc_auc`, `log_loss` or `rmse` at build.
* After `_clean`: it casts the columns `_feature_types` names (a dict gives datetime formats; unused categories are
  removed; a classification target becomes a category without being listed; an `ordinal` column is an ordered
  category, also when `categorical` names it too), then fixes the row order: the rows in
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
    question="How loud is an airfoil's own noise in a given frequency band, on the source's speed-scaled decibel level, for an airfoil size at an angle of attack that was not measured?",
    use_case="An aerodynamics engineer estimates the noise spectrum of an airfoil at a size and angle of attack not yet tested, at any wind speed, before, or instead of, mounting it in a wind tunnel.",
    row="One frequency band of one wind-tunnel run, that is one airfoil size at one angle and one wind speed (106 runs of 8 to 19 bands, the tripped-boundary-layer set of NASA 1989; bands with tunnel noise removed).",
    predicted="The band's sound level as the source scales it, in decibels: the measured level minus a term of the wind speed and the boundary-layer thickness, so the measured level follows exactly from the features.",
    known="The band's frequency and the run's settings (chord length, angle of attack, wind speed) plus a boundary-layer thickness computed from them.",
    split="Whole setups are held out, an airfoil size at one angle with all its wind speeds, so the test data stands for a size and angle never measured together; each size, and most angles, are in training with other partners.",
    changes="We added the setup (size and angle) as a group column and split by it, and treat the angle as a number; with random rows, or whole runs, models filled in spectra of setups they had seen at another speed.",
    fit="direct",
    fit_reason="The features are the settings an engineer chooses, and a held-out setup is an airfoil at an angle not yet tested. The task is narrow (one airfoil shape, tripped, one wind tunnel and microphone) but real.",
)
```

(Written with implicit string concatenation in the file, so no line passes 120 characters.) The fields: `use_case`
(settled first), `question`, `row`, `predicted`, `known` (in plain words, never column names), `known_at_scoring`
(what the scorer knows that the model does not; empty when it knows only the target), `split` (what the test data
stands for), `changes` (only our changes that alter the task for a reader; empty when none), `fit` (`"direct"`,
`"approximate"`, `"none"`) and `fit_reason`.

`known_at_scoring` is for a metric input recorded with the outcome, such as a realized time on risk that weights a
rate (MET-15): known for the training rows and when scoring, since those periods are over, but not at the prediction
point. Say what it is and why the model cannot have it, in plain words: "How long each policy was actually insured,
which a claim or a cancellation can cut short; it weights the claims per year insured in training and in the score."
A metric input known at the prediction point (a weight that is a function of the features) goes in `known` or nowhere
(Lennart, 2026-11-09).

## Field mapping (record to definition)

* `unique_name`: the record's name in snake_case (lowercase, special characters to underscores, no repeated or edge
  underscores); `DatasetMetadata` rejects anything else. It equals the folder name.
* `domain`: exactly one of `"education"`, `"environmental science & climate"`, `"biology & life sciences"`,
  `"handcrafted"`, `"chemistry & material science"`, `"industry & manufacturing"`, `"physics & astronomy"`,
  `"multimedia"`, `"medical & healthcare"`, `"technology & internet"`, `"finance"`, `"social science"`,
  `"business & marketing"`, `"insurance"`; the closest match when the record's value differs. A molecule-property
  dataset (the input is the molecule: QSAR, toxicity, bioactivity) is `"chemistry & material science"` (Lennart,
  2026-10-21, the ten QSAR siblings).
* `sources`: a tuple of `Source(role=..., platform=..., url=..., license=..., year=..., bibtex=..., name=...,
  files=...)`, the publication first.
  * The **publication** (`role="publication"`, exactly one) is where the data was first published, with `url`
    pointing there (PROV-8 in [provenance.md](../../knowledge-curation/references/provenance.md)). `platform` is
    exactly one of `"Kaggle"`, `"Zindi"`, `"OpenML"`, `"GitHub"`, `"UCI"`, `"HuggingFace"`, `"GOV Website"`,
    `"Customer"`, `"Other"`, `"ASlib"`. Its `year` is the year of that first publication (PROV-9), always four digits:
    when it cannot be pinned, the best guess, with the reason in `curation_comments`; a definition with another value
    does not load. Its `bibtex` is the work that published the data (below), its `license` the one it states (None
    when it states none).
  * A **copy** (`role="copy"`) is a later copy of the data, such as the re-upload we download (a Kaggle or UCI copy of
    a paper's supplement): its own `platform`, `url` and `license`, a `name` ("UCI 291") and, if known, its `year`.
    List it when the download is not the publication; `download_description` still says how the files are fetched.
  * A **part** (`role="part"`) is a piece the dataset is assembled from (one of several survey waves, a second table
    joined in), each with its own `license` and a `name` that tells the parts apart.
  * `files=("*.csv",)` names the raw files that come from a source, as paths or glob patterns under the raw folder.
    The container lists them with their SHA-256, size and rows (`raw_files`, "The raw-file manifest" below).
* `data_tags`: context tags only, since listing a regime tag yourself switches the automatic ones off. `"Anonymized"`
  when the source hid what the features are, by replacing their names or values on purpose (common for competition
  data; the record gets the `Anonymized` marker, and the cases without it are in
  [selection.md](../../knowledge-curation/references/selection.md), "Anonymized data"); `"Spatial"` when the data
  holds geographic information (ZIP, latitude and longitude, region, store location). An IID or grouped split carries
  one time basis that says why it is not temporal (SPLIT-32 in
  [splits.md](../../knowledge-curation/references/splits.md)): a use-case prototype, `"Timeless"` (the target is a
  fixed property of the item), `"Snapshot"` (the use case fills in a time the data covers), `"DelayedTarget"` (one
  shared prediction moment, the target later in a window closed for every row) or `"StationaryRelation"` (a present
  state read through a relation that time does not move, measured on a dated source), each with a `Time basis:` line
  in `curation_comments` that states the fact; or a forced tag, `"ForcedIIDFromTemporal"` when a forward use case has
  no usable time or too few periods and ships IID (a definition that declares a `grouping` or `temporal` refuses it),
  `"ForcedGroupedFromTemporal"` when such a task ships grouped (it needs a `grouping`; SPLIT-8). A definition refuses
  two time bases, and a prototype on a temporal split or without its line. `dataset check` notes a split that is not
  temporal and has no time basis, and notes date columns in the data of such a split unless the basis is `Snapshot`.
  `"2ndTierData"` is retired (2026-10-21): old containers that carry it still load, but a new definition refuses it;
  write the doubts as a finding and the fit as `approximate`.
* `problem_type`: "Regression" to `"regression"`, "Binary Classification" to `"binary_classification"`,
  "Multiclass Classification" or "Classification" to `"multiclass_classification"`. A table that supports a regression
  or a classification target, where taking one means dropping the other, gets one folder per framing: the second is
  `<unique_name>_clf/` (or `_reg/`) with its own `unique_name`, written as a child of the first ("Families" below), and
  the record's `problem_type` follows the one that ships.
* `metric` (required): a `Metric` from `data_foundry.v2.metrics`; which one is decided by
  [metrics.md](../../knowledge-curation/references/metrics.md) (MET). Three constructors, one per origin (MET-11):
  * `Metric.source(name, original=..., reference=..., params=..., inputs=..., definition=...)`: what the source
    scored (zillow_prize `Metric.source("mae", original="MAE of logerror", reference=<the evaluation page>)`). A
    metric equal to the original by identity is a source too, with the identity in `definition` (ROC AUC for a binary
    normalized Gini).
  * `Metric.stand_in(name, original=..., reason=..., reference=...)`: the closest computable metric to a unique
    original that cannot be computed on our data; `original` and `reason` are required.
  * `Metric.from_context(name, reason=...)`: the source defines no metric, but the task makes one obvious (diamonds:
    `rmsle` on the price in dollars, since a price's error matters relative to the price); `reason` is required.
  * `Metric.fallback(reason=...)`: no metric of the source the task would use (none defined, several reported, a
    threshold metric without a threshold or costs); `roc_auc`, `log_loss` or `rmse` by problem type at build. The
    reason says where we looked and which source metric was rejected and why.

  Every constructor takes `target_transform` (`"identity"` by default, `"log"`, `"log1p"`, `"log10"`; regression
  only, MET-3): the target ships transformed for modelling, and the metric is computed after the inverse (`exp`,
  `expm1`, `10**`) of both the true values and the predictions, on the original scale. Declare exactly what `_clean`
  applies: `np.log(price)` is `"log"`, `np.log1p(area)` is `"log1p"`. So RMSLE on a log1p target is
  `Metric.source("rmsle", ..., target_transform="log1p")`, the competition's MAE on a logged loss is
  `Metric.source("mae", ..., target_transform="log")`, and a price shipped as its log with no source metric is
  `Metric.from_context("rmsle", reason=..., target_transform="log")`. A custom metric never inverts the target
  itself (par_k reads the runtime after the spec's inverse).

  `name` is a key of `METRICS` (standard scikit-learn style names, or a custom metric under a general name, MET-12);
  an unknown name or param is refused when `dataset.py` is imported, with the close names. `params` holds JSON values
  only (a cost matrix, k, weights); `inputs` maps each role the metric needs (`group`, `weight`, `time`) to a column.
  Each such column is a **scoring column**, except the task's group or time column, which the metric reads where it
  is (`task_metric_input_is_model_input`, info). A feature the metric also needs (MET-2: a weight known for every
  row at the prediction point, such as liberty_mutual_fire_peril_loss_cost's `var11`) stays a feature and is copied
  in `_clean` into a scoring column named for its role (`var11_weight`), so the scoring columns are the complete
  set of the extra data a metric reads; a metric input that is a plain feature is a warning
  (`task_metric_input_is_feature`), and the copy is exempt from `dataset_duplicate_columns`. A scoring column stays in
  the frame, is never a feature, and is declared as
  `scoring_columns = (ScoringColumn(column="era", role="group", used_by="mean_group_pearsonr", description="the week a
  row belongs to; the metric is the mean of the per-era correlations"),)`. `feature_columns(container)` returns the
  model's inputs without the target, the group column and the scoring columns, and `scorer(container)` takes the
  scoring columns' values by row index: `scorer(container)(y_test, y_pred, test_idx)`. It reads class probabilities
  in the sorted order of the classes (scikit-learn's `classes_`), also for an ordered target, whose declared order
  stays type information; a DataFrame whose columns are the class names is matched by name, and a missing or unknown
  class name is an error (Lennart, 2026-11-05). Before declaring a metric with inputs, check on the data that every
  test fold holds what it needs (MET-2).

  A row weight makes each row count in proportion to it: `normalized_weighted_gini`, `weighted_pearsonr` (without
  `weights`), `rescaled_mean_tweedie_deviance` (its required `weight`; since 2026-11-08: each scored set's predictions
  multiplied by `sum(w * y) / sum(w * p)`, then the weighted Tweedie deviance, the stand-in for a pricing game's market
  that rescales every tariff to one total, pricing_game_2016_french_fleet), the optional `weight` input of
  `mean_poisson_deviance` and `mean_tweedie_deviance` (`sum(w * d) / sum(w)`, as scikit-learn's `sample_weight`) and of
  `rmse` (`sqrt(sum(w * (y - p)^2) / sum(w))`, since 2026-11-08: boreal_postfire_lichen_biomass weighs each quadrat by 1
  over its plot's quadrats, so each plot counts once), and `ordered_lorenz_gini` with `params={"per_unit": True}`, where
  the target and the prediction are already per unit of the weight (a loss per year insured; the unnormalised weighted
  Gini). Without `per_unit` its weight is the base premium that totals are compared against, not a row weight.
  `data_foundry.v2.metrics.row_weight_column(spec)` returns a spec's row-weight column, or `None`. The regression
  fallback takes the weight too (`Metric.fallback(reason=..., inputs={"weight": ...})`); the spec of a weighted `rmse`
  states the weighted formula, while the unweighted spec keeps `sqrt(mean((y - p)^2))`, so the containers built before
  keep their checksum. The three deviances require `min_prediction`, the floor on the predicted mean, the lowest value
  the use case's actor acts on, stated with its fact, never above the smallest plausible mean on the scale the metric
  scores (MET-13 as amended 2026-11-09; `1e-4` claims per year for fremtpl2 and bemtpl97, $10 for noaa_storm).
  `score()` refuses an input the metric does not take, so a weight is never dropped without notice.

  The build writes the spec into the task metadata as `objective_metric`: `name`, `kind` (`standard`, `custom` or
  `local`), `prediction` (`proba`, `label`, `value`), `greater_is_better`, `origin`, `params`, `inputs`, `original`,
  `reference`, `definition` (a one-line formula), `reason` and `target_transform`; a reader without Data Foundry can
  implement the metric from these fields. `describe()` and the README show it with the scoring columns. The bundle
  checks: `task_metric_undeclared` (a fallback without a reason), `task_metric_unknown`, `task_metric_not_canonical` (an
  alias), `task_metric_problem_type_mismatch`, `task_metric_unknown_param`, `task_metric_param_invalid` (error: params
  that fail the registry's validation, such as a Poisson deviance without `min_prediction`), `task_metric_input_missing`
  (a role the metric needs is not mapped), `task_metric_input_is_model_input` (info: the metric reads the task's group
  or time column), `task_metric_input_is_feature` (warning: the metric reads a plain feature; ship a scoring copy),
  `task_metric_reference_missing` (a source or stand-in without a link),
  `task_metric_stand_in_incomplete`, `task_metric_not_computable` (no finite score of a random prediction on some fold),
  `task_metric_local`, `task_metric_transform_not_regression`, `task_metric_transform_overflow` (the inverse of
  `target_transform` overflows on a shipped value: the target is not on that scale),
  `task_metric_deviance_on_transformed_target` (error since 2026-11-06, CLEAN-16: a Poisson or Tweedie deviance scores
  the mean on the original scale, which a model fit on a log target misses; ship the target untransformed, as
  pricing_game_2017_french_mtpl) and `task_metric_weight_without_sample_weight` (warning: the metric reads a row weight
  and the task declares no `sample_weight`; accept it with the reason when the weight is a function of the features).
  The training weight's checks: `task_sample_weight_not_metric_weight` (error: `sample_weight` is not the metric's row
  weight), `task_weight_invalid` (error: a missing, non-finite or negative weight, a zero weight on a row a deviance
  scores, a split side whose weights sum to 0), `task_rate_count_not_whole` (warning: under a weighted Poisson
  deviance, target x weight is not a whole count) and `task_feature_looks_like_exposure` (warning: a numeric feature
  named like an amount at risk on a task without a weight; accept it with what the column is, planned or realized).
  `Metric.local(fn, name=..., prediction=..., greater_is_better=...)` holds code only the definition has; it is for a
  user's own dataset that is never shipped (`build(allow_local_metric=True)`), never for the working copy (MET-13).
* `sample_weight = "<column>"` (optional, opt-in per dataset): the task's training weight, a rate's realized
  denominator such as the years insured (MET-14, MET-15). It names a scoring column of role `weight` that the
  objective metric reads as its row weight, so every model trains with the weight it is scored by:

  ```python
  sample_weight = "Exposure"
  scoring_columns = (ScoringColumn(column="Exposure", role="weight", used_by="mean_poisson_deviance",
                                   description="years insured, cut short by a cancellation after a claim; the "
                                   "rate's denominator, the metric's row weight and the training weight"),)
  metric = Metric.source("mean_poisson_deviance", ..., inputs={"weight": "Exposure"}, params={"min_prediction": 1e-4})
  ```

  The container stores it in the task metadata. `feature_columns(container)` leaves it out with the other scoring
  columns, `sample_weight(container)` (`data_foundry.curation_container`) returns it (`None` when the task has none),
  and a harness fits every model with it as each training row's weight, never as a feature. The test-row values of a
  weight scoring column, a training weight or not, are for the scorer only: never read them when predicting a test
  row (LEAK-41; the README and `describe()` say so, Lennart, 2026-11-08). The amount at risk is described in
  text: the scoring column's `description` (what it measures, whether the outcome can cut it short) and a
  `curation_comments` bullet. A metric weight that is a function of the features (liberty_mutual_fire_peril_loss_cost's
  `var11_weight`, g_research_crypto_forecasting_1m's asset `Weight`) needs no sample weight: accept
  `task_metric_weight_without_sample_weight` with that reason.
* `unit_weight = UnitWeight(column="<weight column>", unit="<unit column>")` (optional): a score that counts each unit
  once (MET-17), e.g. each plot of boreal_postfire_lichen_biomass or each mouse of pancreatic_cancer_mouse_detection.
  The column is the metric's weight scoring column (`inputs={"weight": column}`), 1 over the unit's rows (`1.0 /
  df.groupby(unit)[unit].transform("size")`); the unit is a column `_clean` keeps (the group column, or a column kept
  for it), metadata, never a feature. It is for scoring and validation only, never a `sample_weight`. The task metadata
  stores it, so downstream tools can read it: `unit_weight(container)` returns it, `validation_weight(container)`
  returns the column a validation loss is weighted by (the metric's row weight: the training weight, a unit weight or a
  weight that is a function of the features), and `feature_columns(container)` leaves the unit out. Its checks:
  `task_unit_weight_not_one_per_unit` (error: a unit's weights do not sum to 1) and `task_unit_weight_unit_split`
  (warning: a unit has rows on both sides of a split). With it declared, `task_metric_weight_without_sample_weight` is
  not raised (Lennart, 2026-11-08: downstream tools "need to know it to set their own validation loss correctly").
* `download_description`: for a Kaggle dataset `kaggle datasets download <slug> && unzip ... && rm ...`, then the move
  into `local-data-warehouse/<unique_name>/`; for a competition `kaggle competitions download -c <name>`; otherwise
  `wget <url>`. Pin a DOI or an archived release where one exists.
* A source's `bibtex`: the work that published the data. For a Kaggle dataset a `@misc` entry with
  `howpublished = {\url{...}}` and `note = {Kaggle dataset}`. Balance every brace and escape `&`, `%`, `#`, `_` in
  typeset fields; the bundle checks catch broken entries and a key that does not match.
* The task attributes: IID needs nothing beyond `target` and `problem_type` (set `stratify_on = None` only with a
  reason). Temporal: `temporal = Temporal(on=..., splits=TemporalSplits(...))`. Grouped: `grouping = Grouping(...)`.
  A task is grouped or temporal, never both; an order inside groups is `Grouping(time_on=...)`.
* `special_features = (...)`: the model inputs that need handling beyond their dtype, declared like the target
  (`data_foundry.v2.special`). Each entry is one special feature, in one of two layouts:
  * **one column**, a `SpecialColumn`: `Smiles(column="SMILES")`, a molecule's structure (CLEAN-24), cast to `string`;
  * **a group of columns** that hold one object together, a `SpecialColumnGroup`: `Spectrum(name="serum_ms",
    prefix="M/Z:", unit="m/z", technique="mass_spectrometry", state="raw", description=...)`, one numeric column per
    position on a spectrum's axis, named `<prefix><position>` (CLEAN-26). `technique` is `mass_spectrometry`, `raman`,
    `infrared` or `near_infrared`; `state` is `raw`, `processed` or `peaks`, as the source left it; `unit` is `bin`
    when the source gives no axis ([spectra.md](../../knowledge-curation/references/spectra.md)).

  The columns stay features; leave them out of `_feature_types`. The container records each entry in
  `task_metadata.special_features` (`SpecialFeature`: name, kind, layout, columns, `encoding_required`, the recommended
  encoding, a spectrum's details); `special_features(container, kind)` lists them and `encode_special_feature(df,
  feature)` encodes one in place of its columns. A new kind (a shipped embedding, a sequence) is one class in
  `data_foundry.v2.special`'s registry, never a new definition attribute. The recommended encodings of dates and text
  are in `data_foundry.v2.encodings` (`recommended_encodings()`): skrub's `DatetimeEncoder` as BeyondArena for a date,
  TF-IDF and e5 sentence embeddings for text (check both).

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
# 2. Rename columns and the target to meaningful names; fix typos, strip special characters. The target's classes
#    are words (CLEAN-25): binary "No"/"Yes" with "Yes" the event the task predicts,
#    `df = decode(df, {self.target: {0: "No", 1: "Yes"}})`; a multiclass target the source's class names, ordered
#    (`ordinal={target: [...]}`) when they form a scale.
# 3. TODO(verify): drop uninformative identifiers. To keep an id but hide its names (a group id), use
#    `anonymize_ids(df[col])`, never random ids: `uuid4()` changes the data on every run.
# 4. TODO(verify): reverse ordinal codes and true one-hot blocks, restore the labels; yes/no flags that can be set
#    together stay separate columns. A code the codebook names in words is decoded into the words (CLEAN-12), after
#    step 5's `set_missing`: `df = decode(df, CODE_LABELS)` with `CODE_LABELS = {col: {code: "label"}}` at module
#    level (a code without a label raises).
# 5. TODO(verify): proxy missing values and impossible values to NaN, keeping the rows:
#       df = df.replace({"?": np.nan, " ": np.nan})     # UCI style
#       df[col] = df[col].replace(-1, np.nan)           # sentinel style (-1, -9, -999, 999999)
#       df = set_missing(df, {"q7": [8, 9]})           # survey codes: don't know, refused, not asked
# 6. Dtypes by meaning, named in `_feature_types` (not cast here); no `object` column survives. An ordinal scale
#    whose levels the codebook names in words (decoded in step 4), or bands, or a count with an open end, is
#    `ordinal={col: [levels, lowest first]}`, in the order of the codebook (not the order of the codes: it is often
#    reversed); a value that is no level raises, so the codes outside the scale that mean unknown go to `set_missing`
#    first, and a state of its own (no basement) is placed by CLEAN-14. A score with no words per level (a 1-10
#    rating, a points total) stays a number (CLEAN-14). Cast mid-way with
#    `cast_dtypes` only when a later step needs the dtype.
#    A SMILES column ships as a structure (CLEAN-24), declared in
#    `special_features = (Smiles(column="SMILES"),)` (not in `_feature_types`), in RDKit's canonical form:
#       df["SMILES"] = canonical_smiles(df["SMILES"])   # salts as published; stereo kept
#    then check for rows that are copies to a 2D encoding: `canonical_smiles(df["SMILES"], stereo=False).duplicated()`.
#    The benchmark encodes it (recommended: `encode_smiles`, RDKit's 2D descriptors, the MACCS keys and the ECFP4 counts).
#    A spectrum ships as published (CLEAN-26): name its columns `<prefix><position>` and declare it in
#    `special_features` as `Spectrum(name=..., prefix=..., ...)`; never smooth, correct, normalise or align it here:
#    the benchmark encodes it row by row.
# 7. TODO(verify): drop constant, all-missing and duplicated columns.
# 8. TODO(verify): drop leaking features (the traps below; leak_checks.md). The most common step in the collection.
# 9. TODO(verify): duplicate rows: decide and document (leak_checks.md, Copies across the split (LEAK-16 to LEAK-21)).
# 10. TODO(verify): target transform: `np.log` / `np.log1p` a skewed positive target and rename the column; skip it
#     when the source already logged it or a deviance scores the target (CLEAN-16). A count or amount over a realized
#     amount at risk becomes the rate, the amount its weight scoring column and `sample_weight` (MET-14, MET-15).
# 11. TODO(verify): censored or capped target values: decide case by case and document it in `curation_comments`
#     (asp_potassco_classification and sat11_hand_algo_runtime keep a timed-out run at its recorded limit and drop
#     only the instances on which every configuration timed out; a target censored by the download date: LEAK-24).
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
always 3-fold cross-validation, with 20, 10, 3 or 1 repeats by the size of the train side, in the units the metric
scores (the groups of the metric's `group` input, else the groups of `per_group` labels, else the rows; SPLIT-33,
`recommended_dimensions`),
built by `iid_splits` / `grouped_splits` with the benchmark seed, on the full frame: Data Foundry caps no split unless
the definition declares a `row_budget` (a sub-sampled version, below). The comment is "Default splits."; set
`splits_comment` only when there is something to say (a split that deliberately differs from the source's protocol,
what a grouped test fold holds).

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
  chosen by its prediction and scored by its true value under a metric that does not choose by itself. Everything
  else is `row`.
* Algorithm selection (one row per instance and algorithm, the runtime as the target, the algorithm predicted
  fastest is run): the metric chooses. `par_k` takes the instance as its `group` input, picks per instance the row
  with the lowest prediction and counts rows tied there as the mean of their costs. Declare `prediction_unit="row"`
  and no aggregation: the scorer applies an aggregation before the metric, so `select_min` would choose first and
  break a tie by the order of the rows (a constant prediction on sat11_hand_algo_runtime scores 19,140 s, always the
  first solver in the file, against 18,539 s under `par_k`'s rule; trained models did not tie). What the split holds
  out decides where the instance comes from:
  * instances (sat11_hand_algo_runtime): the grouping is on the instance, and the metric reads that column (MET-2);
  * something larger (asp_potassco_classification: problem classes): the grouping is on the class, and the
    anonymised instance ships as `ScoringColumn(column="instance_id", role="group", used_by="par_k")`, never a
    feature.
  sat11_hand_algo_runtime still declares `select_min`; dropping it is open in its `REVIEW.md`.
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
(Lennart, 2026-10-16). A calendar window's gap counts in the window's unit unless `gap_unit` names another
(`"minutes"`, `"hours"` or a calendar unit): `TemporalSplits(window=91, unit="days", n_windows=3, gap=15,
gap_unit="minutes")` leaves 15 minutes for a label known 16 minutes after its row (g_research_crypto_forecasting_1m;
Lennart, 2026-10-22), stored as `time_gap=15, time_gap_unit="minutes"`.

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
| A gap in a smaller unit than the window (g_research_crypto_forecasting_1m: 3 x 91 days, 15-minute gap, whole minutes sampled) | `TemporalSplits(window=91, unit="days", n_windows=3, gap=15, gap_unit="minutes", sample_by="time")` |
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

Data Foundry sets no row budget: by default every split uses the full frame and no side is capped. A definition that
should train and test on fewer rows declares the budget itself, `row_budget = RowBudget(train=..., test=...)` (from
`data_foundry.v2`), which makes it a sub-sampled version. The container records the budget
(`experiment_metadata.row_budget`, None without one), the README states it (`splits.row_budget`), and the split
checks hold the container to it (`splits_train_over_budget` error, `splits_test_over_budget` warning).

TabArena v0.2 sub-samples to 1M train / 500k test rows (Lennart, 2026-10-21: at most 1M training rows). A v0.2
dataset whose splits, without a budget, have a side over that ships only as a sub-sampled version, whatever the size
of its frame (nyc_taxi_trip_duration: 1.45M rows, train sides of 1.28M to 1.39M), and `tests/test_v2_datasets.py`
holds every v0.2 README to it. The version has its own folder and class, `<unique_name>_1m/dataset.py`, with
`unique_name = "<name>_1m"` and `row_budget = RowBudget(train=1_000_000, test=500_000)`; `curation_comments` says
why it is sub-sampled. It reads the raw files of `<name>`, its name without the budget suffix, and is saved under its
own name. The name is `<name>_<suffix>`, the suffix from the train budget (`RowBudget.suffix`: `_1m`; `_10m` for
`RowBudget(train=10_000_000, test=250_000)`, `_2p5m`, `_300k`), for larger versions in large-data experiments. The
splits adapt to the budget:

* IID or grouped data: a frame above `train + test` rows is sub-sampled to it before splitting (`subsample_frame`:
  rows stratified on the target, or whole groups). The usual 3-fold splits are built, then each fold tests on up to
  `test` rows of its third and trains on every other row, at most `train` (`fit_splits_to_budget`; a grouped fold
  up to whole groups). At 1M / 500k that is plain 3-fold cross-validation on 1.5M rows; at 10M / 250k each fold
  trains on 10M and tests on 250k rows of a 10.25M-row frame. A test budget above half the train budget is not
  reached (a fold tests on at most its third). A version whose budget changes nothing (the frame fits and no side is
  over) is an error: take the dataset fully.
* Temporal data: the frame is not sampled. The windows (at least 3) are built on the full data, then
  `sample_temporal_splits` keeps at most `test` rows of each test window and a random `train` of all earlier rows
  for each train side, drawn in one random order so the train sides overlap; the frame keeps only the rows a split
  uses. A temporal version whose windows all fit is an error. When the rows of one time value form a cross-section
  the target or the features are relative to (the 14 coins of a minute), `TemporalSplits(..., sample_by="time")`
  draws whole time values instead of rows: one random order of the values, each side taking whole values while it
  stays within its budget (the value that would cross it is dropped), without stratification
  (g_research_crypto_forecasting_1m; Lennart, 2026-10-22). Random rows would leave about one coin per minute.
  `sample_by` without a `row_budget` is an error.

The rows a version's sampled test sides leave out are never tested; the coverage check (`splits_rows_never_tested`)
does not flag them when the container records a budget. A dataset that sets `splits_comment` itself states the
sub-sampling there.

## Families: one parent, several tasks

Several tasks on the same data (another target, an IID, grouped or temporal split, other preprocessing, a budget
version of a task) share their metadata and cleaning through a parent definition instead of copying it. Each member
is still its own folder, `<root>/<unique_name>/dataset.py`, and ships its own container: one task per container.

```python
# exam_scores/dataset.py: the parent (no `target`)
class ExamScores(AbstractCuratedDataset):
    data_summary = DataSummary(data=..., row=..., goals=..., limits=...)   # required on a parent
    unique_name = "exam_scores"
    domain = ...
    sources = (Source(..., files=("*.csv",)),)   # one file per school, listed in `raw_files`
    download_description = ...   # the family's raw files, read by every member
    non_features = (             # kept in the frame, never a feature: every task drops them
        NonFeature("math_score", "outcome", "The math score of the exam."),
        NonFeature("reading_score", "outcome", "The reading score of the same exam."),
        *provenance_columns(),   # source_file, source_row, source_id
    )
    def _load_raw(self, raw_dir):
        return read_files(raw_dir, "*.csv")   # stacks the files and records where each row comes from
    def _clean(self, raw): ...   # the shared cleaning

# exam_scores_math/dataset.py: a child (a task)
ExamScores = import_definition("exam_scores")

class ExamScoresMath(ExamScores):
    unique_name = "exam_scores_math"
    derivation = "The math score as the target; the reading score, written at the same exam, is dropped."
    task_summary = TaskSummary(...)
    target = "math_score"        # a declared outcome given a role: kept
    problem_type = "regression"
    metric = Metric.fallback(reason=...)
    # the reading score and the provenance columns are dropped by the standard steps
```

* **Kinds.** A definition without a `target` is a parent: it is never built and never discovered as a dataset
  (`discover_datasets` returns tasks; `discover_definitions` returns both). A parent declares `data_summary` (what the
  data is, independent of one task) and may declare the task defaults its children share (`problem_type`, `metric`,
  `grouping`, `temporal`, `stratify_on`, `scoring_columns`, `special_features`, the weights), but no `row_budget`,
  `task_summary`, `splits_comment` or regime tag. A parent without `_load_raw` or full metadata is partial: it shares
  code only, and its children complete it.
* **A child** subclasses its parent, imported with `import_definition("<parent>")` (the sibling folder). It declares
  its own `unique_name`, named `<parent>_<variant>` after what differs (`_cop`, `_grouped`, `_clf`; a row budget's
  suffix last, `<parent>_<variant>_1m`), and `derivation`: how it differs from its parent. It may override any hook
  and call `super()` (`_clean`, `_feature_types`, `_make_splits`, `_decisions`); it inherits everything else.
* **Raw files** belong to the definition that says how to download them (`download_description`): the family root
  when it does, and every member reads that folder. A child does not redeclare `download_description`,
  `_prepare_raw_files` or `prepared_raw_files` that a parent declares.
* **Summaries.** A child inherits the parent's `data_summary`, shown above its own `task_summary` in its README. An
  inherited `task_summary` or `splits_comment` is refused when the child's task differs (target, problem type,
  grouping, temporal); `dataclasses.replace(Parent.task_summary, split=...)` changes single fields.
* **Never features.** The parent keeps every outcome (both scores) and declares it in `non_features`, with the
  provenance columns; each task drops every declared column after `_clean` unless it gives one a role (its target,
  `grouping.on`, a scoring or weight column), since an outcome measured with the target is not known at the
  prediction point (LEAK rules). Section "Columns that are never features" below.
* **The container** records the parent: `dataset_metadata.derived_from` (its `unique_name`) and `derivation`. A
  benchmark groups the tasks of one family by it.
* **Checking.** `dataset check <parent>` checks the parent as data: its frame (in content order), a data checksum, its
  sources and columns, the children found next to it, and the definition findings (`parent_without_children` when
  none derives from it). `dataset build` refuses a parent. A child's check scans the definition files of its parents
  too (`TODO(verify)` markers, nondeterministic calls), and the workbench reloads a child when a parent file changes.
* **Trying a task.** In a notebook next to the parent, `class Try(import_definition("<parent>")): ...` with a target
  and a split runs `check()` without a folder: it writes no README and cannot be built.
* **Scaffold.** `dataset new <parent>_<variant> --parent <parent>` writes a child with the TODOs to fill in.
* **Example.** [`examples/dataset_family/`](../../../../examples/dataset_family/) holds a family (exam scores: a parent
  and two tasks), a README on the idea and `run_family.py`, which runs it on generated raw files.

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
* An amount at risk (time insured, area swept) or a span that the outcome can cut short: a realized one is the rate's
  weight, never a feature (LEAK-41, MET-15).
* Proxy and impossible values.
* Rare classes and merged labels.
* The source's split protocol, taken as a claim.
* Top solutions' preprocessing without their exploits.
* Anonymized data: keep it as it is, tag `Anonymized` (and the record's `Anonymized` marker), and say what could not
  be determined.
* Destroyed meaning to reconstruct.
* Classes recorded differently: "check number formats and missingness per class (probes 3, 9, 17); do two same-label
  subgroups separate, or rows of one class that share a format the other class rarely has (LEAK-39)? Are there
  straight-line fills in the raw order (probe 18, LEAK-40)?" Whatever is found, fixed or not, is one `curation_comments`
  bullet that starts ``Class-dependent recording (record marker `Class-dependent Recording`):``: what was recorded
  differently and how it splits by class, the score of the recording alone (before and after a fix), and what was done:
  harmonised, dropped, kept with the reason, or `Not harmonised yet:` with what the fix would cost. The record gets the
  marker and a short evidence note (LEAK-13 to LEAK-15, LEAK-39 and LEAK-40 in
  [leak_checks.md](../../knowledge-curation/references/leak_checks.md)).
* Cohort and selection, right truncation.
* A label read off a later stage.
* Definition bugs the audit found in shipped datasets: a numeric column listed as categorical (a 125k-level category in
  give_me_some_credit); a target stored as `log1p` with metric `rmsle` and no
  `target_transform`, which logs it again (santander_transaction_value); BibTeX citing a different competition
  (sberbank_housing_market_forecasting); a tag in a source's `license` (cirrhosis: `"IID"`). Read the class
  attributes once more for these before handing off.

## Columns that are never features: `non_features`

`non_features = (NonFeature(column, reason, description), ...)` declares columns a definition keeps in its frame but
no task may use as a feature. The reasons: `outcome` (a result measured with or after the target, such as a second
score of the same exam), `provenance` (where a row comes from: its file, row number, id), `identifier` (a key with no
meaning as an input; a running id often encodes the order of collection or the origin) and `other` (with a
`description` saying why).

* A parent declares them; its children inherit them and may add more (`non_features = (*Parent.non_features,
  NonFeature(...))`), never remove one. A standalone task may declare them too.
* The standard steps drop every declared column after `_clean`, unless the task gives it a role: its target, a group
  or time key, a scoring or weight column. So `revenue` declared as an outcome is the target of one child and dropped
  by another, and a `source_file` declared as provenance may be the group key of a task that holds files out.
* The parent's README lists them ("Never features"); a task's README names the ones it dropped. Nothing about them
  enters the container: a task container holds only its features, target and the columns its task uses.
* A declared column that the declaring definition's `_clean` does not return stops the run (a misspelling).

## Assembled from several files: `read_files`

`read_files(raw_dir, "*.csv")` (from `data_foundry.v2`) stacks the files that match a pattern, in the order of their
sorted paths, and adds three columns: `source_file` (the file's path under the raw folder), `source_row` (the row's
number in its file, from 1) and `source_id` (the file's own id column with `id_column=...`, else a hash of the row's
values, which survives a re-saved or reordered file). `(source_file, source_id)` identifies a row. `read=` takes
another reader (`pd.read_parquet`, `partial(pd.read_csv, sep="\t")`). Declare the three columns with
`non_features = (*provenance_columns(), ...)`, so every task drops them.

## The raw-file manifest

A source that names its files (`Source(files=("*.csv",))`) gets them listed in the container's dataset metadata,
`raw_files`: each file's path, SHA-256, size, source and the rows it gave (counted on `source_file`). With the build's
git commit, the hashes pin what a container was built from: a changed file changes the checksum. The hashes are
cached in the raw folder (`.raw_manifest.json`, by size and modification time), so a large file is read once. The
README front matter records them, and the next check compares: `raw_files_changed` (warning) names the files that
changed, appeared or went; `raw_files_missing` (error) a pattern that matches no file.

## Bundle checks and what to do at scaffold time

`dataset check` runs them (and `dataset build` refuses to save on an error). Pre-empt them:

| Check slug | Scaffold action |
|---|---|
| `dataset_index_range` | handled by the base class |
| `dataset_object_dtype` | name every non-numeric column in `_feature_types` |
| `dataset_identifier_column` | drop uninformative identifiers (recipe step 3) |
| `dataset_sequential_id_column` | an integer column numbered densely, one value per row (a running id): drop it, or declare it `NonFeature(column, "identifier")` in the parent |
| `raw_files_missing`, `raw_files_changed` | a source's `files` pattern matches nothing; a raw file differs from the README's (the raw-file manifest) |
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
| `task_metric_*` | declare `metric` with its origin and reference, the canonical name and the params and inputs the metric takes; each input column a `ScoringColumn` (Field mapping, `metric`) |
| `task_sample_weight_not_metric_weight`, `task_weight_invalid`, `task_rate_count_not_whole`, `task_feature_looks_like_exposure` | a count or amount over a realized amount at risk: build the rate in `_clean` (assert that target x weight rebuilds the count), ship the amount as the weight scoring column the metric reads and as `sample_weight`, never as a feature (MET-14, MET-15, LEAK-41); a feature named like an amount at risk that is known at the prediction point is accepted with that reason |
| `task_stratify_*` | stratify on the target (classification) or a discrete feature |
| `task_time_on_dtype`, `task_time_on_missing_values`, `task_time_on_not_sorted` | a datetime (`_feature_types`) or numeric time column without NaN; the base class sorts |
| `task_group_labels_per_group_violated`, `task_group_on_unique_per_row` | pick `per_group` or `per_sample` correctly |
| `splits_temporal_leakage`, `splits_temporal_order` | expanding train, newest window first |
| `splits_rows_unused` | IID and grouped splits cover every row |
| `splits_train_over_budget`, `splits_test_over_budget` | a split side over the container's `row_budget` (only a version with a budget is checked; format 1 keeps the v1 1M / 250k): the splits of a custom `_make_splits` must keep to it ("Larger than the row budget") |
| `splits_too_few` | a temporal task with fewer than 3 test windows: declare at least 3 |
| `meta_time_horizon_missing` | a fixed-length window in `Temporal(splits=...)`, or `Temporal(horizon=..., horizon_unit=...)` |
| `meta_time_gap_without_time_on` | a gap belongs to a temporal task |
| `groups_test_groups_few` | fewer than 20 test groups in a fold: keep only with real signal across groups (`group_probes.py`) and more than a handful of groups of each class per fold (else `Too Small`), and accept with that evidence |
| `groups_largest_share_high` | one group over 20% of the rows: check it is one entity, not a catch-all value |
| `groups_labels_constant` | `per_sample` with at least 95% single-label groups: `per_group` if one label by construction, else accept with the count of mixed groups |
| `groups_not_clustered` (info) | rows no closer to their group than chance: compare IID and grouped scores before keeping the grouping |
| `splits_test_single_class`, `splits_test_target_constant` | a test fold whose metric is undefined: fewer, larger folds or windows, or the task is too small |
| `splits_test_minority_few`, `splits_test_class_missing` | test folds with under 10 rows of the rarer class, or without some class: widen the windows, merge by convention, or accept with the counts |
| `task_target_value_dominant` | one value holds half of a regression target: name the cap, timeout, placeholder or zero inflation in `curation_comments`; keep or drop censored rows case by case (sat11_hand_algo_runtime keeps its timeouts at the recorded limit), or accept with the reason |
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

## Metrics

Which metric a dataset declares is decided by [metrics.md](../../knowledge-curation/references/metrics.md); this is
how a custom one gets into the library. The registry is `METRICS` in `src/data_foundry/v2/metrics.py`; it is also the
list of names the bundle checks know. The module imports only numpy, pandas, scikit-learn and scipy (a test refuses any
other Data Foundry import), so it can be copied out on its own.

A custom metric is added in the same change as the dataset that needs it (MET-13), under a general name (MET-12):

1. Write `fn(y_true, y_pred, *, labels=None, params, **inputs) -> float`. `y_pred` follows the module's conventions
   (`proba`: the positive class's probability or one column per class in `labels` order; `label`; `value`); `params`
   holds the JSON values of the spec (a matrix, `k`, weights); each input role (`group`, `weight`, `time`) arrives as
   an array aligned with `y_true`. Use the fastest well-tested code: scikit-learn or scipy where they cover the metric,
   otherwise vectorised numpy (a per-group metric through `np.unique(..., return_inverse=True)` and `np.bincount`, or
   a pandas `groupby`, never a Python loop over rows); for a competition whose official code is slow, start from the
   faster versions posted in its discussions or notebooks and check them.
2. Register a `MetricDef` with `kind="custom"`: `name`, `problem_types`, `prediction`, `greater_is_better`, `fn`,
   `implementation` (what it calls), `definition` (one line a reader can implement from), `inputs` (the roles it
   needs), `params` (each param with a short description), `predictions` (other prediction kinds a param may choose,
   such as a cost matrix scored on probabilities), `check_params` (raises a `ValueError` on a missing matrix or a bad
   `k`, so a wrong definition fails when `dataset.py` is imported) and `reference` (where the metric is defined and the
   official code it is tested against).
3. Test it in `tests/test_v2_metrics.py`:
   * equal to the official implementation on random inputs, to 1e-9 or exactly, over several seeds and sizes, with ties
     and with a class missing from a fold where the metric allows it; when the official code cannot run in the test
     environment, a faithful transcription of it in the test file, with its link;
   * one case computed by hand, with the arithmetic in a comment;
   * a fold it cannot score (a single class, an empty group): NaN or a clear `ValueError`, never an infinite value,
     which `task_metric_not_computable` reports;
   * its time on 1M rows (with a realistic number of groups), reported in the test's output or the PR, and fast
     enough to score every fold of a benchmark run;
   * the stability checklist below, which `tests/test_v2_metrics_stability.py` runs on every registered metric (a
     metric with required params needs an entry in its `EXAMPLE_PARAMS`).
4. In the definition, declare it (`Metric.source("cost_matrix", params={...}, reference=...)`), declare every input
   column as a `ScoringColumn`, and run `dataset check`: `task_metric_not_computable` scores a random prediction on
   every split, so a test fold that lacks what the metric needs shows up there (MET-2).

### Metric stability

A benchmark scores every model on every fold, so a metric must not break on a prediction a model can make or on a
fold at the edge of what it measures (MET-13, amended 2026-11-05, Lennart). Every metric in `METRICS`, standard or
custom, meets this checklist; `tests/test_v2_metrics_stability.py` checks items 1 to 4 for every registered metric,
and the rest is checked when the metric is written or reviewed.

1. **Any prediction a model can make gets a finite score**, without scikit-learn's warnings of an ill-defined value:
   constant, tied, 0, negative and huge values, probabilities of exactly 0 and 1, a class never predicted. A constant
   baseline is a model too.
   * A correlation of a constant prediction is 0, no skill, where scipy gives NaN (`pearsonr`, `spearmanr`,
     `weighted_pearsonr`, and per group `mean_group_pearsonr`).
   * A prediction outside the metric's domain is floored, not refused: `rmsle` at 0, the Poisson and Tweedie
     deviances at `min_prediction` (with `prediction_domain="positive"`, so the bundle check draws valid dummies).
     The three deviances require the floor, with no library default (`task_metric_param_invalid` without it): the
     definition states it at the lowest value the use case's actor acts on, with its fact, never above the smallest
     plausible mean on the scale the metric scores (MET-13 as amended 2026-11-09; 1e-4 claims per year on fremtpl2 and
     bemtpl97), and `task_probes.py` reports the share of predictions at it. The floor
     sets the scale of the worst error: one claim predicted at f costs `2 * (log(1/f) - 1 + f)` in Poisson deviance
     (25.6 at 1e-6, 16.4 at 1e-4), and above power 1 a Tweedie deviance charges a claim about `y * p^(1-q)`, so a 2000
     EUR claim predicted at 0 costs about 2e6 at a floor of 1e-6 and 2e3 at 1 EUR. No per-row cap: it makes the
     deviance improper (MET-13).
   * Precision, recall and F1 pass `zero_division=0.0`: the value scikit-learn uses anyway, without the warning.
2. **The score does not depend on the row order.** Tied predictions count by the mean over their orderings (the
   expected share at a cut-off, a tied block's mid position in a cumulative curve, the mean of tied candidates), as in
   `precision_at_k`, `normalized_gini`, `normalized_weighted_gini`, `gini_top_capture`, `par_k` and
   `mean_group_top_k_overlap`. Never `argsort(kind="stable")` or "the first row". Official code often breaks ties by
   row order; the library's value equals it without ties, and the docstring says where it departs.
3. **A NaN or infinite prediction raises a `ValueError`.** `score()` checks the predictions (and a regression
   target) before the metric and again after the inverse of `target_transform`, where a huge log prediction
   overflows. A metric never returns NaN for a bad prediction, nor a score that quietly skipped the row.
4. **A fold whose truth leaves the metric undefined gives NaN**, or a clear `ValueError`: one class (`roc_auc`,
   `average_precision`, `gini_top_capture`), a constant target (the correlations, the normalized Ginis), no loss at
   all, no septic patient (`normalized_early_detection_utility`), a true value of 0 in a ratio (`mape`; `rmspe` leaves
   such rows out, as its competition did). Never an infinite value, a `ZeroDivisionError`, or a number made of
   rounding noise. `task_metric_not_computable` flags a non-finite score on any shipped split, so such a fold never
   ships.
5. **A group that cannot tell models apart is left out, and the docstring says so**: a group whose truth does not
   vary (`mean_group_pearsonr`, `mean_group_normalized_rmse`), a period with one class (`gini_stability`), a group of
   `k` rows or fewer (`mean_group_top_k_overlap`, where every model scores 1). NaN when every group is left out. The
   groups kept keep their positions: `gini_stability` fits its line over each period's own index, so a period left
   out does not shift the later ones.
6. **Degeneracy is decided on the values as given**, never on a computed variance or the result of a division:
   `np.ptp(y) == 0` (or a range below 1e-12 of the group's largest absolute value), not `var > 0`. A constant 0.1
   leaves a variance of about 1e-34 from rounding in the mean, which divides an error into about 1e17.
7. **Every denominator is checked before the division**: a sum of weights, the score of the perfect order (a Gini of
   the perfect order is 0 when every loss is equal), a per-group count, the best-minus-baseline of a normalized score.
   `np.errstate` only silences a branch whose result is then replaced, never a value that is returned.
8. **A scale-free metric stays in its range**: a metric of shares, ranks or relative errors cannot be dominated by
   one row through a divisor near 0. Normalize by the truth's spread only where the spread is guarded (item 6).

`Metric.local(fn, ...)` runs code that only the definition holds. It is for a user's own dataset that is never
shipped; the working copy never uses it.

## Reference definitions

Read the closest one in full before writing (paths under `datasets/_dev/tabarena-v0pt2/`):

| Regime | Reference | What it shows |
|---|---|---|
| IID | `tour_travels_churn/dataset.py`, `forensic_glass_identification/dataset.py` | The minimal definition: attributes, `_load_raw`, a short `_clean`. |
| Grouped | `airfoil_self_noise/dataset.py`, `early_learning_predictors/dataset.py`, `musk/dataset.py`, `emscad/dataset.py` | `Grouping` with a `definition` citing the source (airfoil: a setup built from two columns, with the source's prediction use quoted; musk: one prediction per molecule, `aggregation="any"`), rule-based leak drops in `_clean`, long feature lists (early_learning), a group id built from the data and an accepted group finding (emscad). |
| Temporal | `kick/dataset.py` | `TemporalSplits(window=None, unit="unique", n_windows=9, min_train_fraction=0.5)`, a datetime in `_feature_types`, and `_decisions` with a table and a figure. |
| Temporal with late labels | `brazilian_ecommerce/dataset.py`, `sf_permit_time/dataset.py` | `_make_splits` training on rows whose label had arrived, with the gap on `Temporal`. |
| Sub-sampled `_1m` | `sepsis_prediction_1m/dataset.py` (grouped), `delivery_eta_1m/dataset.py` (temporal) | `row_budget = RowBudget(train=1_000_000, test=500_000)` with the name `<name>_1m`, grouped labels per sample; 3 weekly `TemporalSplits` with a `splits_comment` that states the sub-sampling. |
| Heavy raw data | `acquire_valued_shoppers_challenge/dataset.py` | `prepared_raw_files` + `_prepare_raw_files` (a polars join run once), fixed calendar windows. |

## What the benchmark harness does with a definition

* v0.2 runs a new default pipeline like BeyondArena's, which keeps the hour of a datetime (skrub's `DatetimeEncoder`);
  only the v0.1 pipeline dropped it (Lennart, 2026-10-12). Do not add hour columns to work around it. Nothing changes in
  a definition while the v0.2 runs encode datetimes with the hour (Lennart, 2026-10-21: "we will always run with
  datetime encoding in v0.2, most likely some evolution of tabarena_default"). nyc_taxi_trip_duration_1m and
  pkdd_15_taxi_trip_time_prediction_ii_1m, whose only time feature is a datetime, show what is at stake (LightGBM RMSE
  0.357-0.381 with the hour against 0.414-0.441 with AutoGluon's date parts; R^2 0.482-0.503 against 0.452-0.483), and
  checks and probes may use them to test an encoding.
* A group column is split and scoring metadata, never a feature; the harness drops it before fitting
  (`datasets/_dev/tabarena-v0pt2/BENCHMARK_CHANGES_TODO.md` lists what the harness still needs, such as per-group
  scoring and custom metrics).
* The declared metric changes no score yet: TabArena's adapter scores only `roc_auc`, `log_loss` and `rmse` and does
  not read the `objective_metric` spec; supporting it, the custom metrics and the scoring columns is an entry of
  `BENCHMARK_CHANGES_TODO.md`. Nor does it pass a task's `sample_weight` to the fit: a container that declares one
  enters no run until the adapter fits every model with it (the entry "Training weights").
* String columns are embedded by the pipeline, so a definition ships text as `string`, and molecules as RDKit
  descriptors.
