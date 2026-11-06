"""Probes for curating a tabular dataset: leaks, task difficulty, groups, hidden groups, generated data, dtypes.

The probes are tooling-independent: every function takes plain inputs (a pandas frame, the target column, the problem
type, group or time columns, and splits as lists of ``(train_idx, test_idx)`` row positions) and returns plain numbers,
so they run on a table from any source. Modules:

* ``leak``: what a model learns from the data that it should not (single features, missing indicators, copies of
  test rows in train by label on every split, nearest neighbours, string columns), the target by period, the test
  for right-censoring at the release end (``target_by_period``, probe 13), and the raw state before ``_clean``: the
  target in the source's row order, the rows it removed, the columns it dropped, copies before deduplication
  (``row_order``, ``removed_rows``, ``dropped_column_proxies``, ``raw_copies``; probes 10, 19, 20, 21).
* ``task``: is the task worth benchmarking, or empty, solved, or the same for every model (baselines, three model
  families, the best single feature, and flags for the curator).
* ``groups``: for a grouped task, does the grouping matter, and is there signal across groups.
* ``hidden_groups``: columns, composite keys and near copies that act as an entity, which a random split would leak.
* ``generated``: is the target a formula or a rule set of the features, or were the columns drawn one by one.
* ``dtypes``: is each column typed by its meaning (a count numeric, a code categorical), against its values,
  its name and the source's codebook.
* ``text``: the numeric model inputs and the TF-IDF + SVD text encoding the probes share.
* ``time_recovery``: does a table whose split is not temporal still carry a time order (date columns, dropped
  date columns, the target along the row order or an ID, few-valued columns that encode the period, rows that repeat
  one block later, one entity's rows in consecutive runs, class blocks that are several pieces).

``problem_type`` is ``"regression"`` or a classification type (any other value). Import the package with the folder
that holds it on ``sys.path``.
"""

from __future__ import annotations
