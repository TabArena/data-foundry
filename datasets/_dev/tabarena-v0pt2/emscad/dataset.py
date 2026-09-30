"""Curated dataset definition for `emscad` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class Emscad(AbstractCuratedDataset):
    # Dataset
    unique_name = "emscad"
    year = "2014"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction/data"
    license = (
        "CC0: Public Domain"  # from Kaggle, paper does not state anything, website is down to check -> so maybe None...
    )
    data_tags = ("Spatial",)
    download_description = """
        The original website (http://icsdweb.aegean.gr/emscad) has been down for a while.
        Thus, we us an alternative source from Kaggle (https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction/data).
        There is also an additional alternative source from Kaggle (https://www.kaggle.com/datasets/amruthjithrajvr/recruitment-scam).

        kaggle datasets download -d shivamb/real-or-fake-fake-jobposting-prediction -f fake_job_postings.csv && unzip fake_job_postings.csv.zip fake_job_postings.csv&& rm fake_job_postings.csv.zip
        mkdir -p local-data-warehouse/emscad && mv fake_job_postings.csv local-data-warehouse/emscad
    """
    bibtex = """
        @article{vidros2017automatic,
          title={Automatic detection of online recruitment frauds: Characteristics, methods, and a public dataset},
          author={Vidros, Sokratis and Kolias, Constantinos and Kambourakis, Georgios and Akoglu, Leman},
          journal={Future Internet},
          volume={9},
          number={1},
          pages={6},
          year={2017},
          publisher={MDPI}
        }
    """
    curation_comments = """
        We have no access to the original state and the data already contains some preprocessed features.
        The paper describes them in more detail as well in Table 2.

        In the original paper, the authors subsampled the data to have 450 fraudulent and 450 non-fraudulent samples.
        No details are given on how the subsampling was done. Moreover, duplicates were skipped, but no details are given on how duplicates were identified.

        - The dataset was collected from 2012 to 2014. But the data contains no feature to identify the time of a sample. So we can expect that some bias from temporal leakage. Moreover, the data might contain multiple job postings from the same fraudster, which would need to be grouped, but we cannot identify them from the data.
        - Following the original paper, we drop all duplicates (when ignoring the job_id column) to avoid data leakage.
        - The data has a location description, we do not resolve it lat/longitude but leave it to the pipelines.
        - The salary range has several weird quirks. It contains data either in the thousands, or is missing the "k" to denote thousands. Moreover, it contains empty or 0-0 entries. The column might contain yearly salary, hourly salary, or one-time payment. Finally, for some jobs, the column contains a date (e.g. "Oct-20"). We keep the column as complex as it is. We add one column that contains the maximum salary parsed from the text and we only keep salary values above 50k as valid values to create a numerical feature for differences in the larger ranges.
        - We removed job listings with non english texts (138 rows).
        - We do not subsample the data, as a result, the data is heavily imbalanced.
        - We found no relation of job_id with a timestamp and even found cases where a lower job_id has a description claiming to be a job from 2014 (so the end of the collection period). Thus, we do dropped job_id as it does not contain any signal.
    """

    # Task
    target = "fraudulent"
    problem_type = "binary_classification"

    # Splits
    splits_comment = """
        In the original paper, 10-fold CV is used. We follow our default suggestions in the case of IID.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "fake_job_postings.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Drop duplicates
        df = df[~df.drop(columns=["job_id"]).duplicated(keep="last")]
        # Get max salary proxy for larger ranges
        s = df["salary_range"].astype(str).str.strip()
        invalid_mask = df["salary_range"].isna() | (s == "") | (s == "0-0")
        ranges = s.str.split("-", expand=True)
        min_vals, max_vals = ranges[0], ranges[1]
        is_not_salary_range = (
            pd.to_numeric(max_vals, errors="coerce").isna() | pd.to_numeric(min_vals, errors="coerce").isna()
        )  # remove dates
        not_above_50_k = ~(pd.to_numeric(max_vals, errors="coerce") >= 50_000)
        df["salary_range_max"] = pd.to_numeric(max_vals, errors="coerce")
        df.loc[invalid_mask | is_not_salary_range | not_above_50_k, "salary_range_max"] = np.nan
        # from langdetect import detect, LangDetectException
        #
        # def is_not_english(text: str) -> bool:
        #     try:
        #         return detect(text) != "en"
        #     except LangDetectException:
        #         # Raised for very short or ambiguous text
        #         return False
        # df["is_english_description"] = df["description"].astype(str).apply(lambda x: not is_not_english(x))
        # bad_filter_list = [
        #     # Missing, faulty or, Lorem ipsum description...
        #     1243,
        #     3031,
        #     7613,
        #     5557,
        #     11078,
        #     11894,
        #     12190,
        #     13530,
        # ]
        # print(list(df[(~df["is_english_description"]) & (~df["description"].isna()) & (df["description"] != "Sales Executive") & (~df["job_id"].isin(bad_filter_list))]["job_id"]))
        # Output from the above
        filter_non_en_job = [
            543,
            550,
            557,
            687,
            936,
            986,
            1174,
            1558,
            1667,
            1689,
            1794,
            1831,
            1922,
            2351,
            2384,
            2424,
            2474,
            2677,
            2788,
            2857,
            2929,
            2967,
            2986,
            3126,
            3132,
            3139,
            3156,
            3169,
            3566,
            3576,
            3702,
            3764,
            3856,
            3952,
            3993,
            4157,
            4185,
            4193,
            4315,
            4362,
            4371,
            4401,
            4812,
            4825,
            4867,
            5058,
            5198,
            5274,
            5632,
            5637,
            5651,
            5693,
            5724,
            5931,
            6023,
            6096,
            6169,
            6184,
            6269,
            6284,
            6438,
            6445,
            6573,
            6587,
            6699,
            6752,
            6853,
            6988,
            7025,
            7112,
            7212,
            7549,
            7679,
            7849,
            7881,
            8066,
            8106,
            8214,
            8355,
            8365,
            8397,
            8615,
            8719,
            8791,
            8895,
            9216,
            9393,
            9413,
            9965,
            10450,
            10468,
            10557,
            10570,
            10661,
            11075,
            11314,
            11320,
            11383,
            11419,
            11424,
            11426,
            11427,
            11446,
            11449,
            11463,
            11464,
            11536,
            11631,
            11748,
            11958,
            12231,
            12395,
            12683,
            12973,
            13016,
            13301,
            13474,
            13476,
            13551,
            13696,
            14021,
            14131,
            14333,
            14911,
            15185,
            15410,
            16343,
            16500,
            16586,
            16608,
            16691,
            17034,
            17047,
            17148,
            17226,
            17328,
            17357,
            17781,
        ]
        df = df[~df["job_id"].isin(filter_non_en_job)]
        as_string_col = [
            "title",
            "location",
            "department",
            "salary_range",
            # HTML fragments
            "company_profile",
            "description",
            "requirements",
            "benefits",
        ]
        for c in as_string_col:
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        df = df.drop(columns=["job_id"]).reset_index(drop=True)
        # After our preprocessing, there is just one entry without a description, so we drop it as well.
        df = df[~df["description"].isna()].reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "telecommuting",
                "has_company_logo",
                "has_questions",
                "employment_type",
                "required_experience",
                "required_education",
                "industry",
                "function",
            ],
        )


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
