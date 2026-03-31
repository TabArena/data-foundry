from __future__ import annotations

import pandas as pd
import pytest
from data_foundry.utils.checksum import encode_dataset, encode_pydantic_metadata


def test_encode_pydantic_metadata_returns_bytes():
    result = encode_pydantic_metadata({"key": "value"})
    assert isinstance(result, bytes)


def test_encode_pydantic_metadata_is_deterministic():
    obj = {"a": 1, "b": [1, 2, 3], "c": None}
    assert encode_pydantic_metadata(obj) == encode_pydantic_metadata(obj)


def test_encode_pydantic_metadata_different_inputs_differ():
    a = encode_pydantic_metadata({"x": 1})
    b = encode_pydantic_metadata({"x": 2})
    assert a != b


def test_encode_pydantic_metadata_key_order_stable():
    # json.dumps with sort_keys=True should produce the same bytes regardless of insertion order
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 2, "a": 1}
    assert encode_pydantic_metadata(d1) == encode_pydantic_metadata(d2)


def test_encode_pydantic_metadata_nested_object():
    obj = {"outer": {"inner": [1, 2, 3]}}
    result = encode_pydantic_metadata(obj)
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_encode_pydantic_metadata_empty_dict():
    result = encode_pydantic_metadata({})
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ({"k": 1}, {"k": 1, "extra": 2}),
        ({"k": "str"}, {"k": 42}),
        ([], [1]),
        (None, {}),
    ],
)
def test_encode_pydantic_metadata_distinguishes_types(a, b):
    assert encode_pydantic_metadata(a) != encode_pydantic_metadata(b)


# --- encode_dataset ---


@pytest.fixture
def simple_df() -> pd.DataFrame:
    return pd.DataFrame({"x": [1, 2, 3], "y": [4.0, 5.0, 6.0]})


def test_encode_dataset_returns_bytes(simple_df):
    result = encode_dataset(simple_df)
    assert isinstance(result, bytes)


def test_encode_dataset_is_deterministic(simple_df):
    assert encode_dataset(simple_df) == encode_dataset(simple_df)


def test_encode_dataset_different_values_differ():
    df1 = pd.DataFrame({"x": [1, 2, 3]})
    df2 = pd.DataFrame({"x": [1, 2, 4]})
    assert encode_dataset(df1) != encode_dataset(df2)


def test_encode_dataset_different_column_name_differs():
    df1 = pd.DataFrame({"x": [1, 2, 3]})
    df2 = pd.DataFrame({"y": [1, 2, 3]})
    assert encode_dataset(df1) != encode_dataset(df2)


def test_encode_dataset_different_dtype_differs():
    df_int = pd.DataFrame({"x": [1, 2, 3]})
    df_float = df_int.astype(float)
    assert encode_dataset(df_int) != encode_dataset(df_float)


def test_encode_dataset_different_shape_differs():
    df1 = pd.DataFrame({"x": [1, 2, 3]})
    df2 = pd.DataFrame({"x": [1, 2, 3, 4]})
    assert encode_dataset(df1) != encode_dataset(df2)


def test_encode_dataset_different_column_order_differs():
    df1 = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    df2 = pd.DataFrame({"y": [3, 4], "x": [1, 2]})
    assert encode_dataset(df1) != encode_dataset(df2)


def test_encode_dataset_copy_equals_original(simple_df):
    assert encode_dataset(simple_df) == encode_dataset(simple_df.copy())


def test_encode_dataset_empty_dataframe():
    df = pd.DataFrame({"x": pd.Series([], dtype=int)})
    result = encode_dataset(df)
    assert isinstance(result, bytes)
    assert len(result) > 0
