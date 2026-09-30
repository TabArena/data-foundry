"""The generated ``report.md`` of a dataset: machine-readable evidence plus the same as readable tables.

The YAML frontmatter is the machine-readable part: the build record (UUID, checksum, provenance), the
data and split shape, and the bundle-check outcome. GitHub renders it as a table at the top of the file.
The markdown body repeats it for humans and adds the check messages and the exploratory data-check
tables. :meth:`~data_foundry.v2.dataset.AbstractCuratedDataset.check` rewrites the report without a
timestamp, so an unchanged dataset gives an unchanged file; only
:meth:`~data_foundry.v2.dataset.AbstractCuratedDataset.build` writes a new build record.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pandas as pd
import yaml

from data_foundry.schema import resolve_warehouse_dir
from data_foundry.v2.dataset import provenance, split_summary

if TYPE_CHECKING:
    from data_foundry.v2.dataset import CurationResult

REPORT_FORMAT = "data-foundry-report-v1"
"""Identifies the frontmatter layout, for readers that parse it."""

MAX_TABLE_ROWS = 60
"""Rows shown per table in the body; the rest is summarised in one line."""

MAX_CELL_CHARS = 80
"""Characters shown per table cell in the body."""


def read_report(path: Path | str) -> dict[str, Any]:
    """Return the frontmatter of a ``report.md`` (an empty dict for a missing file or no frontmatter)."""
    path = Path(path)
    if not path.is_file():
        return {}
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    return yaml.safe_load(text[4:end]) or {}


def report_frontmatter(result: CurationResult, *, previous: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build the machine-readable frontmatter for ``result``.

    ``previous`` is the frontmatter of the report being replaced; a check keeps its build record and
    flags it stale when the checksum changed.
    """
    container = result.container
    ds = result.dataset
    task = container.task_metadata
    splits_meta = container.experiment_metadata
    df = container.dataset
    report = result.bundle_report

    if result.saved:
        build = {
            "uuid": container.uuid,
            "checksum": container.checksum,
            "built_at": result.created_at.replace(microsecond=0).isoformat(),
            "path": result.saved_path.relative_to(resolve_warehouse_dir()).as_posix(),
            **provenance(ds.folder),
        }
    else:
        build = (previous or {}).get("build")

    sizes = split_summary(df, splits_meta.splits)
    frontmatter: dict[str, Any] = {
        "report_format": REPORT_FORMAT,
        "unique_name": container.dataset_metadata.unique_name,
        "checksum": container.checksum,
        "build": build,
        "build_stale": bool(build) and build.get("checksum") != container.checksum,
        "data": {
            "n_rows": len(df),
            "n_features": int(df.shape[1] - 1),
            "dtypes": {str(k): int(v) for k, v in df.dtypes.astype(str).value_counts().sort_index().items()},
            "n_test_dataset_rows": None if container.test_dataset is None else len(container.test_dataset),
        },
        "feature_types": _feature_types(ds, df),
        "task": {
            "target": task.target_column_name,
            "problem_type": task.problem_type,
            "metric": task.objective_metric_name,
            "split_regime": task.split_regime,
            "stratify_on": task.stratify_on,
            "time_on": task.time_on,
            "group_on": task.group_on,
            "group_labels": task.group_labels,
        },
        "splits": {
            "n_repeats": len(splits_meta.splits),
            "n_folds": len(next(iter(splits_meta.splits.values()))),
            "random_state": splits_meta.split_random_state,
            "time_horizon": splits_meta.time_horizon,
            "time_horizon_unit": splits_meta.time_horizon_unit,
            "n_train": {"min": int(sizes["n_train"].min()), "max": int(sizes["n_train"].max())},
            "n_test": {"min": int(sizes["n_test"].min()), "max": int(sizes["n_test"].max())},
        },
        "bundle_checks": {
            "ok": report.ok,
            "errors": [r.slug for r in report.errors],
            "warnings": [r.slug for r in report.warnings],
            "infos": [r.slug for r in report.infos],
            "accepted": dict(ds.accepted_check_warnings),
        },
        "decisions": [d.title for d in result.decisions],
    }
    return frontmatter


def _feature_types(ds: Any, df: pd.DataFrame) -> dict[str, Any]:
    types = ds.feature_types(df)
    return {
        "categorical": list(types.categorical),
        "string": list(types.string),
        "datetime": dict(types.datetime_formats),
    }


def render_report(  # noqa: C901, PLR0912 - one branch per report section
    result: CurationResult,
    *,
    previous: dict[str, Any] | None = None,
    figures: dict[int, str] | None = None,
) -> str:
    """Render the full ``report.md`` text for ``result`` (``figures``: decision index -> relative PNG path)."""
    figures = figures or {}
    fm = report_frontmatter(result, previous=previous)
    container = result.container
    meta = container.dataset_metadata
    df = container.dataset
    report = result.bundle_report
    ds = result.dataset

    out: list[str] = ["---", yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).rstrip(), "---", ""]
    out += [
        f"# {meta.unique_name}",
        "",
        "> Generated by `data-foundry-curation dataset check` / `build` from `dataset.py`. Do not edit by hand.",
        "",
        "## Build",
        "",
    ]
    build = fm["build"]
    if build:
        rows = [(k, v) for k, v in build.items()]
        if fm["build_stale"]:
            rows.append(("stale", f"yes: the definition now gives checksum `{fm['checksum']}`"))
        out += [_table(pd.DataFrame(rows, columns=["field", "value"])), ""]
    else:
        out += [f"Not built yet. Current checksum: `{fm['checksum']}`.", ""]

    out += ["## Dataset", ""]
    out += [
        _table(
            pd.DataFrame(
                [
                    ("source", f"{meta.dataset_source}: {meta.original_dataset_source_download_link}"),
                    ("year", meta.dataset_year),
                    ("domain", meta.domain_str),
                    ("license", meta.license),
                    ("data_tags", ", ".join(meta.data_tags)),
                    ("reference", meta.academic_reference_bibtex_key),
                    ("version_from_unique_name", meta.version_from_unique_name),
                    ("rows x columns", f"{df.shape[0]:,} x {df.shape[1]:,}"),
                    *[(f"task.{k}", v) for k, v in fm["task"].items() if v is not None],
                ],
                columns=["field", "value"],
            ),
        ),
        "",
    ]

    splits_meta = container.experiment_metadata
    out += ["## Splits", "", splits_meta.splits_comment.strip(), ""]
    out += [_table(split_summary(df, splits_meta.splits, time_on=container.task_metadata.time_on)), ""]

    if result.decisions:
        out += ["## Decisions", ""]
        for i, decision in enumerate(result.decisions):
            out += [f"### {i + 1}. {decision.title}", "", decision.why.strip(), ""]
            evidence = decision.evidence
            if i in figures:
                out += [f"![{decision.title}]({figures[i]})", ""]
            elif isinstance(evidence, pd.Series):
                out += [_table(evidence.to_frame(), index=True), ""]
            elif isinstance(evidence, pd.DataFrame):
                out += [_table(evidence, index=not isinstance(evidence.index, pd.RangeIndex)), ""]
            elif isinstance(evidence, str) and evidence.strip():
                out += [evidence.strip(), ""]

    out += [
        "## Bundle checks",
        "",
        f"{len(report.errors)} error(s), {len(report.warnings)} warning(s), {len(report.infos)} info "
        f"({report.n_checks_run} checks run, plus the dataset's own checks).",
        "",
    ]
    for result_ in report.results:
        line = f"- **{result_.severity}** `{result_.slug}`: {_one_line(result_.message)}"
        if result_.hint:
            line += f" (hint: {_one_line(result_.hint)})"
        out.append(line)
    if ds.accepted_check_warnings:
        out += ["", "Accepted on purpose:", ""]
        out += [f"- `{slug}`: {_one_line(reason)}" for slug, reason in ds.accepted_check_warnings.items()]
    out.append("")

    out += ["## Data checks", ""]
    titles = {
        "summary": "Feature summary",
        "target": "Target distribution",
        "numeric_stats": "Numeric features",
        "cat_stats": "Categorical features",
    }
    for key, title in titles.items():
        table = result.data_checks.get(key)
        if table is None or len(table) == 0:
            continue
        out += [f"### {title}", "", _table(table, index=key != "summary"), ""]
    return "\n".join(out).rstrip() + "\n"


FIGURE_DIR = "report"
"""Folder next to ``report.md`` that holds the decision figures."""


def write_report(result: CurationResult, path: Path | str) -> Path:
    """Render ``result`` and write it to ``path``, keeping the build record of the report it replaces.

    Decision figures are saved as PNGs under ``report/`` next to it; PNGs of decisions that no longer exist
    are removed.
    """
    path = Path(path)
    figure_dir = path.parent / FIGURE_DIR
    figures: dict[int, str] = {}
    for i, decision in enumerate(result.decisions):
        if hasattr(decision.evidence, "savefig"):
            name = f"decision_{i + 1}_{_slug(decision.title)}.png"
            figure_dir.mkdir(exist_ok=True)
            decision.evidence.savefig(figure_dir / name, dpi=100, bbox_inches="tight", metadata={"Software": None})
            figures[i] = f"{FIGURE_DIR}/{name}"
            _close(decision.evidence)
    if figure_dir.is_dir():
        keep = {Path(f).name for f in figures.values()}
        for png in figure_dir.glob("decision_*.png"):
            if png.name not in keep:
                png.unlink()
    text = render_report(result, previous=read_report(path), figures=figures)
    path.write_text(text)
    return path


def _close(figure: Any) -> None:
    try:
        import matplotlib.pyplot as plt  # noqa: PLC0415 - only when a decision has a figure
    except ImportError:
        return
    plt.close(figure)


def _slug(text: str) -> str:
    return "_".join("".join(c.lower() if c.isalnum() else " " for c in text).split())[:40]


def _one_line(text: str) -> str:
    return " ".join(str(text).split())


def _cell(value: Any) -> str:
    if isinstance(value, float):
        text = f"{value:.6g}"
    elif isinstance(value, (dt.datetime, pd.Timestamp)):
        text = str(value)
    elif value is None or (not isinstance(value, (list, tuple, dict)) and pd.isna(value)):
        text = ""
    else:
        text = str(value)
    text = _one_line(text).replace("|", "\\|")
    return text if len(text) <= MAX_CELL_CHARS else text[: MAX_CELL_CHARS - 1] + "…"


def _table(df: pd.DataFrame, *, index: bool = False) -> str:
    """Render ``df`` as a GitHub markdown table, truncated to :data:`MAX_TABLE_ROWS` rows."""
    if index:
        df = df.reset_index()
    shown = df.head(MAX_TABLE_ROWS)
    header = [_cell(c) for c in shown.columns]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    lines += ["| " + " | ".join(_cell(v) for v in row) + " |" for row in shown.itertuples(index=False)]
    if len(df) > len(shown):
        lines.append(f"\n({len(df) - len(shown):,} more rows not shown)")
    return "\n".join(lines)
