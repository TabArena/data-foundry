"""data-foundry v2: define a curated dataset as one Python class instead of a notebook.

See :mod:`data_foundry.definition.dataset` for the interface, :mod:`data_foundry.definition.preprocessing` for the
standard steps, :mod:`data_foundry.definition.splits` for the split protocol, :mod:`data_foundry.metrics` for the
metrics and their scorers, :mod:`data_foundry.special.chemistry` for SMILES columns, :mod:`data_foundry.special.spectra`
for spectra, :mod:`data_foundry.special` for special features (what a definition declares in ``special_features``),
:mod:`data_foundry.definition.registry` for discovery and :mod:`data_foundry.definition.report` for the generated
``README.md``.
"""

from __future__ import annotations

from data_foundry.definition.dataset import (
    AUTO,
    AbstractCuratedDataset,
    CurationResult,
    DatasetDefinitionError,
    Decision,
    FeatureTypes,
    NonFeature,
    TaskSummary,
    clean_text,
)
from data_foundry.definition.preprocessing import (
    anonymize_ids,
    cast_dtypes,
    decode,
    drop_columns,
    order_rows,
    provenance_columns,
    read_files,
    set_missing,
)
from data_foundry.definition.registry import discover_datasets, get_dataset, load_definition
from data_foundry.definition.report import read_report
from data_foundry.definition.splits import SplitPlan, Splits, Temporal, TemporalSplits, window_bounds
from data_foundry.definition.windows import Window, candidate_windows, window_stats
from data_foundry.definition.workbench import workbench
from data_foundry.encodings import Encoding
from data_foundry.metrics import Metric
from data_foundry.schema import (
    Grouping,
    RawFile,
    RowBudget,
    ScoringColumn,
    Source,
    SpecialFeature,
    SpectrumDetails,
    TrainSampling,
    UnitWeight,
)
from data_foundry.special import SpecialColumn, SpecialColumnGroup
from data_foundry.special.chemistry import (
    DEFAULT_SMILES_ENCODING,
    Smiles,
    canonical_smiles,
    encode_smiles,
    invalid_smiles,
    murcko_scaffolds,
    rdkit_descriptors,
    scaffold_groups,
)
from data_foundry.special.spectra import Spectrum
from data_foundry.time_basis import GroupBasis, TimeBasis
from data_foundry.utils.dtypes import object_columns

__all__ = [
    "AUTO",
    "DEFAULT_SMILES_ENCODING",
    "AbstractCuratedDataset",
    "CurationResult",
    "DatasetDefinitionError",
    "Decision",
    "Encoding",
    "FeatureTypes",
    "GroupBasis",
    "Grouping",
    "Metric",
    "NonFeature",
    "RawFile",
    "RowBudget",
    "ScoringColumn",
    "Smiles",
    "Source",
    "SpecialColumn",
    "SpecialColumnGroup",
    "SpecialFeature",
    "Spectrum",
    "SpectrumDetails",
    "SplitPlan",
    "Splits",
    "TaskSummary",
    "Temporal",
    "TemporalSplits",
    "TimeBasis",
    "TrainSampling",
    "UnitWeight",
    "Window",
    "anonymize_ids",
    "candidate_windows",
    "canonical_smiles",
    "cast_dtypes",
    "clean_text",
    "decode",
    "discover_datasets",
    "drop_columns",
    "encode_smiles",
    "get_dataset",
    "invalid_smiles",
    "load_definition",
    "murcko_scaffolds",
    "object_columns",
    "order_rows",
    "provenance_columns",
    "rdkit_descriptors",
    "read_files",
    "read_report",
    "scaffold_groups",
    "set_missing",
    "window_bounds",
    "window_stats",
    "workbench",
]
