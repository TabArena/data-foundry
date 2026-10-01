"""Check that a migrated v2 definition curates the same data as the v1 notebook it came from.

Usage::

    python scripts/v2/check_equivalence.py <notebook.ipynb> <dataset folder with dataset.py>

The notebook's code cells run in order (from the notebook's folder, plots disabled) up to the bundle,
skipping the bundle checks and the export, so nothing is saved. The v2 definition builds its container
with ``to_container()``. The v2 standard steps may change the row order (one shuffle seed, a stable time
sort), the categories (unused ones removed), the whitespace of metadata text and the split comment, so
the gate compares content:

* the same columns in the same order, with the same dtypes (unused categories removed are reported);
* the same rows as a multiset (row hashes);
* the same number of repeats and folds with the same train/test sizes, and, for temporal tasks, the same
  rows in every fold;
* the metadata after normalising text (dedent/strip) and the known v2 defaults.

It prints ``SAME CHECKSUM`` (identical containers), ``SAME CONTENT`` (the above holds) or ``DIFFERENT``
with the differences. Exit code 0 for the first two.
"""

from __future__ import annotations

import argparse
import gc
import inspect
import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.bundle_checks import canonical_metric_name
from data_foundry.schema import DATA_FOUNDRY_WAREHOUSE_ENV, resolve_warehouse_dir
from data_foundry.v2 import load_definition
from pydantic import TypeAdapter

SKIP_MARKERS = ("run_bundle_checks(", ".save(", "verify_saved_container(")
TEXT_FIELDS = ("download_description", "academic_reference_bibtex", "curation_comments", "version_comment")


def _fingerprint(container) -> dict:
    df = container.dataset
    meta = {}
    for name in ("dataset_metadata", "task_metadata", "experiment_metadata"):
        obj = getattr(container, name)
        meta[name] = TypeAdapter(type(obj)).dump_python(obj, mode="json")
    # The grouping block exists in v2 definitions only; its flat fields (group_on, ...) are compared.
    meta["task_metadata"].pop("grouping", None)
    splits = container.experiment_metadata.splits
    meta["experiment_metadata"].pop("splits")
    hashes = pd.util.hash_pandas_object(df, index=False).to_numpy()
    folds = {f"{r}/{f}": tt for r, fo in splits.items() for f, tt in fo.items()}
    return {
        "checksum": container.checksum,
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "categories": {c: set(df[c].cat.categories) for c in df.columns if str(df[c].dtype) == "category"},
        "rows": np.sort(hashes).tobytes(),
        "fold_sizes": {k: (len(tr), len(te)) for k, (tr, te) in folds.items()},
        "fold_rows": {
            k: (np.sort(hashes[tr]).tobytes(), np.sort(hashes[te]).tobytes()) for k, (tr, te) in folds.items()
        },
        "meta": meta,
    }


def _v1_warehouse(tmp: Path) -> Path:
    """A warehouse view for v1 notebooks: links to every entry, plus ``<name>_1m`` -> ``<name>``.

    A v1 ``_1m`` notebook reads its raw files from ``<warehouse>/<name>_1m/``; v2 reads them from the
    dataset it was made from.
    """
    real = resolve_warehouse_dir()
    for entry in real.iterdir():
        (tmp / entry.name).symlink_to(entry)
    for entry in real.iterdir():
        if entry.is_dir() and not (tmp / f"{entry.name}_1m").exists():
            (tmp / f"{entry.name}_1m").symlink_to(entry)
    return tmp


def run_notebook(nb_path: Path) -> dict:
    """Execute the notebook's definitional cells and fingerprint its ``curated_data``."""
    os.environ.setdefault("MPLBACKEND", "Agg")
    with tempfile.TemporaryDirectory() as tmp:
        previous = os.environ.get(DATA_FOUNDRY_WAREHOUSE_ENV)
        os.environ[DATA_FOUNDRY_WAREHOUSE_ENV] = str(_v1_warehouse(Path(tmp)))
        try:
            return _run_notebook(nb_path)
        finally:
            if previous is None:
                os.environ.pop(DATA_FOUNDRY_WAREHOUSE_ENV)
            else:
                os.environ[DATA_FOUNDRY_WAREHOUSE_ENV] = previous


def _run_notebook(nb_path: Path) -> dict:
    nb = json.loads(nb_path.read_text())
    namespace: dict = {"__name__": "__notebook__"}
    cwd = Path.cwd()
    os.chdir(nb_path.parent)
    try:
        import matplotlib.pyplot as plt  # noqa: PLC0415 - only needed when the notebook plots

        plt.show = lambda *_args, **_kwargs: None
    except ImportError:
        pass
    try:
        for cell in nb["cells"]:
            if cell["cell_type"] != "code":
                continue
            src = "".join(cell["source"])
            if any(marker in src for marker in SKIP_MARKERS):
                continue
            src = "\n".join(line for line in src.split("\n") if not line.lstrip().startswith(("%", "!")))
            exec(compile(src, str(nb_path), "exec"), namespace)  # noqa: S102 - running our own notebooks
    finally:
        os.chdir(cwd)
    return _fingerprint(namespace["curated_data"])


def _normalise_meta(meta: dict) -> dict:
    meta = json.loads(json.dumps(meta))
    ds = meta["dataset_metadata"]
    for key in TEXT_FIELDS:
        if isinstance(ds.get(key), str):
            ds[key] = "\n".join(line.rstrip() for line in inspect.cleandoc(ds[key]).split("\n"))
    ds["academic_reference_bibtex_key"] = ",".join(k.strip() for k in ds["academic_reference_bibtex_key"].split(","))
    ds["data_tags"] = sorted(ds["data_tags"])
    task = meta["task_metadata"]
    task["objective_metric_name"] = canonical_metric_name(task["objective_metric_name"])
    split = meta["experiment_metadata"]
    split.pop("splits_comment", None)
    split.pop("split_random_state", None)
    if split.get("time_horizon") is not None:
        split["time_horizon"] = int(split["time_horizon"])
    return meta


def _diff(a: dict, b: dict, path: str = "") -> list[str]:
    out = []
    for key in sorted(set(a) | set(b)):
        va, vb = a.get(key, "<missing>"), b.get(key, "<missing>")
        if isinstance(va, dict) and isinstance(vb, dict):
            out += _diff(va, vb, f"{path}{key}.")
        elif va != vb:
            out.append(f"  {path}{key}: notebook={repr(va)[:160]} v2={repr(vb)[:160]}")
    return out


def compare(old: dict, new: dict, *, temporal: bool) -> tuple[list[str], list[str]]:
    """(differences, notes) between two fingerprints."""
    diffs, notes = [], []
    if old["columns"] != new["columns"]:
        diffs.append(f"  columns: notebook={old['columns']} v2={new['columns']}")
    for col, dtype in old["dtypes"].items():
        if col in new["dtypes"] and dtype != new["dtypes"][col]:
            diffs.append(f"  dtype {col}: notebook={dtype} v2={new['dtypes'][col]}")
    for col, cats in old["categories"].items():
        extra = cats - new["categories"].get(col, cats)
        if extra:
            notes.append(f"  note: {col}: {len(extra)} unused categories removed")
    if old["rows"] != new["rows"]:
        diffs.append("  rows: the frames hold different rows (compared as multisets)")
    if old["fold_sizes"] != new["fold_sizes"]:
        diffs.append(f"  fold sizes: notebook={old['fold_sizes']} v2={new['fold_sizes']}")
    elif old["fold_rows"] != new["fold_rows"]:
        if temporal:
            diffs.append("  temporal folds: same sizes, different rows")
        else:
            notes.append("  note: the row order changed, so the seeded split drew other rows (same sizes)")
    diffs += _diff(_normalise_meta(old["meta"]), _normalise_meta(new["meta"]))
    return diffs, notes


def main(argv: list[str] | None = None) -> int:
    """Compare one notebook with its v2 definition; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("notebook", type=Path)
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args(argv)

    ds = load_definition(args.dataset.resolve())()
    temporal = ds.task_metadata.time_on is not None
    new = _fingerprint(ds.to_container())
    del ds
    gc.collect()
    old = run_notebook(args.notebook.resolve())

    name = args.dataset.name
    if old["checksum"] == new["checksum"]:
        print(f"SAME CHECKSUM {name}: {new['checksum']}")
        return 0
    diffs, notes = compare(old, new, temporal=temporal)
    print(f"{'DIFFERENT' if diffs else 'SAME CONTENT'} {name}")
    print(*diffs, *notes, sep="\n")
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
