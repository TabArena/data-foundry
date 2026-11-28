"""Curated dataset definition for `ecoli_proteins` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_foundry.definition import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    TaskSummary,
    TimeBasis,
)

# each shipped protein's family: UniProt protein family, else its Pfam domains, else the protein alone (lookup of
# 2026-11-23 from the SWISS-PROT entry names)
FAMILIES = "protein_families.csv"


class EcoliProteins(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Where in an E. coli cell does a protein reside?",
        use_case=(
            "For example, a biologist predicts where a newly sequenced bacterial protein sits in the cell from its "
            "amino-acid sequence, before or instead of testing it in the lab."
        ),
        row="One protein of the bacterium E. coli with a known location (327 proteins, UCI 1996).",
        predicted=(
            "The location: cytoplasm (44%), inner membrane without a signal sequence (24%), periplasm (16%), inner "
            "membrane with an uncleavable signal sequence (11%) or outer membrane (6%)."
        ),
        known=(
            "Five scores computed from the sequence: two signal-sequence recognition methods, a lipoprotein signal "
            "score and two membrane-spanning region predictions."
        ),
        split=(
            "Random proteins, so the test data stands for proteins of unknown location; over the SWISS-PROT entry "
            "years the relation of the scores to the location measures stable."
        ),
        changes=(
            "We drop the three rarest locations (inner- and outer-membrane lipoproteins, and inner membrane with a "
            "cleavable signal sequence), each with fewer than 10 proteins, and the amino-acid content score, a "
            "discriminant fitted to the labels."
        ),
        fit="direct",
        fit_reason=(
            "The scores come from the sequence alone, which is known before any experiment, and a held-out protein is"
            " one of unknown location. The data is small and from 1996."
        ),
    )

    # Dataset
    unique_name = "ecoli_proteins"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5388M",
            license="CC BY 4.0",
            year="1996",
            bibtex="""
                @inproceedings{horton1996probabilistic,
                  title={A probabilistic classification system for predicting the cellular localization sites of proteins.},
                  author={Horton, Paul and Nakai, Kenta},
                  booktitle={Ismb},
                  volume={4},
                  pages={109--115},
                  year={1996},
                  organization={St. Louis, Missouri, USA}
                }
            """,
        ),
    )
    download_description = """
        wget https://archive.ics.uci.edu/static/public/39/ecoli.zip && unzip ecoli.zip && rm ecoli.zip ecoli.names
        mkdir -p local-data-warehouse/ecoli_proteins && mv ecoli.data local-data-warehouse/ecoli_proteins/
    """
    curation_comments = """
        We start with the dataset from UCI.

        - We drop the sequence name column, which is a unique identifier.
        - We drop three classes with less than 10 samples each: omL (5), imL (2), and imS (2).
        - We drop "chg", which becomes constant after our preprocessing steps.
        - We drop "aac", the score of a discriminant analysis of the amino-acid content of outer-membrane and
          periplasmic proteins. It was fitted to the labels of the authors' protein database, the predecessor of this
          dataset (Nakai & Kanehisa 1991, Proteins 11(2):95-110), and cannot be refitted per split, so it leaks the
          labels (the reason `yeast` was rejected). Dropped and the task kept, as the amended LEAK-27 says when the
          other columns still make a real one (Andrej, 2026-11-11). Without it, outer-membrane proteins (6% of rows)
          are barely recognised: TabPFN recall 0.02 instead of 0.90 (stratified 3-fold x 20).
        - Split by protein family (Andrej, 2026-11-23): `protein_families.csv` next to this file maps each of the 327 shipped proteins from its SWISS-PROT entry name to a UniProt accession (289 by ID mapping, 20 by a text search of renamed entries; UniProt REST, 2026-11-23) and to its UniProt protein family (270), else to its set of Pfam domains (39), else to itself (18 unresolved). 219 families, at most 12 proteins in one; 11 families hold proteins of more than one location. UniRef50 clusters are too fine to group anything (312 of 319 hold one protein). On 20 x 3 folds without `aac`, family-held-out folds cost logistic regression +0.015 ± 0.004 and TabPFN +0.012 ± 0.005 log loss against random folds (0.472 and 0.463), the ranking unchanged; under random folds 41% of test proteins had a family member in training and carried 33% of the loss.
    """
    split_leaf = "L-FAMILY.key"
    time_basis = TimeBasis(
        "UnseenGroup",
        """
        the catalogue is split by protein family, its default key: three windows on the SWISS-PROT entry years
        (1986-1995) would need the 1989-90 window, trained on 37%, as an exception, so the entry date does not
        decide. Holding out whole families tests a protein whose family the training set lacks, as the localisation
        of a newly sequenced protein meets it; under random folds 41% of the test proteins had a family member in
        training. The entry years and the stationary-relation test (2026-11-19, flat narrowly; the location mix moves,
        cytoplasm 54% of entries up to 1989 against 34% from 1990) go in the notes; that test ran on the six
        scores, `aac` included, before `aac` was dropped. Not tested: a later entry year.
        """,
        set_by="Andrej",
        on="2026-11-23",
        note="`StationaryRelation` before",
    )

    # Task
    target = "class"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "Horton & Nakai 1996 report cross-validated accuracy (81% over 8 sites), a field habit without costs; we keep"
            " 5 of the 8 sites, so the figure's meaning changed (MET-2). Original rejected: accuracy. log_loss is the "
            "multiclass fallback."
        ),
    )

    grouping = Grouping(
        on="protein_family",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a protein family: the UniProt protein family of the protein's SWISS-PROT entry, else its set of Pfam domains, else the protein alone where the entry name could not be resolved (`protein_families.csv`). Each row is one protein and one prediction of its cell location from its sequence scores. The use case is the location of a protein of a family not seen in training; related proteins share sequence signals, so their scores and their location move together.
        """,
    )

    accepted_check_warnings = {
        "splits_class_missing": (
            "One of the 60 family-grouped test folds (r1f2) lacks one of the five locations: the outer-membrane "
            "proteins (20) sit in few families, 6 in the TonB-dependent receptors and 4 in the porins, so a fold can "
            "draw none. The metric is log loss, which a missing class in a test fold does not break (Andrej, "
            "2026-11-23)."
        ),
    }

    # Splits
    splits_comment = """
        Grouped 20 x 3 folds on the protein family (219 families, at most 12 proteins; 18 unresolved proteins each their own group): a family's proteins stay on one side, so the model predicts the location of a protein whose relatives it has not seen. One of the 60 test folds lacks the outer-membrane location (20 proteins in few families); log loss is unaffected. The SWISS-PROT entry years (1986-1995) would give three windows only with the 1989-90 window trained on 37%, so the catalogue's family key decides (SPLIT-37). Against random folds, holding out families costs +0.012 to +0.015 log loss for TabPFN and logistic regression, the ranking unchanged (curation notes).
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        feature_names = [
            "Sequence Name",
            "mcg",
            "gvh",
            "lip",
            "chg",
            "aac",
            "alm1",
            "alm2",
            "class",
        ]
        df = pd.read_csv(raw_dir / "ecoli.data", header=None, names=feature_names, sep=r"\s+")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Drop samples with classes with too little data (less than 10 samples)
        df = df[~df["class"].isin(["omL", "imL", "imS"])].copy()
        # the protein's family, the group of the split (no input)
        families = pd.read_csv(self.folder / FAMILIES).set_index("sequence_name")["protein_family"]
        df["protein_family"] = df["Sequence Name"].map(families).astype("category")
        assert df["protein_family"].notna().all()
        df = df.drop(
            columns=[
                "Sequence Name",  # avoid leakage from look the name and otherwise unique identifier.
                "chg",  # constant after preprocessing
                "aac",  # discriminant fitted to the labels; leaks them
            ]
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "lip",
            ],
        )
