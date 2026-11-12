"""MixtureSolDB measured solubility in binary solvents; curated v2 definition."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
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
    canonical_smiles,
    scaffold_groups,
)
from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize

RAW_SHA256 = "be72940b1d9ba03eacf142cfb26e774b658617dbf8fefb3cfb96f27c4da5e51d"
STRUCTURES = ("SMILES_Solute", "SMILES_Solvent1", "SMILES_Solvent2")
INPUTS = (*STRUCTURES, "Temperature_K", "Fraction_Solvent1", "Fraction_Solvent2", "Fraction_Type")


# Source-named salt and metallation families; grouping only, never a structure substitution.
FAMILY_LINKS = (
    (
        ("C1=Cc2nc1c(-c1ccccc1)c1ccc([nH]1)c(-c1ccccc1)c1nc(c(-c3ccccc3)c3ccc([nH]3)c2-c2ccccc2)C=C1"),
        ("C1=Cc2nc1c(-c1ccccc1)c1nc(c(-c3ccccc3)c3ccc([n-]3)c(-c3ccccc3)c3ccc([n-]3)c2-c2ccccc2)C=C1.[Cl-].[Mn+3]"),
    ),
    (
        ("CNC(=O)c1cc(Oc2ccc(NC(=O)Nc3ccc(Cl)c(C(F)(F)F)c3)cc2)ccn1"),
        ("CNC(=O)c1cc(Oc2ccc(NC(=O)Nc3ccc(Cl)c(C(F)(F)F)c3)cc2)ccn1.Cc1ccc(S(=O)(=O)O)cc1"),
    ),
    (
        ("Clc1ccc(-c2c3nc(c(-c4ccc(Cl)cc4)c4ccc([nH]4)c(-c4ccc(Cl)cc4)c4nc(c(-c5ccc(Cl)cc5)c5ccc2[nH]5)C=C4)C=C3)cc1"),
        (
            "Clc1ccc(-c2c3nc(c(-c4ccc(Cl)cc4)c4ccc([n-]4)c(-c4ccc(Cl)cc4)c4nc(c(-c5ccc(Cl)cc5)c5ccc2[n-"
            "]5)C=C4)C=C3)cc1.[Cl-].[Mn+3]"
        ),
    ),
    (
        ("NC(N)=NCCC[C@H](N)C(=O)O"),
        ("N=C(N)NCCC[C@H](N)C(=O)O.O=C1CC[C@@H](C(=O)O)N1"),
    ),
    (
        ("NC(N)=NCCC[C@H](N)C(=O)O"),
        ("NC(N)=NCCC[C@H](N)C(=O)O.O=C(O)CCC(=O)C(=O)O"),
    ),
    (
        ("OCCN(CCO)c1nc(N2CCCCC2)c2nc(N(CCO)CCO)nc(N3CCCCC3)c2n1"),
        ("Cc1ccc(S(=O)(=O)O)cc1.Cc1ccc(S(=O)(=O)O)cc1.OCCN(CCO)c1nc(N2CCCCC2)c2nc(N(CCO)CCO)nc(N3CCCCC3)c2n1"),
    ),
)


def canonical_values(values: pd.Series) -> pd.Series:
    """Canonicalize distinct present structures once, preserving complete molecular identities."""
    unique = pd.Series(values.dropna().unique(), dtype="string")
    return values.map(dict(zip(unique, canonical_smiles(unique), strict=True))).astype("string")


def solute_groups(values: pd.Series) -> pd.Series:
    """Keep related chemical identities together without altering shipped structures."""
    unique = pd.Series(sorted(values.unique()), dtype="string")
    remover = rdMolStandardize.FragmentRemover()
    tautomer = rdMolStandardize.TautomerEnumerator()
    uncharger = rdMolStandardize.Uncharger()
    parents = []
    for value in unique:
        molecule = remover.remove(Chem.MolFromSmiles(value))
        Chem.RemoveStereochemistry(molecule)
        parents.append(Chem.MolToSmiles(molecule))
    parent_values = pd.Series(parents, dtype="string")
    parent_unique = pd.Series(sorted(parent_values.unique()), dtype="string")
    scaffold_map = dict(zip(parent_unique, scaffold_groups(parent_unique), strict=True))
    graph = {value: value for value in unique}

    def root(value):
        while graph[value] != value:
            graph[value] = graph[graph[value]]
            value = graph[value]
        return value

    seen = {}
    for value, parent in zip(unique, parents, strict=True):
        molecule = Chem.MolFromSmiles(parent)
        keys = [
            "scaffold:" + scaffold_map[parent],
            "parent:" + parent,
            "tautomer:" + Chem.MolToSmiles(tautomer.Canonicalize(molecule)),
        ]
        neutral = uncharger.uncharge(molecule)
        keys.extend(
            [
                "neutral-parent:" + Chem.MolToSmiles(neutral),
                "neutral-tautomer:" + Chem.MolToSmiles(tautomer.Canonicalize(neutral)),
            ]
        )
        inchi = Chem.MolToInchiKey(molecule)
        if inchi:
            keys.append("inchi:" + inchi)
        for key in keys:
            if key in seen:
                left, right = sorted([root(value), root(seen[key])])
                graph[right] = left
            else:
                seen[key] = value
    for left_value, right_value in FAMILY_LINKS:
        assert left_value in graph
        assert right_value in graph
        left, right = sorted([root(left_value), root(right_value)])
        graph[right] = left
    mapping = {value: "solute-family:" + root(value) for value in unique}
    return values.map(mapping).astype("string")


class MixtureSolDb(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is the natural logarithm of a solute's mole-fraction solubility in a planned molecular-solvent mixture?",
        use_case=(
            "For example, a process chemist screens solvent compositions and temperatures for a new solute before "
            "laboratory measurement, to choose crystallization or formulation conditions."
        ),
        row=(
            "One published experimental solute, molecular-solvent composition and temperature observation with measured "
            "solubility."
        ),
        predicted=(
            "Natural logarithm of the measured solute mole fraction; ln(0.001) is about -6.908. RMSE scores this "
            "log quantity directly."
        ),
        known=(
            "The solute and both molecular solvent structures, planned temperature and initial solvent proportions, with "
            "their mass-or-mole fraction convention."
        ),
        split=(
            "Hold out whole solute scaffold and structural-identity families, including every composition and "
            "temperature of each solute. Solvents can recur across folds."
        ),
        changes=(
            "Convert measured mole fractions to natural logs, remove alternative outcomes and identifiers, "
            "restrict to molecular solvents, exclude 22 composition-uncertain source rows, normalize solvent ordering and pure endpoints, deduplicate identical input-target records and group "
            "solute families."
        ),
        fit="approximate",
        fit_reason=(
            "Literature measurements are not a prospective random sample of new designs, and polymorph, "
            "experimental method and other conditions are incompletely recorded. No chronological validity is "
            "claimed."
        ),
    )
    unique_name = "bigsoldb_2"

    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://zenodo.org/records/18660057",
            license="CC BY 4.0",
            year="2025",
            bibtex="""
        @article{malikov2026mixturesoldb,
          title={Dataset of solubility values for organic compounds in binary mixtures
                 of solvents at various temperatures},
          author={Malikov, Dmitry and Krasnov, Lev and Kiseleva, Marina and others},
          journal={Scientific Data}, year={2026}, volume={13}, pages={727},
          doi={10.1038/s41597-026-07047-z}
        }
    """,
            name="MixtureSolDB v3",
            files=("raw/MixtureSolDB.csv",),
        ),
    )

    download_description = """
        Download MixtureSolDB v3, not the separate single-solvent BigSolDB:
        mkdir -p local-data-warehouse/bigsoldb_2/raw
        curl -L --fail 'https://zenodo.org/records/18660057/files/MixtureSolDB.csv?download=1' \
          -o local-data-warehouse/bigsoldb_2/raw/MixtureSolDB.csv
        MD5: 597e31685fe36c78d568f3d37b6e1336; SHA256:
        be72940b1d9ba03eacf142cfb26e774b658617dbf8fefb3cfb96f27c4da5e51d.
        The 41,107,737-byte file has 175,166 rows and 19 columns.
        RecordID is absent despite the documented 20-column schema.
    """

    target = "ln_solubility_mole_fraction"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "Malikov et al. 2026 Methods, Technical Validation and Usage Notes define no model evaluation metric. "
            "The paper recommends mole-fraction LogS, while Myunghwan explicitly requested natural log. "
            "Use fallback RMSE directly on ln mole fraction; identity scorer transformation, not RMSE on exp(target)."
        )
    )
    special_features = tuple(Smiles(column=column) for column in STRUCTURES)
    grouping = Grouping(
        on="solute_family",
        labels="per_sample",
        definition=(
            "Connected components of parent scaffolds, nonstereo/InChI/tautomer and neutral-parent identities, "
            "plus six source-validated salt/metal-core links. Scaffold prevalence uses distinct parent structures, "
            "not repeated measurement rows. All conditions of every solute remain together; prediction is per row."
        ),
    )
    splits_comment = """
        A new solute family is the held-out unit. All measurements of its compounds remain together across
        temperatures, proportions and papers. The native repeated grouped protocol is used. Parent structures
        remove only the library's defined inorganic/solvent fragments for grouping; shipped structures keep every
        fragment and stereochemistry. Ringless and oversized-scaffold chemicals receive individual identity keys
        under SPLIT-31; InChI, neutral-parent and tautomer links keep alternate representations in one
        component. Six explicit links keep source-named organic salts and porphyrin metal complexes with their
        observed cores, without a global largest-fragment rule. This is a
        row-scored cold-start regression, not temporal validation or a holdout of unseen solvents.
    """
    curation_comments = """
        - CC (2026-11-11, Myunghwan): ship this reviewed molecular-solvent task, with RMSE scored directly on
          ln mole-fraction solubility and whole-solute-family holdout. The documented source/context limits and
          both earlier exclusions are accepted. Build and commit explicitly requested; no predictor or split change.
        - Prediction point: before measuring the proposed solute at the selected temperature and initial solvent
          composition. Structures and experiment settings are inputs; measured solubilities are outcomes.
        - Myunghwan requested natural-log mole-fraction regression as the main candidate, another target only if
          actual qualification makes it unsuitable. We compute ln of the measured mole fraction, not another log
          of the source's already logarithmic column. Negative log targets are physically valid. The metric scores
          ln values directly; target_transform stays identity. No alternate target was selected by model scores.
        - First publication was Zenodo v1 on 2025-12-07 (record 17846307), verified from the official
          version metadata. The selected v3 release was published 2026-02-16 and the paper in March 2026;
          dataset year records the first release, not the updated version or paper year.
        - Source: Malikov et al., Scientific Data 2026, doi:10.1038/s41597-026-07047-z, Methods and Data Records.
          Literature search ended October 2025; measurements were at atmospheric pressure without additives.
          The pinned Zenodo v3 file, not the author repository, defines the actual input bytes.
        - The stable historical identifier bigsoldb_2 denotes MixtureSolDB here. Single-solvent BigSolDB is a
          distinct source/task. Earlier record links conflate them and are reconciled separately from renaming.
        - All three structures ship as typed canonical SMILES; fragments and stereochemistry remain. The benchmark
          computes the recommended RDKit descriptors/fingerprints. No learned or target-derived input is added.
        - Drop all four alternative linear/log solubility representations after constructing the sole target.
          Compound names, CAS, PubChem identifiers, FDA status, source DOI and endpoint flag are not predictors.
          Temperature and mixture fractions are numeric; Fraction_Type is categorical, preserving mass versus mole.
        - Sort solvent components by their canonical structures and exchange their proportions together. For a pure
          endpoint, both solvent fields become the active solvent, fractions become 1 and 0, and type becomes mole:
          the unused solvent and fraction convention have no physical meaning there. Keep pure-solvent conditions;
          never remove that cohort merely to avoid overlap. Remove exact input-target copies after this normalization,
          retaining distinct delivered ln outcomes without inventing an average. Exact ln equality also
          removes machine-decimal tails (at most two ULPs in the underlying mole fraction); this is delivered-
          space deduplication.
        - CC (2026-11-10, Myunghwan): restrict this task to molecular solvents. Exclude 1,309
          deduplicated active-polymer conditions (0.7833% of the prior curated table), since source PEG grades
          describe chain-length distributions without one exact molecular graph. These are valid measurements
          outside the selected task population, not invalid targets. Normalize endpoints first: keep molecular
          pure-solvent rows whose unused zero-share source component is polymer. Drop the now-constant grade
          columns (CLEAN-5). This bounded population decision serves P3 (USE-1/6); it is not a general missing-row
          deletion policy or a model-capacity remedy. Preserve original raw bytes and prior-cohort evidence.
        - Group metadata additionally joins neutralized parent identities and six explicit observed core relations:
          sorafenib/tosylate, dipyridamole/ditosylate, arginine/two organic salts and two porphyrin/metal-complex pairs.
          The source calls dipyridamole ditosylate only 'p-toluene sulfonate'; its graph contains the full drug and
          two tosylates. These source-supported links affect grouping only, not the shipped salt/metal structures.
        - Distinct measurements of one solute are legitimate dependencies; all remain in one held-out family.
          Source overlap with older compilations is a collection-level issue, not proof that compilation names
          identify independent data. Publication dates do not establish a prospective label-availability split.
        - Repair 110 dapsone rows from DOI 10.1016/j.molliq.2021.117403: ethyl acetate/water is ethyl
          acetate/ethanol. All ten zero-ethyl-acetate endpoints exactly match that DOI's pure ethanol values.
          Jouyban et al. 2022, doi:10.1016/j.molliq.2021.118223, Introduction, explicitly lists
          "ethyl acetate + ethanol" for that experiment; Cysewski et al. 2024, doi:10.3390/molecules29081743,
          section 2.2 independently identifies the same organic pair. Guard the source/solute/solvents/count/grid,
          replace only the second solvent identity, and preserve target, fractions and temperatures; the other
          330 rows of that DOI remain untouched. Original experimental SI and interior cells were not recovered;
          this bounded metadata repair is supported by the published descriptions and exact endpoint comparison.
        - CC (2026-11-10, Myunghwan): exclude the 22 nominal propylene-glycol/water source rows
          from DOI 10.1021/je3009842 (11 each diazepam and clonazepam, 298.2 K). Their nominal pure-PG
          endpoints match PEG-200 endpoints exactly while their nominal aqueous endpoints strongly disagree.
          The original mixture table was not recovered; the NIST numeric JSON returned HTTP 403. Do not guess
          replacement compositions. A bounded source-provenance filter protects input fidelity (PROV-13,
          USE-6/8); it is not target-tail trimming, a noise-floor assertion or exclusion of the entire paper.
          All 810 solutes and 606 families remain after both curator-selected exclusions.
        - Exception to CLEAN-11 (2026-11-10, Myunghwan): exclude only the 22 source-composition-uncertain
          PG/water observations above. Source comparisons show the inputs may describe the wrong mixture;
          no faithful replacement mapping was recoverable. Keeping unknown mixture identities would weaken the
          planned-input task (P3 USE-6/8, P5 PROV-13). This is not a target-outlier or general missing-row rule.
        - The source has no systematic per-row uncertainty or experimental-method field. Contradictory outcomes
          can reflect unrecorded conditions or extraction errors; their presence is reported, not called a measured
          MixtureSolDB noise floor using BigSolDB's repeatability number.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        path = raw_dir / "raw/MixtureSolDB.csv"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == RAW_SHA256, "Pinned release bytes changed"
        return pd.read_csv(path)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        source = raw.copy()
        dapsone = source["SMILES_Solute"].eq("Nc1ccc(S(=O)(=O)c2ccc(N)cc2)cc1")
        paper = source["Source"].eq("10.1016/j.molliq.2021.117403")
        repair = dapsone & paper & source["Solvent1"].eq("ethyl acetate") & source["Solvent2"].eq("water")
        assert repair.sum() == 110
        assert (dapsone & paper).sum() == 440
        block = source.loc[repair]
        assert block["SMILES_Solvent1"].eq("CCOC(C)=O").all()
        assert block["SMILES_Solvent2"].eq("O").all()
        assert block["Fraction_Type"].eq("mass").all()
        assert block["Temperature_K"].nunique() == 10
        assert block["Fraction_Solvent1"].nunique() == 11
        endpoints = block.loc[block["Fraction_Solvent1"].eq(0)].set_index("Temperature_K")
        ethanol = source.loc[dapsone & paper & source["Solvent1"].eq("ethanol") & source["Fraction_Solvent1"].eq(1)]
        ethanol = ethanol.set_index("Temperature_K")
        assert len(endpoints) == len(ethanol) == 10
        assert endpoints["Solubility(mole_fraction)"].equals(ethanol.loc[endpoints.index, "Solubility(mole_fraction)"])
        source.loc[repair, "Solvent2"] = "ethanol"
        source.loc[repair, "SMILES_Solvent2"] = "CCO"
        suspect = (
            source["Source"].eq("10.1021/je3009842")
            & source["Solvent1"].eq("propylene glycol")
            & source["Solvent2"].eq("water")
        )
        assert suspect.sum() == 22
        source = source.loc[~suspect].copy()
        df = source.loc[:, list(INPUTS)].copy()
        for number in (1, 2):
            column = f"SMILES_Solvent{number}"
            missing = df[column].eq("-")
            df[f"PolymerGrade_Solvent{number}"] = source[f"Solvent{number}"].where(missing, "molecular")
            df[column] = df[column].mask(missing, pd.NA)
        x = pd.to_numeric(source["Solubility(mole_fraction)"], errors="coerce")
        valid = np.isfinite(x) & x.gt(0) & x.lt(1)
        df = df.loc[valid].copy()
        df[self.target] = np.log(x.loc[valid])
        for column in STRUCTURES:
            df[column] = canonical_values(df[column])
        assert (
            df[["SMILES_Solute", "Temperature_K", "Fraction_Solvent1", "Fraction_Solvent2", "Fraction_Type"]]
            .notna()
            .all()
            .all()
        )
        assert df["Fraction_Type"].isin(["mole", "mass"]).all()
        assert df["Temperature_K"].gt(0).all()
        assert df[["Fraction_Solvent1", "Fraction_Solvent2"]].ge(0).all().all()
        assert df[["Fraction_Solvent1", "Fraction_Solvent2"]].le(1).all().all()
        assert np.allclose(df["Fraction_Solvent1"] + df["Fraction_Solvent2"], 1, atol=1e-6)
        key1 = df["SMILES_Solvent1"].fillna("polymer:" + df["PolymerGrade_Solvent1"])
        key2 = df["SMILES_Solvent2"].fillna("polymer:" + df["PolymerGrade_Solvent2"])
        swap = key1.gt(key2)
        for left, right in [
            ("SMILES_Solvent1", "SMILES_Solvent2"),
            ("Fraction_Solvent1", "Fraction_Solvent2"),
            ("PolymerGrade_Solvent1", "PolymerGrade_Solvent2"),
        ]:
            df.loc[swap, [left, right]] = df.loc[swap, [right, left]].to_numpy()
        pure = df["Fraction_Solvent1"].isin([0, 1])
        active = df["SMILES_Solvent1"].where(df["Fraction_Solvent1"].eq(1), df["SMILES_Solvent2"])
        grade = df["PolymerGrade_Solvent1"].where(df["Fraction_Solvent1"].eq(1), df["PolymerGrade_Solvent2"])
        df.loc[pure, "PolymerGrade_Solvent1"] = grade.loc[pure]
        df.loc[pure, "PolymerGrade_Solvent2"] = grade.loc[pure]
        df.loc[pure, "SMILES_Solvent1"] = active.loc[pure]
        df.loc[pure, "SMILES_Solvent2"] = active.loc[pure]
        df.loc[pure, "Fraction_Solvent1"] = 1.0
        df.loc[pure, "Fraction_Solvent2"] = 0.0
        df.loc[pure, "Fraction_Type"] = "mole"
        # Population is defined by the active solvents after endpoint normalization.
        molecular = df[["SMILES_Solvent1", "SMILES_Solvent2"]].notna().all(axis=1)
        df = df.loc[molecular].drop(columns=["PolymerGrade_Solvent1", "PolymerGrade_Solvent2"])
        df = df.drop_duplicates()
        df["solute_family"] = solute_groups(df["SMILES_Solute"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["Fraction_Type"], string=["solute_family"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        return [
            Decision(
                title="Pinned release and row accounting",
                why="Counts are measured from verified v3 bytes. No new outcome averaging or target sweep.",
                evidence=pd.DataFrame(
                    {
                        "quantity": ["source rows", "curated measurements", "solute structures", "solute families"],
                        "count": [len(raw), len(df), df.SMILES_Solute.nunique(), df.solute_family.nunique()],
                    }
                ),
            )
        ]
