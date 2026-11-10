"""Curated dataset definition for `chromophore_optical_properties_db`. Evidence: README.md."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Smiles,
    TaskSummary,
    canonical_smiles,
    scaffold_groups,
)
from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize

RAW_FILE = "raw/DB_for_chromophore_v3.csv"
RAW_SHA256 = "f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c"


def canonical_values(values: pd.Series, *, stereo: bool = True) -> pd.Series:
    """Canonicalize distinct structures once while preserving source-row indices."""
    unique = pd.Series(values.dropna().unique(), dtype="string")
    mapping = dict(zip(unique, canonical_smiles(unique, stereo=stereo), strict=True))
    return values.map(mapping).astype("string")


class ChromophoreOpticalPropertiesDb(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="At what wavelength will a proposed dye have its first absorption peak in a specified environment?",
        use_case=(
            "A chemist screens proposed chromophore structures and their solvent or host environments before "
            "synthesis and spectroscopy, to choose candidates with useful light absorption."
        ),
        row="One literature-reported dye and environment measurement with a recorded first absorption-peak wavelength.",
        predicted="The first absorption-peak position, measured in nanometres, without a target transformation.",
        known="The dye structure and solvent or host structure, or the source's gas-state designation.",
        split=(
            "Chemical scaffold groups of dyes are held out, with every environment and measurement of each dye "
            "kept together. Solvents may recur across training and testing."
        ),
        changes=(
            "Use the absorption target alone, omit other measured optical outcomes and provenance identifiers, "
            "canonicalize the structures, remove duplicate input-target records and replace random-row splitting "
            "with dye scaffold groups. Decode gas separately from a molecular solvent."
        ),
        fit="approximate",
        fit_reason=(
            "The structures are available before measurement, but literature selection and unrecorded experimental "
            "conditions limit transport to new designs. The archive combines solutions, hosts and neat solids; "
            "a structure alone does not specify every physical condition of the future measurement."
        ),
    )
    unique_name = "chromophore_optical_properties_db"
    year = "2020"
    domain = "chemistry & material science"
    source = "Other"
    source_url = "https://doi.org/10.6084/m9.figshare.12045567.v3"
    license = "CC BY 4.0"
    download_description = """
        Download the publisher's v3 CSV (file 49887156), not the unversioned search webpage:

        mkdir -p local-data-warehouse/chromophore_optical_properties_db/raw
        curl -L --fail https://ndownloader.figshare.com/files/49887156 -o local-data-warehouse/chromophore_optical_properties_db/raw/DB_for_chromophore_v3.csv

        Publisher MD5: 565dbb010480d94e8bb41af1bfb75ea8. SHA256:
        f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c.
        The downloaded CSV has 20,836 rows; the 2020 paper's 20,236 rows describe v2.
    """
    bibtex = """
        @article{joung2020experimental,
          title={Experimental database of optical properties of organic compounds},
          author={Joung, Joonyoung F. and Han, Minhi and Jeong, Minseok and Park, Sungnam},
          journal={Scientific Data},
          volume={7},
          pages={295},
          year={2020},
          doi={10.1038/s41597-020-00634-8}
        }
    """
    curation_comments = """
        - Prediction point: before synthesizing or measuring a candidate dye in its planned solvent, host or gas
          environment. Only the two structures and decoded medium state enter prediction.
        - The publisher's Figshare v3 file contains 20,836 rows and 17,703 nonmissing absorption values. Pin its exact
          bytes rather than reuse the paper's or metadata card's historical counts. Target values stay in nm.
        - The v3 source population includes small nonorganic species, metal complexes and structures with up to
          225 nonhydrogen atoms. Its scope is broader than the historical organic/150-atom description. Preserve
          published rows with absorption labels unless an origin-supported correction establishes an error.
        - Emission peak, both absorption/emission bandwidth representations, quantum yield, lifetime and extinction
          coefficient are other experimental outcomes, not inputs known at this prediction point. Tag is a row
          number and Reference a source DOI; both leave the inputs. Molecular weight leaves as a structure-derived
          quantity rather than an independent measurement needed by this task.
        - Both structures ship as typed SMILES in RDKit's canonical form, with fragments and stereochemistry kept.
          The benchmark encodes them; no descriptor or fingerprint chosen by the curator ships as a raw feature.
        - The source uses gas instead of solvent SMILES in 20 labeled rows. Preserve those rows: medium_state is gas
          and Solvent_SMILES is missing because there is no solvent molecule. When the source writes the same
          structure for dye and environment it denotes a neat solid; other structures can denote solvent or host.
          The latter state remains solvent or host because the release supplies no independent phase column.
        - Remove exact repeated model-input and target records after canonicalization. Distinct observed wavelengths
          for one dye/environment remain separate measurements: laboratory conditions and literature disagreement
          may reflect physical-condition variation or literature/transcription disagreement; this cause is not verified.
          No averaging or target-dependent conflict filtering is invented.
        - Input/target deduplication removes 193 labeled records. Only 50 excess labeled rows also match every raw
          field except Tag; the other 143 removals are a weighting policy, not proven copies of physical experiments.
          Myunghwan approved that weighting on 2026-11-10 separately from retaining differing wavelengths.
        - Every solvent row and stereochemical form of a dye remains in one scaffold group. Groups are computed on
          distinct non-stereochemical dye structures, so repeated solvent measurements do not change the ten-percent
          scaffold fallback. Ringless dyes and dyes in an oversized scaffold are held together by dye structure.
          Scaffold groups joined by a nonempty dye InChIKey or canonical tautomer identity are merged, keeping aliases together.
          Solvents can recur. This tests new dye families, not new solvents or complete chemical novelty.
        - The source paper compiles experimental values, not simulated quantum-chemistry labels. Its model follow-up
          (JACS Au 2021, doi:10.1021/jacsau.1c00035) reports RMSE for absorption peak positions in nm. Its random-row
          scores and expanded database are not qualification results for our grouped release.
        - Literature selection and missing temperature, concentration and some physical-state detail remain limits;
          no row is removed simply for an extreme wavelength. The 17,703 observed targets are positive and finite.
        - Curator decision (2026-11-10, Myunghwan), issues 1A and 2A: keep one row per canonical input and wavelength,
          and retain the 61 input sets with differing published responses. Apply the genuine-ambiguity clause for
          continuous measurements under incomplete conditions; the cause of each disagreement remains unverified.
          Grouping does not validate labels. Repair any later demonstrated source error from its original reference.
        - Myunghwan checked the declared fallback RMSE in untransformed nm and accepted the gas/no-solvent warning
          on 2026-11-10. These are scientific review decisions; no model-only gas accuracy claim follows.
    """
    accepted_check_warnings = {
        "dataset_smiles_column": (
            "Accepted by Myunghwan on 2026-11-10: the 20 gas-state observations have no solvent molecule. "
            "Solvent_SMILES is therefore absent by definition, with medium_state=gas explicitly retained; "
            "these are not rows with an unexplained missing molecular input."
        ),
    }
    target = "Absorption max (nm)"
    problem_type = "regression"
    special_features = (Smiles(column="Chromophore_SMILES"), Smiles(column="Solvent_SMILES"))
    metric = Metric.fallback(
        reason=(
            "The 2020 Scientific Data descriptor defines no predictive metric. Joung et al. 2021 "
            "(https://doi.org/10.1021/jacsau.1c00035) report RMSE and Pearson R-squared and optimize joint "
            "standardized MSE over seven targets; a unique absorption-only model-selection metric is not "
            "established. Use regression fallback RMSE on the retained absorption wavelengths in nm."
        )
    )
    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition=(
            "Dye Bemis-Murcko ring scaffolds define chemical series held out before synthesis, following the "
            "source's proposed-new-chromophore use. Compute groups on distinct dye structures without stereo; "
            "all environments of a dye stay together. Ringless dyes or each dye in a scaffold exceeding ten "
            "percent of distinct dyes form individual dye groups. Merge groups joined by an identical nonempty dye InChIKey or canonical tautomer identity. "
            "Solvent structures do not define the groups."
        ),
    )
    splits_comment = """
        Recommended repeated grouped folds hold out dye scaffold groups. All observations of one dye remain
        together; source solvent and host structures may occur on both sides. A chemical with a different scaffold
        can still be a close analogue. The group key is metadata and is never a predictor.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        path = raw_dir / RAW_FILE
        if hashlib.sha256(path.read_bytes()).hexdigest() != RAW_SHA256:
            raise ValueError("Source CSV differs from the pinned Figshare v3 release")
        return pd.read_csv(path)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.loc[raw[self.target].notna()].copy()
        # Gas is an observed physical state, not an invalid molecular structure to discard.
        gas = df["Solvent"].eq("gas")
        dye = canonical_values(df["Chromophore"])
        solvent = canonical_values(df["Solvent"].mask(gas))
        state = pd.Series("solvent or host", index=df.index, dtype="string")
        state = state.mask(gas, "gas").mask(~gas & dye.eq(solvent).fillna(False), "neat solid")
        df = pd.DataFrame(
            {"Chromophore_SMILES": dye, "Solvent_SMILES": solvent, "medium_state": state, self.target: df[self.target]},
            index=df.index,
        )
        df = df.drop_duplicates(subset=["Chromophore_SMILES", "Solvent_SMILES", "medium_state", self.target])
        # The fallback share counts distinct molecules, not their repeated measurements across solvents.
        key = canonical_values(df["Chromophore_SMILES"], stereo=False)
        unique = pd.Series(key.unique(), dtype="string")
        groups = dict(zip(unique, scaffold_groups(unique), strict=True))
        # Different SMILES/scaffolds can name the same InChI-normalized dye. Join their groups without labels.
        parent = {group: group for group in groups.values()}

        def find(group: str) -> str:
            while parent[group] != group:
                parent[group] = parent[parent[group]]
                group = parent[group]
            return group

        identities: dict[str, str] = {}
        for structure in unique:
            identity = Chem.MolToInchiKey(Chem.MolFromSmiles(structure)) or structure
            group = groups[structure]
            if identity in identities:
                left, right = find(group), find(identities[identity])
                parent[max(left, right)] = min(left, right)
            else:
                identities[identity] = group
        # Standard InChI does not normalize every tautomer; use the independent RDKit tautomer key as well.
        enumerator = rdMolStandardize.TautomerEnumerator()
        tautomers: dict[str, str] = {}
        for structure in unique:
            identity = Chem.MolToSmiles(enumerator.Canonicalize(Chem.MolFromSmiles(structure)))
            group = groups[structure]
            if identity in tautomers:
                left, right = find(group), find(tautomers[identity])
                parent[max(left, right)] = min(left, right)
            else:
                tautomers[identity] = group
        groups = {structure: find(group) for structure, group in groups.items()}
        return df.assign(scaffold=key.map(groups))

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        del df
        return FeatureTypes(categorical=["medium_state", "scaffold"])
