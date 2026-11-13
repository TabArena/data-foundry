"""Curated dataset definition for `thyroid_discordant_archive` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

# The 29 attributes of thyroid0387.names, in file order.
COLUMNS = [
    "age",
    "sex",
    "on_thyroxine",
    "query_on_thyroxine",
    "on_antithyroid_medication",
    "sick",
    "pregnant",
    "thyroid_surgery",
    "I131_treatment",
    "query_hypothyroid",
    "query_hyperthyroid",
    "lithium",
    "goitre",
    "tumor",
    "hypopituitary",
    "psych",
    "TSH_measured",
    "TSH",
    "T3_measured",
    "T3",
    "TT4_measured",
    "TT4",
    "T4U_measured",
    "T4U",
    "FTI_measured",
    "FTI",
    "TBG_measured",
    "TBG",
    "referral_source",
]
# One record: the 29 values, the diagnosis codes and the record id, "<values>,<codes>[<id>]".
RECORD = re.compile(r"^(?P<values>.*),(?P<codes>[^,\[]*)\[(?P<id>\d{9})\]$")


class ThyroidDiscordantArchive(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Would the laboratory comment a patient's thyroid test results as discordant?",
        use_case=(
            "For example, a laboratory's interpretation system flags thyroid results that the laboratory would "
            "comment as discordant, so that a specialist reviews them before the report goes out."
        ),
        row=(
            "One request for thyroid tests at the Garvan Institute in Sydney, August 1984 to January 1987 (9,162 "
            "requests after removing 10 repeated entries); a patient tested more than once appears more than once."
        ),
        predicted=("Whether the report's comment includes 'discordant assay results', code R of the archive (2.2%)."),
        known=(
            "The request date, age, sex, medication (thyroxine, antithyroid drugs, lithium), conditions and history "
            "(pregnancy, illness, thyroid surgery, radioiodine treatment, goitre, tumour), the referring doctor's "
            "suspicion of an under- or overactive thyroid, and six thyroid test results with flags for which were "
            "measured."
        ),
        split=(
            "Later requests: three test windows of four months from February 1986 to January 1987, each trained on "
            "all earlier requests."
        ),
        changes=(
            "We build the label from the archive's diagnosis codes, take the request date from the record id and "
            "drop the referral source."
        ),
        fit="approximate",
        fit_reason=(
            "The label is the laboratory's own comment on these same test results, so the model reproduces that "
            "reading rather than predicting an outcome; the archive does not say who wrote the comments. The data are "
            "from 1984 to 1987."
        ),
    )

    # Dataset
    unique_name = "thyroid_discordant_archive"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5D010",
            license="CC BY 4.0",
            year="1987",
            bibtex="""
                @misc{quinlan1986thyroid,
                  author={Quinlan, Ross},
                  title={{Thyroid Disease}},
                  year={1986},
                  howpublished={UCI Machine Learning Repository},
                  doi={10.24432/C5D010}
                }
                @inproceedings{quinlan1987inductive,
                  title={Inductive knowledge acquisition: a case study},
                  author={Quinlan, John Ross and Compton, Paul J and Horn, KA and Lazarus, Leslie},
                  booktitle={Proceedings of the Second Australian Conference on Applications of expert systems},
                  pages={137--156},
                  year={1987}
                }
            """,
        ),
    )
    download_description = """
        We download thyroid0387.data, the Garvan Institute archive, and its documentation from the UCI Thyroid Disease files (the same zip as thyroid_discordant's dis.data).

        wget https://archive.ics.uci.edu/static/public/102/thyroid+disease.zip && unzip thyroid+disease.zip thyroid0387.data thyroid0387.names && rm thyroid+disease.zip && mkdir -p local-data-warehouse/thyroid_discordant_archive && mv thyroid0387.data thyroid0387.names local-data-warehouse/thyroid_discordant_archive/
    """
    curation_comments = """
        We start with thyroid0387.data from the UCI Thyroid Disease files: "the latest version of an archive of thyroid diagnoses obtained from the Garvan Institute, consisting of 9172 records from 1984 to early 1987" (thyroid0387.names). Each record is one request: 29 values, the report's diagnosis codes and a record id.

        - Prediction point: the laboratory has the test results of a request and writes the report; the label is the comment in that report, known at once, so the windows leave no gap.
        - The label: `discordant` is "Yes" when the diagnosis codes include R, "discordant assay results" (thyroid0387.names), 197 of 9,172 records: 196 "R" and one "D|R" ("consistent with D, but more likely R"; secondary toxic). This is the label of thyroid_discordant (UCI's dis file), built from an earlier version of the same archive: its 58 positives are R records here (2026-11-11); the one "D|R" record is negative in the dis file, where an earlier comment stood (allhypo labels it secondary hypothyroid).
        - The request date is the record id's first six digits (YYMMDD), 1984-08-01 to 1987-01-19; the ids follow the dates. The archive holds almost no requests in February 1985 (1), January 1986 (2), May 1986 (2) and June 1986 (1).
        - We drop the record id (date and sequence number), the other diagnosis codes (the same report as the label) and `referral_source`, as thyroid_discordant does: it marks where a request came from.
        - We keep `TBG` and `TBG_measured`, constant in the dis file: TBG is measured for 341 requests (298 without any other test), none with code R.
        - Impossible ages (455, 65511, 65512, 65526) are set to missing and the rows stay (CLEAN-11).
        - We drop 10 later records whose 28 values and label repeat an earlier record (two of them one day apart, one with the next record id), keeping the first.
        - The `_measured` flags repeat which test values are missing; we keep them, as thyroid_discordant does.
        - Note: T3 is ordered for 79-88% of requests in each quarter up to September 1985 and for 32-75% after, and the share with code R is 4.4% from June to September 1986 against 1.7-2.1% in the other periods: the windows test these shifts.
        - Note: the archive has no patient id, so a patient tested again (a follow-up on thyroxine, say) can sit on both sides of a cutoff; this is the patient's own history under a temporal split.
    """

    # Task
    target = "discordant"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Quinlan et al. (1987) score the error rate (accuracy) of decision trees on earlier versions of this "
            "archive; no publication defines a task or metric for the discordant comment over time, and accuracy is "
            "uninformative at about 2% positives"
        ),
    )

    # Splits
    splits_comment = """
        Three test windows of four months of request dates, newest first: October 1986 to January 1987 (the end of the
        archive), June to September 1986 and February to May 1986; each trains on every earlier request (87%, 73% and
        61% of the rows). The windows hold 1,215, 1,230 and 1,145 requests with 25, 54 and 24 discordant results. They
        follow option C of thyroid_discordant's issue 4 (train on 1984-1985; test on the first half of 1986, its third
        quarter, and its fourth quarter with January 1987), as four-month windows, which one declaration can express:
        the archive holds only 2 requests in January 1986 and 1 in June 1986, none discordant, so the windows differ
        from option C's by those three requests (January trains the oldest window, June is tested with the summer)
        and keep its positives. An IID task of this size would get more folds; more windows would cut the 103 test
        positives into a handful each.
    """
    temporal = Temporal(
        on="request_date",
        splits=TemporalSplits(window=4, unit="months", cutoffs=("1986-02-01", "1986-06-01", "1986-10-01")),
    )
    accepted_check_warnings = {
        "dataset_pure_feature_value": "on_thyroxine and TSH_measured are on the request, before the report comment: "
        "a patient on thyroxine or without a TSH result is rarely commented as discordant (1 of 1,239 and 1 of 834); "
        "no leak",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        rows = []
        for line in (raw_dir / "thyroid0387.data").read_text().splitlines():
            if not line.strip():
                continue
            match = RECORD.match(line)
            assert match, f"unparsed record: {line!r}"
            rows.append([*match["values"].split(","), match["codes"], match["id"]])
        df = pd.DataFrame(rows, columns=[*COLUMNS, "diagnoses", "record_id"])
        return df.replace("?", np.nan)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.sort_values("record_id", kind="stable").reset_index(drop=True)
        # the request date: the record id's first six digits (YYMMDD)
        df["request_date"] = pd.to_datetime("19" + df["record_id"].str[:6], format="%Y%m%d")
        # the label: code R ("discordant assay results") among the report's diagnosis codes
        df[self.target] = np.where(df["diagnoses"].str.contains("R", regex=False), "Yes", "No")
        # the record id, the rest of the report and where the request came from (notes)
        df = drop_columns(df, ["record_id", "diagnoses", "referral_source"])
        for column in ["age", "TSH", "T3", "TT4", "T4U", "FTI", "TBG"]:
            df[column] = pd.to_numeric(df[column])
        # impossible ages: missing, the rows stay (CLEAN-11)
        df.loc[df["age"] > 120, "age"] = np.nan
        # repeated entries: the same 28 values and label on a later record (keep the first)
        df = df.drop_duplicates(subset=[c for c in df.columns if c != "request_date"]).reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "sex",
                "on_thyroxine",
                "query_on_thyroxine",
                "on_antithyroid_medication",
                "sick",
                "pregnant",
                "thyroid_surgery",
                "I131_treatment",
                "query_hypothyroid",
                "query_hyperthyroid",
                "lithium",
                "goitre",
                "tumor",
                "hypopituitary",
                "psych",
                "TSH_measured",
                "T3_measured",
                "TT4_measured",
                "T4U_measured",
                "FTI_measured",
                "TBG_measured",
            ],
            datetime={"request_date": "%Y-%m-%d"},
        )
