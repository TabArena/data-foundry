"""Curated dataset definition for `distribution_transformers_at_cauca_department` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, drop_columns

YEARS = (2019, 2020)
"""One file per year: the same 15,873 transformers in the same row order, labelled with that year's burns."""

TASK_YEAR = "2020"
"""The year we ship (curation_comments, "One year")."""

COLUMNS = {
    "LOCATION": "urban",
    "POWER": "power_kva",
    "SELF-PROTECTION": "self_protected",
    "Average earth discharge density DDT [Rays/km^2-año]": "lightning_density_avg",
    "Maximum ground discharge density DDT [Rays/km^2-año]": "lightning_density_max",
    "Burning rate  [Failures/year]": "burn_rate",
    "Criticality according to previous study for ceramics level": "keraunic_criticality",
    "Removable connectors": "removable_connectors",
    "Type of clients": "client_type",
    "Number of users": "n_users",
    "Electric power not supplied EENS [kWh] ": "energy_not_supplied_kwh",
    "Type of installation": "installation_type",
    "Air network": "overhead_lv_network",
    "Circuit Queue": "circuit_end",
    "km of network LT:": "lv_network_km",
}
"""The source's columns in file order (Data in Brief, Sec. 1, items A-O) and our names; the 16th is the label."""

INSTALLATION_TYPES = {
    "POLE WITH ANTI-FRAU NET": "POLE WITH ANTI-FRAUD NET",  # a typo of the 2020 file only
    "EN H": "H STRUCTURE",
    "OTROS": "OTHER",
    "TORRE METALICA": "METAL TOWER",
    "CABINA": "CABIN",
}
"""The labels version 4 left in Spanish (or misspelt), in the words of the Data in Brief description (item L)."""


def lv_network_km(km: pd.Series) -> pd.Series:
    """Restore the decimal point the source lost for low-voltage networks of 1.1 km and more.

    Those lengths are stored as integers of 4 to 6 digits (1103 to 717125, Excel format ``#,##0``), while every
    length stored with its decimal point is at most 3.56 km. The integer is the length's digits, so the length is the
    integer divided by 10 to the power of its number of digits minus one (curation_comments, "Network length").
    """
    lost = km >= 1_000
    if km[lost].mod(1).any() or km.max() >= 1_000_000:
        msg = "lv_network_km: a stored length is not an integer of 4 to 6 digits; check the repair."
        raise ValueError(msg)
    divisor = np.select([km >= 1e5, km >= 1e4, km >= 1e3], [1e5, 1e4, 1e3], default=1.0)
    return km / divisor


def failure_history(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Per transformer (row): failures 2015-2018 (the 2019 file's rate x 4), in 2019 and the two labels."""
    # the files are aligned by row: every attribute column but the burning rate agrees (one label typo aside)
    attributes = [c for c in COLUMNS if c != "Burning rate  [Failures/year]"]
    aligned = [raw[str(year)][attributes].replace(INSTALLATION_TYPES) for year in YEARS]
    if not aligned[0].equals(aligned[1]):
        msg = "the 2019 and 2020 files no longer hold the same transformers row by row"
        raise ValueError(msg)
    rate = {year: raw[str(year)]["Burning rate  [Failures/year]"] for year in YEARS}
    before_2019 = (rate[2019] * 4).round().astype("int64")
    in_2019 = (rate[2020] * 5).round().astype("int64") - before_2019
    return pd.DataFrame(
        {
            "failures_2015_2018": before_2019,
            "failures_2019": in_2019,
            "burned_2019": raw["2019"]["Burned transformers 2019"],
            "burned_2020": raw["2020"]["Burned transformers 2020"],
        }
    )


class DistributionTransformersAtCaucaDepartment(AbstractCuratedDataset):
    # Dataset
    unique_name = "distribution_transformers_at_cauca_department"
    year = "2021"
    domain = "industry & manufacturing"
    source = "Other"  # Mendeley Data (doi:10.17632/yzyj46xpmy.4) with its Data in Brief article
    source_url = "https://doi.org/10.17632/yzyj46xpmy.4"
    license = "CC BY 4.0"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We download the two yearly files of version 4 of the Mendeley Data release (doi:10.17632/yzyj46xpmy.4) by
        their file ids, which the public API lists with their SHA-256 hashes
        (https://data.mendeley.com/public-api/datasets/yzyj46xpmy/files?folder_id=root&version=4).

        mkdir -p local-data-warehouse/distribution_transformers_at_cauca_department && cd local-data-warehouse/distribution_transformers_at_cauca_department
        curl -L -o Dataset_Year_2019.xlsx https://data.mendeley.com/public-files/datasets/yzyj46xpmy/files/0f334045-f033-44ff-b896-dd6b72ed4198/file_downloaded
        curl -L -o Dataset_Year_2020.xlsx https://data.mendeley.com/public-files/datasets/yzyj46xpmy/files/9798091b-3770-40ab-93b3-4c72a34c3d28/file_downloaded
        sha256sum Dataset_Year_2019.xlsx Dataset_Year_2020.xlsx
        # e7dd9283eb0870ef29fff83c4573373941dfd24b2842a665263ae2ea02c27d77  Dataset_Year_2019.xlsx
        # 22e0d23fd5d2efd4888737edf0657f9fb0044a89e8d66e91f0cda16682de93ca  Dataset_Year_2020.xlsx
    """
    bibtex = r"""
        @article{bravo2021dataset,
          title = {Dataset of distribution transformers for predictive maintenance},
          author = {Bravo M., Diego-A. and Alvarez Q., Laura-I. and Lozano M., Carlos-A.},
          journal = {Data in Brief},
          volume = {38},
          pages = {107454},
          year = {2021},
          doi = {10.1016/j.dib.2021.107454}
        }
        @misc{bravo2021mendeley,
          title = {Dataset of Distribution Transformers at Cauca Department (Colombia)},
          author = {Bravo M., Diego A. and Lozano, Carlos and Alvarez, Laura},
          howpublished = {Mendeley Data, version 4},
          year = {2021},
          doi = {10.17632/yzyj46xpmy.4}
        }
    """
    curation_comments = """
        We start with Dataset_Year_2020.xlsx of version 4 of the Mendeley Data release by Bravo, Lozano and Alvarez (2021, Data in Brief). Dataset_Year_2019.xlsx, the same transformers labelled with the 2019 burns, is read only for the decision tables.

        - Prediction point: the start of 2020, when the operator ranks its transformers by the risk that they burn during the year. Both files carry one inventory taken after the 2020 burns, so a transformer replaced in 2020 shows its replacement.
        - One year, IID (tag ForcedIIDFromTemporal): the two files hold the same transformers, so stacking them would hold each twice, and two years cannot make three temporal windows. 2020 has the longer failure history and is less affected by the late inventory. The random split costs little: LightGBM reaches ROC AUC 0.699 within 2020 and 0.687 trained on 2019 and tested on 2020.
        - burn_rate is history: 5 x the 2020 rate - 4 x the 2019 rate equals each transformer's burns in 2019 (decision table), so the 2020 rate ends with 2019.
        - Dropped self_protected: in the data it marks a unit installed after a burn, set for 2.0% of the transformers that never burned in 2015-2020 and for 46% and 37% of those whose first burn was in 2019 and 2020 (decision table).
        - Potential leak, kept on purpose: power_kva and installation_type come from the same inventory and may show a replacement's size and mounting; power_kva raises the ROC AUC by 0.107 for the self-protected positives and by 0.023 for the others. Both stay, as kVA follows the number of users alike in every failure group and small rural units burning more is the expected risk pattern. Revisit if the operator's replacement records become available.
        - Anomaly, kept: removable_connectors and energy_not_supplied_kwh mark the 2015-2018 failures, history before the prediction point, and are not raised for the first burns of 2019 or 2020 (decision table).
        - Network length: lv_network_km lost its decimal point for lengths of 1.1 km and more, stored as integers of 4 to 6 digits (lengths stored with a decimal point are at most 3.56 km). We divide such an integer by 10 to the power of its number of digits minus one; the authors' MATLAB table of 2019 agrees for all 479 six-digit integers we can match.
        - Anomaly: the source also dropped the zeros right after the decimal point (1.04202 km is stored as 14202) for 178 of the 1,754 rows we match. This blurs the column without carrying the label and cannot be undone row by row.
        - installation_type: the Spanish labels are translated as in the Data in Brief (Sec. 1, item L) and a typo is fixed. Columns are renamed to snake_case, and the label to burned (Yes / No).
        - Duplicates kept: 80 rows repeat an earlier row, nearly all with one user and no low-voltage network: different transformers with identical coarse attributes.
        - The lightning densities (one value per area) are features, not groups, as a transformer's area is known.
    """

    # Task (the metric defaults to roc_auc; stratified on the target)
    target = "burned"
    problem_type = "binary_classification"
    accepted_check_warnings = {
        "dataset_pure_feature_value": (
            "client_type = STRATUM 3 (1 of 427 burned in 2020, 2 in 2019) is a category effect on a 96% base rate: "
            "90% of these transformers are urban, and urban transformers burn at 1.0% against 4.6% for rural ones. "
            "The client type is an inventory attribute, not a value recorded after the burn."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {str(year): pd.read_excel(raw_dir / f"Dataset_Year_{year}.xlsx", sheet_name="Datos") for year in YEARS}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw[TASK_YEAR]
        label = f"Burned transformers {TASK_YEAR}"
        if list(df.columns) != [*COLUMNS, label]:
            msg = f"unexpected columns in Dataset_Year_{TASK_YEAR}.xlsx: {list(df.columns)}"
            raise ValueError(msg)
        # snake_case names in the source's order; the label "burned during 2020" as Yes / No
        df = df.rename(columns={**COLUMNS, label: self.target})
        df[self.target] = df[self.target].map({1: "Yes", 0: "No"})
        # in the data a mark of units installed after a burn; the inventory postdates the 2020 burns
        df = drop_columns(df, ["self_protected"])
        # Spanish labels and a typo of version 4 in English
        df["installation_type"] = df["installation_type"].replace(INSTALLATION_TYPES)
        # lengths of 1.1 km and more lost their decimal point
        df["lv_network_km"] = lv_network_km(df["lv_network_km"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["client_type", "installation_type"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        history = failure_history(raw)
        static = raw[TASK_YEAR]
        first_burn = pd.Series(
            np.select(
                [
                    history["failures_2015_2018"] > 0,
                    history["burned_2019"] == 1,
                    history["burned_2020"] == 1,
                ],
                ["burned in 2015-2018", "first burn in 2019", "first burn in 2020"],
                default="no burn in 2015-2020",
            ),
            name="failure record",
        )
        factor_16_2 = (static["Electric power not supplied EENS [kWh] "] / static["POWER"]).round(4).eq(16.2)
        markers = pd.DataFrame(
            {
                "transformers": first_burn.value_counts(),
                "self-protected": static["SELF-PROTECTION"].groupby(first_burn).mean().round(3),
                "removable connectors": static["Removable connectors"].groupby(first_burn).mean().round(3),
                "EENS = 16.2 x power": factor_16_2.groupby(first_burn).mean().round(3),
            }
        )
        rate_check = pd.crosstab(
            history["failures_2019"].rename("5 x rate 2020 - 4 x rate 2019"),
            history["burned_2019"].rename("burned in 2019"),
        )
        stored = raw[TASK_YEAR]["km of network LT:"]
        repaired = lv_network_km(stored)  # in raw row order; `df` is already in its final order
        kind = pd.Series(
            np.select(
                [stored == 0, stored < 1_000, stored < 1e4, stored < 1e5],
                ["0", "with a decimal point", "integer of 4 digits", "integer of 5 digits"],
                default="integer of 6 digits",
            ),
            name="stored as",
        )
        lengths = pd.DataFrame(
            {
                "rows": kind.value_counts(),
                "stored min": stored.groupby(kind).min(),
                "stored max": stored.groupby(kind).max(),
                "repaired min (km)": repaired.groupby(kind).min().round(5),
                "repaired max (km)": repaired.groupby(kind).max().round(5),
            }
        )
        return [
            Decision(
                "self_protected is dropped: in the data it marks units installed after a burn",
                "The share of self-protected transformers is highest among those whose first burn falls in the "
                "labelled years, which fits an inventory taken after burned units were replaced. The connector and "
                "EENS markers belong to the 2015-2018 failure record (history) and are not raised for later burns.",
                markers,
            ),
            Decision(
                "burn_rate counts the failures before the labelled year",
                "The 2020 rate times five minus the 2019 rate times four is exactly the number of burns in 2019, "
                "so the 2020 file's rate ends with 2019 and holds no burn of 2020.",
                rate_check,
            ),
            Decision(
                "Network lengths of 1.1 km and more get their decimal point back",
                "Lengths stored as integers are the digits of a length with one digit before the decimal point; "
                "we divide them by 10 to the power of their number of digits minus one.",
                lengths,
            ),
        ]
