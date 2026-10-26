"""Curated dataset definition for `phiusil_phishing` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary, drop_columns

TEMPLATE_URL = r"https://www\.[^/?#]+"
"""The form of every legitimate URL in the file: a ranked domain written as ``https://www.<host>``, without a path."""

MIN_LEGITIMATE_LINES = 102
"""The smallest ``LineOfCode`` of a legitimate page; no legitimate page in the file has fewer lines."""

URL_FEATURES = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "TLD",
    "CharContinuationRate",
    "TLDLegitimateProb",
    "URLCharProb",
    "TLDLength",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "IsHTTPS",
]
"""The kept features the source computed from the URL."""

PAGE_FEATURES = [
    "LineOfCode",
    "LargestLineLength",
    "HasTitle",
    "HasFavicon",
    "Robots",
    "IsResponsive",
    "NoOfURLRedirect",
    "NoOfSelfRedirect",
    "HasDescription",
    "NoOfPopup",
    "NoOfiFrame",
    "HasExternalFormSubmit",
    "HasSocialNet",
    "HasSubmitButton",
    "HasHiddenFields",
    "HasPasswordField",
    "Bank",
    "Pay",
    "Crypto",
    "HasCopyrightInfo",
    "NoOfImage",
    "NoOfCSS",
    "NoOfJS",
    "NoOfSelfRef",
    "NoOfEmptyRef",
    "NoOfExternalRef",
]
"""The kept features the source computed from the fetched page."""


def title_rewrite(url: str, *, cut: bool) -> str:
    """The string the source's ``Title`` column holds for a page with a title: the URL rewritten, not the title.

    Lower case, without the scheme and ``www.``, without the last character where the source cut it (``URLLength``
    is ``len(URL) - 1``), without dots and slashes, and without the host's TLD as read from that string.
    """
    text = re.sub(r"^www\.", "", re.sub(r"^https?://", "", url.lower()))
    text = text[:-1] if cut else text
    host = re.split(r"[/?#]", text, maxsplit=1)[0]
    tld = host.rsplit(".", 1)[1] if "." in host else ""
    text = text.replace(".", "").replace("/", "")
    return text.replace(tld, "") if tld else text


def overlap_score(title: str, target: str) -> float:
    """The source's title-match score: 100 times the summed length of the words of ``title`` found in ``target``,
    divided by the length of ``target`` and capped at 100.
    """
    if not target:
        return 0.0
    return min(100.0, 100.0 * sum(len(word) for word in title.split() if word in target) / len(target))


class PhiusilPhishing(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is the web page behind this URL a phishing page?",
        use_case=(
            "A phishing detector fetches the page of a URL and decides whether it is phishing before the user opens it."
        ),
        row=(
            "One URL with features of its fetched page: 134,850 legitimate and 100,520 phishing URLs, published in "
            "2023 and collected mostly in 2023 (Mendeley Data page)."
        ),
        predicted="Whether the URL is phishing or legitimate (43% phishing).",
        known=(
            "The URL text and its top-level domain, counts and ratios computed from the URL, and features of the page"
            " such as its lines, title, links, forms, password fields, images and scripts."
        ),
        split=(
            "Random URLs; hosts are not held out, as a deployed detector meets both known and new hosts. There is no "
            "time column."
        ),
        changes=(
            "We drop columns that encode how the rows were collected: the file name, a similarity to the list the "
            "legitimate rows came from, and a title rebuilt from the URL with the scores computed from it."
        ),
        fit="approximate",
        fit_reason=(
            "The sampling replaces the task: negatives are ranked homepages only (every legitimate URL is the bare "
            "homepage of a ranked site), and half the positives are pages fetched after takedown, so a fixed rule "
            "reaches ROC AUC 0.9998. The curation notes recommend excluding the dataset."
        ),
    )

    # Dataset
    unique_name = "phiusil_phishing"
    year = "2023"
    domain = "technology & internet"
    source = "Other"
    source_url = "https://doi.org/10.17632/shwpxscxy2.1"
    license = "CC BY 4.0"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        The authors published the file on Mendeley Data (doi:10.17632/shwpxscxy2; version 1 of 2023-08-29 and
        version 2 of 2023-11-15 hold the same file) and donated it to the UCI repository (dataset 967, 2024-03-03).
        The UCI zip holds the identical file (sha256 a236549cd369cd80bd478ff8e1779cbf44c58d5c3f79f7a51a1adbed7d06d1c6).

        mkdir -p local-data-warehouse/phiusil_phishing
        wget -P local-data-warehouse/phiusil_phishing/ https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip
        unzip local-data-warehouse/phiusil_phishing/phiusiil+phishing+url+dataset.zip -d local-data-warehouse/phiusil_phishing/
        rm local-data-warehouse/phiusil_phishing/phiusiil+phishing+url+dataset.zip
    """
    bibtex = r"""
        @article{prasad2024phiusiil,
          title={PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning},
          author={Prasad, Arvind and Chandra, Shalini},
          journal={Computers \& Security},
          volume={136},
          pages={103545},
          year={2024},
          publisher={Elsevier},
          doi={10.1016/j.cose.2023.103545}
        }
    """
    curation_comments = """
        We start with PhiUSIIL_Phishing_URL_Dataset.csv from the UCI repository (dataset 967). The paywalled paper (Prasad & Chandra 2024) was not read; how the classes were built is read from the data.

        - Prediction point: a detector fetches the page of a URL and decides whether it is phishing before the user opens it. The phishing pages here were fetched after the URLs were listed (shared-pages bullet).
        - Target: UCI says "Label 1 corresponds to a legitimate URL, label 0 to a phishing URL", and the abstract's 134,850 legitimate URLs are the rows with label 1, which we map to Legitimate.
        - Anomaly: the two classes were collected in different forms (first decision). The fixed rule "the URL is https://www.<host> without a path and the page has at least 102 lines" calls all 134,850 legitimate rows and 38 of the 100,520 phishing rows legitimate (third decision), so no column drop or subset avoids the artifacts. We recommend excluding the dataset as Data Quality Issue, not Trivial: no single feature or fixed rule matches the models fold by fold.
        - Dropped as construction artifacts (second decision): FILENAME (an id; its form, a rank or a feed's file name, gives the label away), URLSimilarityIndex (by its values, the similarity to the list the legitimate rows came from) and Title, which is the URL rewritten (`title_rewrite`), not the page title.
        - Dropped as computed from Title: DomainTitleMatchScore and URLTitleMatchScore, its overlap with the domain and the URL (`overlap_score`).
        - Dropped as a copy: Domain, the authority part of URL. URL, the input the detector classifies, stays as a string; TLD is a categorical.
        - Construction artifacts that stay: every feature family separates the classes (fourth decision); dropping columns would not help, as the URL features alone reach ROC AUC 0.9989 and the page features 0.99994.
        - Anomaly, shared pages: 50.5% of the phishing rows and no legitimate row carry one of 115 pages found on at least 100 rows and several hosts, such as Firebase Hosting's page for an address without a site (fifth decision). A page template is not an entity that new URLs lack, so no split changes this.
        - LEAK-13 departure, acceptable only because the dataset is excluded: URLLength is len(URL) - 1 for every legitimate row and 52,090 phishing rows and len(URL) for 48,428, so the URL counts and ratios use a string cut more often in one class. Adding len(URL) moves the URL features from ROC AUC 0.99893 to 0.99895; recompute len(URL) and the URL counts and ratios from URL if the dataset ever ships.
        - Kept: TLDLegitimateProb (a TLD's share in an outside list of about 10M domains) and URLCharProb (possibly computed from this file's legitimate rows). Without both, ROC AUC stays 1.0000.
        - Duplicates: 425 URLs occur twice (all phishing), as two fetches of the same URL (every pair differs in URLLength, 37 in LineOfCode); we keep the first copy in file order. Near-copies that differ in the scheme, a leading "www." or a trailing slash stay.
        - Note: hosts with several rows are phishing hosts, by construction, apart from 54 hosts (112 rows) that hold both classes, and 43 homepages are listed both as Legitimate and as Phishing (sixth decision).
    """

    # Task
    target = "label"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="The first publication reports several classification scores (accuracy, precision, recall, F1) for its framework without one task metric; no competition. Not verified in the full text (paywalled)."
    )
    accepted_check_warnings = {
        "dataset_identifier_column": "URL is the address the detector classifies, the input of the task, not a row "
        "id; it is unique per row because the 425 repeated URLs are dropped.",
        "dataset_missing_value_label": "TLD 'na' is Namibia's country code (19 legitimate rows such as "
        "https://www.bipa.na), not a missing value.",
        "dataset_pure_feature_value": "These values come from how the two classes were collected (curation_comments): "
        "every legitimate URL is https://www.<host> without a path, so NoOfSubDomain = 0, NoOfQMarkInURL = 1 and "
        "IsHTTPS = 0 occur in phishing rows only, and HasSocialNet = 1 is nearly pure (107,146 legitimate and 511 "
        "phishing rows), as it marks the full homepages of ranked domains. "
        "Dropping them would not help: the URL keeps the template and the page features alone reach ROC AUC 0.99994. "
        "We recommend excluding the dataset for this reason.",
    }

    # Splits
    splits_comment = """
        Default splits (IID). A deployed detector meets URLs on hosts it has seen (shared hosting, known phishing hosts) and on new ones, so hosts are not held out. Holding them out changes little (3 folds, seed 0): LightGBM on the numeric features and TLD reaches ROC AUC 1.0000 with log loss 0.0003 on a random split, 0.0003 grouped by host and 0.0004 grouped by registered domain; the URL text alone (character 3- to 5-grams, logistic regression) reaches ROC AUC 0.9991 and log loss 0.013 on a random split, 0.9990 and 0.014 grouped by host, and 0.9989 and 0.015 grouped by registered domain. The v1 notebook put every row of a host with several rows into train, which removed from the test folds every URL on such a host (path-based shared hosting such as ipfs.io and docs.google.com, and phishing hosts with several URLs); we do not. There is no time column, although phishing changes over time (tag ForcedIIDFromTemporal): only the phishing rows carry an order (feed ids), so no temporal split can be built.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "PhiUSIIL_Phishing_URL_Dataset.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 425 URLs are listed twice by the feeds (all phishing): keep the first copy in file order
        df = df[~df["URL"].duplicated(keep="first")]
        # UCI: "Label 1 corresponds to a legitimate URL, label 0 to a phishing URL"
        df[self.target] = df[self.target].map({1: "Legitimate", 0: "Phishing"})
        # construction artifacts (the rank or feed file id, the similarity to the list the legitimate rows were taken
        # from, a URL-derived string in place of the page title and the two scores computed from it) and a copy (the
        # authority part of URL)
        return drop_columns(
            df,
            ["FILENAME", "URLSimilarityIndex", "Title", "DomainTitleMatchScore", "URLTitleMatchScore", "Domain"],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the yes/no features are categorical (CLEAN-14); the counts NoOfURLRedirect and NoOfSelfRedirect stay
        # numeric although only 0 and 1 occur
        flags = [
            "IsDomainIP",
            "HasObfuscation",
            "IsHTTPS",
            "HasTitle",
            "HasFavicon",
            "Robots",
            "IsResponsive",
            "HasDescription",
            "HasExternalFormSubmit",
            "HasSocialNet",
            "HasSubmitButton",
            "HasHiddenFields",
            "HasPasswordField",
            "Bank",
            "Pay",
            "Crypto",
            "HasCopyrightInfo",
        ]
        return FeatureTypes(categorical=["TLD", *flags], string=["URL"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        from sklearn.metrics import roc_auc_score

        kept = raw[~raw["URL"].duplicated(keep="first")]  # the shipped rows, with the columns _clean drops
        legit = kept["label"].eq(1)
        url, tld, title = kept["URL"], kept["TLD"], kept["Title"]
        cut = url.str.len() - kept["URLLength"]
        has_title = kept["HasTitle"].eq(1)
        host = url.str.extract(r"^[a-zA-Z]+://(?:[^/?#@]*@)?([^/?#:]+)")[0].str.lower()
        page_id = kept.groupby(PAGE_FEATURES).ngroup()
        page_rows = page_id.map(page_id.value_counts())
        page_hosts = host.groupby(page_id).transform("nunique")
        shared_page = page_rows.ge(100) & page_hosts.ge(2)

        def by_class(mask: pd.Series, within: pd.Series | None = None) -> list[str]:
            within = pd.Series(True, index=mask.index) if within is None else within
            return [f"{mask[legit & within].mean():.2%}", f"{mask[~legit & within].mean():.2%}"]

        rank_id = pd.to_numeric(kept["FILENAME"].str.extract(r"^(\d+)\.txt$")[0], errors="coerce")
        construction = pd.DataFrame(
            {
                "URL is https://www.<host> without a path": by_class(url.str.fullmatch(TEMPLATE_URL)),
                "FILENAME is a number below 1,000,000 (a rank)": by_class(rank_id.lt(1_000_000)),
                "URLSimilarityIndex = 100": by_class(kept["URLSimilarityIndex"].eq(100)),
                "IsHTTPS = 1": by_class(kept["IsHTTPS"].eq(1)),
                "URLLength = len(URL) - 1 (last character cut)": by_class(cut.eq(1)),
                f"LineOfCode >= {MIN_LEGITIMATE_LINES}": by_class(kept["LineOfCode"].ge(MIN_LEGITIMATE_LINES)),
                "LineOfCode <= 10": by_class(kept["LineOfCode"].le(10)),
                "HasTitle = 1": by_class(has_title),
                "page found on >= 100 rows and several hosts": by_class(shared_page),
            },
            index=["Legitimate", "Phishing"],
        ).T

        rewritten = pd.Series(
            [title_rewrite(u, cut=c == 1) == t for u, c, t in zip(url, cut, title, strict=True)], index=kept.index
        )
        domain_part = [
            re.sub(r"^www\.", "", d.lower()).removesuffix(f".{t}") for d, t in zip(kept["Domain"], tld, strict=True)
        ]
        url_part = [
            re.sub(r"^www\.", "", re.sub(r"^https?://", "", u.lower())).replace(f".{t}", "").replace("/", "")
            for u, t in zip(url, tld, strict=True)
        ]
        domain_score = [overlap_score(t, d) for t, d in zip(title, domain_part, strict=True)]
        url_score = [overlap_score(t, u) for t, u in zip(title, url_part, strict=True)]
        recomputed = pd.DataFrame(
            {
                "Title is '0' (rows with HasTitle = 0)": by_class(title.eq("0"), ~has_title),
                "Title is the URL rewritten (rows with HasTitle = 1)": by_class(rewritten, has_title),
                "DomainTitleMatchScore = overlap of Title with the domain": by_class(
                    pd.Series(np.isclose(domain_score, kept["DomainTitleMatchScore"], atol=1e-3), index=kept.index)
                ),
                "URLTitleMatchScore = overlap of Title with the URL": by_class(
                    pd.Series(np.isclose(url_score, kept["URLTitleMatchScore"], atol=1e-3), index=kept.index)
                ),
            },
            index=["Legitimate", "Phishing"],
        ).T

        rule = df["URL"].str.fullmatch(TEMPLATE_URL) & df["LineOfCode"].ge(MIN_LEGITIMATE_LINES)
        rule_table = pd.crosstab(
            rule.map({True: "legitimate", False: "phishing"}), df[self.target], rownames=["fixed rule says"]
        )

        is_legit = df[self.target].eq("Legitimate")
        numeric = [c for c in df.columns if c not in (self.target, "URL", "TLD")]
        auc = pd.Series({c: roc_auc_score(is_legit, df[c].astype(float)) for c in numeric})
        single = auc.where(auc >= 0.5, 1 - auc).rename("ROC AUC alone").sort_values(ascending=False, kind="stable")
        family = pd.Series(["URL" if c in URL_FEATURES else "page" for c in single.index], index=single.index)
        single_table = pd.DataFrame({"family": family, "ROC AUC alone": single.round(4)}).head(15)

        suffix = host.str.extract(r"([^.]+\.[^.]+)$")[0].fillna(host)
        pages = pd.DataFrame({"page": page_id, "host": host, "suffix": suffix, "legit": legit})
        largest = (
            pages.groupby("page")
            .agg(rows=("host", "size"), legitimate=("legit", "sum"), hosts=("host", "nunique"))
            .sort_values("rows", ascending=False, kind="stable")
            .head(8)
        )
        first = kept.groupby(page_id)[["LineOfCode", "LargestLineLength", "HasTitle"]].first()
        common_hosts = {
            p: ", ".join(
                f"{s} {n:,}"
                for s, n in pages[pages["page"].eq(p)]
                .groupby("suffix")
                .size()
                .sort_values(ascending=False, kind="stable")
                .head(2)
                .items()
            )
            for p in largest.index
        }
        largest_table = largest.join(first).assign(**{"most common hosts": pd.Series(common_hosts)})
        largest_table.index = [f"page {i}" for i in range(1, len(largest_table) + 1)]
        n_shared = page_rows.ge(2)

        domain = kept["Domain"].str.lower()
        sizes = kept.groupby(domain)["label"].agg(["size", "nunique", "mean"])
        repeated = sizes[sizes["size"] > 1]
        mixed = repeated[repeated["nunique"] > 1]
        same_url = url.str.replace(r"^[a-zA-Z]+://(www\.)?", "", regex=True).str.rstrip("/")
        both_labels = kept.groupby(same_url)["label"].nunique().gt(1)
        hosts = pd.Series(
            {
                "hosts": len(sizes),
                "hosts with several rows": len(repeated),
                "rows on hosts with several rows": int(repeated["size"].sum()),
                "of these hosts, only phishing rows": int((repeated["mean"] == 0).sum()),
                "of these hosts, only legitimate rows": int((repeated["mean"] == 1).sum()),
                "of these hosts, both classes": len(mixed),
                "rows on hosts with both classes": int(mixed["size"].sum()),
                "URLs listed under both labels (up to scheme, www. and a final /)": int(both_labels.sum()),
            },
            name="count",
        )
        return [
            Decision(
                "The two classes were collected in different forms",
                "Legitimate rows are ranked domains written as https://www.<host> (FILENAME is the rank), with pages "
                f"of at least {MIN_LEGITIMATE_LINES} lines; phishing rows are feed URLs, many with empty, stub or "
                "error pages. The share of the kept rows with each property, by class.",
                construction,
            ),
            Decision(
                "Dropped: FILENAME, URLSimilarityIndex, Title and the two title-match scores",
                "FILENAME and URLSimilarityIndex: see the first table. Title is not the page title but the URL "
                "rewritten (title_rewrite in dataset.py), in both classes; the two title-match scores are the "
                "overlap of that rewrite with the domain and with the URL (overlap_score). The share of the kept rows "
                "each rule reproduces, by class.",
                recomputed,
            ),
            Decision(
                "No subset of the file avoids the artifacts",
                "A fixed rule on two kept properties, without training: the URL is https://www.<host> without a path "
                f"and the page has at least {MIN_LEGITIMATE_LINES} lines.",
                rule_table,
            ),
            Decision(
                "Every feature family separates the classes",
                "ROC AUC of each kept numeric feature alone (from ranks, on the shipped rows), the 15 strongest.",
                single_table,
            ),
            Decision(
                "Half of the phishing rows carry a page shared across many hosts",
                f"{int((n_shared & ~legit).sum()):,} of the {int((~legit).sum()):,} phishing rows share all "
                f"{len(PAGE_FEATURES)} page features with another row, against {int((n_shared & legit).sum()):,} of "
                f"the {int(legit.sum()):,} legitimate rows; {int((shared_page & ~legit).sum()):,} phishing rows and "
                f"{int((shared_page & legit).sum()):,} legitimate rows carry one of "
                f"{int(page_id[shared_page].nunique()):,} pages found on at least 100 rows and several hosts, and "
                f"{int((shared_page & kept['HasPasswordField'].eq(1)).sum()):,} of those rows have a password field. "
                "The largest pages below; page 1 is the page Firebase Hosting serves for an address without a site "
                "(its only two intact titles read 'site not found').",
                largest_table,
            ),
            Decision(
                "IID split, hosts not held out",
                "Hosts with several rows are phishing hosts, apart from the hosts that hold both classes (table); a "
                "detector meets known and new hosts, and a "
                "host-grouped split gives the same score (splits comment). Hosts are the authority part of the URL. "
                "The last row counts homepages listed once as Legitimate and once as Phishing (curation_comments).",
                hosts,
            ),
        ]
