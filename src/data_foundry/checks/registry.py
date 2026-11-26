"""The registry of every check finding's slug: its severities, the stage it runs at, and whether a definition may
accept it.

Every :class:`~data_foundry.checks.results.CheckResult` a check emits names a slug listed here (a test holds the
code and this table together). The table also decides what ``accepted_check_warnings`` can silence: a warning or an
info always, an error only when :data:`ACCEPTABLE_ERRORS` lists the slug with the reason. The markdown version of the
table is ``.claude/skills/knowledge-data-foundry/references/check_slugs.md``, written by
``python -m data_foundry.checks.registry`` (a test checks that it is current).

The stages:

* ``definition``: the definition file and the curation rules that need its class (``dataset check`` only);
* ``frame``: the curated frame on its own;
* ``task``: the task metadata against the frame;
* ``splits``: the splits against the frame and the task;
* ``metadata``: the dataset metadata (sources, tags, the time basis, the comments);
* ``saved files``: a saved container reloaded from disk (``verify_saved_container``);
* ``any``: a check that crashed, at whatever stage it ran.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from data_foundry.checks.results import SEVERITY_ORDER

if TYPE_CHECKING:
    from data_foundry.checks.results import Severity

Stage = Literal["definition", "frame", "task", "splits", "metadata", "saved files", "any"]

STAGES: tuple[Stage, ...] = ("definition", "frame", "task", "splits", "metadata", "saved files", "any")


@dataclass(frozen=True)
class Check:
    """One slug of the registry.

    Attributes:
        slug: The stable name the findings carry.
        severities: The severities its findings can have, the highest first.
        stage: What the check looks at (see the module docstring).
        description: What a finding means, in one line.
        accepted_error: Why a definition may accept the slug's error; empty when it may not.
    """

    slug: str
    severities: tuple[Severity, ...]
    stage: Stage
    description: str
    accepted_error: str = ""

    @property
    def severity(self) -> Severity:
        """The highest severity a finding of this slug can have."""
        return self.severities[0]

    @property
    def acceptable(self) -> bool:
        """Whether ``accepted_check_warnings`` may list the slug: it can be a warning or an info, or its error is
        acceptable on purpose.
        """
        return any(s != "error" for s in self.severities) or bool(self.accepted_error)


ACCEPTABLE_ERRORS: dict[str, str] = {
    "splits_test_too_small": "SPLIT-14 lets the curator make an exception when the use case fixes the test window, "
    "as a factory day of garments_worker_productivity (17-24 team records, accepted 2026-11-19).",
}
"""The errors a definition may accept, with the reason. Every other error is fixed in the definition."""

_TABLE: tuple[tuple[str, str, Stage, str], ...] = (
    # --- definition: the definition file and the curation rules that need its class -----------------------------
    ("accepted_check_warnings_unused", "info", "definition", "An accepted slug no longer fires, or is misspelled."),
    ("definition_no_use_case", "error", "definition", "`TaskSummary(fit='none')`: the dataset simulates no decision."),
    (
        "definition_nondeterministic",
        "error",
        "definition",
        "`dataset.py` calls code whose result can change between runs or machines (an unseeded random step, an "
        "unstable sort, an unsorted file listing).",
    ),
    ("definition_summary_long", "warning", "definition", "A `task_summary` field is longer than the word limit."),
    ("definition_summary_missing", "error", "definition", "The definition has no `task_summary`."),
    (
        "definition_time_changed_in_split",
        "warning",
        "definition",
        "`_make_splits` changes the time column after the rows were ordered by it.",
    ),
    ("raw_files_changed", "warning", "definition", "The raw files differ from those the README was written from."),
    ("raw_files_missing", "error", "definition", "A `Source(files=...)` pattern matches no file in the raw folder."),
    ("splits_test_too_small", "error", "definition", "A temporal test window holds fewer than 33 scored units."),
    ("splits_train_under_floor", "error", "definition", "A temporal window trains on less than 30% of the rows."),
    (
        "splits_train_under_half",
        "warning",
        "definition",
        "A temporal window trains on less than half the rows: the curator's exception (SPLIT-14).",
    ),
    (
        "time_newest_period_short",
        "warning",
        "definition",
        "The newest 30 days hold far fewer rows a day than the spans before: often a release cut before the outcomes "
        "were complete.",
    ),
    # --- frame: the curated frame on its own -------------------------------------------------------------------
    ("dataset_all_missing_column", "warning", "frame", "A column is missing in every row."),
    ("dataset_column_names", "error", "frame", "A column name is not a string."),
    (
        "dataset_conflicting_duplicate_rows",
        "warning/info",
        "frame",
        "Rows share every feature but differ in the target (a warning from 1% of the rows).",
    ),
    ("dataset_constant_column", "warning", "frame", "A column holds a single non-missing value."),
    ("dataset_duplicate_column_names", "error", "frame", "Two columns have the same name."),
    (
        "dataset_duplicate_columns",
        "error/warning",
        "frame",
        "Two columns hold the same values (an error when one is a copy of the target).",
    ),
    ("dataset_duplicate_rows", "warning/info", "frame", "Exact duplicate rows (a warning from 1% of the rows)."),
    (
        "dataset_duplicates_skipped",
        "info",
        "frame",
        "The duplicate row and column checks were skipped: the frame is over the cell budget.",
    ),
    ("dataset_empty", "error", "frame", "The frame has no rows or no columns."),
    (
        "dataset_identifier_column",
        "error/warning",
        "frame",
        "A column identifies the row: one category or string value per row, or an integer numbered densely like a "
        "running id; an error when it is the group key, one group per row.",
    ),
    ("dataset_index_range", "error", "frame", "The frame's index is not `RangeIndex(0, n)`."),
    ("dataset_missing", "error", "frame", "The container has no frame loaded."),
    (
        "dataset_missing_value_label",
        "warning",
        "frame",
        "A category or string column holds levels that look like a missing value (`?`, `n/a`, `null`).",
    ),
    (
        "dataset_missing_value_sentinel",
        "warning",
        "frame",
        "A numeric column is dominated by a value that looks like a missing-value code (-1, -999, 9999).",
    ),
    ("dataset_object_dtype", "error", "frame", "A column has `object` dtype."),
    (
        "dataset_pure_feature_value",
        "warning",
        "frame",
        "A frequent feature value determines the class on its own: a possible leak.",
    ),
    (
        "dataset_pure_feature_value_skipped",
        "info",
        "frame",
        "The pure-feature-value check was skipped: the frame is over the cell budget.",
    ),
    (
        "dataset_row_order_leaks_target",
        "warning",
        "frame",
        "The target correlates with the row position: the frame looks ordered, not shuffled.",
    ),
    (
        "dataset_smiles_column",
        "error/warning",
        "frame",
        "A SMILES column is not a string column, or holds SMILES the pinned RDKit cannot parse.",
    ),
    ("dataset_smiles_unchecked", "info", "frame", "A SMILES column was not parsed (RDKit is not installed)."),
    ("dataset_special_feature", "error", "frame", "A special feature names columns that are not in the frame."),
    (
        "dataset_spectrum",
        "error/warning",
        "frame",
        "A spectrum's columns are not numeric or not finite, or miss intensities.",
    ),
    ("dataset_spectrum_negative", "info", "frame", "Raw mass spectra hold negative intensities."),
    ("dataset_unused_categories", "warning", "frame", "A category column declares categories that never occur."),
    ("test_dataset_dtype_mismatch", "error", "frame", "The unlabeled test set's dtypes differ from the frame's."),
    ("test_dataset_extra_columns", "error", "frame", "The unlabeled test set has columns the frame lacks."),
    ("test_dataset_index_range", "warning", "frame", "The unlabeled test set's index is not a range from 0."),
    ("test_dataset_missing_columns", "error", "frame", "The unlabeled test set lacks columns of the frame."),
    # --- task: the task metadata against the frame -------------------------------------------------------------
    (
        "task_feature_looks_like_exposure",
        "warning",
        "task",
        "A feature looks like an amount at risk (time insured, area swept), which is a weight, never a feature.",
    ),
    (
        "task_group_labels_mismatch",
        "error/warning",
        "task",
        "The declared `labels` contradict the data: `per_group` with groups of several labels (an error), or "
        "`per_sample` with nearly every group of one label (a warning).",
    ),
    ("task_group_on_missing_column", "error", "task", "`group_on` names a column that is not in the frame."),
    ("task_group_on_missing_values", "warning", "task", "Rows without a group value."),
    ("task_group_time_on_constant", "error", "task", "The group time column has fewer than two distinct values."),
    ("task_group_time_on_dtype", "error", "task", "The group time column is not datetime, period or numeric."),
    ("task_group_time_on_few_unique", "warning", "task", "The group time column has fewer than 10 distinct values."),
    ("task_group_time_on_missing_column", "error", "task", "`group_time_on` names a column that is not in the frame."),
    ("task_group_time_on_missing_values", "error", "task", "The group time column has missing values."),
    (
        "task_label_time_copy_is_feature",
        "warning",
        "task",
        "A feature follows the time that dates the label, so the model reads that time through it.",
    ),
    ("task_label_time_gap", "warning", "task", "The splits leave a gap on a time that dates the label."),
    (
        "task_metric_context_unexplained",
        "error",
        "task",
        "A metric taken from the task's context has no `reason`.",
    ),
    (
        "task_metric_deviance_on_transformed_target",
        "error",
        "task",
        "A mean deviance scores a target shipped on a transformed scale.",
    ),
    ("task_metric_empty", "error", "task", "The metric name is empty."),
    (
        "task_metric_input_is_feature",
        "warning",
        "task",
        "The metric reads a feature column: a metric's extra data is a scoring column (MET-2).",
    ),
    (
        "task_metric_input_is_model_input",
        "info",
        "task",
        "The metric reads the task's group or time column where it is.",
    ),
    ("task_metric_input_missing", "error", "task", "The metric spec does not map an input role the metric needs."),
    ("task_metric_not_canonical", "error", "task", "A known metric is spelled other than its canonical name."),
    ("task_metric_not_computable", "error", "task", "The metric gives no finite value on a test prediction."),
    ("task_metric_param_invalid", "error", "task", "The metric's params are invalid."),
    ("task_metric_problem_type_mismatch", "error", "task", "The metric belongs to another problem type."),
    ("task_metric_reference_missing", "error", "task", "The source's metric names no `reference`."),
    ("task_metric_spec_mismatch", "error", "task", "The metric spec's kind or direction differs from the registry's."),
    (
        "task_metric_stand_in_incomplete",
        "error",
        "task",
        "A stand-in metric lacks the `original` it stands in for or the `reason` the original cannot be computed.",
    ),
    (
        "task_metric_transform_not_regression",
        "error",
        "task",
        "A `target_transform` is set on a classification target.",
    ),
    (
        "task_metric_transform_overflow",
        "error",
        "task",
        "The inverse `target_transform` overflows: the target is not on the transformed scale.",
    ),
    ("task_metric_undeclared", "error", "task", "No metric is declared, and the default carries no reason."),
    (
        "task_metric_unknown",
        "error/info",
        "task",
        "The metric is not in the registry (an error for format 2, an info for format 1).",
    ),
    ("task_metric_unknown_param", "error", "task", "The metric spec passes a param the metric does not take."),
    (
        "task_metric_weight_without_sample_weight",
        "warning",
        "task",
        "The metric weights rows by an amount at risk that is not the training weight (MET-15).",
    ),
    ("task_prediction_time_after_label", "warning", "task", "Rows whose prediction time is after their label time."),
    ("task_prediction_time_missing", "error", "task", "The prediction time names a column that is not in the frame."),
    (
        "task_prediction_time_not_feature",
        "error",
        "task",
        "The prediction time is a target, group, scoring or label-time column, though the actor holds it.",
    ),
    (
        "task_rate_count_not_whole",
        "warning",
        "task",
        "A Poisson rate times its weight does not rebuild a whole count.",
    ),
    (
        "task_sample_weight_not_metric_weight",
        "error",
        "task",
        "The training weight is not the row weight the metric reads (MET-15).",
    ),
    (
        "task_scoring_column_is_feature",
        "error",
        "task",
        "A scoring column is also the time or stratification column, which models use.",
    ),
    ("task_scoring_column_missing", "error", "task", "A scoring or metric input column is not in the frame."),
    (
        "task_scoring_column_undocumented",
        "error",
        "task",
        "A scoring column lacks its role, description or metric.",
    ),
    (
        "task_scoring_column_unused",
        "error",
        "task",
        "A scoring column is not an input of the metric in the role it declares.",
    ),
    ("task_stratify_dtype", "error", "task", "The stratification column is not discrete."),
    ("task_stratify_high_cardinality", "warning", "task", "The stratification column has many distinct values."),
    ("task_stratify_missing_values", "error", "task", "The stratification column has missing values."),
    ("task_stratify_on_missing_column", "error", "task", "`stratify_on` names a column that is not in the frame."),
    ("task_stratify_on_regression", "warning", "task", "`stratify_on` is set on a regression task."),
    ("task_target_class_count", "error", "task", "The class count does not fit the problem type."),
    (
        "task_target_column_name_missing_column",
        "error",
        "task",
        "The target names a column that is not in the frame.",
    ),
    ("task_target_dtype", "error", "task", "A classification target is not `category`."),
    ("task_target_low_cardinality", "warning", "task", "A regression target has few distinct values."),
    ("task_target_missing_values", "error", "task", "The target has missing values."),
    (
        "task_target_value_dominant",
        "warning",
        "task",
        "One value holds at least half of a regression target (a cap, a placeholder, zero inflation).",
    ),
    ("task_time_on_constant", "error", "task", "The time column has fewer than two distinct values."),
    ("task_time_on_dtype", "error", "task", "The time column is not datetime, period or numeric."),
    ("task_time_on_few_unique", "warning", "task", "The time column has fewer than 10 distinct values."),
    ("task_time_on_missing_column", "error", "task", "`time_on` names a column that is not in the frame."),
    ("task_time_on_missing_values", "error", "task", "The time column has missing values."),
    ("task_time_on_not_sorted", "warning", "task", "The frame is not sorted by the time column."),
    (
        "task_unit_weight_not_one_per_unit",
        "error",
        "task",
        "A unit weight does not sum to 1 per unit (MET-17).",
    ),
    (
        "task_unit_weight_unit_split",
        "warning",
        "task",
        "A unit of a unit weight has rows on both sides of a split.",
    ),
    (
        "task_weight_invalid",
        "error",
        "task",
        "A weight column is not a finite number >= 0 with weight on every split side.",
    ),
    # --- splits: the splits against the frame and the task -----------------------------------------------------
    ("groups_largest_share_high", "warning", "splits", "One group holds more than 20% of the rows."),
    (
        "groups_not_clustered",
        "info",
        "splits",
        "Rows are no closer to their own group than chance: the grouping may not be needed.",
    ),
    (
        "groups_test_groups_few",
        "warning",
        "splits",
        "A test fold holds fewer than 20 groups, or the data fewer than 10 in all.",
    ),
    (
        "splits_class_missing",
        "error/warning",
        "splits",
        "A class is missing from a fold or too rare to spread over the folds: a multiclass test fold lacks one, a "
        "train side lacks a class its test side holds, or a fold flips between binary and multiclass (errors when a "
        "model or the metric then breaks).",
    ),
    (
        "splits_dimensions_off_protocol",
        "warning",
        "splits",
        "The splits are not the v2 protocol's: IID or grouped repeats and folds other than SPLIT-33's for the data's "
        "size, or a temporal split with fewer windows than an IID split of its scored units would get, or under 3 "
        "(SPLIT-15).",
    ),
    ("splits_duplicate_indices", "error", "splits", "A split's index list repeats rows."),
    (
        "splits_feature_missing_in_test",
        "warning",
        "splits",
        "A feature is recorded on one side of a window and missing on the other.",
    ),
    ("splits_group_leakage", "error", "splits", "A group is on both sides of a fold."),
    ("splits_index_out_of_bounds", "error", "splits", "A split indexes outside the frame."),
    ("splits_rows_never_tested", "warning", "splits", "Rows that cross-validation never tests."),
    (
        "splits_rows_unused",
        "error/info",
        "splits",
        "Rows in no train and no test set (an info on a temporal split, where a gap, history no window trains on or "
        "a filter leaves them out).",
    ),
    (
        "splits_temporal_layout",
        "info",
        "splits",
        "How many folds per repeat a temporal split uses.",
    ),
    ("splits_temporal_leakage", "error", "splits", "A fold trains on rows that are not older than its test rows."),
    ("splits_temporal_order", "warning", "splits", "Temporal folds are not ordered newest test window first."),
    (
        "splits_test_minority_few",
        "warning",
        "splits",
        "A binary test fold holds fewer than 10 rows of its rarer class.",
    ),
    (
        "splits_test_over_budget",
        "warning",
        "splits",
        "A split tests on more rows than the container's test budget.",
    ),
    (
        "splits_test_single_class",
        "error/warning",
        "splits",
        "A classification test fold holds a single class (an error when the metric is then undefined, when the train "
        "side lacks that class or when the fold flips between binary and multiclass).",
    ),
    ("splits_test_target_constant", "error", "splits", "A regression test fold has a constant target."),
    (
        "splits_train_sampling_missing",
        "error",
        "splits",
        "The container records a row budget but no `train_sampling`.",
    ),
    ("splits_train_test_overlap", "error", "splits", "A fold has rows on both its train and test side."),
    # --- metadata: sources, tags, the time basis, the comments -------------------------------------------------
    ("meta_bibtex_empty", "error", "metadata", "A source's BibTeX is empty."),
    ("meta_bibtex_fields_missing", "info", "metadata", "BibTeX entries miss recommended fields."),
    (
        "meta_bibtex_key_count",
        "warning",
        "metadata",
        "The citation key lists another number of entries than the BibTeX defines.",
    ),
    ("meta_bibtex_key_empty", "error", "metadata", "A source's citation key is empty."),
    ("meta_bibtex_key_not_defined", "error", "metadata", "The citation key names an entry the BibTeX lacks."),
    ("meta_bibtex_latex_hazard", "warning", "metadata", "The BibTeX holds characters LaTeX reads as markup."),
    ("meta_bibtex_no_entry", "error", "metadata", "The BibTeX holds no `@type{key, ...}` entry."),
    ("meta_bibtex_unbalanced_braces", "error", "metadata", "The BibTeX's braces do not balance."),
    ("meta_curation_comments_empty", "info", "metadata", "`curation_comments` is empty."),
    ("meta_dataset_year", "warning", "metadata", "A source's year is not a plausible 4-digit year."),
    ("meta_download_description_empty", "warning", "metadata", "`download_description` is empty."),
    (
        "meta_group_basis_missing",
        "error",
        "metadata",
        "`ForcedIIDFromGrouped` has no `Group basis:` line (SPLIT-35).",
    ),
    ("meta_license_unknown", "warning", "metadata", "A source's license is unknown."),
    (
        "meta_placeholder_left",
        "error",
        "metadata",
        "Scaffolding placeholders are left: `TODO` or `<unique_name>` in the metadata (a source's license included), "
        "`TODO(verify)` in `dataset.py`.",
    ),
    ("meta_source_link", "warning", "metadata", "A source's link does not look like a URL or DOI."),
    ("meta_splits_comment_empty", "warning", "metadata", "`splits_comment` is empty."),
    ("meta_tags_contradict_regime", "warning", "metadata", "`data_tags` claim a non-IID regime on an IID split."),
    ("meta_tags_missing_iid", "warning", "metadata", "An IID split without the `IID` tag."),
    ("meta_tags_missing_non_iid", "warning", "metadata", "A non-IID split without the `Non-IID` tag."),
    ("meta_tags_missing_regime", "warning", "metadata", "A temporal or grouped split without its regime's tag."),
    ("meta_tags_multiple_regimes", "warning", "metadata", "`data_tags` carry more than one split regime."),
    (
        "meta_time_basis_line_missing",
        "info",
        "metadata",
        "A time basis tag without its `Time basis:` line.",
    ),
    ("meta_time_basis_lines", "error", "metadata", "`curation_comments` hold more than one `Time basis:` line."),
    (
        "meta_time_basis_mismatch",
        "error",
        "metadata",
        "The `Time basis:` line names another tag than `data_tags` carry.",
    ),
    (
        "meta_time_basis_missing",
        "info",
        "metadata",
        "The split is not temporal, and the definition does not say why (SPLIT-32).",
    ),
    (
        "meta_time_basis_on_temporal",
        "error",
        "metadata",
        "A time basis that says why a split is not temporal, on a temporal split.",
    ),
    ("meta_time_basis_regime", "error", "metadata", "The time basis tag contradicts the split's regime."),
    ("meta_time_basis_renamed", "info", "metadata", "A time basis tag under its old name."),
    ("meta_time_basis_several", "error", "metadata", "`data_tags` carry more than one time basis."),
    (
        "meta_time_basis_unattributed",
        "error",
        "metadata",
        "A time basis only a person sets, without the person and date (SPLIT-32).",
    ),
    (
        "meta_time_basis_unstructured",
        "info",
        "metadata",
        "A free-text `Time basis:` line instead of `TimeBasis(tag, reason)`.",
    ),
    ("meta_time_gap_without_time_on", "error", "metadata", "`time_gap` is set on a task without a time column."),
    (
        "meta_time_horizon_mismatch",
        "warning",
        "metadata",
        "The declared horizon differs from the span of the first test window.",
    ),
    ("meta_time_horizon_missing", "error", "metadata", "A temporal task without `time_horizon`."),
    (
        "meta_time_horizon_unit",
        "info",
        "metadata",
        "A calendar horizon unit on a numeric time column, so the horizon cannot be cross-checked.",
    ),
    (
        "meta_time_horizon_without_time_on",
        "error",
        "metadata",
        "`time_horizon` is set on a task without a time column.",
    ),
    (
        "meta_time_present_unused",
        "info",
        "metadata",
        "The frame holds date columns, and the split is not temporal.",
    ),
    # --- saved files: a saved container reloaded from disk -----------------------------------------------------
    ("export_checksum_mismatch", "error", "saved files", "The checksum recomputed from disk differs from the stored."),
    ("export_dtype_changed", "error", "saved files", "Dtypes changed in the save/load round trip."),
    ("export_files_missing", "error", "saved files", "The saved container lacks a file it needs."),
    ("export_metadata_changed", "error", "saved files", "A metadata object changed in the JSON round trip."),
    ("export_path_layout", "warning", "saved files", "The save directory is not named by the container's UUID."),
    ("export_shape_changed", "error", "saved files", "A frame's shape changed in the save/load round trip."),
    ("export_uuid_mismatch", "error", "saved files", "The UUID changed in the save/load round trip."),
    ("export_values_changed", "error", "saved files", "A frame's values changed in the save/load round trip."),
    # --- any stage ---------------------------------------------------------------------------------------------
    ("check_crashed", "error", "any", "A check raised an exception: a bug in the check or an unexpected bundle."),
)


def _build() -> dict[str, Check]:
    checks: dict[str, Check] = {}
    for slug, severities, stage, description in _TABLE:
        if slug in checks:
            raise ValueError(f"check slug {slug!r} is listed twice")
        ordered = tuple(sorted(severities.split("/"), key=SEVERITY_ORDER.__getitem__))
        checks[slug] = Check(slug, ordered, stage, description, ACCEPTABLE_ERRORS.get(slug, ""))  # type: ignore[arg-type]
    unknown = set(ACCEPTABLE_ERRORS) - {s for s, c in checks.items() if "error" in c.severities}
    if unknown:
        raise ValueError(f"ACCEPTABLE_ERRORS names slugs that are no errors: {sorted(unknown)}")
    return dict(sorted(checks.items()))


CHECKS: dict[str, Check] = _build()
"""Every slug a check can emit, by slug."""


def may_accept(slug: str, severity: Severity) -> bool:
    """Whether ``accepted_check_warnings`` silences a finding: a warning or an info always; an error only when
    :data:`ACCEPTABLE_ERRORS` lists its slug.
    """
    return severity != "error" or slug in ACCEPTABLE_ERRORS


def _acceptance(check: Check) -> str:
    if "error" not in check.severities:
        return "yes"
    if check.accepted_error:
        return "yes, the error too"
    return "not the error" if check.acceptable else "no"


def markdown() -> str:
    """The registry as a markdown page: one table per stage."""
    lines = [
        "# Check slugs",
        "",
        "Every slug a Data Foundry check can emit, generated from `src/data_foundry/checks/registry.py` by",
        "`.venv/bin/python -m data_foundry.checks.registry > "
        ".claude/skills/knowledge-data-foundry/references/check_slugs.md`;",
        "do not edit it by hand. *Acceptable* says whether `accepted_check_warnings` may list the slug: a warning or",
        "an info always, an error only for the reason given. What to do about each finding is in",
        '[definitions.md](definitions.md), "Bundle checks", and [checks_and_probes.md](checks_and_probes.md).',
        "",
    ]
    if ACCEPTABLE_ERRORS:
        lines += ["Errors a definition may accept:", ""]
        for slug, reason in ACCEPTABLE_ERRORS.items():
            lines += textwrap.wrap(f"* `{slug}`: {reason}", width=120, subsequent_indent="  ")
        lines.append("")
    for stage in STAGES:
        rows = [c for c in CHECKS.values() if c.stage == stage]
        lines += [f"## {stage}", "", "| slug | severity | acceptable | what it means |", "|---|---|---|---|"]
        lines += [f"| `{c.slug}` | {' / '.join(c.severities)} | {_acceptance(c)} | {c.description} |" for c in rows]
        lines.append("")
    counts = {s: sum(s in c.severities for c in CHECKS.values()) for s in SEVERITY_ORDER}
    lines.append(
        f"{len(CHECKS)} slugs; {counts['error']} can be errors, {counts['warning']} warnings, {counts['info']} infos."
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(markdown(), end="")
