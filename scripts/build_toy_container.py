"""Rebuild the toy curated containers shipped inside `data_foundry.examples`.

This produces two small, fully-formed `CuratedContainer`s on disk under
``src/data_foundry/examples/toy_container/<unique_name>/<uuid>/`` so that
the package can offer a runnable end-to-end example after a plain
``pip install data-foundry`` (no warehouse required):

* ``toy_iid_dataset``, format 1 (the shape of the BeyondArena containers): binary classification, IID folds;
* ``toy_grouped_rates``, format 2 (the shape of the TabArena v0.2 containers): claims per year insured, grouped by
  customer, scored by the Poisson deviance weighted by the years insured (a weight scoring column that is also the
  training weight), with an ordered category among the features.

Run from the repo root::

    python scripts/build_toy_container.py      # both
    python scripts/build_toy_container.py 2    # the format-2 toy only
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

from data_foundry.curation_container import CuratedContainer
from data_foundry.examples import (
    TOY_CONTAINER_UNIQUE_NAME,
    TOY_CONTAINER_UUID,
    TOY_V2_CONTAINER_UNIQUE_NAME,
    TOY_V2_CONTAINER_UUID,
)
from data_foundry.metrics import METRICS
from data_foundry.schema import (
    DatasetMetadataV2,
    Grouping,
    MetricSpec,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadataV2,
    ScoringColumn,
    Source,
)
from data_foundry.v1 import DatasetMetadata, PredictiveMLTaskMetadata

REPO_ROOT = Path(__file__).resolve().parent.parent
TOY_BASE_DIR = REPO_ROOT / "src" / "data_foundry" / "examples" / "toy_container"


TOY_EXTRA_FILENAME: str = "toy_extra.parquet"
"""File name of the toy extra-artifact shipped next to the toy container."""


def make_toy_dataframe(n_rows: int = 200, rng_seed: int = 0) -> pd.DataFrame:
    """Tiny synthetic binary-classification dataset with a few dtype flavours."""
    rng = np.random.default_rng(rng_seed)
    x_num = rng.normal(size=n_rows).astype("float32")
    x_int = rng.integers(low=0, high=10, size=n_rows).astype("int32")
    x_cat = pd.Categorical(rng.choice(["a", "b", "c"], size=n_rows))
    noise = rng.normal(scale=0.5, size=n_rows)
    # A classification target must be ``category`` dtype — this is the Data Foundry curation
    # contract (see ``dataset_checks.summarize_dataset``), and what consumers (e.g. TabArena's
    # ``convert_curated_container_to_user_task``) rely on. Use string labels like a real curated set.
    target = pd.Categorical(np.where((x_num + 0.3 * x_int + noise) > 0, "pos", "neg"))
    return pd.DataFrame(
        {
            "feat_num": x_num,
            "feat_int": x_int,
            "feat_cat": x_cat,
            "target": target,
        },
    )


def make_toy_extra(n_rows: int = 8, n_cols: int = 4, rng_seed: int = 1) -> pd.DataFrame:
    """Toy extra-artifact parquet — random floats with an arbitrary ``key`` index.

    Stands in for any producer-defined sidecar (e.g. an embedding cache) shipped
    alongside the six core container files.
    """
    rng = np.random.default_rng(rng_seed)
    return pd.DataFrame(
        rng.normal(size=(n_rows, n_cols)).astype("float32"),
        index=pd.Index([f"row_{i}" for i in range(n_rows)], name="key"),
    )


def make_toy_splits(n_rows: int, n_folds: int = 3, rng_seed: int = 0) -> dict:
    """Single-repeat K-fold splits in the same shape `PredictiveMLSplitsMetadata` expects."""
    rng = np.random.default_rng(rng_seed)
    perm = rng.permutation(n_rows)
    fold_indices = np.array_split(perm, n_folds)

    folds: dict[int, tuple[list[int], list[int]]] = {}
    for fold_id, test_idx in enumerate(fold_indices):
        test_idx_sorted = sorted(int(i) for i in test_idx)
        train_idx_sorted = sorted(int(i) for i in perm if i not in set(test_idx))
        folds[fold_id] = (train_idx_sorted, test_idx_sorted)
    return {0: folds}


VEHICLE_SIZES = ["small", "medium", "large"]
"""The levels of the ordered category ``vehicle_size`` of the format-2 toy."""


def make_toy_rates_dataframe(n_customers: int = 60, rng_seed: int = 0) -> pd.DataFrame:
    """Policies of customers with one to five policies each: claims per year insured, the years insured
    (``exposure``), and the customer (the group: a customer's policies share a driver).
    """
    rng = np.random.default_rng(rng_seed)
    n_policies = rng.integers(1, 6, n_customers)
    customer = np.repeat(np.arange(n_customers), n_policies)
    n = len(customer)
    driver_age = rng.integers(18, 80, n_customers)[customer]
    vehicle_size = pd.Categorical(rng.choice(VEHICLE_SIZES, n), categories=VEHICLE_SIZES, ordered=True)
    region = pd.Categorical(rng.choice(["north", "south", "east", "west"], n))
    exposure = rng.integers(1, 13, n) / 12  # months insured, in years
    customer_effect = rng.normal(scale=0.3, size=n_customers)[customer]
    rate = 0.15 * np.exp(-0.02 * (driver_age - 40) + 0.3 * vehicle_size.codes + customer_effect)
    claims = rng.poisson(rate * exposure)
    return pd.DataFrame(
        {
            "customer": customer,
            "driver_age": driver_age.astype("int64"),
            "vehicle_size": vehicle_size,
            "region": region,
            "exposure": exposure,
            "claim_rate": claims / exposure,
        },
    )


def make_grouped_splits(groups: np.ndarray, n_folds: int = 3, rng_seed: int = 0) -> dict:
    """One repeat of ``n_folds`` folds that keep each group on one side."""
    rng = np.random.default_rng(rng_seed)
    unique = rng.permutation(np.unique(groups))
    fold_of = {g: i % n_folds for i, g in enumerate(unique)}
    folds_per_row = np.array([fold_of[g] for g in groups])
    positions = np.arange(len(groups))
    return {
        0: {
            fold: (positions[folds_per_row != fold].tolist(), positions[folds_per_row == fold].tolist())
            for fold in range(n_folds)
        }
    }


def build_v2_toy() -> Path:
    """The format-2 toy: a grouped rate task with a weight scoring column, the training weight."""
    df = make_toy_rates_dataframe()
    poisson = METRICS["mean_poisson_deviance"]
    dataset_metadata = DatasetMetadataV2(
        unique_name=TOY_V2_CONTAINER_UNIQUE_NAME,
        domain="handcrafted",
        sources=[
            Source(
                role="publication",
                platform="Other",
                url="https://example.com/toy",
                license="CC0-1.0",
                year="2026",
                bibtex="@misc{toyrates, title={Toy synthetic claim rates}, year={2026}}",
            )
        ],
        download_description="Synthetic dataset generated by scripts/build_toy_container.py.",
        data_tags=["Non-IID", "Grouped"],
        curation_comments=(
            "Tiny synthetic format-2 container shipped inside the data_foundry package: claims per year insured of "
            "customers' policies, for trying the task view (container.task()) right after pip install."
        ),
    )
    task_metadata = PredictiveMLTaskMetadataV2(
        target_column_name="claim_rate",
        problem_type="regression",
        objective_metric=MetricSpec(
            name=poisson.name,
            kind=poisson.kind,
            prediction=poisson.prediction,
            greater_is_better=poisson.greater_is_better,
            origin="context",
            params={"min_prediction": 0.001},
            inputs={"weight": "exposure"},
            definition=poisson.definition,
            reason="A claim rate is scored by the Poisson deviance weighted by the years insured (synthetic data).",
        ),
        grouping=Grouping(
            on="customer",
            labels="per_sample",
            definition="A customer and their policies; new customers are scored, so a customer is held out whole.",
        ),
        scoring_columns=[
            ScoringColumn(
                column="exposure",
                role="weight",
                used_by="mean_poisson_deviance",
                description="years insured: the rate's denominator, known only once the policy period has ended",
            )
        ],
        sample_weight="exposure",
    )
    splits_metadata = PredictiveMLSplitsMetadata(
        splits_comment="3 folds over a single repeat, each customer on one side (for demonstration).",
        splits=make_grouped_splits(df["customer"].to_numpy()),
    )
    container = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
        uuid=TOY_V2_CONTAINER_UUID,
    )
    return _save(container, TOY_V2_CONTAINER_UNIQUE_NAME)


def _save(container: CuratedContainer, unique_name: str) -> Path:
    """Save ``container`` under the toy folder, replacing its earlier build."""
    if (TOY_BASE_DIR / unique_name).exists():
        shutil.rmtree(TOY_BASE_DIR / unique_name)
    return container.save(save_dir=TOY_BASE_DIR)


def build_v1_toy() -> Path:
    """The format-1 toy: binary classification with IID folds, and an extra file next to it."""
    df = make_toy_dataframe()

    dataset_metadata = DatasetMetadata(
        unique_name=TOY_CONTAINER_UNIQUE_NAME,
        dataset_year="2026",
        domain_str="handcrafted",
        dataset_source="Other",
        original_dataset_source_download_link="https://example.com/toy",
        download_description="Synthetic dataset generated by scripts/build_toy_container.py.",
        academic_reference_bibtex="@misc{toy, title={Toy synthetic dataset}, year={2026}}",
        academic_reference_bibtex_key="toy",
        license="CC0-1.0",
        data_tags=["IID"],
        curation_comments=(
            "Tiny synthetic binary-classification dataset shipped inside the data_foundry "
            "package so users can try CuratedContainer.load() right after pip install."
        ),
    )
    task_metadata = PredictiveMLTaskMetadata(
        target_column_name="target",
        problem_type="binary_classification",
        objective_metric_name="roc_auc",
        stratify_on="target",
    )
    splits_metadata = PredictiveMLSplitsMetadata(
        splits_comment="3-fold stratified-ish split over a single repeat (for demonstration).",
        splits=make_toy_splits(n_rows=len(df)),
    )

    container = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
        uuid=TOY_CONTAINER_UUID,
        version_comment="v1 — initial toy container.",
    )
    save_path = _save(container, TOY_CONTAINER_UNIQUE_NAME)

    extra = make_toy_extra()
    extra.to_parquet(save_path / TOY_EXTRA_FILENAME)
    return save_path


def main(formats: list[int]) -> None:
    builds = {1: build_v1_toy, 2: build_v2_toy}
    for format_version in formats:
        print(f"Toy container saved to {builds[format_version]()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "formats", nargs="*", type=int, choices=[1, 2], default=[1, 2], help="The toys to rebuild (default: both)."
    )
    main(parser.parse_args().formats)
