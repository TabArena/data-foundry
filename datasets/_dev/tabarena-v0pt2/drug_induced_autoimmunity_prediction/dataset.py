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
    canonical_smiles,
    decode,
    scaffold_groups,
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
        known=("The drug's chemical structure, as a SMILES string."),
        split=(
            "Whole chemical scaffolds (a drug's ring skeleton) are held out, so the test data stands for drugs from "
            "chemical series not seen in training."
        ),
        changes=(
            "We pool the source's training and test sets and split them by scaffold instead of at random; a drug "
            "entered twice as two stereoisomers is kept once, and the descriptors the source computed from the "
            "structure give way to the structure itself."
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
        - The structure ships as `SMILES` (CLEAN-24 as amended, Lennart, 2026-11-01; Andrej's call of 2026-10-26 to keep it), in RDKit's canonical form (`canonical_smiles`; 503 of the source's strings were not canonical, none is a salt), declared in `smiles_columns`, so a benchmark encodes it as a structure and never as text; the recommended encoding is `data_foundry.v2.chemistry.encode_smiles` (RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts). Scaffold-grouped ROC AUC over our 60 splits (LightGBM / random forest, 2026-11-01): the source's 176 descriptors 0.771 / 0.776, our full RDKit set in their place 0.772 / 0.777, the MACCS keys added 0.796 / 0.799 (better on 51 and 59 of 60 splits), the SMILES read as text (character n-grams) 0.763 / 0.766. Andrej measured the same gain for TabPFN 3.5 (0.803 to 0.826 with MACCS keys, 27 of 30 splits; `~/claude_jobs/dia_review/`).
        - The source's 176 RDKit descriptors leave (2026-11-01): RDKit computed them from the same SMILES, and the recommended encoding reproduces them (the full RDKit set scores as they do, above), so shipping both would give a model the structure twice.
        - Scaffold-grouped splits (2026-10-19), not random ones: under random splits about a third of the test drugs have a close relative in training with the same label, and a nearest-neighbour fingerprint lookup without a model reaches ROC AUC 0.822 against TabPFN's 0.854; with whole scaffolds held out, TabPFN 0.768, HGB 0.737, RF 0.724, LR 0.687 (generic scaffolds, `~/claude_jobs/dia_review/`). The use case screens new candidates, which come from series not yet seen, and scaffold splits are the standard for this: the Therapeutics Data Commons ADMET group splits all its endpoints by scaffold, among them drug-induced liver injury, a drug-level label like this one (Huang et al. 2021, NeurIPS Datasets and Benchmarks, arXiv:2102.09548). The source validated on random splits (its test file is as similar to its training file as a random split is), so our scores are lower than the paper's AUC 0.88-0.89 by design. The groups are the Bemis-Murcko scaffolds (Bemis and Murcko 1996, J Med Chem 39(15):2887-2893): 443 groups, the largest 41 drugs (benzene), 10 with both labels. The 53 drugs without a ring each form their own group (390 ring scaffolds plus these 53): they share no skeleton, only 2 have a close relative among them (Tanimoto >= 0.7), and their nearest neighbour's label agrees at the base rate (0.925). The groups come from `scaffold_groups` since 2026-11-01, as in qsar_bioconcentration and qsar_oral_toxicity: the same 443 groups as the definition's own code before, under other group names, so the drugs fall into other folds.
        - Duplicates dropped: 9 pairs of rows are one structure once the stereo marks are set aside (the same 18 rows that share every one of the source's descriptors), stereoisomers a 2D encoding does not tell apart (PubChem): quinine and quinidine, and 8 drugs entered twice with other stereo marks (lovastatin, fluticasone propionate, enalapril, fluvastatin, lisinopril, pravastatin, carbidopa, streptomycin), 3 pairs across the source's two files. We keep one row of the 8 pairs with one label and drop both streptomycin rows (one positive, one negative), as for qsar_oral_toxicity: 587 drugs, 140 positive (decision table).
        - The target (2026-11-01, CLEAN-25): `Label` ships its classes as words (1 is the event). Binary: "Yes" is the
          event, the class that sorts second, so it is the metrics' positive class.
    """

    # Task
    target = "Label"
    problem_type = "binary_classification"
    smiles_columns = ("SMILES",)
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
            One group is a chemical scaffold: the drugs that share one Bemis-Murcko scaffold (ring systems and the chains linking them, atom and bond types kept, stereochemistry dropped; Bemis and Murcko 1996), computed with RDKit from the source's SMILES. A drug without a ring is a group of its own, and so would be each drug of a scaffold holding more than a tenth of the drugs (SPLIT-31; none here: the bare benzene ring holds 7%). The use case is screening new drug candidates by structure, and a new candidate comes from a chemical series not yet tested, so whole scaffolds are held out, as the Therapeutics Data Commons ADMET benchmarks do (Huang et al. 2021). Each row is one prediction, made from the drug's structure alone.
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
        # The structure ships as a SMILES column (`smiles_columns`), in RDKit's canonical form; the source's RDKit
        # descriptors of it leave, since the recommended encoding reproduces them (curation_comments)
        df = pd.DataFrame({"SMILES": canonical_smiles(raw["SMILES"]), self.target: raw[self.target]})
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
        # The split groups: the chemical series (Bemis-Murcko scaffold); no ring, or a scaffold above a tenth, alone
        df = df.assign(scaffold=scaffold_groups(df["SMILES"]))
        # Stereoisomers are one structure to a 2D encoding: one row per pair with one label, none of a pair with two
        flat = canonical_smiles(df["SMILES"], stereo=False)
        keep = ~pd.DataFrame({"flat": flat, "label": df[self.target]}).duplicated()
        df, flat = df[keep], flat[keep]
        return df[~flat.duplicated(keep=False)]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the SMILES is typed by `smiles_columns`; the target becomes a category
        del df
        return FeatureTypes()

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        flat = canonical_smiles(raw["SMILES"], stereo=False)
        shared = raw[flat.duplicated(keep=False)]
        pair = flat[shared.index].rank(method="dense").astype(int).rename("pair")
        labels = shared.groupby(pair)[self.target].transform("nunique")
        pairs = (
            shared[["SMILES", self.target]]
            .assign(pair=pair, kept=labels.eq(1) & ~flat[shared.index].duplicated())
            .set_index("pair")
            .sort_index(kind="stable")
        )
        return [
            Decision(
                "Stereoisomers that are one 2D structure are kept once",
                "A 2D encoding carries no stereochemistry, so each pair differs only in the stereo marks of its "
                "SMILES (the source's 2D descriptors are equal too). "
                "Quinine and quinidine are two drugs; the other pairs are one drug entered twice with other stereo "
                "marks. A pair with one label keeps one row, the pair with both labels (streptomycin) none.",
                pairs,
            ),
        ]
