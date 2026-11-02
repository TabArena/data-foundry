"""The packaged toy container and the example scripts (the metric examples on a format-2 toy container)."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from data_foundry.curation_container import CuratedContainer
from data_foundry.dataset_checks import run_all_checks
from data_foundry.examples import (
    TOY_CONTAINER_UNIQUE_NAME,
    TOY_CONTAINER_UUID,
    get_toy_container_path,
    load_toy_container,
)
from data_foundry.schema import DatasetMetadata, PredictiveMLSplitsMetadata, PredictiveMLTaskMetadataV2, ScoringColumn
from data_foundry.v2.dataset import metric_spec
from data_foundry.v2.metrics import Metric


def test_toy_container_path_exists_inside_package():
    path = get_toy_container_path()
    assert path.is_dir(), f"toy container missing — re-run scripts/build_toy_container.py ({path})"
    assert (path / "dataset.parquet").exists()
    assert (path / "container_metadata.json").exists()


def test_load_toy_container_round_trip():
    container = load_toy_container()
    assert isinstance(container, CuratedContainer)
    assert container.uuid == TOY_CONTAINER_UUID
    assert container.dataset_metadata.unique_name == TOY_CONTAINER_UNIQUE_NAME
    assert container.dataset is not None
    assert len(container.dataset) > 0
    assert container.task_metadata.target_column_name in container.dataset.columns
    # Checksum must be stable after a load.
    assert container.checksum == container._create_checksum()


def test_toy_container_ships_extra_file():
    container = load_toy_container()
    extras = container.list_extra_files()
    assert "toy_extra.parquet" in extras
    assert container.has_extra_file("toy_extra.parquet") is True
    resolved = container.extra_file_path("toy_extra.parquet")
    assert resolved.is_file()


def test_toy_container_satisfies_curation_contract():
    """The shipped toy container must pass the curation checks for its declared problem type.

    Regression guard for the classification-target contract (a classification target must be
    ``category`` dtype) that downstream consumers rely on — e.g. TabArena's
    ``convert_curated_container_to_user_task``. ``run_all_checks`` raises if it is violated.
    """
    container = load_toy_container()
    run_all_checks(
        data=container.dataset,
        problem_type=container.task_metadata.problem_type,
        target_feature=container.task_metadata.target_column_name,
        print_report=False,
    )


# --- the metric examples: a format-2 toy container with a scoring column ---------------------------------------------

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def _example(name: str):
    spec = importlib.util.spec_from_file_location(f"example_{name}", EXAMPLES / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _format_2_toy(tmp_path: Path) -> Path:
    """A regression container scored per era (``mean_group_pearsonr`` on the scoring column ``era``)."""
    rng = np.random.default_rng(0)
    n = 120
    df = pd.DataFrame(
        {
            "x1": rng.normal(size=n),
            "x2": pd.Categorical(rng.choice(["a", "b", "c"], size=n)),
            "era": np.repeat(np.arange(12), n // 12),
        }
    )
    df["y"] = df["x1"] + rng.normal(scale=0.5, size=n)
    metric = Metric.source(
        "mean_group_pearsonr", original="per-era correlation", reference="https://example.org", inputs={"group": "era"}
    )
    task = PredictiveMLTaskMetadataV2(
        target_column_name="y",
        problem_type="regression",
        objective_metric=metric_spec(metric, "regression"),
        scoring_columns=[
            ScoringColumn(
                column="era", role="group", used_by="mean_group_pearsonr", description="the era a row belongs to"
            )
        ],
    )
    index = np.arange(n)
    splits = {0: {0: (index[index % 2 == 0].tolist(), index[index % 2 == 1].tolist())}}
    container = CuratedContainer(
        dataset=df,
        dataset_metadata=DatasetMetadata(
            unique_name="toy_eras",
            dataset_year="2025",
            domain_str="finance",
            dataset_source="Kaggle",
            original_dataset_source_download_link="http://example",
            download_description="desc",
            academic_reference_bibtex="bib",
            academic_reference_bibtex_key="key",
            license=None,
            data_tags=[],
            curation_comments=None,
        ),
        task_metadata=task,
        experiment_metadata=PredictiveMLSplitsMetadata(splits_comment="toy", splits=splits),
        uuid="u",
    )
    return container.save(save_dir=tmp_path)


def test_read_metric_without_data_foundry_imports_no_data_foundry():
    """The plain-json example imports nothing from data_foundry."""
    tree = ast.parse((EXAMPLES / "read_metric_without_data_foundry.py").read_text())
    imported = [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
    imported += [n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    assert not [m for m in imported if m.startswith("data_foundry")]


def test_read_metric_without_data_foundry_on_both_formats(tmp_path, capsys):
    """Format 1 gives the bare name and a sklearn score; format 2 the full spec and the scoring column."""
    example = _example("read_metric_without_data_foundry")
    # Format 1 (the packaged toy): the bare name, scored by scikit-learn.
    value = example.main(get_toy_container_path())
    assert 0.0 <= value <= 1.0
    out = capsys.readouterr().out
    assert "name: roc_auc" in out
    assert "Scoring columns: none" in out
    # Format 2: the full spec and the scoring column, which is not a feature; a custom metric is not scored here.
    assert example.main(_format_2_toy(tmp_path)) is None
    out = capsys.readouterr().out
    assert "name: mean_group_pearsonr" in out
    assert "original: per-era correlation" in out
    assert "era: role group, used by mean_group_pearsonr" in out
    assert "Features: 2 of 4 columns" in out


def test_benchmark_example_scores_a_format_2_container_by_its_spec(tmp_path, capsys):
    """The benchmark example drops the scoring column and scores by scorer(container)."""
    pytest.importorskip("sklearn")
    example = _example("benchmark_on_beyond_arena")
    path = _format_2_toy(tmp_path)
    scores = example.main(None, "unused", path)
    assert len(scores) == 1
    assert 0.0 < scores[0] <= 1.0  # x1 drives y, so the per-era correlation is positive
    assert "mean_group_pearsonr=" in capsys.readouterr().out
