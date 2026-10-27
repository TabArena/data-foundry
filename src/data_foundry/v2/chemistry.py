"""Molecules as numbers: RDKit's 2D descriptors of a SMILES column, the one way v2 definitions ship a structure.

A SMILES string holds the whole structure, but a tabular model reads it as text and gains nothing over descriptors
computed from it (the working copy's CHANGELOG, 2026-10-14). A definition with a SMILES column therefore adds
``rdkit_descriptors(df[column])`` in ``_clean`` and drops the string, so every method gets the molecule in the same
tabular form. RDKit is in the ``build`` extra, pinned, because descriptor values can change between releases.
``murcko_scaffolds`` gives the scaffolds of the same column, and ``scaffold_groups`` the groups of a scaffold-grouped
split (``Grouping(on=...)``) built from them.

Mordred, not used: its open 2D descriptors (``mordredcommunity`` 2.0.7, BSD-3, 1,613 descriptors, many of them
Dragon's) run with the pinned RDKit. On qsar_bioconcentration (2026-10-26) they lowered macro ROC AUC: RDKit's
descriptors and the logKOW scored 0.759 (random forest) and 0.765 (LightGBM) over 3 x 10 folds, and adding Mordred's
1,220 descriptors that do not copy an RDKit one 0.746 and 0.745 (paired -0.013 and -0.020). Every SMILES dataset
ships RDKit's descriptors alone (CLEAN-24); revisit Mordred for all of them at once, with a gain measured on several.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from data_foundry.v2._optional import import_build_dependency
from data_foundry.v2.dataset import DatasetDefinitionError

RDKIT_VERSION = "2026.03.6"
"""The RDKit release the descriptors are computed with (pinned in the ``build`` extra); another version is an
error."""


def _molecules(smiles: pd.Series) -> list:
    """The RDKit molecule of each SMILES.

    Raises:
        DatasetDefinitionError: Another RDKit version is installed, or a SMILES does not parse.
    """
    rdkit = import_build_dependency("rdkit")
    if rdkit.__version__ != RDKIT_VERSION:
        msg = f"The SMILES descriptors need RDKit {RDKIT_VERSION}, found {rdkit.__version__}."
        raise DatasetDefinitionError(msg)
    chem = import_build_dependency("rdkit.Chem")
    import_build_dependency("rdkit.RDLogger").DisableLog("rdApp.*")
    molecules = [chem.MolFromSmiles(s) for s in smiles]
    invalid = [s for s, molecule in zip(smiles, molecules, strict=True) if molecule is None]
    if invalid:
        msg = f"RDKit cannot parse {len(invalid)} SMILES, for example {invalid[:3]}."
        raise DatasetDefinitionError(msg)
    return molecules


def rdkit_descriptors(smiles: pd.Series, *, prefix: str = "rdkit_") -> pd.DataFrame:
    """RDKit's 2D descriptors of each SMILES as ``<prefix><name>`` columns, on the index of ``smiles``.

    Values RDKit cannot compute for a molecule (partial charges, BCUT descriptors) are missing. Descriptors that are
    constant over the molecules or an exact copy of an earlier descriptor are left out. ``Ipc`` (the information
    content of the molecular graph) grows exponentially with the molecule, beyond the float32 range for large ones
    (6e166 in qsar_oral_toxicity), so it ships as ``Ipc_log10`` = log10(1 + Ipc), the same order on a usable scale.

    Raises:
        DatasetDefinitionError: Another RDKit version is installed, or a SMILES does not parse.
    """
    molecules = _molecules(smiles)
    descriptors = import_build_dependency("rdkit.Chem.Descriptors")
    rows = [descriptors.CalcMolDescriptors(molecule) for molecule in molecules]
    out = pd.DataFrame(rows, index=smiles.index).astype("float64")
    if "Ipc" in out.columns:
        out.insert(out.columns.get_loc("Ipc"), "Ipc_log10", np.log10(1 + out.pop("Ipc")))
    out = out.add_prefix(prefix)
    out = out.where(np.isfinite(out))
    out = out.loc[:, out.nunique(dropna=False).gt(1)]
    return out.loc[:, ~out.T.duplicated()]


MAX_SCAFFOLD_SHARE = 0.1
"""A scaffold that holds more molecules than this share is no series to hold out (SPLIT-31)."""


def murcko_scaffolds(smiles: pd.Series) -> pd.Series:
    """The Bemis-Murcko scaffold of each SMILES (its ring systems and the chains linking them, atom and bond types
    kept, stereochemistry dropped) as canonical SMILES, on the index of ``smiles``.

    A molecule without a ring has the empty scaffold ``""``; a definition that groups on the scaffolds decides what
    such molecules share (Bemis and Murcko 1996, J Med Chem 39(15):2887-2893).

    Raises:
        DatasetDefinitionError: Another RDKit version is installed, or a SMILES does not parse.
    """
    molecules = _molecules(smiles)
    scaffold = import_build_dependency("rdkit.Chem.Scaffolds.MurckoScaffold")
    out = [scaffold.MurckoScaffoldSmiles(mol=molecule, includeChirality=False) for molecule in molecules]
    return pd.Series(out, index=smiles.index, dtype="string", name="scaffold")


def scaffold_groups(smiles: pd.Series, *, max_share: float = MAX_SCAFFOLD_SHARE) -> pd.Series:
    """The group of each molecule in a scaffold-grouped split (SPLIT-31), on the index of ``smiles``.

    Molecules that share a Bemis-Murcko scaffold form one group. A molecule without a ring is a group of its own, and
    so is each molecule of a scaffold that holds more than ``max_share`` of the molecules (in practice the bare
    benzene ring: 34% of qsar_bioconcentration, 18% of qsar_oral_toxicity), which is no series and would leave folds of
    very unequal size. A single molecule's group is ``"single: <its SMILES>"``.

    Raises:
        DatasetDefinitionError: Another RDKit version is installed, or a SMILES does not parse.
    """
    scaffold = murcko_scaffolds(smiles)
    share = scaffold.map(scaffold.value_counts(normalize=True))
    alone = scaffold.eq("") | share.gt(max_share)
    return scaffold.mask(alone, "single: " + smiles.astype("string")).rename("scaffold")
