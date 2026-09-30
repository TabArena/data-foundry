"""Curated dataset definition for `pva_revenue_prediction_kddcup98` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class PvaRevenuePredictionKddcup98(AbstractCuratedDataset):
    # Dataset
    unique_name = "pva_revenue_prediction_kddcup98"
    year = "1997"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://kdd.ics.uci.edu/databases/kddcup98/kddcup98.html"  # Rel 10.24432/C5401H
    license = None  # Unclear but has usage instruction that do not count as license (?)
    download_description = """
        wget https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98lrn.zip && unzip cup98lrn && rm cup98lrn.zip
        wget https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98val.zip && unzip cup98val && rm cup98val.zip && wget https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/valtargt.txt
        mkdir -p local-data-warehouse/pva_revenue_prediction_kddcup98 && mv cup98VAL.txt local-data-warehouse/pva_revenue_prediction_kddcup98/ && mv cup98LRN.txt local-data-warehouse/pva_revenue_prediction_kddcup98/ && mv valtargt.txt local-data-warehouse/pva_revenue_prediction_kddcup98/
    """
    bibtex = r"""
        @misc{Parsa1998KDDCup1998,
          author = {Ismail Parsa},
          title  = {KDD Cup 1998},
          year   = {1998},
          howpublished = {\url{https://kdd.ics.uci.edu/databases/kddcup98/kddcup98.html}},
          note   = {Dataset, UCI Machine Learning Repository. DOI: 10.24432/C5401H}
        }
    """
    curation_comments = """
        We start with the train and validation data from the KDD Cup 1998 website and combine them.

        - The description of the task and data for the KDD Cup (https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98doc.txt) is among the best real-world dataset and task descriptions I have ever seen.
        - The task was made IID through feature engineering and would usually used to predict the next year. We only predict from the training data from the current year, other samples from the current year (as to see who else to contact in the same year). Features contain information from the previous year.
        - The task is revenue generation and the score function is profit-based with a cost of $0.68 per prediction. The higher the revenue generated, the better. We use the binary classification target (TARGET_B) to predict if a person would donate.
        - The TCODE contains titles now in the data dictionary. We map large amount of missing values to placeholder titles and the smaller ones to a new "other" title.
        - We treat data as string or category based on the data dictionary suggestions. In cases where the column is from a predefined set of choices, it becomes categorical. We treat various free-text categorical as string columns (they are also high-cardinality otherwise).
        - We transform the date columns to pandas datetime.
        - The data contains spatial information (ZIP, STATE). We do not resolve them and leave them for the pipeline to handle.
        - We remove a faulty postfix ("-") in the ZIP code.
        - We drop rows with PVASTATE='E' as this represent a group of donors represent by a different organization chapter. These are 8 rows only.
        - The data contains two entries with a faulty day of birth (born in month 00). We drop both rows, as we assume this is indicative of faulty data.
        - We noticed that nan values and dtypes mismatch for NOEXCH do correlate with the target. We add these cases as their own categories.
        - We resolve the ordinal encoding and nan encoding for all columns.
        - Note, that data has a lot of features that contain data from a similar origin that was transformed into individual columns.
        - We do not decode the promotion codes across years but keep them as string columns as it would blow up the dimensionality too much otherwise.
    """

    # Task
    target = "TARGET_B"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "cup98LRN.txt")
        val_df = pd.read_csv(raw_dir / "cup98VAL.txt")
        val_targets = pd.read_csv(raw_dir / "valtargt.txt")
        return {"df": df, "val_df": val_df, "val_targets": val_targets}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, val_df, val_targets = raw["df"], raw["val_df"], raw["val_targets"]
        df = pd.concat([df, val_df.merge(val_targets, on="CONTROLN")], axis=0).reset_index(drop=True)
        title_code_map = {
            0: "No Title",
            1: "MR.",
            1001: "MESSRS.",
            1002: "MR. & MRS.",
            2: "MRS.",
            2002: "MESDAMES",
            3: "MISS",
            3003: "MISSES",
            4: "DR.",
            4002: "DR. & MRS.",
            4004: "DOCTORS",
            5: "MADAME",
            6: "SERGEANT",
            9: "RABBI",
            10: "PROFESSOR",
            10002: "PROFESSOR & MRS.",
            10010: "PROFESSORS",
            11: "ADMIRAL",
            11002: "ADMIRAL & MRS.",
            12: "GENERAL",
            12002: "GENERAL & MRS.",
            13: "COLONEL",
            13002: "COLONEL & MRS.",
            14: "CAPTAIN",
            14002: "CAPTAIN & MRS.",
            15: "COMMANDER",
            15002: "COMMANDER & MRS.",
            16: "DEAN",
            17: "JUDGE",
            17002: "JUDGE & MRS.",
            18: "MAJOR",
            18002: "MAJOR & MRS.",
            19: "SENATOR",
            20: "GOVERNOR",
            21002: "SERGEANT & MRS.",
            22002: "COLNEL & MRS.",
            24: "LIEUTENANT",
            26: "MONSIGNOR",
            27: "REVEREND",
            28: "MS.",
            28028: "MSS.",
            29: "BISHOP",
            31: "AMBASSADOR",
            31002: "AMBASSADOR & MRS.",
            33: "CANTOR",
            36: "BROTHER",
            37: "SIR",
            38: "COMMODORE",
            40: "FATHER",
            42: "SISTER",
            43: "PRESIDENT",
            44: "MASTER",
            46: "MOTHER",
            47: "CHAPLAIN",
            48: "CORPORAL",
            50: "ELDER",
            56: "MAYOR",
            59002: "LIEUTENANT & MRS.",
            62: "LORD",
            63: "CARDINAL",
            64: "FRIEND",
            65: "FRIENDS",
            68: "ARCHDEACON",
            69: "CANON",
            70: "BISHOP",
            72002: "REVEREND & MRS.",
            73: "PASTOR",
            75: "ARCHBISHOP",
            85: "SPECIALIST",
            87: "PRIVATE",
            89: "SEAMAN",
            90: "AIRMAN",
            91: "JUSTICE",
            92: "MR. JUSTICE",
            100: "M.",
            103: "MLLE.",
            104: "CHANCELLOR",
            106: "REPRESENTATIVE",
            107: "SECRETARY",
            108: "LT. GOVERNOR",
            109: "LIC.",
            111: "SA.",
            114: "DA.",
            116: "SR.",
            117: "SRA.",
            118: "SRTA.",
            120: "YOUR MAJESTY",
            122: "HIS HIGHNESS",
            123: "HER HIGHNESS",
            124: "COUNT",
            125: "LADY",
            126: "PRINCE",
            127: "PRINCESS",
            128: "CHIEF",
            129: "BARON",
            130: "SHEIK",
            131: "PRINCE AND PRINCESS",
            132: "YOUR IMPERIAL MAJEST",
            135: "M. ET MME.",
            210: "PROF.",
        }
        recency_map = {
            "C": "Current Donor",
            "L": "Lapsed Donor",
            "I": "Inactive Donor",
            "D": "Dormant Donor",
        }
        frequency_map = {
            "1": "One gift in the period of recency",
            "2": "Two-Four gifts in the period of recency",
            "5": "Five+ gifts in the period of recency",
        }
        amount_map = {
            "L": "Less than $100 (Low Dollar)",
            "C": "$100-499 (Core)",
            "M": "$500-999 (Major)",
            "T": "$1,000+ (Top)",
        }
        urbanicity_map = {
            "U": "Urban",
            "C": "City",
            "S": "Suburban",
            "T": "Town",
            "R": "Rural",
        }
        ses_map = {
            "1": "Highest SES",
            "2": "Average SES",
            "3": "Lowest SES",
            "4": "Lower Lowest SES in Urban communities",  # weird name to show it is lower as otherwise we would need to rename 2 and 3 only for urban cases, but this should be fine.
        }
        # Handle DOB
        df = df[
            ~df["DOB"].replace(np.nan, 1111).astype(float).astype(int).astype(str).str.zfill(4).str.endswith("00")
        ]  # drop 2 rows with month 00
        df["DOB"] = df["DOB"].replace(0, np.nan)
        dob_nan_mask = df["DOB"].isna()
        df.loc[dob_nan_mask, "DOB"] = 0
        df["DOB"] = df["DOB"].astype(float).astype(int).astype("string").str.zfill(4)
        df.loc[dob_nan_mask, "DOB"] = np.nan
        df["DOB"] = pd.to_datetime("19" + df["DOB"], format="%Y%m")
        # Make pd Dates (unclear if best preprocessing is not just int as in original data but this way we have the correct metadata of the col)
        prom_dates = [
            "ADATE_2",
            "ADATE_3",
            "ADATE_4",
            "ADATE_5",
            "ADATE_6",
            "ADATE_7",
            "ADATE_8",
            "ADATE_9",
            "ADATE_10",
            "ADATE_11",
            "ADATE_12",
            "ADATE_13",
            "ADATE_14",
            "ADATE_15",
            "ADATE_16",
            "ADATE_17",
            "ADATE_18",
            "ADATE_19",
            "ADATE_20",
            "ADATE_21",
            "ADATE_22",
            "ADATE_23",
            "ADATE_24",
            "RDATE_3",
            "RDATE_4",
            "RDATE_5",
            "RDATE_6",
            "RDATE_7",
            "RDATE_8",
            "RDATE_9",
            "RDATE_10",
            "RDATE_11",
            "RDATE_12",
            "RDATE_13",
            "RDATE_14",
            "RDATE_15",
            "RDATE_16",
            "RDATE_17",
            "RDATE_18",
            "RDATE_19",
            "RDATE_20",
            "RDATE_21",
            "RDATE_22",
            "RDATE_23",
            "RDATE_24",
            "MAXADATE",
            "ODATEDW",
            "MINRDATE",
            "MAXRDATE",
            "LASTDATE",
            "FISTDATE",
            "NEXTDATE",
        ]
        df["FISTDATE"] = df["FISTDATE"].replace(0, np.nan)
        for col in prom_dates:
            nan_mask = df[col].isna()
            df.loc[nan_mask, col] = 1111
            df[col] = pd.to_datetime("19" + df[col].astype(int).astype("string"), format="%Y%m")
            df.loc[nan_mask, col] = np.nan
        # Update title map
        missing_title_in_data_dic = list(np.unique(df[~df["TCODE"].isin(title_code_map.keys())]["TCODE"]))
        for code in missing_title_in_data_dic:
            title_code_map[code] = f"Missing Title {code}"
        # Replace Title
        assert df["TCODE"].isin(title_code_map.keys()).all(), "Some TCODE values are not in the title_code_map"
        df["Title"] = df["TCODE"].map(title_code_map)
        df = df.drop(columns=["TCODE"])
        # Handle outsource codes
        df["OSOURCE"] = df["OSOURCE"].replace(" ", np.nan)
        # Remove postfix from ZIP
        df["ZIP"] = df["ZIP"].str.replace("-", "")
        # Handle mailcode
        df["MAILCODE"] = df["MAILCODE"].replace({" ": "Address is OK", "B": "Bad Address"})
        # Handle missing values PVASTATE
        df["PVASTATE"] = df["PVASTATE"].replace(" ", np.nan)
        df = df[df["PVASTATE"] != "E"]
        # a scatterplot of these values and the targets shows some superficial correlation
        df["NOEXCH"] = df["NOEXCH"].replace(
            {
                " ": "can be exchanged",
                "X": "cannot be exchanged",
                0: "0-nan-case",
                "0": "0-nan-case",
                1: "1-nan-case",
                "1": "1-nan-case",
            }
        )  # .value_counts(dropna=False)
        # -- Resolve some of the cat variables
        df["RECINHSE"] = df["RECINHSE"].replace(
            {" ": "Not an In House Record", "X": "Donor has given to PVA's In House program"}
        )
        df["RECP3"] = df["RECP3"].replace({" ": "Not a P3 Record", "X": "Donor has given to PVA's P3 program"})
        df["RECPGVG"] = df["RECPGVG"].replace({" ": "Not a Planned Giving Record", "X": "Planned Giving Record"})
        df["RECSWEEP"] = df["RECSWEEP"].replace({" ": "Not a Sweepstakes Record", "X": "Sweepstakes Record"})
        # -- Resolve MDMAUD
        # Split into 4 bytes (pad right so short strings don't error)
        b = df["MDMAUD"].str.pad(4, side="right").str[:4]
        b1, b2, b3 = b.str[0], b.str[1], b.str[2]
        # Create categorical columns using the descriptions
        df["MDMAUD_recency"] = b1.map(recency_map)
        df["MDMAUD_frequency"] = b2.map(frequency_map)
        df["MDMAUD_amount"] = b3.map(amount_map)
        df["MAJOR"] = df["MAJOR"].replace({" ": "Not a Major Donor", "X": "Major Donor"})
        assert ((df["MAJOR"] == "Not a Major Donor") == df["MDMAUD"].str.upper().eq("XXXX")).all()
        df.loc[df["MAJOR"] == "Not a Major Donor", ["MDMAUD_recency", "MDMAUD_frequency", "MDMAUD_amount"]] = (
            "Not applicable"
        )
        df = df.drop(columns=["MDMAUD"])  # can be recovered by pipelines if needed via arithmetic interactions
        # Resolve DOMAIN Code
        s = df["DOMAIN"].replace(" ", np.nan).astype("string")
        b = s.str.pad(2, side="right")
        b1 = b.str[0]
        b2 = b.str[1]
        df["DOMAIN_urbanicity"] = b1.map(urbanicity_map)
        df["DOMAIN_ses"] = b2.map(ses_map)
        df = df.drop(columns=["DOMAIN"])
        # Cluster fix nan
        df["CLUSTER"] = df["CLUSTER"].replace(" ", np.nan)  # Likely not Ordinal
        # Age (has no - values like data dict is saying), so skip but resolve for ageflag
        df["AGEFLAG"] = df["AGEFLAG"].replace({0: np.nan, "E": "Exact", "I": "Inferred from Date of Birth Field"})
        df["HOMEOWNR"] = df["HOMEOWNR"].replace({" ": np.nan, "H": "Homeowner", "U": "Unknown"})
        # Resolve child
        child_map = {"B": "Both", "F": "Female", "M": "Male", " ": np.nan}
        child_cols = ["CHILD03", "CHILD07", "CHILD12", "CHILD18"]
        for col in child_cols:
            df[col] = df[col].replace(child_map)
        df["GENDER"] = df["GENDER"].replace(
            {"M": "Male", "F": "Female", "U": "Unknown", " ": np.nan, "J": "Joint Account, unknown gender"}
        )
        df["DATASRCE"] = df["DATASRCE"].replace({" ": np.nan, "1": "MetroMail", "2": "Polk", "3": "Both"})
        # Not Ordinal/Int as 0 is equal to INF
        df["SOLIH"] = df["SOLIH"].replace(
            {
                " ": "can be mailed (Default)",
                "00": "Do Not Solicit",
                "01": "one solicitation per year",
                "02": "two solicitations per year",
                "03": "three solicitations per year",
                "04": "four solicitations per year",
                "05": "five solicitations per year",
                "06": "six solicitations per year",
                "12": "twelve solicitations per year",
            }
        )
        df["SOLP3"] = df["SOLP3"].replace(
            {
                " ": "can be mailed (Default)",
                "00": "Do Not Solicit or Mail",
                "01": "one solicitation per year",
                "02": "two solicitations per year",
                "03": "three solicitations per year",
                "04": "four solicitations per year",
                "05": "five solicitations per year",
                "06": "six solicitations per year",
                "12": "twelve solicitations per year",
            }
        )
        df["GEOCODE"] = df["GEOCODE"].replace(" ", "No code has been assigned or did not match at any level")
        df["LIFESRC"] = df["LIFESRC"].replace(
            {
                " ": np.nan,
                "1": "MATCHED ON METRO MAIL ONLY",
                "2": "MATCHED ON POLK ONLY",
                "3": "MATCHED BOTH MM AND POLK",
            }
        )
        df["PEPSTRFL"] = df["PEPSTRFL"].replace({" ": np.nan, "X": "Has PEP Star RFA Status"})
        df["GEOCODE2"] = df["GEOCODE2"].replace(" ", np.nan)
        # Resolve interests
        y_n_map_list = [
            "COLLECT1",
            "VETERANS",
            "BIBLE",
            "CATLG",
            "HOMEE",
            "PETS",
            "CDPLAY",
            "STEREO",
            "PCOWNERS",
            "PHOTO",
            "CRAFTS",
            "FISHER",
            "GARDENIN",
            "BOATS",
            "WALKER",
            "KIDSTUFF",
            "CARDS",
            "PLATES",
        ]
        for col in y_n_map_list:
            # Data dir says it is yes/no, but data is yes or missing, so I will go for missing as it is more general
            assert np.unique(df[col].dropna()).tolist() == [" ", "Y"]
            df[col] = df[col].replace({"Y": "Yes", " ": np.nan})
        df = df.drop(
            columns=[
                "CONTROLN",  # uninformative index column
                "RFA_2R",  # constant col
                # Already decoded above and added semantics
                "MDMAUD_R",
                "MDMAUD_A",
                "MDMAUD_F",
                # Other target
                "TARGET_D",
            ]
        )
        # -- Dtypes
        as_type_str = [
            "OSOURCE",
            "STATE",
            "ZIP",
            "Title",
            # RFA codes (not decoded as too many columns otherwise)
            "RFA_2",
            "RFA_3",
            "RFA_4",
            "RFA_5",
            "RFA_6",
            "RFA_7",
            "RFA_8",
            "RFA_9",
            "RFA_10",
            "RFA_11",
            "RFA_12",
            "RFA_13",
            "RFA_14",
            "RFA_15",
            "RFA_16",
            "RFA_17",
            "RFA_18",
            "RFA_19",
            "RFA_20",
            "RFA_21",
            "RFA_22",
            "RFA_23",
            "RFA_24",
        ]
        as_type_cat = [
            "PVASTATE",
            "MAILCODE",
            "NOEXCH",
            "RECINHSE",
            "RECP3",
            "RECPGVG",
            "RECSWEEP",
            "MDMAUD_recency",
            "MDMAUD_frequency",
            "MDMAUD_amount",
            "MAJOR",
            "DOMAIN_urbanicity",
            "DOMAIN_ses",
            "CLUSTER",
            "CLUSTER2",
            "AGEFLAG",
            "HOMEOWNR",
            "CHILD03",
            "CHILD07",
            "CHILD12",
            "CHILD18",
            "GENDER",
            "DATASRCE",
            "SOLIH",
            "SOLP3",
            "GEOCODE",
            "GEOCODE2",
            "LIFESRC",
            "PEPSTRFL",
            "HPHONE_D",
            "RFA_2F",
            "RFA_2A",
            "TARGET_B",  # will be dropped later, but making sure it is valid
        ] + y_n_map_list
        for c in as_type_str:
            df[c] = df[c].replace(" ", np.nan)
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        df[as_type_cat] = df[as_type_cat].astype("category")
        return df
