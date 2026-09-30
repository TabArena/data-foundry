"""Curated dataset definition for `qsar_aquatic_toxicity` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class QsarAquaticToxicity(AbstractCuratedDataset):
    # Dataset
    unique_name = "qsar_aquatic_toxicity"
    year = "2014"
    domain = "biology & life sciences"
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
