"""Curated dataset definition for `noaa_storm_events_damage` (data-foundry v2). Evidence: README.md."""

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

# The yearly details files read: 2007 is the first full year in the current entry format (History bullet)
FIRST_YEAR, LAST_YEAR = 2007, 2025
TARGET = "log1p_property_damage_usd"
# The episode narrative is not read; the event narrative only finds double entries and is dropped (LEAK-10, LEAK-19)
NOT_READ = ("EPISODE_NARRATIVE",)
IDS = ("EVENT_ID", "EPISODE_ID")
# DAMAGE_PROPERTY is a number with a magnitude letter ("10.00K"); a few values carry no letter and are dollars
MAGNITUDE_LETTER = {"K": 1e3, "M": 1e6, "B": 1e9}
# MAGNITUDE is the hail size in inches for these types and a wind speed in knots for the others (format document)
HAIL_TYPES = ("Hail", "Marine Hail")
# Hazards no one sends a damage assessor for (the domain practitioner's list, review issue 2): marine zones, drought,
# heat, cold, fog, rip current, funnel cloud, waterspout and high surf.
UNASSESSED = (
    "Drought",
    "Heat",
    "Excessive Heat",
    "Cold/Wind Chill",
    "Extreme Cold/Wind Chill",
    "Dense Fog",
    "Freezing Fog",
    "Rip Current",
    "Funnel Cloud",
    "Waterspout",
    "High Surf",
)
# Wind speeds the preparer estimated from the damage: gust (EG) and sustained (ES), NWSI 10-1605 Sec. 46.3
ESTIMATED = ("EG", "ES")
# Types whose begin and end the outcome alone sets (NWSI 10-1605 App. A): a tornado's ground contact, which the damage
# survey sets (Sec. 47), and the span of Strong Wind (Sec. 45) and Heavy Rain (Sec. 21), timed by the damage
OUTCOME_SPAN = ("Tornado", "Strong Wind", "Heavy Rain")


def _dollars(code: pd.Series) -> pd.Series:
    """Parse Storm Data's damage code ("10.00K", "1.55M", "0.00K", "0") into dollars; blank stays missing."""
    s = code.str.strip().str.upper()
    letter = s.str[-1]
    factor = letter.map(MAGNITUDE_LETTER).where(letter.isin(list(MAGNITUDE_LETTER)), 1.0)
    return pd.to_numeric(s.str.rstrip("KMB"), errors="coerce") * factor


def _local_time(yearmonth: pd.Series, day: pd.Series, hhmm: pd.Series) -> pd.Series:
    """The begin or end time from Storm Data's YYYYMM, DD and hhmm columns (local standard time, as published)."""
    return pd.to_datetime(yearmonth + day.str.zfill(2) + hhmm.str.zfill(4), format="%Y%m%d%H%M")


class NoaaStormEventsDamage(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much property damage, in dollars, did a storm event reported by the US National Weather Service "
            "cause in one county or forecast zone?"
        ),
        use_case=(
            "For example, a state hazard-mitigation planner estimates the property damage of storm events from what "
            "is known about each event before its damage is assessed (its type, place, season, size and cause), to "
            "plan where disaster resources and mitigation go, as Diaz and Joseph (2019) do for tornadoes "
            '"for science-informed tornado disaster planning".'
        ),
        row=(
            "One event of the NWS Storm Data archive in one US county or forecast zone, 2007-2025 (thunderstorm wind, "
            "hail, flood, tornado, winter storm and 29 other types), with a damage entry; the hazards no one sends a "
            "damage assessor for are left out."
        ),
        predicted=(
            "The property damage the NWS office entered for the event, in nominal dollars, shipped as log(1 + "
            "dollars); 68% of the entries are $0."
        ),
        known=(
            "The event type, the place (state, county or zone, forecast office, where county events began), when it "
            "began and, unless damage alone timed it, how long it lasted, a measured wind speed or the hail size, "
            "whether a wind report was measured or a damage report, and a flood's cause. The first report says "
            "whether damage was seen; some types are entered only with damage (3.5-4.0% of test rows)."
        ),
        split=(
            "The test data is a later calendar year (2023, 2024 or 2025), with every event published by the refit at "
            "the start of that year (all but the last three months) for training."
        ),
        changes=(
            "We drop the entries without a damage figure and 1,072 double entries. We drop the narratives, the "
            "tornado rating and path, the end point, casualties, crop damage, reporter and hurricane category, and "
            "blank the wind speeds estimated from the damage and the durations the damage sets (tornado, strong wind, "
            "heavy rain): all written from the damage, with it or after it. Wind speed and hail size get one column "
            "each."
        ),
        fit="approximate",
        fit_reason=(
            "A planner plans for kinds of events, while a row is one event in one county segment, described by "
            "Storm Data entries made weeks later (tornado types from damage surveys, some spans timed by damage). The "
            "label is the preparer's rough estimate, and a $0 means no damage or no estimate made, by a convention "
            "that differs by office and drifts over the years. No exposure (population, buildings) is given."
        ),
    )

    # Dataset
    unique_name = "noaa_storm_events_damage"
    year = "2026"
    domain = "environmental science & climate"
    source = "GOV Website"
    source_url = "https://www.ncei.noaa.gov/access/storm-events-database/"
    license = "Public Domain"
    data_tags = ("Spatial",)
    download_description = """
        # The yearly details files of the Storm Events Database (NOAA NCEI bulk CSV), as downloaded on 2026-10-30.
        # NCEI rewrites a year's file when it changes (the c-date in the name); _load_raw takes the one file per year.
        mkdir -p local-data-warehouse/noaa_storm_events_damage && cd local-data-warehouse/noaa_storm_events_damage
        for f in d2007_c20260323 d2008_c20260323 d2009_c20260323 d2010_c20260323 d2011_c20260323 \\
                 d2012_c20261026 d2013_c20260323 d2014_c20260323 d2015_c20260323 d2016_c20260323 \\
                 d2017_c20260519 d2018_c20260323 d2019_c20260323 d2020_c20260323 d2021_c20260323 \\
                 d2022_c20260625 d2023_c20260323 d2024_c20260728 d2025_c20260819; do
            wget https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_${f}.csv.gz
        done
        # Column documentation: Storm-Data-Bulk-csv-Format.pdf in the same directory; the preparation rules:
        # NWS Instruction 10-1605 (https://www.weather.gov/media/directives/010_pdfs/pd01016005curr.pdf).
    """
    bibtex = r"""
        @misc{ncei_storm_events_database,
          author = {{NOAA National Centers for Environmental Information}},
          title = {Storm Events Database},
          year = {2026},
          howpublished = {\url{https://www.ncei.noaa.gov/access/storm-events-database/}},
          note = {Bulk CSV files (details), 2007-2025, downloaded 2026-10-30 from https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/}
        }
    """
    curation_comments = """
        We start with the yearly details files 2007-2025 of NOAA NCEI's Storm Events Database (bulk CSV, one row per Storm Data event in one county, forecast zone or marine zone), the archive of the National Weather Service's Storm Data publication. The source defines no prediction task.

        - Prediction point: a storm has passed, the event has ended and is logged from the first reports (type, place, begin and end time, a measured wind speed or the hail size, whether damage was seen), before any damage survey, claim or damage estimate. Every column is checked against it. Strong Wind, Lightning and Thunderstorm Wind below 50 kt enter Storm Data only when they result in "a fatality, injury, or damage" (NWSI 10-1605, Sec. 29, 45 and 46): 3.5-4.0% of the test rows, 95-96% of them with damage. They stay, since the first report says whether damage was seen (LEAK-37). The numbers below are untuned LightGBM (400 trees) on the shipped features, trained on 2007 to September 2023 and tested on 2024, RMSE on the log1p target: 2.626 as shipped (scratch, 2026-11-01).
        - Target: `DAMAGE_PROPERTY`, coded as a number and a magnitude letter ("10.00K" = $10,000), parsed to dollars and shipped as log1p (`log1p_property_damage_usd`); the metric is computed on the dollars (`target_transform="log1p"`). Nominal dollars as entered, not adjusted for inflation.
        - Rows without a damage figure (blank `DAMAGE_PROPERTY`, 18% of the 1,225,290 events 2007-2025) have no target and are dropped. We read the blank as the "no information available" box ("either check the 'no information available' box, or make an estimate. The lone exception is for flood events", NWSI 10-1605, Sec. 2.7, p. 11): an inference, since the export of the box is not documented; Flood and Flash Flood have 26 blanks, all in 2007, and none from 2008 on. A $0 entry stays a 0. The curator's call (Andrej, 2026-10-30, zero-inflated review): "We don't care. We want to add any relevant predictive task, independent if it is zero inflated or not"; reading it as making $0 against blank a cleaning choice is the AI's.
        - Dropped as no assessment decision (USE-1; Andrej, 2026-11-03, review issue 2, the domain practitioner's list): every marine type and drought, heat, excessive heat, cold/wind chill, extreme cold/wind chill, dense fog, freezing fog, rip current, funnel cloud, waterspout and high surf: 156,767 entries with a damage figure (15.7%), 99.1% of them $0, with 0.5% of the dollars. The event type alone predicts their zeros, so they made the task look easier; the rows left are the hazards whose damage is assessed and planned for. On the rows left untuned LightGBM scores RMSLE 2.67, 2.93 and 2.94 (2025, 2024, 2023) against 4.05, 4.28 and 4.20 for a constant.
        - No storm-level input (review issue 4): the number of a storm's entries and counties (`EPISODE_ID`) changes untuned LightGBM's RMSLE by -0.010 to +0.001 counted over all its entries, and by -0.012 to +0.017 counted over the types entered whatever the damage (strong wind, lightning and thunderstorm wind under 50 kt enter Storm Data only with damage, 3.3% of the entries), so it adds no measurable signal and would carry part of the label.
        - Exposure (MET-14, MET-15; 2026-11-06): none. The target is the damage of one event as entered, not a count or an amount accrued over an amount at risk, so it ships without a rate, a weight or an offset. The source gives no population, building or insured value, and the one proxy tested, the county's population (Census estimate for 2020, county rows of 2016-2025), does not scale with the damage (Spearman -0.14 to +0.05 with the log damage among the positive entries of five types; exposure study of 2026-11-05). `duration_hours` is a span the outcome partly sets, not an exposure (below). The storms whose positive entries all carry one figure (2,063 of the 16,080 with two or more, 2016-2025) hold round office values (one of eight round amounts from $1,000 to $100,000 in 73.5% of them; one or two significant digits in every one with three or more entries), not a storm total split over its zones.
        - Anomaly: a $0 mixes "no damage" with "no estimate made" (13 of 121 EF4 and EF5 tornado segments, and 17.3% of EF2 and above, are at $0), and the mix is office practice: among Thunderstorm Wind entries the share at $0 runs from 7% to 91% between the 10th and 90th percentile of the 107 offices with 100 or more entries (decision table). It drifts: an office's 2024 share predicts its 2025 share at r 0.958 and its 2007-2016 share at r 0.575, and 30.5% of 82 offices moved by more than 0.2 from 2007-2021 to 2023-2025. The line between $0 and blank moves inside an office too: from 2007-2010 to 2022-2025, 70% of the rise in an office's Thunderstorm Wind blanks came out of its $0 entries (98 offices). The office (`wfo`) is a feature, so a model can learn the practice; it is not repaired. Kept under LEAK-25 as amended for this case (Andrej, 2026-11-02): a mix whose recording follows a reporting unit shipped as a feature stays, with the unit's spread and drift in the notes and fit approximate, as the task keeps a measured signal beyond the office, the period and the place; the blanks, the source's own 'not recorded' box, are dropped.
        - History: from 2007 on. In the files of 2000-2005, 70% to 72% of the events have no damage figure, 61% in 2006 (the year the files move from the PDS to the CSV entry format; in 2006 the PDS rows are 71.3% blank, floods 63.3%, the CSV rows 0.1%), then 7.3% in 2007, rising to 22-24% in 2022-2025, so the kept rows change composition; the positive damage drifts down within the kept years too (median of Thunderstorm Wind $5,000 in 2007-2017, $2,000 in 2025).
        - Dropped, written from the damage or recorded with it (LEAK-10): the narratives (the episode narrative is not read, the event narrative only finds double entries), `TOR_F_SCALE` (the Enhanced Fujita rating "describes the strength of the tornado based on the amount and type of damage", format document p. 4), `TOR_LENGTH`, `TOR_WIDTH` and the `TOR_OTHER_*` continuation fields (the path from the damage survey), the end point `END_LAT`, `END_LON`, `END_RANGE`, `END_AZIMUTH`, `END_LOCATION` (for a tornado the end of the surveyed path, for a wind swath "within the county where the wind damage swath exists", NWSI 10-1605, Sec. 46.1, p. A-68), the injuries and deaths, and the crop damage. Measured: with the rating, the path and the end point the RMSE falls from 2.626 to 2.596 (tornado rows 4.796 to 4.107); with the casualties and the crop damage to 2.561; two flags read off the event narrative (a dollar amount, a damage word such as "roof" or "downed") give 2.559.
        - Dropped (LEAK-10): `CATEGORY`, which the format document calls unknown. It is filled for the Hurricane (Typhoon) events only, 1 to 5, and set per zone: 23 of the 95 episodes with a category carry more than one value, and Hurricane Michael's Category 5 zone (2018) is the reanalysis of April 2019, after the event; NWSI 10-1605 (Sec. 25.3) pairs each category with the types of damage. 482 rows, none in 2025.
        - Dropped (LEAK-10): `SOURCE`, the reporter of the event. One of its values, "NWS Storm Survey" (about 23,700 entries, 72% with damage), is a damage survey the office makes after the event, and the column has no missing values, so blanking that value would leave the same marker; merged into "Unknown" (about 1,400 entries) it would hold it too (RMSE 2.559 merged and as published). The other reporters (a 911 call center, a utility, a trained spotter) are known at the first report, so the drop costs real signal: RMSE 2.626 without the column. The drop follows kick and expresso_churn_prediction.
        - Blanked (LEAK-10): the wind speeds the office estimated from the damage, `magnitude_type` "EG" (254,988 entries) and "ES" (the same for sustained wind, 1,162); the type stays. NWSI 10-1605, Sec. 46.3, p. A-69: the preparer "exercises professional judgment to determine the estimated maximum wind value based on observed structural or tree damage". Matched to the real-time Local Storm Reports of 2024 (same office, within 15 minutes and 10 km), 94.4% of 12,498 EG Thunderstorm Wind events had a first report "TSTM WND DMG" without a speed, while measured gusts kept their speed in 92.7% of cases and hail sizes in 97.9%. Whether a wind report was a damage report or a measured gust is in the first report, so `magnitude_type` stays and the blank follows it (no marker). Among entries with damage the estimate tracks the dollars (Spearman 0.46); on the EG and ES test rows the RMSE is 2.760 with it and 2.860 blank. The 24 impossible speeds (22 Thunderstorm Wind entries of 1-10 kt, 2 Strong Wind entries of 0 kt) are all estimates and go with them.
        - Blanked (LEAK-10): `duration_hours` where the outcome alone sets the span, by event type, not by reporter, so a blank is no survey marker. Tornado: a tornado begins and ends with the vortex's ground contact, which the damage survey sets (NWSI 10-1605, Sec. 47; 68% of the tornado rows come from "NWS Storm Survey"), and the duration tracks the dropped path length (Spearman 0.83 with `TOR_LENGTH`); on the tornado test rows the RMSE is 4.537 with it and 4.796 blank. Strong Wind and Heavy Rain (CC 2026-11-06, Lennart; 18,243 and 20,836 rows, 4.6%): App. A times them by the damage, Strong Wind from "When the wind started to cause a fatality, injury, or significant damage" to "When the wind no longer caused a fatality, injury, or significant damage" (Sec. 45), Heavy Rain from "When the heavy rain that led to damage began" until it "no longer posed a threat to life or property" (Sec. 21). Their blank costs nothing measurable: on their test rows RMSLE changes by -0.009, -0.018 and -0.046 (2023, 2024, 2025; untuned LightGBM on the shipped splits, mean of 4 bagging seeds, SD 0.03 to 0.06).
        - Potential leak, kept on purpose (CC 2026-11-06, Lennart): `duration_hours` of Thunderstorm Wind, High Wind, Coastal Flood, Lakeshore Flood and Storm Surge/Tide (318,813 rows, 37.8%), whose span App. A times by the damage or by a criterion without it. Thunderstorm Wind runs from "When damage first occurred or winds 50 knots (58 mph) or greater were first reported" to "When damage ended or winds of 50 knots (58 mph) were last reported" (Sec. 46), High Wind likewise with the high-wind criteria (Sec. 24), and the three floods from "When the water level began to cause damage or flooding" to "When the water level dropped to a point where damage or flooding ended" (Sec. 4, 27, 44). Which of the two set a given span is not recorded, so the part the damage set cannot be located row by row. The whole column is worth +0.012 to +0.021 RMSLE on these types' test rows (2023-2025, untuned LightGBM on the shipped splits, mean of 4 bagging seeds, SD 0.016 to 0.030; +0.001 to +0.015 on all rows), an upper bound on that part, against a gain of about 1.3 over a constant. Kept by the LEAK-10 / LEAK-37 Cases row of 2026-11-06 (a span drawn by the outcome or by a criterion without it stays, with its worth noted); revisit if Storm Data records which criterion timed an event.
        - Dropped as identifiers or copies: `EVENT_ID`, `EPISODE_ID`, `DATA_SOURCE` (constant from 2007); `YEAR`, `MONTH_NAME`, the begin and end date and time columns and `CZ_TIMEZONE` (in `begin_time` and `duration_hours`); `STATE_FIPS`, `CZ_FIPS`, `CZ_NAME` (in `county_zone`); `BEGIN_RANGE`, `BEGIN_AZIMUTH`, `BEGIN_LOCATION` (a place name and the offset from it, which `begin_lat` and `begin_lon` give); `MAGNITUDE` (in `wind_speed_kt` and `hail_size_in`).
        - Built: `begin_time` from `BEGIN_YEARMONTH`, `BEGIN_DAY` and `BEGIN_TIME` (local standard time, as published); `duration_hours` from the end columns the same way (end minus begin; none is negative, the longest are the 31-day entries of a month, such as Drought; blank where the outcome alone sets the span, above); `county_zone`, the state FIPS code, the zone type and the county or zone number (one code per county, forecast zone or marine zone); `hail_size_in` and `wind_speed_kt` from `MAGNITUDE`, which holds inches for Hail and Marine Hail and knots for the wind types (format document p. 4), one unit per column (a lossless split).
        - Dropped as double entries (LEAK-19): 1,072 rows equal to another row in every column but the event and episode ids, event narrative included, in every year and type (248 Thunderstorm Wind, 228 Hail).
        - Note: duplicate rows are kept otherwise: 0.6% of the rows (5,370) are copies of another row in every feature and the target, mostly forecast-zone entries of one storm in one zone at the same time (Heavy Snow, Winter Storm), which the source entered as separate events with their own narratives; with the same begin time they never fall on both sides of a window.
        - Note: zone events (40% of the rows) mostly have no begin latitude and longitude (37% of all rows lack them); their place is `county_zone` (8,135 codes).
        - Note: the same storm system appears as several events (one per county or zone, `EPISODE_ID` groups them, each storm entered by one office); no episode spans two months (0 of 167,629), so none crosses a window boundary.
        - Note: a year's file is rewritten when NCEI updates it. The 2024 files of 17 March 2025 and of 28 July 2026 agree on the damage of 99.83% of the 69,545 events in both (107 blanks filled, 14 values changed; 907 events, 1.3%, were added or removed), and 0 of the 64,921 damage values of January-October 2025 differ between the files of 16 January and 19 August 2026, so the newest year, 2025 (file of 19 August 2026), is settled (leak probe 13).
        - Licence: US Government work; NCEI's metadata (C00510) asks to "Cite dataset when used as a source" and warns that reports "may be unverified by the NWS".
        - CC (2026-11-06, Lennart): decision D13 of the exposure study (#51; review issue 6): `duration_hours` is blank for Strong Wind and Heavy Rain, whose span NWSI 10-1605 App. A draws by the damage (Sec. 45, 21), and kept with a note for Thunderstorm Wind, High Wind, Coastal Flood, Lakeshore Flood and Storm Surge/Tide, which it times by the damage or a wind or flooding criterion (Sec. 46, 24, 4, 27, 44), under the new LEAK-10 / LEAK-37 Cases row on spans the outcome sets. Supersedes the definition Andrej shipped on 2026-11-03, which blanked only the tornado durations, as the column audit of 2026-11-01 had read the begin and end of Thunderstorm Wind alone and judged the other spans first-report facts: the study of 2026-11-05 read App. A for every type and measured the column's worth on the seven damage-timed types (+0.02 to +0.04 RMSLE, trained from 2016). On the shipped splits it is +0.013 to +0.021 on those rows, all of it on the five kept types (+0.012 to +0.021) and none on Strong Wind and Heavy Rain.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason=(
            "NCEI and NWSI 10-1605 define no task or metric, and no competition was found. Diaz and Joseph (2019, "
            "Weather and Climate Extremes 25:100216, https://doi.org/10.1016/j.wace.2019.100216) model tornado damage "
            "from this database with several metrics (accuracy and AUROC for any damage, MSE on the log of the "
            "positive amounts), on tornadoes only and a random split: no source metric for this task (MET-5), but a "
            "log scale. The damage spans nine orders of magnitude ($0 to $17 billion): on the raw dollars the "
            "largest 0.1% of the entries hold 99.96% of the squared deviation, so RMSE would score a few hurricanes "
            "and floods. The manager ranks counties by orders of magnitude, so RMSLE on the dollars (RMSE on the "
            "shipped log1p). It takes the $0 entries: 37-47% of a model's squared error falls on them (untuned "
            "LightGBM, 3 windows), so the score also rewards telling a $0 entry from a small figure."
        ),
        target_transform="log1p",
    )
    accepted_check_warnings = {
        "task_target_value_dominant": (
            "Zero-inflated: 68% of the entries are $0, kept as entered; part of the zeros are unestimated damage "
            "(13 of 121 EF4 and EF5 tornado segments at $0; kept under LEAK-25 as amended, Andrej, 2026-11-02)."
        ),
    }

    # Splits: three calendar years, newest first, with a three-month gap for the publication delay
    temporal = Temporal(
        on="begin_time",
        splits=TemporalSplits(window=1, unit="years", cutoffs=(2023, 2024, 2025), gap=3, gap_unit="months"),
    )
    splits_comment = """
        A model refit at the start of each year estimates the damage of that year's events; the yearly cadence is ours (NCEI releases monthly). The test windows are the calendar years 2025, 2024 and 2023 (newest first), each a full cycle of the storm seasons (tornadoes in spring, hurricanes in autumn, winter storms), since storm damage is strongly seasonal and a shorter window would test one season. Each window trains on every earlier event from 2007 on except the last three months before it: a Storm Data month is certified "no later than 60 days after the end of the month" (NWSI 10-1605, Sec. 3), and NCEI's public files are "updated monthly with up to a 120 day delay possible" (C00510). In archived releases a month first appears complete 75-80 days after its end (the 2025 file of 16 January 2026 holds all of October 2025 and no November), so at a refit on 1 January the public files hold the events through September. Offices and counties recur across the years (SPLIT-13): the model estimates the damage of new events in known places.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        frames = []
        for year in range(FIRST_YEAR, LAST_YEAR + 1):
            files = sorted(raw_dir.glob(f"StormEvents_details-ftp_v1.0_d{year}_c*.csv.gz"))
            assert len(files) == 1, f"expected one details file for {year}, found {[f.name for f in files]}"
            frames.append(pd.read_csv(files[0], dtype=str, usecols=lambda c: c not in NOT_READ))
        return pd.concat(frames, ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. The target in dollars; entries without a damage figure are no task rows (notes)
        dollars = _dollars(df["DAMAGE_PROPERTY"])
        df = df[dollars.notna()].copy()
        df[TARGET] = np.log1p(dollars[dollars.notna()])
        # The hazards no one assesses go: the listed types and every marine type (review issue 2).
        df = df[~(df["EVENT_TYPE"].isin(UNASSESSED) | df["EVENT_TYPE"].str.startswith("Marine "))]
        # 2. Double entries: equal to another row in every column but the ids, event narrative included (LEAK-19)
        df = df.drop_duplicates(subset=[c for c in df.columns if c not in IDS], keep="first")
        # 3. Times: begin as a datetime, end as the duration in hours (local standard time, as published)
        begin = _local_time(df["BEGIN_YEARMONTH"], df["BEGIN_DAY"], df["BEGIN_TIME"])
        end = _local_time(df["END_YEARMONTH"], df["END_DAY"], df["END_TIME"])
        df["begin_time"] = begin
        df["duration_hours"] = (end - begin).dt.total_seconds() / 3600
        # A span the outcome alone sets is blanked by event type, not by reporter (LEAK-10, LEAK-37; notes)
        df.loc[df["EVENT_TYPE"].isin(OUTCOME_SPAN), "duration_hours"] = np.nan
        # 4. One code per county, forecast zone or marine zone
        df["county_zone"] = df["STATE_FIPS"].str.zfill(2) + df["CZ_TYPE"] + df["CZ_FIPS"].str.zfill(3)
        # 5. Numbers; the speeds estimated from the damage are blanked and their type stays (LEAK-10, notes)
        for col in ("MAGNITUDE", "BEGIN_LAT", "BEGIN_LON"):
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df["MAGNITUDE_TYPE"].isin(ESTIMATED), "MAGNITUDE"] = np.nan
        # 6. One unit per column: hail size in inches, wind speed in knots (CLEAN-21)
        hail = df["EVENT_TYPE"].isin(HAIL_TYPES)
        df["hail_size_in"] = df["MAGNITUDE"].where(hail)
        df["wind_speed_kt"] = df["MAGNITUDE"].where(~hail)
        # 7. Written from the damage or recorded with it (LEAK-10), then identifiers and copies (notes)
        post_outcome = [
            "DAMAGE_PROPERTY",
            "DAMAGE_CROPS",
            "INJURIES_DIRECT",
            "INJURIES_INDIRECT",
            "DEATHS_DIRECT",
            "DEATHS_INDIRECT",
            "SOURCE",  # "NWS Storm Survey" marks a damage survey (notes)
            "EVENT_NARRATIVE",
            "CATEGORY",  # the hurricane category, set per zone, partly after the event (notes)
            "TOR_F_SCALE",
            "TOR_LENGTH",
            "TOR_WIDTH",
            "TOR_OTHER_WFO",
            "TOR_OTHER_CZ_STATE",
            "TOR_OTHER_CZ_FIPS",
            "TOR_OTHER_CZ_NAME",
            "END_LAT",
            "END_LON",
            "END_RANGE",
            "END_AZIMUTH",
            "END_LOCATION",
        ]
        copies = [
            "EVENT_ID",
            "EPISODE_ID",
            "DATA_SOURCE",
            "YEAR",
            "MONTH_NAME",
            "BEGIN_YEARMONTH",
            "BEGIN_DAY",
            "BEGIN_TIME",
            "END_YEARMONTH",
            "END_DAY",
            "END_TIME",
            "BEGIN_DATE_TIME",
            "END_DATE_TIME",
            "CZ_TIMEZONE",
            "STATE_FIPS",
            "CZ_FIPS",
            "CZ_NAME",
            "BEGIN_RANGE",
            "BEGIN_AZIMUTH",
            "BEGIN_LOCATION",
            "MAGNITUDE",
        ]
        df = drop_columns(df, post_outcome + copies)
        return df.rename(
            columns={
                "STATE": "state",
                "EVENT_TYPE": "event_type",
                "CZ_TYPE": "cz_type",
                "WFO": "wfo",
                "MAGNITUDE_TYPE": "magnitude_type",
                "FLOOD_CAUSE": "flood_cause",
                "BEGIN_LAT": "begin_lat",
                "BEGIN_LON": "begin_lon",
            }
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "event_type",
                "state",
                "cz_type",
                "county_zone",
                "wfo",
                "magnitude_type",
                "flood_cause",
            ],
            datetime=["begin_time"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        dollars = _dollars(raw["DAMAGE_PROPERTY"])
        # The entries by event type: blank (dropped), $0 and positive
        top = raw["EVENT_TYPE"].value_counts().head(12).index
        by_type = pd.DataFrame(
            {
                "events": raw["EVENT_TYPE"].value_counts()[top],
                "blank (dropped)": dollars.isna().groupby(raw["EVENT_TYPE"]).mean()[top].round(3),
                "$0 among entries": (dollars[dollars.notna()] == 0)
                .groupby(raw["EVENT_TYPE"][dollars.notna()])
                .mean()[top]
                .round(3),
                "median of the positive ($)": dollars[dollars > 0]
                .groupby(raw["EVENT_TYPE"][dollars > 0])
                .median()[top],
            }
        )
        by_type.index.name = "event type"
        # The office practice: the share of $0 among the Thunderstorm Wind entries, per office
        tsw = (raw["EVENT_TYPE"] == "Thunderstorm Wind") & dollars.notna()
        per_office = (dollars[tsw] == 0).groupby(raw["WFO"][tsw]).agg(["mean", "size"])
        per_office = per_office[per_office["size"] >= 100]
        quantiles = per_office["mean"].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).round(3)
        office = pd.Series(
            {
                "offices with 100 or more Thunderstorm Wind entries": len(per_office),
                **{f"share at $0, {int(q * 100)}th percentile of the offices": v for q, v in quantiles.items()},
            },
            name="value",
        )
        return [
            Decision(
                "Entries without a damage figure are dropped; $0 stays",
                "A blank damage field leaves the row without a target. We read it as the 'no information available' "
                "box of NWSI 10-1605, Sec. 2.7 (an inference: floods, which must get an amount, have no blank from "
                "2008 on). A $0 is kept as entered; it mixes no damage with no estimate made, and an office can move "
                "between $0 and blank for the same kind of event over the years (notes).",
                by_type,
            ),
            Decision(
                "A $0 depends on the office",
                "Offices differ widely in how often they enter $0 for the same event type, and the practice drifts "
                "over the years; the office is a feature, so a model can learn the practice, and the target is not "
                "repaired (kept under LEAK-25 as amended, Andrej, 2026-11-02).",
                office,
            ),
        ]
