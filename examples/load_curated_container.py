"""Load a :class:`CuratedContainer` and inspect its metadata and its extra files.

Every container is a self-contained directory with a dataset (parquet), the
preserved column dtypes, three pieces of structured metadata, and the
container-level integrity info (uuid + checksum). All of it round-trips
through :meth:`CuratedContainer.save` / :meth:`CuratedContainer.load`, for both
container formats (1: the shipped BeyondArena containers, 2: a v2 definition's).

A producer may also ship extra files next to the core ones (embedding caches,
per-fold predictions, documentation). Data Foundry does not interpret them; it
lists them and resolves their paths, and the caller loads them. The toy container
ships one, ``toy_extra.parquet``.

Run::

    # Use the toy container shipped with the package (no download needed).
    python examples/load_curated_container.py

    # Or point at any container in your warehouse or cache.
    python examples/load_curated_container.py /path/to/warehouse/<name>/<uuid>
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from data_foundry.curation_container import CuratedContainer
from data_foundry.examples import get_toy_container_path


def main(path: Path) -> None:
    """Print the container's identity, data, metadata and extra files."""
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
    print(f"  container format:   {container.format_version}")  # 1: a v1 notebook, 2: a v2 definition
    print(f"  target_column_name: {tm.target_column_name}")
    print(f"  problem_type:       {tm.problem_type}")
    print(f"  objective_metric:   {tm.objective_metric_name}")
    print(f"  stratify_on:        {tm.stratify_on}")
    print(f"  group_on:           {tm.group_on}")
    print(f"  time_on:            {tm.time_on}")
    # How a grouped task is used (prediction unit, aggregation, context): format 2 only; None for IID and temporal.
    grouping = container.grouping if container.format_version >= 2 else None
    if grouping is not None:
        print(f"  prediction_unit:    {grouping.prediction_unit} (aggregation: {grouping.aggregation})")
        print(f"  group context:      {grouping.context}")

    print("\n-- Experiment metadata --")
    em = container.experiment_metadata
    print(f"  # repeats:           {len(em.splits)}")
    print(f"  # folds of repeat 0: {len(em.splits[0])}")
    print(f"  splits_comment:      {em.splits_comment}")

    print("\n-- Extra files --")
    extras = container.list_extra_files()
    print(f"  present: {extras or '(none)'}")
    if extras:
        resolved = container.extra_file_path(extras[0])  # raises for a name that is not a plain extra file
        print(f"  {extras[0]} -> {resolved}")
        if resolved.suffix == ".parquet":
            print(pd.read_parquet(resolved).head().to_string())


if __name__ == "__main__":
    container_path = Path(sys.argv[1]) if len(sys.argv) > 1 else get_toy_container_path()
    main(container_path)
