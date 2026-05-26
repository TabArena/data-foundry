"""Side-by-side look at the BeyondArena data regimes.

Loads one container from each regime and prints its task/split metadata so
you can see how IID vs. grouped non-IID vs. temporal non-IID surface
through the curated metadata:

* ``airfoil_self_noise``                          — IID (random splits)
* ``parkinsons_biomedical_voice_measurements``    — grouped non-IID, one label
  per group (``group_labels="per_group"``; all rows of a subject share the
  same target value)
* ``asp_potassco_classification``                 — grouped non-IID, label per
  sample (``group_labels="per_sample"``; rows in the same group can have
  different targets)
* ``garments_worker_productivity``                — temporal non-IID (split on
  ``time_on``; future rows must not leak backwards)

The key distinguisher is which column the task sets:

* ``time_on`` set        → temporal non-IID
* ``group_on`` set       → grouped non-IID
* neither set            → IID

Run::

    python examples/data_foundry_data_regimes.py
"""

from __future__ import annotations

from data_foundry.collections import BEYOND_ARENA


def main() -> None:
    # IID Dataset
    container = BEYOND_ARENA.get_dataset("airfoil_self_noise")
    print("\n#### IID Dataset (random splits)")
    print(container.describe())

    # Grouped non-IID Dataset (group_labels="per_group" — one label shared across the whole group).
    container = BEYOND_ARENA.get_dataset("parkinsons_biomedical_voice_measurements")
    print("\n#### Grouped non-IID Dataset (group_labels='per_group' — one label shared across the whole group)")
    print(container.describe())

    # Grouped non-IID Dataset (group_labels="per_sample" — each row in a group can have its own label).
    print("\n#### Grouped non-IID Dataset (group_labels='per_sample' — each row in a group can have its own label)")
    container = BEYOND_ARENA.get_dataset("asp_potassco_classification")
    print(container.describe())

    # Temporal non-IID Dataset
    print("\n#### Temporal non-IID Dataset (split on `time_on` — future rows must not leak backwards)")
    container = BEYOND_ARENA.get_dataset("garments_worker_productivity")
    print(container.describe())



if __name__ == "__main__":
    main()
