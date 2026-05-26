"""Load a downloaded :class:`CuratedContainer` and inspect its metadata.

Every container is a self-contained directory with a dataset (parquet), the
preserved column dtypes, three pieces of structured metadata, and the
container-level integrity info (uuid + checksum). All of it round-trips
through :meth:`CuratedContainer.save` / :meth:`CuratedContainer.load`.

Run::

    # Use the toy container shipped with the package (no download needed).
    python examples/load_curated_container.py

    # Or point at any container you've downloaded into your warehouse.
    python examples/load_curated_container.py /path/to/warehouse/<name>/<uuid>
"""

from __future__ import annotations

import sys
from pathlib import Path

from data_foundry.curation_container import CuratedContainer
from data_foundry.examples import get_toy_container_path


def main(path: Path) -> None:
    container = CuratedContainer.load(path)

    print(f"Loaded curated container from: {path}")
    print(f"  uuid:     {container.uuid}")
    print(f"  checksum: {container.checksum}")
    print(f"  unique_name: {container.unique_name}")

    print("\n-- Dataset --")
    df = container.dataset
    print(f"  shape:  {df.shape}")
    print(f"  dtypes:\n{df.dtypes.to_string()}")
    print(f"  head:\n{df.head().to_string()}")

    print("\n-- Dataset metadata --")
    dsm = container.dataset_metadata
    print(f"  domain:    {dsm.domain_str}")
    print(f"  source:    {dsm.dataset_source}")
    print(f"  license:   {dsm.license}")
    print(f"  data_tags: {dsm.data_tags}")

    print("\n-- Task metadata --")
    tm = container.task_metadata
    print(f"  target_column_name: {tm.target_column_name}")
    print(f"  problem_type:       {tm.problem_type}")
    print(f"  objective_metric:   {tm.objective_metric_name}")
    print(f"  stratify_on:        {tm.stratify_on}")
    print(f"  group_on:           {tm.group_on}")
    print(f"  time_on:            {tm.time_on}")

    print("\n-- Experiment metadata --")
    em = container.experiment_metadata
    print(f"  # repeats:           {len(em.splits)}")
    print(f"  # folds of repeat 0: {len(em.splits[0])}")
    print(f"  splits_comment:      {em.splits_comment}")


if __name__ == "__main__":
    container_path = Path(sys.argv[1]) if len(sys.argv) > 1 else get_toy_container_path()
    main(container_path)
