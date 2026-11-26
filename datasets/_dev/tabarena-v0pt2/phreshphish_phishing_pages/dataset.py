"""Curated dataset definition for `phreshphish_phishing_pages` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import math
import os
import re
from collections import Counter
from html import unescape
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
    drop_columns,
)

FEATURES_FILE = "phreshphish_features.parquet"
"""One row per page of the release: its id, label, date and language as published, the URL in our canonical form and
the URL and HTML features below; written once by `_prepare_raw_files` (the HTML is about 193 GB and is read in
batches)."""

KEEP_MONTHS = ("2024-08", "2024-09", "2024-10", "2025-06", "2025-07", "2025-08", "2025-09")
"""The collection months that hold both classes, recorded the same way. Measured on the release: no benign page from
November 2024 to May 2025 (and no page at all in May 2025), 147 benign against 53,409 phishing pages in July 2024, and
only benign pages in December 2025 (1,017); in October and November 2025 the phishing pages were written down in
another form (`curation_comments`)."""

LAST_DAY = "2025-09-07"
"""The last collection day kept: the last day of the source's train split. From 2025-09-08 the release holds its test
split, from which the source removed pages close to a training page; the months before keep them (`curation_comments`)."""

MIN_HTML_LENGTH = 10_000
"""The smallest page kept, in characters of HTML, for both classes: the release kept no benign page under 10,000
characters from 2024-08-19 on, and phishing pages from 1,000 or 5,000 (`curation_comments`)."""

URL_RX = re.compile(r"^(?:([a-zA-Z][a-zA-Z0-9+.-]*)://)?([^/?#]*)([^?#]*)")
DEFAULT_PORT_RX = re.compile(r":(?:80|443)$")
STRIPPED_RX = re.compile(r"[&,+;=]|[^\x00-\x7f]")
URL_KEYWORDS = (
    "login",
    "signin",
    "verify",
    "account",
    "secure",
    "update",
    "bank",
    "wallet",
    "auth",
    "confirm",
    "support",
)
PAGE_EXTENSIONS = (".php", ".html", ".htm", ".asp", ".aspx")

TAG_PATTERNS = {
    "n_forms": r"<form\b",
    "n_inputs": r"<input\b",
    "n_password_inputs": r"<input\b[^>]*type\s*=\s*[\"']?password",
    "n_hidden_inputs": r"<input\b[^>]*type\s*=\s*[\"']?hidden",
    "n_links": r"<a\b",
    "n_scripts": r"<script\b",
    "n_external_scripts": r"<script\b[^>]*\bsrc\s*=",
    "n_iframes": r"<iframe\b",
    "n_images": r"<img\b",
    "n_stylesheets": r"<link\b[^>]*stylesheet",
    "n_meta": r"<meta\b",
    "n_buttons": r"<button\b",
    "n_divs": r"<div\b",
    "n_svgs": r"<svg\b",
    "n_word_login": r"log\s?in|sign\s?in",
    "n_word_password": r"password",
    "n_word_verify": r"verif",
    "n_word_account": r"account",
    "n_word_copyright": r"&copy;|©|copyright",
}
"""Counts of tags and words in the page's HTML, case-insensitive. Only counts of what the page contains: nothing is
read from how the crawler wrote the page down (a leading DOCTYPE, the raw length, the line count), which changed by
class over time (`curation_comments`)."""

TAG_RX = {k: re.compile(v, re.I) for k, v in TAG_PATTERNS.items()}
HREF_RX = re.compile(r"<a\b[^>]*href\s*=\s*[\"']([^\"']*)", re.I)
TITLE_RX = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
MAX_TITLE_LENGTH = 1000
"""A `<title>` over 1,000 characters is an unclosed or embedded tag, not the page's title: its text and length are set
to missing."""
NULL_HREFS = ("", "#", "#!", "javascript:void(0)", "javascript:;")


def canonical_url(url: str) -> str:
    """The URL as the features read it, in one form for both classes: no scheme, no query, no fragment, the host in
    lower case without a default port (":80", ":443"), a bare host ending with "/", and no `&`, `,`, `+`, `;`, `=` or
    non-ASCII character. The release removed the query from benign URLs only, recorded 5,741 benign URLs without a
    scheme and nearly every bare phishing host without its "/", and stored benign URLs without those characters
    (`curation_comments`).
    """
    m = URL_RX.match(url or "")
    host = DEFAULT_PORT_RX.sub("", m.group(2).lower())
    return STRIPPED_RX.sub("", host + (m.group(3) or "/"))


def url_host(url: str) -> str:
    """The host of a canonical URL, lower case, without user, port and trailing dot."""
    return url.split("/", 1)[0].rsplit("@", maxsplit=1)[-1].split(":", maxsplit=1)[0].lower().strip(".")


def _entropy(s: str) -> float:
    if not s:
        return 0.0
    n = len(s)
    return -sum(v / n * math.log2(v / n) for v in Counter(s).values())


def url_features(url: str) -> dict[str, float]:
    """Lexical features of a canonical URL (host and path)."""
    hostport, _, rest = url.partition("/")
    path = "/" + rest
    host = url_host(url)
    bare = host[4:] if host.startswith("www.") else host
    labels = bare.split(".")
    n_host_digits = sum(ch.isdigit() for ch in bare)
    return {
        "host_length": len(bare),
        "host_dots": bare.count("."),
        "host_hyphens": bare.count("-"),
        "host_digits": n_host_digits,
        "host_digit_share": n_host_digits / max(len(bare), 1),
        "host_labels": len(labels),
        "host_longest_label": max(len(x) for x in labels),
        "host_entropy": _entropy(bare),
        "host_is_ip": int(bool(re.fullmatch(r"[\d.]+", bare))),
        "tld_length": len(labels[-1]),
        "host_punycode": int("xn--" in bare),
        "host_vowel_share": sum(ch in "aeiou" for ch in bare) / max(len(bare), 1),
        "host_www": int(host.startswith("www.")),
        "host_port": int(":" in hostport.split("@")[-1]),
        "url_length": len(url),
        "url_entropy": _entropy(url),
        "url_at_signs": url.count("@"),
        "url_percent_signs": url.count("%"),
        "url_tildes": url.count("~"),
        "url_keywords": sum(k in url.lower() for k in URL_KEYWORDS),
        "path_length": len(path),
        "path_depth": path.count("/"),
        "path_is_root": int(path == "/"),
        "path_dots": path.count("."),
        "path_hyphens": path.count("-"),
        "path_digits": sum(ch.isdigit() for ch in path),
        "path_page_extension": int(path.lower().endswith(PAGE_EXTENSIONS)),
    }


def page_title(html: str) -> str:
    """The text of the page's first `<title>` tag, entities decoded and white space collapsed ("" when there is none);
    read the same way from every page, whatever its class or month.
    """
    m = TITLE_RX.search(html)
    return " ".join(unescape(m.group(1)).split()) if m else ""


def html_features(html: str, host: str) -> dict[str, float | str]:
    """Tag and word counts of a page, its links to other hosts, its title's length and its title as text."""
    f: dict[str, float | str] = {k: len(rx.findall(html)) for k, rx in TAG_RX.items()}
    hrefs = HREF_RX.findall(html)
    external = 0
    for h in hrefs:
        if h.startswith(("http://", "https://", "//")):
            external += url_host(canonical_url(h if "://" in h else "http:" + h)) != host
    f["n_external_links"] = external
    f["n_empty_links"] = sum(h.strip() in NULL_HREFS for h in hrefs)
    f["external_link_share"] = external / len(hrefs) if hrefs else np.nan
    m = TITLE_RX.search(html)
    f["title_length"] = len(m.group(1).strip()) if m else 0
    f["title"] = page_title(html)
    return f


def features_of_file(path: Path) -> pd.DataFrame:
    """The features of one parquet file of the release, read in batches of 500 pages, with the length of the HTML
    (`html_length`, for the size floor in `_clean`; never a feature).
    """
    import pyarrow.parquet as pq

    cols = ["sha256", "url", "html", "label", "date", "lang", "lang_score"]
    parts = []
    for batch in pq.ParquetFile(path).iter_batches(batch_size=500, columns=cols):
        t = batch.to_pandas()
        rows = []
        for url, html in zip(t["url"], t["html"], strict=True):
            cu = canonical_url(url)
            rows.append(
                {
                    "url": cu,
                    "html_length": len(html or ""),
                    **url_features(cu),
                    **html_features(html or "", url_host(cu)),
                }
            )
        meta = t[["sha256", "label", "date", "lang", "lang_score"]].reset_index(drop=True)
        meta.insert(0, "source_split", path.name.split("-")[0])
        parts.append(pd.concat([meta, pd.DataFrame(rows)], axis=1))
    return pd.concat(parts, ignore_index=True)


class PhreshphishPhishingPages(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is this web page, opened on a given day, a phishing page?",
        use_case=(
            "A browser plug-in or web filter rates a page when it is opened, from the URL and the page alone, to warn "
            "the user or block it; the vendor refits the model on the pages it collected up to then (Dalton et al. "
            '2025: "browser plugins", detection "within a few hundred milliseconds").'
        ),
        row=(
            "One page, rendered by one crawler on its collection day: benign pages from the browsing telemetry of "
            "Webroot users and searches for targeted brands, phishing pages reported to PhishTank, the APWG and "
            "NetCraft (348,287 pages of at least 10,000 characters, from August to October 2024 and 1 June to 7 "
            "September 2025, the days that hold both classes recorded alike)."
        ),
        predicted="Whether the page is phishing (21% of the pages; 12% to 50% by month).",
        known=(
            "The URL without its scheme and query (as text and as counts: host length, dots, digits, path depth, "
            "keywords), counts of tags and words in the page (forms, password fields, links to other hosts, scripts, "
            "frames), the title's length, the title itself as text and the page's language."
        ),
        split=(
            "The next four weeks: three four-week test windows, 16 June to 7 September 2025, each trained on every "
            "page collected up to one day before it (August to October 2024, then June 2025 on)."
        ),
        changes=(
            "We build the features from the URLs and HTML. The release recorded the classes differently, so for both "
            "we write the URL in one form, keep each URL's first collection and pages of 10,000 characters or more, "
            "and read nothing from how a page was written down. We keep months with both classes, up to 7 September "
            "2025, before the source's pruned test split; the date orders the split."
        ),
        fit="approximate",
        fit_reason=(
            "Pages real users opened and pages reported as phishing, rendered by one crawler, as a filter meets them. "
            "Three gaps: the URL lacks its query and scheme, which a filter sees (removed for the recording by "
            "class); the 50 counts are ours, not the page a product reads; and "
            "the class mix follows the collection, not the web (benign pages missing on many days)."
        ),
    )

    # Dataset
    unique_name = "phreshphish_phishing_pages"
    domain = "technology & internet"
    sources = (
        Source(
            role="publication",
            platform="HuggingFace",
            url="https://huggingface.co/datasets/phreshphish/phreshphish",
            license="CC BY 4.0",
            year="2025",
            bibtex=r"""
                @article{dalton2025phreshphish,
                  title = {PhreshPhish: A Real-World, High-Quality, Large-Scale Phishing Website Dataset and Benchmark},
                  author = {Dalton, Thomas and Gowda, Hemanth and Rao, Girish and Pargi, Sachin and Khodabakhshi, Alireza Hadj and Rombs, Joseph and Jou, Stephan and Marwah, Manish},
                  year = {2025},
                  journal = {arXiv preprint arXiv:2507.10854},
                  url = {https://arxiv.org/abs/2507.10854}
                }
            """,
            files=("data/*.parquet",),
        ),
    )
    download_description = """
        We download the 77 parquet files of version 1.0.1 (git tag v1.0.1, commit eca603e0) of the Hugging Face
        dataset (36.6 GB; URL, HTML, label and date of every page). The benchmark lists (`benchmark/`) are left out.

        mkdir -p local-data-warehouse/phreshphish_phishing_pages
        python -c "from huggingface_hub import snapshot_download; snapshot_download('phreshphish/phreshphish', repo_type='dataset', revision='v1.0.1', allow_patterns=['data/*.parquet', 'README.md'], local_dir='local-data-warehouse/phreshphish_phishing_pages')"
    """
    curation_comments = """
        We start with the 77 parquet files (`data/train-*.parquet`, `data/test-*.parquet`) of PhreshPhish v1.0.1 on
        Hugging Face (Dalton et al. 2025, arXiv 2507.10854): 666,315 pages (367,989 benign, 298,326 phishing) with
        `sha256`, `url`, `html`, `label`, `target` (the impersonated brand), `date` (collection day, 2024-07-02 to
        2025-12-16), `lang` and `lang_score`. The card asks that the data "should only be used for anti-phishing
        research" (CC BY 4.0).

        - Prediction point: a filter rates a page when it is opened, from its URL and HTML. The release's `date` is
          the collection day. For a phishing page it records when its label arrived: the page was crawled "within
          minutes of being reported" (Sec. 3). For a benign page it records when the crawler rendered it from the
          telemetry. So the date orders the split and is no input (`time_of="label"`); the class mix by day is the
          collection's schedule, not the web's (no benign page on 41 of the 210 collection days). Measured as support
          on the earlier monthly windows: the day's class share alone scores ROC AUC 0.72 to 0.85 within each test
          month, while the weekday or the day of the month learnt from earlier months scores 0.47 to 0.51.
        - Files left out: `benchmark/` lists subsets of the release's test split at fixed low phishing rates (the
          card's benchmarks), no new rows. The release's README is read for the field list.
        - Features are ours: the release has no table. `_prepare_raw_files` writes `phreshphish_features.parquet`
          (one pass over the HTML): the URL features of `url_features` and the counts of `html_features` (19 tag and
          word counts, links to other hosts, empty links, the title's length; `TAG_PATTERNS`) and the page's title as
          text (`page_title`).
        - Class-dependent recording (LEAK-13), removed from the URL: the release removed the query from benign URLs
          only (68 of 367,989 benign URLs keep one, against 11.7% of phishing URLs; Appendix A.2, where the removal of
          personal data "focused on the benign class only"), recorded 5,741 benign URLs without a scheme (no phishing
          URL) and wrote a bare phishing host without its "/" (45,195 phishing, 25 benign URLs). Every URL is read
          without scheme, query and fragment, and a bare host gets its "/" (`canonical_url`); so the scheme is no
          feature (http on 15.6% of phishing and 0.6% of benign URLs that have one). The release also stored benign
          URLs without `&`, `,`, `+`, `;`, `=` and non-ASCII characters (all 10,986 benign Wikipedia URLs lost their
          commas), which marked 0.3% to 0.5% of phishing test rows with no false positive; and it wrote 137 phishing
          hosts and no benign one in upper case, and 61 phishing URLs and 1 benign URL with an explicit ":443".
          `canonical_url` drops those characters from every URL, writes the host in lower case and drops a default
          port.
        - Class-dependent recording (LEAK-13), copies: the release keeps one row per lower-cased URL, so benign URLs,
          already without their query, were deduplicated, and phishing URLs that differ only in the query were not.
          The same rule on the canonical URL for both classes keeps each URL's first collection (by date, then
          `sha256`) and drops 16,217 rows (16,105 phishing, 112 benign), before the months are chosen.
        - Class-dependent recording (LEAK-13), the HTML: from October 2025, 79% of phishing pages start with a
          DOCTYPE, against none before and none of the benign pages of October and November (98.8% of December's
          benign pages). The tag counts carry that form: within the phishing pages of October and November they tell
          a page with a DOCTYPE from one without at ROC AUC 0.976 (LightGBM, 5-fold), and benign pages of December
          from those of October at 0.956; the median phishing page fell from 7 to 24 links (June to September) to 4.
          So October and November 2025 are dropped (132,183 rows), and no feature reads the DOCTYPE, the raw length or
          the line count.
        - Class-dependent recording (LEAK-13), the page size: the release kept benign pages from a floor of 10,000
          characters of HTML (from 2024-08-19 on; the shortest benign page of each month from September 2024 is
          10,000 to 10,114 characters) and phishing pages from 1,000 characters, then 5,000 from April 2025. Page
          length is no feature, but the tag counts recover it at ROC AUC 0.998 within phishing, and "under 10,000
          characters, so phishing" had precision 1.00 in every test window. One floor for both classes
          (`MIN_HTML_LENGTH`, read from `html_length`, which is no feature) drops 24,429 pages (23,855 phishing,
          574 benign); on the earlier monthly windows the fix moved LightGBM's mean ROC AUC from 0.9591 to 0.9555.
          It also removes the pages under 200 characters (1.46% of phishing pages in the release, a page taken down or
          empty when crawled), which the release had dropped from the benign class.
        - End of the data (LEAK-42, `LAST_DAY`): the source's split cuts on 2025-09-08, and from that day the release
          holds its test split, from which the source removed pages close to a training page (TF-IDF cosine,
          threshold not given). Measured: exact HTML repeats among September phishing pages fall from 9.0% before the
          8th to 0.4% after (July and August keep 4.7% and 6.8% after their 8th), and phishing pages whose tag
          signature was seen before from 21% to 32% (July to 1-7 September) to 3.7%. The earlier days keep the
          reused kits a filter meets again (natural), so the data end on 2025-09-07 and 32,255 pages of 8 to 30
          September are dropped (4,431 phishing).
        - Rows (`KEEP_MONTHS`, `LAST_DAY`, `MIN_HTML_LENGTH`): the days that hold both classes recorded alike,
          348,287 pages (275,528 benign, 72,759 phishing). Also dropped: July 2024 (147 benign pages), November 2024
          to April 2025 (phishing only; no page in May 2025) and December 2025 (987 benign pages only).
        - History: the months August to October 2024 stay in training although 7.5 months without benign pages
          separate them from June 2025; without them no window would train on half the rows. Version 1.0.1
          "downsampl[ed] some earlier samples" for temporal consistency (the card). Measured against v1.0.0 (commit
          3d861877): it held 139,229 benign pages from July 2024 and 2,507 from March 2025; v1.0.1 keeps 147 of the
          July ones (0.5% of v1.0.0's July benign pages) and none of March.
        - Target: `label` renamed `is_phishing` ("Yes" for phish).
        - Dropped: `sha256` (an id), `target` (the brand a phishing page imitates; empty on every benign page), the
          raw URL (replaced by the canonical one) and the release's split (`source_split`, a cut on the date).
        - Kept: the canonical URL as text (`url`; the filter's input, not an id, so its identifier warning is
          accepted), `lang`, the language the release detected, and `lang_score`, its confidence; the release writes
          -1 where it gives no language (1.0% of benign, 4.2% of phishing pages), set to missing. Six 0/1 flags of ours (`host_is_ip`, `host_punycode`, `host_www`, `host_port`,
          `path_is_root`, `path_page_extension`) are categories. A `title_length` over 1,000 characters (an unclosed
          or embedded `<title>`, 25 pages) is set to missing.
        - Title (`title`, text): the page's first `<title>` tag, entities decoded and white space collapsed
          (`page_title`), read the same way from every page; missing where the page has none, an empty one or one
          over 1,000 characters (2.4% of benign, 4.0% of phishing pages; 275,877 distinct titles). It carries the
          brand a page names, which none of the counts does, and is encoded like `url`, by the framework's text
          encodings (`tfidf-svd` fitted on each training side). Checked against the recordings by class above:
          within benign pages the share without a title (2.1% to 2.7%), the median length (46 to 47 characters) and
          the share written with HTML entities (9.3% to 10.1%) hold in every month, and the title does not tell
          2025 from 2024 benign pages (ROC AUC 0.503, 5-fold). By page size the classes lack a title alike above the
          floor: 9.8% of benign and 12.1% of phishing pages of 10,000 to 20,000 characters, 1.6% and 1.8% of those
          over 50,000. The phishing titles move with the campaigns: 15.1% of June 2025 phishing pages have none (342
          of the 410 of 18 June), and "One moment..." heads 2,786 phishing pages of July and August 2025 and no
          benign one. Untuned, with every other column and the URL encoded the same way, the title (`tfidf-svd`)
          moves LightGBM's ROC AUC from 0.986, 0.913 and 0.989 (newest window first) to 0.988, 0.921 and 0.988 and
          its partial ROC AUC up to a 1% false-positive rate from 0.832, 0.798 and 0.843 to 0.848, 0.799 and 0.858;
          logistic regression's ROC AUC moves from 0.918, 0.885 and 0.968 to 0.936, 0.881 and 0.971. The title's
          `e5-small-v2` embedding gives LightGBM 0.989, 0.925 and 0.991.
        - Note: registered domains recur across every window (hosting platforms such as gitbook.io, webflow.io and
          pages.dev for phishing, wikipedia.org for benign); a filter meets known domains, so the split keeps them
          (SPLIT-13). No canonical URL repeats across a cut (one row per URL). On the earlier monthly windows, a
          page's HTML (case and white space aside) was in an earlier month for 3.7% to 8.2% of phishing and 0.1% to
          0.2% of benign test pages, the same sequence of tags for 19% to 30% of phishing pages: reused phishing kits,
          which a filter meets again. Kept (LEAK-42, natural), up to the source's pruning (above); 9 identical pages
          carry both labels.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): phishing arrives in same-day bursts from the
          feeds, so counting how many test rows of the same day share a host, a registered domain or an HTML
          fingerprint added +0.031, +0.009 and +0.045 ROC AUC on the earlier monthly windows; the same counts over
          past days only add nothing. Each test row is predicted from the training rows and its own features; a method
          that reads other test rows is not benchmarked.
    """

    # Task
    target = "is_phishing"
    problem_type = "binary_classification"
    metric = Metric(
        name=None,
        origin="fallback",
        original="average_precision",
        reference="Dalton et al. 2025, arXiv 2507.10854, Sec. 5.1",
        reason=(
            "The paper scores average precision and precision at recall 0.9, argued from the cost of a false "
            'positive ("Users ... are typically highly sensitive to false positives", Sec. 5.1), on subsets of its '
            "test split at fixed phishing base rates of 0.05% to 5% (the card's benchmarks). Our test windows hold "
            "13.5% to 38.0% phishing, so average precision here would measure something else (MET-2, MET-9), and "
            "precision at recall 0.9 needs a threshold (MET-6): the fallback roc_auc, which does not depend on the "
            "class share, here set by the collection. It scores the whole curve, while a filter sets its threshold "
            "at a false-positive rate of 1% or less: on the earlier monthly windows the best of four untuned models "
            "was the same under every score, but among the three weaker ones ROC AUC ranked the URL-only LightGBM "
            "last, and the partial ROC AUC up to a 1% false-positive rate, the true-positive rate at 0.1% and the "
            "average precision at 1% phishing ranked it first."
        ),
    )

    # Splits
    split_leaf = "L-ORDER.windows"
    temporal = Temporal(
        on="date",
        splits=TemporalSplits(
            window=4,
            unit="weeks",
            cutoffs=("2025-08-11", "2025-07-14", "2025-06-16"),
            gap=1,
            gap_unit="days",
        ),
        time_of="label",
    )
    splits_comment = """
        A filter vendor refits its model on the pages collected so far and scores the next pages. The source states no
        refit cadence; four weeks is our assumption (a person signs it off), close to a monthly refit. Three four-week
        test windows: 11 August to 7 September, 14 July to 10 August and 16 June to 13 July 2025 (50,120, 35,257 and 42,194
        pages; 9,899, 13,397 and 5,701 phishing), each trained on every page collected at least one day before it (85.5%,
        74.8% and 63.3% of the rows); the newest window is the deployment period. The gap of one day is the time a refit
        takes to build before it is used, as on fugaku_hpc_job_failure_1m and ga_merchandise_store_sessions; the label
        itself needs none (a phishing page's label is its feed report, made minutes before the crawl). The data end on
        2025-09-07, the last day of the source's train split: from 2025-09-08 the source removed pages close to a
        training page, which the earlier days keep (`curation_comments`), so a window after it would be another
        population. The oldest window trains on 2024 and 3,401 pages of 1 to 14 June 2025, little of 2025; a June
        window would train on 2024 alone, after 7.5 months without benign pages, so it is no window. October and
        November 2025 are left out for the changed HTML form. Registered domains stay across the cuts: the sibling
        web_page_phishing_detection groups by registered domain because it has no dates, so its groups stand in for
        time; here the dated cut gives the real mix of known and new domains (SPLIT-13). Three windows against the
        target of 9 for 348,287 rows (SPLIT-33): a fourth four-week window (19 May to 15 June 2025) would hold 3,517
        pages and train on 2024 alone, and shorter windows would shorten the assumed refit only to reach the count.
        `dataset check` warns on the count, on the gap on a date that dates the label (the gap stands for the refit,
        not the label) and on 2024-10-31, a day with phishing pages only (the date is no input); the three are
        accepted with the horizon (`accepted_check_warnings`).
    """
    accepted_check_warnings = {
        "dataset_identifier_column": (
            "The canonical URL is the filter's input, not an id: one value per row by the rule of one row per URL; "
            "alone it scores ROC AUC 0.896 (Andrej, 2026-11-26)."
        ),
        "splits_below_target": (
            "Three of the nine windows an IID split of 348,287 pages would get: a fourth four-week window (19 May to "
            "15 June 2025) would hold 3,517 pages and train on 2024 alone, after 7.5 months without benign pages, and "
            "shorter windows would shorten the assumed four-week refit only to reach the count (Andrej, 2026-11-26)."
        ),
        "task_label_time_gap": (
            "The one-day gap stands for the time a refit takes to build before it is used, not for the label's "
            "delay: a phishing page's label is its feed report, made minutes before the crawl (Andrej, 2026-11-26)."
        ),
        "dataset_pure_feature_value": (
            "2024-10-31 holds 3,562 phishing pages and no benign one, a day of the collection's schedule; the date "
            "orders the split and is no input (Andrej, 2026-11-26)."
        ),
    }

    prepared_raw_files = (FEATURES_FILE,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        import multiprocessing
        import shutil
        import tempfile

        # One forked process per file (a fork needs no pickling of this module's functions), each writing its part;
        # the parts are joined in the sorted order of the files, so the result does not depend on the process count.
        files = sorted((raw_dir / "data").glob("*.parquet"))
        n_jobs = max(1, min(16, (os.cpu_count() or 2) - 1))
        ctx = multiprocessing.get_context("fork")
        tmp = Path(tempfile.mkdtemp(dir=raw_dir, prefix=".features_parts_"))
        try:
            for i in range(0, len(files), n_jobs):
                procs = [
                    ctx.Process(target=lambda p=p: features_of_file(p).to_parquet(tmp / p.name, index=False))
                    for p in files[i : i + n_jobs]
                ]
                for proc in procs:
                    proc.start()
                for proc in procs:
                    proc.join()
                    if proc.exitcode != 0:
                        raise RuntimeError(f"feature extraction failed with exit code {proc.exitcode}")
            parts = [pd.read_parquet(tmp / p.name) for p in files]
            pd.concat(parts, ignore_index=True).to_parquet(raw_dir / FEATURES_FILE, index=False)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / FEATURES_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        # The release keeps one row per lower-cased URL; a benign URL had lost its query first, a phishing URL had not.
        # The same rule on the canonical URL, for both classes: the first collection of each URL stays.
        df = df.sort_values(["date", "sha256"], kind="stable")
        df = df[~df["url"].str.lower().duplicated(keep="first")]
        df = df[df["date"].str[:7].isin(KEEP_MONTHS) & (df["date"] <= LAST_DAY)]
        # The release kept benign pages from 10,000 characters and phishing pages from 1,000 or 5,000: one floor for both.
        df = df[df["html_length"] >= MIN_HTML_LENGTH]
        # `lang_score` is -1 exactly where the release gives no language: missing, as `lang` is.
        df["lang_score"] = df["lang_score"].where(df["lang"].notna())
        # A "title" over 1,000 characters is an unclosed or embedded <title> tag, not the page's title; an empty one is none.
        whole_title = df["title_length"] <= MAX_TITLE_LENGTH
        df["title_length"] = df["title_length"].where(whole_title)
        df["title"] = df["title"].where(whole_title & (df["title"] != ""))
        df = df.rename(columns={"label": self.target})
        df = decode(df, {self.target: {"benign": "No", "phish": "Yes"}})
        return drop_columns(df, ["sha256", "source_split", "html_length"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "lang",
                "host_is_ip",
                "host_punycode",
                "host_www",
                "host_port",
                "path_is_root",
                "path_page_extension",
            ],
            string=["url", "title"],
            datetime={"date": "%Y-%m-%d"},
        )
