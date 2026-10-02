"""Curated dataset definition for `labour_inspection_compliance` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class LabourInspectionCompliance(AbstractCuratedDataset):
    # Dataset
    unique_name = "labour_inspection_compliance"
    year = "2019"
    domain = "industry & manufacturing"
    source = "Other"
    source_url = "https://doi.org/10.18710/7U6TZP"
    license = "CC0 1.0"
    data_tags = ("Spatial", "ForcedIIDFromTemporal")
    download_description = """
        Get the data from dataverse.

        wget https://dataverse.no/api/access/datafile/:persistentId?persistentId=doi:10.18710/7U6TZP/HAV8AG &&  mv  ':persistentId?persistentId=doi:10.18710%2F7U6TZP%2FHAV8AG' data.csv
        mkdir -p local-data-warehouse/labour_inspection_compliance && mv data.csv local-data-warehouse/labour_inspection_compliance
    """
    bibtex = """
        @inproceedings{flogard2022dataset,
          title={A dataset for efforts towards achieving the sustainable development goal of safe working environments},
          author={Flogard, Eirik Lund and Mengshoel, Ole Jakob},
          booktitle={Thirty-sixth Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
          year={2022}
        }
    """
    curation_comments = """
        We start with the data from dataverse. We create a task for the Non-compliance Classification Problem (NCP).

        - We resolve the industry codes to their true names.
        - We drop the checklist ID, as we use the checklist text as predictive signal.
        - We remove two rows with missing values for IsRegisteredVATregister, as these seem to be data artifact given the data state.
        - The data has spatial information (County).
        - There are lot of undescribed numeric values. Thus, we do some general purpose preprocessing and drop all columns with less than 5 not nan values
        - As it turns out, the data does not contain temporal information, although it is clearly a temporal task and has data from 2021 to 2019. It seems the curators have removed the temporal information. This can mean that there is not temporal leakage or relevance for the task, or that it was forgotten. In any case, we must treat the task as IID now.
    """

    # Task
    target = "NonCompliance"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "data.csv", sep=";")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Resolve industry codes
        code_resolution = pd.read_csv(self.folder / "klass-version-30-codes.csv", sep=";")
        code_as_number = pd.to_numeric(code_resolution["code"], errors="coerce")
        int_codes_mask = code_as_number.notna() & (code_as_number % 1 == 0)
        code_resolution = code_resolution[int_codes_mask].copy()
        code_resolution["code"] = code_as_number[int_codes_mask].astype(int)
        code_resolution = code_resolution.set_index(["code", "parentCode"])["name"].to_dict()
        df["Industry Sub Area"] = df.apply(
            lambda row: code_resolution[(row["Industry Code"], row["Industry Main Area Code"])],  # noqa: F821 - runs before the `del` below
            axis=1,
        )
        del code_resolution
        sector_map = {
            "A": "Agriculture, forestry and fishing",
            "B": "Mining and quarrying",
            "C": "Manufacturing",
            "D": "Electricity, gas, steam and air conditioning supply",
            "E": "Water supply; sewerage, waste management and remediation activities",
            "F": "Construction",
            "G": "Wholesale and retail trade; repair of motor vehicles and motorcycles",
            "H": "Transportation and storage",
            "I": "Accommodation and food service activities",
            "J": "Information and communication",
            "K": "Financial and insurance activities",
            "L": "Real estate activities",
            "M": "Professional, scientific and technical activities",
            "N": "Administrative and support service activities",
            "O": "Public administration and defence; compulsory social security",
            "P": "Education",
            "Q": "Human health and social work activities",
            "R": "Arts, entertainment and recreation",
            "S": "Other service activities",
            "T": "Activities of household as employers; undifferentiated goods- and services-producing activities of households for own account",
            "U": "Activities of extraterritorial organisations and bodies",
        }
        df["Industry Main Area"] = df["Industry Main Area Code"].map(sector_map)
        df = df[df["IsRegisteredVATregister"].notna()]
        set(df.columns)
        df = df.dropna(axis=1, thresh=5)
        df = df.drop(
            columns=[
                "Checklist ID",
                "Industry Main Area Code",
            ]
        )
        # Drop duplicated columns
        df = df.loc[:, ~df.T.duplicated()]
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Industry Code",
                "IsRegisteredVATregister",
                "IsRegisteredEmploymentregister",
                "Currency code",
                "Fiscal accounting type",
            ],
            string=[
                "Checklist Content",
                "Industry Main Area",
                "Industry Sub Area",
                "County",
            ],
        )
