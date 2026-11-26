"""The Data Foundry checks: every rule a curated dataset is checked against, and the registry of their slugs.

* :mod:`~data_foundry.checks.bundle`: the bundle checks of a container (frame, task, splits, metadata) and the
  round trip of a saved one (:func:`run_bundle_checks`, :func:`verify_saved_container`);
* :mod:`~data_foundry.checks.task` and :mod:`~data_foundry.checks.groups`: the checks of a v2 task (every test fold
  scorable, the group statistics);
* :mod:`~data_foundry.checks.protocol`: the numbers of the v2 split protocol and the checks that hold a format-2
  container to them and to its row budget (:func:`~data_foundry.checks.protocol.protocol_checks`);
* :mod:`~data_foundry.checks.tables`: the summary tables of a frame that each dataset's README shows
  (:func:`run_all_checks`);
* :mod:`~data_foundry.checks.registry`: every slug with its severities, stage and whether a definition may accept it;
* :mod:`~data_foundry.checks.results`: a finding (:class:`CheckResult`) and a report (:class:`BundleCheckReport`).

The time basis's checks stay with its rules (:func:`data_foundry.time_basis.problems`); the bundle checks run them.
The curation checks that need a definition class (the definition file, the training floor and the test windows of a
temporal split, the raw files) and the acceptance of findings are :mod:`data_foundry.definition.checks`: this
package imports nothing of :mod:`data_foundry.definition`.
"""

from __future__ import annotations

from data_foundry.checks.bundle import run_bundle_checks, verify_saved_container
from data_foundry.checks.results import BundleCheckReport, CheckResult
from data_foundry.checks.tables import run_all_checks

__all__ = ["BundleCheckReport", "CheckResult", "run_all_checks", "run_bundle_checks", "verify_saved_container"]
