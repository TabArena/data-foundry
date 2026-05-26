"""Example assets shipped with data_foundry.

Currently exposes a tiny synthetic :class:`CuratedContainer` so that users can
exercise the ``load`` API without first downloading any data. To rebuild the
shipped toy container, run ``python scripts/build_toy_container.py`` from the
repo root.
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path

from data_foundry.curation_container import CuratedContainer

TOY_CONTAINER_UNIQUE_NAME = "toy_iid_dataset"
"""``unique_name`` of the toy dataset shipped with this package."""

TOY_CONTAINER_UUID = "00000000-0000-7000-8000-000000000001"
"""Pinned UUID of the toy curated container shipped with this package."""


def get_toy_container_path() -> Path:
    """Return the on-disk path to the bundled toy curated container."""
    base = resources.files("data_foundry").joinpath(
        "examples",
        "toy_container",
        TOY_CONTAINER_UNIQUE_NAME,
        TOY_CONTAINER_UUID,
    )
    # `resources.files()` returns a Traversable; for files already on disk
    # (the regular install case) `str(...)` resolves to a real path.
    return Path(str(base))


def load_toy_container(
    *,
    load_dataset: bool = True,
    load_test_data: bool = False,
) -> CuratedContainer:
    """Load the toy :class:`CuratedContainer` shipped with data_foundry."""
    return CuratedContainer.load(
        get_toy_container_path(),
        load_dataset=load_dataset,
        load_test_data=load_test_data,
    )


__all__ = [
    "TOY_CONTAINER_UNIQUE_NAME",
    "TOY_CONTAINER_UUID",
    "get_toy_container_path",
    "load_toy_container",
]
