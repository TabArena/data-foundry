"""Tests for the SMILES descriptors and scaffolds (``data_foundry.v2.chemistry``)."""

from __future__ import annotations

import pandas as pd
import pytest
from data_foundry.v2 import (
    DatasetDefinitionError,
    Encoding,
    chemistry,
    murcko_scaffolds,
    rdkit_descriptors,
    scaffold_groups,
)

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


def test_encode_smiles_gives_every_descriptor_the_maccs_keys_and_the_ecfp4_counts_per_molecule() -> None:
    """The recommended encoding: the same columns for any molecules, one row per value, each distinct SMILES once."""
    smiles = pd.Series(["CCO", "c1ccccc1", "CCO"], index=[7, 8, 9])
    out = chemistry.encode_smiles(smiles)

    assert list(out.index) == [7, 8, 9]
    maccs = [c for c in out.columns if c.startswith("maccs_")]
    descriptors = [c for c in out.columns if c.startswith("rdkit_")]
    assert maccs == [f"maccs_{i}" for i in range(1, 167)]
    ecfp4 = [c for c in out.columns if c.startswith("ecfp4_")]
    assert ecfp4 == [f"ecfp4_{i}" for i in range(1024)]
    assert len(descriptors) + len(maccs) + len(ecfp4) == out.shape[1]
    assert (out[ecfp4].dtypes == "int16").all()
    assert out.loc[7, ecfp4].sum() > 0
    assert "rdkit_Ipc_log10" in descriptors
    assert "rdkit_Ipc" not in descriptors
    assert (out[maccs].dtypes == "int8").all()
    assert (out[descriptors].dtypes == "float64").all()
    pd.testing.assert_series_equal(out.loc[7], out.loc[9], check_names=False)
    # no column is dropped for being constant: two molecules give the same columns as many
    assert list(chemistry.encode_smiles(pd.Series(["CCO"])).columns) == list(out.columns)


def test_encode_smiles_prefix_and_missing_values() -> None:
    """A prefix names the columns; a missing SMILES gives a row of missing values (nullable MACCS keys)."""
    out = chemistry.encode_smiles(pd.Series(["CCO", None], dtype="string"), prefix="SMILES__")

    assert out.columns[0].startswith("SMILES__rdkit_")
    assert out.iloc[1].isna().all()
    assert out["SMILES__maccs_1"].dtype == "Int8"
    assert out["SMILES__ecfp4_0"].dtype == "Int16"


def test_the_default_encoding_names_rdkit_and_its_revision() -> None:
    """The spec id keys a cache: the encoding's name, the pinned RDKit release and the revision."""
    encoding = chemistry.DEFAULT_SMILES_ENCODING

    assert encoding.id == f"rdkit2d-maccs-ecfp4-rdkit{chemistry.RDKIT_VERSION}-r1"
    with pytest.raises(ValueError, match="Unknown SMILES encoding"):
        chemistry.encode_smiles(pd.Series(["CCO"]), Encoding(kind="smiles", name="other", revision=1, description=""))


def test_canonical_smiles_keeps_fragments_and_stereochemistry_unless_asked() -> None:
    """Every fragment and the stereo marks stay by default; equal molecules get one string; missing stays missing."""
    smiles = pd.Series(["N[C@@H](C)C(=O)O.Cl", "C[C@H](N)C(=O)O", "OCC", None], index=[3, 4, 5, 6], name="SMILES")
    out = chemistry.canonical_smiles(smiles)

    assert out.dtype == "string"
    assert out.name == "SMILES"
    assert list(out.index) == [3, 4, 5, 6]
    assert "Cl" in out[3]
    assert "@" in out[4]
    assert out[5] == "CCO"
    assert pd.isna(out[6])
    stripped = chemistry.canonical_smiles(smiles, largest_fragment=True)
    assert stripped[3] == stripped[4] == out[4]
    flat = chemistry.canonical_smiles(pd.Series(["C[C@H](N)C(=O)O", "C[C@@H](N)C(=O)O"]), stereo=False)
    assert flat[0] == flat[1]
    assert "@" not in flat[0]


def test_invalid_smiles_lists_the_values_rdkit_cannot_parse() -> None:
    """Each unparseable value once; missing values are not checked."""
    assert chemistry.invalid_smiles(pd.Series(["CCO", "C1CC", None, "C1CC"])) == ["C1CC"]
