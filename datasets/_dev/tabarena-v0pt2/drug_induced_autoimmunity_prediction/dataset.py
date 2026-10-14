"""Curated dataset definition for `drug_induced_autoimmunity_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns


class DrugInducedAutoimmunityPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Can a drug cause an autoimmune reaction, judging from its chemical structure?",
        use_case=(
            "For example, a toxicologist screens drug candidates by structure early in development and decides which "
            "need closer testing for autoimmune side effects; the source aims at flagging that risk."
        ),
        row="One drug, given by its chemical structure (587 drugs; InterDIA, Huang et al. 2025).",
        predicted=(
            "Whether the drug is labelled as causing drug-induced autoimmunity (23.85% are); how the positive and "
            "negative drugs were chosen is not stated in the definition."
        ),
        known=(
            "Descriptors computed from the structure with RDKit (size, shape and connectivity indices, charge and "
            "polarity measures, counts of rings and chemical groups)."
        ),
        split=(
            "Random drugs, so the test data stands for drugs not seen in training; close structural relatives of a "
            "test drug can be in training."
        ),
        changes=(
            "We pool the source's training and test sets, split them at random and drop the structure's text, "
            "keeping the descriptors computed from it; a drug entered twice as two stereoisomers is kept once."
        ),
        fit="direct",
        fit_reason=(
            "The features come from the structure alone, which is all a screen has before testing, and the test drugs"
            " are unseen. The set is small, and a new candidate may differ more from known drugs than a random test "
            "drug does."
        ),
    )

    # Dataset
    unique_name = "drug_induced_autoimmunity_prediction"
    year = "2025"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5332M"
    license = "CC BY 4.0"
    download_description = """
        wget https://archive.ics.uci.edu/static/public/1104/drug_induced_autoimmunity_prediction.zip && unzip drug_induced_autoimmunity_prediction.zip && rm drug_induced_autoimmunity_prediction.zip RDKit_ChemDes.xlsx && mkdir -p local-data-warehouse/drug_induced_autoimmunity_prediction && mv DIA_trainingset_RDKit_descriptors.csv local-data-warehouse/drug_induced_autoimmunity_prediction/ && mv DIA_testset_RDKit_descriptors.csv local-data-warehouse/drug_induced_autoimmunity_prediction/
    """
    bibtex = """
        @article{huang2025interdia,
          title={InterDIA: Interpretable prediction of drug-induced autoimmunity through ensemble machine learning approaches},
          author={Huang, Lina and Liu, Peineng and Huang, Xiaojie},
          journal={Toxicology},
          volume={511},
          pages={154064},
          year={2025},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        We start with the dataset from UCI.

        - We pool the source's training file (477 drugs, 118 positive) and test file (120 drugs, 30 positive) into 597 drugs and use our own splits; the files share no SMILES, and UCI's count of 477 instances is the training file alone.
        - We drop the constant columns, and fr_Nhpyrrole, MaxEStateIndex and fr_benzene, which copy other descriptor columns in these drugs.
        - `SMILES` dropped, as in every SMILES dataset (2026-10-14): the source's RDKit descriptors carry the structure, and next to them the SMILES as text (character n-grams) lowers LightGBM's ROC AUC from 0.835 to 0.810, on 15 of 15 splits.
        - Duplicates dropped: without the SMILES, 9 pairs of rows share every descriptor, all stereoisomers, which 2D descriptors do not tell apart (PubChem): quinine and quinidine, and 8 drugs entered twice with other stereo marks (lovastatin, fluticasone propionate, enalapril, fluvastatin, lisinopril, pravastatin, carbidopa, streptomycin), 3 pairs across the source's two files. We keep one row of the 8 pairs with one label and drop both streptomycin rows (one positive, one negative), as for qsar_oral_toxicity: 587 drugs, 140 positive (decision table).
    """

    # Task
    target = "Label"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "DIA_trainingset_RDKit_descriptors.csv")
        df = pd.concat([df, pd.read_csv(raw_dir / "DIA_testset_RDKit_descriptors.csv")], ignore_index=True)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Drop constant columns
        constant_cols = df.columns[df.nunique(dropna=False) == 1]
        df = df.drop(columns=constant_cols)
        # dropping duplicated columns (by chance)
        duplicated = ["fr_Nhpyrrole", "MaxEStateIndex", "fr_benzene"]
        df = df.drop(columns=duplicated)
        # The structure is in the source's RDKit descriptors; the SMILES text adds nothing to them
        df = drop_columns(df, ["SMILES"])
        # Stereoisomers share every 2D descriptor: one row per pair with one label, none of a pair with two
        df = df.drop_duplicates()
        return df[~df.duplicated(subset=df.columns.drop(self.target), keep=False)]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes()

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        descriptors = raw.columns.drop(["SMILES", self.target])
        shared = raw[raw.duplicated(subset=descriptors, keep=False)]
        pair = shared.groupby(list(descriptors), sort=False, dropna=False).ngroup().rename("pair") + 1
        labels = shared.groupby(pair)[self.target].transform("nunique")
        pairs = (
            shared[["SMILES", self.target]]
            .assign(pair=pair, kept=labels.eq(1) & ~shared.duplicated(subset=descriptors))
            .set_index("pair")
            .sort_index(kind="stable")
        )
        return [
            Decision(
                "Stereoisomers that share every descriptor are kept once",
                "2D descriptors carry no stereochemistry, so without the SMILES each pair is one feature vector. "
                "Quinine and quinidine are two drugs; the other pairs are one drug entered twice with other stereo "
                "marks. A pair with one label keeps one row, the pair with both labels (streptomycin) none.",
                pairs,
            ),
        ]
