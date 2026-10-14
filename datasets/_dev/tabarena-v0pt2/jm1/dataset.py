"""Curated dataset definition for `jm1` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import openml
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary

if TYPE_CHECKING:
    import pandas as pd


class Jm1(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a function of a NASA software system have a reported defect?",
        use_case=(
            "For example, a verification team decides which modules of a large C program to inspect by hand first, "
            "from static code measures that are cheap to collect (the use the source describes)."
        ),
        row=(
            "One module (a C function) of JM1, a NASA real-time ground system that simulates missions, from the NASA "
            "Metrics Data Program (8,736 modules after removing duplicates); the period is not stated."
        ),
        predicted=(
            "Whether the module has one or more reported defects (22% do). Over which period the defects were "
            "reported is not stated."
        ),
        known=(
            "21 static measures of the module's code: line counts (code, comments, blank lines), McCabe measures of "
            "the complexity of its control paths, and Halstead measures from counts of operators and operands."
        ),
        split=(
            "Random modules of the same program, so the test data stands for modules of this program not yet inspected."
        ),
        changes=(
            "We drop exact duplicate rows and every copy of a code-measure profile that appears with both labels "
            "(10,885 to 8,736 rows); 25% of the rows shared their profile with another row."
        ),
        fit="approximate",
        fit_reason=(
            "Inspecting the riskiest modules first is a real decision, but the label has no stated horizon and when "
            "the code was measured relative to the defect reports and their fixes is not stated, so the measures may "
            "describe the fixed code."
        ),
    )

    # Dataset
    unique_name = "jm1"
    year = "2004"
    domain = "technology & internet"
    source = "Other"  # the PROMISE repository (from the NASA Metrics Data Program); OpenML 1053 is a copy
    source_url = "http://promise.site.uottawa.ca/SERepository/datasets/jm1.arff"  # plain http only; https gives 404
    license = "Public Domain"
    download_description = """
        `_load_raw` reads OpenML dataset 1053 with openml-python, which downloads the file to its own cache
        (~/.cache/openml), not to local-data-warehouse/jm1/. To fetch it before a check or build:

        .venv/bin/python -c "import openml; openml.datasets.get_dataset(1053, download_data=True).get_data()"

        OpenML 1053 is a copy of jm1.arff from the PROMISE repository (the source URL). The ARFF on OpenML
        (https://api.openml.org/data/v1/download/53936/jm1.arff) is byte-identical to the PROMISE file (md5
        0c19aefce52ccb955d0de57e4c0fe8bf), and the parquet that openml-python 0.15 reads
        (https://data.openml.org/datasets/0000/1053/dataset_1053.pq) holds the same 10,885 rows and values. The
        PROMISE file answers over plain http only; the Wayback Machine holds the same file:
        https://web.archive.org/web/20240126152134id_/http://promise.site.uottawa.ca/SERepository/datasets/jm1.arff
    """
    bibtex = """
        @inproceedings{menzies2004good,
          title={How good is your blind spot sampling policy},
          author={Menzies, Tim and Di Stefano, Justin S},
          booktitle={Eighth IEEE International Symposium on High Assurance Systems Engineering, 2004. Proceedings.},
          pages={129--138},
          year={2004},
          organization={IEEE}
        }
    """
    curation_comments = """
        - We selected this dataset as representative of a set of predictive modeling tasks of software engineering (other examples of such tasks are available on OpenML under the names mozilla4, pc1, pc2, pc3, mc1, kc1, kc2). This dataset was selected as it has the largest sample size.
        - We drop duplicates. 25% of the rows share their code-metric vector with another row (669 groups, mostly trivial modules such as 173 copies of a 4-line, complexity-1 function), so a random split puts copies on both sides. We drop exact duplicate rows (1,973) and then every copy of a metric vector that appears with both labels (88 vectors, 176 rows): 10,885 -> 8,736 rows.
        - The source URL is jm1.arff of the PROMISE repository, donated in 2004 by Tim Menzies from the NASA Metrics Data Program; it answers over plain http but gives 404 over https, and the Wayback Machine holds the same file. We read OpenML dataset 1053, whose ARFF is byte-identical to it (see the download description).
    """

    # Task
    target = "defects"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = openml.datasets.get_dataset(1053).get_data()[0]
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.drop_duplicates()
        features = [c for c in df.columns if c != self.task_metadata.target_column_name]
        df = df[~df.duplicated(subset=features, keep=False)]
        return df.reset_index(drop=True)
