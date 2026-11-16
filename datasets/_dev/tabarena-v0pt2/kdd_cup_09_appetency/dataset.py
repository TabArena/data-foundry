"""Curated dataset definition for `kdd_cup_09_appetency` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode

N_NUMERIC = 14740  # Var1-Var14740 numeric, Var14741-Var15000 categorical
GENERATED_COLUMNS = ["Var5963", "Var11750"]


class KddCup09Appetency(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a customer of the French telecom operator Orange buy a new product or service?",
        use_case=(
            "Orange's marketing decides which customers to approach with an offer for a new product or service (the "
            "customer-relationship task of the KDD Cup 2009)."
        ),
        row="One Orange customer (50,000 customers, the competition's large training set, 2009).",
        predicted=(
            "Whether the customer bought the new product or service (1.8% did); the source states no time window."
        ),
        known=(
            "The competition's 15,000 unnamed features (its large version) less empty, constant, copied and two "
            "generated columns: 12,887, of them 12,729 numeric (mostly sparse counts) and 158 categorical, with hidden "
            "meanings and many missing values."
        ),
        split="Random customers of the same database extract.",
        fit="approximate",
        fit_reason=(
            "The features are anonymised, so it cannot be checked that they were known before the purchase, and the "
            "label has no stated window."
        ),
    )

    # Dataset
    unique_name = "kdd_cup_09_appetency"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://kdd.org/kdd-cup/view/kdd-cup-2009/Data",
            license="Public Domain",
            year="2009",
            bibtex=r"""
                @inproceedings{guyon2009analysis,
                  title={Analysis of the kdd cup 2009: Fast scoring on a large orange customer database},
                  author={Guyon, Isabelle and Lemaire, Vincent and Boull{\'e}, Marc and Dror, Gideon and Vogel, David},
                  booktitle={KDD-Cup 2009 Competition},
                  pages={1--22},
                  year={2009},
                  organization={PMLR}
                }
            """,
        ),
    )
    data_tags = ("Anonymized",)
    download_description = """
        We download the large training data (five zipped chunks, kept zipped) and its appetency labels from the KDD
        challenge website:

        mkdir -p local-data-warehouse/kdd_cup_09_appetency && for k in 1 2 3 4 5; do wget -P local-data-warehouse/kdd_cup_09_appetency https://kdd.org/cupfiles/KDDCupData/2009/orange_large_train.data.chunk$k.zip; done && wget -P local-data-warehouse/kdd_cup_09_appetency https://kdd.org/cupfiles/KDDCupData/2009/orange_large_train_appetency.labels
    """
    curation_comments = """
        - The large training data (2026-11-11): the same 50,000 customers and appetency labels (890 buyers) as the
          cup's small set, with all 15,000 features Orange released (Var1-Var14740 numeric, Var14741-Var15000
          categorical); the small set's 230 are a subset, reshuffled and renamed (Guyon et al. 2009, Sec. 2). On the
          same customers, LightGBM scores ROC AUC 0.877 on the large set's columns against 0.820 on the small set's
          (5-fold CV x 3). The rows come in another order than the small set's, with their own labels file.
        - We use appetency as label.
        - Empty and constant columns dropped (CLEAN-5): 109 all missing, 1,422 with one value in every row. The 50
          columns with one value and missing rows are presence flags and stay (as in the small set).
        - Copied columns dropped (CLEAN-5): 580 columns are a one-to-one relabelling (categorical) or a constant
          multiple (numeric) of an earlier column, with the same rows missing; the first of each group stays. Each is
          confirmed against its group's first column (same missing and zero rows, ratio constant to 0.1%). 544 of them
          sit in the 389 groups among columns with two or more values; 24 more are scaled copies that a float32 check
          missed; 12 are presence flags missing in the same rows as another flag. The seven copies found among the
          small set's columns (`Var220`, `Var222` of `Var198`, `Var214` of `Var200`, `Var156`, `Var91`, `Var128`,
          `Var105` of `Var66`, `Var71`, `Var88`, `Var104`) fall into these groups.
        - Generated columns dropped: `Var5963`, uniform on 0-2, the variable of the cup's artificial toy target
          (Guyon et al. 2009, Sec. 5), and `Var11750`, uniform on 0-9; ROC AUC alone 0.511 and 0.501, Kolmogorov-Smirnov
          distance to uniform 0.004 (the next column 0.16). The small set's third such column, `Var57`, has no match in
          the large set.
        - 12,887 features remain, 12,729 numeric and 158 categorical; the median numeric column is 99.7% zeros, and
          about half are counts. The width is the form Orange's platform gave every marketing task, not added probes.
        - Anomaly: the feature names and categorical feature values have no semantic meaning.
        - Anomaly: this dataset has many missing values.
        - The target (2026-11-01, CLEAN-25): `Appetency` ships its classes as words (1 is the event). Binary: "Yes" is
          the event, the class that sorts second, so it is the metrics' positive class.
        - Time basis: DelayedTarget: one extract of Orange's customer datamart (date not stated, before mid-2009),
          100,000 customers resampled toward the labels and split at random by the host; the target, appetency, is read
          as a purchase of a new product or service after the scoring date, as the marketing use case needs. Every
          customer was taken in the same extract and labelled over the same window, so no test row is later than a
          training row and the random split is IID. The label window and the features' windows are not stated and the
          features are masked, so neither the closed window nor the features' timing can be checked. Not tested: the
          next campaign.
    """

    accepted_check_warnings = {
        "dataset_constant_column": "Presence flags: one value or missing, as Orange released them.",
        "dataset_pure_feature_value": "Segments without buyers at a 1.8% base rate; no column documentation to check, "
        "the host masked the features.",
    }

    # Task
    target = "Appetency"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original=("AUC (area under the ROC curve), per task; the ranking averaged churn, appetency and up-selling AUC"),
        reference=(
            "Guyon et al. 2009, Analysis of the KDD Cup 2009, JMLR W&CP 7; https://kdd.org/kdd-cup/view/kdd-cup-2009"
        ),
        definition="ROC AUC of the appetency score on the test customers.",
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        # the large training set: five zipped chunks of 10,000 customers, the first with the header; Var1-Var14740
        # numeric, Var14741-Var15000 categorical (KDD Cup 2009 data page)
        names = [f"Var{i}" for i in range(1, 15001)]
        dtypes = {name: (float if i < N_NUMERIC else str) for i, name in enumerate(names)}
        parts = []
        for k in range(1, 6):
            with zipfile.ZipFile(raw_dir / f"orange_large_train.data.chunk{k}.zip") as z, z.open(z.namelist()[0]) as f:
                parts.append(
                    pd.read_csv(f, sep="\t", header=0 if k == 1 else None, names=names, dtype=dtypes, low_memory=False)
                )
        df = pd.concat(parts, ignore_index=True)
        df_y = pd.read_csv(raw_dir / "orange_large_train_appetency.labels", header=None)
        assert len(df) == len(df_y) == 50_000
        return {"df": df, "df_y": df_y}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw["df"]
        # empty and constant columns (CLEAN-5): all missing, or one value in every row; a column with one value and
        # missing rows is a presence flag and stays
        df = df.loc[:, df.nunique(dropna=False) > 1]
        # exact or scaled copies of an earlier column (CLEAN-5); the first of each group stays
        df = df.drop(columns=copied_columns(df))
        # generated by the host, uniform with no signal: Var5963 is the variable of the cup's artificial toy target
        df = df.drop(columns=GENERATED_COLUMNS)
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        y = decode(pd.DataFrame({self.target: raw["df_y"][0].to_numpy()}), {self.target: {"-1": "No", "1": "Yes"}})
        return pd.concat([df, y], axis=1)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[c for c in df.columns if c != self.target and int(c[3:]) > N_NUMERIC])


def copied_columns(df: pd.DataFrame) -> list[str]:
    """The columns that copy an earlier one: a categorical whose levels match another's one to one in the same rows
    (a relabelling), a numeric equal to another times a constant, with the same rows missing.

    Candidates share a key (first-appearance codes; values divided by the first nonzero one, to 5 significant digits),
    and each is confirmed against the group's first column: same missing rows, same zero rows, constant ratio.
    """
    first: dict[bytes, str] = {}
    copies = []
    for col in df.columns:
        s = df[col]
        if int(col[3:]) > N_NUMERIC:
            codes = pd.factorize(s)[0]
            key = b"c" + hashlib.sha256(codes.tobytes()).digest()
            if key in first:
                assert (pd.factorize(df[first[key]])[0] == codes).all()
                copies.append(col)
            else:
                first[key] = col
            continue
        x = s.to_numpy(dtype=float)
        nonzero = x[~np.isnan(x) & (x != 0)]
        v = x / nonzero[0] if len(nonzero) else x
        with np.errstate(divide="ignore", invalid="ignore"):
            e = np.where((v == 0) | np.isnan(v), 0, np.floor(np.log10(np.abs(v))))
            mantissa = np.where(np.isnan(v), 99, np.round(v / 10**e, 4))
        key = b"n" + hashlib.sha256(np.concatenate([mantissa, e]).tobytes()).digest()
        if key not in first:
            first[key] = col
        elif _scaled_copy(x, df[first[key]].to_numpy(dtype=float)):
            copies.append(col)
    return copies


def _scaled_copy(x: np.ndarray, base: np.ndarray) -> bool:
    """Whether x is base times one constant: same missing rows, same zero rows, constant ratio elsewhere."""
    if not (np.array_equal(np.isnan(x), np.isnan(base)) and np.array_equal(x == 0, base == 0)):
        return False
    filled = ~np.isnan(x) & (x != 0)
    if not filled.any():
        return True
    ratio = x[filled] / base[filled]
    return bool(np.allclose(ratio, np.median(ratio), rtol=1e-3, atol=0))
