"""Curated dataset definition for `qsar_aquatic_toxicity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


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
        known=(
            "Eight molecular descriptors computed from the structure, such as polar surface area, a fat-solubility "
            "estimate, the number of nitrogen atoms and counts of atom fragments."
        ),
        split="Random chemicals, so the test data stands for new chemicals like those measured.",
        fit="approximate",
        fit_reason=(
            "The descriptors come from the structure alone, as in screening, but the authors chose these eight from a"
            " larger set by their fit to the toxicity values, which may carry information on the test chemicals into "
            "the features."
        ),
    )

    # Dataset
    unique_name = "qsar_aquatic_toxicity"
    year = "2014"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5SG7H"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/505/qsar+aquatic+toxicity.zip && unzip qsar+aquatic+toxicity.zip && rm qsar+aquatic+toxicity.zip && mkdir -p local-data-warehouse/qsar_aquatic_toxicity && mv qsar_aquatic_toxicity.csv local-data-warehouse/qsar_aquatic_toxicity/
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
        We start with the data from UCI.

        - Note, the dataset has only a subset of features of the original data. The original data was reduced through feature selection with kNN by the authors in the paper above. We only have the 8 descriptors available in the UCI version. This might leak target information into the feature selection (or behave like an expert giving us the best features). Moreover, it biases the datasets and might make it trivial.
    """

    # Task
    target = "LC50"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = ["TPSA", "SAacc", "H-050", "MLOGP", "RDCHI", "GATS1p", "nN", "C-040", "LC50"]
        df = pd.read_csv(raw_dir / "qsar_aquatic_toxicity.csv", sep=";", names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        return df
