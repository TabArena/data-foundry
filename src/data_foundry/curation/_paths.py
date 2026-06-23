from __future__ import annotations

import os
from pathlib import Path

DATA_FOUNDRY_CURATION_ENV = "DATA_FOUNDRY_CURATION_DIR"
"""Environment variable that overrides the curation root directory.

Set this when the curation backlog (records + vocabularies) does not live next
to the data-foundry source tree, e.g. on a pip-installed deployment where the
default would otherwise land inside ``site-packages``.
"""

DEFAULT_CURATION_ROOT = Path(__file__).resolve().parents[3] / "curation"
"""Default curation root (``<data-foundry-root>/curation``) for editable installs."""


def resolve_curation_root() -> Path:
    """Resolve the curation root directory.

    Precedence: ``$DATA_FOUNDRY_CURATION_DIR`` > :data:`DEFAULT_CURATION_ROOT`.
    The path is **not** created; callers that write are responsible for that.
    """
    return Path(os.environ.get(DATA_FOUNDRY_CURATION_ENV) or DEFAULT_CURATION_ROOT).expanduser()


def records_dir() -> Path:
    """Directory holding one ``<unique_name>.md`` curation record per dataset."""
    return resolve_curation_root() / "records"


def vocabularies_path() -> Path:
    """Path to the editable dropdown vocabularies (``vocabularies.yaml``)."""
    return resolve_curation_root() / "vocabularies.yaml"
