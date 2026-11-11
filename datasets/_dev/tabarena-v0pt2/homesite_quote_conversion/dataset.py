"""Curated dataset definition for `homesite_quote_conversion` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

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
    decode,
    object_columns,
)


class HomesiteQuoteConversion(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a customer buy the home-insurance policy they were quoted?",
        use_case=(
            "Homesite, a home insurer, estimates which quotes will turn into purchases, to judge the effect of price "
            "changes and keep the customer mix it wants (the competition's stated aim)."
        ),
        row="One quote Homesite gave a customer for a home-insurance policy (260,753 quotes).",
        predicted="Whether the customer bought the quoted policy (19% did).",
        known=(
            "The quote date and about 300 anonymised fields on the coverage, the sale, the customer, the property and"
            " its area."
        ),
        split=(
            "The test data is the most recent quotes, in nine windows of one month (September 2014 to May 2015, the "
            "last to the 18th), each trained on every earlier quote, with no gap: a purchase is recorded within days."
        ),
        changes=(
            "We split by quote date instead of the competition's random split, whose test quotes cover the same "
            "dates, as TabReD does; seven anonymised fields that mark the purchase are dropped."
        ),
        fit="direct",
        fit_reason=(
            "The split by quote date mirrors Homesite scoring the quotes it issues next. Anonymised fields that read "
            "like a status filled in after the quote are dropped (one combination held 99.3% to 99.8% buyers), with "
            "the fields marking the same quotes, until no large group is 95% buyers: no model scoring a quote before "
            "the customer decides could know the purchase that precisely."
        ),
    )

    # Dataset
    unique_name = "homesite_quote_conversion"
    domain = "insurance"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/homesite-quote-conversion",
            license="Kaggle Competition Rules",
            year="2015",
            bibtex=r"""
                @misc{Darrel2015HomesiteQuoteConversion,
                  author = {Darrel and Stephen D. Stayton and Will Cukierski},
                  title  = {Homesite Quote Conversion},
                  year   = {2015},
                  howpublished = {\url{https://kaggle.com/competitions/homesite-quote-conversion}},
                  note   = {Kaggle competition}
                }
            """,
        ),
    )
    data_tags = ("Anonymized",)
    accepted_check_warnings = {
        "dataset_constant_column": (
            "Twelve presence flags: 25 or missing (the source's -1, set to missing), filled in about 2.5% of the "
            "quotes; the buyers' share differs between filled and missing (GeographicField14A 4.4% against 19.1%)."
        ),
    }
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c homesite-quote-conversion -f train.csv.zip && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/homesite_quote_conversion && mv train.csv local-data-warehouse/homesite_quote_conversion/
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized, so feature meanings are unknown.
        - The data contains decoded spatial information.
        - We fix the Field10 column to be integer instead of string with ',' characters.
        - We convert the Original_Quote_Date to datetime.
        - Split by quote date (2026-11-11, Andrej; SPLIT-6), as TabReD does, instead of the competition's random split, whose test quotes cover the same dates: Homesite scores the quotes it issues next, and conversion drifts (15.3% to 19.9% a month in the test windows). Nine monthly windows back from May 2015 (the last a partial month, to the 18th), each trained on every earlier quote (at least 70.7% of the rows). Before the drops of the fields below, untuned LightGBM scored ROC AUC 0.956 on average over the windows (0.943 to 0.963) against 0.964 on random folds; nearly all of the gap is the test months themselves (training on as many random quotes adds 0.0017).
        - No gap (2026-11-11, Andrej; SPLIT-10): the last weekdays of the release convert as before (18 May 2015: 19.3%), so purchases are recorded within days, and the source names no horizon. After the drops, a gap of 7 days changes the mean ROC AUC from 0.9043 to 0.9040, 30 days to 0.9025 (untuned LightGBM, nine windows).
        - We drop the ID number and constant columns (PropertyField6 is 0 in every row), and set the blank level of GeographicField63 (2 quotes) to missing.
        - We replace -1 with NaN (https://www.kaggle.com/competitions/homesite-quote-conversion/discussion/17417) and keep ordinals as numeric features following TabRed's preprocessing.
        - We drop "PropertyField37" and "PersonalField12" (2026-11-11, Andrej; LEAK-10): together they read like a status code filled in after the quote. With PropertyField37 = Y, PersonalField12 codes 1 to 3 converted at 99.3% to 99.8% (19,934 quotes) and code 5 at 0.14% (54,769 quotes, all but one of the code-5 quotes); with N, codes 1 to 3 convert at 13.6% to 15.5%, below the base rate of 18.75%. The pattern holds in every quarter 2013 to 2015. No field can tell a customer's purchase before the decision with that precision, so the pair is treated as recorded after it, although the fields are anonymised and Kaggle's test file carries them. Dropping both lowers untuned LightGBM ROC AUC from 0.965 to 0.952 (3 random folds, 2026-11-11). PersonalField9 = 3 and missing PersonalField10A/B mark the same quotes as code 5 (54,785 quotes, 0.14% converted), so they are dropped too (2026-11-11, Andrej): 0.916 without all five. Other levels with almost no buyers stay (Field7 = 23, PropertyField29 = 0): none marks the code-5 quotes as a whole and none has a near-certain buyer side; a quote that cannot be bought is known when it is issued.
        - We drop "PersonalField2" and "PersonalField13" (2026-11-11, Andrej; LEAK-10): after the five fields above, PersonalField1 = 1 with PersonalField2 = 0 still marked 7,266 quotes at 98.0% bought (4,987 outside the dropped buyer codes at 97.1%, 97% to 100% in every quarter), and PersonalField13 = 1 marked 2,092 at 97.8%. Each field on its own is graded (PersonalField1 = 1: 21.0% against 12.9%), so the fewest fields that leave no group of at least 300 quotes converting at 95% or more (a depth-6 tree on all quotes) are dropped, and PersonalField1 stays. Mean ROC AUC over the nine windows (untuned LightGBM): 0.956 with every field, 0.904 without the five fields, 0.898 without the seven. The near-zero side stays (PropertyField29 filled, Field7 = 23, PersonalField4A/B or PropertyField38 missing, PropertyField18 = 0: 66,506 quotes, 12 buyers), as a quote that cannot be bought is known when it is issued. Half the quotes (130,844) carry no near-certain marker either way; on them the model scores 0.859.
        - Potential leak, kept on purpose: SalesField5 is the strongest field (35% of the model's gain; on the quotes no near-certain marker settles, level 5 converts at 6.7% (71,454 quotes), levels 2 to 4 at 30.5% to 32.5%, the same in 2013, 2014 and 2015; 0.765 alone). It may record the sales channel, known at the quote, or a sales stage the customer reached, partly after it; the anonymisation hides which. It is graded, not near-certain, so it stays under the rule for untestable anonymised fields (2026-11-11, Andrej; LEAK-38); without it the mean ROC AUC is 0.879. Revisit if Homesite's field descriptions surface.
        - The target (2026-11-01, CLEAN-25): `QuoteConversion_Flag` ships its classes as words (1 is the event). Binary:
          "Yes" is the event, the class that sorts second, so it is the metrics' positive class.
    """

    # Task
    target = "QuoteConversion_Flag"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC (area under the ROC curve)",
        reference="https://www.kaggle.com/competitions/homesite-quote-conversion/overview/evaluation",
        definition="Area under the ROC curve between predicted probability of QuoteConversion_Flag and the observed label.",
    )

    temporal = Temporal(
        on="Original_Quote_Date",
        splits=TemporalSplits(window=1, unit="months", n_windows=9, min_train_fraction=0.5),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["Field10"] = df["Field10"].astype("string").str.replace(",", "").astype(int)
        df["Original_Quote_Date"] = pd.to_datetime(df["Original_Quote_Date"])
        ordinal_fields_with_nan_mask = [
            "CoverageField1A",
            "CoverageField1B",
            "CoverageField11A",
            "CoverageField11B",
            "SalesField2A",
            "SalesField2B",
            "PersonalField4A",
            "PersonalField4B",
            "PersonalField10A",
            "PersonalField10B",
            "PropertyField1A",
            "PropertyField1B",
            "PropertyField2A",
            "PropertyField11A",
            "PropertyField16A",
            "PropertyField16B",
            "PropertyField21A",
            "PropertyField21B",
            "PropertyField24A",
            "PropertyField24B",
            "PropertyField26A",
            "PropertyField26B",
            "PropertyField39A",
            "PropertyField39B",
            "GeographicField1A",
            "GeographicField1B",
            "GeographicField2A",
            "GeographicField2B",
            "GeographicField5A",
            "GeographicField5B",
            "GeographicField6A",
            "GeographicField6B",
            "GeographicField7A",
            "GeographicField7B",
            "GeographicField8A",
            "GeographicField8B",
            "GeographicField9A",
            "GeographicField9B",
            "GeographicField10A",
            "GeographicField10B",
            "GeographicField11A",
            "GeographicField11B",
            "GeographicField12A",
            "GeographicField12B",
            "GeographicField13A",
            "GeographicField13B",
            "GeographicField14A",
            "GeographicField14B",
            "GeographicField15A",
            "GeographicField15B",
            "GeographicField16A",
            "GeographicField16B",
            "GeographicField17A",
            "GeographicField17B",
            "GeographicField18A",
            "GeographicField18B",
            "GeographicField19A",
            "GeographicField19B",
            "GeographicField20A",
            "GeographicField20B",
            "GeographicField21A",
            "GeographicField21B",
            "GeographicField22A",
            "GeographicField22B",
            "GeographicField23A",
            "GeographicField23B",
            "GeographicField24A",
            "GeographicField24B",
            "GeographicField25A",
            "GeographicField25B",
            "GeographicField26A",
            "GeographicField26B",
            "GeographicField27A",
            "GeographicField27B",
            "GeographicField28A",
            "GeographicField28B",
            "GeographicField29A",
            "GeographicField29B",
            "GeographicField30A",
            "GeographicField30B",
            "GeographicField31A",
            "GeographicField31B",
            "GeographicField32A",
            "GeographicField32B",
            "GeographicField33A",
            "GeographicField33B",
            "GeographicField34A",
            "GeographicField34B",
            "GeographicField35A",
            "GeographicField35B",
            "GeographicField36A",
            "GeographicField36B",
            "GeographicField37A",
            "GeographicField37B",
            "GeographicField38A",
            "GeographicField38B",
            "GeographicField39A",
            "GeographicField39B",
            "GeographicField40A",
            "GeographicField40B",
            "GeographicField41A",
            "GeographicField41B",
            "GeographicField42A",
            "GeographicField42B",
            "GeographicField43A",
            "GeographicField43B",
            "GeographicField44A",
            "GeographicField44B",
            "GeographicField45A",
            "GeographicField45B",
            "GeographicField46A",
            "GeographicField46B",
            "GeographicField47A",
            "GeographicField47B",
            "GeographicField48A",
            "GeographicField48B",
            "GeographicField49A",
            "GeographicField49B",
            "GeographicField50A",
            "GeographicField50B",
            "GeographicField51A",
            "GeographicField51B",
            "GeographicField52A",
            "GeographicField52B",
            "GeographicField53A",
            "GeographicField53B",
            "GeographicField54A",
            "GeographicField54B",
            "GeographicField55A",
            "GeographicField55B",
            "GeographicField56A",
            "GeographicField56B",
            "GeographicField57A",
            "GeographicField57B",
            "GeographicField58A",
            "GeographicField58B",
            "GeographicField59A",
            "GeographicField59B",
            "GeographicField60A",
            "GeographicField60B",
            "GeographicField61A",
            "GeographicField61B",
            "GeographicField62A",
            "GeographicField62B",
        ]
        df[ordinal_fields_with_nan_mask] = df[ordinal_fields_with_nan_mask].replace(-1, np.nan)
        df = df.drop(
            columns=[
                "QuoteNumber",  # ID
                # a status-like pair recorded after the quote (LEAK-10; 2026-11-11, Andrej)
                "PropertyField37",
                "PersonalField12",
                # the same status's non-buyer code on other fields (PersonalField9 = 3, PersonalField10A/B missing)
                "PersonalField9",
                "PersonalField10A",
                "PersonalField10B",
                # a near-certain buyer group after the five above (PersonalField1 = 1 with PersonalField2 = 0: 98.0%;
                # PersonalField13 = 1: 97.8%); the fewest fields leaving no group of 300 quotes at 95% or more
                "PersonalField2",
                "PersonalField13",
                # constant (0 in every row; CLEAN-5)
                "PropertyField6",
                # Constant columns
                "GeographicField10A",
                "GeographicField10B",
            ]
        )
        # a blank level (2 quotes) is a missing value (CLEAN-10)
        df["GeographicField63"] = df["GeographicField63"].replace(" ", np.nan)
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=object_columns(df),
            datetime=["Original_Quote_Date"],
        )
