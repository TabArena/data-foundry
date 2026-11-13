"""Curated dataset definition for `qsar_fish_toxicity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Smiles,
    Source,
    TaskSummary,
    canonical_smiles,
    scaffold_groups,
)

RAW_FILE = "qsar_fish_toxicity.csv"
"""The UCI file: the 6 descriptors and LC50, no structures, LC50 rounded to 3 decimals."""
STRUCTURES_FILE = "toxicity_data_fish.xlsx"
"""The authors' workbook (michem.unimib.it): CAS-RN, SMILES, their train/test split, LC50 at full precision and the
same 6 descriptors, in the same row order as the UCI file."""
DESCRIPTORS = ["CIC0", "SM1_Dz(Z)", "GATS1i", "NdsCH", "NdssC", "MLOGP"]
"""The authors' 6 descriptors, chosen by a genetic algorithm on their training set; all computed from the structure."""


class QsarFishToxicity(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How toxic is a chemical to fish, judging from its molecular structure?",
        use_case=(
            "For example, a regulatory toxicologist estimates the acute fish toxicity of an untested chemical, to "
            "decide whether it needs testing or a hazard label."
        ),
        row=("One chemical tested for 96-hour toxicity to fathead minnows (908 chemicals, Cassotti et al. 2015)."),
        predicted=(
            "The concentration that kills half the test fish within 96 hours, as minus the log of moles per litre, so"
            " higher means more toxic."
        ),
        known="The chemical's structure, as a SMILES string.",
        split=(
            "Whole chemical series are held out: chemicals that share a ring skeleton stay on one side, so a test "
            "chemical belongs to a family the model has not seen. Chemicals without a ring are held out one by one."
        ),
        changes=(
            "We add each chemical's structure from the authors' own workbook and ship it in place of their six "
            "descriptors, take the target from the same workbook at full precision, and split by chemical series "
            "instead of at random."
        ),
        fit="direct",
        fit_reason=(
            "The structure is all a toxicologist has for an untested chemical, and a held-out series stands for a "
            "family not yet tested."
        ),
    )

    # Dataset
    unique_name = "qsar_fish_toxicity"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5JG7B",
            license="CC BY 4.0",
            year="2015",
            bibtex=r"""
                @article{cassotti2015similarity,
                  title={A similarity-based QSAR model for predicting acute toxicity towards the fathead minnow (Pimephales promelas)},
                  author={Cassotti, Matteo and Ballabio, Davide and Todeschini, Roberto and Consonni, Viviana},
                  journal={SAR and QSAR in Environmental Research},
                  volume={26},
                  number={3},
                  pages={217--243},
                  year={2015},
                  publisher={Taylor \& Francis}
                }
            """,
        ),
    )
    special_features = (Smiles(column="SMILES"),)
    data_tags = ("UnseenGroup",)
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/qsar_fish_toxicity/ && wget -P local-data-warehouse/qsar_fish_toxicity/ https://archive.ics.uci.edu/static/public/504/qsar+fish+toxicity.zip && unzip local-data-warehouse/qsar_fish_toxicity/qsar+fish+toxicity.zip -d local-data-warehouse/qsar_fish_toxicity/

        The structures come from the authors' own release, which UCI left out: the Excel file of the Milano
        Chemometrics group's page https://michem.unimib.it/download/data/acute-aquatic-toxicity-to-fish/ (a RAR archive
        behind a notification form; the form page links the file on Google Drive, downloaded 2026-11-01). It holds
        CAS-RN, SMILES, the authors' train/test split, LC50 and the same 6 descriptors, in the UCI file's row order.
        The page states: "The dataset is freeware and may be used if proper reference is given to the authors."

        toxicity_data_fish.xlsx (90,196 bytes), sha256
        98ae9433bcf8ffd5b32b3954a9571a4ec97d2d93f66119c9e36b8130925be721
    """
    curation_comments = """
        - The structure ships as `SMILES` (CLEAN-24 as amended, Lennart, 2026-11-01), in RDKit's canonical form (`canonical_smiles`; no salts or mixtures here), declared in `special_features`, so a benchmark encodes it as a structure and never as text; the recommended encoding is `data_foundry.v2.chemistry.encode_smiles` (RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts).
        - The authors' 6 descriptors leave (Lennart, 2026-11-01, as for qsar_tid_11: the task goes from the structure to a prediction, and the descriptors are one modelling choice of the authors). This also removes the mild optimism they carried: a genetic algorithm chose them on the paper's 726 training chemicals, which overlap our test folds (LEAK-31).
        - The structures come from the authors' own workbook, which the UCI copy left out. It is the same 908 rows in the same order: every one of the 6 descriptors is identical on all 908 rows (the CSV's rounding aside, LC50 too), so the link is exact and needs no key. All 908 SMILES parse, and no two are the same chemical, with or without stereochemistry.
        - The target comes from the workbook as well: the UCI file rounds LC50 to 3 decimals (every row differs by at most 0.0005), the workbook gives it at full precision.
        - 24% of the rows share all six of the authors' descriptors with another row, but their structures differ: isomers the descriptors could not tell apart. With the structure shipped the pairs are distinguishable, which is one more reason the descriptors leave.
        - Split (CLEAN-24, SPLIT-31 as amended): grouped on the Bemis-Murcko scaffold of the structure (`scaffold_groups`); chemicals without a ring, and those of a scaffold holding more than a tenth of the set, are groups of their own. An assessor estimates the toxicity of an untested chemical, often of a series not yet measured, so whole series are held out; qsar_bioconcentration, qsar_oral_toxicity and qsar_tid_11 group the same way. The source split at random.
        - Sibling of qsar_aquatic_toxicity (Andrej, 2026-11-11: keep both, note the overlap): the same Milano group, source databases (ECOTOX, EAT5, OASIS) and pipeline. 237 chemicals are in both, counted on the canonical SMILES of the two authors' workbooks with the stereo set aside (26.1% of this set, 43.4% of the Daphnia set; 225 of them carry the same CAS-RN in both), and their LC50s correlate at r = 0.81 (Spearman 0.82), the Daphnia values 0.37 log units more toxic on average. Another species (the fathead minnow, not Daphnia magna) and exposure time (96 h, not 48 h), so a different task, not a duplicate (PROV-7); a method that suits this study design gains on both.
        - CC (2026-11-12, Andrej): the fit stays direct (review issue 2, A; USE-8): whole series are held out and the authors' selected descriptors have left, the setting in which qsar_bioconcentration reads direct, so the open proposal of 2026-10-26 is closed as superseded. On the shipped scaffold splits (10 x 3), 12.4% of the test chemicals have a close training analog (Tanimoto 0.7 or more, Morgan radius 2, 2,048 bits; 9.4% to 16.5% per split), against 13.1% under random 3-fold splits of the same rows: holding out series removes few close analogs here.
        - Time basis: UnseenGroup (Andrej, 2026-11-13; `Timeless` before): the use case predicts for chemicals not
          tested yet, which whole scaffolds held out stand for. A chemical's 96-hour LC50 for the fathead minnow is a
          property of the chemical, and the Milano group compiled historic laboratory tests in 2015 without dates
          (Andrej, 2026-11-12; review issue 3, reply a). Dated through the EPA's ECOTOX bulk release
          (`ecotox_ascii_09_15_2026`), joined on the CAS-RN of the authors' workbook to the fathead minnow 96-hour LC50
          records, the year being the publication year of the earliest matching test: 850 of 908 chemicals (93.6%), 1956
          to 2005, median 1984, 90% by 1990. Where ECOTOX gives mg/L, its median per chemical matches the target at r =
          0.923 (212 chemicals, median difference 0.02 log units, 95.3% within one log unit). The relation does not move
          with the year (Spearman of first test year and LC50 -0.06; the authors' own train share is 0.78 to 0.88 in
          every period), and a forward split by first test year is no stricter than the scaffold folds (untuned models
          on `encode_smiles`, RMSE, three expanding windows, each training side at least half the dated chemicals; Slurm
          1378105, 2026-11-11):

          | Scheme | RMSE, LightGBM / RF | Close training analog | Test scaffold in training |
          |---|---|---|---|
          | Forward by first test year | 0.970 / 0.974 | 7.2% | 15-18% |
          | Scaffold-disjoint, any year | 0.970 / 0.978 | 5.9% | 0 |
          | Random, any year | 0.941 / 0.941 | 6.9% | 15-20% |
          | Scaffold 3-fold, all rows | 0.872 / 0.848 | 12.0% | 0 |

          The first three rows score the same test chemicals of the dated windows; the last is a scaffold 3-fold over all rows. The spread between windows (RMSE 0.81 to 1.17) is larger than the spread between schemes. The split cannot test a chemistry newer than the 1990s (90% of the dated chemicals were first tested by 1990, none after 2005), nor whether the 58 undated chemicals follow the same pattern; a publication year is an upper bound on the test date.
    """

    # Task
    target = "LC50"
    problem_type = "regression"
    data_tags = ("Timeless",)
    metric = Metric.fallback(
        reason=(
            "Cassotti et al. 2015 report R2/Q2 with RMSE on training and external sets; rmse is the "
            "regression fallback."
        ),
    )

    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a chemical series: the chemicals that share one Bemis-Murcko scaffold (ring systems and the chains linking them; Bemis and Murcko 1996), computed with RDKit from the structure. A chemical without a ring, or one of a scaffold that holds more than a tenth of the set, is a group of its own (SPLIT-31). A toxicologist estimates the fish toxicity of an untested chemical, often of a series not yet measured, so whole series are held out. Each row is one prediction, made from the chemical's structure alone.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the Bemis-Murcko scaffold: all chemicals of one series stay on one side, so a model predicts chemicals of a series it has not seen; chemicals without a ring are held out one by one. Chemicals with similar but not identical scaffolds can be on both sides.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        uci = pd.read_csv(raw_dir / RAW_FILE, sep=";", header=None)
        uci.columns = [*DESCRIPTORS, "LC50"]
        return {"uci": uci, "authors": pd.read_excel(raw_dir / STRUCTURES_FILE)}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        uci, authors = raw["uci"], raw["authors"]
        # The workbook is the UCI file with the structures and the unrounded target, row for row (curation_comments)
        assert len(uci) == len(authors), "the authors' workbook and the UCI file differ in length"
        assert np.allclose(uci[DESCRIPTORS].to_numpy(float), authors[DESCRIPTORS].to_numpy(float)), (
            "the authors' workbook and the UCI file differ in a descriptor"
        )
        # The structure ships as a SMILES column (`special_features`), in RDKit's canonical form; the authors' 6
        # descriptors leave, one modelling choice of the structure (curation_comments)
        df = pd.DataFrame(
            {"SMILES": canonical_smiles(authors["SMILES"]), self.target: authors["LC50[-LOG(mol/L)]"].astype(float)}
        )
        # The split groups: the chemical series (Bemis-Murcko scaffold); no ring, or a scaffold above a tenth, alone
        return df.assign(scaffold=scaffold_groups(df["SMILES"]))

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the SMILES is typed by `special_features`; the target stays numeric
        del df
        return FeatureTypes()
