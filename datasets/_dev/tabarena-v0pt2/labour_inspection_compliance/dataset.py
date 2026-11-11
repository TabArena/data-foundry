"""Curated dataset definition for `labour_inspection_compliance` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
)


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
            "registers, its accounting type and currency, the checklist's text, the organisation's accounts (one "
            "set, year not stated), several hundred figures that the source does not describe one by one, and the "
            "inspection's place in the export's order."
        ),
        split=(
            "Three windows of the export's row order, which follows time coarsely; each tests later inspections on "
            "earlier ones."
        ),
        fit="approximate",
        fit_reason=(
            "Inspections are targeted ahead of time and the split keeps later inspections for testing, but the data "
            "has no dates and its row order resolves time only to about 14 months; the accounts are of an unknown "
            "year; the meaning of most numbers is not stated."
        ),
    )

    # Dataset
    unique_name = "labour_inspection_compliance"
    domain = "industry & manufacturing"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.18710/7U6TZP",
            license="CC0 1.0",
            year="2022",
            bibtex="""
                @inproceedings{flogard2022dataset,
                  title={A dataset for efforts towards achieving the sustainable development goal of safe working environments},
                  author={Flogard, Eirik Lund and Mengshoel, Ole Jakob},
                  booktitle={Thirty-sixth Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
                  year={2022}
                }
            """,
        ),
    )
    data_tags = ("Spatial",)
    download_description = """
        Get the data from dataverse.

        wget https://dataverse.no/api/access/datafile/:persistentId?persistentId=doi:10.18710/7U6TZP/HAV8AG &&  mv  ':persistentId?persistentId=doi:10.18710%2F7U6TZP%2FHAV8AG' data.csv
        mkdir -p local-data-warehouse/labour_inspection_compliance && mv data.csv local-data-warehouse/labour_inspection_compliance
    """
    curation_comments = """
        We start with the data from dataverse. We create a task for the Non-compliance Classification Problem (NCP).

        - We resolve the industry codes to their true names.
        - We drop the checklist ID, as we use the checklist text as predictive signal.
        - We remove two rows with missing values for IsRegisteredVATregister, as these seem to be data artifact given the data state.
        - The data has spatial information (County).
        - There are lot of undescribed numeric values. Thus, we do some general purpose preprocessing and drop all columns with less than 5 not nan values
        - Time order: the data has no dates (the inspections span January 2012 to June 2019, per the Dataverse
          description), but the raw file is in a coarse time order: among rows of one organisation (identical
          register and account fields), the later row has the higher business age in 92% of pairs more than 40,000
          rows apart; 67 of the 228 checklists used 30 times or more stop before the last four tenths of the file and
          50 first appear after its first three tenths. We keep the raw row number as `file_row` and split by it
          (2026-11-11, Andrej, review issue 2 b).
        - Account figures: one set per organisation, attached to all its inspections (8,888 organisations inspected
          at two or more business ages carry identical figures, 33,168 rows; first and last inspection a median 35
          months apart); the paper says the register keeps no history and gives no fiscal year; the payroll matches
          the employee count of the first inspection as well as of the last (Spearman 0.67 and 0.65). Kept: they add
          0.004 precision at half (untuned LightGBM, random folds), no more where they must come from another year
          (0.003) than for organisations seen once (0.004) (2026-11-11, Andrej, review issue 3 B).
        - Repeats kept: 497 rows (0.8%) equal another row in every column, the outcome included, and 179 rows (0.3%)
          equal another row in every feature with the other outcome. The release has no date or case number to tell a
          re-inspection from a double entry; a copy lies a median 61 rows from its original, so under the windows of
          file order only 3 to 11 test rows per window find their copy in training (0.03% to 0.10%). Each copy counts
          twice in training and, inside a test window, twice in the score; the copies found a breach in 57.7%
          (287 of 497) against 74.3% of all rows, so the double count tilts the class balance slightly (dropped, the
          breach share would move from 74.28% to 74.41%) (2026-11-11, Andrej, review issue 1 A).
        - Metric: precision at the median score (k = 50% of the test fold), which the paper calls the most important statistic; the same section calls accuracy or AUC also important, and the median cut is the paper's choice, not a stated inspection capacity (curator call, Lennart 2026-10-21).
        - The target (2026-11-01, CLEAN-25): `NonCompliance` ships its classes as words (1 is the event). Binary: "Yes"
          is the event, the class that sorts second, so it is the metrics' positive class.
    """

    accepted_check_warnings = {
        "dataset_sequential_id_column": "`file_row` is the export's row order, the dataset's declared time column "
        "(review issue 2 b); it is the only time the release keeps and cannot be dropped.",
    }

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

    # Splits
    splits_comment = """
        Three test windows of 10,605 inspections (a sixth of the rows) in the raw file's order, walking back from the
        newest; each trains on all earlier rows (50%, 67% and 83%), so no window trains on less than half of the data
        (SPLIT-14). The order is the export's and coarse: it resolves time only to about 10,000 rows (some 14 months
        of the 7.5 years), so the windows are a sixth of the rows each, wider than that resolution, and a test window
        is later on average, not row by row. The windows follow the file's own order: the checklists of one visit lie
        a median 1,211 rows apart, so a window's start cuts some visits (0.3% to 1.0% of test rows have another row of
        their visit in training, against 4.0% on random folds). An inspection's result is known when it ends, so there
        is no gap (2026-11-11, Andrej, review issue 2 b).
    """
    temporal = Temporal(
        on="file_row",
        splits=TemporalSplits(window=10605, unit="rows", n_windows=3, min_train_fraction=0.5),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "data.csv", sep=";")
        # the export's row order, a coarse time order (see the curation notes); kept before any row is dropped
        df["file_row"] = range(len(df))
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
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
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
