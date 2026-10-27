"""Tests for the SMILES descriptors and scaffolds (``data_foundry.v2.chemistry``)."""

from __future__ import annotations

import pandas as pd
import pytest
from data_foundry.v2 import DatasetDefinitionError, chemistry, murcko_scaffolds, rdkit_descriptors, scaffold_groups

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


def test_ipc_ships_on_a_log_scale() -> None:
    """``Ipc`` overflows float32 for large molecules, so it is replaced by log10(1 + Ipc)."""
    smiles = pd.Series(["CCO", "c1ccccc1", "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)O"])
    out = rdkit_descriptors(smiles)

    assert "rdkit_Ipc" not in out.columns
    assert out["rdkit_Ipc_log10"].between(0, 38).all()


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


def test_scaffolds_keep_rings_and_linkers_and_drop_side_chains() -> None:
    """Toluene and benzoic acid share the benzene scaffold, pyridine keeps its nitrogen, ethanol has none."""
    smiles = pd.Series(["Cc1ccccc1", "OC(=O)c1ccccc1", "c1ccncc1", "CCO", "c1ccccc1CCc1ccccc1"], index=[3, 4, 5, 6, 7])
    out = murcko_scaffolds(smiles)

    assert list(out.index) == [3, 4, 5, 6, 7]
    assert out.dtype == "string"
    assert list(out) == ["c1ccccc1", "c1ccccc1", "c1ccncc1", "", "c1ccc(CCc2ccccc2)cc1"]


def test_scaffolds_drop_stereochemistry() -> None:
    """Stereoisomers share one scaffold."""
    out = murcko_scaffolds(pd.Series(["C[C@H]1CC[C@@H](C)C1c1ccccc1", "C[C@@H]1CC[C@@H](C)C1c1ccccc1"]))

    assert out.iloc[0] == out.iloc[1]


def test_a_scaffold_smiles_that_does_not_parse_is_an_error() -> None:
    """A SMILES RDKit cannot parse stops the definition, as for the descriptors."""
    with pytest.raises(DatasetDefinitionError, match="cannot parse 1 SMILES"):
        murcko_scaffolds(pd.Series(["CCO", "C1CC"]))


def test_scaffold_groups_keep_series_together_and_ring_less_or_common_scaffolds_apart() -> None:
    """Biphenyls share a group; ethanol, methanol and the benzenes (here 3 of 6) each get one of their own."""
    smiles = pd.Series(["c1ccccc1Cl", "Cc1ccccc1", "Oc1ccccc1", "Clc1ccc(cc1)-c1ccccc1", "c1ccc(cc1)-c1ccccc1", "CCO"])
    out = scaffold_groups(smiles, max_share=0.4)

    assert out.iloc[3] == out.iloc[4] == "c1ccc(-c2ccccc2)cc1"
    assert list(out.iloc[[0, 1, 2, 5]]) == [f"single: {s}" for s in smiles.iloc[[0, 1, 2, 5]]]
    assert out.nunique() == 5


def test_scaffold_groups_keep_a_scaffold_below_the_share_together() -> None:
    """With a higher share the benzenes form one group."""
    smiles = pd.Series(["c1ccccc1Cl", "Cc1ccccc1", "Oc1ccccc1", "Clc1ccc(cc1)-c1ccccc1", "c1ccc(cc1)-c1ccccc1", "CCO"])
    out = scaffold_groups(smiles, max_share=0.6)

    assert out.iloc[0] == out.iloc[1] == out.iloc[2] == "c1ccccc1"
