"""The old import path of the definition API, kept while open pull requests still use it.

The modules of ``data_foundry.v2`` moved into the package on 2026-11-25: the definition API to
:mod:`data_foundry.definition`, the metrics to :mod:`data_foundry.metrics`, the train sampler to
:mod:`data_foundry.sampling`, special features to :mod:`data_foundry.special` and the encodings to
:mod:`data_foundry.encodings`. ``from data_foundry.v2 import X`` and ``import data_foundry.v2.<module>`` resolve to
the new homes, so a definition written against the old path keeps working. New code imports the new paths; this shim
goes once the open pull requests are merged.
"""

from __future__ import annotations

import importlib
import sys

from data_foundry.definition import *  # noqa: F403 - the old path re-exports the definition API
from data_foundry.definition import __all__  # noqa: F401

_MOVED = {
    "metrics": "data_foundry.metrics",
    "encodings": "data_foundry.encodings",
    "special": "data_foundry.special",
    "chemistry": "data_foundry.special.chemistry",
    "spectra": "data_foundry.special.spectra",
    "_optional": "data_foundry.utils.optional",
    **{
        name: f"data_foundry.definition.{name}"
        for name in (
            "dataset",
            "preprocessing",
            "registry",
            "workbench",
            "report",
            "cli",
            "splits",
            "windows",
            "task_checks",
            "group_checks",
        )
    },
}

for _old, _new in _MOVED.items():
    _module = importlib.import_module(_new)
    sys.modules[f"{__name__}.{_old}"] = _module
    globals()[_old] = _module
