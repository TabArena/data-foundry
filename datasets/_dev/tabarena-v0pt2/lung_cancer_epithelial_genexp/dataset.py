"""Curated dataset definition for `lung_cancer_epithelial_genexp` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


class LungCancerEpithelialGenexp(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Does a smoker with suspected lung cancer have it, judging from gene activity in cells brushed from the "
            "airway?"
        ),
        use_case=(
            "During bronchoscopy for suspected lung cancer, a pulmonologist brushes cells from the normal-looking "
            "airway and uses their gene expression to judge whether the patient has cancer and needs further invasive"
            " tests (Spira et al. 2007)."
        ),
        row=(
            "One smoker undergoing bronchoscopy for suspected lung cancer (187 patients of the extended GEO release "
            "GSE4115)."
        ),
        predicted=(
            "Whether the patient was finally diagnosed with lung cancer (52% were); the time to the final diagnosis "
            "is not stated."
        ),
        known=(
            "The measured activity of about 22,000 gene probes (Affymetrix microarrays) in the brushed airway cells."
        ),
        split="Random patients, standing for new patients examined the same way.",
        changes=(
            "We use the extended release of 192 patients rather than the paper's 129 and drop the 5 whose diagnosis "
            "was still open."
        ),
        fit="direct",
        fit_reason=(
            "The sample is taken at the bronchoscopy, before the diagnosis is known, and a held-out patient is a new "
            "one. The task is small, with 187 patients and far more genes than patients."
        ),
    )

    # Dataset
    unique_name = "lung_cancer_epithelial_genexp"
    year = "2006"
    domain = "medical & healthcare"
    source = "GOV Website"
    source_url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4115"
    license = "Public Domain"
    download_description = """
        We download the original gene expression data from the GEO records.

        mkdir -p local-data-warehouse/lung_cancer_epithelial_genexp/ && wget -P local-data-warehouse/lung_cancer_epithelial_genexp/ https://ftp.ncbi.nlm.nih.gov/geo/series/GSE4nnn/GSE4115/matrix/GSE4115_series_matrix.txt.gz && gzip -d local-data-warehouse/lung_cancer_epithelial_genexp/GSE4115_series_matrix.txt.gz
    """
    bibtex = """
        @article{spira2007airway,
          title={Airway epithelial gene expression in the diagnostic evaluation of smokers with suspect lung cancer},
          author={Spira, Avrum and Beane, Jennifer E and Shah, Vishal and Steiling, Katrina and Liu, Gang and Schembri, Frank and Gilman, Sean and Dumas, Yves-Martine and Calner, Paul and Sebastiani, Paola and others},
          journal={Nature medicine},
          volume={13},
          number={3},
          pages={361--366},
          year={2007},
          publisher={Nature Publishing Group US New York}
        }
    """
    curation_comments = """
        - We start with an extended dataset of 192 patients. The original reference uses 129 samples as "Individuals without final diagnoses as of May 2005 were excluded from this primary dataset". We remove 5 samples without a clear label ("Smoker with suspect lung cancer Sample"), yielding a dataset of 187 samples.
        - We use "Sample_title" from the metadata as labels for the prediction task.
    """

    # Task
    target = "DiagnosedCancer"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "GSE4115_series_matrix.txt", sep="\t", comment="!", index_col=0).T
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # read labels
        with open(self.raw_dir / "GSE4115_series_matrix.txt") as f:
            for line in f:
                if line.startswith("!Sample_title"):
                    labels = [t.strip('"') for t in line.strip().split("\t")[1:]]
                    break
        df["DiagnosedCancer"] = pd.Series(labels, index=df.index)

        def resolve_label(label):
            if label.startswith("Smoker diagnosed with cancer Sample"):
                return "Yes"
            if label.startswith("Smoker NOT diagnosed with cancer Sample"):
                return "No"
            if label.startswith("Smoker with suspect lung cancer Sample"):
                return np.nan
            raise ValueError(f"Unknown label: {label}")

        df["DiagnosedCancer"] = df["DiagnosedCancer"].apply(resolve_label)
        df = df.dropna(subset=["DiagnosedCancer"])  # remove suspected cancer samples
        return df
