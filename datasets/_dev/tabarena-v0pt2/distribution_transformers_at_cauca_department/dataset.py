"""Curated dataset definition for `distribution_transformers_at_cauca_department` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

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
"""The mounting labels version 4 left in Spanish (or misspelt), in the words of the Data in Brief (item L).

Used only to check that the two yearly files hold the same transformers: the 2020 file misspells one category.
"""

EENS_PER_KVA_HOUR = 1.08
"""energy_not_supplied_kwh = power_kva x 1.08 x outage hours (curation_comments, "Outage hours")."""


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
    # the files are aligned by row: every attribute column but the burning rate agrees, once the 2020 file's
    # misspelt mounting category (ANTI-FRAU) is corrected
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
    task_summary = TaskSummary(
        question="Which distribution transformers will burn out during the coming year?",
        use_case=(
            "At the start of 2020, the grid operator in Cauca, Colombia, ranks its transformers by the risk that they"
            " burn during the year, to plan maintenance and protection."
        ),
        row=(
            "One distribution transformer of the Cauca department (15,873 transformers), with the attributes of one "
            "inventory taken during or after 2020."
        ),
        predicted="Whether the transformer burned during 2020 (629 did, 4%).",
        known=(
            "Urban or rural, number and type of customers, the low-voltage network (length, overhead or not, end of "
            "circuit), the planned outage hours after a failure, the area's lightning density and criticality, and the "
            "failure history before 2020."
        ),
        split=("Random transformers of 2020; the 2019 file holds the same transformers and is not stacked."),
        changes=(
            "We drop a self-protection flag that marks units installed after a burn, and the rated power and mounting, "
            "which the inventory may show for a replacement unit; the energy not supplied is kept as outage hours."
        ),
        fit="approximate",
        fit_reason=(
            "With one year of labels the split is random rather than by time, and the training rows hold labels of "
            "the year being predicted. Whether the 2020 label covers the whole year is not stated."
        ),
    )

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

        - Prediction point: the start of 2020, when the operator ranks its transformers by the risk that they burn during the year. Both files carry one inventory, identical in both, taken during or after 2020: both workbooks were created on 2020-08-05 (a template date, so circumstantial). A transformer replaced in 2020 may show its replacement. Whether the 2020 label covers the whole year is not stated; a question for the authors.
        - One year, IID (tag ForcedIIDFromTemporal): the real use scores the known fleet one year ahead, which needs a temporal split, and two label years give one window, not three. The split follows SPLIT-8 as amended for a task with too few periods (Lennart, 2026-10-21). We keep one year rather than stacking two because the two files hold the same transformers with identical attributes, so stacking adds near-copies with a second label, and the 2019 rows are more affected by the later inventory (46% of their first burns self-protected, against 37%). The random split costs nothing measurable: LightGBM reaches ROC AUC 0.639 +- 0.012 on the 9 shipped folds and 0.648 trained on 2019 and tested on 2020; logistic regression is last under both splits, and random forest and LightGBM swap places within one standard deviation.
        - burn_rate is history: 5 x the 2020 rate - 4 x the 2019 rate equals each transformer's burns in 2019 (decision table), so the 2020 rate ends with 2019.
        - Dropped self_protected: in the data it marks a unit installed after a burn, set for 2.0% of the transformers that never burned in 2015-2020 and for 46% and 37% of those whose first burn was in 2019 and 2020 (decision table).
        - Dropped power_kva and installation_type (LEAK-10): they come from the same inventory, and the data shows the rating changed on replacement. Of the 163 self-protected first burns of 2020 none is 5 kVA and 68% are 10 kVA, against 9% and 31% of the 277 other first burns; self-protected units that never burned are 10% 5 kVA and 44% 10 kVA, so the units' make-up does not explain it (decision table). Revisit if the operator's replacement records or the inventory date become available.
        - Outage hours: energy_not_supplied_kwh is power_kva x 1.08 x hours, so it carries the rating. We keep only the hours (EENS / (1.08 x kVA), computed before power_kva is dropped), as outage_hours.
        - Anomaly, kept: removable_connectors and outage_hours mark the 2015-2018 failures (all units burned then have connectors; 15 h is the value for nearly all of them), history before the prediction point, and are not raised for the first burns of 2019 or 2020 (decision table).
        - Lightning: one area has both densities at 0.0 (487 rows). Zero flashes is not credible there: 65.7% of these rows are rated keraunic-critical, more than in any band of non-zero densities (decision table). We set both to missing. Their burn rate is 2.9% against 4.0% elsewhere, so the zeros do not carry the label. The article does not say which years the densities cover.
        - Network length: lv_network_km lost its decimal point for lengths of 1.1 km and more, stored as integers of 4 to 6 digits (lengths stored with a decimal point are at most 3.56 km). We divide such an integer by 10 to the power of its number of digits minus one; the authors' MATLAB table of 2019 agrees for all 479 six-digit integers we can match.
        - Anomaly: the source also dropped the zeros right after the decimal point (1.04202 km is stored as 14202) for 178 of the 1,754 rows we match. This blurs the column without carrying the label and cannot be undone row by row.
        - Anomaly, kept: 1,008 transformers have lv_network_km = 0, most of them with one user and an overhead network. The article says the data has no missing values and does not say what 0 means, so the zeros stay.
        - Columns are renamed to snake_case, and the label to burned (Yes / No).
        - Duplicates kept: 140 rows repeat an earlier row once power and mounting are dropped, 86% with one user and 96% with no low-voltage network: different transformers with identical coarse attributes.
        - The lightning densities (one value per area) are features, not groups, as a transformer's area is known. A same-year area effect, which the random split could reward, is absent: last year's burn rate of the area predicts the 2020 burns better than the same year's.
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
        # the energy not supplied is rated power x 1.08 x outage hours; keep the hours, which do not carry the power
        hours = df["energy_not_supplied_kwh"] / (EENS_PER_KVA_HOUR * df["power_kva"])
        df["energy_not_supplied_kwh"] = hours.round(3)
        df = df.rename(columns={"energy_not_supplied_kwh": "outage_hours"})
        # from the inventory taken during or after 2020: a replacement mark, and the replacement's size and mounting
        df = drop_columns(df, ["self_protected", "power_kva", "installation_type"])
        # one area has densities of 0.0 in both columns: a proxy for a missing value
        unknown = df["lightning_density_avg"].eq(0) & df["lightning_density_max"].eq(0)
        df.loc[unknown, ["lightning_density_avg", "lightning_density_max"]] = np.nan
        # lengths of 1.1 km and more lost their decimal point
        df["lv_network_km"] = lv_network_km(df["lv_network_km"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["client_type"])

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
        hours = static["Electric power not supplied EENS [kWh] "] / (EENS_PER_KVA_HOUR * static["POWER"])
        markers = pd.DataFrame(
            {
                "transformers": first_burn.value_counts(),
                "self-protected": static["SELF-PROTECTION"].groupby(first_burn).mean().round(3),
                "removable connectors": static["Removable connectors"].groupby(first_burn).mean().round(3),
                "outage hours = 15": hours.round(3).eq(15).groupby(first_burn).mean().round(3),
            }
        )
        rate_check = pd.crosstab(
            history["failures_2019"].rename("5 x rate 2020 - 4 x rate 2019"),
            history["burned_2019"].rename("burned in 2019"),
        )
        self_protected = static["SELF-PROTECTION"].map({1: "self-protected", 0: "not self-protected"})
        not_before = first_burn.isin(["first burn in 2020", "no burn in 2015-2020"])
        groups = (first_burn[not_before] + ", " + self_protected[not_before]).rename("failure record, protection")
        rating = pd.DataFrame(
            {
                "transformers": groups.value_counts(),
                "5 kVA": static["POWER"][not_before].eq(5).groupby(groups).mean().round(3),
                "10 kVA": static["POWER"][not_before].eq(10).groupby(groups).mean().round(3),
            }
        )
        density = static["Average earth discharge density DDT [Rays/km^2-año]"]
        zero = density.eq(0) & static["Maximum ground discharge density DDT [Rays/km^2-año]"].eq(0)
        band = pd.Series(
            np.where(zero, "0.0 in both", pd.qcut(density.where(~zero), 5).astype(str)), name="average density"
        )
        lightning = pd.DataFrame(
            {
                "transformers": band.value_counts(),
                "keraunic-critical": static["Criticality according to previous study for ceramics level"]
                .groupby(band)
                .mean()
                .round(3),
                "burned in 2020": static[f"Burned transformers {TASK_YEAR}"].groupby(band).mean().round(3),
            }
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
                "outage-hours markers belong to the 2015-2018 failure record (history) and are not raised for later "
                "burns.",
                markers,
            ),
            Decision(
                "power_kva and installation_type are dropped: the rating changed on replacement",
                "Among the first burns of 2020, the self-protected units (replacements) include no 5 kVA unit and "
                "mostly 10 kVA units, unlike the other first burns and unlike self-protected units that never burned. "
                "The inventory shows the replacement's rating, so the rating and the mounting are not known at the "
                "start of 2020.",
                rating,
            ),
            Decision(
                "Lightning densities of 0.0 are set to missing",
                "The one area with both densities at 0.0 is rated keraunic-critical more often than any band of "
                "non-zero densities, so 0.0 stands for an unknown value; its burn rate is not higher than elsewhere.",
                lightning,
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
