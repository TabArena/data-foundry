"""Clean room: the input folder of a blind reviewer, who judges a dataset without our curation notes.

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/clean_room.py <unique_name> --out DIR [--max-rows 200000]
        [--root datasets/_dev/tabarena-v0pt2] [--records curation/records] [--built]
    python .claude/skills/knowledge-data-foundry/scripts/clean_room.py <unique_name> --out DIR/participant_kit
        --participant --prediction-point "the policy is quoted" [--root ...] [--records ...]

Loads the v2 definition of ``<unique_name>`` through ``dataset_io.py`` (its curated frame and split plan, rebuilt from
the raw files; ``--built`` reads the container of the README's build record instead) and the curation record for its
source links, and writes two files:

* ``DIR/data.parquet``: the curated frame with the target, without the scoring columns (metric inputs, never
  features; ``dataset_io.py`` drops them). A frame with more than ``--max-rows`` rows is a random
  sample of that many rows (seed 0, original order kept), and ``task.md`` says so.
* ``DIR/task.md``: the target column, the problem type, rows x columns, the regime (IID, grouped with the group
  column, temporal with the time column), the number of folds or test windows, and the source links.

Nothing else goes into the folder: no ``task_summary``, ``curation_comments``, record comments, README text or link
notes (the ``#`` lines of ``source_links``), so the reviewer's judgement is their own. The folder name ``<unique_name>``
is not in ``task.md`` either; the links name the source.

``--participant`` writes the participant kit of the ``task-gamer`` agent instead, everything a benchmark participant
gets and nothing more: ``data.parquet`` with every row, ``splits.parquet`` (the shipped splits as ``repeat``, ``fold``,
``side``, ``row``: positions into ``data.parquet``), ``scoring.parquet`` (the scoring columns, when the metric has
inputs), ``task.json`` and ``task.md`` (the facts above plus the metric and the prediction point, one neutral sentence
the main session writes), a copy of ``src/data_foundry/v2/metrics.py`` and ``score.py``, which scores a prediction by
the shipped metric as the benchmark does, and an empty ``work/`` for the agent's scripts. The kit's folder name must
contain ``participant_kit``: the ``task_gamer_hook.py`` sandbox lets the agent touch nothing else.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import shutil
import sys
from pathlib import Path

import dataset_io
import pandas as pd
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.store import load_record

SEED = 0
REGIMES = {"iid": "IID", "grouped_non_iid": "grouped", "temporal_non_iid": "temporal"}
METRICS_PY = Path(__file__).resolve().parents[4] / "src" / "data_foundry" / "v2" / "metrics.py"
# The spec fields a participant needs; ``origin``, ``original`` and ``reason`` are our curation notes.
PARTICIPANT_METRIC_KEYS = (
    "name",
    "kind",
    "prediction",
    "greater_is_better",
    "params",
    "inputs",
    "definition",
    "reference",
    "target_transform",
)
GROUPING_KEYS = ("on", "labels", "time_on", "prediction_unit", "aggregation", "context")
SCORE_PY = '''"""Score a prediction on this task as the benchmark does.

    from score import TARGET, features, load, score, splits

    df = load()
    for name, train_idx, test_idx in splits():
        X, y = df[features()], df[TARGET]
        ...fit on X.iloc[train_idx], y.iloc[train_idx]; predict X.iloc[test_idx]...
        print(name, score(y.iloc[test_idx], y_pred, test_idx))

``python score.py`` scores a random prediction on every split: it shows the metric computes, it is not a baseline.
The kind of prediction the metric takes (``proba``, ``label`` or ``value``) is ``task.json``'s ``metric.prediction``;
``metrics.py`` implements it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import metrics  # noqa: E402

TASK = json.loads((HERE / "task.json").read_text())
TARGET = TASK["target"]
_SCORER = []


def load() -> pd.DataFrame:
    """The rows: the features, the target and the group column, if any."""
    return pd.read_parquet(HERE / "data.parquet")


def features() -> list[str]:
    """The model inputs: every column but the target and the group column(s)."""
    drop = {TARGET, *TASK["group_columns"]}
    return [c for c in load().columns if c not in drop]


def splits() -> list[tuple[str, list[int], list[int]]]:
    """Every shipped split as (name, train positions, test positions), positions into ``load()``."""
    s = pd.read_parquet(HERE / "splits.parquet")
    out = []
    for (repeat, fold), part in s.groupby(["repeat", "fold"], sort=True):
        train = part.loc[part["side"] == "train", "row"].tolist()
        test = part.loc[part["side"] == "test", "row"].tolist()
        out.append((f"r{repeat}f{fold}", train, test))
    return out


def score(y_true, y_pred, test_idx) -> float:
    """The metric on the test rows ``test_idx`` (positions into ``load()``)."""
    if not _SCORER:
        frame = load()
        if (HERE / "scoring.parquet").exists():
            frame = frame.join(pd.read_parquet(HERE / "scoring.parquet"))
        grouping = SimpleNamespace(**TASK["grouping"]) if TASK["grouping"] else None
        task = SimpleNamespace(target_column_name=TARGET, objective_metric=TASK["metric"], grouping=grouping)
        _SCORER.append(metrics.scorer(SimpleNamespace(dataset=frame, task_metadata=task)))
    return _SCORER[0](y_true, y_pred, test_idx)


if __name__ == "__main__":
    df = load()
    y = df[TARGET]
    labels = list(y.cat.categories) if isinstance(y.dtype, pd.CategoricalDtype) else None
    for name, train_idx, test_idx in splits():
        pred = metrics.dummy_prediction(TASK["metric"]["prediction"], y.iloc[train_idx], len(test_idx), labels=labels)
        value = score(y.iloc[test_idx], pred, test_idx)
        print(f"{name}: train {len(train_idx):,}, test {len(test_idx):,}, random prediction {value:.5f}")
'''


def source_links(name: str, records: Path, folder_class: type | None = None) -> list[str]:
    """The record's source links without the note lines (``#``); the record of a ``version_of`` folder if needed."""
    path = records / f"{name}.md"
    if not path.exists() and folder_class is not None and getattr(folder_class, "version_of", None):
        path = records / f"{folder_class.version_of}.md"
    if not path.exists():
        return []
    return [link for link in load_record(path).source_links if not link.lstrip().startswith("#")]


def _folder(name: str, root: Path, records: Path) -> tuple[str, Path]:
    """The definition folder of ``name``: ``root/name``, else the folder the record's ``v2_path`` names."""
    if (root / name / "dataset.py").exists():
        return name, root
    path = records / f"{name}.md"
    if path.exists() and (v2_path := load_record(path).v2_path):
        folder = resolve_curation_root().parent / Path(v2_path).parent  # v2_path is relative to the repo
        return folder.name, folder.parent
    raise SystemExit(f"no definition for {name!r}: neither {root / name / 'dataset.py'} nor a v2_path in {path}")


def regime_line(data: dataset_io.ProbeInput) -> str:
    """The regime in one line, with its group or time column."""
    regime = REGIMES.get(data.regime, data.regime)
    groups = ", ".join(f"`{c}`" for c in data.group_cols)
    if regime == "grouped":
        return f"grouped by {groups} (whole groups are held out)"
    if regime == "temporal":
        line = f"temporal on `{data.time_on}` (each test window comes after its training rows)"
        return line + (f"; rows grouped by {groups}" if groups else "")
    return f"{regime} (random rows)"


def splits_line(data: dataset_io.ProbeInput) -> str:
    """The number of folds (IID, grouped) or test windows (temporal)."""
    repeats = data.repeats()
    total = sum(len(r) for r in repeats)
    if REGIMES.get(data.regime) == "temporal":
        return f"{total} test windows"
    folds = {len(r) for r in repeats}
    per = folds.pop() if len(folds) == 1 else f"{min(len(r) for r in repeats)}-{max(len(r) for r in repeats)}"
    return f"{len(repeats)} repeats x {per} folds ({total} train/test splits)"


def task_markdown(data: dataset_io.ProbeInput, links: list[str], *, rows: int, sampled: int | None) -> str:
    """The task.md of the clean room: only the facts the reviewer needs to start."""
    columns = data.df.shape[1]
    lines = [
        "# Task",
        "",
        f"- Target column: `{data.target}`",
        f"- Problem type: {data.problem_type.replace('_', ' ')}",
        f"- Size: {rows:,} rows x {columns} columns (target included)",
        f"- Regime: {regime_line(data)}",
        f"- Splits: {splits_line(data)}",
    ]
    if sampled is not None:
        lines.append(
            f"- `data.parquet` is a random sample of {sampled:,} of the {rows:,} rows (seed {SEED}, original order "
            "kept); the size above is the full data."
        )
    else:
        lines.append("- `data.parquet` holds every row.")
    lines += ["", "## Source links", ""]
    lines += [f"- {link}" for link in links] or ["- (none recorded)"]
    return "\n".join(lines) + "\n"


def write(name: str, out: Path, *, root: Path, records: Path, max_rows: int, built: bool) -> dict:
    """Write ``data.parquet`` and ``task.md`` for ``name`` into ``out``; return what was written."""
    folder, folder_root = _folder(name, root, records)
    ds = dataset_io.definition(folder, folder_root)
    # the blind reviewer sees a special feature (a SMILES, a spectrum) as shipped, not in our encoding
    data = (
        dataset_io.load(folder, folder_root, built=True, encode_special=False)
        if built
        else dataset_io.from_definition(ds, encode_special=False)
    )
    links = source_links(name, records, type(ds))
    df = data.df
    rows = len(df)
    sampled = None
    if rows > max_rows:
        df = df.sample(n=max_rows, random_state=SEED).sort_index()
        sampled = max_rows
    out.mkdir(parents=True, exist_ok=True)
    df.reset_index(drop=True).to_parquet(out / "data.parquet")
    (out / "task.md").write_text(task_markdown(data, links, rows=rows, sampled=sampled))
    return {"name": name, "folder": folder, "rows": rows, "columns": df.shape[1], "sampled": sampled, "out": str(out)}


def participant_task(ds, data: dataset_io.ProbeInput, scoring: list[str]) -> dict:
    """The ``task.json`` of the participant kit: the task as a benchmark harness reads it, without our notes."""
    task = ds.task_metadata
    spec = task.objective_metric
    spec = dataclasses.asdict(spec) if dataclasses.is_dataclass(spec) else dict(spec)
    grouping = None
    if data.grouping is not None:
        grouping = {key: getattr(data.grouping, key, None) for key in GROUPING_KEYS}
    return {
        "target": data.target,
        "problem_type": data.problem_type,
        "regime": data.regime,
        "time_column": data.time_on,
        "group_columns": data.group_cols,
        "grouping": grouping,
        "scoring_columns": scoring,
        "special_features": list(data.special_features),
        "metric": {key: spec.get(key) for key in PARTICIPANT_METRIC_KEYS},
    }


def prediction_point_line(prediction_point: str) -> str:
    """The kit's prediction-point line from a clause ("the policy is quoted") or a whole sentence ("The prediction
    is made for an hour after ..."), which is kept as written instead of getting a second "the prediction is made".
    """
    text = prediction_point.strip().rstrip(".")
    if text.lower().startswith("the prediction is "):
        return f"- Prediction point: {text[0].lower()}{text[1:]}."
    return f"- Prediction point: the prediction is made when {text}."


def participant_markdown(data: dataset_io.ProbeInput, links: list[str], task: dict, prediction_point: str) -> str:
    """The ``task.md`` of the participant kit: the clean room's facts, the prediction point, the metric, the files."""
    metric = task["metric"]
    params = f", params {json.dumps(metric['params'])}" if metric["params"] else ""
    direction = "higher" if metric["greater_is_better"] else "lower"
    lines = task_markdown(data, links, rows=len(data.df), sampled=None).rstrip("\n").split("\n")
    at = lines.index("## Source links")
    extra = [
        prediction_point_line(prediction_point),
        f"- Metric: `{metric['name']}` on a `{metric['prediction']}` prediction{params}; {direction} is better.",
    ]
    if task["grouping"]:
        g = task["grouping"]
        extra.append(
            f"- Groups: one prediction per {g['prediction_unit']}"
            + (f" (aggregated by `{g['aggregation']}`)" if g["aggregation"] else "")
            + f"; what a model may use about the group: `{g['context']}`. The group column is not a feature."
        )
    if task.get("special_features"):
        names = ", ".join(task["special_features"])
        extra.append(f"- Special features (one input over several columns, or a SMILES string, as shipped): {names}.")
    if task["scoring_columns"]:
        extra.append(f"- Scoring columns (metric inputs, never features): {', '.join(task['scoring_columns'])}.")
    files = [
        "## Files",
        "",
        "- `data.parquet`: the rows; `splits.parquet`: the shipped splits (`repeat`, `fold`, `side`, `row`, positions "
        "into `data.parquet`).",
        "- `score.py`: `load()`, `features()`, `splits()` and `score(y_true, y_pred, test_idx)`, the metric as the "
        "benchmark computes it (`metrics.py`). `task.json`: these facts as data.",
        "- `work/`: your scripts and outputs.",
        "",
    ]
    return "\n".join(lines[: at - 1] + extra + [""] + files + lines[at:]) + "\n"


def write_participant(name: str, out: Path, *, root: Path, records: Path, prediction_point: str) -> dict:
    """Write the participant kit for ``name`` into ``out`` (see the module docstring); return what was written."""
    if "participant_kit" not in out.resolve().as_posix():
        raise SystemExit(f"the kit's path must contain 'participant_kit' (the agent's sandbox allows only it): {out}")
    folder, folder_root = _folder(name, root, records)
    ds = dataset_io.definition(folder, folder_root)
    plan = ds.make_splits()
    data = dataset_io.from_definition(ds, plan, encode_special=False)  # as shipped, like the clean room
    scoring = list(data.scoring_cols)
    task = participant_task(ds, data, scoring)
    out.mkdir(parents=True, exist_ok=True)
    (out / "work").mkdir(exist_ok=True)
    data.df.reset_index(drop=True).to_parquet(out / "data.parquet")
    if scoring:
        plan.df[scoring].reset_index(drop=True).to_parquet(out / "scoring.parquet")
    rows = [
        (repeat, fold, side, int(i))
        for repeat, folds in data.splits.items()
        for fold, (train, test) in folds.items()
        for side, idx in (("train", train), ("test", test))
        for i in idx
    ]
    pd.DataFrame(rows, columns=["repeat", "fold", "side", "row"]).to_parquet(out / "splits.parquet")
    (out / "task.json").write_text(json.dumps(task, indent=2, default=str) + "\n")
    links = source_links(name, records, type(ds))
    (out / "task.md").write_text(participant_markdown(data, links, task, prediction_point))
    shutil.copyfile(METRICS_PY, out / "metrics.py")
    (out / "score.py").write_text(SCORE_PY)
    return {"name": name, "folder": folder, "rows": len(data.df), "columns": data.df.shape[1], "out": str(out)}


def main(argv: list[str] | None = None) -> int:
    """Write the clean room; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name", help="The record's unique_name.")
    parser.add_argument("--out", type=Path, required=True, help="The folder to write data.parquet and task.md to.")
    parser.add_argument("--max-rows", type=int, default=200_000, help="Sample larger frames down to this many rows.")
    parser.add_argument("--root", type=Path, default=None, help="Default: datasets/_dev/tabarena-v0pt2.")
    parser.add_argument("--records", type=Path, default=None, help="Records folder (default: curation/records).")
    parser.add_argument("--built", action="store_true", help="Read the built container (README build record).")
    parser.add_argument("--participant", action="store_true", help="Write the task-gamer's participant kit.")
    parser.add_argument("--prediction-point", help="With --participant: 'the prediction is made when ...'.")
    args = parser.parse_args(argv)

    if args.participant:
        if not args.prediction_point:
            parser.error("--participant needs --prediction-point")
        result = write_participant(
            args.name,
            args.out,
            root=args.root or resolve_curation_root().parent / "datasets" / "_dev" / "tabarena-v0pt2",
            records=args.records or records_dir(),
            prediction_point=args.prediction_point,
        )
        size = f"{result['rows']:,} rows x {result['columns']} columns"
        print(f"{result['name']}: participant kit, {size} -> {result['out']}")
        return 0
    result = write(
        args.name,
        args.out,
        root=args.root or resolve_curation_root().parent / "datasets" / "_dev" / "tabarena-v0pt2",
        records=args.records or records_dir(),
        max_rows=args.max_rows,
        built=args.built,
    )
    sample = f", sampled to {result['sampled']:,}" if result["sampled"] else ""
    print(f"{result['name']}: {result['rows']:,} rows x {result['columns']} columns{sample} -> {result['out']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
