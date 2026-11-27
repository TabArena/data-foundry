"""Helpers several test modules share: toy metadata, metric specs, containers and v2 definitions.

The fixtures several modules use are in ``conftest.py``; a helper that one module uses stays in that module.
"""

from __future__ import annotations

import os
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

from data_foundry.checks.bundle import run_bundle_checks
from data_foundry.curation_container import CuratedContainer
from data_foundry.definition import AbstractCuratedDataset, load_definition
from data_foundry.schema import (
    MetricSpec,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadataV2,
    ScoringColumn,
    UnitWeight,
)
from data_foundry.v1 import DatasetMetadata, PredictiveMLTaskMetadata


# --- Format-1 dataset metadata ------------------------------------------------------------------------------------
def toy_dataset_metadata(**overrides) -> DatasetMetadata:
    """Format-1 dataset metadata with placeholder values; each keyword replaces one field."""
    kwargs = {
        "unique_name": "toy_ds",
        "dataset_year": "2025",
        "domain_str": "finance",
        "dataset_source": "Kaggle",
        "original_dataset_source_download_link": "http://example",
        "download_description": "desc",
        "academic_reference_bibtex": "bib",
        "academic_reference_bibtex_key": "key",
        "license": None,
        "data_tags": ["IID"],
        "curation_comments": None,
    }
    return DatasetMetadata(**(kwargs | overrides))


BIBTEX = """@misc{toy2025dataset,
  author = {Toy Author},
  title  = {A Toy Dataset},
  year   = {2025},
  howpublished = {\\url{https://example.com/toy}}
}
"""


def make_dataset_metadata(**overrides) -> DatasetMetadata:
    """The toy metadata with a parseable BibTeX, a license and curation comments, as the bundle checks read them."""
    kwargs = {
        "original_dataset_source_download_link": "https://example.com/toy",
        "download_description": "kaggle datasets download toy",
        "academic_reference_bibtex": BIBTEX,
        "academic_reference_bibtex_key": "toy2025dataset",
        "license": "CC BY 4.0",
        "curation_comments": "Read the CSV.",
    }
    return toy_dataset_metadata(**(kwargs | overrides))


# --- Metric specs -------------------------------------------------------------------------------------------------
def make_spec(problem_type: str = "binary_classification", metric=None) -> MetricSpec:
    """A format-2 metric spec: ``metric`` (a `Metric`), or a fallback with a reason, for ``problem_type``."""
    from data_foundry.definition.dataset import metric_spec
    from data_foundry.metrics import Metric

    return metric_spec(metric or Metric.fallback(reason="test data"), problem_type)


def source_spec(name: str = "roc_auc", **fields) -> MetricSpec:
    """A metric spec from the source: ``name``'s kind, prediction and direction from the registry, then ``fields``."""
    from data_foundry.metrics import METRICS

    definition = METRICS.get(name)
    base = {
        "name": name,
        "kind": definition.kind if definition else "custom",
        "prediction": definition.prediction if definition else "proba",
        "greater_is_better": definition.greater_is_better if definition else True,
        "origin": "source",
        "reference": "https://example.org/evaluation",
    }
    return MetricSpec(**(base | fields))


# --- Toy containers -------------------------------------------------------------------------------------------------
def make_iid_frame(n: int = 60) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    return pd.DataFrame(
        {
            "feat_num": rng.normal(size=n),
            "feat_cat": pd.Categorical(rng.choice(["a", "b", "c"], size=n)),
            "target": pd.Categorical(rng.choice(["yes", "no"], size=n)),
        },
    )


def make_iid_splits(n: int = 60, n_folds: int = 3) -> dict:
    folds = {}
    positions = np.arange(n)
    for fold in range(n_folds):
        test = positions[fold::n_folds]
        train = np.setdiff1d(positions, test)
        folds[fold] = (train.tolist(), test.tolist())
    return {0: folds}


def make_container(df: pd.DataFrame | None = None, **overrides) -> CuratedContainer:
    df = make_iid_frame() if df is None else df
    kwargs = {
        "dataset": df,
        "dataset_metadata": make_dataset_metadata(),
        "task_metadata": PredictiveMLTaskMetadata(
            target_column_name="target",
            problem_type="binary_classification",
            objective_metric_name="roc_auc",
            stratify_on="target",
        ),
        "experiment_metadata": PredictiveMLSplitsMetadata(
            splits_comment="Default splits.",
            splits=make_iid_splits(len(df)),
        ),
    }
    kwargs.update(overrides)
    return CuratedContainer(**kwargs)


def make_v2_container(
    df: pd.DataFrame | None = None, *, spec=None, scoring_columns=(), dataset_metadata=None, **task
) -> CuratedContainer:
    df = make_iid_frame() if df is None else df
    problem_type = task.pop("problem_type", "binary_classification")
    splits = task.pop("splits", None)
    return CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata or make_dataset_metadata(),
        task_metadata=PredictiveMLTaskMetadataV2(
            target_column_name="target",
            problem_type=problem_type,
            objective_metric=spec or make_spec(problem_type),
            scoring_columns=list(scoring_columns),
            **task,
        ),
        experiment_metadata=PredictiveMLSplitsMetadata(
            splits_comment="Toy split.", splits=make_iid_splits() if splits is None else splits
        ),
        uuid="u",
    )


def metric_findings(container: CuratedContainer) -> dict[str, str]:
    report = run_bundle_checks(container, verbose=False)
    return {r.slug: r.severity for r in report.results if r.slug.startswith(("task_metric", "task_scoring"))}


def unit_frame() -> pd.DataFrame:
    """60 rows in 30 plots of 1, 2 or 3 quadrats; ``plot_weight`` is 1 over the plot's quadrats."""
    sizes = np.tile([1, 2, 3], 10)
    df = make_iid_frame(60).assign(target=np.linspace(0.0, 3.0, 60), plot=np.repeat(np.arange(30), sizes))
    return df.assign(plot_weight=1.0 / df.groupby("plot")["plot"].transform("size"))


def plot_splits(df: pd.DataFrame) -> dict:
    """Three folds by plot, so every plot's rows lie on one side."""
    fold = df["plot"].to_numpy() % 3
    rows = np.arange(len(df))
    return {0: {f: (rows[fold != f].tolist(), rows[fold == f].tolist()) for f in range(3)}}


def unit_container(df=None, *, splits="plots", **task) -> CuratedContainer:
    df = unit_frame() if df is None else df
    weight = ScoringColumn(column="plot_weight", role="weight", used_by="rmse", description="1 / quadrats of the plot")
    task.setdefault("unit_weight", UnitWeight(column="plot_weight", unit="plot"))
    return make_v2_container(
        df,
        spec=source_spec("rmse", inputs={"weight": "plot_weight"}),
        scoring_columns=[weight],
        problem_type="regression",
        splits=plot_splits(df) if splits == "plots" else None,
        **task,
    )


def grouped_toy(task: PredictiveMLTaskMetadata | PredictiveMLTaskMetadataV2 | None = None) -> CuratedContainer:
    # `object`, as pandas 2 infers it: pandas 3 infers `str`, a different dtype in the pinned checksum
    g = pd.Series(["a", "a", "b", "b", "c", "c"], dtype=object)
    df = pd.DataFrame({"g": g, "x": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6], "y": [0, 0, 1, 1, 0, 0]})
    if task is None:
        task = PredictiveMLTaskMetadata(
            target_column_name="y",
            problem_type="binary_classification",
            objective_metric_name="roc_auc",
            group_on="g",
            group_labels="per_group",
        )
    # the metadata is written out: the format-1 checksum pinned in test_curation_container encodes these values
    return CuratedContainer(
        dataset=df,
        dataset_metadata=DatasetMetadata(
            unique_name="toy_ds",
            dataset_year="2025",
            domain_str="finance",
            dataset_source="Kaggle",
            original_dataset_source_download_link="http://example",
            download_description="desc",
            academic_reference_bibtex="bib",
            academic_reference_bibtex_key="key",
            license=None,
            data_tags=["Non-IID", "Grouped"],
            curation_comments=None,
        ),
        task_metadata=task,
        experiment_metadata=PredictiveMLSplitsMetadata(splits_comment="toy", splits={0: {0: ([0, 1, 2, 3], [4, 5])}}),
        uuid="u",
    )


# --- v2 toy definitions (the raw file is the `warehouse` fixture of conftest.py) ----------------------------------
DEFINITION = '''
from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_foundry.definition import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, drop_columns


class Toy(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a generated row positive?",
        use_case="A tester checks that the pipeline runs end to end.",
        row="One generated row.",
        predicted="A random yes/no label.",
        known="A number and a colour.",
        split="Random rows.",
        fit="direct",
        fit_reason="The data is generated for the test.",
    )

    unique_name = "{name}"
    domain = "handcrafted"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://example.org/toy",
            license="CC0",
            year="2024",
            bibtex="""
                @misc{{toy2024,
                  author = {{Tester}},
                  title = {{Toy}},
                  year = {{2024}}
                }}
            """,
        ),
    )
    download_description = """
        Generated by the test.
    """
    curation_comments = "{comment}"

    target = "y"
    problem_type = "binary_classification"
    metric = Metric.fallback(reason="the toy data is generated; it has no source metric")

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "toy.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["y"] = df["y"].map({{0: "no", 1: "yes"}})
        return drop_columns(df, ["row_id"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["colour"])
'''


def write_definition(root: Path, name: str = "toy_ds", *, comment: str = "Toy data.", body: str | None = None) -> Path:
    """Write ``<root>/<name>/dataset.py`` and return the folder."""
    folder = root / name
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "dataset.py"
    path.write_text(DEFINITION.format(name=name, comment=comment) if body is None else body)
    # a rewrite within the same second must still change the mtime that auto-reload looks at
    stamp = time.time() + len(path.read_text()) % 7 + 1
    os.utime(path, (stamp, stamp))
    return folder


def load_definition_from_text(text: str, name: str) -> type[AbstractCuratedDataset]:
    """Load a definition from source text via a temporary folder named ``name``."""
    folder = Path(tempfile.mkdtemp()) / name
    folder.mkdir()
    (folder / "dataset.py").write_text(text)
    return load_definition(folder)


def temporal_body(
    *,
    time_of: str | None = None,
    gap: int | None = None,
    copy: bool = False,
    n_windows: int = 3,
    prediction_time: str | None = None,
    listed: int | None = None,
) -> str:
    """A temporal ``toy_ds``: the 600 toy rows over 30 days (20 per day), windows of 5 days; ``copy`` adds a feature
    ``day`` that counts the same days as the time column, ``listed`` a date feature ``listed`` that many days from it.
    """
    extra = "".join(
        [
            f", gap={gap}" if gap else "",
            ")",
            f', time_of="{time_of}"' if time_of else "",
            f', prediction_time="{prediction_time}"' if prediction_time else "",
        ],
    )
    clean = '        df["t"] = pd.Timestamp("2024-01-01") + pd.to_timedelta(df["row_id"] // 20, unit="D")\n'
    if copy:
        clean += '        df["day"] = df["row_id"] // 20\n'
    if listed is not None:
        clean += f'        df["listed"] = df["t"] + pd.Timedelta(days={listed})\n'
    dates = '["t", "listed"]' if listed is not None else '["t"]'
    return (
        DEFINITION.format(name="toy_ds", comment="Toy data.")
        .replace(
            "from data_foundry.definition import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, "
            "drop_columns",
            "from data_foundry.definition import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, "
            "Temporal, TemporalSplits, drop_columns",
        )
        .replace('        return drop_columns(df, ["row_id"])', clean + '        return drop_columns(df, ["row_id"])')
        .replace(
            '        return FeatureTypes(categorical=["colour"])',
            f'        return FeatureTypes(categorical=["colour"], datetime={dates})',
        )
        .replace(
            '    target = "y"\n',
            f'    temporal = Temporal(on="t", splits=TemporalSplits(window=5, unit="days", '
            f"n_windows={n_windows}{extra})\n"
            '    target = "y"\n',
        )
    )


_IMPORTED = "AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, drop_columns"
IMPORTS = f"from data_foundry.definition import {_IMPORTED}"


def version_body(name: str = "toy_ds_0p2k", extra: str = "") -> str:
    """A version of the toy dataset, sub-sampled to the budget of its collection (:func:`write_version`).

    Named ``toy_ds_<suffix>``, it reads the raw files of ``toy_ds``.
    """
    return (
        DEFINITION.format(name=name, comment="Toy data.")
        .replace(IMPORTS, IMPORTS.replace("Metric,", "Grouping, Metric,"))
        .replace('    target = "y"\n', f'{extra}    target = "y"\n')
    )


def write_collection(root: Path, budget: str = "RowBudget(train=200, test=50)") -> None:
    """Write ``<root>/collection.py`` setting the collection's row budget."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "collection.py").write_text(f"from data_foundry.definition import RowBudget\n\nrow_budget = {budget}\n")


def write_version(root: Path, name: str, body: str, budget: str = "RowBudget(train=200, test=50)") -> None:
    """Write the definition ``body`` into a collection whose row budget is ``budget``."""
    write_collection(root, budget)
    write_definition(root, name, body=body)


TEMPORAL_BUDGET = "RowBudget(train=190, test=60)"
"""The row budget of the temporal versions' collection (``toy_ds_0p19k``)."""


def temporal_version_body(
    name: str = "toy_ds_0p19k", windows: str = 'TemporalSplits(window=5, unit="days", n_windows=3)'
) -> str:
    """A temporal version: the 600 toy rows over 30 days (20 per day), 3 windows of 5 days."""
    return (
        version_body(name, extra=f'    temporal = Temporal(on="t", splits={windows})\n')
        .replace("Metric,", "Metric, Temporal, TemporalSplits,", 1)
        .replace(
            '        return drop_columns(df, ["row_id"])',
            '        df["t"] = pd.Timestamp("2024-01-01") + pd.to_timedelta(df["row_id"] // 20, unit="D")\n'
            '        return drop_columns(df, ["row_id"])',
        )
        .replace(
            '        return FeatureTypes(categorical=["colour"])',
            '        return FeatureTypes(categorical=["colour"], datetime=["t"])',
        )
    )
