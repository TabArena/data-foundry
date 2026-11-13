"""Curated dataset definition for `aps_failure` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Grouping, Metric, Source, TaskSummary
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

TARGET = "AirPressureSystemFailure"
RARE_MAX = 5  # a value held by 2 to 5 rows in its column is rare
MIN_SHARED = 5  # two rows are a candidate pair when they share at least 5 rare values
COPY_COUNTERS = 140  # a pair equal in at least 140 of the 170 counters is one read-out copied: one row stays
TRUCK_COUNTERS = 60  # a pair equal in at least 60 counters is the same truck read again: one group


def _linked_pairs(values: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The candidate pairs ``(a, b)`` with ``a < b`` and the number of counters each pair agrees on.

    A candidate pair shares at least ``MIN_SHARED`` values that 2 to ``RARE_MAX`` rows hold in their column (missing
    cells are never rare); two missing cells count as equal in the agreement.
    """
    n = len(values)
    keys = []
    for j in range(values.shape[1]):
        column = pd.Series(values[:, j])
        rows = np.flatnonzero(column.map(column.value_counts()).between(2, RARE_MAX).to_numpy())
        order = np.argsort(values[rows, j], kind="stable")  # equal values keep the rows' ascending order
        rows = rows[order]
        _, start, size = np.unique(values[rows, j], return_index=True, return_counts=True)
        for k in range(2, RARE_MAX + 1):
            first = start[size == k]
            for i in range(k):
                for m in range(i + 1, k):
                    keys.append(rows[first + i].astype(np.int64) * n + rows[first + m])
    pair, shared = np.unique(np.concatenate(keys), return_counts=True)
    pair = pair[shared >= MIN_SHARED]
    a, b = pair // n, pair % n
    left, right = values[a], values[b]
    agree = ((left == right) | (np.isnan(left) & np.isnan(right))).sum(axis=1)
    return a, b, agree


def _clusters(n: int, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """One number per row: the connected components of the links ``(a, b)``."""
    graph = coo_matrix((np.ones(len(a)), (a, b)), shape=(n, n))
    return connected_components(graph, directed=False)[1]


class ApsFailure(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Is a heavy truck's failure in one specific component of its air pressure system, rather than in another "
            "part?"
        ),
        use_case=(
            "From a truck's operational data, a workshop decides whether a mechanic should check the air pressure "
            "system, which drives braking and gear changes: a needless check costs 10 and a missed faulty truck, "
            "which may break down, costs 500 (the challenge's costs)."
        ),
        row=(
            "One read-out of a heavy Scania truck in everyday use with a component failure, from its operational "
            "data; a subset of the available data chosen by experts (IDA 2016 Industrial Challenge, 76,000 rows, "
            "63,937 once copies of one read-out are dropped). A truck can appear in more than one row. The period is "
            "not stated."
        ),
        predicted=(
            "Whether the failure is in the specific air pressure system component (2.0% of the rows) or in a "
            "component unrelated to that system. How long before or after the failure the data were read is not "
            "stated."
        ),
        known=(
            "170 anonymised readings of the truck's operation: single counters and seven histograms whose bins count "
            "values in different ranges of a measured condition; many readings are missing."
        ),
        split=(
            "Whole trucks: rows that agree on at least 60 of the 170 counters, probably the same truck read again, "
            "stay on one side, so the test data stand for trucks not seen in training. The challenge held out its last"
            " 16,000 rows, which share trucks with its training rows and are not shown to be later in time; the files "
            "have no dates."
        ),
        changes=(
            "We merge the challenge's training and test files, keep one row of each set of rows that agree on at "
            "least 140 of the 170 counters (one read-out copied; 12,063 rows go), and split by truck, the rows that "
            "agree on at least 60 counters."
        ),
        fit="approximate",
        fit_reason=(
            "Failures are undated, so a split by truck stands in for a "
            "split by time (the dataset is tagged as a forced grouped split of temporal data). When the data were read"
            " relative to the failure is not stated, so whether the model warns before a breakdown or diagnoses after"
            " it is unclear."
        ),
    )

    # Dataset
    unique_name = "aps_failure"
    domain = "industry & manufacturing"
    sources = (
        Source(
            role="publication",
            platform="Other",  # the IDA 2016 Industrial Challenge (Scania); its site is gone, UCI 421 re-hosts its zip
            url="https://web.archive.org/web/20161011/http://ida2016.blogs.dsv.su.se/",
            license="CC BY 4.0",
            year="2016",
            bibtex=r"""
                @misc{ida2016challenge,
                  author       = {{IDA2016Challenge}},
                  title        = {IDA2016Challenge [Dataset]},
                  year         = {2016},
                  howpublished = {\url{https://doi.org/10.24432/C5V60Q}},
                  note         = {UCI Machine Learning Repository},
                }
            """,
        ),
        Source(
            role="copy",
            platform="UCI",
            url="https://doi.org/10.24432/C5V60Q",
            license="CC BY 4.0",
            name="UCI 414, the re-hosted challenge zip",
        ),
    )
    data_tags = ("ForcedGroupedFromTemporal", "Anonymized")
    download_description = """
        We download UCI's copy (https://doi.org/10.24432/C5V60Q) of the IDA 2016 Industrial Challenge files.

        mkdir -p local-data-warehouse/aps_failure && wget -P local-data-warehouse/aps_failure/ https://archive.ics.uci.edu/static/public/414/ida2016challenge.zip && unzip local-data-warehouse/aps_failure/ida2016challenge.zip -d local-data-warehouse/aps_failure/ && rm local-data-warehouse/aps_failure/ida2016challenge.zip
    """
    curation_comments = """
        - We combined the original training and testing data into a single dataset.
        - We renamed the target feature to "AirPressureSystemFailure".
        - We converted "na" strings to real NaN/missing values, making the data numeric.
        - Anomaly: we cannot determine the data types of the features.
        - Anomaly: some features are bins of histograms (see original data description).
        - Metric: the challenge's cost matrix, scored from probabilities by the least expected cost rather than on hard labels (AI choice, 2026-10-21).
        - Copies of one read-out dropped, the same truck grouped (2026-11-12, Andrej; Review issue 1, option cg). Two
          rows are linked when they share at least 5 values that 2 to 5 rows hold in their column and agree in many of
          the 170 counters (two missing cells count as equal). With every counter shuffled within its class (10 draws),
          no pair shares 5 such values and none agrees on more than 68 counters; in the data 17,461 pairs do.
          - 140 counters or more (13,409 pairs): one read-out copied. 106 non-zero values match at the median (a random
            row's best match among the rows not linked to it: 5, 99th percentile 19) and one cell differs, mostly
            `bx_000`, by 0.012% at the median. All 133 such pairs with a failure are two failures; a model that never
            sees a truck's copies predicts about 93 of these partners from their own counters. One row of each cluster
            stays, the first in file order (training file first): 12,063 rows go (115 failures, 8.4% of them; 11,948
            other trucks, 16.0%), leaving 63,937 rows with 1,260 failures; the failure share moves from 1.81% to 1.97%.
          - 60 to 139 counters (3,966 pairs): probably the same truck read again, not a copy (47 to 81 cells differ at
            the median); the label is the same in every pair (133 failure pairs) and `aa_000` equal in 84% to 93%. The
            rows are one group, `truck`: the clusters of the links at 60 counters or more, found on the kept rows
            (where a value that several copies held becomes rare: 94 more links) and on all 76,000 rows (so a link
            through a dropped copy still joins). 63,937 rows in 61,466 trucks (2,200 with 2 to 5 rows); no truck
            carries two labels. Below 60 counters (86 pairs, one with two labels) rows stay apart.
          - 368 rows with 100 or more blank counters (4 failures) agree with each other on blanks only, share no rare
            value and stay: look-alikes, not copies.
          - 4,458 pairs of copies sit across the challenge's two files, so its own split shared trucks.
          - Effect (untuned LightGBM, 3 folds, 2 seeds, the challenge's cost at its threshold; Slurm 1379970 and
            1379994): test rows with a linked row in training, 25.2% under random folds on all 76,000 rows (cost per
            row 1.145), 5.1% with one row per copied read-out and random folds (1.530), 0.05% split by truck (1.625;
            1.539 with each truck counted once).
        - Time basis: ForcedGroupedFromTemporal: failed trucks read out over a period Scania does not state; the release
          has no date, and the challenge's two files are not shown to be two periods (near copies across them have the
          larger counters in the test file in 2,237 pairs, the smaller in 2,220), and the one counter that changes
          between copies, `bx_000`, is a cumulative usage counter that moves by a small step in either direction, no
          clock. Which component fails can move with season and fleet, so whole trucks held out stand in for the
          trucks to come. Not tested: trucks read out later than the training trucks, which a dated release (as
          `scania_component_x`) would allow.
    """

    # Task
    target = TARGET
    problem_type = "binary_classification"
    metric = Metric.source(
        "cost_matrix",
        original=("Total cost = Cost_1 * #false positives + Cost_2 * #false negatives (IDA 2016 Industrial Challenge)"),
        reference=(
            "https://web.archive.org/web/20161011/http://ida2016.blogs.dsv.su.se/ ; UCI "
            "https://doi.org/10.24432/C5V60Q (aps_failure_description.txt)"
        ),
        definition=(
            "mean cost per truck: 10 per false alarm (needless check), 500 per missed APS failure; from "
            "probabilities, predicted pos when p(pos) > 10/510"
        ),
        params={"labels": ["neg", "pos"], "matrix": [[0, 10], [500, 0]], "prediction": "proba"},
    )

    # Splits: whole trucks held out
    grouping = Grouping(
        on="truck",
        labels="per_group",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a truck as the data show it: the rows linked by at least 5 shared rare values and agreement on
            at least 60 of the 170 counters, probably the same truck read again (curation notes). A workshop meets each
            failed truck once and decides from its counters (the IDA 2016 Industrial Challenge's use case, a check of
            the air pressure system), so whole trucks are held out. Each row is one prediction, made from its own
            counters; no truck's rows carry two labels.
        """,
    )
    splits_comment = """
        Stratified grouped 3-fold cross-validation over the 61,466 trucks with 3 repeats: a truck's rows stay on one
        side, and the folds are drawn over trucks, stratified by label (no truck carries two labels). Each test fold
        holds 20,488 or 20,489 trucks, about 21,300 rows and about 420 failures. 0.05% of the test rows keep a linked
        row in training (a pair sharing 5 rare values but fewer than 60 equal counters, left apart), against 25% under
        random folds on all 76,000 rows. The challenge's own split held out its last 16,000 rows, with 4,458 pairs of
        copies across its two files; the files have no dates for a temporal split.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # remove the leading text before the header form both the training and test data.
        df = pd.concat(
            [
                pd.read_csv(f"{raw_dir}/to_uci/aps_failure_training_set.csv", skiprows=20, na_values="na"),
                pd.read_csv(f"{raw_dir}/to_uci/aps_failure_test_set.csv", skiprows=20, na_values="na"),
            ]
        )
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.reset_index(drop=True).rename(columns={"class": TARGET})
        values = df.drop(columns=[TARGET]).to_numpy(dtype=np.float64)
        a, b, agree = _linked_pairs(values)
        copies = _clusters(len(df), a[agree >= COPY_COUNTERS], b[agree >= COPY_COUNTERS])
        trucks_all_rows = _clusters(len(df), a[agree >= TRUCK_COUNTERS], b[agree >= TRUCK_COUNTERS])
        # one row per copied read-out: the first in file order (the training file comes first)
        keep = np.flatnonzero(~pd.Series(copies).duplicated().to_numpy())
        df = df.iloc[keep].reset_index(drop=True).copy()  # .copy() joins the read blocks
        # the same truck: links at 60 counters on the kept rows (where a value several copies held becomes rare), and
        # on all rows (a link through a dropped copy), each kept row joined to the first kept row of its cluster there
        ka, kb, kagree = _linked_pairs(values[keep])
        first = pd.Series(np.arange(len(keep))).groupby(trucks_all_rows[keep]).transform("first").to_numpy()
        link = kagree >= TRUCK_COUNTERS
        df["truck"] = _clusters(len(keep), np.r_[ka[link], np.arange(len(keep))], np.r_[kb[link], first])
        return df
