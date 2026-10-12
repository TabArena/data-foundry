"""Curated dataset definition for `biomechanical_orthopaedic_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class BiomechanicalOrthopaedicPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "biomechanical_orthopaedic_prediction"
    year = "2006"
    domain = "medical & healthcare"
    source = "Other"  # Appendix A of da Rocha Neto's 2006 master's thesis lists all 310 samples; UCI 212 is a copy
    source_url = "https://repositorio.ufc.br/bitstream/riufc/15977/1/2006_dis_arrochaneto.pdf"
    license = "CC BY 4.0"
    download_description = """
        We download UCI's copy (https://doi.org/10.24432/C5K89B) of the data the 2006 thesis lists.

        wget https://archive.ics.uci.edu/static/public/212/vertebral+column.zip && unzip vertebral+column.zip column_3C_weka.arff && rm vertebral+column.zip && mkdir -p local-data-warehouse/biomechanical_orthopaedic_prediction && mv column_3C_weka.arff local-data-warehouse/biomechanical_orthopaedic_prediction/
    """
    bibtex = """
        @inproceedings{da2011diagnostic,
          title={Diagnostic of pathology on the vertebral column with embedded reject option},
          author={da Rocha Neto, Ajalmar R and Sousa, Ricardo and de A. Barreto, Guilherme and Cardoso, Jaime S},
          booktitle={Iberian Conference on Pattern Recognition and Image Analysis},
          pages={588--595},
          year={2011},
          organization={Springer}
        }
    """
    curation_comments = """
        We start with UCI's copy (`column_3C_weka.arff`) of the 310 samples that Appendix A of da Rocha Neto's 2006
        master's thesis lists: 60 disc hernia, 150 spondylolisthesis and 100 normal, with six biomechanical features.
    """

    # Task
    target = "class"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # Read arff file
        with open(raw_dir / "column_3C_weka.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df
