"""Curated dataset definition for `<unique_name>` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, drop_columns  # noqa: F401


class ClassName(AbstractCuratedDataset):
    # Dataset
    unique_name = "<unique_name>"
    year = "TODO"
    domain = "TODO"  # one of data_foundry.schema.Domain
    source = "TODO"  # where the data first appeared: one of data_foundry.schema.DatasetSource
    source_url = "TODO"
    license = "TODO"
    data_tags = ()  # context tags only (Spatial, Anonymized, ...); the regime tags are added from the task
    download_description = """
        TODO(verify): commands that recreate the raw files.
        mkdir -p local-data-warehouse/<unique_name> && mv data_files local-data-warehouse/<unique_name>/
    """
    bibtex = """
        @misc{TODO,
          title = {TODO},
        }
    """
    curation_comments = """
        We start with <file> from <source>.

        - TODO(verify): what was dropped and why (identifiers, leaking features, constant columns).
    """
    # Data over the row budget ships as a sub-sampled `<name>_1m` version, which also sets: version_of = "<name>",
    # version_comment = "...", subsample_to_budget = True.

    # Task (the metric defaults to roc_auc / log_loss / rmse; stratifying on a classification target is the default)
    target = "TODO"
    problem_type = "TODO"
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
        # TODO(verify): the preprocessing steps (see the add-dataset skill's dataset_patterns.md, §B), including
        # the column drops: df = drop_columns(df, ["id", ...]).
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The dtypes of the cleaned frame; a classification target becomes a category without being listed.
        return FeatureTypes(
            categorical=[],  # TODO(verify): fixed, finite value sets
            string=[],  # free text, high-cardinality text
            datetime={},  # {"column": "%Y-%m-%d"}, or a list of names to infer the format
        )
