"""Molecules in tabular data: SMILES columns, their recommended encoding, and the scaffolds of a scaffold split.

A molecule's structure ships as a SMILES column, declared in the definition's ``smiles_columns`` (CLEAN-24 as amended
on 2026-11-01): the container marks it as a semantic column (:class:`~data_foundry.schema.SemanticColumn`, type
``smiles``), so a benchmark encodes it as a structure instead of reading it as text. A tabular model gains nothing
from a SMILES read as text (character n-grams or a text embedding; the working copy's CHANGELOG, 2026-10-14, and
apistox's record, 2026-10-07), but it does from a fixed encoding of the structure. :func:`canonical_smiles` gives the
form a definition ships: RDKit's canonical SMILES, every fragment and the stereochemistry kept. Salts stay as
published: the largest fragment is no salt stripper (apistox's triclopyr and picloram triethylammonium salts both
reduce to triethylamine), so salt forms of one compound are a definition's decision (LEAK-19).

:func:`encode_smiles` is the recommended encoding (:data:`DEFAULT_SMILES_ENCODING`): RDKit's 2D descriptors, the
166 MACCS keys and the ECFP4 counts, one row per molecule, the same for a molecule in every dataset, so a benchmark can cache it by value.
Its spec id names the RDKit release and a revision; the container records it as the column's
``recommended_encoding``. A benchmark may use it or its own encoding; the probes of this repository use it
(``dataset_io.py``). Measured on the SMILES datasets of 2026-11-01: the MACCS keys add 0.02 ROC AUC next to the
descriptors on drug_induced_autoimmunity_prediction and change the others by -0.006 to +0.009; the ECFP4 counts lift
qsar_tid_11's LightGBM R^2 from 0.601 to 0.658.

:func:`rdkit_descriptors` gives the descriptors alone, with the columns that are constant or copies in the given
molecules left out (the form the definitions shipped before 2026-11-01). RDKit is in the ``build`` extra, pinned,
because descriptor values can change between releases. ``murcko_scaffolds`` gives the scaffolds of a SMILES column,
and ``scaffold_groups`` the groups of a scaffold-grouped split (``Grouping(on=...)``) built from them.

Mordred, not used: its open 2D descriptors (``mordredcommunity`` 2.0.7, BSD-3, 1,613 descriptors, many of them
Dragon's) run with the pinned RDKit. On qsar_bioconcentration (2026-10-26) they lowered macro ROC AUC: RDKit's
descriptors and the logKOW scored 0.759 (random forest) and 0.765 (LightGBM) over 3 x 10 folds, and adding Mordred's
1,220 descriptors that do not copy an RDKit one 0.746 and 0.745 (paired -0.013 and -0.020). The recommended encoding
leaves Mordred out; revisit it for all SMILES datasets at once, with a gain measured on several.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from data_foundry.v2._optional import import_build_dependency
from data_foundry.v2.dataset import DatasetDefinitionError
from data_foundry.v2.encodings import Encoding

RDKIT_VERSION = "2026.03.6"
"""The RDKit release the descriptors are computed with (pinned in the ``build`` extra); another version is an
error."""


def _chem():
    """``rdkit.Chem``, after checking the installed RDKit is the pinned release.

    Raises:
        DatasetDefinitionError: Another RDKit version is installed.
    """
    rdkit = import_build_dependency("rdkit")
    if rdkit.__version__ != RDKIT_VERSION:
        msg = f"The SMILES descriptors need RDKit {RDKIT_VERSION}, found {rdkit.__version__}."
        raise DatasetDefinitionError(msg)
    import_build_dependency("rdkit.RDLogger").DisableLog("rdApp.*")
    return import_build_dependency("rdkit.Chem")


def _molecules(smiles: pd.Series) -> list:
    """The RDKit molecule of each SMILES.

    Raises:
        DatasetDefinitionError: Another RDKit version is installed, or a SMILES does not parse.
    """
    chem = _chem()
    molecules = [chem.MolFromSmiles(s) for s in smiles]
    invalid = [s for s, molecule in zip(smiles, molecules, strict=True) if molecule is None]
    if invalid:
        msg = f"RDKit cannot parse {len(invalid)} SMILES, for example {invalid[:3]}."
        raise DatasetDefinitionError(msg)
    return molecules


def invalid_smiles(smiles: pd.Series) -> list[str]:
    """The distinct values of ``smiles`` that RDKit cannot parse (missing values are not checked).

    Raises:
        DatasetDefinitionError: Another RDKit version is installed.
    """
    chem = _chem()
    return [s for s in pd.unique(smiles.dropna()) if chem.MolFromSmiles(str(s)) is None]


def canonical_smiles(smiles: pd.Series, *, largest_fragment: bool = False, stereo: bool = True) -> pd.Series:
    """RDKit's canonical SMILES of each molecule, on the index of ``smiles``, as a ``string`` column: the form a
    definition ships in a SMILES column (every fragment and the stereochemistry kept).

    ``largest_fragment`` keeps only the largest fragment (RDKit's ``LargestFragmentChooser``, by atom count): it
    removes a chloride or a water, but it is no salt stripper, since the counter-ion of an amine salt can be the larger
    part (apistox: triclopyr and picloram triethylammonium both reduce to triethylamine); check what it keeps before
    using it. ``stereo=False`` drops the stereochemistry: the key of rows a 2D encoding cannot tell apart. Missing
    values stay missing.

    Raises:
        DatasetDefinitionError: Another RDKit version is installed, or a SMILES does not parse.
    """
    chem = _chem()
    present = smiles.dropna()
    molecules = _molecules(present)
    if largest_fragment:
        chooser = import_build_dependency("rdkit.Chem.MolStandardize.rdMolStandardize").LargestFragmentChooser()
        molecules = [chooser.choose(molecule) for molecule in molecules]
    out = pd.Series(pd.NA, index=smiles.index, dtype="string", name=smiles.name)
    out.loc[present.index] = [chem.MolToSmiles(molecule, isomericSmiles=stereo) for molecule in molecules]
    return out


def _descriptor_frame(molecules: list, index: pd.Index) -> pd.DataFrame:
    """Every RDKit 2D descriptor of each molecule, ``Ipc`` as ``Ipc_log10``, values RDKit cannot compute missing."""
    descriptors = import_build_dependency("rdkit.Chem.Descriptors")
    rows = [descriptors.CalcMolDescriptors(molecule) for molecule in molecules]
    out = pd.DataFrame(rows, index=index).astype("float64")
    if "Ipc" in out.columns:
        out.insert(out.columns.get_loc("Ipc"), "Ipc_log10", np.log10(1 + out.pop("Ipc")))
    return out.where(np.isfinite(out))


def rdkit_descriptors(smiles: pd.Series, *, prefix: str = "rdkit_") -> pd.DataFrame:
    """RDKit's 2D descriptors of each SMILES as ``<prefix><name>`` columns, on the index of ``smiles``.

    Values RDKit cannot compute for a molecule (partial charges, BCUT descriptors) are missing. Descriptors that are
    constant over the molecules or an exact copy of an earlier descriptor are left out. ``Ipc`` (the information
    content of the molecular graph) grows exponentially with the molecule, beyond the float32 range for large ones
    (6e166 in qsar_oral_toxicity), so it ships as ``Ipc_log10`` = log10(1 + Ipc), the same order on a usable scale.

    Raises:
        DatasetDefinitionError: Another RDKit version is installed, or a SMILES does not parse.
    """
    out = _descriptor_frame(_molecules(smiles), smiles.index).add_prefix(prefix)
    out = out.loc[:, out.nunique(dropna=False).gt(1)]
    return out.loc[:, ~out.T.duplicated()]


ECFP4_SIZE = 1024
"""The positions of the ECFP4 count fingerprint in the recommended encoding."""

MACCS_KEYS = 166
"""The MACCS keys in RDKit's fingerprint (its bit 0 is unused and left out)."""

DEFAULT_SMILES_ENCODING = Encoding(
    kind="smiles",
    name="rdkit2d-maccs-ecfp4",
    revision=1,
    library=f"rdkit{RDKIT_VERSION}",
    description=(
        "RDKit's 2D descriptors (Descriptors.CalcMolDescriptors; Ipc as Ipc_log10 = log10(1 + Ipc); values RDKit "
        f"cannot compute missing) as rdkit_<name>, the {MACCS_KEYS} MACCS keys (0/1) as maccs_1 to maccs_{MACCS_KEYS}, "
        f"and the ECFP4 count fingerprint (Morgan, radius 2, {ECFP4_SIZE} positions) as ecfp4_0 to "
        f"ecfp4_{ECFP4_SIZE - 1}, one row per molecule, no column dropped."
    ),
)
"""The recommended encoding of a SMILES column (Lennart, 2026-11-01): RDKit's 2D descriptors with the MACCS keys, and
the ECFP4 counts, which helped once (qsar_tid_11: LightGBM R^2 0.601 to 0.658 on the scaffold splits). One pipeline
choice to revisit for the benchmark; a feature selection step may follow it."""


def encode_smiles(smiles: pd.Series, encoding: Encoding = DEFAULT_SMILES_ENCODING, *, prefix: str = "") -> pd.DataFrame:
    """A SMILES column in the recommended encoding: one row per value of ``smiles``, on its index.

    The columns are ``<prefix>rdkit_<descriptor>`` (float64), ``<prefix>maccs_1`` to ``<prefix>maccs_166`` (int8) and
    ``<prefix>ecfp4_0`` to ``<prefix>ecfp4_1023`` (the ECFP4 counts, int16); the integer columns are nullable (``Int8``,
    ``Int16``) when a SMILES is missing. They are the same for every dataset (none is dropped for being constant in the
    given molecules), and each distinct SMILES is computed once, so a benchmark can cache the rows by value under
    ``encoding.id``. A missing SMILES gives a row of missing values.

    Raises:
        ValueError: ``encoding`` is not :data:`DEFAULT_SMILES_ENCODING` (the one encoding implemented).
        DatasetDefinitionError: Another RDKit version is installed, or a SMILES does not parse.
    """
    if encoding != DEFAULT_SMILES_ENCODING:
        msg = f"Unknown SMILES encoding {encoding.id!r}; implemented: {DEFAULT_SMILES_ENCODING.id!r}."
        raise ValueError(msg)
    values = pd.Index(pd.unique(smiles.dropna()), dtype="object")
    molecules = _molecules(pd.Series(values, dtype="object"))
    maccs = import_build_dependency("rdkit.Chem.MACCSkeys")
    keys = pd.DataFrame(
        [list(maccs.GenMACCSKeys(molecule))[1:] for molecule in molecules],
        index=values,
        columns=[f"maccs_{i}" for i in range(1, MACCS_KEYS + 1)],
        dtype="int8",
    )
    morgan = import_build_dependency("rdkit.Chem.rdFingerprintGenerator").GetMorganGenerator(
        radius=2, fpSize=ECFP4_SIZE
    )
    counts = pd.DataFrame(
        np.array([morgan.GetCountFingerprintAsNumPy(molecule) for molecule in molecules], dtype="int16").reshape(
            len(molecules), ECFP4_SIZE
        ),
        index=values,
        columns=[f"ecfp4_{i}" for i in range(ECFP4_SIZE)],
    )
    table = pd.concat([_descriptor_frame(molecules, values).add_prefix("rdkit_"), keys, counts], axis=1)
    out = table.reindex(smiles.to_numpy(dtype="object"))
    if smiles.isna().any():
        out[keys.columns] = out[keys.columns].astype("Int8")
        out[counts.columns] = out[counts.columns].astype("Int16")
    out.index = smiles.index
    return out.add_prefix(prefix)


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
