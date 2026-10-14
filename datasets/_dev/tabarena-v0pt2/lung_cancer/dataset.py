"""Curated dataset definition for `lung_cancer` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


class LungCancer(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Which type of lung tissue, tumour or normal, does a specimen's gene expression profile show?"),
        use_case=(
            "For example, a pathology lab assigns a lung specimen to its tissue type from its gene expression "
            "profile, as a check on the microscope reading."
        ),
        row=(
            "One lung tissue specimen of a 2001 study (Bhattacharjee et al., its Dataset A without the 6 small-cell "
            "carcinomas: 197 specimens); the place and period are not stated in the definition."
        ),
        predicted=(
            "The tissue type by histology: adenocarcinoma (71%, including 12 suspected metastases of adenocarcinomas "
            "from other organs), squamous cell carcinoma (11%), pulmonary carcinoid (10%) or normal lung (9%)."
        ),
        known="The expression of 12,600 gene probes measured by microarray on the specimen.",
        split="Random specimens, so the test data stands for new specimens of the same study.",
        changes=(
            "We drop the 6 small-cell carcinomas. The source already merges lung adenocarcinomas with 12 suspected "
            "metastases from other organs, which we cannot separate."
        ),
        fit="approximate",
        fit_reason=(
            "The label is the histology pathologists already read under the microscope, so the profile reproduces a "
            "known diagnosis; the adenocarcinoma class mixes lung tumours with metastases, and whether expression "
            "would be measured for this purpose is unclear (record). The study itself used the data to find "
            "subclasses."
        ),
    )

    # Dataset
    unique_name = "lung_cancer"
    year = "2001"
    domain = "medical & healthcare"
    source = "Other"  # supplementary materials of the paper
    source_url = "https://www.pnas.org/doi/10.1073/pnas.191502998#supplementary-materials"
    license = "None"  # not given as part of data download on the website, likely Copyright for the journal
    download_description = """
        Cannot download automatically!

        Click and download yourself: "https://www.pnas.org/doi/suppl/10.1073/pnas.191502998/suppl_file/dataseta_12600gene.xls"
        mkdir -p local-data-warehouse/lung_cancer/ && mv dataseta_12600gene.xls local-data-warehouse/lung_cancer/
    """
    bibtex = """
        @article{bhattacharjee2001classification,
          title={Classification of human lung carcinomas by mRNA expression profiling reveals distinct adenocarcinoma subclasses},
          author={Bhattacharjee, Arindam and Richards, William G and Staunton, Jane and Li, Cheng and Monti, Stefano and Vasa, Priya and Ladd, Christine and Beheshti, Javad and Bueno, Raphael and Gillette, Michael and others},
          journal={Proceedings of the National Academy of Sciences},
          volume={98},
          number={24},
          pages={13790--13795},
          year={2001},
          publisher={The National Academy of Sciences}
        }
    """
    curation_comments = """
        - The original data comes with lung adenocarcinoma and other adenocarcinomas merged into one class already. We keep the same and were not able to find a way to reverse this from the public data.
        - We also drop the class "small-cell lung carcinoma" as it only has 6 samples, which is not a meaningful sample size for benchmarking, or the predictive task.  We could add another version with all classes in the future.
    """

    # Task
    target = "CancerType"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(f"{raw_dir}/dataseta_12600gene.xls")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Translate into tabular format
        df = (
            df.set_index("probe set")  # use probe set as row index → becomes columns after .T
            .drop(columns=["gene"])  # drop unwanted column
            .T.reset_index(names="CancerType")  # transpose
        )
        # Extract classes from index
        prefix_to_class = {
            "AD": "lung adenocarcinoma",
            "SQ": "squamous cell carcinoma",
            "COID": "pulmonary carcinoid",
            "SMCL": "small-cell lung carcinoma",
            "NL": "normal lung",
        }
        # extract prefix and map to class
        df["CancerType"] = df["CancerType"].str.split("-").str[0].map(prefix_to_class)
        df = df[df["CancerType"] != "small-cell lung carcinoma"]
        return df
