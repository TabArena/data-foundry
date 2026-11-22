"""Curated dataset definition for `ecoli_proteins` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, TimeBasis


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
            "Six scores computed from the sequence: two signal-sequence recognition methods, a lipoprotein signal "
            "score, an amino-acid content score and two membrane-spanning region predictions."
        ),
        split=(
            "Random proteins, so the test data stands for proteins of unknown location; over the SWISS-PROT entry "
            "years the relation of the scores to the location measures stable."
        ),
        changes=(
            "We drop the three rarest locations (inner- and outer-membrane lipoproteins, and inner membrane with a "
            "cleavable signal sequence), each with fewer than 10 proteins."
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
    """
    time_basis = TimeBasis(
        "StationaryRelation",
        """
        the proteins are dated by their SWISS-PROT entry years (1986-1995; 309 of 336 entries dated, UniProt and
        UniSave lookup of 2026-11-16), and the random folds stand for later entries because the relation reads flat.
        The stationary-relation test (2026-11-19, log loss, 5 seeds, 297 dated proteins, periods up to 1988, 1989-90,
        1991-92 and 1993-96) pooled over the three tested periods gives LightGBM +0.012 ± 0.047 and Kumo-Tabular
        +0.034 ± 0.033; over the two periods trained on half the data or more Kumo-Tabular gives +0.050 ± 0.047
        (2 SD 9.8 floors of 10), flat, narrowly. The location mix moves (cytoplasm 54% of entries up to 1989 against
        34% from 1990) but under twofold, so it changes which proteins arrive, not how the scores map to a location.
        Three windows on the entry year would need the 1989-90 window, trained on 37%, as an exception and would
        test 46 to 76 proteins each; the 20 x 3 random folds stay. Not tested: a protein of a family the 1996
        database did not hold, and homologous proteins on both sides of the split, which the dropped accessions
        would be needed to find.
        """,
        set_by="Andrej",
        on="2026-11-20",
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
