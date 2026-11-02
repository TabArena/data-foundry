"""Curated dataset definition for `qsar_aquatic_toxicity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    TaskSummary,
    canonical_smiles,
    scaffold_groups,
)

RAW_FILE = "qsar_aquatic_toxicity.csv"
"""The UCI file: the authors' 8 descriptors and LC50, no structures."""
STRUCTURES_FILE = "toxicity_data.xlsx"
"""The authors' workbook (michem.unimib.it): CAS-RN, SMILES, their train/test split, LC50 and the same 8 descriptors,
in the same row order as the UCI file."""
DESCRIPTORS = ["TPSA(Tot)", "SAacc", "H-050", "MLOGP", "RDCHI", "GATS1p", "nN", "C-040"]
"""The authors' 8 descriptors, chosen by a genetic algorithm on the measured chemicals; all computed from the
structure."""


class QsarAquaticToxicity(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How toxic is a chemical to water fleas, judging from its molecular structure?",
        use_case=(
            "For example, a chemist or regulator estimates the acute toxicity of a chemical to the water flea Daphnia"
            " magna before, or instead of, an animal test (the source paper builds such a model)."
        ),
        row="One of 546 chemicals with a measured toxicity (Cassotti et al. 2014).",
        predicted=(
            "The concentration that kills half of the water fleas within 48 hours, as minus the log of moles per "
            "litre (higher is more toxic)."
        ),
        known="The chemical's structure, as a SMILES string.",
        split=(
            "Whole chemical series are held out: chemicals that share a ring skeleton stay on one side, so a test "
            "chemical belongs to a family the model has not seen. Chemicals without a ring are held out one by one."
        ),
        changes=(
            "We add each chemical's structure from the authors' own workbook and ship it in place of their eight "
            "descriptors, and split by chemical series instead of at random."
        ),
        fit="direct",
        fit_reason=(
            "The structure is all an assessor has for an untested chemical, and a held-out series stands for a family "
            "not yet measured."
        ),
    )

    # Dataset
    unique_name = "qsar_aquatic_toxicity"
    year = "2014"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5SG7H"
    license = "CC BY 4.0"
    smiles_columns = ("SMILES",)
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/505/qsar+aquatic+toxicity.zip && unzip qsar+aquatic+toxicity.zip && rm qsar+aquatic+toxicity.zip && mkdir -p local-data-warehouse/qsar_aquatic_toxicity && mv qsar_aquatic_toxicity.csv local-data-warehouse/qsar_aquatic_toxicity/

        The structures come from the authors' own release, which UCI left out: the Excel file of the Milano
        Chemometrics group's page https://michem.unimib.it/download/data/acute-aquatic-toxicity-to-daphnia-magna/ (a
        RAR archive behind a notification form; the form page links the file on Google Drive, downloaded 2026-11-01).
        It holds CAS-RN, SMILES, the authors' train/test split, LC50 and the same 8 descriptors, in the UCI file's row
        order. The page states: "The dataset is freeware and may be used if proper reference is given to the authors."

        toxicity_data.xlsx (67,506 bytes), sha256
        61bcf1b04e60f4b7e7750568c197f1889db796076f06fbed94a78c8aaf581a0d
    """
    bibtex = """
        @article{cassotti2014prediction,
          title={Prediction of acute aquatic toxicity toward daphnia magna by using the ga-k nn method},
          author={Cassotti, Matteo and Ballabio, Davide and Consonni, Viviana and Mauri, Andrea and Tetko, Igor V and Todeschini, Roberto},
          journal={Alternatives to Laboratory Animals},
          volume={42},
          number={1},
          pages={31--41},
          year={2014},
          publisher={SAGE Publications Sage UK: London, England}
        }
    """
    curation_comments = """
        We start with the data from UCI and add the structures from the authors' own workbook.

        - The structure ships as `SMILES` (CLEAN-24 as amended, Lennart, 2026-11-01), in RDKit's canonical form (`canonical_smiles`; no salts or mixtures here), declared in `smiles_columns`, so a benchmark encodes it as a structure and never as text; the recommended encoding is `data_foundry.v2.chemistry.encode_smiles` (RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts).
        - The authors' 8 descriptors leave (Lennart, 2026-11-01, as for qsar_tid_11: the task goes from the structure to a prediction, and the descriptors are one modelling choice of the authors). This also settles the kept potential leak the record and `fit_reason` named: a genetic algorithm chose the eight by their fit to the measured toxicity of chemicals that sit in our test folds (LEAK-31), and with the structure shipped no such selection reaches the features.
        - The structures come from the authors' own workbook, which the UCI copy left out. It is the same 546 rows in the same order: all 8 descriptors and LC50 are identical on every row, so the link is exact and needs no key. All 546 SMILES parse, and no two are the same chemical, with or without stereochemistry.
        - Split (CLEAN-24, SPLIT-31 as amended): grouped on the Bemis-Murcko scaffold of the structure (`scaffold_groups`); chemicals without a ring, and those of a scaffold holding more than a tenth of the set, are groups of their own. An assessor estimates the toxicity of an untested chemical, often of a series not yet measured, so whole series are held out; qsar_bioconcentration, qsar_oral_toxicity, qsar_fish_toxicity and qsar_tid_11 group the same way. The source split at random.
    """

    # Task
    target = "LC50"
    problem_type = "regression"
    metric = Metric.fallback(
        reason="Cassotti et al. 2014 report Q2 (cv and external) with RMSE; r2 and rmse rank models the same within a fold. rmse is the regression fallback."
    )

    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a chemical series: the chemicals that share one Bemis-Murcko scaffold (ring systems and the chains linking them; Bemis and Murcko 1996), computed with RDKit from the structure. A chemical without a ring, or one of a scaffold that holds more than a tenth of the set, is a group of its own (SPLIT-31). An assessor estimates the toxicity of an untested chemical, often of a series not yet measured, so whole series are held out. Each row is one prediction, made from the chemical's structure alone.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the Bemis-Murcko scaffold: all chemicals of one series stay on one side, so a model predicts chemicals of a series it has not seen; chemicals without a ring are held out one by one. Chemicals with similar but not identical scaffolds can be on both sides.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        uci = pd.read_csv(raw_dir / RAW_FILE, sep=";", names=[*DESCRIPTORS, "LC50"])
        return {"uci": uci, "authors": pd.read_excel(raw_dir / STRUCTURES_FILE)}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        uci, authors = raw["uci"], raw["authors"]
        # The workbook is the UCI file with the structures added, row for row (curation_comments)
        assert len(uci) == len(authors), "the authors' workbook and the UCI file differ in length"
        assert np.allclose(uci[DESCRIPTORS].to_numpy(float), authors[DESCRIPTORS].to_numpy(float)), (
            "the authors' workbook and the UCI file differ in a descriptor"
        )
        # The structure ships as a SMILES column (`smiles_columns`), in RDKit's canonical form; the authors' 8
        # descriptors leave, one modelling choice of the structure (curation_comments)
        df = pd.DataFrame(
            {"SMILES": canonical_smiles(authors["SMILES"]), self.target: authors["LC50[-LOG(mol/L)]"].astype(float)}
        )
        # The split groups: the chemical series (Bemis-Murcko scaffold); no ring, or a scaffold above a tenth, alone
        return df.assign(scaffold=scaffold_groups(df["SMILES"]))

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the SMILES is typed by `smiles_columns`; the target stays numeric
        del df
        return FeatureTypes()
