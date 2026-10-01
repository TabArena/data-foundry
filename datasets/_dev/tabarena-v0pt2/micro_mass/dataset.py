"""Curated dataset definition for `micro_mass` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class MicroMass(AbstractCuratedDataset):
    # Dataset
    unique_name = "micro_mass"
    year = "2013"
    domain = "biology & life sciences"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5T61S"
    license = "CC BY 4.0"
    download_description = """
        wget https://archive.ics.uci.edu/static/public/253/micromass.zip && unzip micromass.zip micromass_un_anonymized.zip && rm micromass.zip && mkdir -p local-data-warehouse/micro_mass && unzip micromass_un_anonymized.zip -d local-data-warehouse/micro_mass/ && rm micromass_un_anonymized.zip
    """
    bibtex = r"""
        @article{mahe2014automatic,
          title={Automatic identification of mixed bacterial species fingerprints in a MALDI-TOF mass-spectrum},
          author={Mahe, Pierre and Arsac, Maud and Chatellier, Sonia and Monnin, Val{\'e}rie and Perrot, Nadine and Mailler, Sandrine and Girard, Victoria and Ramjeet, Mahendrasingh and Surre, J{\'e}r{\'e}my and Lacroix, Bruno and others},
          journal={Bioinformatics},
          volume={30},
          number={9},
          pages={1280--1286},
          year={2014},
          publisher={Oxford University Press}
        }
    """
    curation_comments = """
        We use the pure spectra version (without mixing) and replicate a grouped-based task to predict the species of strains.

        - We drop columns with the same value across all samples.
        - We drop constant columns (all 0).
    """

    # Task
    target = "Species"
    problem_type = "multiclass_classification"
    group_on = "Strain"
    group_labels = "per_group"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(
            raw_dir / "micromass" / "pure_spectra_matrix.csv",
            header=None,
            names=[f"peak_list_spectra_bin_{i}" for i in range(1, 1301)],
            sep=";",
        )
        metadata = pd.read_csv(raw_dir / "micromass" / "pure_spectra_metadata_with-species-name.csv", sep=";")
        return {"df": df, "metadata": metadata}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, metadata = raw["df"], raw["metadata"]
        df = pd.concat([metadata, df], axis=1)
        # cast before the sort below, which orders by category
        df["Strain"] = df["Strain"].astype("category")
        # Drop duplicate columns based on values
        df = df.loc[:, ~df.T.duplicated()]
        # DRop constant columns
        df = df.loc[:, (df != df.iloc[0]).any()]
        df = df.sample(frac=1, random_state=42).sort_values(by="Strain").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["Strain"])


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
