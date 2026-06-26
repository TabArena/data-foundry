from __future__ import annotations

from data_foundry.curation_container import CuratedContainer
from data_foundry.dataset_checks import run_all_checks
from data_foundry.examples import (
    TOY_CONTAINER_UNIQUE_NAME,
    TOY_CONTAINER_UUID,
    get_toy_container_path,
    load_toy_container,
)


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
