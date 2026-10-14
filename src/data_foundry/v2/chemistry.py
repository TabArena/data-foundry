"""Molecules as numbers: RDKit's 2D descriptors of a SMILES column, the one way v2 definitions ship a structure.

A SMILES string holds the whole structure, but a tabular model reads it as text and gains nothing over descriptors
computed from it (the working copy's CHANGELOG, 2026-10-14). A definition with a SMILES column therefore adds
``rdkit_descriptors(df[column])`` in ``_clean`` and drops the string, so every method gets the molecule in the same
tabular form. RDKit is in the ``build`` extra, pinned, because descriptor values can change between releases.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from data_foundry.v2._optional import import_build_dependency
from data_foundry.v2.dataset import DatasetDefinitionError

RDKIT_VERSION = "2026.03.6"
"""The RDKit release the descriptors are computed with (pinned in the ``build`` extra); another version is an
error."""


def rdkit_descriptors(smiles: pd.Series, *, prefix: str = "rdkit_") -> pd.DataFrame:
    """RDKit's 2D descriptors of each SMILES as ``<prefix><name>`` columns, on the index of ``smiles``.

    Values RDKit cannot compute for a molecule (partial charges, BCUT descriptors) are missing. Descriptors that are
    constant over the molecules or an exact copy of an earlier descriptor are left out.

    Raises:
        DatasetDefinitionError: Another RDKit version is installed, or a SMILES does not parse.
    """
    rdkit = import_build_dependency("rdkit")
    if rdkit.__version__ != RDKIT_VERSION:
        msg = f"The SMILES descriptors need RDKit {RDKIT_VERSION}, found {rdkit.__version__}."
        raise DatasetDefinitionError(msg)
    chem = import_build_dependency("rdkit.Chem")
    descriptors = import_build_dependency("rdkit.Chem.Descriptors")
    import_build_dependency("rdkit.RDLogger").DisableLog("rdApp.*")
    molecules = [chem.MolFromSmiles(s) for s in smiles]
    invalid = [s for s, molecule in zip(smiles, molecules, strict=True) if molecule is None]
    if invalid:
        msg = f"RDKit cannot parse {len(invalid)} SMILES, for example {invalid[:3]}."
        raise DatasetDefinitionError(msg)
    rows = [descriptors.CalcMolDescriptors(molecule) for molecule in molecules]
    out = pd.DataFrame(rows, index=smiles.index).astype("float64").add_prefix(prefix)
    out = out.where(np.isfinite(out))
    out = out.loc[:, out.nunique(dropna=False).gt(1)]
    return out.loc[:, ~out.T.duplicated()]
