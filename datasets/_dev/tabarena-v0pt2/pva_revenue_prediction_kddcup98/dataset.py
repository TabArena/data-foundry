"""Curated dataset definition for `pva_revenue_prediction_kddcup98` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode, set_missing

DATE_COLUMNS = [
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
"""Dates coded as YYMM numbers, parsed with a "19" century prefix."""

INTEREST_COLUMNS = [
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
"""Interest flags: "Y" or blank in the raw data."""

STRING_COLUMNS = [
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
"""Free-text and high-cardinality code columns, kept as strings."""


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "SOLP3": [
        "Do Not Solicit or Mail",
        "one solicitation per year",
        "two solicitations per year",
        "twelve solicitations per year",
        "can be mailed (Default)",
    ],  # open-ended
    "SOLIH": [
        "Do Not Solicit",
        "one solicitation per year",
        "two solicitations per year",
        "three solicitations per year",
        "four solicitations per year",
        "five solicitations per year",
        "six solicitations per year",
        "twelve solicitations per year",
        "can be mailed (Default)",
    ],  # open-ended
    "RFA_2F": [
        "one gift in the period of recency",
        "two gifts in the period of recency",
        "three gifts in the period of recency",
        "four or more gifts in the period of recency",
    ],  # open-ended
    "RFA_2A": ["$5.00 - $9.99", "$10.00 - $14.99", "$15.00 - $24.99", "$25.00 and above"],  # open-ended
    "GEOCODE2": ["D", "C", "B", "A"],
    "DOMAIN_ses": ["Lowest SES", "Below average SES", "Average SES", "Above average SES", "Highest SES"],
    "MDMAUD_recency": ["Dormant Donor", "Inactive Donor", "Lapsed Donor", "Current Donor"],
    "MDMAUD_frequency": [
        "One gift in the period of recency",
        "Two-Four gifts in the period of recency",
        "Five+ gifts in the period of recency",
    ],  # open-ended
    "MDMAUD_amount": [
        "Less than $100 (Low Dollar)",
        "$100-499 (Core)",
        "$500-999 (Major)",
        "$1,000+ (Top)",
    ],  # open-ended
}


# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "RFA_2F": {
        "1": "one gift in the period of recency",
        "2": "two gifts in the period of recency",
        "3": "three gifts in the period of recency",
        "4": "four or more gifts in the period of recency",
    },
    "RFA_2A": {"D": "$5.00 - $9.99", "E": "$10.00 - $14.99", "F": "$15.00 - $24.99", "G": "$25.00 and above"},
    "AGEFLAG": {"Exact": "exact", "Inferred from Date of Birth Field": "inferred from date of birth field"},
    "GENDER": {"Male": "male", "Female": "female", "Joint Account, unknown gender": "joint account, unknown gender"},
    "PVASTATE": {"P": "PVA state"},
}


# Scores and ratings with no words per level: numbers, as the source ships them (CLEAN-14).
SCORES = ["INCOME", "WEALTH1", "WEALTH2"]


class PvaRevenuePredictionKddcup98(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a lapsed donor give to a veterans' charity in response to its renewal mailing?",
        use_case=(
            "Before a renewal mailing, the Paralyzed Veterans of America decides which lapsed donors to mail, where "
            "each piece costs $0.68 (KDD Cup 1998)."
        ),
        row=(
            "One lapsed donor (last gift 13 to 24 months earlier) who received the June 1997 renewal mailing, from "
            "the KDD Cup's learning and validation files."
        ),
        predicted="Whether the donor responded with a gift (5.1% of the whole mailing did).",
        known=(
            "The donor's age, sex, household and neighbourhood data bought from outside sources, interests, how the "
            "donor was acquired, and up to 24 months of mailing and giving history (dates, amounts, recency, "
            "frequency and amount codes)."
        ),
        split="Random donors of the same mailing, as in the KDD Cup's learning and validation files.",
        changes=(
            "We predict whether a donor gives instead of the amount given (the KDD Cup scored the mailing's net "
            "revenue) and drop the amount."
        ),
        fit="approximate",
        fit_reason=(
            "Everything the model sees precedes the mailing, but one mailing stands in for the next: training and "
            "test donors come from the same June 1997 mailing, whereas the charity would score the next one."
        ),
    )

    # Dataset
    unique_name = "pva_revenue_prediction_kddcup98"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://kdd.ics.uci.edu/databases/kddcup98/kddcup98.html",  # Rel 10.24432/C5401H
            license=None,  # Unclear but has usage instruction that do not count as license (?)
            year="1998",
            bibtex=r"""
                @misc{Parsa1998KDDCup1998,
                  author = {Ismail Parsa},
                  title  = {KDD Cup 1998},
                  year   = {1998},
                  howpublished = {\url{https://kdd.ics.uci.edu/databases/kddcup98/kddcup98.html}},
                  note   = {Dataset, UCI Machine Learning Repository. DOI: 10.24432/C5401H}
                }
            """,
        ),
    )
    data_tags = ("DelayedTarget",)
    download_description = """
        wget https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98lrn.zip && unzip cup98lrn && rm cup98lrn.zip
        wget https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98val.zip && unzip cup98val && rm cup98val.zip && wget https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/valtargt.txt
        mkdir -p local-data-warehouse/pva_revenue_prediction_kddcup98 && mv cup98VAL.txt local-data-warehouse/pva_revenue_prediction_kddcup98/ && mv cup98LRN.txt local-data-warehouse/pva_revenue_prediction_kddcup98/ && mv valtargt.txt local-data-warehouse/pva_revenue_prediction_kddcup98/
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
        - DOB 0 means no birth date on file (47,677 donors): these rows stay, with DOB missing (fixed 2026-10-14; the month-00 filter had dropped them too).
        - We noticed that nan values and dtypes mismatch for NOEXCH do correlate with the target. We add these cases as their own categories.
        - We resolve the ordinal encoding and nan encoding for all columns.
        - Note, that data has a lot of features that contain data from a similar origin that was transformed into individual columns.
        - We do not decode the promotion codes across years but keep them as string columns as it would blow up the dimensionality too much otherwise.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 9 columns are ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); 2 of them decoded from the source's codes
          into its words (`CODE_LABELS`, 2026-11-01); 3 hold a state outside the scale, placed by the curator's rule
          (missing when the column has no other missing value, else the lowest level; a state that is simply not on the
          scale, such as Other, is missing); codes that mean unknown are missing (CLEAN-10).
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 2 ordered codes carry their codebook's
          words (`CODE_LABELS`), in the same order; 3 unordered codes carry their words: `AGEFLAG`, `GENDER`,
          `PVASTATE`; 3 scores with no words per level are numbers (`SCORES`): `INCOME`, `WEALTH1`, `WEALTH2`.
        - `DOMAIN_ses` (2026-11-01, CLEAN-12): the dictionary codes the neighbourhood's socio-economic status in two
          schemes, "1 = Highest SES 2 = Average SES 3 = Lowest SES (except for Urban communities, where 1 = Highest SES,
          2 = Above average SES, 3 = Below average SES, 4 = Lowest SES.)" (cup98dic.txt). Each row is read by its own
          scheme, on one line: lowest < below average < average < above average < highest. Before, urban codes 2 and 3
          (6,504 and 5,270 rows) were read as average and lowest, and code 4 had a coined label.
        - `DOMAIN_urbanicity` stays an unordered category (2026-11-05, Lennart, GitHub issue #48, CLEAN-14): the
          dictionary lists the first byte of `DOMAIN` as U=Urban, C=City, S=Suburban, T=Town, R=Rural and calls the
          field "A nominal or symbolic field" (cup98dic.txt); it does not say whether a city neighbourhood is denser
          than a suburb, so no order is imposed.
        - The target (2026-11-01, CLEAN-25): `TARGET_B` ships its classes as words (1 is the event). Binary: "Yes" is
          the event, the class that sorts second, so it is the metrics' positive class.
        - Time basis: DelayedTarget: one renewal mailing (97NK, June 1997) to lapsed donors; every field is the donor
          before June 1997 (the gift receipts of earlier promotions dated after it are blanked); the target is the
          response to that mailing, recorded for every donor by the cup's release in 1998. Every donor got the same
          mailing and its response was recorded over the same window, so no test row is later than a training row and
          the random split is IID. The date columns are the donors' shared past, not a time to split on (random split
          kept, 2026-11-12, Andrej): every row is about the one promotion date (191,758 of the cup's 191,779 donors
          mailed in June 1997, 21 in April 1997; all of them lapsed). The 23 earlier promotions, June 1994 to June 1996,
          are columns, not rows: each reached 60,000 to 188,000 of these donors, in changing mail types, with responses
          of 0.02% to 36%, and of 0.02% to 0.9% from March 1996 on, because the cup selected donors who had stopped
          giving; their responses are a selected past, not training mailings. Within the target mailing the response
          falls from 6.1% (recruited 1986) to 3.3% (recruited 1996) while the gift of those who gave rises from $12.95
          to $19.80, and it rises from 3.6% (last gift early 1995) to 9.9% (1997). A split on these donor dates tests
          new kinds of donors, not a later mailing: on the donors recruited from 1995 on, a model trained on the earlier
          recruits earns $0.046 per test donor, against $0.083 for the same donors under random folds and $0.041 for
          mailing everyone (untuned LightGBM). The cup's learning and validation files agree (5.08% and 5.06% gave). Not
          tested: the next mailing.
    """

    # Task
    target = "TARGET_B"
    problem_type = "binary_classification"
    metric = Metric.stand_in(
        "roc_auc",
        original="Net revenue of the mailing: sum over mailed donors of (TARGET_D - 0.68)",
        reason="The original scores the donation amount (TARGET_D) and a mail/no-mail decision; our task is changed to the binary response and TARGET_D is dropped. Closest computable stand-in is roc_auc on response.",
        reference="https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98doc.txt",
        definition="Original: total net profit = sum_{i mailed}(donation_i - $0.68), mailing decided by the model; stand-in: ROC AUC of TARGET_B (responded).",
    )

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
        # the dictionary's two schemes for the second byte: urban neighbourhoods have four levels, the others three
        ses_map = {"1": "Highest SES", "2": "Average SES", "3": "Lowest SES"}
        urban_ses_map = {"1": "Highest SES", "2": "Above average SES", "3": "Below average SES", "4": "Lowest SES"}
        # Handle DOB (YYMM; 0 = no birth date on file)
        dob = df["DOB"].fillna(0).astype(int)
        df = df[(dob == 0) | (dob % 100 != 0)]  # drop the 2 rows with month 00; DOB 0 becomes missing below
        df["DOB"] = df["DOB"].replace(0, np.nan)
        dob_nan_mask = df["DOB"].isna()
        df.loc[dob_nan_mask, "DOB"] = 0
        df["DOB"] = df["DOB"].astype(float).astype(int).astype("string").str.zfill(4)
        df.loc[dob_nan_mask, "DOB"] = np.nan
        df["DOB"] = "19" + df["DOB"]  # "19YYMM", parsed as a date in `_feature_types`
        df["FISTDATE"] = df["FISTDATE"].replace(0, np.nan)
        for col in DATE_COLUMNS:
            nan_mask = df[col].isna()
            df.loc[nan_mask, col] = 1111
            df[col] = "19" + df[col].astype(int).astype("string")  # "19YYMM", parsed as a date in `_feature_types`
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
        df["DOMAIN_ses"] = b2.map(ses_map).where(b1 != "U", b2.map(urban_ses_map))
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
        for col in INTEREST_COLUMNS:
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
        for c in STRING_COLUMNS:
            df[c] = df[c].replace(" ", np.nan)
        # codes outside a scale that mean unknown, and states outside it placed as missing (CLEAN-10,
        # CLEAN-14): don't know, refused, not asked, other
        df = set_missing(
            df,
            {
                "MDMAUD_recency": ["Not applicable"],
                "MDMAUD_frequency": ["Not applicable"],
                "MDMAUD_amount": ["Not applicable"],
            },
        )
        # codes the codebook leaves without words, or a question that did not apply (CLEAN-10)
        df = set_missing(df, {"AGEFLAG": [" "], "GENDER": ["A", "C", "Unknown"]})
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        # scores with no words per level are numbers (CLEAN-14)
        df[SCORES] = df[SCORES].astype("object").apply(pd.to_numeric)
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
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
                *INTEREST_COLUMNS,
            ],
            string=STRING_COLUMNS,
            # Make pd Dates (unclear if best preprocessing is not just int as in original data but this way we have the correct metadata of the col)
            datetime=dict.fromkeys(["DOB", *DATE_COLUMNS], "%Y%m"),
        )
