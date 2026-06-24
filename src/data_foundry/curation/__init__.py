"""Git-native curation backlog: one record per candidate dataset.

This subpackage replaces the legacy curation Google Sheet with a code-able,
git-trackable representation:

* :class:`~data_foundry.curation.record.CurationRecord` — the per-dataset schema;
* :mod:`~data_foundry.curation.store` — one markdown file per record;
* :mod:`~data_foundry.curation.exporter` — one-way compile to CSV/Parquet/Sheet;
* the local dashboard + CLI (``data_foundry.curation.app`` / ``cli``).
"""

from __future__ import annotations

from data_foundry.curation._paths import records_dir, resolve_curation_root, vocabularies_path
from data_foundry.curation.record import (
    FIELDS,
    FIELDS_BY_NAME,
    CurationRecord,
    FieldSpec,
    load_vocabularies,
    save_vocabularies,
)
from data_foundry.curation.store import (
    load_all,
    load_index,
    load_record,
    markdown_to_record,
    record_to_markdown,
    save_record,
)

__all__ = [
    "FIELDS",
    "FIELDS_BY_NAME",
    "CurationRecord",
    "FieldSpec",
    "load_all",
    "load_index",
    "load_record",
    "load_vocabularies",
    "markdown_to_record",
    "record_to_markdown",
    "records_dir",
    "resolve_curation_root",
    "save_record",
    "save_vocabularies",
    "vocabularies_path",
]
