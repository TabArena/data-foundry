"""Curated dataset definition for `qsar_tid_11` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
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

RAW_FILE = "11.arff"
STRUCTURES_FILE = "chembl_17_chemreps.txt.gz"
"""ChEMBL 17's structure table (chembl_id, canonical SMILES, InChI, InChIKey; 133.6 MB, sha256 484009d0...b44e): the
ChEMBL release the Meta-QSAR data was drawn from, so every compound id of the file has its structure as it stood then."""
PREPARED_FILE = "chembl_17_structures_tid11.csv"
"""The ChEMBL 17 SMILES of this file's compounds, cut out of STRUCTURES_FILE once."""

# Salt forms of a compound that is also in the data (LEAK-19). The raw file has no structures, so the ids come from
# ChEMBL's molecule_hierarchy (API, 2026-10-21) for the rows in repeated fingerprint vectors: 37 groups of two
# ChEMBL ids with one parent_chembl_id, the same fingerprint and nearly the same target. We keep the parent's own
# row (the lowest ChEMBL id in the one group without it) and drop the other.
SALT_FORM_COPIES = frozenset(
    {
        "CHEMBL79422",
        "CHEMBL84575",
        "CHEMBL93210",
        "CHEMBL152854",
        "CHEMBL153611",
        "CHEMBL160489",
        "CHEMBL216318",
        "CHEMBL307446",
        "CHEMBL318112",
        "CHEMBL323543",
        "CHEMBL327331",
        "CHEMBL328069",
        "CHEMBL328298",
        "CHEMBL328582",
        "CHEMBL330496",
        "CHEMBL534707",
        "CHEMBL535862",
        "CHEMBL536721",
        "CHEMBL539053",
        "CHEMBL540119",
        "CHEMBL540121",
        "CHEMBL543817",
        "CHEMBL553840",
        "CHEMBL556575",
        "CHEMBL557579",
        "CHEMBL558198",
        "CHEMBL559015",
        "CHEMBL599035",
        "CHEMBL603888",
        "CHEMBL607008",
        "CHEMBL1159688",
        "CHEMBL1159692",
        "CHEMBL1160045",
        "CHEMBL1215083",
        "CHEMBL1215085",
        "CHEMBL1215086",
        "CHEMBL2337676",
    }
)


class QsarTid11(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How potent will a molecule be against one drug target?",
        use_case=(
            "In drug discovery, a medicinal chemist screens candidate molecules for activity on one protein target "
            "before making and testing them (the Meta-QSAR project builds one such model per target)."
        ),
        row=(
            "One compound measured against human thrombin (ChEMBL target 11, CHEMBL204; ChEMBL version 17, Meta-QSAR "
            "project 2015; 5,704 compounds after the salt-form copies leave)."
        ),
        predicted=(
            "The compound's median measured potency, as the negative log of the concentration that gives half the "
            "effect; higher means more potent."
        ),
        known=("The compound's chemical structure, as a SMILES string."),
        split=(
            "Whole chemical series (compounds sharing a ring skeleton) are held out, so the test data stands for "
            "compounds of series not measured yet."
        ),
        changes=(
            "We drop one row with a negative activity value, judged a data error, and 37 rows that are salt forms "
            "of a compound already in the data, replace the authors' fingerprint with the compound's structure from "
            "ChEMBL 17, and split by chemical series instead of at random."
        ),
        fit="direct",
        fit_reason=(
            "The structure is all a chemist has before synthesis, and "
            "held-out series stand for new ones. The activities are medians over measurements of many sources."
        ),
    )

    # Dataset
    unique_name = "qsar_tid_11"
    year = "2015"
    domain = "chemistry & material science"
    source = "OpenML"
    source_url = "https://www.openml.org/d/3050"
    license = "Public Domain"
    download_description = """
        We download the dataset from OpenML to a predefined folder.

        mkdir -p local-data-warehouse/qsar_tid_11/ && wget -P local-data-warehouse/qsar_tid_11/ https://www.openml.org/data/download/1674848/11.arff

        The compounds' structures, for the SMILES column and the scaffold groups of the split, come from ChEMBL 17's structure table (133,574,872 bytes, sha256 484009d05a2b1a4af714b18f76f329b69fcce806044ebcca7695efa30d58b44e); the definition cuts out this file's compounds once (chembl_17_structures_tid11.csv).

        wget -P local-data-warehouse/qsar_tid_11/ https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_17/chembl_17_chemreps.txt.gz
    """
    bibtex = """
        @article{olier2018meta,
          title={Meta-QSAR: a large-scale application of meta-learning to drug design and discovery},
          author={Olier, Ivan and Sadawi, Noureddin and Bickerton, G Richard and Vanschoren, Joaquin and Grosan, Crina and Soldatova, Larisa and King, Ross D},
          journal={Machine Learning},
          volume={107},
          pages={285--311},
          year={2018},
          publisher={Springer}
        }
    """
    curation_comments = """
        - The target is ChEMBL target 11, human prothrombin (thrombin, CHEMBL204), named by OpenML's original data URL.
        - OpenML (uploaded 2015-10-06, creators the Meta-QSAR team) is the first publication; the Mendeley Data release
          (doi:10.17632/spwgrcnjdg.1) came in 2020 and computes the fingerprints with RDKit instead of Pipeline Pilot.
        - We drop the "MOLECULE_CHEMBL_ID" column after it has served the join to the structures.
        - The file lists the compounds roughly in ChEMBL ID order, and the mean activity drifts along it (6.8 in the
          first tenth, 5.6 in the ninth); the standard shuffle removes this order.
        - Scaffold-grouped splits (Lennart, 2026-11-01; SPLIT-31 as amended), in place of random ones. The rows carry
          ChEMBL compound ids, and ChEMBL 17, the release the data was drawn from, holds the structure of every one
          (its InChIKey equals today's ChEMBL for all 5,505 ids still served). The groups are the Bemis-Murcko
          scaffolds of those structures (`scaffold_groups`): 2,529 groups for 5,704 compounds, 21 compounds without a
          ring alone, the largest group the bare benzene ring with 117 compounds (2%), 89 groups of 10 or more holding
          1,751 compounds. Counter-ions carry no ring here: stripping the 549 salts to their largest fragment changes
          no scaffold. A random split gave 79.7% of the test compounds a close training analog (Tanimoto >= 0.7,
          Morgan radius 2, 2,048 bits; median nearest 0.81), the scaffold groups 59.2% (median 0.73), and untuned
          LightGBM's RMSE rises from 0.794 to 0.920 (3 x 3 folds, 2026-11-01 run). On the definition's splits the
          group probe gives LightGBM R^2 0.747 under IID and 0.657 grouped, and the task probes raise no flag
          (LightGBM R^2 0.66, random forest 0.62, linear 0.48: the families still separate). Of the 356 fingerprint vectors
          that repeat (802 rows; the repeated-fingerprint bullet below), 303 lie within one scaffold and now stay on
          one side; 53 vectors (128 rows) span two or more scaffolds, analogs whose ring systems differ in a way the
          fingerprint does not see.
        - The structure ships as `SMILES` (CLEAN-24 as amended, Lennart, 2026-11-01): ChEMBL 17's SMILES in RDKit's
          canonical form (`canonical_smiles`; the 549 salts as ChEMBL records them), declared in `special_features`, so a
          benchmark encodes it as a structure and never as text; the recommended encoding is
          `data_foundry.v2.chemistry.encode_smiles` (RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts). The source's
          1,024 FCFP6 bits leave (Lennart, 2026-11-01: "the real task here is going from smiles to a prediction, the
          bits are just one possible modelling choice by the authors"). RDKit computes the same kind of fingerprint, but
          not these columns: with its closest settings (radius 3, feature invariants, 1,024 bits) no source bit is
          matched exactly by any RDKit bit, at any position. A benchmark computes its own encoding of the structure.
          On the scaffold splits LightGBM's R^2 was 0.66 on the bits alone and 0.68 with the encoded structure added.
        - Stereoisomers stay (as the repeated-fingerprint decision below): 474 rows in 217 groups share one structure
          once the stereo marks are set aside, each with its own measured potency (range within a group: median 0.45,
          up to 4.48 pXC50). The SMILES keeps the stereo marks; the recommended 2D encoding does not tell them apart.
          Each group shares a scaffold, so it stays on one side of the split. No two rows share a SMILES.
        - Only one row has a negative value (-6.24) and is thus extremely out-of-distribution, which is likely results from the target being log scaled in the original domain. We remove this row as it is unclear if this is a scaling or labeling error, but we judge it is in all cases a data artifact.
        - Why the row may leave (CLEAN-11, CLEAN-15): a pXC50 of -6.24 is a half-effect concentration of 10^6.24 mol/L, about 1.7 million mol/L, which no substance reaches (pure water is 55 mol/L). The value is impossible, so the target is missing and the row drops. It does not meet CLEAN-11's clause for an extreme target in the training period only: the split is random, and the source does not name the row.
        - We do not log scale the target (it could make sense for this distribution), as the original label is already log transformed.
        - Repeated fingerprints (LEAK-16 asks for a recorded decision; Lennart, 2026-10-21): 870 of 5,741 rows sit in
          387 repeated FCFP vectors (116 with the same target too), and every row has its own ChEMBL compound id. We
          traced 798 of the 870 rows in ChEMBL (the other 72 ids are no longer in ChEMBL). Most repeats are different
          compounds the fingerprint cannot tell apart: stereoisomers (179 vectors) and analogs such as F against Cl
          (125 vectors), with their own measured potency. These stay. Untuned LightGBM RMSE (5-fold, 2 seeds): random
          split 0.765, grouped on the vector 0.781, one row per vector 0.757; predicting a repeated row by its
          vector-mates' mean gives 0.798, worse than the model. Grouping on a bare fingerprint hash is barred
          (SPLIT-24) and would test whether the fingerprint resolves stereoisomers.
        - We drop 37 rows that are salt forms of a compound also in the data (LEAK-19, as in qsar_oral_toxicity): two
          ChEMBL ids with one ChEMBL parent (molecule_hierarchy), the same fingerprint and nearly the same target
          (median sd 0.04 within a pair; 0.006 in the 31 pairs that make up a whole vector). The rule does not read
          the target: we keep the parent's own row (in the one pair without it, the lowest ChEMBL id). The ids are
          embedded as SALT_FORM_COPIES: the parent links come from ChEMBL's molecule_hierarchy, which neither the
          raw file nor ChEMBL 17's structure table carries.
    """

    # Task
    target = "MEDIAN_PXC50"
    problem_type = "regression"
    special_features = (Smiles(column="SMILES"),)
    metric = Metric.source(
        "rmse",
        original="Average root mean squared error (RMSE) with 10-fold cross-validation",
        reference=(
            "Olier et al. 2018, Meta-QSAR, Machine Learning 107:285-311, doi:10.1007/s10994-017-5685-x, Sec. "
            "2.3 (arXiv:1709.03854)"
        ),
        definition="RMSE of MEDIAN_PXC50 (pXC50, already a -log10 scale).",
    )
    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a chemical series: the compounds that share one Bemis-Murcko scaffold (ring systems and the chains linking them; Bemis and Murcko 1996), computed with RDKit from the compound's ChEMBL 17 structure. A compound without a ring is a group of its own, and so would be each compound of a scaffold holding more than a tenth of the compounds (SPLIT-31; none here: the bare benzene ring holds 2%). A medicinal chemist screens candidates that often come from a series not yet measured on the target, so whole series are held out. Each row is one prediction, made from the compound's structure alone.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the Bemis-Murcko scaffold: all compounds of one series stay on one side, so a model predicts compounds of a series it has not seen; compounds without a ring are held out one by one. Compounds with similar but not identical scaffolds can be on both sides.
    """

    prepared_raw_files = (PREPARED_FILE,)

    @staticmethod
    def _read_arff(raw_dir: Path) -> pd.DataFrame:
        with open(raw_dir / RAW_FILE) as f:
            data = arff.load(f)
        return pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        ids = set(self._read_arff(raw_dir)["MOLECULE_CHEMBL_ID"])
        reps = pd.read_csv(raw_dir / STRUCTURES_FILE, sep="\t", usecols=["chembl_id", "canonical_smiles"])
        reps = reps[reps["chembl_id"].isin(ids)].rename(columns={"chembl_id": "MOLECULE_CHEMBL_ID"})
        reps.rename(columns={"canonical_smiles": "SMILES"}).to_csv(raw_dir / PREPARED_FILE, index=False)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = self._read_arff(raw_dir)
        # The structure of each compound, joined on the source's own key (ChEMBL 17 holds every id of the file)
        structures = pd.read_csv(raw_dir / PREPARED_FILE)
        df = df.merge(structures, on="MOLECULE_CHEMBL_ID", how="left", validate="many_to_one")
        assert df["SMILES"].notna().all(), "a compound id of the file has no ChEMBL 17 structure"
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Salt-form copies of a compound in the data leave (LEAK-19); the parent's row stays.
        df = df[~df["MOLECULE_CHEMBL_ID"].isin(SALT_FORM_COPIES)]
        # Remove one negative outlier row
        df = df[df["MEDIAN_PXC50"] >= 0].reset_index(drop=True)
        # The split groups: the chemical series (Bemis-Murcko scaffold); no ring, or a scaffold above a tenth, alone.
        # Counter-ions carry no ring here, so a salt's scaffold is its parent's.
        df = df.assign(scaffold=scaffold_groups(df["SMILES"]))
        # The structure ships as a SMILES column (`special_features`), in RDKit's canonical form; the authors' FCFP6
        # bits leave, one modelling choice of the structure (curation_comments)
        return pd.DataFrame(
            {"SMILES": canonical_smiles(df["SMILES"]), "MEDIAN_PXC50": df["MEDIAN_PXC50"], "scaffold": df["scaffold"]}
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the SMILES is typed by `special_features`; the target stays numeric
        del df
        return FeatureTypes()
