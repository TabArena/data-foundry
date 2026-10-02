"""One call to set up a notebook next to a ``dataset.py``: :func:`workbench`."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_foundry.v2.dataset import DEFINITION_FILENAME, AbstractCuratedDataset
from data_foundry.v2.registry import load_definition


def workbench(path: Path | str | None = None, *, wide_display: bool = True) -> AbstractCuratedDataset:
    """Load the dataset defined next to the notebook and switch it to automatic reloading.

    Args:
        path: The dataset folder or its ``dataset.py`` (default: the current directory, which is the
            notebook's folder in Jupyter and VS Code).
        wide_display: Show all columns and full cell text in pandas output.

    Returns:
        The dataset. Every access to ``ds.raw`` / ``ds.df`` / ``ds.check()`` first re-imports
        ``dataset.py`` if it changed on disk; the raw data stays cached while ``_load_raw`` is unchanged.
    """
    folder = Path.cwd() if path is None else Path(path)
    definition = folder if folder.name == DEFINITION_FILENAME else folder / DEFINITION_FILENAME
    ds = load_definition(definition)()
    ds.auto_reload = True
    if wide_display:
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_colwidth", 200)
    return ds
