"""Curated dataset definition for `website_phishing` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class WebsitePhishing(AbstractCuratedDataset):
    # Dataset
    unique_name = "website_phishing"
    year = "2014"
    domain = "technology & internet"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5B301"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/website_phishing/ && wget -P local-data-warehouse/website_phishing/ https://archive.ics.uci.edu/static/public/379/website+phishing.zip && unzip local-data-warehouse/website_phishing/website+phishing.zip && rm local-data-warehouse/website_phishing/website+phishing.zip
    """
    bibtex = """
        @article{abdelhamid2014phishing,
          title={Phishing detection based associative classification data mining},
          author={Abdelhamid, Neda and Ayesh, Aladdin and Thabtah, Fadi},
          journal={Expert Systems with Applications},
          volume={41},
          number={13},
          pages={5948--5959},
          year={2014},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - We reversed the ordinal encoding of the original data.
        - We renamed the target feature to be more meaningful.
        - Anomaly: the data has many duplicates (~50%).
    """

    # Task
    target = "WebsiteType"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(f"{raw_dir}/PhishingData.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # According to description this is the encoding for all features and the target
        encoding_map = {"1": "Legitimate", "0": "Suspicious", "-1": "Phishy"}
        df = df.map(lambda x: encoding_map[x])
        target_feature = "WebsiteType"
        df = df.rename(columns={"Result": target_feature})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "SFH",
                "popUpWidnow",
                "SSLfinal_State",
                "Request_URL",
                "URL_of_Anchor",
                "web_traffic",
                "URL_Length",
                "age_of_domain",
                "having_IP_Address",
            ],
        )
