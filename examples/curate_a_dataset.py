"""End-to-end walk-through of curating a single dataset into a CuratedContainer.

This example mirrors how a contributor would turn a raw download (here the
UCI Blood Transfusion Service Center dataset) into the bundled
:class:`CuratedContainer` artifact that ships with a BeyondArena release.

The pipeline:

1. Write the **dataset / task metadata** (:class:`DatasetMetadata`,
   :class:`PredictiveMLTaskMetadata`).
2. Load the raw data and apply minimal **preprocessing**.
3. Run the **dataset checks** (sanity statistics, head, target distribution).
4. Generate **outer CV splits** using the curation recommendations.
5. Bundle everything into a :class:`CuratedContainer`.
6. Run the **bundle checks** (:func:`data_foundry.bundle_checks.run_bundle_checks`) —
   the cross-referential integrity checks that need the whole bundle at once.
7. Persist it under the local data warehouse and **verify the export** round-tripped
   (:func:`data_foundry.bundle_checks.verify_saved_container`).

In the end, we run this inside a notebook under
``datasets/_dev/<topic>/<unique_name>/<unique_name>.ipynb`` so the curator
keeps the rendered output of each step in version control. This file is the
same pipeline, condensed to one script you can read top-to-bottom.

Note: the download command in ``DatasetMetadata.download_description`` is not
executed here — you have to run it once to materialize
``local-data-warehouse/blood_transfusion/transfusion.data`` before this
script can read it.

For the full contributor flow (template, PR layout, best practices) see
``CONTRIBUTING_DATASETS.md``.
"""

from __future__ import annotations

import pandas as pd

from data_foundry import dataset_checks
from data_foundry.bundle_checks import run_bundle_checks, verify_saved_container
from data_foundry.curation_container import CuratedContainer
from data_foundry.curation_recommendations import (
    get_recommended_iid_splits,
    get_recommended_splits_dimensions,
)
from data_foundry.schema import (
    DatasetMetadata,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadata,
)

# --- 1. Basic metadata --------------------------------------------------------
dataset_mold = DatasetMetadata(
    unique_name="blood_transfusion",
    dataset_year="2008",
    domain_str="medical & healthcare",
    dataset_source="UCI",
    original_dataset_source_download_link="https://doi.org/10.24432/C5GS39",
    download_description="""
We download the data from the UCI repository and unzip it to a predefined folder.

mkdir -p local-data-warehouse/blood_transfusion/ \\
  && wget -P local-data-warehouse/blood_transfusion/ \\
       https://archive.ics.uci.edu/static/public/176/blood+transfusion+service+center.zip \\
  && unzip local-data-warehouse/blood_transfusion/blood+transfusion+service+center.zip \\
       -d local-data-warehouse/blood_transfusion/
""",
    academic_reference_bibtex="""@article{yeh2009knowledge,
  title={Knowledge discovery on RFM model using Bernoulli sequence},
  author={Yeh, I-Cheng and Yang, King-Jang and Ting, Tao-Ming},
  journal={Expert Systems with applications},
  volume={36},
  number={3},
  pages={5866--5871},
  year={2009},
  publisher={Elsevier}
}
""",
    academic_reference_bibtex_key="yeh2009knowledge",
    license="CC BY 4.0",
    data_tags=["IID"],
    curation_comments="""
- We made feature names more descriptive.
- We renamed the target and mapped binary values to "Yes"/"No".
- Anomaly: the data has a lot of duplicates (29%) and several duplicates with
  different target values.
""",
)
task_mold = PredictiveMLTaskMetadata(
    target_column_name="DonatedBloodInMarch2007",
    problem_type="binary_classification",
    objective_metric_name="roc_auc",
    stratify_on="DonatedBloodInMarch2007",
)

# --- 2. Preprocessing / data cleaning -----------------------------------------
# `dataset_mold.path` resolves to `local-data-warehouse/blood_transfusion/`.
df = pd.read_csv(f"{dataset_mold.path}/transfusion.data")

target_feature = "DonatedBloodInMarch2007"
df.columns = [
    "MonthsSinceLastDonation",
    "NumberOfDonations",
    "TotalBloodDonated",
    "MonthsSinceFirstDonation",
    target_feature,
]
df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"})

cat_features = [target_feature]
df[cat_features] = df[cat_features].astype("category")

# Stable shuffle so the OUTER splits we generate next are reproducible.
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# --- 3. Dataset checks --------------------------------------------------------
df_head, summary, numeric_stats, cat_stats, target_df = dataset_checks.run_all_checks(
    data=df,
    target_feature=task_mold.target_column_name,
    problem_type=task_mold.problem_type,
)

# --- 4. Outer CV splits -------------------------------------------------------
n_repeats, n_splits, none_or_test_size = get_recommended_splits_dimensions(dataset=df)
print(
    f"Recommended IID splits: n_repeats={n_repeats}, n_splits={n_splits}, "
    f"test_size={none_or_test_size}",
)

splits = get_recommended_iid_splits(
    dataset=df,
    n_repeats=n_repeats,
    n_splits=n_splits,
    test_size=none_or_test_size,
    stratify_on=task_mold.stratify_on,
)

splits_mold = PredictiveMLSplitsMetadata(
    splits_comment="Default splits for IID data.",
    splits=splits,
)

# --- 5. Bundle ----------------------------------------------------------------
curated_data = CuratedContainer(
    dataset=df,
    dataset_metadata=dataset_mold,
    task_metadata=task_mold,
    experiment_metadata=splits_mold,
)
print(curated_data.describe())

# --- 6. Bundle checks ---------------------------------------------------------
# Cross-referential integrity checks over the assembled bundle: do the metadata
# columns exist, are the split indices positional and leak-free, does every fold's
# train set cover its test classes, do the `data_tags` match the split regime.
# Errors must be fixed; a warning you accept on purpose goes into `ignore=[...]`.
report = run_bundle_checks(
    curated_data,
    ignore=[
        # Known and documented in `curation_comments`: this dataset really does
        # contain ~29% duplicated rows, including some with conflicting targets.
        "dataset_duplicate_rows",
        "dataset_conflicting_duplicate_rows",
    ],
)
report.raise_if_errors()

# --- 7. Persist + verify the export -------------------------------------------
save_path = curated_data.save()
print(curated_data.uuid)
print(curated_data.checksum)

# The one check that can only run after export: reload from disk and compare the
# file inventory, checksum, dtypes, values, and metadata against what we saved.
verify_saved_container(save_path, container=curated_data).raise_if_errors()
