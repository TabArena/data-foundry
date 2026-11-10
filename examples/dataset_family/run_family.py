"""Run the example family: generate its raw files, check the parent and its two tasks, and try a third task.

The definitions are the folders next to this script (``exam_scores``, ``exam_scores_math``, ``exam_scores_reading``);
the README of this folder explains the idea. Nothing is built and no file in the repository is written.

Run from the repository root::

    python examples/dataset_family/run_family.py                  # a temporary warehouse
    python examples/dataset_family/run_family.py /path/to/warehouse
"""

from __future__ import annotations

import contextlib
import os
import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from data_foundry.schema import DATA_FOUNDRY_WAREHOUSE_ENV
from data_foundry.v2 import Metric, TaskSummary, discover_definitions, get_dataset, load_definition
from data_foundry.v2.dataset import is_task, parent_definition

FAMILY = Path(__file__).resolve().parent
"""The folder of the family's definitions, one ``<name>/dataset.py`` each (this script's folder)."""

SCHOOLS = {"Ashford": 3.0, "Brookside": -2.0, "Cedar Hill": 0.0, "Dunmore": 5.0, "Elmwood": -4.0, "Fairview": 1.0}
"""The schools of the generated data, with how much better or worse their students score."""


def write_raw_files(folder: Path, students_per_school: int = 40) -> list[Path]:
    """Write one CSV per school into ``folder``: one row per student, with the two exam scores."""
    folder.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)
    paths = []
    for school, effect in SCHOOLS.items():
        n = students_per_school
        df = pd.DataFrame(
            {
                "study_hours_per_week": rng.uniform(0, 20, n).round(1),
                "attendance": rng.uniform(0.6, 1.0, n).round(2),
                "parents_education": rng.choice(["primary", "secondary", "tertiary"], n, p=[0.2, 0.5, 0.3]),
                "last_year_grade": rng.normal(70, 10, n).clip(30, 100).round(),
            },
        )
        education = df["parents_education"].map({"primary": -3.0, "secondary": 0.0, "tertiary": 3.0})
        ability = (
            1.2 * df["study_hours_per_week"]
            + 30 * (df["attendance"] - 0.8)
            + 0.5 * (df["last_year_grade"] - 70)
            + education
            + effect
            + rng.normal(0, 4, n)
        )
        df["math_score"] = (50 + ability + rng.normal(0, 4, n)).clip(0, 100).round()
        df["reading_score"] = (55 + 0.8 * ability + rng.normal(0, 4, n)).clip(0, 100).round()
        path = folder / f"{school.replace(' ', '_')}.csv"
        df.to_csv(path, index=False)
        paths.append(path)
    return paths


@contextlib.contextmanager
def _warehouse(path: Path | None) -> Iterator[Path]:
    """Point Data Foundry at ``path`` (default: a temporary folder) while the family runs."""
    previous = os.environ.get(DATA_FOUNDRY_WAREHOUSE_ENV)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(path) if path is not None else Path(tmp)
        os.environ[DATA_FOUNDRY_WAREHOUSE_ENV] = str(root)
        try:
            yield root
        finally:
            if previous is None:
                os.environ.pop(DATA_FOUNDRY_WAREHOUSE_ENV, None)
            else:
                os.environ[DATA_FOUNDRY_WAREHOUSE_ENV] = previous


def main(warehouse: Path | None = None) -> dict[str, Any]:
    """Check the family: the parent's data checksum, and each task's container checksum and parent."""
    with _warehouse(warehouse) as root:
        files = write_raw_files(root / "exam_scores")
        print(f"Wrote {len(files)} school files to {root / 'exam_scores'}\n")

        print("-- The family --")
        for name, cls in discover_definitions(FAMILY).items():
            parent = parent_definition(cls)
            kind = cls.task_metadata.split_regime if is_task(cls) else "parent"
            print(f"  {name:22s} {kind:16s} {'<- ' + parent.unique_name if parent else ''}")

        print("\n-- The parent: data, never built --")
        parent = get_dataset(FAMILY, "exam_scores")
        checked = parent.check(write_report=False, verbose=False)
        print(f"  {len(checked.frame)} rows, columns {list(checked.frame.columns)}")
        print(f"  data checksum {checked.data_checksum}; children {checked.children}")
        out: dict[str, Any] = {"exam_scores": checked.data_checksum}

        print("\n-- The tasks: one container each --")
        for name in checked.children:
            result = get_dataset(FAMILY, name).check(write_report=False, verbose=False)
            container = result.container
            meta, task = container.dataset_metadata, container.task_metadata
            print(f"  {name}: target `{task.target_column_name}`, {task.split_regime}, {len(container.dataset)} rows")
            print(f"    columns {list(container.dataset.columns)}")
            print(f"    derived from `{meta.derived_from}`: {' '.join(meta.derivation.split())}")
            print(f"    bundle checks: {len(result.bundle_report.errors)} error(s), checksum {container.checksum}")
            out[name] = container.checksum

        print("\n-- Trying a task before writing its folder (a class written here, as in a notebook) --")
        exam_scores = load_definition(FAMILY / "exam_scores")

        class TryMathIid(exam_scores):
            unique_name = "exam_scores_math_iid"
            derivation = "The math score of random students of the known schools (IID)."
            task_summary = TaskSummary(
                question="What math score will this student reach?",
                use_case="A teacher plans extra lessons for their own students.",
                row="One student.",
                predicted="The math score.",
                known="The student's school, study time, attendance, parents' education and last year's grade.",
                split="Random students of the same schools.",
                fit="approximate",
                fit_reason="Generated data.",
            )
            target = "math_score"
            problem_type = "regression"
            metric = Metric.fallback(reason="Generated example data: there is no source metric.")

            def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
                return super()._clean(raw).drop(columns=["reading_score"])

        trial = TryMathIid()
        splits = trial.preview_splits()
        print(f"  {trial.unique_name}: folder {trial.folder}, so `check` writes no README and `build` refuses it")
        print(
            f"  its splits: {splits['repeat'].nunique()} repeats x {splits['fold'].nunique()} folds, "
            f"{splits['n_train'].iloc[0]} train / {splits['n_test'].iloc[0]} test students, where the grouped math "
            "task holds out whole schools"
        )
        return out


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
