"""The dependency direction between the packages: ``data_foundry.definition`` uses the checks, never the reverse."""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path


def test_importing_the_checks_loads_no_definition_module() -> None:
    """Every module of ``data_foundry.checks``, imported in a fresh interpreter (so the modules other tests imported
    do not count), loads no module of ``data_foundry.definition``.
    """
    code = (
        "import importlib, pkgutil, sys\n"
        "import data_foundry.checks as package\n"
        "for info in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):\n"
        "    importlib.import_module(info.name)\n"
        "print(sorted(m for m in sys.modules if m.startswith('data_foundry.definition')))\n"
    )
    env = {**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)}
    run = subprocess.run(  # noqa: S603 - a fixed snippet, run with this interpreter
        [sys.executable, "-c", code], capture_output=True, text=True, check=True, env=env
    )
    assert run.stdout.strip() == "[]"


def test_no_checks_module_imports_the_definition_package() -> None:
    """Also inside a function or under ``TYPE_CHECKING``, where an import does not run when the module loads."""
    checks = Path(__file__).resolve().parents[1] / "src" / "data_foundry" / "checks"
    found = []
    for path in sorted(checks.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else []
            if isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module, *(f"{node.module}.{a.name}" for a in node.names)]
            if any(n == "data_foundry.definition" or n.startswith("data_foundry.definition.") for n in names):
                found.append(f"{path.name}:{node.lineno}")
    assert found == []
