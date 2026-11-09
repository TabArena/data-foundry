"""Curated dataset definition for `<unique_name>` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (  # noqa: F401
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    drop_columns,
)


class ClassName(AbstractCuratedDataset):
    # In brief: the task in plain words, for a reader who has not seen the source (first in the README). One or two
    # plain sentences per field; the house format and examples are in knowledge-data-foundry definitions.md.
    task_summary = TaskSummary(
        question="TODO(verify): the prediction as a one-line question.",
        use_case="TODO(verify): who uses the prediction, when, and the decision it informs.",
        row="TODO(verify): what one row is.",
        predicted="TODO(verify): the target in plain words, by when after the prediction point.",
        known="TODO(verify): what the model knows then, in plain words.",
        known_at_scoring="",  # a metric input recorded with the outcome (a realized time on risk); "" when none
        split="TODO(verify): what the test data stands for (new customers, the next weeks, unseen patients).",
        changes="",  # our changes to the source a reader needs to know
        fit="direct",  # TODO(verify): "direct", "approximate" (a stand-in with a known gap) or "none" (retire)
        fit_reason="TODO(verify): why the data simulates the use case this closely.",
    )

    # Dataset
    unique_name = "<unique_name>"
    domain = "TODO"  # one of data_foundry.schema.Domain
    sources = (
        # The publication: where the data first appeared, not a later re-upload; its year and BibTeX are the
        # dataset's. Add Source(role="copy", platform=..., url=..., license=...) for the copy we download when it is
        # not the publication, and Source(role="part", name=..., ..., files=("...",)) per piece of an assembled dataset.
        Source(
            role="publication",
            platform="TODO",  # one of data_foundry.schema.DatasetSource
            url="TODO",
            license="TODO",
            year="TODO",
            bibtex="""
                @misc{TODO,
                  title = {TODO},
                }
            """,
        ),
    )
    data_tags = ()  # context tags only (Spatial, Anonymized, ...); the regime tags are added from the task
    download_description = """
        TODO(verify): commands that recreate the raw files.
        mkdir -p local-data-warehouse/<unique_name> && mv data_files local-data-warehouse/<unique_name>/
    """
    curation_comments = """
        We start with <file> from <source>.

        - TODO(verify): what was dropped and why (identifiers, leaking features, constant columns).
    """
    # TabArena v0.2 ships data over its row budget (a split side over 1M train / 500k test rows) as the version
    # `<name>_1m` (folder and unique_name; it reads the raw files of `<name>`). The working copy's collection.py
    # sets the budget, so the definition declares none; the build says when the name must carry the suffix.

    # Task (stratifying on a classification target is the default)
    target = "TODO"
    problem_type = "TODO"
    # The metric (required). Look for the source's metric first: the competition's evaluation page, the paper's
    # evaluation section, the task description. Then declare one of
    #   metric = Metric.source("rmse", original="RMSE", reference="https://...")  # the name in data_foundry.v2.metrics
    #   metric = Metric.stand_in("pearsonr", original="...", reason="why it cannot be computed", reference="https://...")
    # and only when the source defines none, the fallback (roc_auc / log_loss / rmse by problem type) with where you
    # looked. A metric that needs a column (a group, a weight) maps it in `inputs={"group": "era"}` and declares it in
    # `scoring_columns = (ScoringColumn(column="era", role="group", used_by="...", description="..."),)`.
    # sample_weight = None  # a rate's realized denominator (MET-15): the metric's row-weight column and fit weight
    metric = Metric.fallback(reason="TODO(verify): where we looked for the source's metric, and found none.")
    # The regime: neither declaration is an IID task with the recommended split. A grouped task (import `Grouping`):
    # grouping = Grouping(
    #     on="...",                  # the group column, never a model feature
    #     labels="...",              # "per_group" (one label per group) or "per_sample"
    #     time_on=None,              # the order inside a group, if any; needed by aggregation="last" and "past_rows"
    #     prediction_unit="row",     # or "group" with aggregation="mean" / "any" / "last" / "select_min" / ...
    #     context="none",            # what a model may know about the group: "none", "all_rows", "past_rows"
    #     definition="""
    #         What one group is, why groups are held out, and the use case with its source.
    #     """,
    # )
    # A temporal task (import `Temporal`, `TemporalSplits`) declares its windows and says why in `splits_comment`
    # (which replaces the generated text, so restate the windows there). A window of fixed length (a calendar unit, or
    # unit="rows") is the horizon; windows of unit="unique" or window=None need `horizon=..., horizon_unit=...`:
    # temporal = Temporal(on="...", splits=TemporalSplits(window=7, unit="days", n_windows=3))

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # Only read here (cached across edits of `_clean`).
        return pd.read_csv(raw_dir / "TODO.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # TODO(verify): the preprocessing steps (knowledge-data-foundry definitions.md, the recipe), including
        # the column drops: df = drop_columns(df, ["id", ...]).
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The dtypes of the cleaned frame; a classification target becomes a category without being listed.
        return FeatureTypes(
            categorical=[],  # TODO(verify): fixed, finite value sets
            string=[],  # free text, high-cardinality text
            datetime={},  # {"column": "%Y-%m-%d"}, or a list of names to infer the format
        )
