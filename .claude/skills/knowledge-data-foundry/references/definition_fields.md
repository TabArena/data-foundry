# Definition fields: record to definition

The field-by-field mapping from a curation record to the attributes of a `dataset.py` class: what each attribute
holds, its allowed values and the house conventions. The guide to writing a definition (the folder, the base class,
the preprocessing recipe, the splits, the checks and how decisions are recorded) is [definitions.md](definitions.md).

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
    The container lists them with their SHA-256, size and rows (`raw_files`; [definitions.md](definitions.md), "The
    raw-file manifest").
* `data_tags`: context tags only, since listing a regime tag yourself switches the automatic ones off. `"Anonymized"`
  when the source hid what the features are, by replacing their names or values on purpose (common for competition
  data; the record gets the `Anonymized` marker, and the cases without it are in
  [selection.md](../../knowledge-curation/references/selection.md), "Anonymized data"); `"Spatial"` when the data
  holds geographic information (ZIP, latitude and longitude, region, store location). An IID or grouped split carries
  one time basis that says why it is not temporal (SPLIT-32 in
  [splits.md](../../knowledge-curation/references/splits.md)), declared as `time_basis = TimeBasis(tag, reason)`
  (`from data_foundry.definition import TimeBasis`), never as a tag in `data_tags` or a line written by hand: the build
  adds the tag to `data_tags` and renders the reason as the `- Time basis: <tag>: <reason>` bullet of
  `curation_comments`, which the container and the README carry. The tag is a use-case prototype, `"Timeless"` (the
  target is a fixed property of the item, and the data has no time dimension, or its time changes only which items are
  held, as in a catalogue whose entry date does not decide the split), `"RetrospectiveFillIn"` (the data is one snapshot
  of a moment or period, and the use case fills in what is missing for that time, not a later one; a definition refuses
  the old name `"Retrospective"`, which containers built before 2026-11-23 carry and are read with),
  `"StationaryRelation"` (the use case scores later units, too few periods give the windows SPLIT-14 asks for, and the
  stationary-relation test over the periods held, dated or a rebuilt order, reads the relation flat; it replaces a
  forced tag) or `"UnseenGroup"` (the use case aims at groups the data does not hold, a site, a well, a protein or a
  chemical family, not at a later period; it needs a `grouping` on the group); or a forced tag,
  `"ForcedIIDFromTemporal"` when a forward use case has no usable time or too few periods and ships IID (a definition
  that declares a `grouping` or `temporal` refuses it), `"ForcedGroupedFromTemporal"` when such a task ships grouped (it
  needs a `grouping`; SPLIT-8). `"AssumedStationaryRelation"` replaces a forced tag where a person judged earlier and
  later samples interchangeable for a reason from the dataset's domain or use case and nothing can be measured (no
  comparison over time is possible, or the stationary-relation test is inconclusive); the split is then random, or
  grouped by the unit where a unit has several rows and the use case meets new units. Only a person sets
  `StationaryRelation` (on the measurement) and `AssumedStationaryRelation` (on a reason): never set them yourself
  unless a person asks (you may offer and recommend them in a review), and give `set_by` and `on`, which render as
  `<tag> (<person>, <YYYY-MM-DD>):`:

  ```python
  time_basis = TimeBasis(
      "StationaryRelation",
      "the stationary-relation test reads flat pooled over 2023 and 2024 (LightGBM +0.001 +- 0.010, floor 0.003) ...",
      set_by="Lennart",
      on="2026-11-22",
  )
  ```

  The reason states the fact behind the tag and ends with what the split cannot test; a forced tag's reason names
  why (time lost, or too few periods) and what a dated release would change. `group_basis = GroupBasis(reason)` sits
  beside the time basis when the use case holds out a group of distinct items the data cannot key (no structure for a
  scaffold, no stand id or coordinates, a single site): it adds `"ForcedIIDFromGrouped"` and the `- Group basis:`
  bullet, naming the group, why it cannot be keyed and the overlap left, and marks an IID split (SPLIT-35). A definition
  refuses a malformed declaration, a prototype on a temporal split, a regime the tag contradicts, a human-set tag
  without a person, a date and a reason of eight words or more, and a time-basis tag or line written by hand beside
  `time_basis` (`data_foundry.time_basis` holds the rules, which `dataset check` applies to a built container too).
  A forced tag in `data_tags` and a free-text line without `time_basis` are refused; `dataset check` still notes them
  on an old container (`meta_time_basis_unstructured`).
  `dataset check` also notes a split that is not temporal and says nothing about why, and date columns in the data of
  such a split unless the basis is `RetrospectiveFillIn` or a forced tag's line gives the reason; it prints where the
  curation record's collection type and facts contradict the definition (`data_foundry.curation.consistency`).
  `split_leaf = "L-FILL.unit"` names the leaf of the split decision tree
  ([split_tree.md](../../knowledge-curation/references/split_tree.md), SPLIT-36) the split comes from, by its ID; the
  tests check that the leaf exists and that the definition ships its split and tag, unless the tree lists the
  definition as a departure from it.
  `"2ndTierData"` is retired (2026-10-21): old containers that carry it still load, but a new definition refuses it;
  write the doubts as a finding and the fit as `approximate`.
* `problem_type`: "Regression" to `"regression"`, "Binary Classification" to `"binary_classification"`,
  "Multiclass Classification" or "Classification" to `"multiclass_classification"`. A table that supports a regression
  or a classification target, where taking one means dropping the other, gets one folder per framing: the second is
  `<unique_name>_clf/` (or `_reg/`) with its own `unique_name` and its own definition, and the record's
  `problem_type` follows the one that ships.
* `metric` (required): a `Metric` from `data_foundry.metrics`; which one is decided by
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
  model's inputs without the target, the group column, the scoring columns and a time column that dates the label
  (`Temporal(..., time_of="label")`); all of them come from `non_feature_columns(task)`, which the probes call too.
  `scorer(container)` takes the scoring columns' values by row index: `scorer(container)(y_test, y_pred, test_idx)`. It
  reads class probabilities in the sorted order of the classes (scikit-learn's `classes_`), also for an ordered target,
  whose declared order stays type information; a DataFrame whose columns are the class names is matched by name, and a
  missing or unknown class name is an error (Lennart, 2026-11-05). Before declaring a metric with inputs, check on the
  data that every test fold holds what it needs (MET-2).

  A row weight makes each row count in proportion to it: `normalized_weighted_gini`, `weighted_pearsonr` (without
  `weights`), `rescaled_mean_tweedie_deviance` (its required `weight`; since 2026-11-08: each scored set's predictions
  multiplied by `sum(w * y) / sum(w * p)`, then the weighted Tweedie deviance, the stand-in for a pricing game's market
  that rescales every tariff to one total, pricing_game_2016_french_fleet), the optional `weight` input of
  `mean_poisson_deviance` and `mean_tweedie_deviance` (`sum(w * d) / sum(w)`, as scikit-learn's `sample_weight`) and of
  `rmse` (`sqrt(sum(w * (y - p)^2) / sum(w))`, since 2026-11-08: boreal_postfire_lichen_biomass weighs each quadrat by 1
  over its plot's quadrats, so each plot counts once), and `ordered_lorenz_gini` with `params={"per_unit": True}`, where
  the target and the prediction are already per unit of the weight (a loss per year insured; the unnormalised weighted
  Gini). Without `per_unit` its weight is the base premium that totals are compared against, not a row weight.
  `data_foundry.metrics.row_weight_column(spec)` returns a spec's row-weight column, or `None`. The regression
  fallback takes the weight too (`Metric.fallback(reason=..., inputs={"weight": ...})`); the spec of a weighted `rmse`
  states the weighted formula, while the unweighted spec keeps `sqrt(mean((y - p)^2))`, so the containers built before
  keep their checksum. The three deviances require `min_prediction`, the floor on the predicted mean, the lowest value
  the use case's actor acts on, stated with its fact, never above the smallest plausible mean on the scale the metric
  scores (MET-13 as amended 2026-11-09; `1e-4` claims per year for fremtpl2 and bemtpl97, $10 for noaa_storm).
  `score()` refuses an input the metric does not take, so a weight is never dropped without notice.

  The build writes the spec into the task metadata as `objective_metric`: `name`, `kind` (`standard` or `custom`),
  `prediction` (`proba`, `label`, `value`), `greater_is_better`, `origin`, `params`, `inputs`, `original`,
  `reference`, `definition` (a one-line formula), `reason` and `target_transform`; a reader without Data Foundry can
  implement the metric from these fields. `describe()` and the README show it with the scoring columns. The bundle
  checks: `task_metric_undeclared` (a fallback without a reason), `task_metric_unknown`, `task_metric_not_canonical` (an
  alias), `task_metric_problem_type_mismatch`, `task_metric_unknown_param`, `task_metric_param_invalid` (error: params
  that fail the registry's validation, such as a Poisson deviance without `min_prediction`), `task_metric_input_missing`
  (a role the metric needs is not mapped), `task_metric_input_is_model_input` (info: the metric reads the task's group
  or time column), `task_metric_input_is_feature` (warning: the metric reads a plain feature; ship a scoring copy),
  `task_metric_reference_missing` (a source or stand-in without a link),
  `task_metric_stand_in_incomplete`, `task_metric_not_computable` (no finite score of a random prediction on some fold),
  `task_metric_transform_not_regression`, `task_metric_transform_overflow` (the inverse of
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

  A weight for training alone (MET-16: a design weight when sampling depends on the outcome, a label's precision) is
  the `sample_weight` too, its scoring column declared `used_by="training"` and left out of the metric's `inputs`:

  ```python
  sample_weight = "replicate_weight"
  scoring_columns = (ScoringColumn(column="replicate_weight", role="weight", used_by="training",
                                   description="replicate measurements behind the mean label; trains, does not "
                                   "score, since each compound is one decision"),)
  ```

  The checks then accept it as the training weight and no unused scoring column; it is never a feature, and a harness
  still weights a validation loss by the metric's weight (`validation_weight(container)`), not by this one.
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
  (`data_foundry.special`). Each entry is one special feature, in one of two layouts:
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
  `data_foundry.special`'s registry, never a new definition attribute. The recommended encodings of dates and text
  are in `data_foundry.encodings` (`recommended_encodings()`): skrub's `DatetimeEncoder` as BeyondArena for a date,
  TF-IDF and e5 sentence embeddings for text (check both).
