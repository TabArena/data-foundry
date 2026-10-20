"""Curated dataset definition for `ecoli_proteins` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


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
        split="Random proteins, so the test data stands for proteins of unknown location.",
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
    year = "1996"
    domain = "biology & life sciences"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5388M"
    license = "CC BY 4.0"
    download_description = """
        wget https://archive.ics.uci.edu/static/public/39/ecoli.zip && unzip ecoli.zip && rm ecoli.zip ecoli.names
        mkdir -p local-data-warehouse/ecoli_proteins && mv ecoli.data local-data-warehouse/ecoli_proteins/
    """
    bibtex = """
        @inproceedings{horton1996probabilistic,
          title={A probabilistic classification system for predicting the cellular localization sites of proteins.},
          author={Horton, Paul and Nakai, Kenta},
          booktitle={Ismb},
          volume={4},
          pages={109--115},
          year={1996},
          organization={St. Louis, Missouri, USA}
        }
    """
    curation_comments = """
        We start with the dataset from UCI.

        - We drop the sequence name column, which is a unique identifier.
        - We drop three classes with less than 10 samples each: omL (5), imL (2), and imS (2).
        - We drop "chg", which becomes constant after our preprocessing steps.
        - We drop "aac", the score of a discriminant analysis of the amino-acid content of outer-membrane and
          periplasmic proteins. It was fitted to the labels of the authors' protein database, the predecessor of this
          dataset (Nakai & Kanehisa 1991, Proteins 11(2):95-110), and cannot be refitted per split, so it leaks the
          labels (the reason `yeast` was rejected). Without it, outer-membrane proteins (6% of rows) are barely
          recognised: TabPFN recall 0.02 instead of 0.90 (stratified 3-fold x 20).
    """

    # Task
    target = "class"
    problem_type = "multiclass_classification"

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
        df = df.drop(
            columns=[
                "Sequence Name",  # avoid leakage from look the name and otherwise unique identifier.
                "chg",  # constant after preprocessing
                "aac",  # discriminant fitted to the labels; leaks them
            ]
        )
        # Drop samples with classes with too little data (less than 10 samples)
        df = df[~df["class"].isin(["omL", "imL", "imS"])]
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "lip",
            ],
        )
