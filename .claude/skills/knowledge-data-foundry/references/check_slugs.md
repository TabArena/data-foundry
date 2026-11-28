# Check slugs

Every slug a Data Foundry check can emit, generated from `src/data_foundry/checks/registry.py` by
`.venv/bin/python -m data_foundry.checks.registry > .claude/skills/knowledge-data-foundry/references/check_slugs.md`;
do not edit it by hand. *Acceptable* says whether `accepted_check_warnings` may list the slug: a warning or
an info always, an error only for the reason given. What to do about each finding is in
[definitions.md](definitions.md), "Bundle checks", and [checks_and_probes.md](checks_and_probes.md).

Errors a definition may accept:

* `splits_test_too_small`: SPLIT-14 lets the curator make an exception when the use case fixes the test window, as a
  factory day of garments_worker_productivity (17-24 team records, accepted 2026-11-19).

## definition

| slug | severity | acceptable | what it means |
|---|---|---|---|
| `accepted_check_warnings_unused` | info | yes | An accepted slug no longer fires, or is misspelled. |
| `definition_no_use_case` | error | no | `TaskSummary(fit='none')`: the dataset simulates no decision. |
| `definition_nondeterministic` | error | no | `dataset.py` calls code whose result can change between runs or machines (an unseeded random step, an unstable sort, an unsorted file listing). |
| `definition_summary_long` | warning | yes | A `task_summary` field is longer than the word limit. |
| `definition_summary_missing` | error | no | The definition has no `task_summary`. |
| `definition_time_changed_in_split` | warning | yes | `_make_splits` changes the time column after the rows were ordered by it. |
| `raw_files_changed` | warning | yes | The raw files differ from those the README was written from. |
| `raw_files_missing` | error | no | A `Source(files=...)` pattern matches no file in the raw folder. |
| `splits_test_too_small` | error | yes, the error too | A temporal test window holds fewer than 33 scored units. |
| `splits_train_under_floor` | error | no | A temporal window trains on less than 30% of the rows. |
| `splits_train_under_half` | warning | yes | A temporal window trains on less than half the rows: the curator's exception (SPLIT-14). |
| `time_newest_period_short` | warning | yes | The newest 30 days hold far fewer rows a day than the spans before: often a release cut before the outcomes were complete. |

## frame

| slug | severity | acceptable | what it means |
|---|---|---|---|
| `dataset_all_missing_column` | warning | yes | A column is missing in every row. |
| `dataset_column_names` | error | no | A column name is not a string. |
| `dataset_conflicting_duplicate_rows` | warning / info | yes | Rows share every feature but differ in the target (a warning from 1% of the rows). |
| `dataset_constant_column` | warning | yes | A column holds a single non-missing value. |
| `dataset_duplicate_column_names` | error | no | Two columns have the same name. |
| `dataset_duplicate_columns` | error / warning | not the error | Two columns hold the same values (an error when one is a copy of the target). |
| `dataset_duplicate_rows` | warning / info | yes | Exact duplicate rows (a warning from 1% of the rows). |
| `dataset_duplicates_skipped` | info | yes | The duplicate row and column checks were skipped: the frame is over the cell budget. |
| `dataset_empty` | error | no | The frame has no rows or no columns. |
| `dataset_identifier_column` | error / warning | not the error | A column identifies the row: one category or string value per row, or an integer numbered densely like a running id; an error when it is the group key, one group per row. |
| `dataset_index_range` | error | no | The frame's index is not `RangeIndex(0, n)`. |
| `dataset_missing` | error | no | The container has no frame loaded. |
| `dataset_missing_value_label` | warning | yes | A category or string column holds levels that look like a missing value (`?`, `n/a`, `null`). |
| `dataset_missing_value_sentinel` | warning | yes | A numeric column is dominated by a value that looks like a missing-value code (-1, -999, 9999). |
| `dataset_object_dtype` | error | no | A column has `object` dtype. |
| `dataset_pure_feature_value` | warning | yes | A frequent feature value determines the class on its own: a possible leak. |
| `dataset_pure_feature_value_skipped` | info | yes | The pure-feature-value check was skipped: the frame is over the cell budget. |
| `dataset_row_order_leaks_target` | warning | yes | The target correlates with the row position: the frame looks ordered, not shuffled. |
| `dataset_smiles_column` | error / warning | not the error | A SMILES column is not a string column, or holds SMILES the pinned RDKit cannot parse. |
| `dataset_smiles_unchecked` | info | yes | A SMILES column was not parsed (RDKit is not installed). |
| `dataset_special_feature` | error | no | A special feature names columns that are not in the frame. |
| `dataset_spectrum` | error / warning | not the error | A spectrum's columns are not numeric or not finite, or miss intensities. |
| `dataset_spectrum_negative` | info | yes | Raw mass spectra hold negative intensities. |
| `dataset_unused_categories` | warning | yes | A category column declares categories that never occur. |
| `test_dataset_dtype_mismatch` | error | no | The unlabeled test set's dtypes differ from the frame's. |
| `test_dataset_extra_columns` | error | no | The unlabeled test set has columns the frame lacks. |
| `test_dataset_index_range` | warning | yes | The unlabeled test set's index is not a range from 0. |
| `test_dataset_missing_columns` | error | no | The unlabeled test set lacks columns of the frame. |

## task

| slug | severity | acceptable | what it means |
|---|---|---|---|
| `task_feature_looks_like_exposure` | warning | yes | A feature looks like an amount at risk (time insured, area swept), which is a weight, never a feature. |
| `task_group_labels_mismatch` | error / warning | not the error | The declared `labels` contradict the data: `per_group` with groups of several labels (an error), or `per_sample` with nearly every group of one label (a warning). |
| `task_group_on_missing_column` | error | no | `group_on` names a column that is not in the frame. |
| `task_group_on_missing_values` | warning | yes | Rows without a group value. |
| `task_group_time_on_constant` | error | no | The group time column has fewer than two distinct values. |
| `task_group_time_on_dtype` | error | no | The group time column is not datetime, period or numeric. |
| `task_group_time_on_few_unique` | warning | yes | The group time column has fewer than 10 distinct values. |
| `task_group_time_on_missing_column` | error | no | `group_time_on` names a column that is not in the frame. |
| `task_group_time_on_missing_values` | error | no | The group time column has missing values. |
| `task_label_time_copy_is_feature` | warning | yes | A feature follows the time that dates the label, so the model reads that time through it. |
| `task_label_time_gap` | warning | yes | The splits leave a gap on a time that dates the label. |
| `task_metric_context_unexplained` | error | no | A metric taken from the task's context has no `reason`. |
| `task_metric_deviance_on_transformed_target` | error | no | A mean deviance scores a target shipped on a transformed scale. |
| `task_metric_empty` | error | no | The metric name is empty. |
| `task_metric_input_is_feature` | warning | yes | The metric reads a feature column: a metric's extra data is a scoring column (MET-2). |
| `task_metric_input_is_model_input` | info | yes | The metric reads the task's group or time column where it is. |
| `task_metric_input_missing` | error | no | The metric spec does not map an input role the metric needs. |
| `task_metric_not_canonical` | error | no | A known metric is spelled other than its canonical name. |
| `task_metric_not_computable` | error | no | The metric gives no finite value on a test prediction. |
| `task_metric_param_invalid` | error | no | The metric's params are invalid. |
| `task_metric_problem_type_mismatch` | error | no | The metric belongs to another problem type. |
| `task_metric_reference_missing` | error | no | The source's metric names no `reference`. |
| `task_metric_spec_mismatch` | error | no | The metric spec's kind or direction differs from the registry's. |
| `task_metric_stand_in_incomplete` | error | no | A stand-in metric lacks the `original` it stands in for or the `reason` the original cannot be computed. |
| `task_metric_transform_not_regression` | error | no | A `target_transform` is set on a classification target. |
| `task_metric_transform_overflow` | error | no | The inverse `target_transform` overflows: the target is not on the transformed scale. |
| `task_metric_undeclared` | error | no | No metric is declared, and the default carries no reason. |
| `task_metric_unknown` | error / info | not the error | The metric is not in the registry (an error for format 2, an info for format 1). |
| `task_metric_unknown_param` | error | no | The metric spec passes a param the metric does not take. |
| `task_metric_weight_without_sample_weight` | warning | yes | The metric weights rows by an amount at risk that is not the training weight (MET-15). |
| `task_prediction_time_after_label` | warning | yes | Rows whose prediction time is after their label time. |
| `task_prediction_time_missing` | error | no | The prediction time names a column that is not in the frame. |
| `task_prediction_time_not_feature` | error | no | The prediction time is a target, group, scoring or label-time column, though the actor holds it. |
| `task_rate_count_not_whole` | warning | yes | A Poisson rate times its weight does not rebuild a whole count. |
| `task_sample_weight_not_metric_weight` | error | no | The training weight is not the row weight the metric reads (MET-15). |
| `task_scoring_column_is_feature` | error | no | A scoring column is also the time or stratification column, which models use. |
| `task_scoring_column_missing` | error | no | A scoring or metric input column is not in the frame. |
| `task_scoring_column_undocumented` | error | no | A scoring column lacks its role, description or metric. |
| `task_scoring_column_unused` | error | no | A scoring column is not an input of the metric in the role it declares. |
| `task_stratify_dtype` | error | no | The stratification column is not discrete. |
| `task_stratify_high_cardinality` | warning | yes | The stratification column has many distinct values. |
| `task_stratify_missing_values` | error | no | The stratification column has missing values. |
| `task_stratify_on_missing_column` | error | no | `stratify_on` names a column that is not in the frame. |
| `task_stratify_on_regression` | warning | yes | `stratify_on` is set on a regression task. |
| `task_target_class_count` | error | no | The class count does not fit the problem type. |
| `task_target_column_name_missing_column` | error | no | The target names a column that is not in the frame. |
| `task_target_dtype` | error | no | A classification target is not `category`. |
| `task_target_low_cardinality` | warning | yes | A regression target has few distinct values. |
| `task_target_missing_values` | error | no | The target has missing values. |
| `task_target_value_dominant` | warning | yes | One value holds at least half of a regression target (a cap, a placeholder, zero inflation). |
| `task_time_on_constant` | error | no | The time column has fewer than two distinct values. |
| `task_time_on_dtype` | error | no | The time column is not datetime, period or numeric. |
| `task_time_on_few_unique` | warning | yes | The time column has fewer than 10 distinct values. |
| `task_time_on_missing_column` | error | no | `time_on` names a column that is not in the frame. |
| `task_time_on_missing_values` | error | no | The time column has missing values. |
| `task_time_on_not_sorted` | warning | yes | The frame is not sorted by the time column. |
| `task_unit_weight_not_one_per_unit` | error | no | A unit weight does not sum to 1 per unit (MET-17). |
| `task_unit_weight_unit_split` | warning | yes | A unit of a unit weight has rows on both sides of a split. |
| `task_weight_invalid` | error | no | A weight column is not a finite number >= 0 with weight on every split side. |

## splits

| slug | severity | acceptable | what it means |
|---|---|---|---|
| `groups_largest_share_high` | warning | yes | One group holds more than 20% of the rows. |
| `groups_not_clustered` | info | yes | Rows are no closer to their own group than chance: the grouping may not be needed. |
| `groups_test_groups_few` | warning | yes | A test fold holds fewer than 20 groups, or the data fewer than 10 in all. |
| `splits_class_missing` | error / warning | not the error | A class is missing from a fold or too rare to spread over the folds: a multiclass test fold lacks one, a train side lacks a class its test side holds, or a fold flips between binary and multiclass (errors when a model or the metric then breaks). |
| `splits_dimensions_off_protocol` | warning | yes | The splits are not the v2 protocol's: IID or grouped repeats and folds other than SPLIT-33's for the data's size, or a temporal split with fewer windows than an IID split of its scored units would get, or under 3 (SPLIT-15). |
| `splits_duplicate_indices` | error | no | A split's index list repeats rows. |
| `splits_feature_missing_in_test` | warning | yes | A feature is recorded on one side of a window and missing on the other. |
| `splits_group_leakage` | error | no | A group is on both sides of a fold. |
| `splits_index_out_of_bounds` | error | no | A split indexes outside the frame. |
| `splits_rows_never_tested` | warning | yes | Rows that cross-validation never tests. |
| `splits_rows_unused` | error / info | not the error | Rows in no train and no test set (an info on a temporal split, where a gap, history no window trains on or a filter leaves them out). |
| `splits_temporal_layout` | info | yes | How many folds per repeat a temporal split uses. |
| `splits_temporal_leakage` | error | no | A fold trains on rows that are not older than its test rows. |
| `splits_temporal_order` | warning | yes | Temporal folds are not ordered newest test window first. |
| `splits_test_minority_few` | warning | yes | A binary test fold holds fewer than 10 rows of its rarer class. |
| `splits_test_over_budget` | warning | yes | A split tests on more rows than the container's test budget. |
| `splits_test_single_class` | error / warning | not the error | A classification test fold holds a single class (an error when the metric is then undefined, when the train side lacks that class or when the fold flips between binary and multiclass). |
| `splits_test_target_constant` | error | no | A regression test fold has a constant target. |
| `splits_train_sampling_missing` | error | no | The container records a row budget but no `train_sampling`. |
| `splits_train_test_overlap` | error | no | A fold has rows on both its train and test side. |

## metadata

| slug | severity | acceptable | what it means |
|---|---|---|---|
| `meta_bibtex_empty` | error | no | A source's BibTeX is empty. |
| `meta_bibtex_fields_missing` | info | yes | BibTeX entries miss recommended fields. |
| `meta_bibtex_key_count` | warning | yes | The citation key lists another number of entries than the BibTeX defines. |
| `meta_bibtex_key_empty` | error | no | A source's citation key is empty. |
| `meta_bibtex_key_not_defined` | error | no | The citation key names an entry the BibTeX lacks. |
| `meta_bibtex_latex_hazard` | warning | yes | The BibTeX holds characters LaTeX reads as markup. |
| `meta_bibtex_no_entry` | error | no | The BibTeX holds no `@type{key, ...}` entry. |
| `meta_bibtex_unbalanced_braces` | error | no | The BibTeX's braces do not balance. |
| `meta_curation_comments_empty` | info | yes | `curation_comments` is empty. |
| `meta_dataset_year` | warning | yes | A source's year is not a plausible 4-digit year. |
| `meta_download_description_empty` | warning | yes | `download_description` is empty. |
| `meta_group_basis_missing` | error | no | `ForcedIIDFromGrouped` without its group basis (SPLIT-35). |
| `meta_license_unknown` | warning | yes | A source's license is unknown. |
| `meta_placeholder_left` | error | no | Scaffolding placeholders are left: `TODO` or `<unique_name>` in the metadata (a source's license included), `TODO(verify)` in `dataset.py`. |
| `meta_source_link` | warning | yes | A source's link does not look like a URL or DOI. |
| `meta_splits_comment_empty` | warning | yes | `splits_comment` is empty. |
| `meta_tags_contradict_regime` | warning | yes | `data_tags` claim a non-IID regime on an IID split. |
| `meta_tags_missing_iid` | warning | yes | An IID split without the `IID` tag. |
| `meta_tags_missing_non_iid` | warning | yes | A non-IID split without the `Non-IID` tag. |
| `meta_tags_missing_regime` | warning | yes | A temporal or grouped split without its regime's tag. |
| `meta_tags_multiple_regimes` | warning | yes | `data_tags` carry more than one split regime. |
| `meta_time_basis_field_missing` | info | yes | A time basis tag in `data_tags` without the stored time basis. |
| `meta_time_basis_mismatch` | error | no | The stored time basis names another tag than `data_tags` carry. |
| `meta_time_basis_missing` | info | yes | The split is not temporal, and the definition does not say why (SPLIT-32). |
| `meta_time_basis_on_temporal` | error | no | A time basis that says why a split is not temporal, on a temporal split. |
| `meta_time_basis_regime` | error | no | The time basis tag contradicts the split's regime. |
| `meta_time_basis_several` | error | no | `data_tags` carry more than one time basis. |
| `meta_time_basis_unattributed` | error | no | A time basis only a person sets, without the person and date (SPLIT-32). |
| `meta_time_gap_without_time_on` | error | no | `time_gap` is set on a task without a time column. |
| `meta_time_horizon_mismatch` | warning | yes | The declared horizon differs from the span of the first test window. |
| `meta_time_horizon_missing` | error | no | A temporal task without `time_horizon`. |
| `meta_time_horizon_unit` | info | yes | A calendar horizon unit on a numeric time column, so the horizon cannot be cross-checked. |
| `meta_time_horizon_without_time_on` | error | no | `time_horizon` is set on a task without a time column. |
| `meta_time_present_unused` | info | yes | The frame holds date columns, and the split is not temporal. |

## saved files

| slug | severity | acceptable | what it means |
|---|---|---|---|
| `export_checksum_mismatch` | error | no | The checksum recomputed from disk differs from the stored. |
| `export_dtype_changed` | error | no | Dtypes changed in the save/load round trip. |
| `export_files_missing` | error | no | The saved container lacks a file it needs. |
| `export_metadata_changed` | error | no | A metadata object changed in the JSON round trip. |
| `export_path_layout` | warning | yes | The save directory is not named by the container's UUID. |
| `export_shape_changed` | error | no | A frame's shape changed in the save/load round trip. |
| `export_task_view_mismatch` | error | no | benchmark_task.json differs from container.task(). |
| `export_task_view_missing` | warning | yes | A format-2 container has no benchmark_task.json. |
| `export_uuid_mismatch` | error | no | The UUID changed in the save/load round trip. |
| `export_values_changed` | error | no | A frame's values changed in the save/load round trip. |

## any

| slug | severity | acceptable | what it means |
|---|---|---|---|
| `check_crashed` | error | no | A check raised an exception: a bug in the check or an unexpected bundle. |

164 slugs; 96 can be errors, 61 warnings, 18 infos.
