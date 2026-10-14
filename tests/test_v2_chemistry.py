"""Tests for the SMILES descriptors (``data_foundry.v2.chemistry``)."""

from __future__ import annotations

import pandas as pd
import pytest
from data_foundry.v2 import DatasetDefinitionError, chemistry, rdkit_descriptors

pytest.importorskip("rdkit")


def test_descriptors_keep_the_index_and_leave_out_constant_and_copied_columns() -> None:
    """One float column per descriptor that varies, on the index of the SMILES."""
    smiles = pd.Series(["CCO", "c1ccccc1", "CC(=O)O", "CCN"], index=[10, 11, 12, 13])
    out = rdkit_descriptors(smiles)

    assert list(out.index) == [10, 11, 12, 13]
    assert "rdkit_MolWt" in out.columns
    assert all(column.startswith("rdkit_") for column in out.columns)
    assert (out.dtypes == "float64").all()
    assert out.nunique(dropna=False).gt(1).all()
    assert not out.T.duplicated().any()


def test_prefix_names_the_columns() -> None:
    """The prefix is put before each descriptor name."""
    out = rdkit_descriptors(pd.Series(["CCO", "c1ccccc1"]), prefix="")

    assert "MolWt" in out.columns


def test_a_smiles_that_does_not_parse_is_an_error() -> None:
    """A SMILES RDKit cannot parse stops the definition instead of giving a row of missing values."""
    with pytest.raises(DatasetDefinitionError, match="cannot parse 1 SMILES"):
        rdkit_descriptors(pd.Series(["CCO", "C1CC"]))


def test_another_rdkit_version_is_an_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Descriptor values can change between RDKit releases, so only the pinned one computes them."""
    monkeypatch.setattr(chemistry, "RDKIT_VERSION", "0.0.0")
    with pytest.raises(DatasetDefinitionError, match=r"need RDKit 0\.0\.0"):
        rdkit_descriptors(pd.Series(["CCO"]))
