"""Curated dataset definition for `turkcell_radio_link_failure_prediction_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
    set_missing,
)

TABLES = ("rl-kpis", "rl-sites", "met-forecast", "met-real", "met-stations", "distances")
"""The tables of RegionA.zip the task reads (all six)."""

COUNTERS = ("unavail_second", "bbe", "error_second", "severaly_error_second")
"""The day's counters that the training release sometimes writes in thousands with a decimal point ("22.425" for
22,425): seconds and block counts are whole numbers, so a value with a decimal part is in thousands (PROV-13)."""

OBSERVED = {
    "observed_precipitation": ("precipitation", lambda hours: hours.sum(min_count=1)),
    "observed_precipitation_max": ("precipitation", "max"),
    "observed_wind_speed_max": ("wind_speed", "max"),
    "observed_temp": ("temp", "mean"),
    "observed_humidity": ("humidity", "mean"),
    "observed_pressure": ("pressure", "mean"),
}
"""The day's observed weather from met-real.tsv's hourly rows: name -> (source column, daily aggregate); a day
without a reading stays missing, also for the rain total."""

LINK = ("site_id", "mlid")
"""One end of a microwave link: the site that reports it and the link id. Turkcell's notebook joins the label on the
date, `site_id` and `mlid`; `mlid` alone is unique per day too."""

FORECAST_VARIABLES = ("weather", "temp_max", "temp_min", "humidity_max", "humidity_min", "wind_dir", "wind_speed")
"""The seven values a forecast report gives for each of its five days (`<variable>_day<k>`)."""

FORECAST_DAYS = 5
"""A report dated r holds forecasts for r+1 to r+5: `day<k>` matches the observed weather of r+k best (daily maximum
temperature, mean absolute error 2.86 against 3.53 for r+k-1 and 3.77 for r+k+1, day 1 of the evening reports)."""


def _next_day_failure(kpis: pd.DataFrame) -> pd.Series:
    """The failure flag of the same link end on the next day, aligned to `kpis` (missing where the next day has no row)."""
    nxt = kpis[[*LINK, "datetime", "rlf"]].assign(datetime=kpis["datetime"] - pd.Timedelta(days=1))
    merged = kpis[[*LINK, "datetime"]].merge(nxt, on=[*LINK, "datetime"], how="left", validate="one_to_one")
    return pd.Series(merged["rlf"].to_numpy(), index=kpis.index)


def _repair_counters(kpis: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """The counters in one unit (seconds, blocks) and a mask of the rows the repair touched.

    A counter with a decimal part is in thousands. On ENK rows the unavailable seconds are also in thousands when they
    and `avail_time` (thousands of seconds) add up to the day's 86.4, though they look whole.
    """
    kpis = kpis.copy()
    touched = pd.Series(False, index=kpis.index)
    for col in COUNTERS:
        thousands = (kpis[col] % 1).abs() > 1e-9
        kpis.loc[thousands, col] = kpis.loc[thousands, col] * 1000
        touched |= thousands
    whole_day = (
        (kpis["type"] == "ENK")
        & (kpis["unavail_second"] > 0)
        & ~touched
        & ((kpis["avail_time"] + kpis["unavail_second"] - 86.4).abs() < 1e-6)
    )
    kpis.loc[whole_day, "unavail_second"] = kpis.loc[whole_day, "unavail_second"] * 1000
    return kpis, touched | whole_day


def _observed_weather(met_real: pd.DataFrame, distances: pd.DataFrame) -> pd.DataFrame:
    """The day's observed weather at each site's nearest station of met-real.tsv, one row per (`site_id`, day)."""
    hourly = met_real.assign(day=pd.to_datetime(met_real["datetime"]).dt.floor("D"))
    daily = hourly.groupby(["station_no", "day"]).agg(**OBSERVED).reset_index()
    sites = [name for name in distances.index if name.startswith("RL_")]
    nearest = distances.loc[sites, sorted(hourly["station_no"].unique())].idxmin(axis=1)
    link = pd.DataFrame({"site_id": sites, "station_no": nearest.to_numpy()})
    return link.merge(daily, on="station_no").drop(columns="station_no")


def _nearest_forecast_station(distances: pd.DataFrame, forecast_stations: list[str]) -> pd.DataFrame:
    """Each site's nearest station among those that publish forecasts, with the distance to it."""
    sites = [name for name in distances.index if name.startswith("RL_")]
    to_stations = distances.loc[sites, forecast_stations]
    return pd.DataFrame(
        {
            "site_id": sites,
            "station_no": to_stations.idxmin(axis=1).to_numpy(),
            "station_distance": to_stations.min(axis=1).to_numpy(),
        }
    )


def _forecast_for_next_day(forecast: pd.DataFrame) -> pd.DataFrame:
    """For each station and target day, the forecast of the latest report that covers it, with its lead in days.

    The rows are (`station_no`, `target_day`). A report dated r covers r+1 to r+5; the evening report of a date is
    taken over its morning report, and among reports that cover the target day the latest (the shortest lead) wins.
    A row of day d reads the target day d+1, so every report it reads is dated d or earlier: issued by the end of the
    row's day (LEAK-10).
    """
    reports = forecast.assign(
        report_date=pd.to_datetime(forecast["datetime"]),
        is_evening=(forecast["report_time"] == "evening").astype(int),
    )
    reports = reports.sort_values(["station_no", "report_date", "is_evening"], kind="stable")
    reports = reports.drop_duplicates(["station_no", "report_date"], keep="last")
    leads = []
    for lead in range(1, FORECAST_DAYS + 1):
        columns = {f"{v}_day{lead}": f"forecast_{v}" for v in FORECAST_VARIABLES}
        part = reports[["station_no", "report_date", *columns]].rename(columns=columns)
        part["target_day"] = part["report_date"] + pd.Timedelta(days=lead)
        part["forecast_lead_days"] = lead
        leads.append(part.drop(columns="report_date"))
    long = pd.concat(leads, ignore_index=True).sort_values(
        ["station_no", "target_day", "forecast_lead_days"], kind="stable"
    )
    return long.drop_duplicates(["station_no", "target_day"], keep="first")


class TurkcellRadioLinkFailurePrediction1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will this microwave backhaul link fail tomorrow, given its counters today and tomorrow's weather "
            "forecast at the nearest station?"
        ),
        use_case=(
            "Turkcell's network operations, at the end of each day, flag the backhaul links likely to fail the "
            "next day from the weather forecast and each link's counters, to assess the risk and act ahead (the "
            "source leaves the action open)."
        ),
        row=(
            "One end of one microwave link on one day in an anonymised Turkish region, 31 December 2018 to 24 "
            "December 2020 (about 2,700 link ends a day, 3,681 in all at 1,674 sites)."
        ),
        predicted=(
            "Whether the link end has a radio link failure the next day: Turkcell's rule for a day with at least "
            "120 unavailable seconds and at least 100 background block errors, on the counters in one unit (0.10% "
            "of link-days)."
        ),
        known=(
            "The link's equipment and configuration, the day's error, unavailability and received-level counters "
            "and failure flag, its site's height and land cover, the day's observed weather at the nearest observing "
            "station, and the latest forecast for the next day at the nearest station that publishes forecasts."
        ),
        split=(
            "Three four-month windows of 2020, newest first, one day apart from training; each trains on up to a "
            "random million earlier link-days, so the test links are links already seen, on days to come."
        ),
        changes=(
            "We repaired the counters written in thousands and recomputed the failure flag by Turkcell's rule, built "
            "the next-day label as Turkcell's example notebook does, added the day's observed weather, joined "
            "each site to its nearest forecast station through the distance table, took the latest forecast issued "
            "by the end of the day, and score the ranking of the links rather than the challenge's F1."
        ),
        fit="direct",
        fit_reason=(
            "The rows, inputs and windows mirror a daily risk review of the operator's own links, with only the "
            "forecast issued by then; the label is Turkcell's own rule on the next day's counters. Failures come in "
            "storms: 43% of them fall on 10 of 725 days, so a window's score rests partly on a few storm days."
        ),
    )

    # Dataset
    unique_name = "turkcell_radio_link_failure_prediction_1m"
    version_of = "turkcell_radio_link_failure_prediction"
    version_comment = """
        The full table holds 1,964,000 link-days. The oldest window trains on all 984,904 earlier rows; the two newer windows would train on 1,323,386 and 1,668,466. We sample per test window (v2 split protocol): each test window keeps all its rows (292,714 to 345,035, under the 500k budget), and a train side above 1M is a random 1M of the earlier rows outside the gap, stratified on the label, drawn in one random order for all windows; the frame keeps only the rows a split uses (1,963,348).
    """
    year = "2021"
    domain = "technology & internet"
    source = "GitHub"
    source_url = "https://github.com/Turkcell/ITU-AIMLin5GChallenge-2021"
    license = None  # the repository has no licence file; its README asks users to cite Aktas, Alemdar and Ergut 2022
    data_tags = ("Spatial",)
    download_description = """
        Turkcell's GitHub repository for the ITU AI/ML in 5G Challenge 2021 (problem ITU-ML5G-PS-012), pinned to the commit of 5 July 2022 (the newest):

        mkdir -p local-data-warehouse/turkcell_radio_link_failure_prediction && cd local-data-warehouse/turkcell_radio_link_failure_prediction
        BASE=https://raw.githubusercontent.com/Turkcell/ITU-AIMLin5GChallenge-2021/4938c53979d650f94d5208ff4cb977ea954b6907/RLF_Prediction_ITU_AIML_Challenge_Data
        wget $BASE/RLF_Prediction_ITU_AIML_Challenge_Data.7z $BASE/ReadMe_RLF.txt $BASE/TurkcellExampleProject.ipynb
        7z x RLF_Prediction_ITU_AIML_Challenge_Data.7z -otrain_7z   # or: uvx --from py7zr py7zr x RLF_Prediction_ITU_AIML_Challenge_Data.7z train_7z
        unzip train_7z/RLF_Prediction_ITU_AIML_Challenge_Data/RegionA.zip -d RegionA

        The definition reads all six tables of RegionA: rl-kpis.tsv, rl-sites.tsv, met-forecast.tsv, met-real.tsv, met-stations.tsv and distances.tsv. The test archive (RLF_Prediction_ITU_AIML_Challenge_Test.7z, four 20-day windows of 2021) was downloaded and unpacked into test_7z/ and test_2021*/ but is not read.
    """
    bibtex = """
        @article{aktas2022radiolinkfailure,
          title = {Towards 5G and beyond radio link diagnosis: Radio link failure prediction by using historical weather, link parameters},
          author = {Akta{\\c{s}}, Semih and Alemdar, Hande and Erg{\\"u}t, Salih},
          journal = {Computers \\& Electrical Engineering},
          volume = {99},
          pages = {107742},
          year = {2022},
          doi = {10.1016/j.compeleceng.2022.107742},
        }
    """
    curation_comments = """
        We start with RegionA.zip from Turkcell's repository for the ITU AI/ML in 5G Challenge 2021 (problem ITU-ML5G-PS-012): rl-kpis.tsv (one row per link end and day), rl-sites.tsv, met-forecast.tsv, met-real.tsv (hourly observations), met-stations.tsv and distances.tsv.

        - Prediction point: the end of day d, once the day's link counters are in. A row is one link end on day d with that day's counters, and the label is its failure flag on day d+1 (LEAK-10: nothing from d+1 is an input).
        - Year: 2021, when Turkcell first shared these files (the commit "add dataset" of 28 June 2021). The 2020 challenge (ITU-ML5G-PS-036) used another region (the ITU archive: "the data belongs to a new region").
        - Counters repaired (PROV-13, PROV-14): the training release writes some counters of 1,000 or more in thousands with a decimal point ("22.425" for 22,425 s): `unavail_second` has 2,637 such rows (its whole numbers stop at 999), `bbe` 4,101, `error_second` 328, `severely_error_second` 26; on ENK rows `avail_time` (thousands of seconds) and `unavail_second` add up to 86.4 when the outage is in thousands too. Seconds and block counts are whole, so a value with a decimal part is multiplied by 1000, and the ENK rows of that identity as well (6,723 rows touched). Turkcell's 2021 test release writes plain seconds up to 86,400, and there its `rlf` equals the rule on 125 of 125 flagged rows. The published `rlf` was computed on the damaged numbers and is never set on a damaged row, so it misses the long outages: the rule on the repaired counters gives 2,052 failure days against the published 1,219. `rlf_today` is recomputed by the rule; it equals the published flag on every row the repair leaves alone (asserted in `_clean`). `avail_time` stays as published (thousands of seconds on 95% of rows, 900.0 on 867 rows, sums above 86.4 of unknown meaning).
        - Label: `fails_next_day` is Yes when the same link end (`site_id`, `mlid`) fails Turkcell's rule on day d+1, Turkcell's "1-day-predict" on the repaired counters: 2,011 of 1,963,348 rows (0.10%; the notebook's flag gives 1,204), 946 link ends. A failure of a hop shows at both its ends on 477 of 1,451 failing hop-days, so a third of the hop events count twice (USE-5: the link end is the unit Turkcell labels and queries). The 28,986 rows whose link end has no row on day d+1 have no label and leave; 13 days of rl-kpis hold under 1,200 rows (19 days of the shipped frame, once those rows leave; reporting gaps, five of them on 2 to 6 October 2020), and December 2020 has about 2,630 link ends a day against 2,830 a year earlier; the failure rate does not fall at the release end (probe 13), as a one-day label cannot be censored by it. After a failure 6.4% of the rows lack a next day, against 1.4%, so a few failures may hide in the gaps.
        - Horizon: the next day, not the challenge's second label (any failure on d+1 to d+5), which the source scores alike (SPLIT-12, USE-5). On the published flag the five-day label's LightGBM leads the link's past failure rate by +0.10, +0.10 and -0.02 ROC AUC (the next day +0.22, +0.17, +0.04), counts one failure on up to five consecutive rows of a link, and needs five days of follow-up (about 111,000 rows lack it).
        - The last observation of the target stays: today's flag (`rlf_today`) and the counters it is ruled on (`unavail_second`, `bbe`) are known at the prediction point and read by the operator (TP-10). No longer history of the flag is built. Naive-profile test on the repaired label, newest window first, by ROC AUC, a regularised LightGBM (rate 0.05, 200 rows per leaf, 300 trees) over seeds 0 to 2: 0.80-0.86, 0.72-0.82 and 0.76-0.77; the link's training failure rate 0.694, 0.709 and 0.765; today's flag 0.51, 0.51 and 0.53. Leads over the rate +0.10 to +0.15 (day-block bootstrap SE 0.02-0.05), +0.01 to +0.10 (SE 0.02-0.05) and -0.01 to +0.01 (SE 0.03): ahead in the two newer windows, a tie in January to April. The model's spread over seeds (up to 0.10 in May to August) is as large as some leads: rare positives make a tree model unstable here. The 2021 winner (MLGrads, ranked first; its code is public) fit AdaBoost and XGBoost on point-in-time rows: the day's counters, today's flag, the day's observed weather and the forecast, no longer history; Turkcell's example model is a decision tree on the day's counters. The data paper's best model reads the history as a sequence (its abstract; the text is paywalled).
        - Weather station: each site's nearest station among the 11 with forecasts, through distances.tsv (`station_no`, `station_distance`, in the source's unit, likely km: 0.08 to 19.7, mean 3.5; 9 stations are nearest to some site), with its height and land cover. The 9 stations without forecasts are not used.
        - Forecast: from the latest report dated d or earlier (the evening one of a date before its morning one), the values for d+1 (`forecast_*`) and the report's lead (`forecast_lead_days`): 97.1% from a report dated d, 1.5% missing (no report within five days). `day<k>` of a report dated r is r+k: its daily maximum temperature matches the observed one of r+k best (mean absolute error 2.86, 2.96 and 3.10 for days 1 to 3, as forecasts 1 to 3 days ahead do). The report dated d belongs to the prediction point by the source: each window of Turkcell's 2021 test archive ships met-forecast reports dated up to its query day d (morning and evening) and none later, and the winner MLGrads joins the report dated d to row d. Its rain forecast loses skill smoothly with the lead (ROC AUC against the observed rain 0.72, 0.71, 0.70, 0.69 and 0.66 for days 1 to 5), with no jump at day 1 that a forecast issued on the target day would show.
        - Observed weather: met-real.tsv, hourly observations at 20 stations, aggregated to day d at the site's nearest observing station (`observed_*`: the rain total and hourly maximum, the maximum wind speed, the mean temperature, humidity and pressure; 5-8% missing, pressure 51%). The day's observations are complete at the end of day d, the prediction point; the source offers them as the "actual realizations" and the 2021 winner reads them. Their effect on a regularised LightGBM is within fit noise (with minus without, seed-matched, -0.10 to +0.05 ROC AUC; mean -0.015), so they stay as the source gives them (CLEAN-22).
        - Not read: the 2021 test archive, four 20-day windows four months after the release, whose query days have no labels, so the challenge's own test rows cannot be scored.
        - Identifiers kept as categories: `site_id` and `mlid` (the link end, the key of the challenge's query files) and `mw_connection_no` (the hop shared by a link's two ends). The test link ends are known: 94.6% to 98.6% of a window's rows have training rows of the same link end (USE-10).
        - Cleaning: `rxlevmax` (the maximum received level, dBm) is 0 on 80 rows, on links that are up, and at most -10 elsewhere: set to missing (CLEAN-10). `1024 QAM` merged into `1024QAM` (52,278 rows; both spellings run the whole period on both vendors, and four links switch from one to the other). `severaly_error_second` renamed `severely_error_second`, `rlf` `rlf_today`.
        - Kept as published: `card_type`, `freq_band` (f1 to f5), the site and link ids, all anonymised codes; `modulation` unordered: QAM sizes with vendor suffixes (`(QO)`, `*`, `_light*`) the source does not explain, so no single order; the land-cover classes of sites and stations unordered too, as they cross building height (low to very high) with density (sparse to dense) beside open land, trees, sea and industry (CLEAN-14).
        - Anomaly: failures come in storms. 43% of the 2,011 positives fall on 10 of 725 days. The newest window's 414 fall 79% on three days (159 on the row date 7 October 2020, after a five-day gap in which only NEC links reported); the other windows are spread (37% and 17% on their top three days). Within a day the model ranks links with ROC AUC 0.69-0.72, 0.73-0.78 and 0.75-0.77 (the link's rate 0.71, 0.71, 0.77; the forecast alone 0.44-0.52), so the pooled score also measures which days a model flags as stormy.
        - Metric: ROC AUC in place of the challenge's F1 of the failure class (the metric's reason).
    """

    # Task
    target = "fails_next_day"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The challenge scored the F1 of the failure class on hard labels for each horizon (ITU-ML5G-PS-012: "
            "'F1-scores of identifying at least one radio link failure in the next day'; Turkcell's example "
            "notebook: precision_recall_fscore_support with average='binary'), on one query day per window. "
            "Overruled on resolution (MET-4, evidence measured on the shipped splits; MET-10): on the repaired "
            "label every scorer's F1 is 0.000 to 0.06 a window and rests on 0 to 39 true positives; even the best "
            "threshold chosen on the test rows reaches at most 0.06; and the day-block bootstrap SEs (0.004 to 0.016) "
            "are as large as the differences between scorers, so F1 cannot order methods. ROC AUC separates them: "
            "a regularised LightGBM leads the link's own failure rate by +0.10 to +0.15 ROC AUC in September to "
            "December 2020 (SE 0.02 to 0.05). roc_auc is the binary fallback (MET-8); the imbalance alone is no "
            "reason for PR AUC (MET-9). As african_credit_scoring_challenge, whose Zindi F1 was overruled on "
            "2026-10-26."
        )
    )

    # Splits
    temporal = Temporal(
        on="date",
        splits=TemporalSplits(window=4, unit="months", n_windows=3, gap=1, gap_unit="days"),
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)
    splits_comment = """
        A model refit at the start of a window flags links for the days to come. The three test windows are the four-month thirds of 2020, newest first (1 September to 24 December, May to August, January to April): 2020 is the newest half of the rows, so the oldest window trains on 50.2%, and three is the number of folds a frame of this size gets. They hold 414, 250 and 156 positives on 55, 75 and 75 failure days; shorter windows would leave a few dozen in some (TP-9). Short weather windows (SPLIT-18) are for a weather quantity itself; here each row carries the forecast for its own next day, and the window is only how long a model runs before its refit. The gap is one day: the last training day's label is the first test day's flag, unknown at the refit (SPLIT-10). Each test window keeps all its rows; a train side above the budget is a random 1M of the earlier rows (version notes). Every test link end is a known one (USE-10).

        Protocol (LEAK-9): a method sees only its split's train rows and scores each test row on its own. A test row's label is the `rlf_today` of the same link end's row of the next day, which the test window holds (the link end is `site_id` and `mlid`), so reading other test rows gives the labels away: the next-day row of the same link end is in the same test window for 97% to 99% of test rows, its `rlf_today` equals the label on all of them, its counters alone give the label away too, and a window's daily count of positives can be read off the test rows (correlation 0.999). A valid result scores each test row on its own; a method that reads other test rows is called out and not benchmarked.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        # The tables are tab-separated with a row index in the first column; numbers above 999 carry thousands
        # separators ("1,349,988" in mw_connection_no).
        return {
            name: pd.read_csv(raw_dir / "RegionA" / f"{name}.tsv", sep="\t", index_col=0, thousands=",")
            for name in TABLES
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        raw_kpis = raw["rl-kpis"].assign(datetime=lambda d: pd.to_datetime(d["datetime"]))
        # 0. The counters in one unit, then today's flag by Turkcell's rule on the repaired counters. The published
        #    flag was computed on the counters written in thousands, so it misses the long outages; it must agree
        #    with the rule on every row the repair leaves alone.
        kpis, touched = _repair_counters(raw_kpis)
        rule = (kpis["unavail_second"] >= 120) & (kpis["bbe"] >= 100)
        assert (rule == kpis["rlf"])[~touched].all(), "rlf is no longer the rule on the counters left as published"
        kpis["rlf"] = rule
        # 1. The label: the failure flag of the same link end on the next day (Turkcell's "1-day-predict"). Rows
        #    whose link end has no row on the next day have no label and leave.
        nxt = _next_day_failure(kpis)
        df = kpis.assign(fails_next_day=nxt).loc[nxt.notna()].copy()
        df["fails_next_day"] = df["fails_next_day"].astype(bool)
        # 2. The site's ground height and land cover.
        sites = raw["rl-sites"].rename(columns={"clutter_class": "site_clutter_class"})
        df = df.merge(sites, on="site_id", how="left", validate="many_to_one")
        # 3. The weather station: the nearest of the stations that publish forecasts, through distances.tsv.
        forecast = raw["met-forecast"]
        nearest = _nearest_forecast_station(raw["distances"], sorted(forecast["station_no"].unique()))
        stations = raw["met-stations"].rename(
            columns={"height": "station_height", "clutter_class": "station_clutter_class"}
        )
        df = df.merge(nearest, on="site_id", how="left", validate="many_to_one")
        df = df.merge(stations, on="station_no", how="left", validate="many_to_one")
        # 4. The forecast for the next day from the latest report issued by the end of the row's day.
        df["target_day"] = df["datetime"] + pd.Timedelta(days=1)
        df = df.merge(
            _forecast_for_next_day(forecast), on=["station_no", "target_day"], how="left", validate="many_to_one"
        )
        # 4b. The day's observed weather at the site's nearest station of met-real.tsv, known at the end of the day.
        df = df.merge(
            _observed_weather(raw["met-real"], raw["distances"]),
            left_on=["site_id", "datetime"],
            right_on=["site_id", "day"],
            how="left",
            validate="many_to_one",
        ).drop(columns="day")
        # 5. Names: the date, today's failure flag, the source's typo.
        df = df.rename(
            columns={"datetime": "date", "rlf": "rlf_today", "severaly_error_second": "severely_error_second"}
        )
        # 6. A maximum received level of 0 dBm is no reading (every other one is -14 dBm or lower); one modulation
        #    written two ways.
        df = set_missing(df, {"rxlevmax": [0.0]})
        df["modulation"] = df["modulation"].replace({"1024 QAM": "1024QAM"})
        # 7. The label's classes in words (CLEAN-25), "Yes" the failure.
        df = decode(df, {"fails_next_day": {False: "No", True: "Yes"}})
        return drop_columns(df, ["target_day"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        positive = df["fails_next_day"] == "Yes"
        by_month = df.assign(month=df["date"].dt.strftime("%Y-%m"), positive=positive)
        days = by_month[positive].groupby("month")["date"].nunique()
        top = by_month[positive].groupby(["month", "date"]).size().groupby("month").max()
        table = by_month.groupby("month").agg(rows=("positive", "size"), positives=("positive", "sum"))
        table["failure days"] = days.reindex(table.index).fillna(0).astype(int)
        table["positives on the worst day"] = top.reindex(table.index).fillna(0).astype(int)
        kpis, _ = _repair_counters(raw["rl-kpis"].assign(datetime=lambda d: pd.to_datetime(d["datetime"])))
        kpis["rlf"] = (kpis["unavail_second"] >= 120) & (kpis["bbe"] >= 100)
        has_next = _next_day_failure(kpis).notna()
        gaps = (
            pd.DataFrame({"rlf today": kpis["rlf"], "has a next-day row": has_next})
            .groupby("rlf today")["has a next-day row"]
            .agg(rows="size", without_next_day=lambda s: int((~s).sum()))
        )
        gaps["share without a next-day row (%)"] = (100 * gaps["without_next_day"] / gaps["rows"]).round(2)
        return [
            Decision(
                "Positives per month: failures come in storms",
                "Each month's link-days, positives (a failure the next day), the days with a failure and the "
                "positives on the month's worst day. The three test windows are the four-month thirds of 2020.",
                table,
            ),
            Decision(
                "Rows without a next-day row leave (no label)",
                "A row whose link end has no row the next day has no label. After a failure a next-day row is "
                "missing more often, so a few failures may hide in the reporting gaps.",
                gaps,
            ),
        ]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            # The vendor (`type`), the end of the hop (`tip`), the anonymised ids and codes, today's flag, the land
            # cover classes and the forecast's weather words are fixed sets; the counters, heights, distance,
            # capacity and forecast numbers stay numbers (the wind direction in degrees, a cycle shipped as numbers).
            categorical=[
                "type",
                "tip",
                "mlid",
                "mw_connection_no",
                "site_id",
                "card_type",
                "adaptive_modulation",
                "freq_band",
                "modulation",
                "rlf_today",
                "site_clutter_class",
                "station_no",
                "station_clutter_class",
                "forecast_weather",
            ],
            datetime=["date"],
        )
