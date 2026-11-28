"""Dependencies that building a dataset needs beyond the core install (the ``build`` extra)."""

from __future__ import annotations

import importlib
from types import ModuleType

BUILD_INSTALL = "pip install 'data-foundry[build]'"


def import_build_dependency(module: str, extra: str = "build") -> ModuleType:
    """Import ``module``, or raise an ImportError that names the extra installing it.

    Loading and using containers needs only the core dependencies. Making splits, running the group checks and
    building a dataset need the ``build`` extra (scikit-learn, and the readers some definitions import); the
    recommended encodings of dates and text need the ``encodings`` extra.
    """
    try:
        return importlib.import_module(module)
    except ImportError as error:
        package = module.split(".", maxsplit=1)[0]
        install = BUILD_INSTALL if extra == "build" else f"pip install 'data-foundry[{extra}]'"
        msg = f"This needs `{package}`, which the {extra} extra installs: {install}"
        raise ImportError(msg) from error
