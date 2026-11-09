"""Curated dataset definition for `acs_food_stamps_2014_2024_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import csv
import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

# The regular ACS 1-year PUMS files we read. 2020 has no regular file: the Census Bureau released the 2020 1-year data
# only as experimental estimates with experimental weights (pandemic collection), so the year is left out.
YEARS = (2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024)
PREPARED_FILE = "acs_households_2014_2024.parquet"

# Items read from the housing file (one record per housing unit) and the person file (one record per person), as
# named in the 2024 data dictionary; older files name the state ST (until 2022) and the unit type TYPE (until 2019),
# and mark the householder by RELP 0 (until 2018) instead of RELSHIPP 20. The survey weights (WGTP, PWGTP and their 80
# replicates), the allocation flags other than FFSP, PUMA, REGION and DIVISION are never read.
HOUSING_ITEMS = (
    "SERIALNO", "STATE", "TYPEHUGQ", "NP", "FS", "FFSP", "ADJINC", "ADJHSG", "HINCP", "GRNTP", "SMOCP", "TEN", "BLD",
    "VEH", "HHL", "HHT", "HUPAC", "NOC", "NRC", "R60", "R65", "MULTG", "LNGI", "WIF", "WKEXREL",
)  # fmt: skip
PERSON_ITEMS = (
    "SERIALNO", "AGEP", "SEX", "RAC1P", "HISP", "SCHL", "MAR", "CIT", "NATIVITY", "POBP", "ANC", "ENG", "DIS", "DEAR",
    "DEYE", "DREM", "ESR", "WKHP", "COW", "OCCP", "MIL", "PUBCOV", "POVPIP", "FER",
)  # fmt: skip
OLD_NAMES = {"ST": "STATE", "TYPE": "TYPEHUGQ"}

# Codes whose meaning is the same in every year: decoded with the words of the 2024 data dictionary (older
# dictionaries word a few levels differently, e.g. HHT "no wife present", CIT "Born in the U.S.").
STABLE_CODED = (
    "STATE", "TEN", "BLD", "VEH", "HHL", "HHT", "HUPAC", "R60", "R65", "MULTG", "LNGI", "WIF", "WKEXREL", "SEX",
    "RAC1P", "HISP", "SCHL", "MAR", "CIT", "NATIVITY", "ANC", "ENG", "DIS", "DEAR", "DEYE", "DREM", "ESR", "COW", "MIL",
    "PUBCOV", "FER",
)  # fmt: skip
# Codes whose list changed over the years: decoded with each year's own dictionary (2017's for 2014-2016, whose
# dictionaries are only published as text files), then written in the 2024 wording where the words agree up to case.
# OCCP follows the 2010 Census occupation codes until 2017 and the 2018 codes from 2018.
YEARLY_CODED = ("POBP", "OCCP")
# POBP codes of the 2014-2016 dictionaries (PUMSDataDict14.txt to PUMSDataDict16.txt) that the 2017 dictionary drops
# (208) or gives to another country (463, South Sudan from 2017).
POBP_2014_2016 = {208: "Cyprus", 463: "Eastern Africa, Not Specified"}
# A blank ENG means "less than 5 years old/speaks only English"; every householder is 15 or older, so it is the top
# of the scale.
ENG_ONLY_ENGLISH = "Speaks only English"

NAMES = {
    "survey_year": "survey_year",
    "STATE": "state",
    "NP": "household_size",
    "HHT": "household_type",
    "HUPAC": "children_present",
    "NOC": "own_children",
    "NRC": "related_children",
    "R60": "persons_60_and_over",
    "R65": "persons_65_and_over",
    "MULTG": "multigenerational_household",
    "LNGI": "limited_english_household",
    "HHL": "household_language",
    "TEN": "tenure",
    "BLD": "units_in_structure",
    "VEH": "vehicles",
    "HINCP": "household_income",
    "GRNTP": "gross_rent_monthly",
    "SMOCP": "owner_costs_monthly",
    "WIF": "workers_in_family",
    "WKEXREL": "work_experience_householder_spouse",
    "AGEP": "householder_age",
    "SEX": "householder_sex",
    "RAC1P": "householder_race",
    "HISP": "householder_hispanic_origin",
    "SCHL": "householder_education",
    "MAR": "householder_marital_status",
    "CIT": "householder_citizenship",
    "NATIVITY": "householder_nativity",
    "POBP": "householder_place_of_birth",
    "ANC": "householder_ancestry_reported",
    "ENG": "householder_english_ability",
    "DIS": "householder_disability",
    "DEAR": "householder_hearing_difficulty",
    "DEYE": "householder_vision_difficulty",
    "DREM": "householder_cognitive_difficulty",
    "ESR": "householder_employment_status",
    "WKHP": "householder_hours_per_week",
    "COW": "householder_class_of_worker",
    "OCCP": "householder_occupation",
    "MIL": "householder_military_service",
    "PUBCOV": "householder_public_coverage",
    "POVPIP": "householder_poverty_ratio",
    "FER": "householder_gave_birth_past_year",
}
TARGET = "snap_received"

# Ordered scales (CLEAN-14), lowest first, in the words of the 2024 dictionary.
EDUCATION_LEVELS = [
    "No schooling completed", "Nursery school, preschool", "Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4",
    "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "12th grade - no diploma",
    "Regular high school diploma", "GED or alternative credential", "Some college, but less than 1 year",
    "1 or more years of college credit, no degree", "Associate's degree", "Bachelor's degree", "Master's degree",
    "Professional degree beyond a bachelor's degree", "Doctorate degree",
]  # fmt: skip
ENGLISH_LEVELS = ["Not at all", "Not well", "Well", "Very well", ENG_ONLY_ENGLISH]
VEHICLE_LEVELS = [
    "No vehicles", "1 vehicle", "2 vehicles", "3 vehicles", "4 vehicles", "5 vehicles", "6 or more vehicles",
]  # fmt: skip
R60_LEVELS = ["No person 60 and over", "1 person 60 and over", "2 or more persons 60 and over"]
R65_LEVELS = ["No person 65 and over", "1 person 65 and over", "2 or more persons 65 and over"]
WIF_LEVELS = ["No workers", "1 worker", "2 workers", "3 or more workers in family"]
NUMERIC = (
    "survey_year", "household_size", "own_children", "related_children", "household_income", "gross_rent_monthly",
    "owner_costs_monthly", "householder_age", "householder_hours_per_week", "householder_poverty_ratio",
)  # fmt: skip


def _read_items(zip_path: Path, items: tuple[str, ...], *, householders_only: bool):
    """Read the named items of one national housing or person zip (two CSV parts) as integer codes."""
    import polars as pl

    parts = []
    with zipfile.ZipFile(zip_path) as archive:
        for name in sorted(n for n in archive.namelist() if n.endswith(".csv")):
            data = archive.read(name)
            header = [OLD_NAMES.get(c, c) for c in data[: data.index(b"\n")].decode().strip().split(",")]
            wanted = [*items, "RELP", "RELSHIPP"] if householders_only else list(items)
            columns = [i for i, c in enumerate(header) if c in wanted]
            part = pl.read_csv(io.BytesIO(data), columns=columns, infer_schema_length=0)
            del data
            part = part.rename({c: OLD_NAMES[c] for c in part.columns if c in OLD_NAMES})
            if householders_only:
                is_householder = (
                    pl.col("RELP").cast(pl.Int32) == 0 if "RELP" in part.columns else pl.col("RELSHIPP") == "20"
                )
                part = part.filter(is_householder).drop([c for c in ("RELP", "RELSHIPP") if c in part.columns])
            # a blank (the dictionaries' "b", N/A) is written as an empty or space-filled field: a missing value
            codes = [c for c in part.columns if c != "SERIALNO"]
            blank_to_null = [pl.col(c).str.strip_chars().replace("", None).cast(pl.Int64) for c in codes]
            parts.append(part.with_columns(blank_to_null))
    return pl.concat(parts, how="vertical")


def _read_dictionaries(raw_dir: Path) -> pd.DataFrame:
    """The coded values of the CSV data dictionaries 2017-2024: one row per year, item and single code."""
    rows = []
    for year in (2017, 2018, 2019, 2021, 2022, 2023, 2024):
        path = raw_dir / "dictionaries" / f"PUMS_Data_Dictionary_{year}.csv"
        with path.open(encoding="latin-1") as fh:
            for row in csv.reader(fh):
                if row and row[0] == "VAL" and row[4] == row[5] and row[4].strip().isdigit():
                    rows.append((year, row[1], int(row[4]), row[6].strip()))
    table = pd.DataFrame(rows, columns=["year", "item", "code", "label"])
    # STATE and the other shared items are listed twice (housing and person record): one entry each
    return table.drop_duplicates(["year", "item", "code"], keep="first").reset_index(drop=True)


def _decode_codes(codes: pd.Series, labels: dict[int, str], item: str) -> pd.Series:
    """Codes to the dictionary's words as a category (12 million rows: no object column); a code without a label
    raises, as `decode` does. Missing codes stay missing.
    """
    values = codes.to_numpy(dtype="float64", na_value=np.nan)
    known = ~np.isnan(values)
    present = np.unique(values[known])
    unlabelled = [int(c) for c in present if int(c) not in labels]
    if unlabelled:
        raise ValueError(f"Codes of {item!r} without a label: {unlabelled[:10]}")
    words = sorted({labels[int(c)] for c in present})
    position = np.array([words.index(labels[int(c)]) for c in present], dtype="int16")
    category_codes = np.full(len(values), -1, dtype="int16")
    category_codes[known] = position[np.searchsorted(present, values[known])]
    return pd.Series(pd.Categorical.from_codes(category_codes, categories=words), index=codes.index)


class AcsFoodStamps201420241m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Did a US household receive SNAP (food stamps) at any time in the past 12 months, as it reports in the "
            "American Community Survey?"
        ),
        use_case=(
            "For example, a state SNAP agency or an outreach programme fits a model on past survey years and ranks "
            "households of the next year by how likely they are to receive SNAP, to target outreach (TableShift's "
            "'low-cost, low-friction screening tools')."
        ),
        row=(
            "One occupied household in the 50 states and DC, interviewed in an ACS 1-year sample of 2014-2019 or "
            "2021-2024, with its householder's answers; households whose SNAP answer the Census Bureau imputed are "
            "left out."
        ),
        predicted=(
            "Whether anyone in the household received SNAP benefits in the 12 months before the interview, as the "
            "household reported it."
        ),
        known=(
            "The household's make-up, income, housing costs, tenure, vehicles and language, and the householder's "
            "age, sex, race, origin, education, work, occupation, disability, health coverage and poverty ratio, all "
            "from the same interview, with the survey year and the state."
        ),
        split=(
            "Each of the three newest survey years (2022, 2023, 2024) is a test window of up to 500,000 households, "
            "trained on a random million households of all earlier years, as a programme refit on past survey years "
            "would be."
        ),
        changes=(
            "One row per household (TableShift: one per low-income adult); the 2020 experimental file and the "
            "imputed SNAP answers are left out; codes decoded into the codebook's words."
        ),
        fit="approximate",
        fit_reason=(
            "The label is the household's own report, from the interview that gives the features (SEL-7, open for "
            "the curator), and survey answers stand in for what an agency would know about a household; recipients "
            "under-report SNAP in the ACS."
        ),
    )

    # Dataset
    unique_name = "acs_food_stamps_2014_2024_1m"
    version_of = "acs_food_stamps_2014_2024"
    version_comment = """
        We sample per test window (v2 split protocol): each survey-year window keeps at most 500k of its households, and its train side is a random 1M of all households of earlier survey years, drawn in one random order for all windows; the frame keeps only the rows a split uses. The full data has about 1.2 to 1.3 million households a year, 12.5 million in all.
    """
    year = "2025"
    domain = "social science"
    source = "GOV Website"
    source_url = "https://www.census.gov/programs-surveys/acs/microdata.html"
    license = "Public domain (US Government work); no licence is stated on the PUMS pages"
    data_tags = ("Spatial",)
    download_description = """
        The national 1-year PUMS files of the US Census Bureau (no login): the housing (csv_hus.zip) and person (csv_pus.zip) zips of each regular year 2014-2019 and 2021-2024, and the data dictionaries. 2020 has no regular 1-year file (only the experimental release under https://www2.census.gov/programs-surveys/acs/experimental/2020/), and Puerto Rico's files (csv_hpr.zip, csv_ppr.zip) are not read. Each year's zips are as the Census Bureau published them: the server dates run from 2015-10 (the 2014 files) to 2025-12 (the 2024 files, released on 2025-12-04 after a delay from 2025-10-16).

        mkdir -p local-data-warehouse/acs_food_stamps_2014_2024 && cd local-data-warehouse/acs_food_stamps_2014_2024
        for y in 2014 2015 2016 2017 2018 2019 2021 2022 2023 2024; do mkdir -p $y; for f in csv_hus.zip csv_pus.zip; do wget -P $y https://www2.census.gov/programs-surveys/acs/data/pums/$y/1-Year/$f; done; done
        mkdir -p dictionaries
        for y in 2017 2018 2019 2021 2022 2023 2024; do wget -P dictionaries https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_$y.csv; done
        for yy in 14 15 16; do wget -P dictionaries https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMSDataDict$yy.txt; done

        The first run writes acs_households_2014_2024.parquet next to them (`_prepare_raw_files`: the occupied housing units with their householder's items, all years).
    """
    bibtex = """
        @misc{uscensus_acs_pums_1year_2014_2024,
          title = {American Community Survey 1-Year Public Use Microdata Sample, 2014-2019 and 2021-2024},
          author = {{U.S. Census Bureau}},
          year = {2025},
          howpublished = {\\url{https://www.census.gov/programs-surveys/acs/microdata.html}},
          note = {National housing and person files, https://www2.census.gov/programs-surveys/acs/data/pums/}
        }
    """
    curation_comments = """
        We start with the national housing and person files of the ACS 1-year PUMS for 2014-2019 and 2021-2024 (US Census Bureau), joined on SERIALNO as the Census Bureau documents them.

        - Prediction point: a household of a survey year, scored by a model fit on earlier survey years. Everything the interview records is known at that point (the household's own answers); the SNAP answer is the label. The task follows TableShift's Food Stamps task (Gardner et al. 2023; target FS, "Low-cost, low-friction screening tools powered by machine learning models might provide useful information", tableshift.org) with more years and a temporal split in place of TableShift's held-out East South Central division, which the curator found not representative (record `food_stamps`, now a duplicate of this one). The features and the label cover the same past 12 months: the household income, the poverty ratio, the householder's hours, the workers in the family and the work experience summarise the 12 months whose SNAP receipt is the label, so the label is concurrent with them, not later (SEL-7, the curator's call).
        - Unit: one row per occupied housing unit (TYPEHUGQ 1, NP above 0), not per person as in TableShift. FS is a housing item, the household's receipt, and SNAP certifies households: in TableShift's person rows every adult of a household carries the household's label (LEAK-17), and a large household counts several times in a decision made once per household (MET-17). The householder's person items (RELP 0 until 2018, RELSHIPP 20 from 2019; exactly one per household in every year) stand for the person items; group quarters and vacant units have no FS. We keep every occupied household, without TableShift's filter on the person (age 18 to 61, personal income up to $30,000, HUPAC not blank).
        - Dropped rows: households whose FS answer the Census Bureau allocated (FFSP 1; the label is the Bureau's hot-deck imputation, not a report): 1.7% to 1.8% of households in 2014-2018, 1.9% in 2019 and 2.9% to 3.1% in 2021-2024 (decision table). The Bureau's imputed Yes share on these rows is 12.3% to 14.7% a year, above the 9.3% to 12.0% reported, so the drop removes somewhat poorer households, not a random 2-3%.
        - Target: `snap_received`, "Yes" for FS 1 ("Yearly food stamp/Supplemental Nutrition Assistance Program (SNAP) recipiency": yes), "No" for FS 2. Its unweighted share falls from 12.0% (2014) to 9.3% (2019) and is 10.9%, 10.7%, 10.6% and 10.2% in 2021-2024. These are shares of the sample, not the published rates: weighted with the housing weight WGTP, the shares are 13.2% (2014), 10.7% (2019) and 11.7% (2024), so the sample holds 1.2 to 1.5 points fewer recipient households than the population.
        - Note: the label is the household's own report. Linked to administrative SNAP records of two states, 35% of true recipient households did not report receipt in the ACS (Meyer, Mittag and Goerge, "Errors in Survey Reporting and Imputation and their Effects on Estimates of Food Stamp Program Participation", NBER WP 25143, 2018, abstract; Journal of Human Resources 2022), so "No" holds unreported recipients.
        - Features: the household items HHT, HUPAC, NOC, NRC, NP, R60, R65, MULTG, LNGI, HHL, TEN, BLD, VEH, HINCP, GRNTP, SMOCP, WIF, WKEXREL and the state, and the householder's AGEP, SEX, RAC1P, HISP, SCHL, MAR, CIT, NATIVITY, POBP, ANC, ENG, DIS, DEAR, DEYE, DREM, ESR, WKHP, COW, OCCP, MIL, PUBCOV, POVPIP and FER, plus the survey year. They are TableShift's person items that keep one meaning in every year, for the householder, and the household items the housing file has in every year (FES is gone from 2021, so WIF and WKEXREL describe the family's work). Left out of TableShift's list: RELP (the householder by construction), WKW (weeks worked: bands until 2018, a number from 2019), NWLA, NWLK and WRK (ESR holds the labour-force status), DIVISION (a function of the state).
        - Not read, as survey design rather than the household (MET-16): the housing weight WGTP and the person weight PWGTP with their 80 replicate weights each. The task scores each household's label, not a population estimate, so it is scored unweighted and declares no training weight. Not read either: SERIALNO beyond the join (an identifier), the allocation flags other than FFSP, REGION and DIVISION (functions of the state), and PUMA, whose codes were redrawn on the 2020 census from the 2022 files on, so one code means another area before and after.
        - Not read, as a choice of the feature set (TableShift's list): public assistance income (PAP), SSI (SSIP) and Medicaid (HINS4) as items of their own. Their content enters the household income (PAP, SSIP) and the householder's public coverage recode (PUBCOV), which TableShift keeps. They are no leak: each is known at the interview, and none is a part, a consequence or an encoding of the SNAP answer. Measured with untuned LightGBM (400k households of 2022-2023 for training, 200k of 2024 for testing, review panel 2026-11-09): the householder's PAP, SSIP and HINS4 add 0.0065 ROC AUC; any member's public assistance, SSI or Medicaid add 0.017 (0.9142 to 0.9312), and some member has Medicaid in 80.1% of the Yes households against 16.2% of the No households.
        - Allocated feature values are kept as the Census Bureau released them; the allocation flags are no inputs (PROV-13). In 2024, among the households with a reported SNAP answer, some member's income is allocated in 33.6%, the householder's public coverage recode in 18.5% and public assistance income in 13.2% (age 0.6%, race 0.5%, sex 0.01%). The income hot-deck carries no SNAP answer: the two income columns add 0.0143 ROC AUC on the households with reported income and 0.0015 on those with allocated income, so imputed incomes do not encode FS (LEAK-10 not triggered).
        - Dollars: household income (HINCP) is multiplied by ADJINC and the rent and owner costs (GRNTP, SMOCP) by ADJHSG, the Census Bureau's factors that put each file's amounts in the survey year's dollars, rounded to the dollar. Amounts of different survey years stay in their own year's dollars; `householder_poverty_ratio` (POVPIP, income over the poverty threshold of the family's size, in percent, 501 meaning 501% or more) is the measure that is comparable across years. SNAP's income test is set against the poverty guidelines.
        - Coded items are decoded into the dictionary's words (CLEAN-12): the items whose codes keep one meaning in every year with the 2024 words; POBP and OCCP with each year's own dictionary (2017's for 2014-2016, plus the two POBP codes of the 2014-2016 dictionaries the 2017 one lacks or gives to another country: 208 Cyprus, 463 Eastern Africa, Not Specified), then in the 2024 wording where the words agree up to case. Occupations follow the 2010 Census codes until 2017 and the 2018 codes from 2018, so some occupations have two levels.
        - Ordered (CLEAN-14): education (SCHL, the dictionary's 24 levels), English ability (ENG; a blank, "speaks only English" for a person of 5 or older, is its top level), vehicles (VEH, open end "6 or more vehicles"), persons 60 and over, persons 65 and over (open end "2 or more") and workers in family (open end "3 or more"). Units in structure (BLD) stays unordered: mobile homes and boats are not on the scale of apartments.
        - Blanks stay missing: WIF and WKEXREL for a household that is not a family, GRNTP for owners and households without rent payment, SMOCP for renters, COW and OCCP for a householder who last worked more than 5 years ago or never worked (ESR says whether they work now), WKHP for one who did not work in the past 12 months, FER for a male householder or one over 50, MIL for a householder under 17, and ANC code 8 ("Suppressed for data year 2018 for select PUMAs", 2018 and 2019 files).
        - Anomaly: AGEP and WKHP are top-coded (99 hours or more), and income amounts are rounded and top-coded per state by the Census Bureau's disclosure rules.
        - Anomaly: the race item has a coding break at 2020 (the Bureau's new coding of written-in races): "Two or More Races" is 1.7% to 1.9% of householders in 2014-2019 and 8.6% to 8.7% in 2021-2024, "White alone" falls from 80% to 73%. Every test window lies after the break; no crosswalk exists.
        - Potential leak, kept on purpose: the household income is the reported amount, and an exact, non-round amount (a benefit payment, for example) goes with SNAP: flags for multiples of 10, 100, 1,000 and 10,000 of the reported income reach ROC AUC 0.60 on their own (review panel, 2026-11-09), and the number-format probe's 0.706 is the same signal together with the tenure blanks. It stays because it is the household's own answer, known at the interview, not a mark the recording left by class (LEAK-13 not triggered); revisit if a release rounds the amounts differently by survey year.
        - Note: the householder's sex, age, race, Hispanic origin, ancestry (how it was reported), place of birth, citizenship, nativity, disability and the hearing, vision and cognitive difficulty items are inputs, as in TableShift. A state SNAP agency may not discriminate against "any applicant or participant" in "the certification of households" or any program service "for reasons of age, race, color, sex, disability, religious creed, national origin, or political beliefs" (7 CFR 272.6(a)). The householder's sex also shows in household_type, work_experience_householder_spouse and householder_gave_birth_past_year, which name it for 69.4% of the rows. A state agency could not use them under the outreach framing; the imputer framing keeps them, as no such law binds the Census Bureau (the framing is SEL-7's open call).
        - History: 2014 to 2024, the record's range, so the oldest of the three yearly test windows still trains on 7 of the 10 survey years (SPLIT-14). 2020 is left out (see the splits). The training years cross the 2020 break (SPLIT-20): the Yes share falls from 12.0% (2014) to 9.3% (2019) and is 10.9% in 2021, with the pandemic and SNAP's emergency allotments; a model trained on 2014-2019 alone under-predicts the test years' Yes share by about 2 points (2.1 to 2.4) and scores 0.003 to 0.005 ROC AUC below the shipped history. The test years are not typical either: 2022 lies in the emergency-allotment period, 2023 holds its end (after February 2023 in 32 states and DC, earlier in the other 18) and the start of the Medicaid unwinding (April 2023, which moves the public coverage feature), and 2024 is the first year after both. The older years stay: three yearly windows need them for SPLIT-14's floor, and the survey year is a feature.
        - Protocol (LEAK-9, SPLIT-9): a method fits only on its split's train rows and predicts each test row from them and its own inputs. The frame also holds the labelled rows of later survey years, and adding them to training gains 0.003 to 0.006 ROC AUC (about 0.0005 of it from the future itself, the rest from more rows). Statistics over the test rows are no feature step either: income percentiles within a survey year over the train and test rows gain 0.0006 to 0.0013, the nominal-dollar drift (LEAK-30). Nor is a lookup in the public PUMS, which returns a row's answer (543 of 963 Wyoming rows of 2024 matched uniquely, all with the same answer). A method that uses any of these is called out and not benchmarked.
        - Puerto Rico is not in the national files (its programme is the Nutrition Assistance Program, not SNAP); TableShift read the state files, Puerto Rico's included.
    """

    # Task
    target = TARGET
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The Census Bureau publishes the PUMS for estimates and defines no prediction task. TableShift (Gardner "
            "et al. 2023), which defined the food stamps task, reports accuracy for every task of its benchmark, a "
            "house convention, not a choice from the decision (MET-5, MET-6), on person rows and a held-out "
            "region. No other source metric was found (tableshift.org, the record's screening of 2026-10-31). "
            "roc_auc is the binary fallback, scored unweighted: the task ranks households, not a population "
            "estimate (MET-16)."
        ),
    )

    # Splits
    splits_comment = """
        We use each of the three newest survey years (2022, 2023, 2024) once as test data, with all households of the earlier years as train data (2014-2019 and 2021; 2020 has no regular file). A programme refits once a year on the newest released file. The Census Bureau releases a year's 1-year PUMS 9 to 11 months after the year ends (the 2023 file on 17 October 2024, the 2024 file on 4 December 2025), so for most of a test year the newest file at hand is two years old. No gap is set all the same (SPLIT-10, as amended on lt_vehicle_loan_default_prediction): all of a year's labels arrive together and final, so the newest training year holds no selection by the outcome. At equal training size it adds 0.0010 to 0.0027 ROC AUC over a one-year gap (0.0027 for the 2022 window, 0.0010 for 2023, 0.0013 for 2024). The oldest window trains on 7 of the 10 survey years. Each window keeps at most 500k of its households; each train side is a random 1M of all earlier households (one random order for all windows). The cap is the row budget: training on every earlier household instead would gain 0.0028 to 0.0045 ROC AUC in the 2024 and 2023 windows.
    """
    temporal = Temporal(
        on="survey_year",
        splits=TemporalSplits(window=1, unit="unique", n_windows=3),
        horizon=1,
        horizon_unit="years",
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (PREPARED_FILE,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        import polars as pl

        frames = []
        for survey_year in YEARS:
            housing = _read_items(raw_dir / str(survey_year) / "csv_hus.zip", HOUSING_ITEMS, householders_only=False)
            persons = _read_items(raw_dir / str(survey_year) / "csv_pus.zip", PERSON_ITEMS, householders_only=True)
            # occupied housing units only: group quarters (TYPEHUGQ 2, 3) and vacant units (NP 0) have no FS
            housing = housing.filter((pl.col("TYPEHUGQ") == 1) & (pl.col("NP") > 0)).drop("TYPEHUGQ")
            assert persons["SERIALNO"].n_unique() == persons.height, "one householder per housing unit"
            frame = housing.join(persons, on="SERIALNO", how="left")
            assert frame["AGEP"].null_count() == 0, "every occupied housing unit has a householder record"
            frames.append(frame.with_columns(pl.lit(survey_year, dtype=pl.Int32).alias("survey_year")))
        households = pl.concat(frames, how="vertical").sort(["survey_year", "SERIALNO"])
        households.write_parquet(raw_dir / PREPARED_FILE)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        households = pd.read_parquet(raw_dir / PREPARED_FILE)
        return {"households": households, "dictionary": _read_dictionaries(raw_dir)}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw["households"]
        dictionary = raw["dictionary"]

        # 1. Rows: a reported SNAP answer only (FFSP 0); an allocated FS is the Census Bureau's imputation.
        df = df[df["FFSP"] == 0].copy()

        # 2. The target in words (CLEAN-25).
        df[TARGET] = _decode_codes(df["FS"], {1: "Yes", 2: "No"}, "FS")
        assert df[TARGET].notna().all(), "FS is 1 or 2 for every occupied household"

        # 3. Dollars of the survey year: the Census Bureau's adjustment factors (6 implied decimals).
        df["HINCP"] = (df["HINCP"] * df["ADJINC"] / 1e6).round()
        for item in ("GRNTP", "SMOCP"):
            df[item] = (df[item] * df["ADJHSG"] / 1e6).round()

        # 4. Codes that mean unknown: ANC 8, suppressed in 2018 for select PUMAs.
        df["ANC"] = df["ANC"].where(df["ANC"] != 8)

        # 5. Decode (CLEAN-12): one meaning per code in every year, the 2024 words. A blank ENG of a householder (15
        #    or older) is "speaks only English", the top of the scale: code 0 here, a code the dictionary never uses.
        df["ENG"] = df["ENG"].fillna(0)
        words_2024 = dictionary[dictionary["year"] == 2024]
        for item in STABLE_CODED:
            entries = words_2024[words_2024["item"] == item]
            labels = dict(zip(entries["code"], entries["label"], strict=True))
            if item == "ENG":
                labels[0] = ENG_ONLY_ENGLISH
            df[item] = _decode_codes(df[item], labels, item)

        # 6. Decode POBP and OCCP with each year's own dictionary (2017's for 2014-2016), in the 2024 wording: one
        #    label per (survey year, code), keyed as year * 100000 + code.
        for item in YEARLY_CODED:
            canonical = {label.casefold(): label for label in words_2024.loc[words_2024["item"] == item, "label"]}
            labels = {}
            for survey_year in YEARS:
                own = dictionary[(dictionary["year"] == max(survey_year, 2017)) & (dictionary["item"] == item)]
                year_labels = dict(zip(own["code"], own["label"], strict=True))
                if item == "POBP" and survey_year <= 2016:
                    year_labels.update(POBP_2014_2016)
                for code, label in year_labels.items():
                    labels[survey_year * 100000 + code] = canonical.get(label.casefold(), label)
            keys = df["survey_year"].astype("int64") * 100000 + df[item]
            df[item] = _decode_codes(keys, labels, item)

        # 7. Drop what is not a feature: the identifier, the raw label and its flag, the dollar factors.
        df = drop_columns(df, ["SERIALNO", "FS", "FFSP", "ADJINC", "ADJHSG"])
        df = df.rename(columns=NAMES)
        return df[[*NAMES.values(), TARGET]]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        ordinal = {
            "householder_education": EDUCATION_LEVELS,
            "householder_english_ability": ENGLISH_LEVELS,
            "vehicles": VEHICLE_LEVELS,
            "persons_60_and_over": R60_LEVELS,
            "persons_65_and_over": R65_LEVELS,
            "workers_in_family": WIF_LEVELS,
        }
        categorical = [c for c in df.columns if c not in NUMERIC and c not in ordinal and c != TARGET]
        return FeatureTypes(categorical=categorical, ordinal=ordinal)

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        households = raw["households"][["survey_year", "FS", "FFSP"]]
        reported = households[households["FFSP"] == 0]
        by_year = pd.DataFrame(
            {
                "occupied households": households.groupby("survey_year").size(),
                "share with an allocated SNAP answer": households.groupby("survey_year")["FFSP"].mean().round(4),
                "SNAP share among reported answers (unweighted)": (reported["FS"] == 1)
                .groupby(reported["survey_year"])
                .mean()
                .round(4),
            }
        )
        return [
            Decision(
                title="Households with an allocated SNAP answer are dropped",
                why=(
                    "FFSP 1 marks an FS value the Census Bureau imputed for a household that did not answer the item: "
                    "the label of those rows is the Bureau's hot-deck guess, not a report. The table gives, per survey "
                    "year, the occupied households, the share with an allocated FS and the unweighted SNAP share "
                    "among the reported answers."
                ),
                evidence=by_year,
            )
        ]
