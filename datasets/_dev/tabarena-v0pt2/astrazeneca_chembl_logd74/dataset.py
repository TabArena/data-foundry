"""Curated dataset definition for `astrazeneca_chembl_logd74` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from data_foundry.definition import (
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
    drop_columns,
    scaffold_groups,
)
from data_foundry.special.chemistry import RDKIT_VERSION

ACTIVITY_FILES = tuple(f"chembl_activities_{offset}.json" for offset in (0, 1000, 2000, 3000, 4000))
"""The five pages of the ChEMBL activity endpoint for assay CHEMBL3301363, 1,000 activities each (4,200 in all)."""

ASSAY = "CHEMBL3301363"
"""AstraZeneca's shake-flask octan-1-ol/water (pH 7.4) distribution assay, the one assay of this task."""

KEPT = [
    "molecule_chembl_id",
    "canonical_smiles",
    "standard_type",
    "standard_value",
    "parent_molecule_chembl_id",
]
"""The fields of an activity record the definition reads; the rest describe the assay, not the measurement. The
parent id is read only as the drift guard of `_clean`: it differs from the molecule id exactly on the salt, hydrate
and solvate records."""

PAGE_SHA256 = {
    "chembl_activities_0.json": ("00e62a2f745aa303985ae3d292771314da050565aab6bc6768817ea98b99fd7f", 1478910),
    "chembl_activities_1000.json": ("a1e6188a34b5b7e6c3d3a435b42435d8c760db77f8d77062b6e623be8637ae24", 1478670),
    "chembl_activities_2000.json": ("bceb507171223e40e18df0d179fe399fe226abbd63d87569ca2d4105c2824058", 1479767),
    "chembl_activities_3000.json": ("a5fc21826b031460daccacf777ec9fc7e45bdfdd060bdcc5b4eb4c0cfb7e3a41", 1476981),
    "chembl_activities_4000.json": ("dc3d735269b01a3a8c3758c55a20571d098648f8ef669b0499d3e385b668660e", 296116),
}
"""The sha256 and the byte size of each page as downloaded on 2026-11-25, so the endpoint's answer can be compared
with the one this definition was written on (PROV-8; the endpoint serves the current release and is not pinned)."""

SALT_FORMS = {
    "CHEMBL1355736": "CHEMBL190",  # theophylline monohydrate
    "CHEMBL1409": "CHEMBL814",  # fluvoxamine maleate
    "CHEMBL3545252": "CHEMBL92",  # docetaxel trihydrate
    "CHEMBL5315124": "CHEMBL33",  # levofloxacin hemihydrate
    "CHEMBL5416410": "CHEMBL1421",  # dasatinib hydrate
    "CHEMBL5483011": "CHEMBL115",  # indinavir hydrate
}
"""The six activities ChEMBL records on a salt, hydrate or solvate rather than on the parent compound, with the
parent they point at. `_clean` asserts this exact set: a later release re-pointing another activity changes a
structure, and so a feature, which the count asserts cannot see."""

MERGED_IDS = {
    "CHEMBL1626": ("CHEMBL1626", "CHEMBL315157"),  # clemastine, both centres defined and both undefined
    "CHEMBL170": ("CHEMBL97", "CHEMBL522505"),  # quinine and quinidine, epimers at the carbinol centre
    "CHEMBL273575": ("CHEMBL273575", "CHEMBL51697"),  # nomifensine, the racemate and one enantiomer
    "CHEMBL499": ("CHEMBL173706", "CHEMBL499"),  # timolol, undefined and (S)
    "CHEMBL517712": ("CHEMBL9751", "CHEMBL517712"),  # atropine, fully undefined and the tropane-defined form
}
"""The five ids that carry two activities each, with the two compounds the deposit registered for them.

They are not the assay measuring one compound twice. In CHEMBL_20 each pair was two separately registered
compounds, a stereo-defined form and an undefined or differently defined one, each with its own measured value;
MoleculeNet's copy of that release still carries both, under the two ids and with the two structures, which is how
the pairing was read: for each merged id, the partner is the member of its 2D structure group that no longer carries
an activity of its own. ChEMBL has since merged each pair onto one id and one structure, so today's download answers
with two activities and one SMILES and no longer says which value belongs to which compound. The merge did not take
in every stereoisomer: nomifensine's other enantiomer (CHEMBL400964) and a third cinchona alkaloid (CHEMBL1294) keep
their own id, their own activity and their own row here. `_clean` drops all ten merged activities
(curation_comments)."""


def group_structures(smiles: pd.Series) -> pd.Series:
    """Each structure as the scaffold's input: without common salts and solvents, and without repeated identical
    fragments.

    RDKit's `FragmentRemover` drops the fragments of its list of common salts and solvents (halides, metal ions,
    water, sulfate, ammonia, mesylate and others) and keeps organic counter-ions, which can be a compound of their
    own (molecules.md). It leaves a structure that writes the parent twice, as a hemihydrate does, with both copies,
    so the identical fragments are de-duplicated afterwards and a salt, hydrate or solvate form reduces to its
    parent. The shipped SMILES stays whole (CLEAN-24): this form is only the group key.

    Raises:
        ValueError: Another RDKit version is installed.
    """
    from rdkit import Chem, RDLogger, __version__
    from rdkit.Chem.MolStandardize import rdMolStandardize

    if __version__ != RDKIT_VERSION:
        msg = f"The group key needs RDKit {RDKIT_VERSION}, found {__version__}."
        raise ValueError(msg)
    RDLogger.DisableLog("rdApp.*")
    remover = rdMolStandardize.FragmentRemover()
    keys = []
    for value in smiles:
        molecule = Chem.MolFromSmiles(value)
        stripped = remover.remove(molecule)
        if stripped is None or stripped.GetNumAtoms() == 0:
            stripped = molecule  # a structure that is nothing but solvent keeps its own fragments
        fragments = {Chem.MolToSmiles(part) for part in Chem.GetMolFrags(stripped, asMols=True)}
        keys.append(".".join(sorted(fragments)))
    return pd.Series(keys, index=smiles.index, dtype="string", name="group_structure")


class AstrazenecaChemblLogd74(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How lipophilic is a compound: what is its octanol/water distribution coefficient at pH 7.4?",
        use_case=(
            "Before a compound is made, or before a made one is progressed, a medicinal chemist or DMPK scientist "
            "estimates its logD7.4 from the structure, to decide which compounds of a design idea are worth "
            "synthesising and testing: lipophilicity drives membrane permeability, solubility, metabolic clearance "
            "and off-target binding, so it is one of the numbers a design round is steered by."
        ),
        row=(
            "One compound AstraZeneca measured and later disclosed, with its logD7.4 from one shake-flask protocol "
            "(4,190 compounds; ChEMBL document CHEMBL3301361, assay CHEMBL3301363)."
        ),
        predicted=(
            "The measured logD7.4: the log of the compound's concentration ratio between octan-1-ol and pH 7.4 "
            "buffer. The assay reports -1.5 to 4.5, and the measured values span exactly that range (median 2.36)."
        ),
        known="The compound's chemical structure, as a SMILES string. Nothing is measured on it yet.",
        split=(
            "Whole chemical series are held out: compounds that share a ring skeleton stay on one side, so a test "
            "compound belongs to a series this laboratory never measured."
        ),
        changes=(
            "We take the assay's 4,200 activities from ChEMBL, the source of the deposit, rather than from "
            "MoleculeNet's mirror of them, which strips salts and restandardises tautomers. We drop the ten "
            "activities of the five compound pairs ChEMBL has merged onto one id since the deposit, split by "
            "chemical series instead of at random, and ship the structure as a SMILES string in RDKit's canonical "
            "form."
        ),
        fit="direct",
        fit_reason=(
            "The structure is all a chemist has before synthesis, and the prediction stands in for the assay, so "
            "the assay's reporting range is the range a user predicts in. Two limits, measured in the notes: the "
            "compounds are AstraZeneca's patent-disclosed lead-optimisation chemistry, narrower than a chemist's "
            "design space, and the model is shrunk at both ends of the range, where compounds are flagged."
        ),
    )

    # Dataset
    unique_name = "astrazeneca_chembl_logd74"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.6019/CHEMBL3301361",
            license="CC BY-SA 3.0",
            year="2015",
            bibtex="""
                @misc{wenlock2015experimental,
                  title = {Experimental in vitro {DMPK} and physicochemical data on a set of publicly disclosed compounds},
                  author = {Wenlock, Mark and Tomkinson, Nicholas},
                  year = {2015},
                  howpublished = {Deposited data set {CHEMBL3301361}, {ChEMBL} release {CHEMBL\\_20}},
                  doi = {10.6019/CHEMBL3301361},
                }
            """,
        ),
    )
    data_tags = ()
    time_basis = TimeBasis(
        "UnseenGroup",
        """
            A chemist asks for a compound that has not been made, usually from a series this laboratory has not
            measured, so the split holds out whole chemical series: what matters is which chemistry a model has
            seen, not when. The compounds do carry a time dimension, and the record's collection facts record it
            (`Samples: Over Time`, `Time: Dated`): a compound's first public disclosure is dated by the parent
            source and matched to the row by the molecule id. That year, read from a compound's other ChEMBL
            documents, follows the molecule id at Spearman 0.912 over the 146 datable of 160 sampled compounds
            (median year per eighth of the id range 1994 to 2013, span 1974-2022). What it dates is the compound's
            first disclosure and not its measurement: all 4,200 activities of this assay entered in one 2015
            deposit, and this document carries no year of its own. Three measurements say that order does
            not earn a temporal split. Eight blocks of 524 compounds held out of it at the same training size score
            R^2 0.526 (the newest) to 0.705 (a middle one), and the score tracks the share of close training
            analogs (Pearson 0.81) rather than recency, so a forward split is harder only where the chemistry is
            isolated; the target does not move along the order (Spearman 0.028), as logD7.4 is a fixed property of
            the molecule under one protocol; and every value arrived in one 2015 batch (contiguous record ids, one
            document, one assay). That batch is what sets this deposit apart from qsar_tid_11, which read the same
            first-publication years and did change its split on them: there the catalogue grew with the years,
            while here a compound's literature year is not when its measurement entered. The split therefore
            cannot test how the model would age as the chemistry of a portfolio moves on.
        """,
    )
    split_leaf = "L-EXP.kind"
    download_description = """
        The data is AstraZeneca's deposition in ChEMBL: document CHEMBL3301361, assay CHEMBL3301363, 4,200 activities
        of standard type LogD7.4. We read them from the ChEMBL web API in five pages of 1,000 (downloaded 2026-11-25
        from release CHEMBL_37 of 2026-05-01; `https://www.ebi.ac.uk/chembl/api/data/status.json` names the release).

        mkdir -p local-data-warehouse/astrazeneca_chembl_logd74 && for off in 0 1000 2000 3000 4000; do curl -sS -L -o local-data-warehouse/astrazeneca_chembl_logd74/chembl_activities_$off.json "https://www.ebi.ac.uk/chembl/api/data/activity.json?assay_chembl_id=CHEMBL3301363&limit=1000&offset=$off"; done

        The deposit is release CHEMBL_20 of 2015-01-14; the endpoint answers from CHEMBL_37, and the two are not the
        same data. Between them ChEMBL re-pointed four of these 4,200 activities from the compound onto a hydrate
        record registered after the deposit (CHEMBL5483011, CHEMBL5416410, CHEMBL5315124, CHEMBL1355736), which
        MoleculeNet's 2015-era copy still carries under the parent id with the identical value; the other two
        multi-fragment records (CHEMBL3545252, CHEMBL1409) are the deposit's own. Nothing in the endpoint's answer
        dates a row, so the drift is found only by comparison.

        The endpoint serves the current release, so it is not pinned: a later release can revise a structure or add
        an activity. `_clean` asserts the 4,200 activities, the one standard type, the five ids that carry two
        activities (`MERGED_IDS`), the 4,190 compounds that remain and the six activities whose
        `parent_molecule_chembl_id` differs from their `molecule_chembl_id` (`SALT_FORMS`), so a further
        re-pointing or merge fails the check rather than changing a feature unseen. The sha256 and byte size of each
        page as downloaded are in `PAGE_SHA256`:

        00e62a2f745aa303985ae3d292771314da050565aab6bc6768817ea98b99fd7f  chembl_activities_0.json     (1,478,910 bytes)
        a1e6188a34b5b7e6c3d3a435b42435d8c760db77f8d77062b6e623be8637ae24  chembl_activities_1000.json  (1,478,670 bytes)
        bceb507171223e40e18df0d179fe399fe226abbd63d87569ca2d4105c2824058  chembl_activities_2000.json  (1,479,767 bytes)
        a5fc21826b031460daccacf777ec9fc7e45bdfdd060bdcc5b4eb4c0cfb7e3a41  chembl_activities_3000.json  (1,476,981 bytes)
        dc3d735269b01a3a8c3758c55a20571d098648f8ef669b0499d3e385b668660e  chembl_activities_4000.json  (296,116 bytes)

        MoleculeNet's copy of the same assay is downloaded as a cross-check and is not read by the definition
        (curation_comments):

        curl -sS -L -o local-data-warehouse/astrazeneca_chembl_logd74/Lipophilicity.csv https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/Lipophilicity.csv

        sha256 of Lipophilicity.csv: aed41590cb30609d51d8e08ad3ff06495a76e80e211358801f596b10da69bacd
    """
    curation_comments = """
        We start with the 4,200 activities of assay CHEMBL3301363 in ChEMBL: AstraZeneca's octan-1-ol/water (pH 7.4) shake-flask distribution coefficient, deposited as document CHEMBL3301361 ("Experimental in vitro DMPK and physicochemical data on a set of publicly disclosed compounds", Mark Wenlock and Nicholas Tomkinson, doc_type DATASET, release CHEMBL_20 of 2015-01-14, doi 10.6019/CHEMBL3301361). Each activity carries a compound id, the compound's structure as a SMILES string and the measured value. The assay description fixes the protocol and the reporting range: "ASTRAZENECA: Octan-1-ol/water (pH7.4) distribution coefficent measured by a shake flask method described in J. Biomol. Screen. 2011, 16, 348-355. Experimental range -1.5 to 4.5".

        - Prediction point: a compound that has not been through the assay, before it is made or before it is progressed. Its structure is known; no measurement on it exists. Only the structure ships.
        - Target: `logd74`, the measured value as deposited. It is a measurement, not a derived label, so nothing about the compound can be circular with it.
        - The reporting range is a selection on the target, not censoring within the rows (decision table): every value falls inside -1.5 to 4.5, and the ends carry 1 and 4 compounds against 36 and 135 in the outermost half-log bands, so there is no pile-up at a bound. Compounds whose logD7.4 fell outside the assay's range are not in the deposit at all; a user predicts the number the assay would report, which is the same range.
        - Five merged pairs, dropped (decision table): five ids carry two activities each (CHEMBL1626, CHEMBL170, CHEMBL273575, CHEMBL499, CHEMBL517712). The assay did not measure one compound twice. In CHEMBL_20 each of the five was two separately registered compounds, a stereo-defined form and an undefined or differently defined one, each with its own value: clemastine with both centres defined (3.48) and with neither (3.04, CHEMBL315157), quinine (2.16, CHEMBL97) and quinidine (2.26, CHEMBL522505), the nomifensine racemate (2.08) and one of its enantiomers (2.11, CHEMBL51697), timolol undefined (-0.35, CHEMBL173706) and (S) (-0.22), atropine fully undefined (-0.09, CHEMBL9751) and its tropane-defined form (-0.66). Each pair was read off its 2D structure group: the partner is the member that no longer carries an activity of its own. The merge did not take in every stereoisomer of these structures, and the ones it left keep their row here: nomifensine's other enantiomer (CHEMBL400964, 2.11) and a third cinchona alkaloid (CHEMBL1294, 2.21) still have their own ChEMBL id and their own measurement. MoleculeNet's copy of that release still carries both members of every pair, under the two ids and with the two structures, which is how the pairing was read. ChEMBL has merged each pair onto one id and one structure since, so today's download answers with two activities, one SMILES and no way to tell which value is which compound. Averaging them would put two different compounds in one row and quinine would carry quinidine's measurement; keeping both would pair two now-identical structures with targets up to 0.57 apart. The two structures cannot be recovered from this download, so all ten activities are dropped: 0.24% of the deposit, and 4,200 activities become 4,190 compounds.
        - Dropping those ten rows against SPLIT-26 (2026-11-26, Andrej; revised 2026-11-26 after the pairs were identified): the rule keeps the source's rows, and ten of them are not shipped. What the rule protects against is a curator quietly reshaping the source's task; here the source's own rows can no longer be reconstructed from the source, because ChEMBL has merged the two registrations and serves one structure for both values. The three ways to ship them are all worse than dropping: one averaged row makes a compound that was never measured and gives quinine quinidine's value; two rows pair identical features with targets up to 0.57 apart, an error floor no model can avoid and one that scores five compounds twice; and restoring the two structures means reading them out of MoleculeNet's copy, the processed mirror this definition rejects for exactly that reason. The cost is bounded and named: 10 of 4,200 activities, 0.24%, five of them compounds a benchmark elsewhere does carry. The earlier reading of these five as protocol replicates, and the averaging it justified, was wrong on the facts; this bullet replaces it.
        - The fit is direct, and these are its limits (USE-8). The range is the assay's own: a compound outside -1.5 to 4.5 has no logD7.4 from this protocol, so the chemist who runs the shake flask instead of asking the model meets the same bound, and the decision the use case names is made at a threshold inside the range. The selection that does not mirror the setting is the population: these are the compounds AstraZeneca disclosed in patents from programmes it advanced that far (median molecular weight 388, three aromatic rings, TPSA 80, 82% of them within Lipinski's rule of five), so early exploratory ideas and newer modalities are under-represented. That shifts which structures a model is trained on, not what logD7.4 is of a given structure, and the scaffold split is what tests against it: on the nine shipped folds the model scores RMSE 0.747 on test compounds with no close training analog against 0.570 on those with one. The second limit is at the ends of the range, where the too-lipophilic and too-polar flags are set: an untuned LightGBM under-calls by 0.74 above logD 3.5 and over-calls by 1.00 below 0, and nothing above 4.5 exists in the deposit to teach it. Against those, a single measurement of this assay has an SD of 0.106, matching AstraZeneca's published 0.07 to 0.10: the shipped compounds hold 47 pairs differing only by having every stereocentre inverted, and the SD of their differences over root two is 0.106 with the one 1.55 pair left out that the stereoisomer decision argues is a label error (0.191 with it). The same model reaches RMSE 0.711, so the task is not noise-limited.
        - Other assays of the same deposit (pKa, aqueous solubility, plasma protein binding, intrinsic clearance) are sibling tasks on the same compounds (PROV-7; `hepatocyte_clearance_astrazeneca`), not features: they are measurements that do not exist for a compound that has not been made.
        - Stereoisomers stay (molecules.md, LEAK-19 as applied to qsar_tid_11): 166 compounds in 76 groups share a 2D structure with another compound once the salts and solvents are off, and differ only in stereochemistry, each with its own measured value. All 4,190 full InChIKeys are distinct, so there are no tautomer copies either. They share a scaffold and never straddle the split; a 2D encoding cannot tell them apart, so their spread bounds the error such a model can reach on them. That bound is 0.5 or less: the median spread is 0.08, only three of the 105 within-group pairs exceed 0.5, and the largest spread, 1.55, is a label error rather than a floor (its two compounds are enantiomers, whose logD7.4 must be identical in an achiral system; decision table).
        - The structure ships as `SMILES` (CLEAN-24), in RDKit's canonical form (`canonical_smiles`), every fragment kept and stereochemistry kept, declared in `special_features` so a benchmark encodes it as a structure and never as text. Six records hold more than one fragment: four hydrates, one hemihydrate written as two parent molecules and a water (CHEMBL5315124), and one maleate salt (CHEMBL1409). The group key is the structure without them (`group_structures`): RDKit's `FragmentRemover` drops the common salts and solvents and keeps the organic counter-ion of the maleate, and the identical fragments of the hemihydrate are de-duplicated afterwards, so each of the six groups with its parent. `FragmentRemover` alone does not: it leaves the hemihydrate's two parent copies, so the scaffold is still the parent's scaffold written twice and the check run on 2026-11-25 reproduced the old 2,414 groups for that reason (LEAK-17).
        - The six multi-fragment records ship whole, so RDKit reads them whole, and for them the encoded descriptors are the substance's and not the compound's: MolLogP 0.79 against the compound's 3.26 for docetaxel trihydrate (CHEMBL3545252, logD 3.40), 2.26 against 1.54 for the hemihydrate, and 0.82 to 0.83 too low on each of the three remaining hydrates; the maleate's descriptors are the salt's, which is the substance the deposit records. MolLogP is one of the descriptors the recommended encoding computes, and on its own it is no model of this task: a random forest on MolLogP alone loses to the training mean on every one of the nine folds (R^2 -0.165). What matters here is that its value on these six rows is the substance's and not the compound's, so a benchmark that strips solvents itself will get other values on them. Four of the six are also not the deposit's structures: ChEMBL re-pointed those activities (CHEMBL5483011, CHEMBL5416410, CHEMBL5315124, CHEMBL1355736) onto hydrate records registered after CHEMBL_20, while MoleculeNet's 2015-era copy still carries them under the parent id with the identical value (download_description). They are kept whole and unrepaired by decision (2026-11-26): the six rows are 0.14% of the set and bound the effect on the score at about 0.0014 on the declared MAE per fold (about 0.001 RMSE) even if each were predicted a full log worse, the group key already reduces them to their parent so no split is affected, and a repair would add four parent structures that the download does not carry. The cost is named rather than removed: on those four rows the structure we publish is the hydrate ChEMBL now records and not the one the deposit published, and the descriptors a benchmark computes from them are the hydrate's.
        - Split (SPLIT-31, leaf L-EXP.kind): grouped on the Bemis-Murcko scaffold of the group structure (`scaffold_groups`), 2,411 groups over 4,190 compounds, 1,863 of them a single compound. The largest scaffold is the bare benzene ring with 76 compounds (1.8%), far below the tenth at which a scaffold is broken up, and five compounds have no ring. The groups are mostly small rather than deep series: 77.3% hold one compound, 88.2% at most two, 139 hold five or more, and 44.5% of the compounds are alone. What the split buys is measured on the nine shipped folds: 22.7% of the test compounds have a close training analog (Tanimoto 0.7 or more, Morgan radius 2, 2,048 bits; fold SD 1.4), against 45.9% (SD 1.7) over nine random draws of the same test sizes. There is nothing to look up either way: a 1-NN prediction over the same fingerprints scores RMSE 1.243, worse than the training mean's 1.202.
        - One recipe behind the measured numbers (decided 2026-11-26): every figure these notes quote as a measurement comes from one run on the shipped 4,190 compounds and the shipped nine folds (three repeats of three grouped folds on the scaffold, the dimensions the splits are built with), so the numbers agree with each other and with the data that ships. The model is an untuned LightGBM regressor at its defaults on the recommended encoding of the SMILES column (`rdkit2d-maccs-ecfp4`, 1,407 columns), the baselines are the training mean of the same fold and a 1-NN over Morgan fingerprints (radius 2, 2,048 bits) with a close analog at Tanimoto 0.7, and R^2 is taken against that training mean. The assay's noise floor is the SD of the differences of the stereocentre-inverted pairs over root two, the estimator for a single measurement from duplicates, which is what AstraZeneca's published 0.07 to 0.10 also reports. An earlier reading of these notes put the floor at 0.211 by taking the SD of the pair differences themselves, which is the difference's spread and not a single measurement's, and counted 43 pairs where the shipped compounds hold 47. The claim that did not survive the re-run is MolLogP's: it was called the task's strongest single feature, and alone it loses to the training mean on all nine folds.
        - Dropped: `molecule_chembl_id`, an identifier (CLEAN-3, CLEAN-22), `standard_type`, which is `LogD7.4` on every row, and `parent_molecule_chembl_id`, read only by the drift assert. The other fields of an activity record are never read: they describe the assay rather than the measurement. The censoring and quality fields are constant across all 4,200 (`units`, `standard_relation`, `relation`, `upper_value`, `standard_upper_value` and `data_validity_comment` null, `standard_flag` 1, `potential_duplicate` 0; checked 2026-11-25). The ones that do vary carry nothing for the task: `activity_id` and `record_id` are running numbers, `molecule_pref_name` is on 651 of the rows and is given long after the assay, and `parent_molecule_chembl_id` differs from the molecule id on exactly the six salt, hydrate and solvate records, which is how they are found.
        - The raw file is sorted by the target, which the shipped frame must not inherit: `activity_id` rises monotonically and the values form two long non-decreasing runs (Spearman of `activity_id` against logD -0.348; a 40-bin step function of the raw row position fits the target at R^2 0.757 in sample, above an honest model's 0.659). The ids are never read and the pipeline shuffles the rows with seed 42 before shipping (CLEAN-23), so the shipped order carries nothing (Spearman of row position against the target 0.029); the shuffle is load-bearing and not housekeeping.
        - The labels are publicly recoverable, which matters for a pretrained baseline and for nothing else (EV-4, PROV-15): MoleculeNet's CSV of the same assay gives the exact value for 4,157 of the 4,190 compounds by canonical SMILES, ChemPile carries the structure-value pairs as pretraining text, and Zueco et al. (NeurIPS 2026) report MAE 0.0069 by looking the compounds up in ChEMBL. A score from a model that may have read them is not a generalisation score. It changes no decision here: the same work's nearest-neighbour baseline (MAE 0.787) says the split itself is not easy.
        - The metric is TDC's MAE in log units and not MoleculeNet's RMSE (decided 2026-11-26): the two benchmarks that made a task of this deposit declare different metrics, neither is the source's, and the one taken is the definer whose task design this definition follows (the scaffold hold-out, one prediction per compound), while MoleculeNet pairs its RMSE with the random split over its own reprocessed copy, which was rejected here. The choice does not change what the benchmark ranks: over eight candidate models the ranking is identical under MAE, RMSE, median absolute error, the share within 0.5 and within 1.0 log, Spearman and a 3-band accuracy (per-fold Kendall tau 1.00 on 7 of the 9 folds, 0.929 on the other two), and an L1-trained LightGBM does not win on MAE either (0.567 against 0.542). Every error in log units quoted elsewhere in these notes and in the splits comment is an RMSE over the nine shipped folds and is labelled as one; on the declared metric the untuned LightGBM of that comparison scores MAE 0.542.
        - MoleculeNet's Lipophilicity.csv is not read (PROV-4, molecules.md: a benchmark is a processed copy, go to the primary). It is the same assay with 4,200 rows, 4,200 distinct compound ids and 4,200 distinct structures, downloaded here only to compare: it shares 4,180 ids with today's ChEMBL and on every one of them the value agrees exactly (four of those ids now carry a second activity as well, the value of the compound ChEMBL has merged into them). 20 of its ids no longer carry this activity and ChEMBL carries 15 it does not, which is the ids drifting between releases: six of the twenty are the members of the five merged pairs that lost their own id (`MERGED_IDS`), four are compounds whose activity ChEMBL now records on a salt or hydrate form (`SALT_FORMS`), and ten are other drift. Because it predates the merges, it is the only copy that still shows those five pairs as the ten compounds the deposit measured, which is what identified them. It drops the compound ids' link to the deposit's other assays.
        - Licence: ChEMBL is CC BY-SA 3.0 ("The ChEMBL data is made available on a Creative Commons Attribution-Share Alike 3.0 Unported License", ChEMBL interface documentation, read 2026-11-25). A licence is never a verdict reason (EV-4).
    """

    # Task
    target = "logd74"
    problem_type = "regression"
    special_features = (
        Smiles(
            column="SMILES",
            description="The compound's structure, RDKit's canonical SMILES of the SMILES ChEMBL stores for it.",
        ),
    )
    metric = Metric.from_context(
        "mae",
        reason=(
            "Mean absolute error in log units, the criterion TDC declares for this data. The source fixes no "
            "metric: ChEMBL document CHEMBL3301361 and assay CHEMBL3301363 define the protocol and no task (read "
            "2026-11-25), and where we looked beyond them (the deposit's report card, the GEO-style series page, "
            "the two benchmarks that made a task of it) there is no competition and no single source choice to "
            "take. The two later definers declare different metrics, and this definition takes TDC's: its ADMET "
            'benchmark group gives "Regression | MAE | Scaffold", which is the task design shipped here, the '
            "Bemis-Murcko scaffold hold-out and one prediction per compound. MoleculeNet's dataset table gives "
            '"Physical Chemistry | Lipophilicity | SMILES | 1 | Regression | 4200 | Random | RMSE" under its rule '
            'that "for each dataset, we propose a metric and a splitting pattern that best fit the properties of '
            'the dataset"; its RMSE is not taken, because the pattern it pairs that metric with is the random '
            "split over its own reprocessed copy, and both are what this definition rejected as not the use case. "
            "The decision reads the error in log units too: a design round works in half-log bands, and a "
            "squared error punishes a large miss harder than the decision does. Neither definer is the source, so the origin is the context (MET-11): the metric "
            "a later definer declares for exactly this task, adopted here, not a source metric (MET-5), and the "
            "regression fallback it replaces is overruled rather than filled in. Little moves either way: over "
            "eight candidate models the ranking is identical under MAE, RMSE, median absolute error, the share "
            "within 0.5 and within 1.0 log, Spearman and a 3-band accuracy (per-fold Kendall tau 1.00 on 7 of the "
            "9 folds, 0.929 on the other two), and an L1-trained LightGBM does not win on MAE either (0.567 "
            "against 0.542). The metric reads only the target and the prediction, so no scoring column is needed."
        ),
    )

    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a chemical series: the compounds that share one Bemis-Murcko scaffold (the ring systems and
            the chains linking them; Bemis and Murcko 1996), computed with RDKit from the shipped SMILES. A compound
            without a ring, or with a scaffold that holds more than a tenth of the set, is a group of its own
            (SPLIT-31; here five compounds have no ring and no scaffold reaches a tenth). A chemist estimates the
            logD7.4 of a compound that has not been made, usually from a series this laboratory has not measured, so
            whole series are held out. Each row is one prediction, made from the structure alone.
        """,
    )
    splits_comment = """
        Grouped splits on the Bemis-Murcko scaffold: every compound of one series stays on one side, so a model predicts compounds of a series it has not seen. The scaffold is computed on the structure without its common salts and solvents and without repeated identical fragments, so a salt, hydrate or stereoisomer form of a compound shares a group with it and the two never land on opposite sides. Compounds with similar but not identical scaffolds can be on both sides. A test compound is a series this laboratory never measured, but not a chemical class nobody has seen: 22.7% of test compounds still have a close training analog (Tanimoto 0.7 or more, Morgan radius 2, 2,048 bits; fold SD 1.4), against 45.9% over random draws of the same test sizes, and the model scores RMSE 0.747 on the test compounds with no such analog against 0.570 on those with one.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # Only read: the five pages of the activity endpoint, concatenated in the order they were fetched.
        pages = [json.loads((raw_dir / name).read_text())["activities"] for name in ACTIVITY_FILES]
        return pd.DataFrame([activity for page in pages for activity in page], columns=KEPT)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # The download is not pinned to a ChEMBL release: fail rather than curate silently different data. The
        # counts catch a row appearing or leaving; the parent ids catch a structure being revised under a row that
        # stays, which is how a feature changed unseen between CHEMBL_20 and CHEMBL_37 (curation_comments).
        assert len(df) == 4200, f"expected the assay's 4,200 activities, got {len(df)}"
        assert set(df["standard_type"]) == {"LogD7.4"}, "the assay reports one standard type"
        on_salt = df[df["parent_molecule_chembl_id"] != df["molecule_chembl_id"]]
        found = dict(zip(on_salt["molecule_chembl_id"], on_salt["parent_molecule_chembl_id"], strict=True))
        assert found == SALT_FORMS, f"expected the six known salt/hydrate records, got {found}"
        df = df.rename(columns={"canonical_smiles": "SMILES", "standard_value": self.target})
        df[self.target] = df[self.target].astype(float)
        # The structure ships as a SMILES column (`special_features`), in RDKit's canonical form; every fragment and
        # the stereochemistry stay (CLEAN-24). It is also the scaffold's input: no counter-ion here has a ring.
        df["SMILES"] = canonical_smiles(df["SMILES"])
        # Five ids carry two activities each. They are two compounds the deposit measured separately, which ChEMBL
        # has merged onto one id and one structure since (`MERGED_IDS`), so the download no longer says which value
        # belongs to which compound. All ten activities are dropped (curation_comments, decision table).
        merged = {i for i, n in df.groupby("molecule_chembl_id").size().items() if n > 1}
        assert merged == set(MERGED_IDS), f"expected the five known merged ids, got {sorted(merged)}"
        # reset_index because the splits are positions, not labels (`_require_range_index`)
        df = df[~df["molecule_chembl_id"].isin(MERGED_IDS)].reset_index(drop=True)
        assert len(df) == 4190, f"expected 4,190 compounds, got {len(df)}"
        # The split groups: the chemical series (Bemis-Murcko scaffold) of the structure without common salts and
        # solvents and without repeated identical fragments, so a salt or hydrate form groups with its parent
        # (`group_structures`); a compound without a ring is its own group
        df = df.assign(scaffold=scaffold_groups(group_structures(df["SMILES"])))
        # molecule_chembl_id is an identifier (CLEAN-3, CLEAN-22); its only other use, the link to the deposit's
        # other assays, is a sibling task, not this one. standard_type is `LogD7.4` on every row and
        # parent_molecule_chembl_id is read only by the drift assert above (curation_comments).
        return drop_columns(df, ["molecule_chembl_id", "standard_type", "parent_molecule_chembl_id"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The SMILES is typed by `special_features`, `scaffold` is the group column and the target is numeric.
        del df
        return FeatureTypes()

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        measured = raw["standard_value"].astype(float)
        merged = (
            raw.assign(**{self.target: measured})
            .groupby("molecule_chembl_id")[self.target]
            .agg(activities="size", lowest="min", highest="max")
        )
        merged = merged[merged["activities"] > 1].assign(
            registered_as=lambda frame: [" + ".join(MERGED_IDS[name]) for name in frame.index],
            spread=lambda frame: (frame["highest"] - frame["lowest"]).round(2),
        )
        shipped = df[self.target]
        bounds = pd.DataFrame(
            {
                "compounds": [
                    int((shipped == -1.5).sum()),
                    int(((shipped >= -1.5) & (shipped < -1.0)).sum()),
                    int(((shipped > 4.0) & (shipped <= 4.5)).sum()),
                    int((shipped == 4.5).sum()),
                    int(((shipped < -1.5) | (shipped > 4.5)).sum()),
                ]
            },
            index=[
                "exactly at the lower end, -1.5",
                "in the lowest half-log band, -1.5 to -1.0",
                "in the highest half-log band, 4.0 to 4.5",
                "exactly at the upper end, 4.5",
                "outside the assay's stated range",
            ],
        )
        flat = canonical_smiles(group_structures(df["SMILES"]), stereo=False)
        stereo_groups = flat.groupby(flat).size()
        spread = df.assign(flat=flat).groupby("flat")[self.target].agg(["size", "min", "max"])
        spread = spread[spread["size"] > 1]
        spreads = spread["max"] - spread["min"]
        stereo = pd.DataFrame(
            {
                "count": [
                    int((stereo_groups > 1).sum()),
                    int(stereo_groups[stereo_groups > 1].sum()),
                    float(spreads.median().round(2)),
                    int((spreads > 0.5).sum()),
                    float(spreads.max().round(2)),
                ]
            },
            index=[
                "2D structures shared by more than one compound",
                "compounds in them",
                "median spread of logD7.4 within one of them",
                "of them whose spread is above 0.5",
                "largest spread of logD7.4 within one of them",
            ],
        )
        sizes = df["scaffold"].value_counts()
        groups = pd.DataFrame(
            {
                "count": [
                    len(df),
                    len(sizes),
                    int((sizes == 1).sum()),
                    int(sizes.max()),
                    round(100 * sizes.max() / len(df), 1),
                ]
            },
            index=[
                "compounds",
                "scaffold groups",
                "groups of one compound",
                "compounds in the largest group",
                "share of the set in the largest group (%)",
            ],
        )
        return [
            Decision(
                "The five pairs ChEMBL has merged onto one id are dropped",
                "Five ids carry two activities each. The assay did not measure one compound twice: the deposit "
                "registered two compounds, a stereo-defined form and an undefined or differently defined one, and "
                "each carries its own value (quinine and quinidine are one of the pairs, atropine and its "
                "tropane-defined form another). ChEMBL has merged each pair onto one id and one structure since, "
                "so the download no longer says which value belongs to which compound. Averaging them would put "
                "two different compounds in one row, and keeping both would pair two now-identical structures "
                "with targets up to 0.57 apart. Neither is this task, and the two structures cannot be recovered "
                "from this download, so all ten activities are dropped: 0.24% of the deposit.",
                merged,
            ),
            Decision(
                "The assay's range selects compounds, it does not censor values",
                "The assay reports -1.5 to 4.5 and no value falls outside, which would be censoring if the ends "
                "carried a pile-up. They do not: one compound sits at -1.5 and four at 4.5, while the outermost "
                "half-log bands hold 36 and 135. Compounds outside the range are missing from the deposit, and a "
                "user predicts the number this assay would report.",
                bounds,
            ),
            Decision(
                "Stereoisomers keep their own row and their own value",
                "Compounds that share a 2D structure differ only in stereochemistry and each carry their own "
                "measurement, so they are distinct compounds, not copies (LEAK-19 as applied to qsar_tid_11). They "
                "share a scaffold and never straddle the split. A 2D encoding cannot tell them apart, so their "
                "spread bounds the error such a model can reach on them: that bound is 0.5 or less, the median "
                "spread being 0.08 and only three of the 105 within-group pairs exceeding 0.5. The largest spread, "
                "1.55 log units, "
                "is not a floor at all. Its two compounds are enantiomers (CHEMBL1770464 2.03, CHEMBL1770465 3.58), "
                "whose logD7.4 must be identical in an achiral octanol/buffer system, so one of the two "
                "measurements is wrong by 15 to 22 times the assay's own uncertainty (a single measurement's SD is "
                "0.106, from the 47 stereocentre-inverted pairs among these groups with this one left out, and "
                "0.191 with it). The largest spread between "
                "compounds that really do differ in 3D is 0.49. All the rows stay.",
                stereo,
            ),
            Decision(
                "The groups are chemical series, not one dominant skeleton",
                "A scaffold that holds more than a tenth of the set is broken into single compounds (SPLIT-31), "
                "because it is no series. Here the largest is the bare benzene ring at 1.8%, so the rule does not "
                "fire and the groups are the series the data has.",
                groups,
            ),
        ]
