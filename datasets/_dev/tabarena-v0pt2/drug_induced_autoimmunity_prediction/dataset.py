"""Curated dataset definition for `drug_induced_autoimmunity_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    TaskSummary,
    drop_columns,
    murcko_scaffolds,
)


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
            "Whole chemical scaffolds (a drug's ring skeleton) are held out, so the test data stands for drugs from "
            "chemical series not seen in training."
        ),
        changes=(
            "We pool the source's training and test sets, split them by scaffold instead of at random and drop the "
            "structure's text, keeping the descriptors computed from it; a drug entered twice as two stereoisomers is "
            "kept once."
        ),
        fit="direct",
        fit_reason=(
            "The features come from the structure alone, which is all a screen has before testing, and the test drugs"
            " come from scaffolds the model has not seen, as new candidates do. The set is small."
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
        - Scaffold-grouped splits (2026-10-19), not random ones: under random splits about a third of the test drugs have a close relative in training with the same label, and a nearest-neighbour fingerprint lookup without a model reaches ROC AUC 0.822 against TabPFN's 0.854; with whole scaffolds held out, TabPFN 0.768, HGB 0.737, RF 0.724, LR 0.687 (generic scaffolds, `~/claude_jobs/dia_review/`). The use case screens new candidates, which come from series not yet seen, and scaffold splits are the standard for this: the Therapeutics Data Commons ADMET group splits all its endpoints by scaffold, among them drug-induced liver injury, a drug-level label like this one (Huang et al. 2021, NeurIPS Datasets and Benchmarks, arXiv:2102.09548). The source validated on random splits (its test file is as similar to its training file as a random split is), so our scores are lower than the paper's AUC 0.88-0.89 by design. The groups are the Bemis-Murcko scaffolds (Bemis and Murcko 1996, J Med Chem 39(15):2887-2893): 443 groups, the largest 41 drugs (benzene), 10 with both labels. The 53 drugs without a ring each form their own group (390 ring scaffolds plus these 53): they share no skeleton, only 2 have a close relative among them (Tanimoto >= 0.7), and their nearest neighbour's label agrees at the base rate (0.925).
        - Duplicates dropped: without the SMILES, 9 pairs of rows share every descriptor, all stereoisomers, which 2D descriptors do not tell apart (PubChem): quinine and quinidine, and 8 drugs entered twice with other stereo marks (lovastatin, fluticasone propionate, enalapril, fluvastatin, lisinopril, pravastatin, carbidopa, streptomycin), 3 pairs across the source's two files. We keep one row of the 8 pairs with one label and drop both streptomycin rows (one positive, one negative), as for qsar_oral_toxicity: 587 drugs, 140 positive (decision table).
    """

    # Task
    target = "Label"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Huang, Liu & Huang 2024 (InterDIA) report AUC, accuracy, sensitivity, specificity, F1 and MCC side by side; "
            "no unique metric. roc_auc is the binary fallback."
        ),
    )
    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a chemical scaffold: the drugs that share one Bemis-Murcko scaffold (ring systems and the chains linking them, atom and bond types kept, stereochemistry dropped; Bemis and Murcko 1996), computed with RDKit from the source's SMILES. A drug without a ring is a group of its own. The use case is screening new drug candidates by structure, and a new candidate comes from a chemical series not yet tested, so whole scaffolds are held out, as the Therapeutics Data Commons ADMET benchmarks do (Huang et al. 2021). Each row is one prediction, made from the drug's descriptors alone.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the Bemis-Murcko scaffold: all drugs with one ring skeleton stay on one side, so a model predicts drugs of a series it has not seen. Drugs with similar but not identical scaffolds can be on both sides.
    """

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
        # The split groups: the Bemis-Murcko scaffold, a drug without a ring on its own
        scaffold = murcko_scaffolds(df["SMILES"])
        df = df.assign(scaffold=scaffold.mask(scaffold.eq(""), "acyclic: " + df["SMILES"]))
        # The structure is in the source's RDKit descriptors; the SMILES text adds nothing to them
        df = drop_columns(df, ["SMILES"])
        # Stereoisomers share every 2D descriptor: one row per pair with one label, none of a pair with two
        features = df.columns.drop([self.target, "scaffold"])
        df = df.drop_duplicates(subset=[*features, self.target])
        return df[~df.duplicated(subset=features, keep=False)]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # every feature is a descriptor; the RDKit fragment counts stay numeric even where only 0 and 1 occur
        # (CLEAN-14)
        del df
        return FeatureTypes()

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        descriptors = raw.columns.drop(["SMILES", self.target])
        shared = raw[raw.duplicated(subset=descriptors, keep=False)]
        pair = shared.groupby(list(descriptors), sort=False, dropna=False, observed=True).ngroup().rename("pair") + 1
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
