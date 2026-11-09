"""TabArena v0.2's working copy: what every definition in this folder is built with.

``row_budget``: the collection's row budget, set here once for every dataset folder next to this file
(``data_foundry.v2.dataset.collection_row_budget``). A definition does not declare it. When its splits have a side
over the budget, it is the version ``<name>_1m`` (folder and ``unique_name``): the build samples each test side to
500k rows and records the budget with the train sampling a benchmark uses to fit on at most 1M rows. The build
refuses a dataset over the budget without the suffix, and a ``_1m`` version whose splits keep within the budget anyway.
"""

from __future__ import annotations

from data_foundry.collections import TABARENA_V0PT2_ROW_BUDGET

row_budget = TABARENA_V0PT2_ROW_BUDGET
