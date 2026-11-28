"""Probes for curating a tabular dataset: leaks, task difficulty, groups, hidden groups, time order, generated data,
dtypes.

``data-foundry probe {leak,task,group,hidden-groups,time,dtypes,generated} NAME...`` runs one on datasets of a working
copy (``cli``). Each probe's core takes plain inputs (a pandas frame, the target column, the problem type, group or
time columns, and splits as lists of ``(train_idx, test_idx)`` row positions) and returns plain numbers, so it runs on
a table from any source; its ``probe(name, root, args)`` reads a dataset through ``inputs`` first. Modules:

* ``cli``: the ``probe`` command, its shared options and each probe's own.
* ``inputs``: a definition or a built container as the probes take it (``ProbeInput``); the model inputs are the
  package's ``feature_columns``, never the target, group, scoring or unit columns.
* ``encode``: the model inputs as numbers (``numeric``) or as LightGBM reads them (``native``), and text columns as
  TF-IDF + SVD components.
* ``scoring``: ROC AUC, R^2, skill against the dummy, the training weight and the task's declared metric.
* ``models``: the model families, untuned and regularised LightGBM, and the foundation-model wrappers.
* ``leak``: what a model learns from the data that it should not, the raw state before ``_clean``, the target by
  period, the weight proxy and the leak tests of a split forced from temporal (probes 1 to 23 of ``leak_checks.md``).
* ``stationarity``: is the target's relation to the features flat across the periods the data holds (SPLIT-32).
* ``task``: is the task worth benchmarking, or empty, solved, or the same for every model.
* ``groups``: for a grouped task, does the grouping matter, and is there signal across groups.
* ``hidden_groups``: columns, composite keys and near copies that act as an entity, which a random split would leak.
* ``time_recovery``: does a table whose split is not temporal still carry a time order.
* ``generated``: is the target a formula or a rule set of the features, or were the columns drawn one by one.
* ``dtypes``: is each column typed by its meaning (a count numeric, a code categorical), against its values, its name
  and the source's codebook.

``problem_type`` is ``"regression"`` or a classification type (any other value). A task with a training weight
passes it as ``sample_weight`` (one value per row); the probes that fit models fit and score with it. The probes need
the ``probes`` extra (``pip install data-foundry[probes]``).
"""

from __future__ import annotations
