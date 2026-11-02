"""data-foundry v2: define a curated dataset as one Python class instead of a notebook.

See :mod:`data_foundry.v2.dataset` for the interface, :mod:`data_foundry.v2.preprocessing` for the standard
steps, :mod:`data_foundry.v2.splits` for the split protocol, :mod:`data_foundry.v2.metrics` for the metrics and
their scorers, :mod:`data_foundry.v2.chemistry` for SMILES columns, :mod:`data_foundry.v2.spectra` for spectra,
:mod:`data_foundry.v2.registry` for discovery and :mod:`data_foundry.v2.report` for the generated ``README.md``.
"""

from __future__ import annotations

from data_foundry.schema import FeatureGroup, Grouping, ScoringColumn, SemanticColumn
from data_foundry.utils.dtypes import object_columns
from data_foundry.v2.chemistry import (
    DEFAULT_SMILES_ENCODING,
    canonical_smiles,
    encode_smiles,
    invalid_smiles,
    murcko_scaffolds,
    rdkit_descriptors,
    scaffold_groups,
)
from data_foundry.v2.dataset import (
    AUTO,
    AbstractCuratedDataset,
    CurationResult,
    DatasetDefinitionError,
    Decision,
    FeatureTypes,
    TaskSummary,
    clean_text,
)
from data_foundry.v2.encodings import (
    Encoding,
    encode_datetime,
    encode_text_e5,
    encode_text_tfidf,
    recommended_encodings,
)
from data_foundry.v2.metrics import Metric, score, scorer
from data_foundry.v2.preprocessing import anonymize_ids, cast_dtypes, decode, drop_columns, order_rows, set_missing
from data_foundry.v2.registry import discover_datasets, get_dataset, load_definition
from data_foundry.v2.report import read_report
from data_foundry.v2.spectra import Spectrum, encode_spectrum, spectrum_encoding
from data_foundry.v2.splits import SplitPlan, Splits, Temporal, TemporalSplits
from data_foundry.v2.workbench import workbench

__all__ = [
    "AUTO",
    "DEFAULT_SMILES_ENCODING",
    "AbstractCuratedDataset",
    "CurationResult",
    "DatasetDefinitionError",
    "Decision",
    "Encoding",
    "FeatureGroup",
    "FeatureTypes",
    "Grouping",
    "Metric",
    "ScoringColumn",
    "SemanticColumn",
    "Spectrum",
    "SplitPlan",
    "Splits",
    "TaskSummary",
    "Temporal",
    "TemporalSplits",
    "anonymize_ids",
    "canonical_smiles",
    "cast_dtypes",
    "clean_text",
    "decode",
    "discover_datasets",
    "drop_columns",
    "encode_datetime",
    "encode_smiles",
    "encode_spectrum",
    "encode_text_e5",
    "encode_text_tfidf",
    "get_dataset",
    "invalid_smiles",
    "load_definition",
    "murcko_scaffolds",
    "object_columns",
    "order_rows",
    "rdkit_descriptors",
    "read_report",
    "recommended_encodings",
    "scaffold_groups",
    "score",
    "scorer",
    "set_missing",
    "spectrum_encoding",
    "workbench",
]
