"""Curated dataset definition for `labour_inspection_compliance` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class LabourInspectionCompliance(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will an inspection find an organisation in breach of the working-environment rules on a given checklist?"
        ),
        use_case=(
            "For example, the Norwegian labour inspection authority decides which organisations to inspect, and with "
            "which checklist, by predicting where an inspection would find a breach (the source's non-compliance "
            "task)."
        ),
        row=(
            "One inspection of a Norwegian organisation with one checklist, January 2012 to June 2019 (63,634 rows); "
            "the data has no dates."
        ),
        predicted=(
            "Whether the organisation was found non-compliant with any regulation the checklist covers, which is "
            "known only when the inspection is completed."
        ),
        known=(
            "The organisation's industry, county, age and number of employees, whether it is in the VAT and employer "
            "registers, its accounting type and currency, the checklist's text, and several hundred figures, many "
            "from its accounts, that the source does not describe one by one."
        ),
        split="Random inspections, so training and test inspections come from the same period.",
        fit="approximate",
        fit_reason=(
            "Inspections are targeted ahead of time, but the data has no dates, so the split cannot keep later "
            "inspections for testing; the meaning of most numbers is not stated."
        ),
    )

    # Dataset
    unique_name = "labour_inspection_compliance"
    year = "2022"
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
        - The data has no dates, although the task is temporal and the inspections span January 2012 to June 2019 (per the Dataverse description). Without the inspection dates, we must treat the task as IID.
        - Metric: precision at the median score (k = 50% of the test fold), which the paper calls the most important statistic; the same section calls accuracy or AUC also important, and the median cut is the paper's choice, not a stated inspection capacity (curator call, Lennart 2026-10-21).
    """

    # Task
    target = "NonCompliance"
    problem_type = "binary_classification"
    metric = Metric.source(
        "precision_at_k",
        original="precision at the median prediction score (with balanced accuracy, accuracy, recall and AUC)",
        reference="Flogard & Mengshoel 2022, NeurIPS Datasets and Benchmarks, Sec. 6.4-6.5",
        definition=(
            "share of non-compliant inspections among the half of the test fold with the highest scores "
            "(threshold at the median score)"
        ),
        params={"k_fraction": 0.5},
    )

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
