"""Curated dataset definition for `emscad` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, anonymize_ids

CONTACT_PATTERN = r"#(?:EMAIL|PHONE|URL)_[0-9a-f]{8,}#"
"""EMSCAD masks e-mails, phones and URLs as ``#(EMAIL|PHONE|URL)_Keyed_SHA2#``, so one hash is one contact."""


def poster_groups(df: pd.DataFrame) -> pd.Series:
    """One group per poster: ads linked by the same company profile or a poster-specific masked contact.

    Two ads are in the same group when they share the exact (non-empty) ``company_profile``, or a masked e-mail, phone
    or URL that occurs within at most one company profile (contacts shared across several companies are generic, e.g.
    job-board links, and are not used). The group is named after the smallest ``job_id`` in it, hashed.
    """
    parent = list(range(len(df)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        parent[find(i)] = find(j)

    profile = df["company_profile"].fillna("").astype(str).str.strip().to_numpy()
    first: dict[str, int] = {}
    for i, text in enumerate(profile):
        if text:
            union(i, first.setdefault(text, i))
    text_cols = ["company_profile", "description", "requirements", "benefits", "title"]
    text = df[text_cols].fillna("").astype(str).agg(" ".join, axis=1)
    rows: dict[str, list[int]] = {}
    for i, tokens in enumerate(text.str.findall(CONTACT_PATTERN)):
        for token in set(tokens):
            rows.setdefault(token, []).append(i)
    for idx in rows.values():
        if len(idx) > 1 and len({profile[i] for i in idx} - {""}) <= 1:
            for j in idx[1:]:
                union(idx[0], j)
    roots = pd.Series([find(i) for i in range(len(df))], index=df.index)
    first_job = df["job_id"].groupby(roots).transform("min")
    return anonymize_ids(first_job.astype(str))


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

        - The dataset was collected from 2012 to 2014. But the data contains no feature to identify the time of a sample. So we can expect that some bias from temporal leakage. Ads of the same poster are grouped (see below).
        - Following the original paper, we drop all duplicates (when ignoring the job_id column) to avoid data leakage. We also drop reposts, which the paper describes as "fraudsters can quickly and repeatedly try to post the same job ad in identical or different locations" (Sec. 5): rows identical in every field except job_id and location (1,343 more rows, 115 of them fraudulent).
        - The labels were assigned per client ("based on client's suspicious activity on the system, false contact or company information, candidate complaints and periodic meticulous analysis of the clientele", Sec. 5), and ads of the same client appear several times. We group them exactly, without similarity thresholds: same non-empty company_profile (the client's own company text; none of the 1,708 profiles mixes labels), or a shared masked e-mail, phone or URL that occurs within at most one company profile (contacts shared by several companies, e.g. job-board links, are generic and not used). This gives about 4,500 groups (largest 539 ads, a legitimate recruiter); ads without a profile or shared contact are their own group. Random splits scored ROC AUC 0.99 because the model recognises known clients; grouped splits score about 0.93 (leak audit 2026-09-24, re-checked 2026-09-30).
        - Residual: about 335 ads without profile or shared contact still have a near-identical text (TF-IDF cosine >= 0.95) in another group, likely lightly edited reposts. Dropping them at thresholds 0.95 to 0.7 did not change the grouped AUC measurably, so we keep them.
        - The data has a location description, we do not resolve it lat/longitude but leave it to the pipelines.
        - The salary range has several weird quirks. It contains data either in the thousands, or is missing the "k" to denote thousands. Moreover, it contains empty or 0-0 entries. The column might contain yearly salary, hourly salary, or one-time payment. Finally, for some jobs, the column contains a date (e.g. "Oct-20"). We keep the column as complex as it is. We add one column that contains the maximum salary parsed from the text and we only keep salary values above 50k as valid values to create a numerical feature for differences in the larger ranges.
        - We removed job listings with non english texts (138 rows).
        - We do not subsample the data, as a result, the data is heavily imbalanced.
        - We found no relation of job_id with a timestamp and even found cases where a lower job_id has a description claiming to be a job from 2014 (so the end of the collection period). Thus, we do dropped job_id as it does not contain any signal.
    """

    # Task
    target = "fraudulent"
    problem_type = "binary_classification"
    group_on = "poster_group"
    group_labels = "per_sample"
    accepted_check_warnings = {
        "dataset_pure_feature_value": "Large legitimate clients (e.g. one company profile with 539 ads) and their "
        "locations, departments and industries are all legitimate at a 95% base rate; the grouped split keeps each "
        "client on one side, so these values do not leak across the split.",
    }

    # Splits
    splits_comment = """
        Grouped splits on poster_group: all ads of one poster (same company profile or poster-specific masked contact)
        stay on one side, so the benchmark measures detecting fraud from posters not seen in training. The labels were
        assigned per client (Vidros et al. 2017, Sec. 5), and ads of a known client share its label. The original paper
        uses a random 10-fold CV on a balanced subset.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "fake_job_postings.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Drop duplicates
        df = df[~df.drop(columns=["job_id"]).duplicated(keep="last")]
        # Drop reposts: "fraudsters can quickly and repeatedly try to post the same job ad in identical or different
        # locations" (Vidros et al. 2017, Sec. 5), i.e. rows identical in every field except job_id and location
        df = df[~df.drop(columns=["job_id", "location"]).duplicated(keep="last")]
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
            nan_mask = df[c].isna() | (df[c].astype(str).str.strip() == "")  # " " and "\xa0" mean missing
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        # After our preprocessing, there is just one entry without a description, so we drop it as well.
        df = df[~df["description"].isna()].reset_index(drop=True)
        # Group ads of the same poster (used for the splits only)
        df["poster_group"] = poster_groups(df)
        df = df.drop(columns=["job_id"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "poster_group",
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
