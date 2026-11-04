"""Tests for the recommended encodings of date, text and SMILES columns (``data_foundry.v2.encodings``)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from data_foundry.v2 import encodings
from data_foundry.v2.encodings import (
    DATETIME_ENCODING,
    TEXT_E5_ENCODING,
    TEXT_TFIDF_ENCODING,
    Encoding,
    encode_datetime,
    encode_text_e5,
    encode_text_tfidf,
    recommended_encodings,
)


def test_the_registry_lists_every_encoding_by_kind_with_its_cache_scope() -> None:
    """One encoding for SMILES and dates, two for text to be compared, seven for spectra (which fit one spectrum
    depends on it); each declares what a cache holds.
    """
    recommended = recommended_encodings()

    assert set(recommended) == {"smiles", "datetime", "text", "spectrum"}
    assert recommended["datetime"] == (DATETIME_ENCODING,)
    assert recommended["text"] == (TEXT_TFIDF_ENCODING, TEXT_E5_ENCODING)
    assert len(recommended["spectrum"]) == 7
    assert all(encoding.kind == kind for kind, specs in recommended.items() for encoding in specs)
    assert (TEXT_TFIDF_ENCODING.scope, TEXT_E5_ENCODING.scope, DATETIME_ENCODING.scope) == ("split", "value", "value")
    assert recommended["smiles"][0].scope == "value"
    assert recommended["smiles"][0].id.startswith("rdkit2d-maccs-ecfp4-rdkit")


def test_the_spec_id_names_the_encoding_the_library_and_the_revision() -> None:
    """The id leaves out a library that is not pinned."""
    assert Encoding(kind="text", name="x", revision=2, description="", scope="value").id == "x-r2"
    assert (
        Encoding(kind="smiles", name="x", revision=1, description="", scope="value", library="rdkit1").id
        == "x-rdkit1-r1"
    )


def test_encode_datetime_uses_skrub_with_the_weekday_and_circular_parts() -> None:
    """BeyondArena's datetime encoding: the year, the total seconds, circular pairs down to the resolution."""
    pytest.importorskip("skrub")
    values = pd.Series(pd.to_datetime(["2024-01-01 10:00", "2024-06-15 23:30", "2025-03-03 00:15"]), name="when")
    values.index = [5, 6, 7]
    out = encode_datetime(values)

    assert list(out.index) == [5, 6, 7]
    assert any("weekday" in c for c in out.columns)
    assert "when_year" in out.columns
    assert {"when_month_circular_0", "when_month_circular_1"} <= set(out.columns)
    assert all(c.startswith("when_") for c in out.columns)
    renamed = encode_datetime(values, prefix="t__")
    assert all(c.startswith("t__") for c in renamed.columns)
    assert len(renamed.columns) == len(out.columns)


def test_encode_text_tfidf_is_fitted_on_the_training_rows_only() -> None:
    """The vocabulary and the SVD come from the train rows; test words unseen in training add nothing."""
    train = pd.Series(["red apple pie", "green apple tart", "red cherry pie", "blue berry jam"] * 5, name="t")
    test = pd.Series(["purple unknown words", "red apple pie"], index=[100, 101])
    out_train, out_test = encode_text_tfidf(train, test, components=3)

    assert list(out_train.columns) == ["tfidf_0", "tfidf_1", "tfidf_2"]
    assert list(out_test.index) == [100, 101]
    np.testing.assert_allclose(out_test.loc[100].to_numpy(), 0.0, atol=1e-7)
    np.testing.assert_allclose(out_test.loc[101].to_numpy(), out_train.iloc[0].to_numpy(), atol=1e-6)


def test_encode_text_tfidf_reads_one_token_values_by_character_ngrams() -> None:
    """Codes and identifiers (one token per value) are compared by their character n-grams."""
    vectorizer = encodings._text_vectorizer(pd.Series(["CCO", "c1ccccc1", "CCN"] * 10))

    assert vectorizer.analyzer == "char"
    assert encodings._text_vectorizer(pd.Series(["a short sentence", "another one here"] * 10)).analyzer == "word"


class _StubModel:
    """Stands in for the sentence-transformer: a value's vector is its length, then zeros; counts the values seen."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.seen: list[str] = []

    def encode(self, texts: list[str], *, batch_size: int, normalize_embeddings: bool) -> np.ndarray:
        del batch_size, normalize_embeddings
        self.seen.extend(texts)
        return np.array([[len(t), 0.0, 1.0] for t in texts])


def test_encode_text_e5_encodes_each_distinct_value_once_with_the_query_prefix() -> None:
    """Each distinct value is encoded once, a missing one as empty text, all with e5's query prefix."""
    models: list[_StubModel] = []

    def factory(name: str) -> _StubModel:
        models.append(_StubModel(name))
        return models[-1]

    values = pd.Series(["ab", None, "ab", "xyz"], index=[1, 2, 3, 4], dtype="string")
    out = encode_text_e5(values, model_factory=factory)

    (model,) = models
    assert model.name == encodings.E5_MODEL
    assert sorted(model.seen) == ["query: ", "query: ab", "query: xyz"]
    assert list(out.index) == [1, 2, 3, 4]
    assert list(out.columns) == ["e5_0", "e5_1", "e5_2"]
    assert out.loc[1, "e5_0"] == out.loc[3, "e5_0"] == len("query: ab")
    assert out.loc[2, "e5_0"] == len("query: ")
