"""Curated dataset definition for `ready_biodegradability_huang_zhang` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    Smiles,
    Source,
    TaskSummary,
    TimeBasis,
    canonical_smiles,
    scaffold_groups,
)
from data_foundry.v2.chemistry import RDKIT_VERSION

RAW_FILE = "class_all.csv"
"""Huang and Zhang's ClassDataset_all as Körner et al.'s repository carries it: the chemical's name, name type, CAS
number, the part it comes from, its SMILES and its class, plus the pKa and speciation columns Körner et al. add."""

ECHA_FILE = "iuclid_echa.csv"
"""Körner et al.'s export of the ECHA registration dossiers: one row per study record of 2,858 registered
substances. Read here for one thing only, to adjudicate the rows whose structure is not the substance their CAS
number names (PROV-13); no row and no study of it ships."""

ECHA_COLUMNS = ("cas", "molecular_formula", "molecular_weight", "smiles_echa")
"""The four columns of that export this definition reads: the substance's CAS number and ECHA's own molecular
formula, molecular weight and structure."""

CLASSES = {1: "Yes", 0: "No"}
"""The source's class: 1 readily biodegradable, 0 not readily biodegradable."""

CARBON_NAMES = (
    "methyl",
    "ethyl",
    "propyl",
    "butyl",
    "pentyl",
    "hexyl",
    "phenyl",
    "benzyl",
    "benzo",
    "benzen",
    "pyridin",
    "cyclohex",
    "cyclopent",
    "anoic",
    "enoic",
    "amine",
    "amide",
    "aniline",
    "acetate",
    "acryl",
    "alcohol",
    "naphthal",
    "toluene",
    "azo",
    "carboxyl",
    "glycol",
    "ether",
    "ester",
)
"""Parts of a chemical's name that can only belong to a carbon skeleton. A row whose name holds one of them and whose
structure holds no carbon names a substance its structure cannot be, which no outside source is needed to see."""


def desalted(smiles: pd.Series, *, stereo: bool = True) -> pd.Series:
    """Each structure without RDKit's common salts and solvents, on the index of ``smiles``.

    ``FragmentRemover`` drops halides, metal ions, water, sulfate, ammonia and the rest of RDKit's list; organic
    counter-ions stay, so a salt of an amine keeps both parts. A structure that is wholly inorganic would be emptied
    by the remover and is kept as it is. With ``stereo=True`` the result is that structure as canonical SMILES, which
    is what the scaffold is computed on.

    ``stereo=False`` returns the key of the rows a 2D encoding cannot tell apart (LEAK-19, LEAK-20): the connectivity
    block of the InChIKey of that structure with the stereochemistry removed. It is the house key for molecules, and
    it goes one step further than the canonical SMILES, which still writes a stripped salt's anion, a protonated
    amine and a tautomer differently from the neutral form the other row carries. A structure the InChI code cannot
    read keeps its canonical SMILES as its key, so such rows are never merged with one another.

    Raises:
        ValueError: Another RDKit version is installed.
    """
    from rdkit import Chem, RDLogger, __version__
    from rdkit.Chem import inchi
    from rdkit.Chem.MolStandardize import rdMolStandardize

    if __version__ != RDKIT_VERSION:
        msg = f"The structures need RDKit {RDKIT_VERSION}, found {__version__}."
        raise ValueError(msg)
    RDLogger.DisableLog("rdApp.*")
    remover = rdMolStandardize.FragmentRemover()
    compounds = []
    for value in smiles:
        molecule = Chem.MolFromSmiles(value)
        stripped = remover.remove(molecule)
        if stripped is None or stripped.GetNumAtoms() == 0:
            stripped = molecule
        if stereo:
            compounds.append(Chem.MolToSmiles(stripped))
            continue
        Chem.RemoveStereochemistry(stripped)
        key = inchi.MolToInchiKey(stripped)
        compounds.append(key.split("-")[0] if key else Chem.MolToSmiles(stripped))
    return pd.Series(compounds, index=smiles.index, dtype="string", name="compound")


def element_counts(formula: str) -> dict[str, int]:
    """The elements of a molecular formula and how many atoms of each, a charge suffix ignored."""
    counts: dict[str, int] = {}
    for symbol, number in re.findall(r"([A-Z][a-z]?)(\d*)", re.sub(r"[+-]\d*$", "", formula.strip())):
        counts[symbol] = counts.get(symbol, 0) + (int(number) if number else 1)
    return counts


def heavy_atoms(counts: Mapping[str, int]) -> str:
    """The heavy atoms of ``counts`` as one comparable string, hydrogen left out ("C7 O6 S1")."""
    return " ".join(f"{symbol}{number}" for symbol, number in sorted(counts.items()) if symbol != "H")


def composition(smiles: pd.Series, *, parent: bool = False) -> pd.Series:
    """The heavy atoms of each structure, in the form :func:`heavy_atoms` writes.

    With ``parent=True`` RDKit's common salts and solvents are removed first and repeated copies of one fragment
    count once, so that a substance drawn as its sodium salt, or written twice over, has the composition of the
    substance itself. That is what makes a comparison with a dossier's formula fair: the two sources write the
    counter-ions of one substance differently without disagreeing about which substance it is.
    """
    from rdkit import Chem, RDLogger
    from rdkit.Chem import rdMolDescriptors
    from rdkit.Chem.MolStandardize import rdMolStandardize

    RDLogger.DisableLog("rdApp.*")
    remover = rdMolStandardize.FragmentRemover()
    out = []
    for value in smiles:
        molecule = Chem.MolFromSmiles(value) if isinstance(value, str) else None
        if molecule is None:
            out.append(None)
            continue
        if not parent:
            out.append(heavy_atoms(element_counts(rdMolDescriptors.CalcMolFormula(molecule))))
            continue
        stripped = remover.remove(molecule)
        if stripped is None or stripped.GetNumAtoms() == 0:
            stripped = molecule
        merged: dict[str, int] = {}
        for fragment in sorted(set(Chem.MolToSmiles(stripped).split("."))):
            formula = rdMolDescriptors.CalcMolFormula(Chem.MolFromSmiles(fragment))
            for symbol, number in element_counts(formula).items():
                merged[symbol] = merged.get(symbol, 0) + number
        out.append(heavy_atoms(merged))
    return pd.Series(out, index=smiles.index, dtype="string", name="composition")


def molecular_weights(smiles: pd.Series) -> pd.Series:
    """The average molecular weight of each structure, as a dossier reports it."""
    from rdkit import Chem, RDLogger
    from rdkit.Chem import Descriptors

    RDLogger.DisableLog("rdApp.*")
    weights = []
    for value in smiles:
        molecule = Chem.MolFromSmiles(value) if isinstance(value, str) else None
        weights.append(float("nan") if molecule is None else Descriptors.MolWt(molecule))
    return pd.Series(weights, index=smiles.index, dtype="float64", name="weight")


def echa_dossiers(echa: pd.DataFrame) -> pd.DataFrame:
    """ECHA's own formula, weight and structure per CAS number, for the dossiers that say one thing.

    A CAS number is kept when the export reports one molecular formula and one molecular weight for it; the columns
    are named after the source they come from, so that the joined frame still reads as the two files it is.
    """
    reported = (
        echa.dropna(subset=["cas", "molecular_formula", "molecular_weight"])
        .groupby("cas")
        .agg(
            formulas=("molecular_formula", "nunique"),
            weights=("molecular_weight", "nunique"),
            echa_formula=("molecular_formula", "first"),
            echa_weight=("molecular_weight", "first"),
            echa_smiles=("smiles_echa", "first"),
        )
    )
    reported = reported[(reported["formulas"] == 1) & (reported["weights"] == 1)]
    return reported[["echa_formula", "echa_weight", "echa_smiles"]]


def prepared(raw: pd.DataFrame) -> pd.DataFrame:
    """The source's rows with the structure canonical and repaired, and the rows their own name contradicts marked.

    ``contradicted`` marks a row whose CAS number ECHA registers and whose shipped structure is not that substance:
    ECHA's formula and ECHA's weight agree with each other (the weight the formula implies is within 0.5 of the
    weight reported, which holds for every dossier, the weight being computed from the formula) and both disagree
    with the shipped structure, which has neither the composition of that formula nor, once salts and repeated
    fragments are resolved, the composition of ECHA's own structure, and whose weight is more than 0.5 from ECHA's.
    Such a row is repaired (``repaired``) when ECHA's structure parses and has the composition its own formula
    gives, so that nothing enters the data against the dossier, and keeps the published structure otherwise.
    ``impossible`` marks a row whose name is built of carbon stems while its structure holds no carbon at all, which
    needs no outside source to see and which no repair reaches (PROV-13, the remedy ladder: repair, then drop).
    """
    from rdkit import Chem

    table = Chem.GetPeriodicTable()
    smiles = canonical_smiles(raw["smiles"])
    counts = raw["echa_formula"].map(element_counts, na_action="ignore")
    implied = counts.map(
        lambda c: sum(table.GetAtomicWeight(symbol) * n for symbol, n in c.items()), na_action="ignore"
    )
    dossier = counts.map(heavy_atoms, na_action="ignore").where((implied - raw["echa_weight"]).abs() <= 0.5)
    contradicted = (
        (
            dossier.notna()
            & (composition(smiles) != dossier)
            & (composition(smiles, parent=True) != composition(raw["echa_smiles"], parent=True).fillna(""))
            & ((molecular_weights(smiles) - raw["echa_weight"]).abs() > 0.5)
        )
        .fillna(False)
        .astype(bool)
    )
    repaired = (contradicted & (composition(raw["echa_smiles"]) == dossier)).fillna(False).astype(bool)
    smiles = smiles.copy()
    smiles[repaired] = canonical_smiles(raw.loc[repaired, "echa_smiles"])
    named_organic = raw["name"].fillna("").str.lower().str.contains("|".join(CARBON_NAMES))
    impossible = (named_organic & ~composition(smiles).fillna("").str.contains(r"(?:^|\s)C\d")).astype(bool)
    return pd.DataFrame(
        {"SMILES": smiles, "contradicted": contradicted, "repaired": repaired, "impossible": impossible}
    )


class ReadyBiodegradabilityHuangZhang(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Does a chemical reach 60% degradation in a 28-day aerobic screening test (70% where the method "
            "follows dissolved organic carbon), judging from its structure?"
        ),
        use_case=(
            "For example, a producer or a registrant screens a chemical's structure before commissioning a "
            "ready-biodegradability test, which runs at least 28 days and costs thousands of dollars, or a regulator "
            "ranks registered chemicals for a persistence assessment."
        ),
        row=(
            "One chemical with a ready-biodegradability result, from Huang and Zhang's ClassDataset_all: 4,389 "
            "chemicals read off screening-test records and 1,325 compiled from the literature (5,714 of their 6,139, "
            "after copies of one compound are resolved)."
        ),
        predicted=(
            "Whether the chemical passes the standard test, that is at least 60% degradation in 28 days (70% where "
            "the method follows dissolved organic carbon); 33.8% do."
        ),
        known="The chemical's structure, as a SMILES string.",
        split=(
            "Whole chemical series are held out: chemicals that share a ring skeleton stay on one side, so a test "
            "chemical of a series belongs to a family the model has not seen. Chemicals without a ring and those "
            "whose only skeleton is a bare benzene ring, half the set, are held out one by one, so for them the "
            "split is a draw."
        ),
        changes=(
            "We ship the structure in place of the pKa and speciation columns the copy adds, put ECHA's own "
            "structure on the 19 chemicals whose dossier contradicts the one published, drop the chemicals whose "
            "structure carries both classes, and split by chemical series instead of at random."
        ),
        fit="direct",
        fit_reason=(
            "The structure is all a screener has before the test, and a held-out series stands for a family not yet "
            "tested. The label is the day-28 reading and leaves out the 10-day window the OECD 301 series requires "
            "before a chemical counts as readily biodegradable: on the quarter of the chemicals a REACH export "
            "reaches, the registrants' own conclusion turns 89 of 779 positives negative, 1.6% of all rows."
        ),
    )

    # Dataset
    unique_name = "ready_biodegradability_huang_zhang"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.1021/acs.est.2c01764",
            license=None,  # the article states none for its supporting information
            year="2022",
            bibtex="""
                @article{huang2022classification,
                  title={Classification and Regression Machine Learning Models for Predicting Aerobic Ready and
                         Inherent Biodegradation of Organic Chemicals in Water},
                  author={Huang, Kuan and Zhang, Huichun},
                  journal={Environmental Science \\& Technology},
                  volume={56},
                  number={17},
                  pages={12755--12764},
                  year={2022},
                  publisher={American Chemical Society},
                  doi={10.1021/acs.est.2c01764}
                }
            """,
        ),
        Source(
            role="copy",
            platform="GitHub",
            url="https://github.com/pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals",
            license="GPL-3.0",
            year="2024",
            name="Körner et al. 2024, datasets/external_data/class_all.csv and datasets/iuclid_echa.csv",
            files=(RAW_FILE, ECHA_FILE),
        ),
    )
    special_features = (Smiles(column="SMILES"),)
    download_description = """
        mkdir -p local-data-warehouse/ready_biodegradability_huang_zhang && wget -O local-data-warehouse/ready_biodegradability_huang_zhang/class_all.csv https://raw.githubusercontent.com/pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals/main/datasets/external_data/class_all.csv && wget -O local-data-warehouse/ready_biodegradability_huang_zhang/iuclid_echa.csv https://raw.githubusercontent.com/pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals/main/datasets/iuclid_echa.csv

        class_all.csv (2,242,462 bytes), sha256
        428fb480260301f054fae588e768f3ed33397b5cad4d4bc8ae8dc7459a60b121 (downloaded 2026-11-25)

        iuclid_echa.csv (6,517,235 bytes), sha256
        4502fae3312b8a73229714ed90bc9ef59d0b8a4dab99b6a3d54f3402b22f8720 (downloaded 2026-11-25)

        pubs.acs.org refuses a command-line download of the article's supporting information (403), which is where
        the data files are, so the file comes from Körner et al.'s repository, which redistributes Huang and Zhang's
        three classification sets with pKa and speciation columns added. The article itself is readable: the
        accepted manuscript is free at https://par.nsf.gov/servlets/purl/10350359, and every sentence quoted below
        was checked against it on 2026-11-25.

        The second file is Körner et al.'s own export of the ECHA registration dossiers. No row of it ships: it is
        read for ECHA's molecular formula, molecular weight and structure per CAS number, which adjudicate the rows
        whose structure is not the substance they are about (curation_comments).
    """
    accepted_check_warnings = {
        "meta_license_unknown": (
            "The article states no licence for the supporting information that holds the data, and the repository "
            "the file is copied from is GPL-3.0 for its code, which does not govern the data it redistributes, so "
            "no licence can be declared. Accepted as on qsar_biodeg (2026-11-02): noted, not blocking, and to be "
            "regularised before the data ships outside the group (Andrej, 2026-11-25)."
        ),
    }
    curation_comments = """
        We start with class_all.csv from Körner et al.'s repository, which carries Huang and Zhang's ClassDataset_all.

        - Prediction point: a chemical with no ready-biodegradability result, before a test is commissioned. The only
          input is the structure, which exists before any test, so no feature here is recorded after that moment.
          Huang and Zhang give the same reason for the models (Introduction): "As most experimental tests normally
          last at least 28 days, the cost for testing a sample commonly falls in the range of 3000-8000 USD or more",
          and they publish the models as free online predictors for new structures.
        - The file is ClassDataset_all: ClassDataset_original (4,593 chemicals, the classification reading of the
          authors' own regression records, collected "mainly ... using the eChem portal" at reliability 1 and 2) and
          ClassDataset_external (1,546 chemicals "compiled from the literature because it would be meaningful to
          validate our models using data from a different source"). Its counts and balance are the paper's:
          "ClassDataset_original (4593 records), ClassDataset_external (1546 records), and ClassDataset_all (6139
          records) all have around 65% of negative (0s, NRB) and 35% of positive (1s, RB) records".
        - The label is a reading of the test result, not a column of the source: the ready endpoint at day 28 with at
          least 60% degradation, 70% where the method follows dissolved organic carbon ("the DOC-based standard
          methods usually set a threshold of 70% (not 60% for other principles) to classify the ready
          biodegradability"). Rebuilding that reading from the authors' regression workbook reproduces 4,482 of the
          4,591 classes of ClassDataset_original that match by CAS number (97.6%; a majority or a mean over a
          chemical's repeat tests reaches 98.2%), measured 2026-11-25. So the published class is that reading, and it
          ships as published. The 28-day ready records behind it run over the whole OECD 301 series and its EU
          equivalents (301 F 24.6%, 301 B 23.4%, 301 C 22.5%, 301 D 17.2%, 310 2.7%, 301 A and 301 E 2.6% each, EU
          Method C.4 in its four variants 4.4%); the paper treats them as one protocol, since the guidelines "were
          originally designed to be equivalent except that they can handle chemicals with different physicochemical
          properties".
        - The label pools those protocols, and they do not pass the same chemicals: of the 6,130 28-day ready
          records, the pass rate is 27.2% under 301 C, 37.6% under 301 D, 38.8% under 301 F, 40.5% under 301 B,
          40.9% under 301 E, 46.6% under 301 A and 52.7% under 310; 688 chemicals were tested under more than one
          guideline and 26.9% of them get opposite calls, against 13.3% disagreement among the 181 chemicals with
          repeats under one guideline (measured 2026-11-25). The source drops the conditions on purpose, "to expand
          the application of this study to when only binary classification is needed (an industry norm) without
          specifying the experimental conditions and reaction time", and that pooled call is the task here; its own
          regression predictor, a task of its own, is the version that takes the guideline as an input. The sibling
          qsar_biodeg is 301 C alone, the strictest of them.
        - The structure ships as `SMILES` (CLEAN-24 as amended, Lennart, 2026-11-01), in RDKit's canonical form
          (`canonical_smiles`; every fragment and the stereochemistry as published), declared in `special_features`, so
          a benchmark encodes it as a structure and never as text; the recommended encoding is
          `data_foundry.v2.chemistry.encode_smiles` (RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts).
          All 6,139 SMILES parse with the pinned RDKit.
        - The `pka_*` and `α_*` columns leave: Körner et al. computed them from the structure with MolGpKa
          (`add_pka_values.py` in their repository), one modelling choice of the structure, as the Dragon descriptors
          did on qsar_biodeg and the other QSAR siblings (CLEAN-24). `name`, `name_type` and `cas` are identifiers
          (CLEAN-21), and the 1,546 literature rows carry no CAS number at all; `source`, which names the part a row
          comes from, is provenance of the compilation rather than a property of the chemical (CLEAN-22). The three
          dossier columns joined on from the ECHA export are read in `_clean` and leave with them.
        - Structures that are not the substance the row is about (PROV-13, Andrej's decision of 2026-11-25): the
          compilation's identifiers and its structures were retrieved separately, and Körner et al. report mismatched
          chemical identifiers in it. ECHA's own dossiers adjudicate the rows that carry a CAS number: their export
          gives one molecular formula and one molecular weight for 2,764 registered substances, and the two always
          agree with each other, the weight being computed from the formula, so what decides a row is the
          disagreement with the shipped structure. It reaches 1,901 of the 6,139 rows (31.0%), and 34 of those
          (1.8%) carry a structure that is neither the composition ECHA's formula gives nor, once salts and repeated
          fragments are resolved, the substance ECHA's own structure draws, and whose weight is more than 0.5 from
          ECHA's: 2,2-bis(methylthio)propane is drawn as a fluorophenyl thiourea sulfonamide, a trimethoxysilyl
          sorbate as phenothiazine, a difluorophenyl isoxazole as chlorobenzene. 19 of them take ECHA's structure,
          which is where the dossier's own structure parses and has the composition its formula gives; the other 15
          keep the structure as published, 11 of them because the dossier carries no structure at all and 4 because
          its structure contradicts its own formula. A row the repair cannot reach but the file contradicts by
          itself leaves: 4 rows name a carbon skeleton (limonene, an azo dye, a zinc neodecanoate, a
          butylpyridinium aluminate) and hold no carbon at all, being drawn as calcium oxide, sodium sulfate, zinc
          sulfate and ammonium aluminium sulfate. What is not done here, for its scale: the 270 of 3,767 shared CAS
          numbers whose structure differs from Körner et al.'s own curated one, which would be an adjudication of
          its own, and the 1,546 literature rows, which carry no CAS number to adjudicate by.
        - Copies (LEAK-19, LEAK-20): the key is the compound as a 2D encoding sees it - the structure without
          RDKit's list of common salts and solvents (`FragmentRemover`: halides, metal ions, water, sulfate, ammonia
          and others; organic counter-ions stay) and without stereochemistry, read as the connectivity block of its
          InChIKey, which holds a stripped salt's anion, a protonated amine and a tautomer together with the neutral
          form another row writes (the house key for molecules, as on qsar_oral_toxicity). It runs on the repaired
          structures, after the 4 rows above have left. 723 of the structures hold more than one fragment, and 581 of
          them lose something to the remover. 332 compounds occur in more than one row (708 rows), 110 of them found
          only by the InChIKey step. 45 compounds (107 rows) carry both classes and are dropped whole: 25 are one
          structure already to the stereo-free SMILES, and the other 20 are a salt and its free form, two salts of
          one acid, or a tautomer pair, that the sources read differently. Of the 287 compounds that agree, the
          first row is kept (314 rows dropped). 5,714 chemicals remain, 33.8% readily biodegradable against 34.9%
          before, 4,389 of them from the original part and 1,325 from the literature one. The two parts share no
          exact structure, but 210 compounds of the literature part (212 rows) are a chemical of the first part
          under this key, 23 of them carrying both classes; the rule above settles them with the rest.
        - What the key does not merge: the number of organic fragments is part of it, so a sodium and a zinc
          dithiocarbamate, or a mono- and a di-salt of one acid, stay apart, and the InChI code normalises a
          removable proton but not a carbanion, so chloro(propan-2-yl)magnesium stays apart from the alkane. All 110
          clusters the InChIKey step adds were read by name on 2026-11-25: every one is a salt beside its free acid,
          a salt written ionically beside the same salt written covalently, a zwitterion beside its neutral form, or
          a tautomer pair. 8 CAS numbers still name two rows each (16 rows, 2 of them with both classes), where the
          two rows are written as different substances; the record weighs a CAS step against them.
        - Anomaly: a chemical tested several times with conflicting results keeps the one class the source chose. 209
          of the 4,966 chemicals with a 28-day ready test in the authors' regression workbook (4.2%) have at least one
          test on each side of the threshold (measured 2026-11-25). This is the noise of the screening test itself,
          which the source resolved before publishing a class; Körner et al.'s curated sets drop such chemicals
          instead, which removes the hard cases rather than the ambiguity (TP-6), so the class as published stays.
        - Note: the label reads the test at day 28 and ignores the 10-day window that the OECD 301 series requires
          before a regulator calls a chemical readily biodegradable. In Körner et al.'s own REACH export 505 of the
          6,035 ready records that carry a conclusion read "readily biodegradable, but failing 10-day window". That
          export reaches 1,631 of the chemicals shipped here by CAS number (28.5%), agreeing with the class on 91.5%
          of them, and its conclusions would turn 89 of their 779 positives negative (11.4%, 1.6% of all chemicals
          here; measured 2026-11-25). The gap is uneven: 1.4% of the 301 C records called readily biodegradable
          carry the flag, against 13.1% to 22.6% under 301 B, D, E, F and 310, and the guideline is not a column
          here. It covers a quarter of the set, so taking it would mean two different labels in one target column,
          and the day-28 reading stays for every chemical.
        - Not read from the repository: `class_original.csv` and `class_external.csv` (the two parts of this file),
          `Huang_Zhang_RegressionDataset.xlsx` (12,750 test records with the percent degraded, the guideline and the
          duration: the authors' regression task, a task of its own, read here only to check the label and the test
          mix), the three curated sets under `datasets/curated_data/` (Körner et al.'s own compilation, built from
          their ECHA export with Lunghini et al. 2020's set concatenated onto it rather than cut out of this file,
          and weighed against it in the record), `chemical_speciation.xlsx` (the hand-checked species at pH 7.4 behind the dropped speciation
          columns), `substance_file.xlsx` (the example notebook's input) and
          `reach_study_results/RegisteredSubstances_organic6.pkl` (the raw pull behind `iuclid_echa.csv`). None of
          them holds a chemical of Huang and Zhang's series that this file does not. The primary release, the
          article's supporting information, could not be listed at all (403), so this list is of the copy.
        - Split (SPLIT-31, SPLIT-36, leaf L-FAMILY.key): grouped on the Bemis-Murcko scaffold of the compound, the
          structure without common salts and solvents (`scaffold_groups`): 4,329 groups, 4,009 chemicals alone (2,061
          without a ring, 36.1%, 980 whose only skeleton is the bare benzene ring, 17.2%, which holds more than a
          tenth of the set and is therefore no series, and 968 with a scaffold no other chemical here has) and 320
          series of 2 to 103 chemicals. No other scaffold reaches a tenth, the largest series being cyclohexane with
          1.8% of the chemicals. Under the groups 19.0% of the test chemicals have a training chemical at Tanimoto
          0.7 or more (Morgan radius 2, 2,048 bits, on the compound; median nearest 0.520), against 21.4% under a
          random split (0.545), measured over 3 folds on 2026-11-25. The source split at random and reports that
          "higher similarities among the training, validation, and test datasets always gave better model
          performance", so its published figures say nothing about this split (SPLIT-5).
        - What the grouping buys, and where it buys nothing: the close-analogue share is 6.2% for the chemicals that
          sit in a series, 16.3% for the bare-benzene ones and 36.9% for the ring-less third, which is the
          analogue-dense part of the set (homologous series of acids, alcohols, glycol ethers and surfactants) and
          is split at random, where a random split of everything leaves it 34.7%. The consequence is measured:
          untuned LightGBM on the recommended encoding scores 0.861 on ring-less test rows that have a close
          training analogue and 0.837 on those that do not. Holding the bare-benzene chemicals out as one family
          instead, which the rule above forbids, would cost 0.042 ROC AUC on those rows (0.849 against 0.890) and
          0.010 on the task (0.878 against 0.888), all measured on 2026-11-25.
        - Note: the raw file is ordered by chemistry, not by a clock. Neighbouring rows share a ring skeleton in 9.6%
          of the pairs against 2.8% after a shuffle, and share a class in 66.4% against 54.6%, which is why the class
          rate swings between a fifth and a half from one tenth of the file to the next without a trend (the rank
          correlation of the class with the position is -0.04 in each part). The rows are shuffled before the split
          and nothing of the order ships; the grouping holds out the series the order lines up.
        - Note: this set covers the sibling qsar_biodeg, which carries Mansouri et al.'s 1,055 chemicals from Japan's
          testing programme. 1,001 of those 1,055 (94.9%) are here as one compound, 972 of them (97.1%) with the same
          class (measured 2026-11-25 on the key above). The two compilations end at different original sources, so
          neither is a copy of the other (PROV-4); which of them ships is the curator's call on the pair, recorded in
          the records. What the sibling is not is the same label on fewer chemicals: it is OECD 301 C alone, where
          the pass rate is 27.2% against 33.8% here, while this label pools seven protocols.
        - Note on the rows themselves: 147 chemicals (2.57%) are substances of more than one organic component
          (rosin salts, hydrocarbon reaction masses, polyvalent metal resinates; 43 of three components or more, up
          to 368 heavy atoms), whose encoding sums the descriptors over the components, so for them the feature
          vector describes the mixture rather than a molecule; their pass rate is 0.408 against 0.338 overall. They
          stay, because a registrant does commission this test for such substances. 4 chemicals (0.07%) hold no
          carbon at all, and all four are inorganic by their own name (three borates and sodium chlorate): the
          remover would empty them, so they keep their structure as published, and they are their own group. The
          four carbon-free rows whose name is organic left above.
    """
    split_leaf = "L-FAMILY.key"
    time_basis = TimeBasis(
        "UnseenGroup",
        """
        The source builds a screen for chemicals nobody has tested: its reason is the cost and the length of the test
        itself, and it ships free online predictors that take a structure. Its question is a chemical from outside the
        collection, not the collection's next entry, so the scaffold split stands (SPLIT-37, the source's scope).
        No date is in the data: neither this file, nor the authors' regression workbook, nor Körner et al.'s REACH
        export carries a test or dossier date, and the eChem portal links each record to a dossier page that was not
        read. The CAS number is a coarse order of first registration and covers 76.8% of the rows; along it the
        readily biodegradable share falls from 45.0% in the oldest fifth to 18.4% in the newest (Spearman -0.172),
        but holding out the newest 30% of those rows scores 0.864 ROC AUC against 0.880 for a random and 0.869 for a
        scaffold-grouped split of the same rows (measured 2026-11-25), so the order costs little beyond what the
        scaffold split already asks, and a registration number dates the substance rather than the test, so no
        temporal option is given up. The split therefore cannot test whether the
        chemicals registered later are labelled differently from those already in the catalogue.
        """,
    )

    # Task
    target = "Biodegradable"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Huang and Zhang evaluate their classifiers 'based on different matrices, including accuracy, sensitivity, specificity, balanced accuracy, ROC AUC, and f_1' and report all six side by side (85.6, 90.3, 80.4, 85.4, 91.8 and 85.1%) without naming the one that decides, so no metric is one deliberate choice (MET-5); their threshold metrics fix no threshold and no costs (MET-6), and Körner et al. 2024 rank by balanced accuracy, equally unfixed. Original rejected: balanced accuracy. roc_auc is the binary fallback, as on qsar_biodeg."
    )

    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a chemical series: the chemicals whose structure, without common salts and solvents, shares one Bemis-Murcko scaffold (ring systems and the chains linking them; Bemis and Murcko 1996), computed with RDKit. A chemical without a ring (36.1%) is a group of its own, and so is one whose only skeleton is the bare benzene ring (17.2%), which holds more than a tenth of the set and is no series (SPLIT-31). A producer or a registrant screens a chemical that has not been tested, often one of a series nobody has measured, which is why Huang and Zhang open with the cost of the test and publish predictors for new structures; so whole series are held out. Each row is one prediction, made from the chemical's structure alone.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the Bemis-Murcko scaffold of the compound (the structure without common salts and solvents): all chemicals of one series stay on one side, so a model predicts chemicals of a series it has not seen; chemicals without a ring (36.1%), and those whose only skeleton is the bare benzene ring (17.2%), are held out one by one, so for those two groups the split is a draw. Chemicals with similar but not identical scaffolds can be on both sides: 19.0% of the test chemicals still have a training chemical at Tanimoto 0.7 or more, against 21.4% under a random split; by part, 6.2% of the chemicals that sit in a series, 16.3% of the bare-benzene ones and 36.9% of the ring-less ones, where a random split of everything leaves 34.7%. What that costs is measured: 0.861 ROC AUC on ring-less test rows with a close training analogue against 0.837 on those without.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # the dossier file joins on, three columns wide: ECHA's own formula, weight and structure for the row's CAS
        # number, which adjudicate the structures that are not the substance the row is about
        rows = pd.read_csv(raw_dir / RAW_FILE)
        echa = pd.read_csv(raw_dir / ECHA_FILE, low_memory=False, usecols=ECHA_COLUMNS)
        return rows.join(echa_dossiers(echa), on="cas")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # The structure ships as a SMILES column (`special_features`) in RDKit's canonical form, salts and stereo as
        # published; the class becomes words. Everything else leaves: identifiers, the part a row comes from, the
        # dossier columns and the pKa and speciation columns the copy adds (curation_comments)
        #
        # Structures that are not the substance the row is about (PROV-13, Andrej, 2026-11-25): where ECHA's own
        # dossier fields contradict the shipped structure, the structure is ECHA's; where the row's own name
        # contradicts it and no dossier reaches it, the row leaves (`prepared`)
        source = prepared(raw)
        df = pd.DataFrame({"SMILES": source["SMILES"], self.target: raw["y_true"].map(CLASSES)})
        assert df[self.target].notna().all(), "a class is neither 0 nor 1"
        df = df[~source["impossible"]]
        # Copies of one compound (LEAK-19, LEAK-20): the key is the InChIKey connectivity block of the structure
        # without common salts, solvents and stereochemistry, which is what a 2D encoding sees, and which also holds
        # a salt's anion, a protonated amine and a tautomer together; a compound with both classes goes whole
        compound = desalted(df["SMILES"], stereo=False)
        both = compound.isin(df.groupby(compound)[self.target].nunique().loc[lambda n: n > 1].index)
        df, compound = df[~both], compound[~both]
        df = df[~compound.duplicated()]
        # The split groups: the chemical series (the Bemis-Murcko scaffold of the compound, salts removed); a chemical
        # without a ring, and one of a scaffold above a tenth of the set, is a group of its own
        return df.assign(scaffold=scaffold_groups(desalted(df["SMILES"])))

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the SMILES is typed by `special_features`; the target becomes a category
        del df
        return FeatureTypes()

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        source = prepared(raw)
        kept = source[~source["impossible"]]
        compound = desalted(kept["SMILES"], stereo=False)
        classes = raw.loc[kept.index, "y_true"].map(CLASSES).groupby(compound).agg(["nunique", "size"])
        repeated = classes[classes["size"] > 1]
        evidence = pd.DataFrame(
            {
                "compounds": [len(classes), len(repeated), int((repeated["nunique"] > 1).sum())],
                "rows": [
                    len(kept),
                    int(repeated["size"].sum()),
                    int(repeated.loc[repeated["nunique"] > 1, "size"].sum()),
                ],
            },
            index=["all", "in more than one row", "with both classes"],
        )
        reached = raw["echa_formula"].notna()
        damage = pd.DataFrame(
            {
                "rows": [
                    len(raw),
                    int(reached.sum()),
                    int(source["contradicted"].sum()),
                    int(source["repaired"].sum()),
                    int(source["impossible"].sum()),
                ]
            },
            index=[
                "all",
                "a CAS number ECHA registers",
                "a structure ECHA's dossier contradicts",
                "repaired from the dossier",
                "dropped, the name contradicting the structure",
            ],
        )
        return [
            Decision(
                title="Structures that are not the substance the row is about",
                why=(
                    "A row carries a structure that is not the substance its CAS number names: the compilation's "
                    "identifiers and structures were retrieved separately, and Körner et al. 2024 report mismatches "
                    "between them. ECHA's own registration dossiers, exported in the same release, give a molecular "
                    "formula, a molecular weight and a structure per CAS number. Where the formula and the weight "
                    "agree with each other and both disagree with the shipped structure, the structure is replaced "
                    "by ECHA's own, and where the row's own name states a carbon skeleton its structure does not "
                    "have, the row is dropped (PROV-13, the curator's decision of 2026-11-25). "
                    f"{int(source['contradicted'].sum())} of the {int(reached.sum()):,} rows ECHA reaches are "
                    f"contradicted, {int(source['repaired'].sum())} of them repaired and "
                    f"{int((source['contradicted'] & ~source['repaired']).sum())} kept as published, the dossier "
                    f"holding no usable structure; {int(source['impossible'].sum())} rows leave on their own name."
                ),
                evidence=damage,
            ),
            Decision(
                title="Copies of one compound",
                why=(
                    "A chemical appears in several rows as a salt, as a charged or a protonated form, as a "
                    "tautomer, as a stereoisomer or in both parts of the compilation. The key is the InChIKey "
                    "connectivity block of the structure without common salts, solvents and stereochemistry, which "
                    "is what a 2D encoding sees: a compound carrying both classes is dropped whole (LEAK-20), and "
                    "of the rest one row is kept (LEAK-19). "
                    f"{len(kept):,} rows become {len(df):,}, and the readily biodegradable share moves from "
                    f"{raw.loc[kept.index, 'y_true'].mean():.3f} to {df[self.target].eq('Yes').mean():.3f}."
                ),
                evidence=evidence,
            ),
        ]
