"""Curated dataset definition for `rosbank1` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

TRANSACTIONS_FILE = "train.csv.gz"
TIME_FORMAT = "%d%b%y:%H:%M:%S"  # TRDATETIME, e.g. 21OCT17:00:00:00

RATES_DIR = "cbr_rates"
"""The Bank of Russia's official daily rates, one file per currency it quoted (download_description)."""
CURRENCY_LIST = "cbr_currencies.xml"
"""The Bank of Russia's currency list: its series id and the ISO 4217 numeric code of each currency."""
RUBLES = (810, 643)  # the ISO numeric code of the ruble before (RUR) and after (RUB) the 1998 redenomination

# The hand-crafted features of the CoLES paper (Babaev et al. 2022, Sec. 4.1.2) as pytorch-lifestream configures them
# for this dataset (ptls-experiments, scenario_rosbank/conf/inference/seq_encoder/agg_feature.yaml): the count, sum,
# mean and standard deviation of `amount` over all transactions, and per value of each code column the count, mean and
# standard deviation of `amount`. The code columns and their values, most frequent first:
TRX_CATEGORIES = (
    "POS",
    "DEPOSIT",
    "WD_ATM_ROS",
    "WD_ATM_PARTNER",
    "C2C_IN",
    "WD_ATM_OTHER",
    "C2C_OUT",
    "BACK_TRX",
    "CAT",
    "CASH_ADV",
)
CURRENCIES = {810: "810", 978: "978", 840: "840"}  # rubles (810, the old RUR code), euros, US dollars; others "other"
N_MCC = 97  # the most frequent MCC codes get their own columns, the rest share "other" (ptls: `mcc: in: 100`)
OTHER = "other"

# The time features of the competition's 1st place in task 1 (Kirill Khrylchenko, 2018; time.ipynb of
# github.com/KhrylchenkoKirill/rosbank, rewritten here): where a client's active days lie and how far apart they are,
# for all transactions, each transaction category, money in and money out
FIRST_DAY = pd.Timestamp("2016-10-07")  # the first day of the transactions; days are counted from it
INFLOW = {"DEPOSIT", "C2C_IN", "BACK_TRX"}  # the other categories take money out
DATE_STATS = ("span", "std", "median", "mean", "max", "gap_mean", "gap_max", "gap_min", "gap_std", "gap_p50", "gap_p95")

DISCOUNT_MONTHS = 3  # "history of clients' transactions during 3 months of privileged usage" (the task text)
LABEL_MONTHS = 3  # the label covers "the next three months of usage of the product" after the period
# How the label window was placed is not published, and the newest periods' labels are off (March 2018: 24 of 36
# churned). We keep the clients whose period ends before 2018-01-01: a three-month window after the period then closes by
# 2018-03-31, inside the transactions (they end 2018-04-02) (curation_comments, "Cohort").
LABELS_COMPLETE_BEFORE = "2018-01-01"


def read_ruble_rates(raw_dir: Path) -> pd.DataFrame:
    """The Bank of Russia's rates: `currency` (ISO numeric code), `date` (the day a rate takes effect), `rubles`."""
    iso = pd.read_xml(raw_dir / CURRENCY_LIST, xpath="./Item", parser="etree", encoding="cp1251")
    iso = iso.dropna(subset=["ISO_Num_Code"]).set_index("ID")["ISO_Num_Code"].astype(int)
    frames = []
    for path in sorted((raw_dir / RATES_DIR).glob("*.xml")):
        rates = pd.read_xml(path, xpath="./Record", parser="etree", encoding="cp1251")
        frames.append(
            pd.DataFrame(
                {
                    "currency": rates["Id"].map(iso),
                    "date": pd.to_datetime(rates["Date"], format="%d.%m.%Y"),
                    # rubles per `Nominal` units, with a decimal comma
                    "rubles": rates["Value"].str.replace(",", ".").astype(float) / rates["Nominal"],
                }
            )
        )
    rates = pd.concat(frames, ignore_index=True)
    assert rates["currency"].notna().all(), "a rate series without an ISO code"
    return rates


def in_rubles(tx: pd.DataFrame, rates: pd.DataFrame) -> pd.Series:
    """`amount` in rubles at the rate in force on the transaction's day; missing where the Bank set no rate."""
    day = pd.to_datetime(tx["TRDATETIME"], format=TIME_FORMAT).dt.normalize()
    left = pd.DataFrame({"day": day, "currency": tx["currency"]}).sort_values("day", kind="stable")
    quoted = pd.merge_asof(
        left.reset_index(), rates.sort_values("date", kind="stable"), left_on="day", right_on="date", by="currency"
    )
    rate = quoted.set_index("index")["rubles"].reindex(tx.index)
    return tx["amount"] * rate.where(~tx["currency"].isin(RUBLES), 1.0)


def per_value_stats(tx: pd.DataFrame, column: str, values: list[str], prefix: str) -> pd.DataFrame:
    """Per client: the count, mean and standard deviation of `amount` for each value of `column` (in `values` order).

    A client without a transaction of a value has count 0 and a missing mean and standard deviation; the standard
    deviation of a single transaction is missing as well.
    """
    grouped = tx.groupby(["cl_id", column], sort=True)["amount"]
    count = grouped.size().unstack(fill_value=0).reindex(columns=values, fill_value=0)
    mean = grouped.mean().unstack().reindex(columns=values)
    std = grouped.std().unstack().reindex(columns=values)
    count.columns = [f"count_{prefix}_{v}" for v in values]
    mean.columns = [f"mean_amount_{prefix}_{v}" for v in values]
    std.columns = [f"std_amount_{prefix}_{v}" for v in values]
    return pd.concat([count, mean, std], axis=1)


def date_stats(days: np.ndarray) -> list[float]:
    """Of sorted active days: span, spread, median, mean and last day, and the gaps between them; missing if undefined."""
    if len(days) == 0:
        return [np.nan] * len(DATE_STATS)
    stats = [days[-1] - days[0], days.std(), np.median(days), days.mean(), days[-1]]
    if len(days) < 2:
        return [*stats, *[np.nan] * 6]
    gaps = np.diff(days)
    return [*stats, gaps.mean(), gaps.max(), gaps.min(), gaps.std(), *np.percentile(gaps, [50, 95])]


def time_features(tx: pd.DataFrame) -> pd.DataFrame:
    """Per client (`cl_id`, the index): the 1st place's time features, over the whole history and the last month.

    For each group of transactions (all, each category, money in, money out): `date_stats` of the active days, the same
    over the group's last active calendar month, the active days per calendar month (mean, median, max, min, std), and
    the quarter of the last active month.
    """
    time = pd.to_datetime(tx["TRDATETIME"], format=TIME_FORMAT).dt.normalize()
    active = pd.DataFrame(
        {"cl_id": tx["cl_id"], "category": tx["trx_category"], "day": (time - FIRST_DAY).dt.days, "time": time}
    ).drop_duplicates(["cl_id", "category", "day"])
    active["month"] = active["time"].dt.to_period("M")
    groups = {
        "all": None,
        **{c.lower(): {c} for c in TRX_CATEGORIES},
        "in": INFLOW,
        "out": set(TRX_CATEGORIES) - INFLOW,
    }
    rows = {}
    for cl_id, client in active.groupby("cl_id", sort=True):
        row = {}
        for name, categories in groups.items():
            part = client if categories is None else client[client["category"].isin(categories)]
            part = part.drop_duplicates("day").sort_values("day", kind="stable")
            days = part["day"].to_numpy(dtype=float)
            row.update(zip([f"time_{name}_{s}" for s in DATE_STATS], date_stats(days), strict=True))
            last = part["month"].max() if len(part) else None
            in_last = days[(part["month"] == last).to_numpy()] if len(part) else days
            # the last day of the last month is the group's last day (`max` above), so it is left out here
            last_month = {s: v for s, v in zip(DATE_STATS, date_stats(in_last), strict=True) if s != "max"}
            row.update({f"time_{name}_lastmonth_{s}": v for s, v in last_month.items()})
            per_month = part.groupby("month")["day"].size().to_numpy(dtype=float)
            spread = (
                [per_month.mean(), np.median(per_month), per_month.max(), per_month.min(), per_month.std()]
                if len(per_month)
                else [np.nan] * 5
            )
            names = [f"time_{name}_days_per_month_{s}" for s in ("mean", "median", "max", "min", "std")]
            row.update(zip(names, spread, strict=True))
            row[f"time_{name}_last_quarter"] = last.quarter if last is not None else np.nan
        rows[cl_id] = row
    out = pd.DataFrame.from_dict(rows, orient="index")
    out.index.name = "cl_id"
    return out


def aggregate_transactions(tx: pd.DataFrame) -> pd.DataFrame:
    """One row per client (`cl_id`, the index) from its card transactions: the CoLES aggregates plus three dates."""
    assert set(tx["trx_category"].unique()) <= set(TRX_CATEGORIES), "a transaction category without columns"
    tx = tx.assign(time=pd.to_datetime(tx["TRDATETIME"], format=TIME_FORMAT))
    # MCC codes by transaction count, ties by code: the N_MCC most frequent keep their code, the rest are "other"
    counts = tx["MCC"].value_counts().sort_index(kind="stable")
    top_mcc = counts.sort_values(ascending=False, kind="stable").index[:N_MCC]
    mcc_values = [str(code) for code in top_mcc]
    tx = tx.assign(
        mcc=tx["MCC"].astype("int64").astype(str).where(tx["MCC"].isin(top_mcc), OTHER),
        currency_code=tx["currency"].map(CURRENCIES).astype(object).where(tx["currency"].isin(CURRENCIES), OTHER),
    )
    by_client = tx.groupby("cl_id", sort=True)
    # channel_type is one value per client (on all of its transactions): a client attribute, kept as one column
    channels = by_client["channel_type"].agg(["first", "nunique"])
    assert (channels["nunique"] <= 1).all(), "one channel type per client"
    overall = pd.DataFrame(
        {
            "n_transactions": by_client.size(),
            "amount_sum": by_client["amount"].sum(),
            "amount_mean": by_client["amount"].mean(),
            "amount_std": by_client["amount"].std(),
            "channel_type": channels["first"],
        }
    )
    blocks = [
        per_value_stats(tx, "trx_category", list(TRX_CATEGORIES), "trx"),
        per_value_stats(tx, "currency_code", [*CURRENCIES.values(), OTHER], "currency"),
        per_value_stats(tx, "mcc", [*mcc_values, OTHER], "mcc"),
    ]
    distinct = pd.DataFrame(
        {
            "nunique_mcc": by_client["MCC"].nunique(),
            "nunique_currency": by_client["currency"].nunique(),
            "nunique_trx_category": by_client["trx_category"].nunique(),
        }
    )
    # The dates of the first and last transaction, and the estimated end of the discount period (curation_comments,
    # "Time"): three months after the first transaction, or the last transaction when that is later.
    first = by_client["time"].min().dt.normalize()
    last = by_client["time"].max().dt.normalize()
    three_months_on = first + pd.DateOffset(months=DISCOUNT_MONTHS)
    dates = pd.DataFrame(
        {
            "first_transaction": first,
            "last_transaction": last,
            "period_end": last.where(last > three_months_on, three_months_on),
        }
    )
    labels = by_client[["target_flag", "target_sum"]].agg(["min", "max"])
    assert (labels.xs("min", axis=1, level=1) == labels.xs("max", axis=1, level=1)).all().all(), "one label per client"
    labels = labels.xs("min", axis=1, level=1)
    return pd.concat([overall, *blocks, distinct, time_features(tx), dates, labels], axis=1)


class Rosbank1(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Will a bank client stop using the bank's card in the three months after its introductory period?"),
        use_case=(
            "At the end of a client's three-month introductory period on a Rosbank card, the bank scores the risk "
            "that the client stops using it, for example to make a retention offer; the model is refit, for example "
            "every month."
        ),
        row=(
            "One client of Rosbank, a Russian bank, whose introductory period ended by December 2017, with the card "
            "transactions of that period (4,791 clients)."
        ),
        predicted=(
            "Whether the client makes no card purchases in the three months after the period (churn); in the October "
            "2017 window 179 of 515 clients did."
        ),
        known=(
            "Summaries of the client's card transactions up to the end of the period (counts, and sums, means and "
            "spreads in rubles, by transaction type, currency and the 97 most frequent merchant categories), when and "
            "how regularly the client was active (the competition winner's time features), the dates of the first and"
            " last transaction, and the client's channel type (undocumented; constant per client, read as how the "
            "client was acquired)."
        ),
        split=(
            "Each test window is one month of period ends (October, November, December 2017); training holds the "
            "clients whose three-month outcome was known before the window starts."
        ),
        changes=(
            "We summarise the transactions in rubles, add the competition winner's time features, rebuild each "
            "period's end date from the first and last transactions, and "
            "split by it, where the competition split clients at random; periods ending from January 2018 on are left"
            " out as their outcome window may not be complete."
        ),
        fit="approximate",
        fit_reason=(
            "How the label window was placed is not published, and the newest rows contradict 'after the period' "
            "(clients whose period had not ended when the data stops still have full spend labels). The period end "
            "dates are reconstructed from the transactions, as the data has no dates. The test windows are small (63 "
            "to 515 clients) and the two newest are a thin tail of the client intake."
        ),
    )

    # Dataset
    unique_name = "rosbank1"
    year = "2018"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://boosters.pro/championship/rosbank1/overview"
    license = (
        "None stated: the competition rules (boosters.pro API, `regulations`) and the Hugging Face card give no data "
        "licence"
    )
    download_description = """
        Rosbank released the data on boosters.pro for its ML Competition (27 April to 28 May 2018). The competition page (https://boosters.pro/championship/rosbank1/overview) is a JavaScript app whose content (name, dates, task texts, metrics, rules, leaderboards) comes from https://boosters.pro/api/champ/champ?champname=rosbank1; it lists no data files (checked 2026-10-07). The pytorch-lifestream team (Sber AI Lab, authors of the CoLES paper that uses the data) keeps the competition files on Hugging Face (dllllb/rosbank-churn, now pytorch-lifestream/rosbank-churn; earlier as rosbank-ml-contest-boosters.pro.zip on Yandex Cloud, now removed). The decompressed train.csv (33,672,402 bytes, sha256 cd19fe2557a4364f85a27a248ca68cb06efcd2e0642cea98d9319e1e8f90e392) is byte-identical to the copies participants put on GitHub in 2018: kianya/rosbank-competition (data/train.csv, committed 2018-10-26) and Ikitan/ML-Rosbank-competition (train.csv). We download the labelled file at a pinned revision; test.csv.gz (518,376 transactions of 5,217 clients, no labels) is not used.

        mkdir -p local-data-warehouse/rosbank1
        wget -O local-data-warehouse/rosbank1/train.csv.gz https://huggingface.co/datasets/pytorch-lifestream/rosbank-churn/resolve/aad1b512deaee7ffea4c289e496785bc9e17bd80/train.csv.gz

        train.csv.gz: 4,646,502 bytes, sha256 fe27320183acbe038577080ae8b30b9d7f7b8a40dd92cf43e405b56fdd6627f6 (the Git LFS object id on Hugging Face); 490,513 transactions of 5,000 clients.

        The Bank of Russia's official exchange rates (open on its site, no login; downloaded 2026-10-26): its currency list, and the daily rates of 1 September 2016 to 3 April 2018 of the 30 currencies in the data it quoted then (series ids from the list; the other 27 currencies return no rates for these dates).

        cd local-data-warehouse/rosbank1
        curl -fo cbr_currencies.xml https://www.cbr.ru/scripts/XML_valFull.asp
        mkdir -p cbr_rates && for id in R01010 R01020A R01035 R01060 R01090B R01100 R01115 R01135 R01200 R01215 R01235 R01239 R01270 R01335 R01350 R01370 R01375 R01500 R01535 R01565 R01585F R01625 R01700J R01720 R01760 R01770 R01775 R01810 R01815 R01820; do
            curl -fo cbr_rates/$id.xml "https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/09/2016&date_req2=03/04/2018&VAL_NM_RQ=$id"
        done

        cbr_currencies.xml: sha256 b6bc755432f5f3cfa8827496263ce6978a0382ae24c7a1b9ff2568406e6d7ec3 (the list grows when the Bank adds a currency; the 30 ids above are what the definition needs). The 30 rate files concatenated in name order (cat cbr_rates/*.xml | sha256sum): 50cbff2632b63e7f9e0c9b461c6fa47d717f5b5854d9e1f202c485018bd9b339.
    """
    bibtex = r"""
        @misc{Rosbank2018MLCompetition,
          author = {{Rosbank}},
          title = {Rosbank {ML} Competition},
          year = {2018},
          howpublished = {\url{https://boosters.pro/championship/rosbank1/overview}},
          note = {Data science competition on Boosters.pro, 27 April to 28 May 2018; task 1 churn (ROC AUC), task 2 POS spend (RMSE); files mirrored at https://huggingface.co/datasets/pytorch-lifestream/rosbank-churn}
        }
    """
    curation_comments = """
        We start with train.csv.gz of Rosbank's ML Competition on Boosters.pro (2018), from the pytorch-lifestream mirror on Hugging Face: 490,513 card transactions of the 5,000 labelled clients. One row is one client.

        - Prediction point: the end of a client's three-month grace period of Rosbank's card (the task text: "3 months of privileged usage"). Known then: the client's card transactions up to that day.
        - Task: churn, the competition's task 1, as in CoLES (Babaev et al. 2022). target_flag is 1 exactly when target_sum, the POS spend of the next three months, is positive (decision table): churn "Yes" is target_flag 0, and target_sum is dropped.
        - Tabular framing: for this sequence data, the tabular baseline in the literature is LightGBM on hand-crafted aggregates (CoLES, Sec. 4.1.2, Table 6: ROC AUC 0.825, level with the supervised sequence model at 0.817, above CPC, RTD and SOP at 0.782 to 0.802, and below CoLES embeddings fed to LightGBM at 0.843). We build them as pytorch-lifestream configures them for this dataset (`aggregate_transactions`).
        - Features, where we deviate from that configuration: all 10 transaction categories and four currency values (rubles, euros, US dollars, "other") get their own columns, against its 7 categories and 1 currency; the 97 most frequent MCC codes plus "other", as there. A mean or standard deviation over no transactions or of one transaction is missing (the configuration writes 0).
        - Time features of the 1st place (Lennart, CC 2026-10-26, CLEAN-19: the better of the baseline and the top solutions' features, or a reasonable combination): Kirill Khrylchenko won task 1 (private ROC AUC 0.8747) and published his code (github.com/KhrylchenkoKirill/rosbank, no licence; `time_features` is our rewrite, no code copied). His time block, which his slides rank as his best: for all transactions, each category, money in and money out, the span, spread, position and gaps of the client's active days, the same over the last active calendar month, the active days per month and the quarter of the last month (351 columns; two last-month gaps of cash advances copy the whole history's here and are dropped). Untuned LightGBM on our three windows: CoLES 0.857, CoLES plus the time block 0.896 (+0.038; October, 515 clients, +0.051). His full feature set scored lower than this combination (0.882), and his money and MCC blocks add nothing to CoLES (-0.016 to +0.004); his MCC-time block needs his 11 hand-made MCC groups and is not taken. Deviations from his code: days counted in days (not years of 360 days), unique active days per group, the last month and the months by year and month, the quarter as one number, and missing where he writes 0.
        - The 97 MCC codes are the most frequent over all transactions, test windows included: a pipeline choice that approximates the task (a deployed model would choose from its own history), not a value computed from test rows; kept (Lennart, 2026-10-19).
        - channel_type is undocumented (the competition publishes no column descriptions); it is constant per client and read as the acquisition channel (a participant notebook, kianya/rosbank-competition, says so), so it is one categorical column (decision table).
        - Time: the data has no period dates. Most clients transact over 80 to 92 days, so period_end, the time column, is the first transaction plus three months, or the last transaction when that is later (decision table). first_transaction and last_transaction are features. All three are dates, as POS transactions carry a date only. For the clients at first plus three months the estimate is an upper bound of the true period end (a period that started before the first transaction ends earlier), so it errs on the safe side for the gap. The transactions in the file are not in the label window: 107 of the 479 clients with a POS purchase after first plus three months still churned.
        - Cohort: how the label window was placed is not published, and the newest labels are off: 24 of the 36 clients whose period ends in March 2018 churned, against 35.5% for October 2017 to February 2018, while 37 of the 63 clients whose period ends from April 2018 on, after the transactions stop (2 April 2018), have full spend labels that a window after their period could not hold. We keep the periods ending before 1 January 2018, whose three-month window after the period closes by 31 March 2018, inside the transactions (decision table). A window fixed in calendar time would make churn rise with cohort age; in channel type1 (two thirds of the clients) it does not (logit slope +0.006 per month, SE 0.013, with activity controls; panel review 2026-10-20), so we read the window as per client.
        - Split: temporal on period_end, with each training client's three-month label window as a gap (splits_comment; decision table).
        - Not used: test.csv.gz (no labels), PERIOD (the month of TRDATETIME) and cl_id, which carries the label (alone ROC AUC 0.728).
        - Currencies (Lennart, CC 2026-10-26, CLEAN-21): amount is in the transaction's own currency (2.6% of transactions are not in rubles, 1,072 clients have one, and the largest amounts are Vietnamese dong and Indonesian rupiah, up to 35.8 million), where CoLES adds them up as one unit. We convert it to rubles at the Bank of Russia's official rate in force on the transaction's day (a rate holds until the next one is set, so a weekend takes the last rate before it); the rate is public on that day, before the prediction point. currency holds ISO 4217 numeric codes, rubles as 810 (the ruble's code before 1998) and in 32 rows as 643 (the current code). The data has no codebook; the conversion confirms the reading (decision table: converted, the median POS purchase of every currency with 30 or more lies between 355 and 3,346 rubles, against 500 in rubles and 8 to 671,000 units before). The Bank quoted 30 of the 57 other currencies then. The 1,466 transactions (0.3%, of 184 clients) in a currency it did not quote on their day (27 currencies: Thai baht, UAE dirham, Georgian lari, Croatian kuna, rupiah, dong and smaller ones; Hong Kong dollars before April 2017) keep their counts but leave the amount statistics, rather than take a rate from another source. Every amount column changes; the counts do not. std_amount_trx_CASH_ADV is dropped: of the kept clients only one has two or more cash advances in a quoted currency, so it holds one value.
        - Duplicates: 828 transaction rows repeat another row; we count them, as POS transactions carry a date only. Two pairs of clients share all aggregates, the label and period_end, so each pair falls on one side of every split; we keep them.
        - Note: the task probes flag `no_spread` (LightGBM leads linear by 0.017 AUC, a skill gap of 0.034 with paired standard error 0.087), a gap 3 windows cannot test; we keep the task.
    """

    # Task
    target = "churn"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC - Area Under the ROC Curve (task 1, churn); task 2 POS spend used RMSE",
        reference="https://boosters.pro/api/champ/champ?champname=rosbank1 (metric: 'AUC', checked 2026-10-21)",
        definition=(
            "Area under the ROC curve; our label churn = target_flag 0 is the competition label flipped, and "
            "AUC is unchanged under the flip of both label and score."
        ),
    )

    # Splits: monthly windows of the period end after a 3-month gap (the label window), down to half of the clients.
    temporal = Temporal(
        on="period_end",
        splits=TemporalSplits(window=1, unit="months", gap=LABEL_MONTHS, min_train_fraction=0.5),
    )
    accepted_check_warnings = {
        "splits_rows_unused": "The 524 clients whose period ends in September 2017 fall in the three-month label gap "
        "of every window: the newest window (December 2017) trains on the periods that ended by 31 August 2017, the "
        "last whose outcome is known when it starts.",
    }
    splits_comment = """
        A churn model is refit, for example every month, and scores the clients whose grace period ends in that month. A client's label covers the three months after its period, so it is known three months after period_end: each window trains on the clients whose period ended at least three months before the window starts. Windows of one calendar month of period_end, newest first: December 2017 (63 clients, 23 churned), November 2017 (123, 49) and October 2017 (515, 179), training on 3,566, 3,078 and 2,559 clients. A fourth window (September 2017) would train on 44% of the clients, below the 50% floor, and two-month windows would leave one window above it. The periods ending from January 2018 on are not in the dataset (curation_comments, "Cohort"). The client intake drops after July 2017 (first transactions 400 to 800 a month, then about 50 to 110), so November and December are a thin tail of late or irregular clients; the period end is estimated from the last transaction for 11%, 29% and 38% of the October, November and December clients. Every test label window spans the New Year and no training label window does. The competition split its clients at random (its unlabelled test file covers the same months); this split mirrors the refit, and on the same test windows a random training side scores about 0.01 AUC higher, while 3 x 3 random folds score lower (0.817 against 0.860) as the later clients are easier to score.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {"transactions": pd.read_csv(raw_dir / TRANSACTIONS_FILE), "rates": read_ruble_rates(raw_dir)}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        tx = raw["transactions"]
        # amounts in rubles at the Bank of Russia's rate of the day; a currency it did not quote is masked
        # (curation_comments, "Currencies")
        df = aggregate_transactions(tx.assign(amount=in_rubles(tx, raw["rates"])))
        # target_flag is 1 exactly when target_sum (the POS spend of the next three months) is positive: a churned
        # client has no POS purchase in the three months after the discount period
        assert ((df["target_flag"] == 1) == (df["target_sum"] > 0)).all(), "target_flag is target_sum > 0"
        df["churn"] = df["target_flag"].map({0: "Yes", 1: "No"})
        # clients whose three-month label window may not be complete in the labels (curation_comments, "Cohort")
        df = df[df["period_end"] < pd.Timestamp(LABELS_COMPLETE_BEFORE)]
        # target_sum is the other task's target and defines target_flag; the source's cl_id carries the label
        # (curation_comments, "Not used"). Cash advances are rare: of the kept clients only one has two or more in a
        # quoted currency, so their standard deviation is one value (curation_comments, "Currencies"), and the clients
        # with two or more cash advance days have them in one month, so the last month's gaps copy the whole history's.
        cash_advance = ["std_amount_trx_CASH_ADV", "time_cash_adv_lastmonth_gap_max", "time_cash_adv_lastmonth_gap_min"]
        return drop_columns(df.reset_index(), ["cl_id", "target_flag", "target_sum", *cash_advance])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["channel_type"],
            datetime=["first_transaction", "last_transaction", "period_end"],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        tx = raw["transactions"]
        clients = tx.groupby("cl_id", sort=True)[["target_flag", "target_sum"]].first()
        labels = pd.crosstab(clients["target_flag"], clients["target_sum"] > 0)
        labels.columns = [f"target_sum {'> 0' if positive else '= 0'}" for positive in labels.columns]

        # the period_end of all 5,000 clients (as in `aggregate_transactions`), for the months around the cut
        dated = tx.assign(time=pd.to_datetime(tx["TRDATETIME"], format=TIME_FORMAT).dt.normalize())
        first = dated.groupby("cl_id", sort=True)["time"].min()
        last = dated.groupby("cl_id", sort=True)["time"].max()
        three_months_on = first + pd.DateOffset(months=DISCOUNT_MONTHS)
        period_end = last.where(last > three_months_on, three_months_on)
        recent = period_end >= pd.Timestamp("2017-10-01")
        end_month = period_end[recent].dt.to_period("M").rename("period_end month")
        cut = pd.DataFrame(
            {
                "clients": end_month.groupby(end_month).size(),
                "churn share": clients.loc[recent, "target_flag"].eq(0).groupby(end_month).mean().round(3),
                "label window ends": (end_month.groupby(end_month).first() + LABEL_MONTHS).astype(str),
                "kept": end_month.groupby(end_month).first() < pd.Period(LABELS_COMPLETE_BEFORE, freq="M"),
            }
        )

        churned = df["churn"] == "Yes"
        month = df["period_end"].dt.to_period("M").rename("period_end month")
        months = pd.DataFrame(
            {
                "clients": month.groupby(month).size(),
                "churn share": churned.groupby(month).mean().round(3),
                "type2 share": df["channel_type"].eq("type2").groupby(month).mean().round(3),
            }
        )

        channel = df["channel_type"].astype(object).where(df["channel_type"].notna(), "missing").rename("channel_type")
        channels = pd.DataFrame(
            {"clients": channel.groupby(channel).size(), "churn share": churned.groupby(channel).mean().round(3)}
        )
        most = int(tx.groupby("cl_id")["channel_type"].nunique(dropna=False).max())

        span = (df["last_transaction"] - df["first_transaction"]).dt.days
        bucket = pd.cut(
            span, [-1, 30, 79, 92, 100, max(span.max(), 101)], labels=["0-30", "31-79", "80-92", "93-100", "over 100"]
        )
        bucket = bucket.rename("days from first to last transaction")
        later = df["last_transaction"] > df["first_transaction"] + pd.DateOffset(months=DISCOUNT_MONTHS)
        spans = pd.DataFrame(
            {
                "clients": bucket.groupby(bucket, observed=False).size(),
                "period_end = last transaction": later.groupby(bucket, observed=False).sum(),
                "churn share": churned.groupby(bucket, observed=False).mean().round(3),
            }
        )
        # amounts in rubles: the median POS purchase per currency, before and after the conversion
        pos = tx.assign(rubles=in_rubles(tx, raw["rates"]))[tx["trx_category"] == "POS"]
        currencies = pos.groupby("currency").agg(
            transactions=("amount", "size"), median_amount=("amount", "median"), median_rubles=("rubles", "median")
        )
        currencies = (
            currencies[currencies["transactions"] >= 30]
            .sort_values("transactions", ascending=False, kind="stable")
            .round(1)
        )
        currencies.columns = ["POS transactions", "median amount", "median in rubles"]
        return [
            Decision(
                "churn is target_flag 0: no POS purchase in the three months after the period",
                f"target_flag is 1 exactly when target_sum, the POS spend of the next three months (the competition's "
                f"task 2), is positive ({len(clients):,} labelled clients). target_sum defines the label and is dropped.",
                labels,
            ),
            Decision(
                "Periods ending from January 2018 are dropped: their labels may not be complete",
                "How the label window was placed is not published. Churn of the periods ending in March 2018 is far "
                "above the months before, and periods ending from April 2018 on end after the transactions (2 April "
                "2018) yet have labels. A three-month window after a period that ends in 2017 closes by 31 March 2018, "
                "inside the transactions.",
                cut,
            ),
            Decision(
                "Temporal split on the estimated period end, with a three-month gap",
                "Churn falls and the share of channel type2 rises over the periods. A refit model trains only on "
                "clients whose three-month outcome is known; the test windows are December, November and October "
                "2017.",
                months,
            ),
            Decision(
                "channel_type is one column per client",
                f"No client has more than {most} channel type on its transactions (missing counted as a value), so "
                "the channel type is a client attribute and not a transaction code to aggregate.",
                channels,
            ),
            Decision(
                "The period end is three months after the first transaction, or the last transaction when later",
                "The data has no period dates; most clients transact over 80 to 92 days, the three months of the "
                "discounted period.",
                spans,
            ),
            Decision(
                "Amounts in rubles at the Bank of Russia's rate of the day; currencies it did not quote are masked",
                "currency holds ISO 4217 numeric codes (810 and 643 are rubles): converted at the official rate, the "
                "median POS purchase of each currency lands near the ruble one, where the amounts as recorded range "
                "over five orders of magnitude. A missing median: the Bank set no rate for the currency on those days.",
                currencies,
            ),
        ]
