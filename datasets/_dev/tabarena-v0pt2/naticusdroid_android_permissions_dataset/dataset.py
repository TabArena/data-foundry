"""Curated dataset definition for `naticusdroid_android_permissions_dataset` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


class NaticusdroidAndroidPermissionsDataset(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Is an Android app that is already released malware, judged from the permissions it requests?"),
        use_case=(
            "For example, an app store or security scanner sweeps apps already released for malware, judged from the "
            "permissions they declare, to find the malware among apps not yet labelled; the record frames the task as"
            " classifying apps released in the past."
        ),
        row=(
            "One distinct combination of permissions and label from more than 29,000 benign and malware Android apps "
            "released 2010-2019; 7,491 rows remain after removing exact repeats."
        ),
        predicted="Whether the app is malware (35% of the rows are).",
        known="Whether the app declares each of 85 Android permissions, native and custom.",
        split=(
            "Random rows, so the test data stands for released apps of the same decade that are not yet labelled; "
            "release dates are not in the data."
        ),
        changes=(
            "We drop exact repeated rows, 75% of the file, which the paper does not mention; otherwise identical rows"
            " would sit on both sides of the split."
        ),
        fit="direct",
        fit_reason=(
            "The permissions are declared by each app and known without running it, and random apps of the same "
            "decade stand for released apps not yet labelled. With exact repeats dropped, each permission set counts "
            "once, so apps whose exact set is already labelled, easy cases in use, are not in the test data. New apps"
            " would need a split by release date, which the data lacks."
        ),
    )

    # Dataset
    unique_name = "naticusdroid_android_permissions_dataset"
    year = "2022"
    domain = "technology & internet"
    source = "UCI"
    source_url = "https://archive.ics.uci.edu/dataset/722/naticusdroid+android+permissions+dataset"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/naticusdroid_android_permissions_dataset/ && wget -P local-data-warehouse/naticusdroid_android_permissions_dataset/ https://archive.ics.uci.edu/static/public/722/naticusdroid+android+permissions+dataset.zip && unzip local-data-warehouse/naticusdroid_android_permissions_dataset/naticusdroid+android+permissions+dataset.zip -d local-data-warehouse/naticusdroid_android_permissions_dataset/  && rm local-data-warehouse/naticusdroid_android_permissions_dataset/naticusdroid+android+permissions+dataset.zip
    """
    bibtex = """
        @article{mathur2021naticusdroid,
          title={NATICUSdroid: A malware detection framework for Android using native and custom permissions},
          author={Mathur, Akshay and Podila, Laxmi Mounika and Kulkarni, Keyur and Niyaz, Quamar and Javaid, Ahmad Y},
          journal={Journal of Information Security and Applications},
          volume={58},
          pages={102696},
          year={2021},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - Originally, the data has 75% duplicates and a perfect class balance. The authors never mention duplicates in their paper. Given this large amount of duplicates, we dropped all row-duplicates, keeping only the first entry.
        - We drop one duplicated column.
        - Anomaly: all features are binary categorical features.
    """

    # Task
    target = "Malware"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/data.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.rename(
            columns={
                "Result": "Malware",
            }
        )
        df["Malware"] = df["Malware"].map({0: "No", 1: "Yes"})
        # Drop duplicates
        df = df.drop_duplicates(keep="first")
        # Map all to cat
        df = df.astype("category")
        # Drop duplicated col
        df = df.drop(columns=["me.everything.badger.permission.BADGE_COUNT_READ"])
        return df
