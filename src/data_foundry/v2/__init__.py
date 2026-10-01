"""data-foundry v2: define a curated dataset as one Python class instead of a notebook.

See :mod:`data_foundry.v2.dataset` for the interface, :mod:`data_foundry.v2.preprocessing` for the standard
steps, :mod:`data_foundry.v2.splits` for the split protocol, :mod:`data_foundry.v2.registry` for discovery and
:mod:`data_foundry.v2.report` for the generated ``README.md``.
"""

from __future__ import annotations

from data_foundry.schema import Grouping
from data_foundry.v2.dataset import (
    AUTO,
    AbstractCuratedDataset,
    CurationResult,
    DatasetDefinitionError,
    Decision,
    FeatureTypes,
    clean_text,
)
from data_foundry.v2.preprocessing import anonymize_ids, cast_dtypes, drop_columns, order_rows
from data_foundry.v2.registry import discover_datasets, get_dataset, load_definition
from data_foundry.v2.report import read_report
from data_foundry.v2.splits import SplitPlan, Splits, Temporal, TemporalSplits
from data_foundry.v2.workbench import workbench

__all__ = [
    "AUTO",
    "AbstractCuratedDataset",
    "CurationResult",
    "DatasetDefinitionError",
    "Decision",
    "FeatureTypes",
    "Grouping",
    "SplitPlan",
    "Splits",
    "Temporal",
    "TemporalSplits",
    "anonymize_ids",
    "cast_dtypes",
    "clean_text",
    "discover_datasets",
    "drop_columns",
    "get_dataset",
    "load_definition",
    "order_rows",
    "read_report",
    "workbench",
]
