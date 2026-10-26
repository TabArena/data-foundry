"""Curated dataset definition for `aeolus_1m` (data-foundry v2). Evidence: README.md."""

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

DELAY_THRESHOLD_MINUTES = 15
"""US DOT: a flight is on time when it arrives less than 15 minutes after its scheduled arrival (BTS `ARR_DEL15`)."""

HISTORY_START = "2023-01-01"
"""First flight date kept: two seasonal cycles before the test windows, after COVID-19 (curation notes)."""

MIN_SCHEDULED_MINUTES = 15
"""Scheduled block times below 15 minutes are errors; the shortest real hop (Wrangell-Petersburg) is 18 minutes."""

MIN_TEMPERATURE_C = -50
"""Temperatures below -50 C are errors: no US airport outside Alaska comes near it, Alaska's lowest reading is -41 C."""

MAX_WIND_KMH = 120
"""Mean wind speeds above 120 km/h (hurricane force) recorded without rain are sensor errors (ACY, HOU, ATW)."""

TRUE_SIGNS = {"GUM": ("LONGITUDE", 1), "PPG": ("LATITUDE", -1)}
"""Coordinates the release stores with the wrong sign: Guam at 144.80 W (true 144.80 E), Pago Pago at 14.33 N (true
14.33 S)."""

SKIPPED_COLUMNS = (
    "DEP_DELAY",
    "TAXI_OUT",
    "WHEELS_OFF",
    "WHEELS_ON",
    "TAXI_IN",
    "ACTUAL_ELAPSED_TIME",
    "AIR_TIME",
    "FLIGHTS",
    "MONTH",
    "DAY_OF_MONTH",
    "DAY_OF_WEEK",
    "ORIGIN_INDEX",
    "DEST_INDEX",
)
"""Source columns `_load_raw` does not read: recorded at or after the departure (DEP_DELAY to AIR_TIME), always 1
(FLIGHTS), parts of FL_DATE (MONTH, DAY_OF_MONTH, DAY_OF_WEEK) and one index per airport code."""

SUMMER_ZONES = {
    "JFK": "America/New_York",
    "ATL": "America/New_York",
    "ORD": "America/Chicago",
    "DEN": "America/Denver",
    "PHX": "America/Phoenix",
    "LAX": "America/Los_Angeles",
    "SEA": "America/Los_Angeles",
    "ANC": "America/Anchorage",
    "HNL": "Pacific/Honolulu",
}
"""Nine airports across the US time zones, for the second decision (the daily temperature cycle)."""

WEATHER = ("TEMP", "PRCP", "WSPD")
"""The release's hourly weather of each airport (`O_` origin, `D_` destination)."""

# The time zone of every airport of the kept history, from its coordinates (tz database, timezonefinder 2026-10-26;
# Guam and Pago Pago after the sign repair), to time the weather readings against the scheduled departure.
AIRPORT_TIME_ZONES = {
    "ABE": "America/New_York",
    "ABI": "America/Chicago",
    "ABQ": "America/Denver",
    "ABR": "America/Chicago",
    "ABY": "America/New_York",
    "ACK": "America/New_York",
    "ACT": "America/Chicago",
    "ACV": "America/Los_Angeles",
    "ACY": "America/New_York",
    "ADK": "America/Adak",
    "ADQ": "America/Anchorage",
    "AEX": "America/Chicago",
    "AGS": "America/New_York",
    "AKN": "America/Anchorage",
    "ALB": "America/New_York",
    "ALO": "America/Chicago",
    "AMA": "America/Chicago",
    "ANC": "America/Anchorage",
    "APN": "America/Detroit",
    "ASE": "America/Denver",
    "ATL": "America/New_York",
    "ATW": "America/Chicago",
    "AUS": "America/Chicago",
    "AVL": "America/New_York",
    "AVP": "America/New_York",
    "AZO": "America/Detroit",
    "BDL": "America/New_York",
    "BET": "America/Anchorage",
    "BFL": "America/Los_Angeles",
    "BGM": "America/New_York",
    "BGR": "America/New_York",
    "BHM": "America/Chicago",
    "BIL": "America/Denver",
    "BIS": "America/Chicago",
    "BJI": "America/Chicago",
    "BLI": "America/Los_Angeles",
    "BMI": "America/Chicago",
    "BNA": "America/Chicago",
    "BOI": "America/Boise",
    "BOS": "America/New_York",
    "BPT": "America/Chicago",
    "BQK": "America/New_York",
    "BQN": "America/Puerto_Rico",
    "BRD": "America/Chicago",
    "BRO": "America/Chicago",
    "BRW": "America/Anchorage",
    "BTM": "America/Denver",
    "BTR": "America/Chicago",
    "BTV": "America/New_York",
    "BUF": "America/New_York",
    "BUR": "America/Los_Angeles",
    "BWI": "America/New_York",
    "BZN": "America/Denver",
    "CAE": "America/New_York",
    "CAK": "America/New_York",
    "CDC": "America/Denver",
    "CDV": "America/Anchorage",
    "CHA": "America/New_York",
    "CHO": "America/New_York",
    "CHS": "America/New_York",
    "CID": "America/Chicago",
    "CIU": "America/Detroit",
    "CLE": "America/New_York",
    "CLL": "America/Chicago",
    "CLT": "America/New_York",
    "CMH": "America/New_York",
    "CMI": "America/Chicago",
    "CMX": "America/Detroit",
    "CNY": "America/Denver",
    "COD": "America/Denver",
    "COS": "America/Denver",
    "COU": "America/Chicago",
    "CPR": "America/Denver",
    "CRP": "America/Chicago",
    "CRW": "America/New_York",
    "CSG": "America/New_York",
    "CVG": "America/New_York",
    "CWA": "America/Chicago",
    "DAB": "America/New_York",
    "DAL": "America/Chicago",
    "DAY": "America/New_York",
    "DCA": "America/New_York",
    "DEN": "America/Denver",
    "DFW": "America/Chicago",
    "DHN": "America/Chicago",
    "DIK": "America/Denver",
    "DLG": "America/Anchorage",
    "DLH": "America/Chicago",
    "DRO": "America/Denver",
    "DSM": "America/Chicago",
    "DTW": "America/Detroit",
    "DVL": "America/Chicago",
    "EAU": "America/Chicago",
    "ECP": "America/Chicago",
    "EGE": "America/Denver",
    "EKO": "America/Los_Angeles",
    "ELM": "America/New_York",
    "ELP": "America/Denver",
    "ERI": "America/New_York",
    "ESC": "America/Detroit",
    "EUG": "America/Los_Angeles",
    "EVV": "America/Chicago",
    "EWN": "America/New_York",
    "EWR": "America/New_York",
    "EYW": "America/New_York",
    "FAI": "America/Anchorage",
    "FAR": "America/Chicago",
    "FAT": "America/Los_Angeles",
    "FAY": "America/New_York",
    "FCA": "America/Denver",
    "FLG": "America/Phoenix",
    "FLL": "America/New_York",
    "FNT": "America/Detroit",
    "FSD": "America/Chicago",
    "FSM": "America/Chicago",
    "FWA": "America/Indiana/Indianapolis",
    "GCC": "America/Denver",
    "GCK": "America/Chicago",
    "GEG": "America/Los_Angeles",
    "GFK": "America/Chicago",
    "GGG": "America/Chicago",
    "GJT": "America/Denver",
    "GNV": "America/New_York",
    "GPT": "America/Chicago",
    "GRB": "America/Chicago",
    "GRI": "America/Chicago",
    "GRK": "America/Chicago",
    "GRR": "America/Detroit",
    "GSO": "America/New_York",
    "GSP": "America/New_York",
    "GST": "America/Juneau",
    "GTF": "America/Denver",
    "GTR": "America/Chicago",
    "GUC": "America/Denver",
    "GUM": "Pacific/Guam",
    "HDN": "America/Denver",
    "HIB": "America/Chicago",
    "HLN": "America/Denver",
    "HNL": "Pacific/Honolulu",
    "HOB": "America/Denver",
    "HOU": "America/Chicago",
    "HPN": "America/New_York",
    "HRL": "America/Chicago",
    "HSV": "America/Chicago",
    "HYA": "America/New_York",
    "HYS": "America/Chicago",
    "IAD": "America/New_York",
    "IAG": "America/New_York",
    "IAH": "America/Chicago",
    "ICT": "America/Chicago",
    "IDA": "America/Boise",
    "ILM": "America/New_York",
    "IMT": "America/Menominee",
    "IND": "America/Indiana/Indianapolis",
    "INL": "America/Chicago",
    "ISP": "America/New_York",
    "ITH": "America/New_York",
    "ITO": "Pacific/Honolulu",
    "JAC": "America/Denver",
    "JAN": "America/Chicago",
    "JAX": "America/New_York",
    "JFK": "America/New_York",
    "JLN": "America/Chicago",
    "JMS": "America/Chicago",
    "JNU": "America/Juneau",
    "KOA": "Pacific/Honolulu",
    "KTN": "America/Sitka",
    "LAN": "America/Detroit",
    "LAR": "America/Denver",
    "LAS": "America/Los_Angeles",
    "LAW": "America/Chicago",
    "LAX": "America/Los_Angeles",
    "LBB": "America/Chicago",
    "LBE": "America/New_York",
    "LCH": "America/Chicago",
    "LEX": "America/New_York",
    "LFT": "America/Chicago",
    "LGA": "America/New_York",
    "LGB": "America/Los_Angeles",
    "LIH": "Pacific/Honolulu",
    "LIT": "America/Chicago",
    "LNK": "America/Chicago",
    "LRD": "America/Chicago",
    "LSE": "America/Chicago",
    "LWS": "America/Los_Angeles",
    "MAF": "America/Chicago",
    "MBS": "America/Detroit",
    "MCI": "America/Chicago",
    "MCO": "America/New_York",
    "MDT": "America/New_York",
    "MDW": "America/Chicago",
    "MEI": "America/Chicago",
    "MEM": "America/Chicago",
    "MFE": "America/Chicago",
    "MFR": "America/Los_Angeles",
    "MGM": "America/Chicago",
    "MHK": "America/Chicago",
    "MHT": "America/New_York",
    "MIA": "America/New_York",
    "MKE": "America/Chicago",
    "MLB": "America/New_York",
    "MLI": "America/Chicago",
    "MLU": "America/Chicago",
    "MOB": "America/Chicago",
    "MOT": "America/Chicago",
    "MQT": "America/Detroit",
    "MRY": "America/Los_Angeles",
    "MSN": "America/Chicago",
    "MSO": "America/Denver",
    "MSP": "America/Chicago",
    "MSY": "America/Chicago",
    "MTJ": "America/Denver",
    "MVY": "America/New_York",
    "MYR": "America/New_York",
    "OAJ": "America/New_York",
    "OAK": "America/Los_Angeles",
    "OGG": "Pacific/Honolulu",
    "OKC": "America/Chicago",
    "OMA": "America/Chicago",
    "OME": "America/Nome",
    "ONT": "America/Los_Angeles",
    "ORD": "America/Chicago",
    "ORF": "America/New_York",
    "ORH": "America/New_York",
    "OTH": "America/Los_Angeles",
    "OTZ": "America/Nome",
    "PBG": "America/New_York",
    "PBI": "America/New_York",
    "PDX": "America/Los_Angeles",
    "PHF": "America/New_York",
    "PHL": "America/New_York",
    "PHX": "America/Phoenix",
    "PIA": "America/Chicago",
    "PIB": "America/Chicago",
    "PIH": "America/Boise",
    "PIT": "America/New_York",
    "PLN": "America/Detroit",
    "PNS": "America/Chicago",
    "PPG": "Pacific/Pago_Pago",
    "PSC": "America/Los_Angeles",
    "PSE": "America/Puerto_Rico",
    "PSG": "America/Sitka",
    "PSP": "America/Los_Angeles",
    "PUB": "America/Denver",
    "PVD": "America/New_York",
    "PWM": "America/New_York",
    "RAP": "America/Denver",
    "RDD": "America/Los_Angeles",
    "RDM": "America/Los_Angeles",
    "RDU": "America/New_York",
    "RHI": "America/Chicago",
    "RIC": "America/New_York",
    "RKS": "America/Denver",
    "RNO": "America/Los_Angeles",
    "ROA": "America/New_York",
    "ROC": "America/New_York",
    "ROW": "America/Denver",
    "RST": "America/Chicago",
    "RSW": "America/New_York",
    "SAF": "America/Denver",
    "SAN": "America/Los_Angeles",
    "SAT": "America/Chicago",
    "SAV": "America/New_York",
    "SBA": "America/Los_Angeles",
    "SBN": "America/Indiana/Indianapolis",
    "SBP": "America/Los_Angeles",
    "SCC": "America/Anchorage",
    "SCE": "America/New_York",
    "SDF": "America/Kentucky/Louisville",
    "SEA": "America/Los_Angeles",
    "SFO": "America/Los_Angeles",
    "SGF": "America/Chicago",
    "SGU": "America/Denver",
    "SHV": "America/Chicago",
    "SIT": "America/Sitka",
    "SJC": "America/Los_Angeles",
    "SJT": "America/Chicago",
    "SJU": "America/Puerto_Rico",
    "SLC": "America/Denver",
    "SMF": "America/Los_Angeles",
    "SMX": "America/Los_Angeles",
    "SNA": "America/Los_Angeles",
    "SPI": "America/Chicago",
    "SPS": "America/Chicago",
    "SRQ": "America/New_York",
    "STC": "America/Chicago",
    "STL": "America/Chicago",
    "STT": "America/St_Thomas",
    "STX": "America/St_Thomas",
    "SUN": "America/Boise",
    "SUX": "America/Chicago",
    "SWF": "America/New_York",
    "SYR": "America/New_York",
    "TLH": "America/New_York",
    "TPA": "America/New_York",
    "TRI": "America/New_York",
    "TTN": "America/New_York",
    "TUL": "America/Chicago",
    "TUS": "America/Phoenix",
    "TVC": "America/Detroit",
    "TWF": "America/Boise",
    "TXK": "America/Chicago",
    "TYR": "America/Chicago",
    "TYS": "America/New_York",
    "VEL": "America/Denver",
    "VLD": "America/New_York",
    "VPS": "America/Chicago",
    "WRG": "America/Sitka",
    "WYS": "America/Denver",
    "XNA": "America/Chicago",
    "YAK": "America/Yakutat",
    "YUM": "America/Phoenix",
}


class Aeolus1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a US domestic flight arrive 15 minutes or more late?",
        use_case=(
            "Shortly before departure, an airline or airport estimates which of the coming flights will arrive late, "
            "from the schedule and the weather."
        ),
        row="One completed US domestic flight of 2023-2024.",
        predicted=(
            "Whether it arrives at least 15 minutes after its scheduled arrival (the US DOT definition); about one "
            "flight in five does."
        ),
        known=(
            "The date, airline, flight number, route, scheduled times and duration, the airports' locations, and the "
            "weather at both airports observed 3.5 to 11 hours before departure (about a day early for overnight "
            "arrivals); a reading after the departure is missing."
        ),
        split=(
            "Each test window is two weeks at the end of 2024; training is a random million earlier flights from 2023"
            " on, as for a model refit every two weeks."
        ),
        changes=(
            "We use the history from 2023 on (the release starts in 2016) and two-week windows, so only one window "
            "falls in the holiday peak."
        ),
        fit="approximate",
        fit_reason=(
            "The weather is an old observation: 3.5 to 11 hours before departure by time zone, a day early for "
            "overnight arrivals; the 2% of the destination readings and Guam's origin readings that fall after the "
            "departure are set missing. The inbound aircraft, the largest cause of delay, is missing, and so "
            "are cancelled and diverted flights: the task is the delay of a flight that operates."
        ),
    )

    # Dataset
    unique_name = "aeolus_1m"
    version_of = "aeolus"
    version_comment = """
        The release holds 54,674,003 flights of 2016-2024; we keep the 12,930,302 from 2023 on (curation notes). We sample per test window (v2 split protocol): each window keeps at most 500k of its rows (all of them here), and its train side is a random 1M of the earlier flights, drawn in one random order for all windows; the frame keeps only the rows a split uses.
    """
    year = "2025"
    domain = "industry & manufacturing"  # transport has no value of its own; as for nyc_taxi_trip_duration
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/flnny123/mfddmulti-modal-flight-delay-dataset"
    license = "Apache-2.0 (Kaggle data card); the paper (Appendix A.3) states CC BY-NC 4.0"
    data_tags = ("Spatial",)
    download_description = """
        The nine yearly tables of the release's tabular modality (Aeolus/Flight_Tab, 15.2 GB) from the authors' Kaggle
        dataset; the flight-chain (.pt) and flight-network (.dgl) files of the release are not used. Kaggle offers no
        versioned download for this dataset: the files are dated 2025-10-17 (downloaded 2026-10-07).

        mkdir -p local-data-warehouse/aeolus && cd local-data-warehouse/aeolus
        for year in 2016 2017 2018 2019 2020 2021 2022 2023 2024; do
            kaggle datasets download flnny123/mfddmulti-modal-flight-delay-dataset -f Aeolus/Flight_Tab/flight_with_weather_${year}.csv -p .
        done

        SHA-256 of the CSVs (first 16 hex digits): 2016 4ed92ed732721a38, 2017 67b8dbd6678576b1, 2018 0398bab8f1b79a5f,
        2019 eec50211a1a63f37, 2020 787981046c9fe0f4, 2021 5b7cc4801a6ff5cf, 2022 45eb45e801d6eeeb,
        2023 9c9e20f55d3dd10a, 2024 f938ade95a031088. `_prepare_raw_files` writes aeolus_flights.parquet next to them.
    """
    bibtex = """
        @inproceedings{xu2025aeolus,
          title     = {Aeolus: A Multi-structural Flight Delay Dataset},
          author    = {Xu, Lin and Yuan, Xinyun and Liang, Yuxuan and Yin, Suwan and Wu, Yuankai},
          booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2025), Datasets and Benchmarks Track},
          year      = {2025},
          note      = {arXiv:2510.26616},
        }
    """
    curation_comments = """
        We start with the nine yearly tables `Aeolus/Flight_Tab/flight_with_weather_<year>.csv` (2016-2024) of the authors' Kaggle release of Aeolus (Xu et al., NeurIPS 2025): 54,674,003 completed US domestic flights with hourly Meteostat weather at both airports, of which we keep the 12,930,302 from 2023 on.

        - Prediction point: shortly before the scheduled departure, with the paper's tabular features (Table 9).
        - History: we keep the flights from 2023-01-01 on (`HISTORY_START`), what a delay model refit every two weeks would train on: two seasonal cycles with the previous holidays, without COVID-19 (2020: 9.7% delayed against 17-21%). The authors' benchmarks use 2024 alone (Sec. 4.1 and 4.2). The 2016-2018 precipitation code and the one flight recorded twice (2018) fall before it.
        - Target: `ARR_DEL15` is "Yes" for an arrival 15 minutes or more after the schedule, the US DOT definition; the paper's classification task uses more than 15 minutes (0.68% of the flights differ). We do not use the minutes (ARR_DELAY): in 2023 and 2024 the 1% longest delays hold 66-68% of their variance, so an RMSE would mostly score a few extreme delays (third decision). The probe on the source label: untuned LightGBM reached R² 0.01-0.02 on the minutes (2026-10-07, all nine years).
        - Note: the authors' classifier code labels `abs(ARR_DELAY) > 15`, which counts early arrivals as delayed; we follow the DOT definition.
        - Dropped as recorded at or after the departure: DEP_DELAY, TAXI_OUT, WHEELS_OFF, WHEELS_ON, TAXI_IN, ACTUAL_ELAPSED_TIME, AIR_TIME, DEP_TIME and ARR_TIME (the last two read for the first decision), and ARR_DELAY, the target's source. Also not read: FLIGHTS (always 1), ORIGIN_INDEX and DEST_INDEX (one per airport) and the parts of FL_DATE.
        - CRS_DEP_TIME and CRS_ARR_TIME are local clock times dated on the flight date; we keep their time of day in minutes (`CRS_DEP_TIME_MIN`, `CRS_ARR_TIME_MIN`, as the authors' code does).
        - Anomaly: the release joined Meteostat's hourly records, whose timestamps are UTC, to the local scheduled clock times (first and second decision). So the origin weather is from 3.5 to 11.4 hours before the departure depending on the time zone (median 5.2), the destination weather a median 3.0 hours. Kept as released (curator, 2026-10-12).
        - Anomaly: the release dates the scheduled arrival on FL_DATE, so the 460,592 overnight arrivals (3.6% of the kept history) carry the destination reading of the departure date at the arrival's clock hour, a median 25 hours before the departure.
        - LEAK-6 (CC 2026-10-26, issue 7): a weather reading taken after the scheduled departure is set missing: the destination weather of 1.94% of the flights (0.9-1.1% in each test window; a median 0.7 hours and at most 4.4 hours after the departure) and the origin weather of the 686 departures from Guam (106 in the frame, about 10 hours after). Each airport's reading hour is timed in UTC with its time zone (`AIRPORT_TIME_ZONES`, from the coordinates). The mask costs 0.0003-0.0004 ROC AUC per window (untuned LightGBM, 1M train rows); all of the destination weather adds 0.008-0.016. The weather is otherwise as released; a re-join from BTS and Meteostat is the new record aeolus_rebuilt.
        - Proxy missing values: scheduled block times below 15 minutes (3 rows) become missing; the shortest real hop is 18 minutes. Four implausible longer block times stay (17-60 minutes on routes with medians of 90-133 minutes).
        - Impossible weather becomes missing: temperatures below -50 C (-60.6 C at Sarasota in May) and mean wind speeds above 120 km/h recorded without rain (up to 232 km/h), about 0.001% of the rows.
        - Repair: the release stores Guam's longitude and Pago Pago's latitude with the wrong sign; we set the true signs (`TRUE_SIGNS`).
        - Note: the release writes a scheduled midnight as 23:59 (no 00:00 in the kept history), and has no weather for the flights of 2024-12-31 scheduled from 23:30 on (the nearest hour falls in the next year's file), about 300 missing readings in the newest window.
        - OP_CARRIER_FL_NUM is categorical (the paper's Table 9). A service is the carrier plus the number: 92.8% of the numbers are used by more than one carrier, so a model has to combine it with OP_CARRIER.
        - Task probes (50k training rows per window): flag `no_spread` (LightGBM minus linear +0.036, paired standard error 0.019), kept as for amex_non_iid_1m; ROC AUC LightGBM 0.612, linear 0.594, the best single feature (a scheduled time) 0.581. With the full 1M training rows LightGBM reaches 0.629-0.630.
        - Note: the release holds no cancelled or diverted flights, so the task is the delay of a flight that operates.
        - Anomaly: March 2024 is missing from the release, a gap in the training history; the test windows are not affected.
    """

    # Task
    target = "ARR_DEL15"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC and ACC for the delay-occurrence classification task",
        reference=(
            "Xu et al., Aeolus: A Multi-structural Flight Delay Dataset, NeurIPS 2025 D&B, arXiv:2510.26616 "
            "(Sec. 4, Appendix: 'using Area Under the Curve (AUC) and Accuracy (ACC) as evaluation metrics')"
        ),
        definition="ROC AUC of the probability of an arrival delay of 15+ minutes",
    )

    # Splits
    splits_comment = """
        A delay model is refit every two weeks and predicts the flights of the two weeks ahead from the schedule and the weather. We use the last six weeks of 2024 as three two-week test windows (2024-12-18 to 12-31, 12-04 to 12-17 and 11-20 to 12-03, newest first; 25.8%, 16.7% and 17.3% of the flights late), so that one window, not two of three weekly ones, falls in the holiday peak (20.8% late over 2024). Train is every flight from 2023 on dated at least two days before the window (a one-day gap): a flight's arrival delay is known only once it has landed, and the previous evening's departures and long delays land after midnight. Each window keeps all of its flights (258,551, 256,013 and 269,272); each train side is a random 1M of the earlier flights (one random order for all windows). The authors split 1-15 June 2024 chronologically 6:2:2 (Sec. 4.1): one test stretch of about three days and no season, so we depart from it. All three windows lie in late November and December: the score measures early-winter delays.
    """
    temporal = Temporal(on="FL_DATE", splits=TemporalSplits(window=14, unit="days", n_windows=3, gap=1))
    subsample_to_budget = True

    # The nine CSVs (15.2 GB) are too large for pandas: `_prepare_raw_files` converts them once, streaming with
    # polars, into one parquet file with every source column and the timestamps parsed.
    prepared_raw_files = ("aeolus_flights.parquet",)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        import polars as pl

        files = sorted(raw_dir.glob("flight_with_weather_*.csv"))
        assert len(files) == 9, f"Expected the nine yearly files 2016-2024, found {len(files)}."
        header = files[0].open().readline().strip().split(",")
        timestamps = ["FL_DATE", "CRS_DEP_TIME", "DEP_TIME", "WHEELS_OFF", "WHEELS_ON", "CRS_ARR_TIME", "ARR_TIME"]
        text = [*timestamps, "OP_CARRIER", "ORIGIN", "DEST"]
        integers = ["MONTH", "DAY_OF_MONTH", "DAY_OF_WEEK", "ORIGIN_INDEX", "DEST_INDEX"]
        schema = {c: pl.String if c in text else pl.Int64 if c in integers else pl.Float64 for c in header}
        frames = [pl.scan_csv(f, schema=schema) for f in files]
        pl.concat(frames, how="vertical").with_columns(
            pl.col(c).str.to_datetime("%Y-%m-%d %H:%M:%S", time_unit="us", strict=True) for c in timestamps
        ).sink_parquet(raw_dir / "aeolus_flights.parquet")

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import pyarrow.parquet as pq

        path = raw_dir / "aeolus_flights.parquet"
        columns = [c for c in pq.read_schema(path).names if c not in SKIPPED_COLUMNS]  # in the source's order
        table = pq.read_table(
            path,
            columns=columns,
            read_dictionary=["OP_CARRIER", "ORIGIN", "DEST"],
            filters=[("FL_DATE", ">=", pd.Timestamp(HISTORY_START))],  # only the kept history is read
        )
        return table.to_pandas(split_blocks=True, self_destruct=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Target: an arrival 15 minutes or more after the schedule (US DOT on-time definition, BTS `ARR_DEL15`).
        late = (df["ARR_DELAY"] >= DELAY_THRESHOLD_MINUTES).to_numpy().astype("int8")
        df["ARR_DEL15"] = pd.Categorical.from_codes(late, categories=["No", "Yes"])
        # The scheduled times as local minutes since midnight (their date part is FL_DATE, also after midnight).
        for col in ("CRS_DEP_TIME", "CRS_ARR_TIME"):
            df[f"{col}_MIN"] = (df[col].dt.hour * 60 + df[col].dt.minute).astype("int64")
        # Proxy missing values: impossible scheduled block times.
        df["CRS_ELAPSED_TIME"] = df["CRS_ELAPSED_TIME"].mask(df["CRS_ELAPSED_TIME"] < MIN_SCHEDULED_MINUTES)
        # Impossible weather readings to missing.
        for side in ("O", "D"):
            df[f"{side}_TEMP"] = df[f"{side}_TEMP"].mask(df[f"{side}_TEMP"] < MIN_TEMPERATURE_C)
            df[f"{side}_WSPD"] = df[f"{side}_WSPD"].mask(df[f"{side}_WSPD"] > MAX_WIND_KMH)
        # Repair: the two airports whose coordinates the release stores with the wrong sign.
        for side, airport in (("O", "ORIGIN"), ("D", "DEST")):
            for code, (axis, sign) in TRUE_SIGNS.items():
                rows = (df[airport] == code).to_numpy()
                df.loc[rows, f"{side}_{axis}"] = sign * df.loc[rows, f"{side}_{axis}"].abs()
        # A weather reading taken after the prediction point, shortly before the scheduled departure, is missing (CC
        # 2026-10-26, LEAK-6): the release reads the local clock hour as UTC, so the destination reading lies after
        # the departure for about 2% of the flights and the origin reading for the departures from Guam.
        departure_utc = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns, UTC]")
        for airport, rows in df.groupby("ORIGIN", observed=True).groups.items():
            local = df.loc[rows, "CRS_DEP_TIME"].dt.tz_localize(
                AIRPORT_TIME_ZONES[airport], ambiguous="NaT", nonexistent="shift_forward"
            )
            departure_utc[rows] = local.dt.tz_convert("UTC")
        for side, clock in (("O", "CRS_DEP_TIME"), ("D", "CRS_ARR_TIME")):
            reading_utc = (df[clock] + pd.Timedelta(minutes=30)).dt.floor("h").dt.tz_localize("UTC")
            after = (reading_utc > departure_utc).to_numpy()
            df.loc[after, [f"{side}_{w}" for w in WEATHER]] = np.nan
        # A flight number is a label of its carrier, not a quantity (the CSV writes 4814.0).
        df["OP_CARRIER_FL_NUM"] = df["OP_CARRIER_FL_NUM"].astype("int64")
        # Categories in sorted order, whatever order the parquet dictionary had.
        for col in ("OP_CARRIER", "ORIGIN", "DEST"):
            df[col] = df[col].cat.reorder_categories(sorted(df[col].cat.categories))
        df = drop_columns(
            df,
            [
                "DEP_TIME",  # the actual times, read for the first decision only
                "ARR_TIME",
                "ARR_DELAY",  # the target's source
                "CRS_DEP_TIME",  # replaced by CRS_DEP_TIME_MIN
                "CRS_ARR_TIME",  # replaced by CRS_ARR_TIME_MIN
            ],
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["OP_CARRIER", "OP_CARRIER_FL_NUM", "ORIGIN", "DEST"],
            datetime=["FL_DATE"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        year = raw["FL_DATE"].dt.year
        # 1. Which times the weather belongs to: in 2024, the share of (airport, hour) groups of flights with one value.
        times = ["CRS_DEP_TIME", "DEP_TIME", "CRS_ARR_TIME", "ARR_TIME"]
        last = raw.loc[(year == 2024).to_numpy(), ["ORIGIN", "DEST", "O_TEMP", "D_TEMP", *times]]
        rows = []
        for side, airport, weather, keys in (
            ("origin", "ORIGIN", "O_TEMP", ("CRS_DEP_TIME", "DEP_TIME")),
            ("destination", "DEST", "D_TEMP", ("CRS_ARR_TIME", "ARR_TIME")),
        ):
            for key in keys:
                for how in ("nearest, half up", "floor"):
                    shift = pd.Timedelta(minutes=30 if how == "floor" else 0)
                    hour = (last[key] + pd.Timedelta(minutes=30) - shift).dt.floor("h")
                    groups = last.groupby([last[airport], hour], observed=True)[weather].agg(["nunique", "size"])
                    groups = groups[(groups["size"] > 1) & (groups["nunique"] > 0)]
                    rows.append(
                        {
                            "weather": side,
                            "time": key,
                            "hour": how,
                            "groups of 2+ flights": len(groups),
                            "share with one value": round(float((groups["nunique"] == 1).mean()), 4),
                        }
                    )
        alignment = pd.DataFrame(rows)

        # 2. The clock hour was read as UTC: the coldest and warmest scheduled departure hours of summer 2024 per
        # airport (mean origin temperature, hours with 30 or more flights), and the local time of those readings.
        summer = (
            (raw["FL_DATE"] >= "2024-06-01") & (raw["FL_DATE"] < "2024-09-01") & raw["ORIGIN"].isin(list(SUMMER_ZONES))
        )
        flights = raw.loc[summer.to_numpy(), ["ORIGIN", "CRS_DEP_TIME", "O_TEMP"]]
        clock = (flights["CRS_DEP_TIME"] + pd.Timedelta(minutes=30)).dt.floor("h").dt.hour.rename("clock")
        means = flights.groupby([flights["ORIGIN"].astype(str), clock])["O_TEMP"].agg(["mean", "size"])
        means = means[means["size"] >= 30]
        cycle = []
        for airport, zone in SUMMER_ZONES.items():
            offset = int(pd.Timestamp("2024-07-01", tz=zone).utcoffset().total_seconds() // 3600)
            hours = means.loc[airport, "mean"].sort_values(kind="stable")
            coldest, warmest = int(hours.index[0]), int(hours.index[-1])
            cycle.append(
                {
                    "airport": airport,
                    "UTC offset (July)": offset,
                    "coldest scheduled hour": coldest,
                    "coldest mean (C)": round(float(hours.iloc[0]), 1),
                    "coldest reading, local hour": (coldest + offset) % 24,
                    "warmest scheduled hour": warmest,
                    "warmest mean (C)": round(float(hours.iloc[-1]), 1),
                    "warmest reading, local hour": (warmest + offset) % 24,
                }
            )
        utc_reading = pd.DataFrame(cycle)

        # 3. The target: the minutes are dominated by a few long delays; the 15-minute indicator is not.
        delay = raw["ARR_DELAY"]
        per_year = []
        for y, minutes in delay.groupby(year):
            squared = (minutes - minutes.mean()) ** 2
            top = minutes >= minutes.quantile(0.99)
            per_year.append(
                {
                    "year": int(y),
                    "flights": len(minutes),
                    "mean delay (min)": round(float(minutes.mean()), 2),
                    "share 15 min or more": round(float((minutes >= DELAY_THRESHOLD_MINUTES).mean()), 4),
                    "99th percentile (min)": float(minutes.quantile(0.99)),
                    "variance share of the top 1%": round(float(squared[top].sum() / squared.sum()), 3),
                }
            )
        target = pd.DataFrame(per_year)

        return [
            Decision(
                "The weather is looked up by the scheduled clock times",
                "Grouped by airport and scheduled time rounded to the nearest hour (half up), every group of 2024 "
                "flights shares one weather value; grouped by the actual times far fewer do. So the actual departure "
                "and arrival, which carry the delay, played no part in the lookup. The next decision shows which hour "
                "the lookup returned.",
                alignment,
            ),
            Decision(
                "The scheduled clock hour was read as UTC: the weather is from 3.5 to 11 hours earlier",
                "The release joined Meteostat's hourly records, whose timestamps are UTC, to the local scheduled "
                "clock times. Read as local time, each airport's daily temperature cycle is shifted by its UTC offset "
                "(Honolulu would be coldest at 15 h and warmest at midnight); read as UTC, the coldest readings fall "
                "at 4-6 h and the warmest at 12-17 h local time at all nine airports. Meteostat's station files "
                "agree: read as UTC, the origin temperatures of 2024 equal them at 99.6% to 100% of the "
                "airport-hours at JFK, ORD, DEN, PHX, LAX, SEA and HNL, against 2% to 8% at the airports' real "
                "offsets (checked 2026-10-07; the station files are not part of the raw data).",
                utc_reading,
            ),
            Decision(
                "Target: arrival 15 minutes or more late",
                "In every year the 1% longest delays hold most of the variance of the arrival delay in minutes, so "
                "an RMSE on the minutes would mostly score a few extreme delays. The 15-minute indicator is the US "
                "DOT definition and the paper's classification task.",
                target,
            ),
        ]
