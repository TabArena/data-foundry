"""Very simple experimental script to extract some metadata from a local data warehouse."""

from data_foundry.curation_container import CuratedContainer

from pathlib import Path
import uuid6
from typing import Dict, Optional
import pandas as pd
from tqdm import tqdm


def _parse_uuid6_dirname(name: str) -> Optional[uuid6.UUID]:
    """
    Return a uuid.UUID if `name` is a valid UUID and version==7, else None.
    """
    try:
        u = uuid6.UUID(name)
    except ValueError:
        return None
    return u if u.version == 7 else None


def newest_uuid6_folder_per_subfolder(root: str | Path) -> Dict[Path, Optional[Path]]:
    """
    For each direct subfolder in `root` (e.g. local-data-warehouse/<dataset>/),
    find the subdirectory whose name is the newest UUIDv7 and return its path.

    Returns: {dataset_folder_path: newest_uuid7_folder_path_or_None}
    """
    root = Path(root)
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    out: Dict[Path, Optional[Path]] = {}

    for dataset_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        newest_path: Optional[Path] = None
        newest_uuid: Optional[uuid6.UUID] = None

        for child in dataset_dir.iterdir():
            if not child.is_dir():
                continue

            u = _parse_uuid6_dirname(child.name)
            if u is None:
                continue

            # UUIDv6 is time-sortable; comparing by integer value gives newest as max.
            if newest_uuid is None or u.int > newest_uuid.int:
                newest_uuid = u
                newest_path = child

        out[dataset_dir] = newest_path

    return out


def search_local_warehouse():
    root = Path(__file__).parent.parent / "local-data-warehouse"
    newest = newest_uuid6_folder_per_subfolder(root)

    valid_datasets = []
    for dataset_dir, uuid6_dir in newest.items():
        if uuid6_dir is not None:
            valid_datasets.append(uuid6_dir)
        else:
            print(f"[no UUIDv7 folders found] {dataset_dir}")

    print(f"Found {len(valid_datasets)} datasets in the local data warehouse.")
    return valid_datasets


def dataset_paths_to_metadata(dataset_paths: list[Path]) -> pd.DataFrame:

    columns = [
        "name",
        "task_type",
        "dataset_identifier",
        "container_name",
        "container_uuid",
        "tags",
        "num_samples",
        "num_features",
        "num_classes",
        "target_column",
        "is_iid",
        "is_non_iid",
        "stratify_column",
        "group_column",
        "time_column",
        "group_time_column",
        "checksum",
    ]
    metadata = []
    for path in tqdm(dataset_paths, desc="Extracting metadata from datasets"):
        container = CuratedContainer.load(path)

        container_name, container_uuid = path.parts[-2:]
        name = container.dataset_metadata.unique_name

        task_type = container.task_metadata.problem_type
        if task_type == "regression":
            task_type = "regression"
        else:
            task_type = "multiclass"
        dataset_identifier = f"df_{name}"
        tags = ["data_foundry", "gcp"]

        data_tags = container.dataset_metadata.data_tags
        is_iid = "IID" in data_tags
        is_non_iid = "Non-IID" in data_tags
        if is_iid:
            tags.append("iid")
        if is_non_iid:
            if "Grouped" in data_tags:
                tags.append("grouped")
            if "Temporal" in data_tags:
                tags.append("temporal")

        num_samples, num_features = container.dataset.shape
        num_features = num_features - 1 # exclude target column
        target_column = container.task_metadata.target_column_name

        if task_type == "classification":
            num_classes = container.dataset[target_column].nunique()
        else:
            num_classes = None

        stratify_column = container.task_metadata.stratify_on
        group_column = container.task_metadata.group_on
        time_column = container.task_metadata.time_on
        group_time_column = container.task_metadata.group_time_on

        checksum = container.checksum



        metadata.append(
            [
                name,
                task_type,
                dataset_identifier,
                container_name,
                container_uuid,
                tags,
                num_samples,
                num_features,
                num_classes,
                target_column,
                is_iid,
                is_non_iid,
                stratify_column,
                group_column,
                time_column,
                group_time_column,
                checksum,
            ]
        )
        del container # free memory

    return pd.DataFrame(metadata, columns=columns)


if __name__ == "__main__":
    local_datasets = search_local_warehouse()
    res = dataset_paths_to_metadata(local_datasets)
    print(res)
    res.to_csv("local_warehouse_metadata.csv", index=False)
