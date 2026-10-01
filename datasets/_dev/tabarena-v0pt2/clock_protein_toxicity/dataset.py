"""Curated dataset definition for `clock_protein_toxicity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class ClockProteinToxicity(AbstractCuratedDataset):
    # Dataset
    unique_name = "clock_protein_toxicity"
    year = "2021"
    domain = "biology & life sciences"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C59313"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/clock_protein_toxicity && wget -P local-data-warehouse/clock_protein_toxicity/ https://archive.ics.uci.edu/static/public/728/toxicity-2.zip && unzip local-data-warehouse/clock_protein_toxicity/toxicity-2.zip -d local-data-warehouse/clock_protein_toxicity/ && rm local-data-warehouse/clock_protein_toxicity/toxicity-2.zip
    """
    bibtex = """
        @article{gul2021structure,
          title={Structure-based design and classifications of small molecules regulating the circadian rhythm period},
          author={Gul, Seref and Rahim, Fatih and Isin, Safak and Yilmaz, Fatma and Ozturk, Nuri and Turkay, Metin and Kavakli, Ibrahim Halil},
          journal={Scientific reports},
          volume={11},
          number={1},
          pages={18510},
          year={2021},
          publisher={Nature Publishing Group UK London}
        }
    """
    curation_comments = """
        - We remove duplicated columns (same values for all rows).
    """

    # Task
    target = "Toxic"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "data.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "Toxic"
        df = df.rename(columns={"Class": target_feature})
        df[target_feature] = df[target_feature].astype("category")
        # drop duplicated
        duplicate_columns = [
            "nT10Ring",
            "nssS",
            "nssCH2",
            "khs.dsCH",
            "nHdsCH",
            "minHdNH",
            "SHdNH",
            "EE_DzZ",
            "SsBr",
            "maxsBr",
            "nF12HeteroRing",
            "n7Ring",
            "n7HeteroRing",
            "nT7Ring",
            "khs.sF",
            "nsF",
            "nF8HeteroRing",
            "nT8Ring",
            "nT8HeteroRing",
            "ndO",
            "nsCH3",
            "nHssNH",
            "nssNH",
            "nBr",
            "khs.sBr",
            "maxsCl",
            "khs.aaCH",
            "naaCH",
            "maxssssNp",
            "SaaS",
            "khs.sOH",
            "nsOH",
            "nT11HeteroRing",
            "maxdS",
            "mindS",
            "maxsNH2",
            "nssssC",
            "nT5Ring",
            "nT12Ring",
            "SpMax_Dzi",
            "khs.sNH2",
            "nsNH2",
            "SpMax_Dze",
            "minaaNH",
            "SpMax_Dzv",
            "nTG12HeteroRing",
            "nsOm",
            "minHsNH2",
            "minHtCH",
            "ntsC",
            "nBondsT",
            "khs.tsC",
            "nT5HeteroRing",
            "maxHaaNH",
            "ndNH",
            "nHdNH",
            "SdNH",
            "mindNH",
            "SpMax_Dzp",
            "EE_D",
            "naaS",
            "nsssN",
            "maxdCH2",
            "SdCH2",
            "naaNH",
            "khs.tN",
            "nssO",
            "maxtCH",
            "khs.dsN",
            "SHdCH2",
            "maxHdCH2",
            "SpMax_Dzs",
            "n6HeteroRing",
            "nF9Ring",
            "nT11Ring",
            "nT10HeteroRing",
            "nssssNp",
            "SpMax_Dzm",
            "SssS",
            "naaO",
            "khs.ddssS",
            "khs.sCl",
            "nsCl",
            "nsssCH",
            "nT9HeteroRing",
            "nFG12Ring",
        ]
        df = df.drop(columns=duplicate_columns)
        return df
