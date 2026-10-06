"""Curated dataset definition for `homesite_quote_conversion` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, object_columns


class HomesiteQuoteConversion(AbstractCuratedDataset):
    # Dataset
    unique_name = "homesite_quote_conversion"
    year = "2015"
    domain = "insurance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/homesite-quote-conversion"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized",)
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c homesite-quote-conversion -f train.csv.zip && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/homesite_quote_conversion && mv train.csv local-data-warehouse/homesite_quote_conversion/
    """
    bibtex = r"""
        @misc{Darrel2015HomesiteQuoteConversion,
          author = {Darrel and Stephen D. Stayton and Will Cukierski},
          title  = {Homesite Quote Conversion},
          year   = {2015},
          howpublished = {\url{https://kaggle.com/competitions/homesite-quote-conversion}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized, so feature meanings are unknown.
        - The data contains decoded spatial information.
        - We fix the Field10 column to be integer instead of string with ',' characters.
        - We convert the Original_Quote_Date to datetime.
        - IMPORTANT NOTE: this dataset was used as a non-IID task by TabRed. We keep it as an IID task, because: (A) the Kaggle discussions regarding validation converged on doing IID cross-validation, (B) based on our understanding of the prediction task IID seems most appropriate, and (C) the official test data on Kaggle contains timestamps from the same period as the train. Concluding from this, we think that treating the data as IID is appropriate and that potential temporal leakage is insignificant (due to A and B) or intended (due to C).
        - We drop the ID number and constant columns.
        - We replace -1 with NaN (https://www.kaggle.com/competitions/homesite-quote-conversion/discussion/17417) and keep ordinals as numeric features following TabRed's preprocessing.
        - Potential leak, kept on purpose: "PropertyField37" x "PersonalField12" looks like a status code that may be filled after the quote. (Y, 1-4) holds 20,008 quotes of which 99.3% converted (40.6% of all conversions), while (Y, 5) holds 54,769 quotes of which 0.14% converted. Dropping both fields lowers LightGBM ROC AUC from 0.965 to 0.915. We keep them because the fields are anonymised and the meaning cannot be checked, Homesite set the competition up with them (the official test data has the same fields), and the Kaggle discussions do not flag them. Revisit if the fields are ever documented.
    """

    # Task
    target = "QuoteConversion_Flag"
    problem_type = "binary_classification"

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
                # Constant columns
                "GeographicField10A",
                "GeographicField10B",
            ]
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=object_columns(df),
            datetime=["Original_Quote_Date"],
        )
