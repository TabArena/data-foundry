"""Curated dataset definition for `web_page_phishing_detection` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    TaskSummary,
    TimeBasis,
    anonymize_ids,
    decode,
    drop_columns,
)

REGISTERED_DOMAINS = "registered_domains.csv"
"""Each host of the release's URLs with its registered domain: the label left of the public suffix, by tldextract 5.4.0
with its bundled Public Suffix List and the private section left out (`TLDExtract(suffix_list_urls=(),
include_psl_private_domains=False)`), so blogspot.com or appspot.com is one domain. The extraction scripts of the
release use the same tldextract split for the domain they send to WHOIS, Openpagerank and the DNS."""

CONSTANT_COLUMNS = ["nb_or", "ratio_nullHyperlinks", "ratio_intRedirection", "ratio_intErrors", "submit_email", "sfh"]
"""Six of the 87 features hold one value (0) on every row: the release's extraction left them unset."""

# The look-ups' codes for a failed or empty query, from the release's `external_features.py`.
LOOKUP_MISSING = {
    "domain_age": [-1, -2],  # -1: the age service answered with an error; -2: it had no age for the domain
    "domain_registration_length": [-1, 0],  # -1: the WHOIS query failed; 0: WHOIS gave no expiration date
    "web_traffic": [0],  # 0: Alexa returned no rank (any failure of the query also returns 0)
}

HYPERLINK_SHARES = ["ratio_intHyperlinks", "ratio_extHyperlinks"]
"""Internal and external shares of the page's links; undefined on a page without links (`nb_hyperlinks` 0)."""

MEDIA_SHARES = ["ratio_intMedia", "ratio_extMedia"]
"""Internal and external shares of the page's media in percent (they sum to 100); both 0 on a page without media."""


class WebPagePhishingDetection(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is this web page a phishing page or a legitimate one?",
        use_case=(
            "A browser's or mail filter's phishing detector rates a page when a user opens it, to warn the user or "
            'block the page (Hannousse and Yahiouche 2021: "checking the legitimacy of visited web pages").'
        ),
        row=(
            "One URL with its page, crawled and looked up in late July to early August 2020: phishing URLs from the "
            "PhishTank and OpenPhish lists, legitimate ones crawled from Alexa's top 500 domains or taken from an "
            "older Yandex list (11,430 pages; the source's limit of 12 URLs per domain is not met: 40 hosts hold "
            "more, en.wikipedia.org 141)."
        ),
        predicted="Whether the page is phishing (50%), that is, came from one of the two phishing lists.",
        known=(
            "Counts and flags read off the URL (its length, special characters, words, brand names, subdomains), off "
            "the page's HTML (links, forms, media, title), and seven look-ups made at the crawl: the domain's WHOIS "
            "registration and expiry, its age (an age service), Alexa traffic rank, DNS record, Google index and Open "
            "PageRank."
        ),
        split=(
            "All pages of one registered domain stay on one side, so the test data stands for sites the model has "
            "not seen, from the same crawl."
        ),
        changes=(
            "We group the pages by their registered domain and drop the URL. Six features that hold one value on "
            "every row are dropped, the look-ups' codes for a failed query are missing values, and so are shares "
            "taken over an empty set (a page without links or media) and redirect shares above 1."
        ),
        fit="approximate",
        fit_reason=(
            "The classes are separate lists, top-ranked sites against reported phishing; only the 833 pages on "
            "hosting platforms come close to a filter's hard cases (ROC AUC about 0.90 there). The look-ups were read after the "
            "reports, some phishing pages were crawled after their takedown, and the test sites come from the same "
            "weeks as the training ones, while phishing changes over time."
        ),
    )

    # Dataset
    unique_name = "web_page_phishing_detection"
    domain = "technology & internet"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.17632/c2gw7fy2j4.3",
            license="CC BY 4.0",
            year="2020",
            bibtex="""
                @misc{hannousse2020webpage,
                  author = {Hannousse, Abdelhakim and Yahiouche, Salima},
                  title = {Web page phishing detection},
                  year = {2020},
                  howpublished = {Mendeley Data, version 3 (2021), \\url{https://doi.org/10.17632/c2gw7fy2j4.3}},
                  note = {Version 1 published 2020-09-26}
                }
            """,
            files=("dataset_B_05_2020.csv",),
        ),
    )
    split_leaf = "L-FORCED.groups"
    time_basis = TimeBasis(
        "ForcedGroupedFromTemporal",
        """
        phishing pages listed by PhishTank and OpenPhish and legitimate pages,
        all crawled and looked up once in late July to early August 2020; the release shuffled the rows and keeps no date per page
        (Time: Lost), so a filter's use on pages made later cannot be simulated. Within the one crawl nothing is
        measurable over time. The split holds out registered domains, the unit a filter meets new. Phishing adapts
        to filters, so a later period may score lower than this split shows; a dated release (PhishTank ids for the
        phishing half, crawl dates for both) would allow a split by time.
        """,
    )
    download_description = """
        We download the feature table (dataset B) of version 3 of the Mendeley Data release.

        mkdir -p local-data-warehouse/web_page_phishing_detection
        wget -O local-data-warehouse/web_page_phishing_detection/dataset_B_05_2020.csv https://data.mendeley.com/public-files/datasets/c2gw7fy2j4/files/575316f4-ee1d-453e-a04f-7b950915b61b/file_downloaded
        echo "21093e2902e5441c86a6daf95e86e7c332046e477fdf109a579d7bd81e586d6c  local-data-warehouse/web_page_phishing_detection/dataset_B_05_2020.csv" | sha256sum -c
    """
    curation_comments = """
        We start with `dataset_B_05_2020.csv` (11,430 URLs x 87 features, the URL and `status`) of Hannousse and
        Yahiouche's Mendeley Data release (version 3, 2021-06-25), described in "Towards benchmark datasets for
        machine learning based website phishing detection: An experimental study" (arXiv 2010.12847, 2020; Eng Appl
        Artif Intell 104:104347, 2021).

        - Files of the release not read: the ten `dataset_A_05_2020_p*.pickle` files hold 1,000 of the 11,430 URLs
          (100 each) with their source list and the page's parsed HTML (no other column); the source list encodes the
          label (Alexa and Yandex legitimate, PhishTank and OpenPhish phishing), so it is no feature, and it was read
          only for the selection check below. The `scripts` folder holds the extraction code (read for the look-ups'
          codes below).
        - Prediction point: a page is rated when a user opens it. The URL and page features are read from the page
          then; the seven look-ups (Sec. 4.2, Table 4) can be queried then too (Sec. 6.5 weighs their extraction time
          for runtime detection), but their values are as of the crawl, after the phishing page had been reported.
        - Collection (Sec. 4.1, Fig. 2): legitimate URLs from Alexa's top 500 domains (crawled, 12 URLs per domain;
          2,717 kept) and "still active" URLs of Sahingoz et al.'s Yandex list (2,998 kept); phishing URLs from
          PhishTank and OpenPhish; duplicate and dead URLs removed, at most 12 URLs per domain; balanced to 50% and
          shuffled. The paper dates the collection to March 2020 (Sec. 4.3), the data page and the file name to May
          2020, but the pages and look-ups are later: `domain_age` against the known registration dates of large
          legitimate domains (google.com, facebook.com, wikipedia.org, youtube.com and others) puts the legitimate
          look-ups at 21 to 26 July 2020 and the phishing ones over about 15 days into early August; phishing appspot
          URLs carry creation stamps up to 3 August 2020; the release's `external_features.py` is dated 27 July
          2020. So the rows stand for late July to early August 2020.
        - Target: `status` renamed `is_phishing` (Yes for phishing, 5,715 pages; No for legitimate, 5,715).
        - Note: one URL (an appspot.com phishing page) is listed twice; its two rows differ in eight URL and page
          features and in the domain look-ups, which were read 13 days apart, so both rows stay (one domain, one side).
          Within a domain the look-ups' dates differ by up to 15 days (domain age at the crawl), so the crawl and its
          look-ups ran over at least two weeks; no row carries a date.
        - Dropped: the six features that hold 0 on every row (`CONSTANT_COLUMNS`), so 81 features ship.
        - Look-up codes to missing (the release's `external_features.py`): `domain_age` -1 (the age service's error,
          1,781 rows), -2 (no age, 55) and one impossible -12; `domain_registration_length` -1 (WHOIS failed, 46) and 0
          (no expiration date, 1,404); `web_traffic` 0 (no Alexa rank or a failed query, 4,444, 81% of them phishing).
        - Codes that stay, with a failure mixed in (the release's scripts): `page_rank` 0 is Open PageRank's lowest
          rank and also a domain it does not list (2,666 rows, 96% phishing); `dns_record` (1 = no NS record),
          `google_index` (1 = not indexed) and `whois_registered_domain` (1 = WHOIS names another domain) also record a
          failed query, or a result page the script could not parse, as 1, so failures cannot be counted; 108 of the
          230 rows with `dns_record` 1 are hosts given as an IP address, where an NS query fails by design.
          `statistical_report` mixes a match against a static list of phishing hosts and IPs (1) with a failed DNS
          resolution of the domain at the look-up (2: 278 phishing, 28 legitimate pages).
        - Units and names: `domain_age` is days since registration, from an age service (not WHOIS), and
          `domain_registration_length` the absolute number of days to the expiration date in WHOIS (an expired
          domain reads positive), both counted from the look-up date; `web_traffic` is Alexa's reach rank (1 the
          most visited). `ip` flags an IPv4 or hex host or any run of 7 hex characters in the URL (97 of its 1,721
          ones are IP hosts); `nb_subdomains` counts the dots of the whole URL, capped at 3. The crawler falls back
          to the site's homepage when the URL itself raises an error, so a few rows may describe the homepage.
        - Shares over an empty set are missing values (CLEAN-10): `ratio_intHyperlinks` and `ratio_extHyperlinks` on
          pages without links (`nb_hyperlinks` 0, 1,381 rows), `ratio_intMedia` and `ratio_extMedia` where both are 0
          (no media, 3,874 rows; otherwise they sum to 100). The release wrote 0 for both. `nb_hyperlinks` already
          carries the same fact, so no new signal comes in. `ratio_extRedirection` above 1 (50 rows, up to 2: the
          script counts external media twice) is missing too. `links_in_tags`, `safe_anchor`, `ratio_extRedirection`
          and `ratio_extErrors` also read 0 over an empty set that the table cannot locate; they stay.
        - Number format (LEAK-13 to LEAK-15): a model on format alone (missing values, whole-number ratios) reaches
          ROC AUC 0.90 to 0.91, but it reads page content, not a class-dependent recording: one script wrote both classes,
          and `ratio_intHyperlinks`, `ratio_extHyperlinks`, `ratio_digits_url` and `ratio_digits_host` are exact
          fractions k/n of integer counts on 5,715 of 5,715 phishing and 5,711 of 5,715 legitimate rows. Unlike
          polish_companies_bankruptcy, the decimals follow the values.
        - Group: `registered_domain`, from the URL's host (`REGISTERED_DOMAINS`, 6,634 domains), anonymised; the URL is
          then dropped. The source's limit of 12 URLs per domain is not met: 40 hosts and 55 registered domains hold
          more (en.wikipedia.org 141 pages, one phishing host 214). Hosting platforms are one domain each
          (blogspot.com 383 pages, appspot.com 265, google.com 151 with drive.google.com and sites.google.com), one
          phishing campaign holds 351 pages on two hosts under one domain, and 24 domains hold both classes (833
          pages).
        - Duplicates: 291 phishing pages in 117 sets share every feature with another page (different URLs, 174
          surplus copies, no conflicting label); all but 4 surplus copies are within one domain, so the split keeps
          them on one side. Kept, as pages of one site or campaign (LEAK-16).
        - Anomaly: `nb_www` (a `www.` in the URL) is in 67% of legitimate and 21% of phishing URLs, a form difference
          of the two lists (ROC AUC 0.72 alone); dropping it changes grouped LightGBM by 0.0004 ROC AUC. Kept.
        - Selection (record marker `Selection Bias`): the two classes are two lists. Alexa's legitimate pages come
          from the 500 most visited domains, the ranking that `web_traffic` and `page_rank` measure, and the Yandex
          pages were listed before 2019 and looked up in 2020. Measured on the 1,000 URLs of dataset A (296 Alexa, 289
          Yandex, 415 phishing): no look-up tells Alexa from Yandex pages (ROC AUC 0.50 to 0.52 alone), and grouped
          LightGBM on all features separates phishing from either list alike (0.992 against Alexa, 0.993 against
          Yandex; look-ups alone 0.950 and 0.950), so neither the Alexa selection nor the later read of the Yandex
          pages shows in the look-ups.
        - Potential leak, kept on purpose: the look-ups were read once at the crawl, after each phishing page had been
          listed by PhishTank or OpenPhish, by a lag the release does not give (LEAK-10). A page delisted from Google
          or a domain changed after the report would show in `google_index` (0.865 ROC AUC alone), `page_rank` or
          `web_traffic`; no row is dated, so the late values cannot be located. Grouped LightGBM: look-ups alone 0.947,
          all features without them 0.977, all 0.990. Revisit with a dated release. The page features are late for
          part of the phishing side too: the crawler kept any page served with status 200, so in dataset A 65 of 415
          phishing pages are takedown pages (a suspended account, a parking or warning page, an error served as 200)
          and 74 more are blank, against 6 and 30 of 585 legitimate pages. The takedown templates leave fixed
          content fingerprints that match 493 rows of this table (482 phishing, 11 legitimate); the blank pages
          cannot be told from a live page without links.
        - Metric: Sec. 5 reports accuracy and macro F1, "two main metrics", for every model (Weka defaults, 10-fold
          cross-validation); neither is a single deliberate choice and no threshold or costs are fixed, so the fallback.
    """

    # Task
    target = "is_phishing"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Hannousse and Yahiouche (2021, Sec. 5) report accuracy and macro F1 side by side as their 'two main "
            "metrics' for every model, with Weka's default thresholds; no threshold, costs or decision is fixed, and "
            "accuracy is chosen because the classes are balanced, a habit rather than the decision's metric (MET-5, "
            "MET-6). The Mendeley page names no metric. roc_auc is the binary fallback. A deployed filter decides "
            "below 1% false alarms, a part of the curve ROC AUC weighs like any other: there, untuned models catch "
            "0.71 to 0.82 of the phishing pages with all features, while their ROC AUC spans only 0.981 to 0.989."
        ),
    )
    grouping = Grouping(
        on="registered_domain",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a registered domain (the label left of the public suffix, without the private suffixes, so a
            hosting platform such as blogspot.com is one domain); its rows are the domain's pages. The source's rule
            keeps at most 12 URLs per domain, but 55 domains hold more (up to 383, blogspot.com): hosting platforms,
            large sites such as wikipedia.org and one phishing campaign. The use case is a detector that rates a
            page when a user opens it ("checking the legitimacy of visited web pages", Hannousse and Yahiouche 2021):
            pages of one domain share the WHOIS, age, DNS and PageRank look-ups and most of the URL, so holding out
            whole domains tests sites never seen. Each page is one prediction, made from that page alone. The source
            scored 10-fold cross-validation over random rows.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "dataset_B_05_2020.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # The registered domain of the URL's host (the release's own domain split), the group; then the URL goes
        lookup = pd.read_csv(self.folder / REGISTERED_DOMAINS).set_index("host")["registered_domain"]
        host = df["url"].map(lambda u: (urlsplit(u).hostname or "").lower())
        domain = host.map(lookup)
        assert domain.notna().all(), "a host is missing from registered_domains.csv"
        df["registered_domain"] = anonymize_ids(domain)
        df = drop_columns(df, ["url", *CONSTANT_COLUMNS])
        # The look-ups' codes for a failed or empty query become missing values; -12 days of age is impossible
        for col, codes in LOOKUP_MISSING.items():
            df[col] = df[col].mask(df[col].isin(codes))
        df["domain_age"] = df["domain_age"].mask(df["domain_age"] < 0)
        # Shares over an empty set (no links, no media) were written as 0; external media counted twice push the
        # redirect share above 1
        no_links = df["nb_hyperlinks"] == 0
        df.loc[no_links, HYPERLINK_SHARES] = np.nan
        no_media = (df["ratio_intMedia"] == 0) & (df["ratio_extMedia"] == 0)
        df.loc[no_media, MEDIA_SHARES] = np.nan
        df["ratio_extRedirection"] = df["ratio_extRedirection"].mask(df["ratio_extRedirection"] > 1)
        df = df.rename(columns={"status": self.target})
        df = decode(df, {self.target: {"legitimate": "No", "phishing": "Yes"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["registered_domain"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        codes = []
        for col, values in {**LOOKUP_MISSING, "domain_age": [-1, -2, -12]}.items():
            for v in values:
                hit = raw[col] == v
                codes.append(
                    {
                        "column": col,
                        "code": v,
                        "legitimate": int((hit & (raw["status"] == "legitimate")).sum()),
                        "phishing": int((hit & (raw["status"] == "phishing")).sum()),
                    }
                )
        sizes = df.groupby("registered_domain", observed=True)[self.target].agg(
            pages="size", phishing=lambda s: int((s == "Yes").sum())
        )
        bands = pd.cut(sizes["pages"], [0, 1, 4, 12, 50, np.inf], labels=["1", "2-4", "5-12", "13-50", "51+"]).rename(
            "domain_size"
        )
        by_size = sizes.groupby(bands, observed=False).agg(
            domains=("pages", "size"), pages=("pages", "sum"), phishing_pages=("phishing", "sum")
        )
        is_phish = raw["status"] == "phishing"
        empty = {
            "no links: hyperlink shares": raw["nb_hyperlinks"] == 0,
            "no media: media shares": (raw["ratio_intMedia"] == 0) & (raw["ratio_extMedia"] == 0),
            "ratio_extRedirection above 1": raw["ratio_extRedirection"] > 1,
        }
        empty_rows = pd.DataFrame(
            [
                {"case": case, "legitimate": int((hit & ~is_phish).sum()), "phishing": int((hit & is_phish).sum())}
                for case, hit in empty.items()
            ]
        )
        return [
            Decision(
                "Shares over an empty set are missing values",
                "The release writes 0 for a share whose page has no links or no media, and a redirect share above 1 "
                "counts external media twice; these are not measurements, so they become missing values (the rows "
                "stay).",
                empty_rows,
            ),
            Decision(
                "The look-ups' failure codes are missing values",
                "The release's extraction code returns these codes when a query fails or finds nothing; they are not "
                "measurements, so they become missing values (the rows stay).",
                pd.DataFrame(codes),
            ),
            Decision(
                "Grouped by registered domain",
                "Pages of one domain share the domain look-ups and most of the URL. The source's rule keeps at most 12 "
                "URLs per domain, but 55 domains hold more (hosting platforms, large sites, one phishing campaign).",
                by_size,
            ),
        ]
