"""Curated dataset definition for `qsar_fish_toxicity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


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
        known=(
            "Six molecular descriptors computed from the structure: an information index, a matrix-based index, an "
            "autocorrelation of ionisation potential, two counts of carbon atom types, and the predicted "
            "octanol-water partition coefficient."
        ),
        split="Random chemicals, so the test data stands for chemicals not yet tested.",
        fit="direct",
        fit_reason=(
            "The descriptors come from the structure alone, which is all a toxicologist has for an untested chemical."
            " 24% of the rows share all six descriptors with another row: isomers whose toxicity differs but which "
            "look identical to the model."
        ),
    )

    # Dataset
    unique_name = "qsar_fish_toxicity"
    year = "2015"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5JG7B"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/qsar_fish_toxicity/ && wget -P local-data-warehouse/qsar_fish_toxicity/ https://archive.ics.uci.edu/static/public/504/qsar+fish+toxicity.zip && unzip local-data-warehouse/qsar_fish_toxicity/qsar+fish+toxicity.zip -d local-data-warehouse/qsar_fish_toxicity/
    """
    bibtex = r"""
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
    """
    curation_comments = """
        - We assigned descriptive column names following the original dataset documentation.
        - 24% of the rows share all six descriptors with another row, but LC50 differs within every shared vector: they are distinct chemicals (isomers) the descriptors cannot tell apart, not repeated measurements, so we keep them.
        - The six descriptors were chosen by a genetic algorithm on the paper's training set (726 of the 908 chemicals), which overlaps our test folds: a mild optimism we cannot measure. No descriptor is derived from the target.
    """

    # Task
    target = "LC50"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/qsar_fish_toxicity.csv", sep=";", header=None)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "LC50"
        df.columns = [
            "CIC0",
            "SM1_Dz(Z)",
            "GATS1i",
            "NdsCH",
            "NdssC",
            "MLOGP",
            target_feature,
        ]
        return df
