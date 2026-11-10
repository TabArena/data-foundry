"""Curated dataset definition for `qsar_biodeg` (data-foundry v2). Evidence: README.md."""

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

RAW_FILE = "biodeg.csv"
"""The UCI file: the authors' 41 descriptors and the class, no structures and no header row."""
STRUCTURES_FILE = "ci4000213_si_001.xlsx"
"""The paper's supporting information: the sheet "Train+Test" holds CAS-RN, SMILES, the class, the authors'
Train/Test split and the same 41 descriptors, in the UCI file's row order; "External validation" holds 670 further
chemicals (a candidate of its own, see curation_comments)."""
STRUCTURES_SHEET = "Train+Test"


class QsarBiodeg(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a chemical readily biodegradable, judging from its molecular structure?",
        use_case=(
            "For example, a regulator or a chemical manufacturer screens a chemical's structure to decide whether it "
            "needs a ready-biodegradability test, or to rank candidates before one."
        ),
        row=(
            "One chemical with a known ready-biodegradability test result, from the data set of Mansouri et al. 2013 "
            "(1,055 chemicals)."
        ),
        predicted="Whether the chemical is readily biodegradable in the standard test; 33.7% are.",
        known="The chemical's structure, as a SMILES string.",
        split=(
            "Whole chemical series are held out: chemicals that share a ring skeleton stay on one side, so a test "
            "chemical belongs to a family the model has not seen. Chemicals without a ring are held out one by one."
        ),
        changes=(
            "We add each chemical's structure from the paper's supporting information and ship it in place of the "
            "authors' 41 descriptors, and split by chemical series instead of at random."
        ),
        fit="direct",
        fit_reason=(
            "The structure is all a screener has before testing, and a held-out series stands for a family not yet "
            "tested."
        ),
    )

    # Dataset
    unique_name = "qsar_biodeg"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5H60M",
            license="CC BY 4.0",
            year="2013",
            bibtex="""
                @article{mansouri2013quantitative,
                  title={Quantitative structure--activity relationship models for ready biodegradability of chemicals},
                  author={Mansouri, Kamel and Ringsted, Tine and Ballabio, Davide and Todeschini, Roberto and Consonni, Viviana},
                  journal={Journal of chemical information and modeling},
                  volume={53},
                  number={4},
                  pages={867--878},
                  year={2013},
                  publisher={ACS Publications}
                }
            """,
        ),
    )
    special_features = (Smiles(column="SMILES"),)
    download_description = """
        mkdir -p local-data-warehouse/qsar_biodeg/ && wget -P local-data-warehouse/qsar_biodeg/ https://archive.ics.uci.edu/static/public/254/qsar+biodegradation.zip && unzip local-data-warehouse/qsar_biodeg/qsar+biodegradation.zip -d local-data-warehouse/qsar_biodeg/ && rm local-data-warehouse/qsar_biodeg/qsar+biodegradation.zip

        The structures come from the paper's supporting information, which UCI left out (downloaded 2026-11-01;
        pubs.acs.org refuses a command-line download, so we take the Internet Archive's copy of the same file):

        wget -O local-data-warehouse/qsar_biodeg/ci4000213_si_001.xlsx https://web.archive.org/web/20230306145658id_/https://pubs.acs.org/doi/suppl/10.1021/ci4000213/suppl_file/ci4000213_si_001.xlsx

        ci4000213_si_001.xlsx (503,427 bytes), sha256
        64355cd79cedbcc5a6e1fc9178215d22d716643f2ce6ad60fa1aa45c45fc5f98
    """
    curation_comments = """
        - biodeg.csv has no header row, so we read it with `header=None` and keep the first chemical: 1,055 rows,
          356 readily biodegradable, as on UCI.
        - The structure ships as `SMILES` (CLEAN-24 as amended, Lennart, 2026-11-01), in RDKit's canonical form
          (`canonical_smiles`; no salts or mixtures here), declared in `special_features`, so a benchmark encodes it as a
          structure and never as text; the recommended encoding is `data_foundry.v2.chemistry.encode_smiles` (RDKit's
          2D descriptors, the 166 MACCS keys and the ECFP4 counts).
        - The authors' 41 descriptors leave (Lennart, 2026-11-01, as for qsar_tid_11: the task goes from the structure
          to a prediction, and the descriptors are one modelling choice of the authors). They were Dragon descriptors
          selected by a genetic algorithm, which no open tool recomputes. Their meaning and dtypes, settled on
          2026-10-30 (counts numeric, three presence flags categorical), no longer apply.
        - The structures come from the paper's supporting information, which the UCI copy left out. Its "Train+Test"
          sheet is the same 1,055 rows in the same order: all 41 descriptors and the class are identical on every row,
          so the link is exact and needs no key. All 1,055 SMILES parse and no two are the same chemical.
        - Stereoisomers stay: three pairs are one structure once the stereo marks are set aside (maleic and fumaric
          acid, sorbitol and mannitol, dieldrin and endrin), each pair agreeing on its class. They are distinct
          chemicals with distinct structures, as in qsar_tid_11; a 2D encoding cannot tell them apart, and each pair
          shares a scaffold, so they never straddle the split.
        - Not used here: the supporting information's "External validation" sheet holds 670 further chemicals with
          structures and classes. They are not more of this dataset. The 1,055 here were curated from NITE/MITI,
          while those 670 were "constructed from two data sources, Cheng et al. and the Canadian DSL database"
          (Chakravarti and Alla, arXiv 1808.04456, Table 1, whose counts match both sheets), and only 8 of their 670
          canonical structures occur here, one of them with the opposite class. They are screened as their own
          candidate, `ready_biodegradability_mansouri_external` (2026-11-02).
        - Split (CLEAN-24, SPLIT-31 as amended): grouped on the Bemis-Murcko scaffold of the structure
          (`scaffold_groups`); chemicals without a ring, and those of a scaffold holding more than a tenth of the set,
          are groups of their own. A screener judges an untested chemical, often of a series not yet measured, so whole
          series are held out; qsar_bioconcentration, qsar_oral_toxicity, qsar_fish_toxicity, qsar_aquatic_toxicity and
          qsar_tid_11 group the same way. The source split at random.
    """

    # Task
    target = "Biodegradable"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Mansouri et al. 2013 report error rate / NER with sensitivity and specificity, the group's house measure, without a decision threshold or costs. Original rejected: NER (balanced accuracy). roc_auc is the binary fallback."
    )

    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a chemical series: the chemicals that share one Bemis-Murcko scaffold (ring systems and the chains linking them; Bemis and Murcko 1996), computed with RDKit from the structure. A chemical without a ring, or one of a scaffold that holds more than a tenth of the set, is a group of its own (SPLIT-31). A screener judges an untested chemical, often of a series not yet measured, so whole series are held out. Each row is one prediction, made from the chemical's structure alone.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the Bemis-Murcko scaffold: all chemicals of one series stay on one side, so a model predicts chemicals of a series it has not seen; chemicals without a ring are held out one by one. Chemicals with similar but not identical scaffolds can be on both sides.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        uci = pd.read_csv(raw_dir / RAW_FILE, sep=";", header=None)  # no header row
        authors = pd.read_excel(raw_dir / STRUCTURES_FILE, STRUCTURES_SHEET)
        return {"uci": uci, "authors": authors}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        uci, authors = raw["uci"], raw["authors"]
        descriptors = [c for c in authors.columns if c not in ("CAS-RN", "Smiles", "Class", "Status")]
        # The supporting information is the UCI file with the structures added, row for row (curation_comments)
        assert len(uci) == len(authors), "the supporting information and the UCI file differ in length"
        assert np.allclose(uci.iloc[:, : len(descriptors)].to_numpy(float), authors[descriptors].to_numpy(float)), (
            "the supporting information and the UCI file differ in a descriptor"
        )
        assert (uci.iloc[:, -1].astype(str).to_numpy() == authors["Class"].astype(str).to_numpy()).all(), (
            "the supporting information and the UCI file differ in the class"
        )
        # The structure ships as a SMILES column (`special_features`), in RDKit's canonical form; the authors' 41
        # descriptors leave, one modelling choice of the structure (curation_comments)
        df = pd.DataFrame(
            {
                "SMILES": canonical_smiles(authors["Smiles"]),
                self.target: authors["Class"].map({"RB": "Yes", "NRB": "No"}),
            }
        )
        assert df[self.target].notna().all(), "a class is neither RB nor NRB"
        # The split groups: the chemical series (Bemis-Murcko scaffold); no ring, or a scaffold above a tenth, alone
        return df.assign(scaffold=scaffold_groups(df["SMILES"]))

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the SMILES is typed by `special_features`; the target becomes a category
        del df
        return FeatureTypes()
