"""Discover dataset definitions: every ``<root>/<name>/dataset.py`` that holds one dataset class.

The package knows no dataset root; callers pass it in (a repository keeps its datasets wherever it
likes). Discovery only imports the definition files, which reads no data, so listing a few hundred
datasets and validating their metadata is cheap.
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import logging
import sys
from pathlib import Path

from data_foundry.v2.dataset import DEFINITION_FILENAME, AbstractCuratedDataset

logger = logging.getLogger(__name__)

_MODULE_PREFIX = "data_foundry_datasets"
"""Namespace under which definition files are registered in ``sys.modules`` (so ``reload`` works)."""


def _module_name(definition: Path) -> str:
    # The folder name alone could collide between two dataset roots; the path hash keeps them apart.
    digest = hashlib.blake2b(str(definition.resolve().parent.parent).encode(), digest_size=4).hexdigest()
    return f"{_MODULE_PREFIX}.{definition.parent.name}_{digest}"


def load_definition(definition: Path | str) -> type[AbstractCuratedDataset]:
    """Import one ``dataset.py`` and return the single concrete dataset class it defines.

    Raises:
        FileNotFoundError: ``definition`` does not exist.
        LookupError: The file defines no concrete dataset class, or more than one.
        DatasetDefinitionError: The class is incomplete or inconsistent (raised at import).
    """
    definition = Path(definition).resolve()
    if definition.is_dir():
        definition = definition / DEFINITION_FILENAME
    if not definition.is_file():
        raise FileNotFoundError(definition)

    name = _module_name(definition)
    spec = importlib.util.spec_from_file_location(name, definition)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import {definition}")
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(name)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
        raise

    classes = [
        obj
        for obj in vars(module).values()
        if inspect.isclass(obj)
        and issubclass(obj, AbstractCuratedDataset)
        and obj.__module__ == name
        and not inspect.isabstract(obj)
    ]
    if len(classes) != 1:
        found = ", ".join(c.__name__ for c in classes) or "none"
        raise LookupError(f"{definition} must define exactly one dataset class, found: {found}")
    return classes[0]


def discover_datasets(root: Path | str, *, strict: bool = True) -> dict[str, type[AbstractCuratedDataset]]:
    """Import every ``<root>/*/dataset.py`` and return the dataset classes by ``unique_name``.

    Args:
        root: The folder holding one sub-folder per dataset.
        strict: Raise on the first definition that fails to import. With False, broken definitions are
            logged and skipped, but an all-broken root still raises (that is a broken environment, not
            one bad dataset).

    Raises:
        FileNotFoundError: ``root`` is not a directory.
        RuntimeError: Every definition failed to import (only with ``strict=False``).
    """
    root = Path(root)
    if not root.is_dir():
        raise FileNotFoundError(root)

    registry: dict[str, type[AbstractCuratedDataset]] = {}
    skipped: list[str] = []
    for definition in sorted(root.glob(f"*/{DEFINITION_FILENAME}")):
        try:
            cls = load_definition(definition)
        except Exception as error:
            if strict:
                raise
            logger.warning("Skipping %s: %s: %s", definition.parent.name, type(error).__name__, error)
            skipped.append(definition.parent.name)
            continue
        registry[cls.dataset_metadata.unique_name] = cls

    if skipped and not registry:
        raise RuntimeError(
            f"Every dataset definition under {root} failed to import ({', '.join(skipped)}); see the warnings above.",
        )
    return registry


def get_dataset(root: Path | str, name: str) -> AbstractCuratedDataset:
    """Import ``<root>/<name>/dataset.py`` and return an instance of its dataset class."""
    return load_definition(Path(root) / name / DEFINITION_FILENAME)()
