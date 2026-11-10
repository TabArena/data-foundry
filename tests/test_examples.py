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
from data_foundry.v2.metrics import Metric, scorer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_poisson_deviance


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


def _format_2_metadata(unique_name: str) -> DatasetMetadata:
    return DatasetMetadata(
        unique_name=unique_name,
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
    )


def _format_2_toy(tmp_path: Path, extra: dict | None = None) -> Path:
    """A regression container scored per era (``mean_group_pearsonr`` on the scoring column ``era``); ``extra``
    adds feature columns (name to values).
    """
    rng = np.random.default_rng(0)
    n = 120
    df = pd.DataFrame(
        {
            "x1": rng.normal(size=n),
            "x2": pd.Categorical(rng.choice(["a", "b", "c"], size=n)),
            "era": np.repeat(np.arange(12), n // 12),
        }
    )
    for name, values in (extra or {}).items():
        df[name] = values
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
        dataset_metadata=_format_2_metadata("toy_eras"),
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


def test_benchmark_container_example_scores_a_format_2_container_by_its_spec(tmp_path, capsys):
    """The v2 benchmark example drops the scoring column and scores by scorer(container)."""
    pytest.importorskip("sklearn")
    example = _example("benchmark_container")
    path = _format_2_toy(tmp_path)
    scores = example.main(path)
    assert len(scores) == 1
    assert 0.0 < scores[0] <= 1.0  # x1 drives y, so the per-era correlation is positive
    assert "mean_group_pearsonr=" in capsys.readouterr().out


def test_benchmark_container_example_encodes_every_feature_type(tmp_path, capsys):
    """An ordinal by its order, a date and a text column encoded, a categorical as it is; the era is never an input."""
    pytest.importorskip("sklearn")
    example = _example("benchmark_container")
    rng = np.random.default_rng(1)
    n = 120
    extra = {
        "grade": pd.Categorical(rng.choice(["low", "mid", "high"], n), categories=["low", "mid", "high"], ordered=True),
        "seen": pd.date_range("2024-01-01", periods=n, freq="D"),
        "note": pd.Series(rng.choice(["red car fast", "blue bike slow", "green bus late"], n), dtype="string"),
    }
    container = CuratedContainer.load(_format_2_toy(tmp_path, extra))
    df, inputs = example.encoded_frame(container)
    assert "era" not in inputs
    assert "y" not in inputs
    assert df["grade"].dtype == float
    assert set(df["grade"].dropna()) <= {0.0, 1.0, 2.0}
    assert "seen" not in inputs
    assert any(c.startswith("seen_") for c in inputs)
    assert "note" in inputs  # encoded per split, on its training rows
    scores = example.benchmark(container)
    assert len(scores) == 1
    assert "1 text columns encoded per split" in capsys.readouterr().out


def test_benchmark_container_example_scores_an_ordered_target_as_scikit_learn_does(tmp_path):
    """An ordered multiclass target (low < mid < high): the score is scikit-learn's log loss on classes_ order."""
    pytest.importorskip("sklearn")
    from sklearn.ensemble import HistGradientBoostingClassifier  # noqa: PLC0415 - scikit-learn is optional
    from sklearn.metrics import log_loss  # noqa: PLC0415 - scikit-learn is optional

    example = _example("benchmark_container")
    rng = np.random.default_rng(2)
    n = 150
    x1 = rng.normal(size=n)
    scale = ["low", "mid", "high"]
    y = pd.Categorical(
        np.array(scale)[np.digitize(x1 + rng.normal(scale=0.7, size=n), [-0.5, 0.5])], scale, ordered=True
    )
    df = pd.DataFrame({"x1": x1, "y": y})
    task = PredictiveMLTaskMetadataV2(
        target_column_name="y",
        problem_type="multiclass_classification",
        objective_metric=metric_spec(
            Metric.source("log_loss", reference="https://example.org"), "multiclass_classification"
        ),
    )
    index = np.arange(n)
    train, test = index[index % 3 != 0], index[index % 3 == 0]
    container = CuratedContainer(
        dataset=df,
        dataset_metadata=_format_2_metadata("toy_ordered"),
        task_metadata=task,
        experiment_metadata=PredictiveMLSplitsMetadata(
            splits_comment="toy", splits={0: {0: (train.tolist(), test.tolist())}}
        ),
        uuid="u",
    )
    container = CuratedContainer.load(container.save(save_dir=tmp_path))
    assert list(container.dataset["y"].cat.categories) == scale  # the declared order stays in the container
    model = HistGradientBoostingClassifier(categorical_features="from_dtype", random_state=42)
    model.fit(df[["x1"]].iloc[train], df["y"].iloc[train])
    assert list(model.classes_) == sorted(scale)
    expected = log_loss(df["y"].iloc[test], model.predict_proba(df[["x1"]].iloc[test]), labels=model.classes_)
    assert example.benchmark(container) == [pytest.approx(expected)]


def test_benchmark_container_example_refuses_a_format_1_container():
    """A BeyondArena (format 1) container belongs to the other example."""
    example = _example("benchmark_container")
    with pytest.raises(SystemExit, match="benchmark_on_beyond_arena"):
        example.main(get_toy_container_path())


def _rate_toy(tmp_path: Path) -> Path:
    """Claims per year insured, scored by the Poisson deviance weighted by the years insured (the training weight)."""
    rng = np.random.default_rng(2)
    n = 300
    exposure = rng.integers(1, 13, n) / 12
    df = pd.DataFrame({"x1": rng.normal(size=n), "Exposure": exposure})
    df["claim_frequency"] = rng.poisson(0.2 * np.exp(0.5 * df["x1"]) * exposure) / exposure
    metric = Metric.source(
        "mean_poisson_deviance",
        reference="https://example.org",
        params={"min_prediction": 1e-4},
        inputs={"weight": "Exposure"},
    )
    task = PredictiveMLTaskMetadataV2(
        target_column_name="claim_frequency",
        problem_type="regression",
        objective_metric=metric_spec(metric, "regression"),
        scoring_columns=[
            ScoringColumn(
                column="Exposure", role="weight", used_by="mean_poisson_deviance", description="years insured"
            )
        ],
        sample_weight="Exposure",
    )
    index = np.arange(n)
    splits = {0: {0: (index[index % 3 != 0].tolist(), index[index % 3 == 0].tolist())}}
    container = CuratedContainer(
        dataset=df,
        dataset_metadata=_format_2_metadata("toy_rates"),
        task_metadata=task,
        experiment_metadata=PredictiveMLSplitsMetadata(splits_comment="toy", splits=splits),
        uuid="u",
    )
    return container.save(save_dir=tmp_path)


def test_both_examples_weight_a_rate_by_its_training_weight(tmp_path, capsys):
    """The benchmark fits with the training weight and the scorer weights the test rows; the plain-json reader
    floors the predictions and passes the weight to scikit-learn, as the scorer does.
    """
    folder = _rate_toy(tmp_path)
    container = CuratedContainer.load(folder)
    df = container.dataset
    train, test = container.experiment_metadata.splits[0][0]
    model = HistGradientBoostingRegressor(categorical_features="from_dtype", random_state=42)
    model.fit(df[["x1"]].iloc[train], df["claim_frequency"].iloc[train], sample_weight=df["Exposure"].iloc[train])
    expected = scorer(container)(
        df["claim_frequency"].iloc[test].to_numpy(), model.predict(df[["x1"]].iloc[test]), test
    )
    assert _example("benchmark_container").benchmark(container) == [pytest.approx(expected)]
    assert "fitted with `Exposure` as the row weight" in capsys.readouterr().out
    value = _example("read_metric_without_data_foundry").main(folder)
    rate, exposure = df["claim_frequency"].iloc[test], df["Exposure"].iloc[test]
    dummy = np.full(len(test), float(df["claim_frequency"].iloc[train].mean()))
    assert value == pytest.approx(mean_poisson_deviance(rate, dummy, sample_weight=exposure))
    assert "Training weight: Exposure" in capsys.readouterr().out


def test_the_family_example_checks_a_parent_and_its_tasks(tmp_path, capsys):
    spec = importlib.util.spec_from_file_location("example_run_family", EXAMPLES / "dataset_family" / "run_family.py")
    example = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example)
    first = example.main(tmp_path / "warehouse")
    assert set(first) == {"exam_scores", "exam_scores_math", "exam_scores_reading"}
    assert example.main(tmp_path / "again") == first  # the raw files and every checksum are reproducible
    out = capsys.readouterr().out
    assert "exam_scores_math       grouped_non_iid  <- exam_scores" in out
    assert "derived from `exam_scores`: The math score as the target" in out
    assert "0 error(s)" in out
    assert "exam_scores_math_iid: folder None" in out
    assert "dropped as no features: ['reading_score', 'source_file', 'source_row', 'source_id']" in out
    assert "raw files in its metadata: ['Ashford.csv'" in out
    assert not list((EXAMPLES / "dataset_family").glob("*/README.md")), "the example writes no README"


@pytest.mark.parametrize("path", sorted(EXAMPLES.rglob("*.py")), ids=lambda p: p.relative_to(EXAMPLES).as_posix())
def test_every_example_parses(path):
    """An example that does not run in the tests (it needs the network) must still be valid Python."""
    ast.parse(path.read_text(), filename=str(path))
