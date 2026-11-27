"""Example assets shipped with data_foundry.

Two tiny synthetic :class:`CuratedContainer`s, so that users can exercise the ``load`` API and the task view
(``container.task()``) without first downloading any data: ``load_toy_container()`` gives the format-1 toy (binary
classification, IID folds: the shape of the BeyondArena containers), ``load_toy_container(format_version=2)`` the
format-2 toy (claims per year insured grouped by customer, a weight scoring column that is also the training weight,
an ordered category: the shape of the TabArena v0.2 containers). To rebuild them, run
``python scripts/build_toy_container.py`` from the repo root.
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path

from data_foundry.curation_container import CuratedContainer

TOY_CONTAINER_UNIQUE_NAME = "toy_iid_dataset"
"""``unique_name`` of the toy dataset shipped with this package."""

TOY_CONTAINER_UUID = "00000000-0000-7000-8000-000000000001"
"""Pinned UUID of the toy curated container shipped with this package."""

TOY_V2_CONTAINER_UNIQUE_NAME = "toy_grouped_rates"
"""``unique_name`` of the format-2 toy dataset shipped with this package."""

TOY_V2_CONTAINER_UUID = "00000000-0000-7000-8000-000000000002"
"""Pinned UUID of the format-2 toy container shipped with this package."""

_TOYS = {1: (TOY_CONTAINER_UNIQUE_NAME, TOY_CONTAINER_UUID), 2: (TOY_V2_CONTAINER_UNIQUE_NAME, TOY_V2_CONTAINER_UUID)}


def get_toy_container_path(format_version: int = 1) -> Path:
    """Return the on-disk path to the bundled toy curated container of ``format_version`` (1 or 2)."""
    if format_version not in _TOYS:
        raise ValueError(f"the toy containers are of format 1 and 2, not {format_version!r}.")
    unique_name, uuid = _TOYS[format_version]
    base = resources.files("data_foundry").joinpath("examples", "toy_container", unique_name, uuid)
    # `resources.files()` returns a Traversable; for files already on disk
    # (the regular install case) `str(...)` resolves to a real path.
    return Path(str(base))


def load_toy_container(
    *,
    format_version: int = 1,
    load_dataset: bool = True,
    load_test_data: bool = False,
) -> CuratedContainer:
    """Load the toy :class:`CuratedContainer` of ``format_version`` shipped with data_foundry (default: format 1)."""
    return CuratedContainer.load(
        get_toy_container_path(format_version),
        load_dataset=load_dataset,
        load_test_data=load_test_data,
    )


__all__ = [
    "TOY_CONTAINER_UNIQUE_NAME",
    "TOY_CONTAINER_UUID",
    "TOY_V2_CONTAINER_UNIQUE_NAME",
    "TOY_V2_CONTAINER_UUID",
    "get_toy_container_path",
    "load_toy_container",
]
