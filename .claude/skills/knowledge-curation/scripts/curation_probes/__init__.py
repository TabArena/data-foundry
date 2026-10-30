"""Probes for curating a tabular dataset: leaks, task difficulty, groups, hidden groups and generated data.

The probes are tooling-independent: every function takes plain inputs (a pandas frame, the target column, the problem
type, group or time columns, and splits as lists of ``(train_idx, test_idx)`` row positions) and returns plain numbers,
so they run on a table from any source. Modules:

* ``leak``: what a model learns from the data that it should not (single features, missing indicators, copies of
  test rows in train, nearest neighbours, string columns).
* ``task``: is the task worth benchmarking, or empty, solved, or the same for every model (baselines, three model
  families, the best single feature, and flags for the curator).
* ``groups``: for a grouped task, does the grouping matter, and is there signal across groups.
* ``hidden_groups``: columns, composite keys and near copies that act as an entity, which a random split would leak.
* ``generated``: is the target a formula or a rule set of the features, or were the columns drawn one by one.
* ``label_maturity``: release-boundary event rates across explicit windows and end buffers.
* ``duplicate_contamination``: exact-profile matches by label/multiplicity on actual folds, with aligned row losses.
* ``text``: the numeric model inputs and the TF-IDF + SVD text encoding the probes share.

``problem_type`` is ``"regression"`` or a classification type (any other value). Import the package with the folder
that holds it on ``sys.path``.
"""

from __future__ import annotations
