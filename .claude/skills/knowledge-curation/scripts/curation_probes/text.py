"""Model inputs for the probes: a table's columns as numbers, and text columns as TF-IDF + SVD components.

Tooling-independent (pandas, NumPy and scikit-learn); the probes of this package share these encoders, so a column
enters every probe the same way.

* ``features``: the numeric model inputs of a frame. Categoricals enter as their codes, datetimes and periods as
  seconds, and a missing value as the column's median (0 for a column without values); string columns are left out
  and returned by name.
* ``encode_text``: each text column as ``TEXT_COMPONENTS`` TF-IDF + SVD components fitted on the train rows only:
  words for prose, character 2- to 5-grams for strings that are mostly one token (a SMILES, a code, a URL), where
  words would only match whole repeated values.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

TEXT_COMPONENTS = 16
MAX_TEXT_COLUMNS = 30
ONE_TOKEN_SHARE = 0.9
"""A text column whose values are a single token in at least this share of rows is encoded by character n-grams."""


def features(df: pd.DataFrame, drop: list[str]) -> tuple[pd.DataFrame, list[str], list[str]]:
    """Numeric model inputs (columns ``f0``, ``f1``, ...), their original names, and the text columns."""
    X = df.drop(columns=[c for c in drop if c in df.columns])
    text = list(X.select_dtypes(include=["string", "object"]).columns)
    X = X.drop(columns=text)
    for col in X.columns:
        if isinstance(X[col].dtype, pd.CategoricalDtype):
            X[col] = X[col].cat.codes.replace(-1, np.nan)
        elif pd.api.types.is_datetime64_any_dtype(X[col]):
            X[col] = X[col].astype("int64") // 10**9
        elif isinstance(X[col].dtype, pd.PeriodDtype):
            X[col] = X[col].dt.to_timestamp().astype("int64") // 10**9
    X = X.astype(float)
    names = list(X.columns)
    X = X.fillna(X.median()).fillna(0.0)
    X.columns = [f"f{i}" for i in range(X.shape[1])]
    return X, names, text


def text_vectorizer(values: np.ndarray) -> TfidfVectorizer:
    """Word TF-IDF for prose; character 2- to 5-grams when most values are one token (SMILES, codes, URLs)."""
    sample = pd.Series(values[:5_000], dtype="string").fillna("")
    one_token = float((~sample.str.strip().str.contains(r"\s")).mean()) if len(sample) else 0.0
    if one_token >= ONE_TOKEN_SHARE:
        return TfidfVectorizer(
            analyzer="char", ngram_range=(2, 5), max_features=20_000, min_df=2, sublinear_tf=True, dtype=np.float32
        )
    return TfidfVectorizer(max_features=20_000, min_df=2, sublinear_tf=True, dtype=np.float32)


def encode_text(
    df: pd.DataFrame, text: list[str], train: np.ndarray, test: np.ndarray
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, list[str]]]:
    """Each text column as TF-IDF + SVD components fitted on the train rows; the column blocks by source column."""
    tr_parts, te_parts, blocks = [], [], {}
    for k, col in enumerate(text[:MAX_TEXT_COLUMNS]):
        values = df[col].astype("string").fillna("").to_numpy(dtype=object)
        try:
            vectorizer = text_vectorizer(values[train])
            a_train = vectorizer.fit_transform(values[train])
        except ValueError:  # no term occurs twice: nothing to encode
            continue
        n = min(TEXT_COMPONENTS, a_train.shape[1] - 1)
        if n < 1:
            continue
        svd = TruncatedSVD(n_components=n, random_state=0)
        cols = [f"t{k}_{j}" for j in range(n)]
        tr_parts.append(pd.DataFrame(svd.fit_transform(a_train), columns=cols))
        te_parts.append(pd.DataFrame(svd.transform(vectorizer.transform(values[test])), columns=cols))
        blocks[col] = cols
    if not tr_parts:
        return pd.DataFrame(index=range(len(train))), pd.DataFrame(index=range(len(test))), {}
    return pd.concat(tr_parts, axis=1), pd.concat(te_parts, axis=1), blocks
