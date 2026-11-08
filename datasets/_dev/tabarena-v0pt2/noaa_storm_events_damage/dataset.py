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
TARGET = "property_damage_usd"
# The episode narrative is not read; the event narrative only finds double entries and is dropped (LEAK-10, LEAK-19)
NOT_READ = ("EPISODE_NARRATIVE",)
IDS = ("EVENT_ID", "EPISODE_ID")
# DAMAGE_PROPERTY is a number with a magnitude letter ("10.00K"); a few values carry no letter and are dollars
MAGNITUDE_LETTER = {"K": 1e3, "M": 1e6, "B": 1e9}
# MAGNITUDE is the hail size in inches for these types and a wind speed in knots for the others (format document)
HAIL_TYPES = ("Hail", "Marine Hail")
# Hazards whose entries almost never carry property damage (99.1% at $0, 0.5% of the dollars), so a planner of property
# damage does not plan for them (the domain practitioner's list, review issue 2): marine zones, drought, heat, cold,
# fog, rip current, funnel cloud, waterspout and high surf.
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
# Measured wind speeds: gust (MG) and sustained (MS)
MEASURED = ("MG", "MS")
# Wind types whose span runs from the first damage or wind of the criterion to the last (Sec. 46, 24)
DAMAGE_OR_WIND_SPAN = ("Thunderstorm Wind", "High Wind")
# Types whose span or its start the outcome alone sets (NWSI 10-1605 App. A): a tornado's ground contact, which the
# damage survey sets (Sec. 47), the span of Strong Wind (Sec. 45) and Heavy Rain (Sec. 21), timed by the damage, and
# the start of a Seiche, the shoreline flooding "resulting in a fatality, injury or damage" (Sec. 41)
OUTCOME_SPAN = ("Tornado", "Strong Wind", "Heavy Rain", "Seiche")


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
            "hail, flood, tornado, winter storm and 29 other types), among the events with a damage entry (an office "
            "leaves 0% to 98% of its events blank); the hazards whose entries almost never carry property damage "
            "(marine zones, drought, heat, cold, fog and a few more) are left out."
        ),
        predicted=(
            "The property damage the NWS office entered for the event, in nominal dollars; 68% of the entries are $0."
        ),
        known=(
            "The event type, the place (state, county or zone, forecast office, where county events began), when it "
            "began and, unless damage alone timed it, how long it lasted, a measured wind speed or the hail size, "
            "whether a wind report was measured or a damage report, and a flood's cause. The first report says "
            "whether damage was seen; some types are entered only with damage (4.5-5.0% of test rows)."
        ),
        split=(
            "The test data is a later calendar year (2023, 2024 or 2025), with every event published by the refit at "
            "the start of that year (all but the last three months) for training."
        ),
        changes=(
            "We drop entries without a damage figure, 918 double entries, narratives, tornado rating and path, end "
            "point, casualties, crop damage, reporter and hurricane category, and blank the wind speeds estimated from "
            "the damage and the durations it sets (tornado, strong wind, heavy rain, seiche, wind reported as damage or "
            "thunderstorm wind under 50 kt): all written from, with or after the damage. Wind speed and hail size "
            "become two columns."
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

        - Prediction point: a storm has passed, the event has ended and is logged from the first reports (type, place, begin and end time, a measured wind speed or the hail size, whether damage was seen), before any damage survey, claim or damage estimate. Every column is checked against it. Strong Wind, Lightning and Thunderstorm Wind below 50 kt enter Storm Data only when they result in "a fatality, injury, or damage" (NWSI 10-1605, Sec. 29, 45 and 46), and so, mostly, do hail under 3/4 inch (Sec. 19: entered when its accumulations "cause property and/or crop damage") and dust devils (Sec. 10): 4.5-5.0% of the test rows, 95-96% of them with damage. They stay, since the first report says whether damage was seen (LEAK-37). The numbers below are untuned LightGBM (400 trees) on the shipped features, trained on 2007 to September 2023 and tested on 2024, RMSE on log1p of the dollars (RMSLE, the metric until 2026-11-08): 2.626 as shipped (scratch, 2026-11-01).
        - Target: `DAMAGE_PROPERTY`, coded as a number and a magnitude letter ("10.00K" = $10,000), parsed to dollars and shipped in dollars (`property_damage_usd`): a target scored by a deviance ships untransformed, since the deviance scores the mean on the dollars, which a fit on the log scale misses (CLEAN-16). Until 2026-11-08 it shipped as log1p (`log1p_property_damage_usd`) for RMSLE (review issue 8). Nominal dollars as entered, not adjusted for inflation.
        - Metric floor: a prediction below $1 counts as $1 (`min_prediction`; Lennart, 2026-11-08, review issue 8). The $1 follows the collection's rule for a deviance floor, two orders of magnitude below the smallest plausible mean (MET-13 as amended on 2026-11-06, as for the 1e-4 claims per year of fremtpl2 and bemtpl97 and the 0.1 EUR of pricing_game_2017_french_mtpl): a convention of this collection that can change later, not a property of the source, which states no floor. The smallest plausible mean is $909, the training mean damage of Dense Smoke (143 entries, 2 with damage, in the 2024 and 2025 windows; $1,340 in 2023), the cheapest of the 33 event types with a positive training mean on every shipped split; the next is Winter Weather, $1,900 to $1,920 on 45,767 to 50,917 entries. Volcanic Ashfall, $0 in all its 69 to 77 training entries, has no positive mean and is not counted: a model should predict near $0 there, and the floor binds by design. Two orders below $909 is $9.09, rounded down to the power of ten, as the collection's other floors: $1, which is also more than two orders below every type with at least 500 training entries (the cheapest, Astronomical Low Tide, $1,526 in 2024). At the floor (2026-11-08): 0% of the predictions of a LightGBM fitted with the Tweedie loss at 100 trees and 5.6% to 8.1% at 400 trees, whose score moves by 1% to 10% between floors of $0.1 and $10; in the task probe 0% of the random forest's and 43.8% of the linear model's and LightGBM's, fitted by squared error on the dollars, which predict below $1 there.
        - Signal under the declared metric (2026-11-08; untuned LightGBM fitted with the Tweedie loss on the shipped splits, and the task probe): fitted with the Tweedie loss, LightGBM of 100 trees scores 4,108 to 5,327, 2,048 to 2,453 and 788 to 838 in 2023, 2024 and 2025 (5 fits each), against 4,453, 4,216 and 2,929 for the training mean and 2,660, 2,301 and 1,740 for the training mean per event type; at 400 trees 6,153 to 24,115, 3,400 to 6,442 and 994 to 1,447, and at 1,500 trees 12,344 to 51,125, 7,694 to 22,318 and 2,003 to 2,972. So a model fitted for the metric beats a constant in 2024 and 2025 (in 2 of 5 fits in 2023) and the mean per event type clearly only in 2025, and more capacity scores worse: the deviance is decided by the few largest events, as the panel read its picks (review issue 8). The task probe's families, fitted by squared error on the dollars, all lose to the training mean (mean deviance 3,866 over the 3 windows; random forest 5,796, linear 115,411, LightGBM 190,920), so it flags `no_signal`, `drift_baseline` and `unstable` (TP-1, TP-2, TP-5). Under RMSLE untuned LightGBM gained about 1.3 over a constant in every window.
        - Rows without a damage figure (blank `DAMAGE_PROPERTY`, 18% of the 1,225,290 events 2007-2025) have no target and are dropped. We read the blank as the "no information available" box ("either check the 'no information available' box, or make an estimate. The lone exception is for flood events", NWSI 10-1605, Sec. 2.7, p. 11): an inference, since the export of the box is not documented; Flood and Flash Flood have 26 blanks, all in 2007, and none from 2008 on. A $0 entry stays a 0. The curator's call (Andrej, 2026-10-30, zero-inflated review): "We don't care. We want to add any relevant predictive task, independent if it is zero inflated or not"; reading it as making $0 against blank a cleaning choice is the AI's.
        - Dropped as hazards whose entries almost never carry property damage (USE-1; Andrej, 2026-11-03, review issue 2, the domain practitioner's list): every marine type and drought, heat, excessive heat, cold/wind chill, extreme cold/wind chill, dense fog, freezing fog, rip current, funnel cloud, waterspout and high surf: 156,767 entries with a damage figure (15.7%), 99.1% of them $0, with 0.5% of the dollars, so they hold almost none of the property damage the planner plans for. The event type alone predicts their zeros, so they made the task look easier. On the rows left untuned LightGBM scores RMSLE 2.67, 2.93 and 2.94 (2025, 2024, 2023) against 4.05, 4.28 and 4.20 for a constant.
        - No storm-level input (review issue 4): the number of a storm's entries and counties (`EPISODE_ID`) changes untuned LightGBM's RMSLE by -0.010 to +0.001 counted over all its entries, and by -0.012 to +0.017 counted over the types entered whatever the damage (strong wind, lightning and thunderstorm wind under 50 kt enter Storm Data only with damage, 3.3% of the entries), so it adds no measurable signal and would carry part of the label.
        - Exposure (MET-14, MET-15; 2026-11-06): none. The target is the damage of one event as entered, not a count or an amount accrued over an amount at risk, so it ships without a rate, a weight or an offset. The source gives no population, building or insured value, and the one proxy tested, the county's population (Census estimate for 2020, county rows of 2016-2025), does not scale with the damage (Spearman -0.14 to +0.05 with the log damage among the positive entries of five types; exposure study of 2026-11-05). `duration_hours` is a span the outcome partly sets, not an exposure (below). The storms whose positive entries all carry one figure (2,063 of the 16,080 with two or more, 2016-2025) hold round office values (one of eight round amounts from $1,000 to $100,000 in 73.5% of them; one or two significant digits in every one with three or more entries), not a storm total split over its zones.
        - Anomaly: a $0 mixes "no damage" with "no estimate made" (13 of 121 EF4 and EF5 tornado segments, and 17.3% of EF2 and above, are at $0), and the mix is office practice: among Thunderstorm Wind entries the share at $0 runs from 7% to 91% between the 10th and 90th percentile of the 107 offices with 100 or more entries (decision table). It drifts: an office's 2024 share predicts its 2025 share at r 0.958 and its 2007-2016 share at r 0.575, and 30.5% of 82 offices moved by more than 0.2 from 2007-2021 to 2023-2025. The line between $0 and blank moves inside an office too: from 2007-2010 to 2022-2025, 70% of the rise in an office's Thunderstorm Wind blanks came out of its $0 entries (98 offices). The office (`wfo`) is a feature, so a model can learn the practice; it is not repaired. Kept under LEAK-25 as amended for this case (Andrej, 2026-11-02): a mix whose recording follows a reporting unit shipped as a feature stays, with the unit's spread and drift in the notes and fit approximate, as the task keeps a measured signal beyond the office, the period and the place; the blanks, the source's own 'not recorded' box, are dropped.
        - History: from 2007 on. In the files of 2000-2005, 70% to 72% of the events have no damage figure, 61% in 2006 (the year the files move from the PDS to the CSV entry format; in 2006 the PDS rows are 71.3% blank, floods 63.3%, the CSV rows 0.1%), then 7.3% in 2007, rising to 22-24% in 2022-2025, so the kept rows change composition; the positive damage drifts down within the kept years too (median of Thunderstorm Wind $5,000 in 2007-2017, $2,000 in 2025).
        - Dropped, written from the damage or recorded with it (LEAK-10): the narratives (the episode narrative is not read, the event narrative only finds double entries), `TOR_F_SCALE` (the Enhanced Fujita rating "describes the strength of the tornado based on the amount and type of damage", format document p. 4), `TOR_LENGTH`, `TOR_WIDTH` and the `TOR_OTHER_*` continuation fields (the path from the damage survey), the end point `END_LAT`, `END_LON`, `END_RANGE`, `END_AZIMUTH`, `END_LOCATION` (for a tornado the end of the surveyed path, for a wind swath "within the county where the wind damage swath exists", NWSI 10-1605, Sec. 46.1, p. A-68), the injuries and deaths, and the crop damage. Measured: with the rating, the path and the end point the RMSE falls from 2.626 to 2.596 (tornado rows 4.796 to 4.107); with the casualties and the crop damage to 2.561; two flags read off the event narrative (a dollar amount, a damage word such as "roof" or "downed") give 2.559.
        - Dropped (LEAK-10): `CATEGORY`, which the format document calls unknown. It is filled for the Hurricane (Typhoon) events only, 1 to 5, and set per zone: 23 of the 95 episodes with a category carry more than one value, and Hurricane Michael's Category 5 zone (2018) is the reanalysis of April 2019, after the event; NWSI 10-1605 (Sec. 25.3) pairs each category with the types of damage. 482 rows, none in 2025.
        - Dropped (LEAK-10): `SOURCE`, the reporter of the event. One of its values, "NWS Storm Survey" (about 23,700 entries, 72% with damage), is a damage survey the office makes after the event, and the column has no missing values, so blanking that value would leave the same marker; merged into "Unknown" (about 1,400 entries) it would hold it too (RMSE 2.559 merged and as published). The other reporters (a 911 call center, a utility, a trained spotter) are known at the first report, so the drop costs real signal: RMSE 2.626 without the column. The drop follows kick and expresso_churn_prediction.
        - Blanked (LEAK-10): the wind speeds the office estimated from the damage, `magnitude_type` "EG" (252,451 entries) and "ES" (the same for sustained wind, 1,151); the type stays. NWSI 10-1605, Sec. 46.3, p. A-69: the preparer "exercises professional judgment to determine the estimated maximum wind value based on observed structural or tree damage". Matched to the real-time Local Storm Reports of 2024 (same office, within 15 minutes and 10 km), 94.4% of 12,498 EG Thunderstorm Wind events had a first report "TSTM WND DMG" without a speed, while measured gusts kept their speed in 92.7% of cases and hail sizes in 97.9%. Whether a wind report was a damage report or a measured gust is in the first report, so `magnitude_type` stays and the blank follows it (no marker). Among entries with damage the estimate tracks the dollars (Spearman 0.46); on the EG and ES test rows the RMSE is 2.760 with it and 2.860 blank. The 24 impossible speeds (22 Thunderstorm Wind entries of 1-10 kt, 2 Strong Wind entries of 0 kt) are all estimates and go with them.
        - Blanked (LEAK-10): `duration_hours` where the outcome alone sets the span or its start, by event type, and on the wind entries whose span only the damage can have timed, by event type, speed type and measured speed; never by reporter, so a blank is no survey marker. Tornado: a tornado begins and ends with the vortex's ground contact, which the damage survey sets (NWSI 10-1605, Sec. 47; 68% of the tornado rows come from "NWS Storm Survey"), and the duration tracks the dropped path length (Spearman 0.83 with `TOR_LENGTH`); on the tornado test rows the RMSE is 4.537 with it and 4.796 blank. Strong Wind and Heavy Rain (CC 2026-11-06, Lennart; 18,243 and 20,836 rows, 4.6%): App. A times them by the damage, Strong Wind from "When the wind started to cause a fatality, injury, or significant damage" to "When the wind no longer caused a fatality, injury, or significant damage" (Sec. 45), Heavy Rain from "When the heavy rain that led to damage began" until it "no longer posed a threat to life or property" (Sec. 21). Their blank costs nothing measurable: on their test rows RMSLE changes by -0.009, -0.018 and -0.046 (2023, 2024, 2025; untuned LightGBM on the shipped splits, mean of 4 bagging seeds, SD 0.03 to 0.06). Seiche (51 rows; blanked after the re-review of 2026-11-06, which read App. A again for every type and found it missing from D13's reading): it begins "When water levels rose to initiate shoreline flooding, resulting in a fatality, injury or damage" (Sec. 41), so the damage draws its start; too few rows to measure. The Thunderstorm Wind and High Wind entries the first report gives as damage (CC 2026-11-08, Lennart; review issue 7): the entries whose speed the office estimated from the damage (`magnitude_type` EG or ES, 241,088 rows) and the Thunderstorm Wind entries measured under 50 kt (MG or MS, 435 rows), 241,523 rows, 75.8% of the 318,813 rows of the five types D13 kept with a note. App. A times Thunderstorm Wind from "When damage first occurred or winds 50 knots (58 mph) or greater were first reported" to "When damage ended or winds of 50 knots (58 mph) were last reported" (Sec. 46), and High Wind likewise with its wind criteria (Sec. 24); on these entries no wind of the criterion was reported, so only the damage can have timed the span, as for Strong Wind. An EG or ES speed is the preparer's estimate from the damage (Sec. 46.3, above), and 94.4% of the EG Thunderstorm Wind entries of 2024 had a first report of damage without a speed (the other 5.6% had a speed in the first report, so the blank locates these spans closely, not exactly); a Thunderstorm Wind entry measured under 50 kt met no wind criterion and enters Storm Data only with damage (92% of the 435 have property damage). The blank follows `event_type`, `magnitude_type` and `wind_speed_kt`, so a missing duration tells a model nothing those features do not (leak probe, 2026-11-08: the missing indicator alone scores R^2 0.192, `event_type` alone 0.185; all features 0.352, 0.348 without the column). Its cost on these rows' test rows under RMSLE, the metric before review issue 8 (2026-11-08, the shipped splits, mean of 4 bagging seeds per window): +0.023 to +0.036 RMSLE under a LightGBM of 1,500 trees and 127 leaves (12 of 12 seeds positive) and +0.008 to +0.032 under untuned LightGBM of 400 trees; on all rows +0.009 to +0.026 and -0.003 to +0.027.
        - Potential leak, kept on purpose (CC 2026-11-06 and 2026-11-08, Lennart): `duration_hours` of the Thunderstorm Wind and High Wind entries with a measured speed (of 50 kt or more for Thunderstorm Wind; 31,985 and 41,432 rows), of Coastal Flood, Lakeshore Flood and Storm Surge/Tide (3,873 rows) and, by the same reading (re-review of 2026-11-06), of Dust Storm and Volcanic Ashfall (1,553 rows): 78,843 rows (9.4%), whose span App. A times by the damage or by a criterion without it. Thunderstorm Wind runs from "When damage first occurred or winds 50 knots (58 mph) or greater were first reported" to "When damage ended or winds of 50 knots (58 mph) were last reported" (Sec. 46), High Wind likewise with the high-wind criteria (Sec. 24), the three floods from "When the water level began to cause damage or flooding" to "When the water level dropped to a point where damage or flooding ended" (Sec. 4, 27, 44), Dust Storm from when blowing dust "first reduced visibility to locally/regionally established values or began to cause a major impact" (Sec. 11), and Volcanic Ashfall from "When volcanic ash began to cause disruption to transportation, commerce, fatality, injury, or damage" (Sec. 51). On these entries the first report holds a measured wind, a water level, blowing dust or ash, so the criterion can have set the span, and Storm Data does not record which of the two did; the wind entries on which only the damage can have timed it are blank (above). Measured on 2026-11-08 on the declared metric (the column blanked on these rows against the shipped definition; LightGBM fitted with the Tweedie loss, 15 set-ups of 100, 400 and 1,500 trees on the 3 shipped splits): no consistent sign, from -41% to +99% of the mean deviance on these rows' test rows over the re-review's 15 set-up and window pairs (6 positive, median -5%) and 24 positive of all 45 fits (median +2%); -27% to +67% on all rows. By type: the measured Thunderstorm Wind spans gain in 35 of 45 fits (median +11% of the deviance on their rows; +7%, +22% and +19% in 2023, 2024 and 2025 under the 100-tree model, the best fitted for this metric), while High Wind (23 of 45 positive), Coastal Flood (26 of 45) and Dust Storm (16 of 45) show no consistent sign; Lakeshore Flood, Storm Surge/Tide and Volcanic Ashfall have 0 to 60 test rows per window, too few to read. Under RMSLE, the metric before review issue 8, the same blank measured -0.02 to +0.12 RMSLE on these rows (15 fits, 11 positive, median about +0.04; -0.01 to +0.09 on all rows), the measured Thunderstorm Wind spans +0.03 to +0.18 in 30 of 30 fits, more than the blanked spans carried. The +0.012 to +0.021 RMSLE of the CC line of 2026-11-06 and the -0.01 to +0.08 of the re-review were measured on all five types, before the blank. Kept by the LEAK-10 / LEAK-37 Cases row of 2026-11-06 (a span drawn by the outcome or by a criterion without it stays, with its worth noted); revisit if Storm Data records which criterion timed an event. Flood and Flash Flood are timed by a threat to life or property, from "When flood waters began to threaten life or property" (Sec. 15) and when they "became an immediate threat to life or property" (Sec. 14, where water that "causes damage to an above ground residence or public building" is one of four listed onsets), and Hurricane (Typhoon) and Tropical Storm from when "the direct effects" of the storm were first experienced (Sec. 25, 49; the "damage or" wording is that of their marine types, Sec. 34 and 39, which are dropped): judged outcome-free and kept; under the declared deviance the column carries much of a model's skill on the Flood and Flash Flood rows: blanking it there raises the deviance on those rows in 44 of 45 fits (by +80%, +73% and +24% in 2023, 2024 and 2025 under the 100-tree model, mean of 4 seeds) and on all rows in 43 of 45 (median +28%), while under RMSLE its worth there had no consistent sign (-0.09 to +0.09 over the 15 fits).
        - Dropped as identifiers or copies: `EVENT_ID`, `EPISODE_ID`, `DATA_SOURCE` (constant from 2007); `YEAR`, `MONTH_NAME`, the begin and end date and time columns and `CZ_TIMEZONE` (in `begin_time` and `duration_hours`); `STATE_FIPS`, `CZ_FIPS`, `CZ_NAME` (in `county_zone`); `BEGIN_RANGE`, `BEGIN_AZIMUTH`, `BEGIN_LOCATION` (a place name and the offset from it, which `begin_lat` and `begin_lon` give); `MAGNITUDE` (in `wind_speed_kt` and `hail_size_in`).
        - Built: `begin_time` from `BEGIN_YEARMONTH`, `BEGIN_DAY` and `BEGIN_TIME` (local standard time, as published); `duration_hours` from the end columns the same way (end minus begin; none is negative, the longest are the 31-day entries of a month, such as Flood and Wildfire; blank where the outcome alone sets the span or its start, and on the wind entries whose span only the damage can have timed, above); `county_zone`, the state FIPS code, the zone type and the county or zone number (one code per county, forecast zone or marine zone); `hail_size_in` and `wind_speed_kt` from `MAGNITUDE`, which holds inches for Hail and Marine Hail and knots for the wind types (format document p. 4), one unit per column (a lossless split).
        - Dropped as double entries (LEAK-19): 918 rows equal to another row in every column but the event and episode ids, event narrative included, in every year and type (248 Thunderstorm Wind, 228 Hail).
        - Note: duplicate rows are kept otherwise: 0.6% of the rows (5,402) are copies of another row in every feature and the target, mostly forecast-zone entries of one storm in one zone at the same time (Heavy Snow, Winter Storm), which the source entered as separate events with their own narratives; with the same begin time they never fall on both sides of a window.
        - Note: zone events (30.1% of the rows) have no begin latitude and longitude (all but 4), nor do 153 county events (30.1% of all rows lack them); their place is `county_zone` (7,697 codes).
        - Note: the same storm system appears as several events (one per county or zone, `EPISODE_ID` groups them, each storm entered by one office); no episode spans two months (0 of 140,270), so none crosses a window boundary.
        - Note: a year's file is rewritten when NCEI updates it. The 2024 files of 17 March 2025 and of 28 July 2026 agree on the damage of 99.83% of the 69,545 events in both (107 blanks filled, 14 values changed; 907 events, 1.3%, were added or removed), and 0 of the 64,921 damage values of January-October 2025 differ between the files of 16 January and 19 August 2026, so the newest year, 2025 (file of 19 August 2026), is settled (leak probe 13).
        - Licence: US Government work; NCEI's metadata (C00510) asks to "Cite dataset when used as a source" and warns that reports "may be unverified by the NWS".
        - CC (2026-11-06, Lennart): decision D13 of the exposure study (#51; review issue 6): `duration_hours` is blank for Strong Wind and Heavy Rain, whose span NWSI 10-1605 App. A draws by the damage (Sec. 45, 21), and kept with a note for Thunderstorm Wind, High Wind, Coastal Flood, Lakeshore Flood and Storm Surge/Tide, which it times by the damage or a wind or flooding criterion (Sec. 46, 24, 4, 27, 44), under the new LEAK-10 / LEAK-37 Cases row on spans the outcome sets. Supersedes the definition Andrej shipped on 2026-11-03, which blanked only the tornado durations, as the column audit of 2026-11-01 had read the begin and end of Thunderstorm Wind alone and judged the other spans first-report facts: the study of 2026-11-05 read App. A for every type and measured the column's worth on the seven damage-timed types (+0.02 to +0.04 RMSLE, trained from 2016). On the shipped splits it is +0.013 to +0.021 on those rows, all of it on the five kept types (+0.012 to +0.021) and none on Strong Wind and Heavy Rain.
        - CC (2026-11-08, Lennart): review issue 7, B ("Blank these rows"): `duration_hours` is blank also on the Thunderstorm Wind and High Wind entries whose speed the office estimated from the damage (EG, ES) and on the Thunderstorm Wind entries measured under 50 kt, 241,523 rows on which only the damage can have timed the span, as for Strong Wind; the note keeps the measured-wind, dust, ash and flood spans, with their worth measured again (above). Supersedes in part Lennart's D13 of 2026-11-06 (the line above), which kept the duration of every Thunderstorm Wind and High Wind entry with a note.
        - CC (2026-11-08, Lennart): review issue 8, B: the target ships in dollars and is scored by the mean Tweedie deviance at power 1.5 (floor $1, above), since the planner sums expected dollars, which RMSLE does not score; the right metric for the task comes first, and earlier calls that do not match the task give way. Supersedes Andrej's RMSLE: issue 3, A, of 2026-11-03, kept for the earlier triage actor, and "the declared metric, RMSLE from context, checked" (Andrej, 2026-11-03) when issue 5 made the planner the actor.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.from_context(
        "mean_tweedie_deviance",
        params={"power": 1.5, "min_prediction": 1.0},
        reason=(
            "NCEI and NWSI 10-1605 define no task or metric, and no competition was found. Diaz and Joseph (2019, "
            "Weather and Climate Extremes 25:100216, https://doi.org/10.1016/j.wace.2019.100216) model tornado damage "
            "from this database with several metrics (accuracy and AUROC for any damage, MSE on the log of the "
            "positive amounts), on tornadoes only and a random split: no source metric for this task (MET-5). The "
            "planner sums the expected damage of events over counties and hazards, so the metric scores each event's "
            "expected dollars: the mean Tweedie deviance at power 1.5, a compound Poisson-gamma loss minimised by the "
            "mean, for an amount that is $0 for 68% of the entries and heavy-tailed above it. RMSLE, declared until "
            "2026-11-08 (Andrej, 2026-11-03, for the earlier triage actor), scores the order of magnitude and is "
            "minimised by a geometric mean (the RMSLE-optimal constant for 2024 is $16 against a mean of $355,555), "
            "so its predictions summed over events understate the loss the planner plans for; trained each for its "
            "own metric, the two pick different models in 3 of 3 windows (2026-11-06). The deviance damps the tail "
            "far more than a squared error (on the dollars the largest 0.1% of the entries hold 99.94% of the squared "
            "deviation) and less than a log, so large events weigh more than under RMSLE, while the label is coarse "
            "(44% of the positive figures have one significant digit). A prediction below $1 counts as $1, two "
            "orders below the smallest plausible mean, the $909 training mean of Dense Smoke, the cheapest event type "
            "with a positive mean, rounded down to a power of ten: the collection's rule for a deviance floor "
            "(MET-13), a convention that can change later, not a property of the source. At the floor: 0% of a "
            "LightGBM fitted with the Tweedie loss at 100 trees and 6-8% at 400 trees; in the task probe 0% of the "
            "random forest's predictions and 44% of the linear model's and LightGBM's, fitted by squared error. "
            "Chosen over RMSLE by the curator (Lennart, 2026-11-08, review issue 8)."
        ),
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
        df[TARGET] = dollars[dollars.notna()]
        # The hazards whose entries almost never carry property damage go: the listed types and every marine type
        # (review issue 2).
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
        # A wind span only the damage can have timed is blanked too (review issue 7): a speed estimated from the
        # damage, or a Thunderstorm Wind measured under its 50 kt criterion, means no wind of the criterion was reported
        damage_timed = df["EVENT_TYPE"].isin(DAMAGE_OR_WIND_SPAN) & df["MAGNITUDE_TYPE"].isin(ESTIMATED)
        under_50 = (
            (df["EVENT_TYPE"] == "Thunderstorm Wind") & df["MAGNITUDE_TYPE"].isin(MEASURED) & (df["MAGNITUDE"] < 50)
        )
        df.loc[damage_timed | under_50, "duration_hours"] = np.nan
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
