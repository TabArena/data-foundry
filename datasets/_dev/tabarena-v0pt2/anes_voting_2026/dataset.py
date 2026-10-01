"""Curated dataset definition for `anes_voting_2026` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


class AnesVoting2026(AbstractCuratedDataset):
    # Dataset
    unique_name = "anes_voting_2026"
    year = "2026"
    domain = "social science"
    source = "Other"
    source_url = "https://electionstudies.org/data-center/anes-time-series-cumulative-data-file/"
    license = "Use for research or statistical purposes"
    download_description = """
        No automatic download supported!

        mkdir -p local-data-warehouse/anes_voting_2026/

        Download the February 5, 2026 CSV version, unzip and place the .csv in local-data-warehouse/anes_voting_2026/anes_timeseries_cdf_csv_20260205.csv.
    """
    bibtex = r"""
        @misc{anes2026timeseries,
            author       = {{American National Election Studies}},
            title        = {{ANES Time Series Cumulative Data File [dataset and documentation]}},
            year         = {2026},
            month        = feb,
            note         = {February 5, 2026 version},
            howpublished = {\url{https://www.electionstudies.org}}
        }
    """
    curation_comments = """
        - We remove all samples with missing pre-election data, missing post-election data or a missing target.
        - We drop 327 that are missing from the last 9 years, which will be used for the test splits.
        - We drop all columns with questions that appear only in one year.
        - The question columns partially stem from post-election interviews. However, there is no simple way to tell which is post-election. We therefore drop all questions for which "no Post IW" or "no post data" is listed as a reason for missing values in the codebook (February 5, 2026 version), and VCF1005, which is built from the post-election House vote ("R Voted" / "R did not vote"). Some additional questions are dropped based on common sense.
        - We encode gender as a categorical variable, because Other was introduced in 2016. However there are very few of these samples. This would actually require split-specific preprocessing.
        - For all features, we assign " " as missing values. Most features have additional types of missingness with own codes. We keep them as categories. That means NA only is assigned if a question was missing in a survey.
        - We transform only high-cardinality (>10) numeric features to numeric, and leave all other ordinal features as categorical, since they all include at least one value that is out-of-order (e.g., "Don't know", "Refused", "Not applicable", "Other", etc.).
        - Although there are several ways to further preprocess features, we leave the preprocessing minimal to enable the development of models that can handle even complex preprocessing on their own.
        - Note: Alternative target could be constructed using who the candidate voted for (VCF0704). This could be a multi-class target with [Democrat, Republican, Other Party, Did not vote, Voted but unknown who]. However, the last category is less useful to predict, and might introduce problems. We therefore stick to predicting whether someone voted or not.
        - Note: While the data was also used in the TableShift benchmark, we define an entirely different task, with a temporal split and more features.
        - Note: Some information is represented across multiple columns, e.g.,  ['VCF0009x', 'VCF0009y', 'VCF0009z', 'VCF0010x', 'VCF0010y', 'VCF0010z', 'VCF0011x', 'VCF0011y', 'VCF0011z'] all correspond to weight. We keep all of these columns, even though some might be redundant, because we want to keep the data as close to the original as possible leaving the challenge to the model.
        - Note: Ideally, we would select different feature sets per data split, depending on feature availability. However, for simplicity, we just keep all features.
        - Note: We considered keeping the unique respondent identifier in the data, because otherwise models that are able to reconstruct this information would unfairly benefit. However, for now we drop the identifier since it is not a desirable predictive feature for the given task, because the goal is generalization to the population, not memorizing individual behavior.
    """

    # Task
    target = "VCF0702"
    problem_type = "binary_classification"
    time_on = "VCF0004"

    # Splits
    splits_comment = "We use each of the last 9 years once as test data, using all prior data as train data."
    time_horizon = 1
    time_horizon_unit = "years"
    temporal_splits = TemporalSplits(window=1, unit="unique", n_windows=9)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "anes_timeseries_cdf_csv_20260205.csv", low_memory=False)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.loc[df["VCF0013"] == 1]
        df = df.loc[df["VCF0014"] == 1]
        df = df.loc[df["VCF0702"].apply(lambda x: x in ["1", "2"])]  # only keep those with a valid target
        # Drop if last 9 years have only one unique value
        nunique_questions = df.groupby("VCF0004").nunique()
        df = df.drop(columns=nunique_questions.columns[(nunique_questions.iloc[-9:] > 1).sum() == 0])
        # Drop if a question appears only in one year
        nunique_questions = df.groupby("VCF0004").nunique()
        df = df.drop(columns=nunique_questions.columns[(nunique_questions > 1).sum() <= 2])
        drop_cols = [
            # "Version", # constant (already filtered based on availability)
            # "VCF0013","VCF0014", # pre-election and post-election availability (already filtered based on availability)
            "VCF0006",
            "VCF0006a",  # unique respondent identifiers, (might keep "VCF0006")
            # "VCF0012",  # Survey related features (already filtered based on availability)
            "VCF0015a",
            "VCF0015b",
            "VCF0016",
            "VCF0017",
            "VCF0072a",
            "VCF0009x",
            "VCF0009y",
            "VCF0009z",
            "VCF0010x",
            "VCF0010y",
            "VCF0010z",
            "VCF0011x",
            "VCF0011y",
            "VCF0011z",
            "VCF0018a",
            "VCF0050a",
            "VCF0070a",
            "VCF0071a",
            "VCF0071c",  # Survey related features
            "VCF0438",
            "VCF0443",
            "VCF0445",
            "VCF0447",
            "VCF0448",
            "VCF0471",
            "VCF0472",
            "VCF9007",  # too year specific
            "VCF0704",  # alternative targets
            # POST-election interview questions (selected by title and description)
            "VCF0071b",
            "VCF0071d",
            "VCF0072b",
            "VCF9999",
            "VCF0018b",
            "VCF0050b",
            "VCF0015b",
            "VCF0070b",
            "VCF0703",
            "VCF0704a",
            "VCF0705",
            "VCF0706",
            "VCF0707",
            "VCF0708",
            "VCF0709",
            "VCF0710",
            "VCF0712",
            "VCF0717",
            "VCF0718",
            "VCF0719",
            "VCF0720",
            "VCF0721",
            "VCF0723",
            "VCF0723a",
            "VCF0724",
            "VCF0725",
            "VCF0726",
            "VCF0727",
            "VCF0728",
            "VCF0729",
            "VCF0731",
            "VCF0733",
            "VCF0734",
            "VCF0735",  # post
            "VCF1014",
        ]
        df = df.drop(columns=drop_cols)
        # POST-election interview questions (selected by whether "no Post IW" is listed as a reason for missing)
        no_post_election_NA_filter = [
            "VCF0128",
            "VCF0129",
            "VCF0203",
            "VCF0204",
            "VCF0205",
            "VCF0206",
            "VCF0207",
            "VCF0208",
            "VCF0209",
            "VCF0210",
            "VCF0211",
            "VCF0212",
            "VCF0213",
            "VCF0214",
            "VCF0217",
            "VCF0219",
            "VCF0220",
            "VCF0223",
            "VCF0225",
            "VCF0226",
            "VCF0227",
            "VCF0228",
            "VCF0229",
            "VCF0231",
            "VCF0232",
            "VCF0233",
            "VCF0234",
            "VCF0253",
            "VCF0312",
            "VCF0313",
            "VCF0342",
            "VCF0343",
            "VCF0344",
            "VCF0345",
            "VCF0346",
            "VCF0347",
            "VCF0348",
            "VCF0349",
            "VCF0424",
            "VCF0425",
            "VCF0428",
            "VCF0501",
            "VCF0502",
            "VCF0502a",
            "VCF0503",
            "VCF0504",
            "VCF0508",
            "VCF0509",
            "VCF0513",
            "VCF0514",
            "VCF0517",
            "VCF0518",
            "VCF0521",
            "VCF0521a",
            "VCF0522",
            "VCF0537",
            "VCF0538",
            "VCF0541",
            "VCF0542",
            "VCF0549",
            "VCF0550",
            "VCF0604",
            "VCF0605",
            "VCF0606",
            "VCF0608",
            "VCF0609",
            "VCF0613",
            "VCF0614",
            "VCF0615",
            "VCF0619",
            "VCF0620",
            "VCF0621",
            "VCF0622",
            "VCF0624",
            "VCF0630",
            "VCF0631",
            "VCF0640",
            "VCF0648",
            "VCF0649",
            "VCF0656",
            "VCF0675",
            "VCF0700",
            "VCF0736",
            "VCF0737",
            "VCF0740",
            "VCF0741",
            "VCF0742",
            "VCF0744",
            "VCF0745",
            "VCF0748",
            "VCF0749",
            "VCF0750",
            "VCF0801",
            "VCF0803",
            "VCF0804",
            "VCF0806",
            "VCF0808",
            "VCF0809",
            "VCF0816",
            "VCF0823",
            "VCF0824",
            "VCF0826",
            "VCF0829",
            "VCF0830",
            "VCF0838",
            "VCF0846",
            "VCF0847",
            "VCF0848",
            "VCF0848a",
            "VCF0849",
            "VCF0851",
            "VCF0852",
            "VCF0853",
            "VCF0854",
            "VCF0867",
            "VCF0867a",
            "VCF0873",
            "VCF0875",
            "VCF0875b",
            "VCF0876",
            "VCF0876a",
            "VCF0877",
            "VCF0877a",
            "VCF0878",
            "VCF0879",
            "VCF0879a",
            "VCF0880",
            "VCF0880a",
            "VCF0881",
            "VCF0886",
            "VCF0887",
            "VCF0888",
            "VCF0889",
            "VCF0890",
            "VCF0891",
            "VCF0892",
            "VCF0893",
            "VCF0894",
            "VCF0900",
            "VCF0900b",
            "VCF0900c",
            "VCF0901a",
            "VCF0901b",  # DO not have "no post IW" as missing, but clearly are post-IW
            "VCF0902",
            "VCF0903",
            "VCF0904",
            "VCF0905",
            "VCF0906",
            "VCF0907",
            "VCF0908",
            "VCF0909",
            "VCF0972",
            "VCF0973",
            "VCF0974",
            "VCF0975",
            "VCF0976",
            "VCF0977",
            "VCF0978",
            "VCF0980",
            "VCF0981",
            "VCF0982",
            "VCF0983",
            "VCF0984",
            "VCF0985",
            "VCF0986",
            "VCF0987",
            "VCF0988",
            "VCF0989",
            "VCF0990",
            "VCF0991",
            "VCF0992",
            "VCF0993",
            "VCF0994",
            "VCF0995",
            "VCF0996",
            "VCF0997",
            "VCF0998",
            "VCF0999",
            "VCF1000",
            "VCF1001",
            "VCF1002",
            "VCF1003",
            "VCF1004",
            "VCF1006",
            "VCF1007",
            "VCF1008",
            "VCF1009",
            "VCF1010",
            "VCF1011",
            "VCF1012",
            "VCF1013",
            "VCF1016",
            "VCF1017",
            "VCF1018",
            "VCF1020",
            "VCF1021a",
            "VCF1021b",
            "VCF1022a",
            "VCF1022b",
            "VCF1023a",
            "VCF1023b",
            "VCF1024a",
            "VCF1024b",
            "VCF1025a",
            "VCF1025b",
            "VCF1026",
            "VCF1027a",
            "VCF1027b",
            "VCF1028a",
            "VCF1028b",
            "VCF1029a",
            "VCF1029b",
            "VCF1030a",
            "VCF1030b",
            "VCF1031a",
            "VCF1031b",
            "VCF1032",
            "VCF1033a",
            "VCF1033b",
            "VCF1034a",
            "VCF1034b",
            "VCF1035a",
            "VCF1035b",
            "VCF1036a",
            "VCF1036b",
            "VCF1037a",
            "VCF1037b",
            "VCF1038",
            "VCF1039a",
            "VCF1039b",
            "VCF1040a",
            "VCF1040b",
            "VCF1041a",
            "VCF1041b",
            "VCF1042a",
            "VCF1042b",
            "VCF1043a",
            "VCF1043b",
            "VCF9004",
            "VCF9005",
            "VCF9006",
            "VCF9012",
            "VCF9013",
            "VCF9014",
            "VCF9015",
            "VCF9016",
            "VCF9017",
            "VCF9018",
            "VCF9021",
            "VCF9022",
            "VCF9023",
            "VCF9025",
            "VCF9027",
            "VCF9030",
            "VCF9030a",
            "VCF9030b",
            "VCF9030c",
            "VCF9031",
            "VCF9032",
            "VCF9036",
            "VCF9037",
            "VCF9039",
            "VCF9040",
            "VCF9041",
            "VCF9042",
            "VCF9043",
            "VCF9043a",
            "VCF9046",
            "VCF9047",
            "VCF9048",
            "VCF9049",
            "VCF9050",
            "VCF9054",
            "VCF9055",
            "VCF9056",
            "VCF9057",
            "VCF9058",
            "VCF9059",
            "VCF9060",
            "VCF9061",
            "VCF9062",
            "VCF9069",
            "VCF9075",
            "VCF9076",
            "VCF9078",
            "VCF9079",
            "VCF9080",
            "VCF9083",
            "VCF9084",
            "VCF9087",
            "VCF9088",
            "VCF9091",
            "VCF9092",
            "VCF9095",
            "VCF9096",
            "VCF9099",
            "VCF9101",
            "VCF9104",
            "VCF9106",
            "VCF9109",
            "VCF9111",
            "VCF9114",
            "VCF9116",
            "VCF9124",
            "VCF9125",
            "VCF9131",
            "VCF9132",
            "VCF9133",
        ]
        df = df.drop(columns=no_post_election_NA_filter)
        # Missed by the list above (Feb 2026 codebook, leak audit 2026-09-30): post-election interview items
        post_election_missed = [
            "VCF1005",  # "R Voted: ..." / "R did not vote": built from the post-election House vote, leaks the target
            "VCF0426",  # thermometers, missing code "no Post IW"
            "VCF0427",
            # missing code "no post data" (the newer variables' wording for "no Post IW")
            "VCF9201",
            "VCF9202",
            "VCF9203",
            "VCF9204",
            "VCF9205",
            "VCF9206",
            "VCF9207",
            "VCF9208",
            "VCF9219",
            "VCF9221",
            "VCF9223",
            "VCF9227",
            "VCF9228",
            "VCF9229",
            "VCF9230",
            "VCF9231",
            "VCF9232",
            "VCF9233",
            "VCF9234",
            "VCF9235",
            "VCF9236",
            "VCF9237",
            "VCF9240",
            "VCF9241",
            "VCF9242",
            "VCF9245",
            "VCF9246",
            "VCF9247",
            "VCF9248",
            "VCF9249",
            "VCF9250",
            "VCF9251",
            "VCF9252",
            "VCF9253",
            "VCF9254",
            "VCF9255",
            "VCF9256",
            "VCF9257",
            "VCF9258",
            "VCF9259",
            "VCF9260",
            "VCF9261",
            "VCF9262",
            "VCF9263",
            "VCF9264",
            "VCF9267",
            "VCF9268",
            "VCF9269",
            "VCF9270",
            "VCF9271",
            "VCF9272",
            "VCF9273",
            "VCF9274",
            "VCF9275",
        ]
        df = df.drop(columns=post_election_missed)
        # Assign cat features (cast here: the missing-value loop below would turn the integer codes into floats):
        cat_cols = ["VCF0110"]
        for col in cat_cols:
            df[col] = df[col].astype("category")
        # Assign missings:
        for col in df.columns:
            df.loc[df[col] == " ", col] = np.nan
        num_cols = [
            "VCF0101",
            "VCF0218",
            "VCF0222",
            "VCF0224",
            "VCF0290",
            "VCF0291",
            "VCF0412",
            "VCF0413",
            "VCF0414",
            "VCF0415",
            "VCF0429",
            "VCF1015",
            "VCF9123",
        ]
        for col in num_cols:
            df[col] = pd.to_numeric(df[col])
        df = df.sort_values(by="VCF0004").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # VCF0110 is cast in `_clean` already. Every text column as categorical would require more careful audition.
        return FeatureTypes(categorical=["VCF0110", *df.select_dtypes(include="object").columns])
