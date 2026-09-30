"""Curated dataset definition for `biogeographical_ancestry_prediction` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class BiogeographicalAncestryPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "biogeographical_ancestry_prediction"
    year = "2025"  # source data is older, but this version was created in 2025
    domain = "biology & life sciences"
    source = "GitHub"
    source_url = """
        https://github.com/CarolaHeinzel/BGA_Classification/blob/main/data/input_data/full_data.csv
    """
    license = "None"  # Data from GitHub does not have a license, source is Apache-2.0 license (I think)
    download_description = """
        We download the data from the GitHub repository and save it to a predefined folder.

        mkdir -p local-data-warehouse/biogeographical_ancestry_prediction/ && curl -L -o local-data-warehouse/biogeographical_ancestry_prediction/filter_population.xlsx https://raw.githubusercontent.com/CarolaHeinzel/BGA-Classification/main/datat/filtered_population_eur_update.xlsx
    """
    bibtex = r"""
        @article{heinzel2025advancing,
          title={Advancing biogeographical ancestry predictions through machine learning},
          author={Heinzel, Carola Sophia and Purucker, Lennart and Hutter, Frank and Pfaffelhuber, Peter},
          journal={Forensic Science International: Genetics},
          volume={79},
          pages={103290},
          year={2025},
          publisher={Elsevier}
        }
        @article{ruiz2023development,
          title={Development and evaluations of the ancestry informative markers of the VISAGE Enhanced Tool for Appearance and Ancestry},
          author={Ruiz-Ram{\'\i}rez, Jorge and de La Puente, M and Xavier, Catarina and Ambroa-Conde, Adri{\'a}n and {\'A}lvarez-Dios, J and Freire-Aradas, A and Mosquera-Miguel, Ana and Ralf, Arwin and Amory, Christina and Katsara, Maria Alexandra and others},
          journal={Forensic Science International: Genetics},
          volume={64},
          pages={102853},
          year={2023},
          publisher={Elsevier}
        }
        @article{xavier2020development,
          title={Development and validation of the VISAGE AmpliSeq basic tool to predict appearance and ancestry from DNA},
          author={Xavier, Catarina and de la Puente, Maria and Mosquera-Miguel, Ana and Freire-Aradas, Ana and Kalamara, Vivian and Vidaki, Athina and Gross, Theresa E and Revoir, Andrew and Po{\'s}piech, Ewelina and Kartasi{\'n}ska, Ewa and others},
          journal={Forensic Science International: Genetics},
          volume={48},
          pages={102336},
          year={2020},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        We use this dataset as one of the most recent example of a machine learning task based on the Human Genome project.
        We take the targets from the paper by Heinzel et al. (2025) and only rename the targets to be standardized and more concise.
    """

    # Task
    target = "Population"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(f"{raw_dir}/filter_population.xlsx")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(
            columns=[
                "Unnamed: 1",
                "SNP-Indel with complex genotype listing in VCF (not compiled)",
                "Unnamed: 3",
                "Unnamed: 4",
                "ID",
            ],
        )
        column_map = {
            "Iberian population in Spain": "Spain (Iberian)",
            "Toscani in Italia": "Italy (Toscani)",
            "Finnish in Finland": "Finland (Finnish)",
            "Utah Residents (CEPH) with N & W European ancestry": "Utah (CEPH, N/W European ancestry)",
            "British in England and Scotland": "UK (England & Scotland, British)",
            "13. Italy - Sardinian": "Italy (Sardinian)",
            "11. France - French": "France (French)",
            "Turkey": "Turkey",
            "09. Russia - Russian": "Russia (Russian)",
            "10. France - French Basque": "France (Basque)",
        }
        df["Population"] = df["Population"].map(column_map)
        for col in df.columns:
            df[col] = df[col].astype("category")
        return df
