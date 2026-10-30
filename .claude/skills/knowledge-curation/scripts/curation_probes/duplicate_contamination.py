"""Exact training-profile matches by label and multiplicity on actual split positions.

Missing cells compare equal; every selected predictor, including text and dates, is
used without rounding or imputation. Matching profiles do not establish entity identity.
The optional losses are already-computed per-test-row losses, not arbitrary fold metrics.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter

import numpy as np
import pandas as pd


def frame_digest(df: pd.DataFrame) -> str:
    """Bind a saved-loss packet to this ordered frame, column names and semantic dtypes.

    This is a local evidence identity, not a replacement for a container checksum.
    Category labels/order are retained even when their observed values are identical.
    """
    schema = []
    for name, series in df.items():
        item = {"name": str(name), "dtype": str(series.dtype)}
        if isinstance(series.dtype, pd.CategoricalDtype):
            item |= {"categories": [repr(v) for v in series.cat.categories], "ordered": series.cat.ordered}
        schema.append(item)
    digest = hashlib.sha256(json.dumps(schema, sort_keys=True).encode())
    digest.update(pd.util.hash_pandas_object(df, index=False).to_numpy(dtype="<u8").tobytes())
    return digest.hexdigest()


def _positions(values, rows):
    indices = np.asarray(values)
    if indices.ndim != 1 or not np.issubdtype(indices.dtype, np.integer) or not len(indices):
        raise ValueError("Each split side must be a nonempty one-dimensional integer position array.")
    if np.any(indices < 0) or np.any(indices >= rows) or len(np.unique(indices)) != len(indices):
        raise ValueError("Split positions must be unique and within the frame.")
    return indices


def _summary(joint):
    count = sum(joint.values())
    inclusive = {
        "same_label_1": sum(v for (s, _d), v in joint.items() if s == 1),
        "same_label_2plus": sum(v for (s, _d), v in joint.items() if s == 2),
        "different_label_1": sum(v for (_s, d), v in joint.items() if d == 1),
        "different_label_2plus": sum(v for (_s, d), v in joint.items() if d == 2),
        "mixed_same_and_different": sum(v for (s, d), v in joint.items() if s > 0 and d > 0),
        "unmatched": joint[(0, 0)],
        "matched": count - joint[(0, 0)],
    }
    exclusive = {
        "same_only_1": joint[(1, 0)],
        "same_only_2plus": joint[(2, 0)],
        "different_only_1": joint[(0, 1)],
        "different_only_2plus": joint[(0, 2)],
        "mixed_same_and_different": inclusive["mixed_same_and_different"],
        "unmatched": inclusive["unmatched"],
    }

    def shares(counts):
        return {key: {"rows": int(value), "share": value / count if count else None} for key, value in counts.items()}

    return {"test_evaluations": count, "inclusive": shares(inclusive), "exclusive": shares(exclusive)}


def _losses(packet, split, train, test):
    item = packet["folds"][split]
    if not np.array_equal(item["train_indices"], train) or not np.array_equal(item["test_indices"], test):
        raise ValueError("Saved losses must match both ordered train and test positions exactly.")
    values = np.asarray(item["losses"], dtype=float)
    if values.shape != (len(test),) or not np.isfinite(values).all():
        raise ValueError("Saved losses must be finite and contain exactly one value per test row.")
    return values


def _loss_summary(values, matched):
    result = {}
    for name, mask in (("all", np.ones(len(values), dtype=bool)), ("matched", matched), ("unmatched", ~matched)):
        subset = values[mask]
        result[name] = {
            "rows": len(subset),
            "sum": float(subset.sum()),
            "mean": float(subset.mean()) if len(subset) else None,
        }
    return result


def run(df, target, splits, *, features=None, losses=None, include_rows=False) -> dict:
    """Count exact profile matches on every supplied split, with optional aligned losses.

    ``losses`` is a packet with ``frame_digest`` and one ``folds`` entry per split.
    Each entry contains the exact ordered ``train_indices``, ``test_indices`` and
    per-row ``losses`` from one fitted model. Compare subsets descriptively; this
    is neither a grouped retraining experiment nor a causal leakage estimate.
    """
    features = list(features) if features is not None else [c for c in df.columns if c != target]
    if not df.columns.is_unique or not features or len(set(features)) != len(features) or target in features:
        raise ValueError("Choose nonempty, unique predictor columns without the target.")
    if df.empty or df[target].isna().any():
        raise ValueError("The frame must contain observations with nonmissing targets.")
    profiles = pd.MultiIndex.from_frame(df[features]).factorize(sort=False)[0]
    labels = pd.factorize(df[target], sort=False)[0]
    splits = list(splits)
    if not splits:
        raise ValueError("At least one actual split is required.")
    digest = frame_digest(df)
    if losses is not None and (losses["frame_digest"] != digest or len(losses["folds"]) != len(splits)):
        raise ValueError("Saved losses must describe this exact ordered frame and all supplied splits.")
    aggregate, folds = Counter(), []
    pooled_losses, pooled_matched = [], []
    for split, (train_rows, test_rows) in enumerate(splits):
        train, test = _positions(train_rows, len(df)), _positions(test_rows, len(df))
        if np.intersect1d(train, test).size:
            raise ValueError("Train and test positions must be disjoint.")
        counts = Counter(profiles[train])
        pairs = Counter(zip(profiles[train], labels[train], strict=True))
        same = np.array([pairs[(profiles[j], labels[j])] for j in test])
        different = np.array([counts[profiles[j]] for j in test]) - same
        joint = Counter(zip(np.minimum(same, 2), np.minimum(different, 2), strict=True))
        aggregate.update(joint)
        row = {"split": split, "train_rows": len(train), **_summary(joint)}
        if include_rows:
            row["test_indices"] = test.tolist()
            row["same_label_matches"] = same.tolist()
            row["different_label_matches"] = different.tolist()
        if losses is not None:
            values = _losses(losses, split, train, test)
            matched = (same + different) > 0
            row["loss"] = _loss_summary(values, matched)
            pooled_losses.append(values)
            pooled_matched.append(matched)
        folds.append(row)
    result = {
        "rows": len(df),
        "features": features,
        "frame_digest": digest,
        "folds": folds,
        "aggregate": _summary(aggregate),
        "interpretation": "Recorded-profile equality, not verified entity identity. Inclusive categories overlap; "
        "exclusive categories partition test evaluations. Repeats count the same observations again. "
        "Matched/unmatched losses describe different subsets, not causal duplicate-induced optimism.",
    }
    if losses is not None:
        result["pooled_loss"] = _loss_summary(np.concatenate(pooled_losses), np.concatenate(pooled_matched))
    return result
