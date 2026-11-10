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
import types
from pathlib import Path

from data_foundry.v2.dataset import DEFINITION_FILENAME, AbstractCuratedDataset, DatasetDefinitionError, is_task

logger = logging.getLogger(__name__)

_MODULE_PREFIX = "data_foundry_datasets"
"""Namespace under which definition files are registered in ``sys.modules`` (so ``reload`` works)."""


def _module_name(definition: Path) -> str:
    # The folder name alone could collide between two dataset roots; the path hash keeps them apart.
    digest = hashlib.blake2b(str(definition.resolve().parent.parent).encode(), digest_size=4).hexdigest()
    return f"{_MODULE_PREFIX}.{definition.parent.name}_{digest}"


def load_definition(definition: Path | str) -> type[AbstractCuratedDataset]:
    """Import one ``dataset.py`` and return the single definition class it defines: a task, or a parent of tasks.

    The definition is the class defined in the file that declares its own ``unique_name``; a parent it imports
    (``import_definition``) or a helper base class is not it.

    Raises:
        FileNotFoundError: ``definition`` does not exist.
        LookupError: The file defines no definition class, or more than one.
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
        and not isinstance(obj, types.GenericAlias)  # Python 3.10 counts an alias like `Splits` as a class
        and issubclass(obj, AbstractCuratedDataset)
        and obj.__module__ == name
        and "unique_name" in vars(obj)
    ]
    if len(classes) != 1:
        found = ", ".join(c.__name__ for c in classes) or "none"
        raise LookupError(f"{definition} must define exactly one dataset class, found: {found}")
    return classes[0]


_IMPORTING: list[Path] = []
"""The definitions :func:`import_definition` is importing, outermost first (a circular family fails, not hangs)."""


def import_definition(name: str, root: Path | str | None = None) -> type[AbstractCuratedDataset]:
    """The definition class of the folder ``name`` next to the calling one, to derive a child from it.

    ::

        ExamScores = import_definition("exam_scores")


        class ExamScoresMath(ExamScores):
            unique_name = "exam_scores_math"
            derivation = "The math score as the target."
            ...

    Args:
        name: The parent's folder (its ``unique_name``) in the same root as the calling ``dataset.py``.
        root: The folder of dataset folders. Default: the one holding the calling file's folder; from a notebook,
            the parent of the current directory (a notebook next to a ``dataset.py``).

    Raises:
        ImportError: The definitions import each other in a circle.
    """
    if root is None:
        caller = inspect.currentframe().f_back.f_globals.get("__file__")
        root = Path(caller).resolve().parent.parent if caller else Path.cwd().resolve().parent
    definition = (Path(root) / name / DEFINITION_FILENAME).resolve()
    if definition in _IMPORTING:
        chain = " -> ".join(p.parent.name for p in [*_IMPORTING, definition])
        raise ImportError(f"The definitions import each other in a circle: {chain}.")
    _IMPORTING.append(definition)
    try:
        return load_definition(definition)
    finally:
        _IMPORTING.pop()


def discover_datasets(root: Path | str, *, strict: bool = True) -> dict[str, type[AbstractCuratedDataset]]:
    """The tasks under ``root`` by ``unique_name``: :func:`discover_definitions` without the parents."""
    return {name: cls for name, cls in discover_definitions(root, strict=strict).items() if is_task(cls)}


def discover_definitions(root: Path | str, *, strict: bool = True) -> dict[str, type[AbstractCuratedDataset]]:
    """Import every ``<root>/*/dataset.py`` and return the definition classes (tasks and parents) by ``unique_name``.

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
    """Import ``<root>/<name>/dataset.py`` and return an instance of its definition class (a task or a parent)."""
    return instance(load_definition(Path(root) / name / DEFINITION_FILENAME))


def instance(cls: type[AbstractCuratedDataset]) -> AbstractCuratedDataset:
    """An instance of a definition class.

    Raises:
        DatasetDefinitionError: ``cls`` is a partial parent (no ``_load_raw``), which shares code only.
    """
    if inspect.isabstract(cls) and not is_task(cls):
        msg = (
            f"{cls.__name__} is a partial parent: it shares code with its children and has no `_load_raw`, so there "
            "is no data to check; check its children."
        )
        raise DatasetDefinitionError(msg)
    return cls()
