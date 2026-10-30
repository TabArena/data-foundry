"""Curated dataset definition for `website_phishing` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "popUpWidnow": ["-1", "0", "1"],
    "SSLfinal_State": ["-1", "0", "1"],
    "Request_URL": ["-1", "0", "1"],
    "URL_of_Anchor": ["-1", "0", "1"],
    "web_traffic": ["-1", "0", "1"],
    "URL_Length": ["-1", "0", "1"],
}


class WebsitePhishing(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is this website a phishing site or a legitimate one?",
        use_case=(
            "For example, a browser's anti-phishing filter rates a site when a user opens it, to warn the user or "
            "block the page."
        ),
        row=(
            "One website: phishing sites from the PhishTank archive, legitimate ones from Yahoo and starting-point "
            "directories (1,250 sites; period not stated)."
        ),
        predicted="Whether the site is a phishing site (56%) or a legitimate one (44%), by the list it came from.",
        known=(
            "Nine signals of the page and its URL, each coded -1, 0 or 1 by the donors: the form handler, pop-up "
            "windows, the SSL certificate, where requested objects and anchor links point, the site's traffic, URL "
            "length, domain age, and an IP address in the URL. Which code means legitimate is not clear from the data."
        ),
        split=(
            "Random sites, so the test data stands for other sites from the same lists; about half the rows are exact "
            "duplicates, so identical rows can sit on both sides."
        ),
        changes=(
            "We dropped the 103 sites the donors rated suspicious, a third class judged from the same nine signals "
            "rather than from the list a site came from, so the task is phishing against legitimate. The signals keep "
            "their raw codes instead of the words legitimate, suspicious and phishy, whose direction does not match "
            "the data."
        ),
        fit="approximate",
        fit_reason=(
            "Phishing and legitimate sites come from separate lists rather than from the sites users open, so the "
            "class mix (56% phishing) is not what a filter meets. The signals themselves are known at a visit."
        ),
    )

    # Dataset
    unique_name = "website_phishing"
    year = "2016"
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
        - Binary since 2026-10-14 (Lennart): phishing (`Result` -1, 702 sites) against legitimate (1, 548 sites). We
          drop the 103 suspicious sites (0): the data page says such a site "can be either phishy or legitimate", and
          LightGBM tells them apart from the rest by the nine signals alone with ROC AUC 0.987 (record, 2026-10-14).
        - The class counts match the data page (548 legitimate, 702 phishing), so the target follows its coding: 1
          legitimate, 0 suspicious, -1 phishy.
        - The features keep their raw codes -1, 0 and 1 as categories. The page gives them the same coding, but in
          practice their direction is undocumented: under it, 7 of the 9 point away from the label (91% of phishing
          sites have SFH rated legitimate), and `having_IP_Address` takes only 0 and 1.
        - We renamed the target to `is_phishing` (Yes / No).
        - Anomaly: about half the rows are exact duplicates (47% of the 1,250 rows).
        - Ordinal scales (2026-10-30, CLEAN-14): 6 columns typed as ordered categories in the order of the source's
          codebook (`ORDINAL_LEVELS`).
    """

    accepted_check_warnings = {
        "dataset_pure_feature_value": (
            "All 167 sites with popUpWidnow = 1 are phishing (in the 3-class data 15 were suspicious, none legitimate). "
            "Under the documented coding 1 means legitimate, the same reversed direction as the other signals, so it is "
            "a page property, not a leak (Lennart, 2026-10-14)."
        ),
    }

    # Task
    target = "is_phishing"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Abdelhamid, Ayesh & Thabtah 2014 compare associative classifiers by 3-class accuracy; we dropped the suspicious class (binary since 2026-10-14), so the task changed (MET-2), and no costs are fixed. roc_auc is the binary fallback.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(f"{raw_dir}/PhishingData.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # Result: 1 legitimate, 0 suspicious, -1 phishy (data page). The suspicious class is dropped; the features
        # keep their raw codes.
        df = raw[raw["Result"] != "0"].rename(columns={"Result": self.target})
        df[self.target] = df[self.target].map({"-1": "Yes", "1": "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
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
