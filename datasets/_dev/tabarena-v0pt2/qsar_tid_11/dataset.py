"""Curated dataset definition for `qsar_tid_11` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Smiles,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    canonical_smiles,
)

RAW_FILE = "11.arff"
STRUCTURES_FILE = "chembl_17_chemreps.txt.gz"
"""ChEMBL 17's structure table (chembl_id, canonical SMILES, InChI, InChIKey; 133.6 MB, sha256 484009d0...b44e): the
ChEMBL release the Meta-QSAR data was drawn from, so every compound id of the file has its structure as it stood then."""
PREPARED_FILE = "chembl_17_structures_tid11.csv"
"""The ChEMBL 17 SMILES of this file's compounds, cut out of STRUCTURES_FILE once."""
FIRST_YEAR_FILE = "chembl_17_first_year.csv"
"""Next to this file: each compound's first publication year, a one-off extract from the ChEMBL 17 release dump
(`curation_comments`, the split bullet). The dump is 2 GB packed and 9.4 GB unpacked for two columns, so the extract
is kept here, as the salt-form ids are."""

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
        known=(
            "The compound's chemical structure, as a SMILES string, and the year it first appears in the thrombin "
            "literature."
        ),
        split=(
            "The compounds are held out by the year they first appear in the literature: five windows of two years "
            "from 2004 to 2013, each predicted from the compounds published before it, so the test data stands for "
            "the candidates that come next."
        ),
        changes=(
            "We drop one row with a negative activity value, judged a data error, and 37 rows that are salt forms "
            "of a compound already in the data, replace the authors' fingerprint with the compound's structure from "
            "ChEMBL 17, add the year the compound first appears in ChEMBL 17's thrombin records, and split by that "
            "year instead of at random."
        ),
        fit="direct",
        fit_reason=(
            "The structure is all a chemist has before synthesis, and the compounds of a later window stand for the "
            "candidates that come next. The activities are medians over measurements of many sources, and a tenth of "
            "them are assay limits stored as exact values."
        ),
    )

    # Dataset
    unique_name = "qsar_tid_11"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="OpenML",
            url="https://www.openml.org/d/3050",
            license="Public Domain",
            year="2015",
            bibtex="""
                @article{olier2018meta,
                  title={Meta-QSAR: a large-scale application of meta-learning to drug design and discovery},
                  author={Olier, Ivan and Sadawi, Noureddin and Bickerton, G Richard and Vanschoren, Joaquin and Grosan, Crina and Soldatova, Larisa and King, Ross D},
                  journal={Machine Learning},
                  volume={107},
                  pages={285--311},
                  year={2018},
                  publisher={Springer}
                }
            """,
        ),
    )
    download_description = """
        We download the dataset from OpenML to a predefined folder.

        mkdir -p local-data-warehouse/qsar_tid_11/ && wget -P local-data-warehouse/qsar_tid_11/ https://www.openml.org/data/download/1674848/11.arff

        The compounds' structures, for the SMILES column, come from ChEMBL 17's structure table (133,574,872 bytes, sha256 484009d05a2b1a4af714b18f76f329b69fcce806044ebcca7695efa30d58b44e); the definition cuts out this file's compounds once (chembl_17_structures_tid11.csv).

        wget -P local-data-warehouse/qsar_tid_11/ https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_17/chembl_17_chemreps.txt.gz

        chembl_17_first_year.csv next to this file holds each compound's first publication year, extracted once from the same release's database dump (chembl_17_sqlite.tar.gz, 2,068,152,046 bytes, sha256 58432fccfd44c90443002b48b0ec9d6194b1dc11a85982d91684b2f50959d2c0; 9.4 GB unpacked) with the query in the split bullet of the curation notes. The build does not read the dump.
    """
    curation_comments = """
        - The target is ChEMBL target 11, human prothrombin (thrombin, CHEMBL204), named by OpenML's original data URL.
        - OpenML (uploaded 2015-10-06, creators the Meta-QSAR team) is the first publication; the Mendeley Data release
          (doi:10.17632/spwgrcnjdg.1) came in 2020 and computes the fingerprints with RDKit instead of Pipeline Pilot.
        - We drop the "MOLECULE_CHEMBL_ID" column after it has served the join to the structures and the years.
        - Split by the year a compound first appears in the literature (Andrej, 2026-11-11; REVIEW.md issue 2, option
          C), in place of the scaffold-grouped split of 2026-11-01. `first_year` is the earliest year among the
          documents of the compound's human thrombin (CHEMBL204) activity records in ChEMBL 17, the release the
          Meta-QSAR data was drawn from; it is a feature as well as the time column, as in the other temporal tasks
          (apistox). All 5,704 compounds have a CHEMBL204 record there, 5,186 of them in a dated document (years 1992
          to 2013). The other 518 appear only in the one undated document, the PubChem BioAssay deposit CHEMBL1201862,
          and take 2011, the year ChEMBL 9 loaded it and the first year a modeller could have had it. The extract
          (`chembl_17_first_year.csv`, sha256 642e629da88a8a5b3bbd4e39fd059e2c8967b4e3cd3acf546a7fd7540c8475d0) was
          cut once from the release dump with
          `SELECT md.chembl_id, MIN(d.year) FROM activities a JOIN assays s ON a.assay_id = s.assay_id JOIN
          target_dictionary t ON s.tid = t.tid JOIN docs d ON a.doc_id = d.doc_id JOIN molecule_dictionary md ON
          a.molregno = md.molregno WHERE t.chembl_id = 'CHEMBL204' GROUP BY md.chembl_id`.
          Why the split changed: under the scaffold split 58% of the test compounds keep a close training analog
          (Tanimoto >= 0.7, Morgan radius 2), and 71% to 93% of those analogs were first published in the same year as
          the test compound, so the folds hold ring skeletons out but not the series of a paper, which a chemist
          screening a new candidate does not have either. Measured on the shipped windows and all 5,704 compounds,
          with the recommended SMILES encoding, untuned LightGBM and random forest, RMSE (Slurm jobs 1378119 and
          1378141, 2026-11-11); the scaffold columns are the 3 x 3 scaffold-grouped out-of-fold scores on the same
          compounds:

          | Test window | Compounds | Earlier compounds (train) | Scaffold split: LightGBM | Random forest | Close analog | By year: LightGBM | Random forest | Close analog |
          |---|---|---|---|---|---|---|---|---|
          | 2004-05 | 633 | 3,280 | 0.844 | 0.891 | 67% | 1.502 | 1.405 | 18% |
          | 2006-07 | 598 | 3,913 | 0.800 | 0.814 | 72% | 1.049 | 1.020 | 14% |
          | 2008-09 | 290 | 4,511 | 1.038 | 1.074 | 58% | 1.184 | 1.194 | 30% |
          | 2010-11 | 744 | 4,801 | 0.804 | 0.880 | 24% | 1.248 | 1.368 | 6% |
          | 2012-13 | 159 | 5,545 | 0.812 | 0.873 | 71% | 0.894 | 1.005 | 20% |
          | all compounds | 5,704 | - | 0.868 | 0.920 | 58% | - | - | - |

          Where the difference comes from, at the same number of training compounds where the pool allows (LightGBM
          RMSE, the drawn sets averaged over 3 seeds):

          | Test window | Earlier years only (shipped) | Any year, no test scaffold | Any year, at random | Compounds published later |
          |---|---|---|---|---|
          | 2004-05 | 1.502 | 1.281 | 1.305 | 1,791 |
          | 2006-07 | 1.049 | 1.083 | 1.038 | 1,193 |
          | 2008-09 | 1.184 | 1.249 | 1.174 | 903 |
          | 2010-11 | 1.248 | 1.233 | 1.218 | 159 |
          | 2012-13 | 0.894 | 0.860 | 0.894 | 0 |

          Only the oldest window has many later compounds to learn from, and there they are worth about 0.2 RMSE;
          from 2006-07 on the three training sets score within 0.08 of each other, and in the newest two they are
          nearly the same compounds. So on this layout the scaffold split's advantage is the same-year siblings it
          keeps rather than the later papers. An earlier run on four hand-chosen windows (2004, 2005-06, 2007-08,
          2009-13), dated from today's web service with the deposit left out, pointed the same way: LightGBM 0.68 to
          0.90 by scaffold against 1.11 to 1.31 by year (Slurm jobs 1366166 and 1366180, 2026-11-06).
          Checked on the shipped windows (2026-11-11): the task probes raise no flag (LightGBM R^2 0.350, skill
          +0.419 over the dummy and ahead of it on all five windows, random forest 0.313, selected linear 0.138,
          plain linear -0.409; spread LightGBM - linear +0.659, paired standard error 0.177). The leak probes find no
          test row with an exact feature copy in training (0.0% over the five windows) and no single feature near the
          all-feature R^2 of 0.449 (best 0.055); probe 13 reads a mild shift at the end (the mean of the newest three
          years pooled, z -3.7), which is the drift the temporal split is there for. `hidden_groups` finds no
          entity-like column under these windows (61 candidates, 0 hits; 2.6% of test rows have a near copy at
          Tanimoto 0.85, against 16.8% of all rows sitting in such a cluster).
          The potency itself is a fixed property of the compound; what moves with the year is which compounds exist,
          and with them the level of the targets (mean pXC50 6.43 up to 2003, 6.42 in 2004-05, 6.00 in 2006-07, 6.37
          in 2008-09, 5.44 in 2010-11, 5.77 in 2012-13; Spearman year against target -0.24).
        - Assay limits (Andrej, 2026-11-11; REVIEW.md issue 1, option B): 654 targets (11.5%) sit at round limits
          (pXC50 4.30: 348, 5.00: 204, 4.00: 81, 4.70: 21); in a sample of 36 such compounds, ChEMBL holds 31 only as
          bounds (">" the top concentration tested), 3 as exact values and 2 not at all, so these are upper bounds of
          the potency stored as exact values, as in the Meta-QSAR file (LEAK-26: documented). They are the inactive
          end of the screen and stay. 306 of the 654 (47%) are compounds whose only thrombin record is the PubChem
          BioAssay deposit CHEMBL1201862: 59% of its 518 compounds sit at a limit, against 6.7% of the rest, and its
          mean potency is 5.01 against 6.36. For an inactive compound RMSE therefore rewards predicting the top
          concentration its laboratory tested rather than "inactive"; whether a compound is active, the chemist's
          decision, is unaffected. The source (Olier et al., Sec. 2.2) takes "the median of those activities falling
          in the modal log unit" and does not say how bounds were treated.
        - Collection facts (Andrej, 2026-11-11; REVIEW.md issue 3, option B): the compounds arrive over time and
          ChEMBL dates them, so the record carries `Samples: Over Time` and `Time: Dated` in place of `Samples: No
          Time Dimension`. No `Target: Revised Later`: only 5.1% of the compounds have a thrombin record from a year
          later than their first, so a median label seldom moves after the compound's first publication.
        - The file lists the compounds roughly in ChEMBL ID order, and the mean activity drifts along it (6.8 in the
          first tenth, 5.6 in the ninth), mostly the PubChem deposit at positions 70% to 90%; the file position
          follows the first year only loosely (Spearman 0.48). The frame ships sorted by `first_year` (the time
          column), so the file order is gone.
        - Chemical series, as background: the scaffold-grouped split shipped from 2026-11-01 to 2026-11-11 and the
          `scaffold` column left with it, but the numbers describe the data. The Bemis-Murcko scaffolds of the
          ChEMBL 17 structures (`scaffold_groups`) are 2,529 groups for 5,704 compounds, 21 compounds without a ring
          alone, the largest group the bare benzene ring with 117 compounds (2%), 89 groups of 10 or more holding
          1,751 compounds. Counter-ions carry no ring here: stripping the 549 salts to their largest fragment changes
          no scaffold. A random split gave 79.7% of the test compounds a close training analog (Tanimoto >= 0.7,
          Morgan radius 2, 2,048 bits; median nearest 0.81), the scaffold groups 59.2% (median 0.73), and untuned
          LightGBM's RMSE rises from 0.794 to 0.920 (3 x 3 folds, 2026-11-01 run); on those scaffold splits the task
          probes raised no flag (LightGBM R^2 0.66, random forest 0.62, linear 0.48: the families still separate). Of
          the 356 fingerprint vectors that repeat (802 rows; the repeated-fingerprint bullet below), 303 lie within
          one scaffold; 53 vectors (128 rows) span two or more scaffolds, analogs whose ring systems differ in a way
          the fingerprint does not see.
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
          Under the split by year a group falls where each member's first publication year puts it: 78 of the 217
          groups hold more than one year, and 32 reach across a window boundary, so for those a training row and a
          test row differ only in their stereochemistry. No two rows share a SMILES.
        - Only one row has a negative value (-6.24) and is thus extremely out-of-distribution, which is likely results from the target being log scaled in the original domain. We remove this row as it is unclear if this is a scaling or labeling error, but we judge it is in all cases a data artifact.
        - Why the row may leave (CLEAN-11, CLEAN-15): a pXC50 of -6.24 is a half-effect concentration of 10^6.24 mol/L, about 1.7 million mol/L, which no substance reaches (pure water is 55 mol/L). The value is impossible, so the target is missing and the row drops. The reason is the impossible value, not CLEAN-11's clause for an extreme target in the training period only, although the compound (CHEMBL92020, first published 2002) would now fall in every window's training side; the source does not name the row.
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

    # Splits: five windows of two publication years. Every year from 1992 to 2013 is in the data, so two distinct
    # years are two calendar years, and the newest half of the 22 years is cut into five windows (window=None).
    temporal = Temporal(
        on="first_year",
        splits=TemporalSplits(window=None, unit="unique", n_windows=5, min_train_fraction=0.5),
        horizon=2,
        horizon_unit="years",
    )
    splits_comment = """
        Expanding-window temporal splits on the year a compound first appears in ChEMBL 17's human thrombin records: 5 test windows of two years (2012-13, 2010-11, 2008-09, 2006-07, 2004-05), newest first; train is every compound first published before the window. The windows hold 159, 744, 290, 598 and 633 compounds, and their train sides 5,545, 4,801, 4,511, 3,913 and 3,280 compounds (97%, 84%, 79%, 69% and 57% of all 5,704). A model trained on the compounds known up to a year predicts the potency of the compounds that appear in the next two. Two years is the window the protocol derives from five windows over the newest half of the 22 publication years, and the smallest window (2012-13) still holds 159 compounds. The 518 compounds of the undated PubChem BioAssay deposit take 2011, the year ChEMBL 9 loaded it, which puts them in the 2010-11 window. The scaffold-grouped split this replaces trained on same-year siblings of the test compounds (curation notes).
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
        # The first publication year, the time column of the split: the one-off ChEMBL 17 extract next to this file
        years = pd.read_csv(self.folder / FIRST_YEAR_FILE)
        df = df.merge(years, on="MOLECULE_CHEMBL_ID", how="left", validate="many_to_one")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Salt-form copies of a compound in the data leave (LEAK-19); the parent's row stays.
        df = df[~df["MOLECULE_CHEMBL_ID"].isin(SALT_FORM_COPIES)]
        # Remove one negative outlier row
        df = df[df["MEDIAN_PXC50"] >= 0].reset_index(drop=True)
        # Every kept compound has a CHEMBL204 record in ChEMBL 17, dated or in the 2011 deposit (curation_comments)
        assert df["first_year"].notna().all(), "a kept compound has no ChEMBL 17 publication year"
        # The structure ships as a SMILES column (`special_features`), in RDKit's canonical form; the authors' FCFP6
        # bits leave, one modelling choice of the structure (curation_comments)
        return pd.DataFrame(
            {
                "SMILES": canonical_smiles(df["SMILES"]),
                "first_year": df["first_year"].astype("int64"),
                "MEDIAN_PXC50": df["MEDIAN_PXC50"],
            }
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the SMILES is typed by `special_features`; `first_year` and the target stay numeric
        del df
        return FeatureTypes()
