"""Curated dataset definition for `thailand_road_accident_register_2019_2022` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    SplitPlan,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

YEARS = (2019, 2020, 2021, 2022)  # the years of the approved record; 2023 recodes the site and the cause (notes)
# Two-month test windows; train is the crashes at least two months older that were reported before the window starts
WINDOWS = TemporalSplits(window=2, unit="months", n_windows=9, gap=2)
# The order of day and month in each year's file: no date left unparsed, no crash reported before it happens, and the
# Kaggle copy agrees (the 2022 XLSX swaps day and month of the report dates, so it is not the check; notes)
DATE_ORDER = {2019: "dmy", 2020: "mdy", 2021: "mdy", 2022: "mdy"}
EXCEL_EPOCH = pd.Timestamp("1899-12-30")
# Thailand's extent with a margin; coordinates outside it are entry errors
LATITUDE_RANGE, LONGITUDE_RANGE = (5.0, 21.0), (97.0, 106.0)
# The officer's drunk-driving codes, and the Department of Highways (the evidence for the kept presumed cause)
DRUNK_CODES = ("เมาสุรา", "มึนเมาจากแอลกอฮอล์")
HIGHWAYS = "กรมทางหลวง"

# The ministry's Thai column names (2019, and 2020-2022 where they differ) on one English schema
RENAME = {
    "ปีที่เกิดเหตุ": "file_year",
    "วันที่เกิดเหตุ": "crash_date",
    "เวลา": "crash_time",
    "วันที่รายงาน": "report_date",
    "เวลาที่รายงาน": "report_time",
    "ACC_CODE": "acc_code",
    "หน่วยงาน": "agency",
    "สายทางหน่วยงาน": "route_class",
    "รหัสสายทาง": "route_code",
    "สายทาง": "route",
    "ก.ม.": "km",
    "KM": "km",
    "จังหวัด": "province",
    "รถคันที่ 1": "vehicle_1",
    "รถคันที่1": "vehicle_1",
    "บริเวณที่เกิดเหตุ/ลักษณะทาง": "site",
    "บริเวณที่เกิดเหตุ": "site",
    "มูลเหตุสันนิษฐาน": "presumed_cause",
    "ลักษณะการเกิดอุบัติเหตุ": "collision_type",
    "ลักษณะการเกิดเหตุ": "collision_type",
    "จำนวนรถที่เกิดเหตุ (รวมคันที่ 1)": "vehicles",
    "รถที่เกิดเหตุ": "vehicles",
    "รถและคนที่เกิดเหตุ": "vehicles_and_pedestrians",
    "จำนวนผู้เสียชีวิต": "deaths",
    "ผู้เสียชีวิต": "deaths",
    "ผู้บาดเจ็บสาหัส": "serious_injuries",
    "ผู้บาดเจ็บเล็กน้อย": "minor_injuries",
    "รวมจำนวนผู้บาดเจ็บ": "injuries",
    "สภาพอากาศ": "weather",
    "LATITUDE": "latitude",
    "LONGITUDE": "longitude",
    "รถจักรยานยนต์": "n_motorcycle",
    "รถสามล้อเครื่อง": "n_three_wheeler",
    "รถยนต์นั่งส่วนบุคคล": "n_car",
    "รถตู้": "n_van",
    "รถปิคอัพโดยสาร": "n_pickup_passenger",
    "รถโดยสารมากกว่า4ล้อ": "n_bus",
    "รถปิคอัพบรรทุก4ล้อ": "n_pickup_cargo",
    "รถบรรทุก6ล้อ": "n_truck_6_wheels",
    "รถบรรทุกไม่เกิน10ล้อ": "n_truck_up_to_10_wheels",
    "รถบรรทุกมากกว่า10ล้อ": "n_truck_over_10_wheels",
    "รถอีแต๋น": "n_farm_vehicle",
    "รถอื่นๆ": "n_other_vehicle",
    "คนเดินเท้า": "n_pedestrian",
}
COUNT_COLUMNS = [
    "vehicles",
    "n_motorcycle",
    "n_three_wheeler",
    "n_car",
    "n_van",
    "n_pickup_passenger",
    "n_bus",
    "n_pickup_cargo",
    "n_truck_6_wheels",
    "n_truck_up_to_10_wheels",
    "n_truck_over_10_wheels",
    "n_farm_vehicle",
    "n_other_vehicle",
    "n_pedestrian",
]


def _parse_dates(text: pd.Series, year: int) -> pd.Series:
    """A date column of one yearly file: d/m/Y or m/d/Y by the year, or an Excel serial day number.

    The 2022 file writes a crash date whose day is 12 or less as day/month and every other date as month/day (an
    Excel locale conversion); the caller passes ``year=0`` for that column to read such dates as day/month.
    """
    text = text.astype("string").str.strip()
    parts = text.str.extract(r"^(\d{1,2})/(\d{1,2})/(\d{4})$").astype("Float64")
    first, second, yyyy = parts[0], parts[1], parts[2]
    # year 0: the 2022 crash dates, day/month where both parts are 12 or less
    day_first = (first <= 12) & (second <= 12) if year == 0 else pd.Series(DATE_ORDER[year] == "dmy", index=text.index)
    day = first.where(day_first, second)
    month = second.where(day_first, first)
    dates = pd.to_datetime(pd.DataFrame({"year": yyyy, "month": month, "day": day}).astype("float64"), errors="coerce")
    serial = pd.to_numeric(text.where(text.str.fullmatch(r"\d{5}")), errors="coerce")
    return dates.fillna(EXCEL_EPOCH + pd.to_timedelta(serial, unit="D"))


def _parse_times(text: pd.Series) -> pd.Series:
    """HH:MM, or an Excel day fraction, as a time since midnight."""
    text = text.astype("string").str.strip()
    hm = text.str.extract(r"^(\d{1,2}):(\d{2})$").astype("float64")
    fraction = pd.to_numeric(text.where(~text.str.contains(":", na=False)), errors="coerce")
    minutes = (hm[0] * 60 + hm[1]).fillna((fraction * 1440).round())
    return pd.to_timedelta(minutes, unit="min")


def _reported_before_windows(df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    """The windows of `WINDOWS`, each training only on the crashes reported before it starts.

    Returns the splits and, per window, the training rows kept and left out (the evidence in `_decisions`).
    """
    crash, report = df["crash_datetime"], df["report_datetime"]
    deaths = df["deaths"]
    splits, rows = {}, []
    for split, folds in WINDOWS.splits(df, "crash_datetime").items():
        train, test = (np.asarray(side) for side in folds[0])
        start = crash.iloc[test].min().normalize().replace(day=1)
        known = (report.iloc[train] < start).fillna(False).to_numpy()
        splits[split] = {0: (train[known].tolist(), test.tolist())}
        # the newest crashes a refit trains on: two to three months before the start (the gap is two months)
        newest = (crash >= start - pd.DateOffset(months=3)) & (crash < start - pd.DateOffset(months=2))
        rows.append(
            {
                "window start": f"{start:%Y-%m}",
                "test rows": len(test),
                "train rows": int(known.sum()),
                "train share of all rows": f"{known.sum() / len(df):.0%}",
                "left out (reported after the start)": int((~known).sum()),
                "crashes 2-3 months before the start: reported by then": f"{(report[newest] < start).mean():.0%}",
                "their deaths per crash: all / reported": (
                    f"{deaths[newest].mean():.3f} / {deaths[newest & (report < start)].mean():.3f}"
                ),
            }
        )
    return splits, pd.DataFrame(rows).set_index("window start")


class ThailandRoadAccidentRegister20192022(AbstractCuratedDataset):
    # In brief: the task in plain words, for a reader who has not seen the source (first in the README). One or two
    # plain sentences per field; the house format and examples are in knowledge-data-foundry definitions.md.
    task_summary = TaskSummary(
        question=(
            "How many people die in a road crash on Thailand's national highways, rural roads or expressways, given "
            "where, when and how it happened?"
        ),
        use_case=(
            "For example, a road agency's safety engineer screens the network for severity: the expected deaths of "
            "each recorded crash given its circumstances, summed per road section, rank sections, crash types and "
            "vehicle mixes for safety works, as the Highway Safety Manual's relative severity index does."
        ),
        row=(
            "One crash on the Ministry of Transport's road network (highways, rural roads, expressways) in its TRAMS "
            "register, 2019 to 2022 (81,059 crashes)."
        ),
        predicted=(
            "The number of people killed in the crash as the register records it; most crashes have none. How long "
            "after the crash a death still counts is not stated."
        ),
        known=(
            "When the agency screens its recorded crashes: the date and time, the agency, province, road, kilometre "
            "and coordinates, the road layout and slope, the weather, the first vehicle's type, the vehicles of each "
            "type and the pedestrians involved (from 2020), the kind of collision and the cause the officer presumed. "
            "Each record holds one realised count of deaths; the expected deaths the screen needs are on no record."
        ),
        split=(
            "Each test window is two months of crashes, July 2021 to December 2022; training is the crashes at least "
            "two months older that were in the register when the window starts, as for a model refit every two months."
        ),
        changes=(
            "We read the ministry's yearly files rather than the Kaggle copy, repair 2022 crash dates whose day and "
            "month were swapped, drop the injury counts, and train each window only on crashes already reported."
        ),
        fit="approximate",
        fit_reason=(
            "One crash stands in for a decision per road section and year, without crash frequency or traffic "
            "exposure. How long after the crash a death counts is not stated, and deaths are revised in place (41 of "
            "3,210 crashes changed in a 2024 revision). The officer's presumed cause and kind of collision are kept on "
            "purpose (notes). Roads and provinces recur, as they do for a real road agency."
        ),
    )

    # Dataset
    unique_name = "thailand_road_accident_register_2019_2022"
    year = "2026"
    domain = "social science"  # closest of the fixed list for road safety (as the 2015 DDPM sibling)
    source = "GOV Website"
    source_url = "https://datagov.mot.go.th/dataset/roadaccident"
    license = "Open Data Common (Thailand)"
    data_tags = ("Spatial",)
    download_description = """
        The Ministry of Transport's dataset `roadaccident` on datagov.mot.go.th (CKAN), one CSV per crash year; the
        ministry revises the files in place (2019 last on 2026-05-26, 2020-2022 on 2024-06-14), so this is the
        snapshot of 2026-10-30, with its MD5 sums.
        BASE=https://datagov.mot.go.th/dataset/7e077ffd-dc4f-4dc6-a71c-0813726f3c12/resource
        mkdir -p local-data-warehouse/thailand_road_accident_register_2019_2022 && cd $_
        curl -O $BASE/4d919e5b-aa06-4fe4-8a13-5571747a1254/download/accident2019.csv  # b1914b2a9631ea105cf5a64c9558a149
        curl -O $BASE/40476c7b-4194-4dc2-aba5-7326819ed071/download/accident2020.csv  # 2f7763cb5a243e99cfa631f9949ebde3
        curl -O $BASE/d0a8601a-3ee5-4ce8-8e9d-3dae3915dc30/download/accident2021.csv  # 6bc52defa66e4ca539500459053cb194
        curl -O $BASE/733b7874-bd5f-44b9-b271-650890b061f2/download/accident2022.csv  # 6a3d15e3039ffc54ed116dcec4e3944f
        md5sum accident20*.csv
        The Kaggle upload thaweewatboy/thailand-road-accident-2019-2022 (August 2023, CC0) is an English copy of an
        earlier version of these files; it is not read.
    """
    bibtex = r"""
        @misc{mot_trams_roadaccident_2026,
          author = {{Ministry of Transport, Office of the Permanent Secretary, Information and Communication Technology Centre}},
          title = {Accidents on the Road Network of the Ministry of Transport (TRAMS), yearly record files},
          year = {2026},
          howpublished = {\url{https://datagov.mot.go.th/dataset/roadaccident}},
          note = {Open government data, Open Data Common licence; files for 2019 to 2022, snapshot of 2026-10-30}
        }
    """
    curation_comments = """
        We start with the yearly crash files accident2019.csv to accident2022.csv of the Ministry of Transport's dataset `roadaccident` (TRAMS), snapshot of 2026-10-30.

        - Prediction point: a road agency screens the crashes recorded on its network (where, when, the road, the vehicles and pedestrians involved, how it happened and the cause the officer presumed) for the expected deaths of a crash given these circumstances. This is the severity part of network screening: the Highway Safety Manual's relative severity index (ch. 4) assigns each crash type its average severity, and the Department of Rural Roads ranks black spots by a severity-weighted equivalent accident number. No record holds that expectation, only one realised count (the target), so the model supplies what the agency does not have on file. Nothing recorded with the crash's other outcomes is a feature.
        - Source: the Office of the Permanent Secretary's ICT Centre publishes TRAMS, the reporting system of the Department of Highways, the Department of Rural Roads and the Expressway Authority, as one file per crash year (dataset page: "accidents on the ministry's road network: highways, rural roads and expressways", translated). It publishes no codebook, no task and no metric. The Kaggle upload of August 2023 (thaweewatboy, the record's second link) is an English copy of an earlier version and is not read: the ministry revised the 2020-2022 files in June 2024, and 21,040 of 21,239, 19,869 of 20,062 and 17,180 of 20,566 of today's crashes have the Kaggle copy's accident code; on those, deaths and injuries agree in every row.
        - Years: 2019 to 2022, the scope of the record that was approved. The 2023 file codes the site and the cause in another scheme (7.5% and 20.0% of its site and cause labels occur in 2019-2022, against 94.0% of its collision types; the code for a straight road without slope holds 50 crashes in 2023 against 13,409 to 16,810 in every other year) and holds 1,641 crashes two or three times (1,702 extra rows; the copies agree on deaths in every case). 2024 and 2025 use the older scheme (99.9-100% of their labels occur in 2019-2022), about 47,700 crashes. An extension to 2025, with 2023's site and cause masked and its repeats dropped, is possible and left open (REVIEW.md). Not 2026: the year is still being reported.
        - Time: the crash date and time. Each file writes dates its own way: 2019 day/month/year, 2020-2022 month/day/year, and one 2020 crash as an Excel day number. These orders leave no date unparsed and no crash reported before it happens in any file; the XLSX date cells agree on the 2019-2021 crash dates and the 2019 report dates, the Kaggle copy on the 2020-2021 report dates. The 2022 XLSX (revised 2025-07-23) swaps day and month for 6,823 report dates; the CSV's month/day reading is kept because it leaves 0 crashes reported before they happen (1,579 under the XLSX reading), follows the accident-code order (172 report dates more than 30 days off their neighbours' against 518) and agrees with the Kaggle copy on 99.98%.
        - Repair (2022): the 2022 file writes a crash date whose day is 12 or less as day/month and every other one as month/day. Read as month/day, 2,472 crashes would be reported before they happened; read as day/month where both parts are 12 or less (7,268 dates change), none is. On the crashes the Kaggle copy also has, its dates agree with this reading for 6,088 of 6,088 such dates and the month/day reading for 10,345 of 10,345 others; the XLSX date cells agree on all 8,135 ambiguous crash dates, and the holiday peaks fall on 1-3 January and in Songkran.
        - Empty rows: the 2019 file ends in 21,052 empty rows; dropped.
        - Duplicates: two crashes entered twice in adjacent rows (accident codes 7678227 and 7678228 in 2020, 7508085 and 7508100 in 2022), identical in every other field; one record of each kept. Four more pairs share the crash time, the exact coordinates and the deaths but differ in one to six fields; they stay (not exact copies), and each pair falls inside one window, so no copy crosses the split.
        - Dropped for what they are: the accident code (an identifier), the file year (the crash year), the route class (a copy of the agency), the vehicles-and-pedestrians total (the vehicle count plus the pedestrians in every row), the bus and farm-vehicle counts (0 in every row: the files count those vehicles under other vehicles), and the injured, serious and minor (the crash's other outcomes, recorded with its deaths; LEAK-10).
        - Dropped for what they are, after the split: the report date and time. The record is entered a median of 27 days after a fatal crash and 57 days after one without a death (LEAK-10: recorded after the outcome, and its delay follows it: 15-20% of the crashes reported within a week had a death, 8% of those reported after four months). It sets which crashes each window trains on (splits_comment) and is then removed.
        - Site: the source's site code joins the road layout and, for 70,154 crashes, the slope ("straight+no slope"); split into road_layout and road_slope (CLEAN-12). Category labels stay in the source's Thai.
        - Missing values: 4 coordinate pairs outside Thailand (one with latitude and longitude swapped, 100 and 13) are entry errors, made missing (211 missing in all). A vehicle count of 0 with no first vehicle recorded (86 crashes) is not recorded, made missing; 20 crashes with a pedestrian as the first party and no vehicle keep 0. The 2019 file has no vehicle counts by type, no pedestrian count and no route code: missing for its 19,194 crashes. The collision type is missing for 50 crashes of 2019 and about 1,200 a year from 2020, nearly all the Department of Rural Roads' (3,425 of its 3,547 crashes of 2020-2022), which stopped filling the field; within each agency a blank collision type is less often fatal (2020-2022: highways 4.7% against 11.1%, rural roads 30.0% against 35.2%).
        - Gaps of incomplete records, kept: 213 highway crashes without a kilometre post are fatal in 1.9% (11.4% for the rest) and 73 rural-road crashes without a first vehicle in none (30% for the rest); masking these gaps costs R^2 0.0028 (SE 0.0009, 9 windows, untuned LightGBM). Whether a gap follows the outcome or marks a minor crash recorded in less detail is open; they stay as recorded (LEAK-6).
        - Agencies: the three record to different thresholds. Crashes with no death or injury are 10-12% of the rural roads department's records, 43-48% of the highways department's and 65-76% of the expressway authority's, and 28-32% of rural-road records have a death against 10-12% on highways. Every expressway crash lacks the presumed cause (666 of the 685 missing). `agency` is a feature, so a model learns each threshold, as an agency ranking its own network would.
        - Potential leak, kept on purpose: `presumed_cause` (53 codes) and `collision_type` are the reporting officer's reading, entered in the record that holds the deaths (a median 27 days after a fatal crash), so a death could change what is written. The trace is the drunk-driving code: on highways off the New Year and Songkran campaign days (27 Dec-4 Jan, 10-18 Apr, when police test drivers for alcohol widely) 21.3% of the 315 crashes coded drunk had a death against 11.3% of the rest, on campaign days 11.6% against 11.8% (decision table). Given the hour, weekend, year, first vehicle, collision type, road layout and vehicle count, the off-campaign odds ratio falls from 2.10 to 1.17 (95% CI 0.88-1.57, approximate), and blanking the code on the 530 crashes the trace locates changes R^2 by +0.001 to +0.003 over 3 seeds (9 windows, untuned LightGBM), against at most 0.0015 that part could carry. The column's gain (R^2 +0.0077, SE 0.0021) sits on codes an officer reads at the scene: cutting in, running a signal, illegal overtaking, driving the wrong way (20-48% fatal); speeding, the default code, is given for 75% of crashes without a death and 69% with one. The collision type is a fact of the scene; its blanks follow the agency (above). They stay because the part that can be traced carries no gain (LEAK-10) and both describe the crash a road agency screens on. Revisit if the task moves to a first-report prediction point, or if a TRAMS codebook says when the cause is entered.
        - Zero inflation: 70,958 of 81,059 crashes (87.5%) have no death, 8,794 one, 1,307 two to thirteen. The zero is observed, a recorded crash without a death, and no more frequent than one count model gives: a Poisson model given the features predicts 89.2% zeros on the test windows against 89.0% observed (a negative binomial with the target's mean and variance and no extra zeros: 87.9% against 87.5%). On the 9 windows most of the signal is whether anyone dies (ROC AUC 0.840); how many die once someone does is weakly predictable (R^2 0.03 on the fatal crashes with a regularised Poisson model, positive in 9 of 9 windows; an untuned model overfits to -0.05). A hurdle model scores as one model (R^2 0.174 against 0.171).
        - Coding breaks, kept as published (the source gives no crosswalk): records entered from November 2022 use finer cause codes (tyre, brakes, slippery road, loss of control and reckless crossing in place of equipment defect and other; 591 crashes, 577 of them reported in November 2022 or later), and 1,527 crashes entered in December 2022 have no route name but keep `route_code`. Neither reaches a training set, since each window trains on crashes reported before it starts; 64 of the 3,537 rows of the newest window carry a cause code unseen in training.
        - Note: how long after the crash a death counts is not stated anywhere we looked (dataset page, Kaggle card, the ministry's New Year 2565 report, a web search for TRAMS definitions). Deaths are revised in place: of the 3,210 crashes of 2022 that the June 2024 revision gave a new accident code, 41 changed their deaths (32 down, 9 up).
    """

    # Task
    target = "deaths"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "The ministry publishes the register as open data with no task, codebook or metric (dataset page "
            "datagov.mot.go.th/dataset/roadaccident); the Kaggle copy has no competition, discussion or notebook. The "
            "one paper on the register, Ratanawimon and Tanawongsuwan (EECSS 2024, CIST 179, "
            "doi:10.11159/cist24.179), classifies fatal against injured crashes in the 81,735 Kaggle-era records on a "
            "random 80/20 split and reports precision, recall, F1, balanced accuracy and ROC AUC side by side, none "
            "named as the criterion (MET-5), so the fallback applies. The field's loss for a count, the Poisson "
            "deviance, is not in the metric library and needs strictly positive predictions. Crashes with three or "
            "more deaths (0.3% of the test rows) hold 14-34% of each window's squared error, and the top models "
            "differ by less than their paired standard error."
        )
    )
    splits_comment = """
        A model refit at the start of every second month predicts the deaths of the crashes of the next two months. It trains on the crashes at least two months older that the register holds by then. A crash reaches the register a median of 53 days after it happens (27 days for a fatal crash, 57 otherwise; one in ten after more than eight months), so at a refit many recent crashes are missing and the reported ones are more often fatal (decision table): only crashes reported before the window starts train it, which leaves out 941 to 4,790 older crashes per window. The two-month gap, about the median delay, leaves out the months where the reported share is lowest (7-59% reported). Crashes two to four months old are still partly reported (48-96%), and the reported ones are more often fatal (11.3-14.6% against 10.0-12.4% of all of them), as at a real refit; no bias is measured (mean prediction over mean truth 0.96-0.98).

        The cadence is ours, as the source states no horizon: two-month windows are the shortest that fill 9 windows and cover every season once (Songkran 2022 in one window, New Year in three); quarterly windows keep half the rows in training for only 7. The test windows walk back from November-December 2022 to July-August 2021: 9 windows, newest first, 2,492 to 3,978 test crashes and 47,333 to 69,688 training crashes (58% to 86% of the rows).

        The full expanding history is kept, with its breaks: 2019 has no counts by vehicle type and no route code, April 2020 has about half the crashes of April 2019 (COVID-19, no Songkran), deaths per crash fall from 0.168 (2019) to 0.127 (2022), and the two oldest test windows fall in the low-traffic months of 2021. Without 2019 the two oldest windows would train on 49% and 46% of the rows.

        On the 9 windows the reporting filter and the gap change little: untuned LightGBM (Poisson, without the two route columns) on the shipped frame gives RMSE 0.3616 trained on every earlier crash, 0.3619 on those reported by the window start (+0.0002, paired SE 0.0009) and 0.3628 with the gap (+0.0011, paired SE 0.0012).
    """
    temporal = Temporal(on="crash_datetime", horizon=2, horizon_unit="months", gap=2, gap_unit="months")

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        frames = []
        for year in YEARS:
            df = pd.read_csv(raw_dir / f"accident{year}.csv", encoding="utf-8-sig", dtype=str)
            df = df.dropna(how="all")  # the 2019 file ends in 21,052 empty rows
            frames.append(df.rename(columns=RENAME).assign(file=year))
        return pd.concat(frames, ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. Crash and report times from each file's own date format (DATE_ORDER), the 2022 crash dates repaired
        crash_date = pd.concat(
            [_parse_dates(df.loc[df["file"] == y, "crash_date"], 0 if y == 2022 else y) for y in YEARS]
        ).reindex(df.index)
        report_date = pd.concat([_parse_dates(df.loc[df["file"] == y, "report_date"], y) for y in YEARS]).reindex(
            df.index
        )
        df["crash_datetime"] = crash_date + _parse_times(df["crash_time"])
        df["report_datetime"] = report_date + _parse_times(df["report_time"])
        # 2. The same crash entered twice in adjacent rows under another accident code: keep one record
        df = df.drop_duplicates(subset=[c for c in df.columns if c != "acc_code"], keep="first").copy()
        # 3. Numbers
        for col in ["deaths", "km", "latitude", "longitude", *COUNT_COLUMNS]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        # 4. Coordinates outside Thailand are entry errors: missing
        bad = ~df["latitude"].between(*LATITUDE_RANGE) | ~df["longitude"].between(*LONGITUDE_RANGE)
        df.loc[bad, ["latitude", "longitude"]] = np.nan
        # 5. No vehicle and no first vehicle recorded: the vehicle count 0 is not recorded, so missing
        df.loc[(df["vehicles"] == 0) & df["vehicle_1"].isna(), "vehicles"] = np.nan
        # 6. The site is the road layout and, for most crashes, its slope ("straight+no slope"): two columns
        site = df["site"].str.split("+", n=1, expand=True)
        df["road_layout"], df["road_slope"] = site[0].str.strip(), site[1].str.strip()
        # 7. Drops: identifiers and raw text of the times, copies, the bus and farm-vehicle counts (0 in every row: the
        #    files count those vehicles under n_other_vehicle) and the crash's other outcomes (the injuries).
        #    report_datetime stays for `_make_splits`, which drops it.
        return drop_columns(
            df,
            [
                "acc_code",
                "file",
                "file_year",
                "crash_date",
                "crash_time",
                "report_date",
                "report_time",
                "route_class",
                "vehicles_and_pedestrians",
                "n_bus",
                "n_farm_vehicle",
                "injuries",
                "serious_injuries",
                "minor_injuries",
                "site",
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "agency",
                "province",
                "vehicle_1",
                "road_layout",
                "road_slope",
                "presumed_cause",
                "collision_type",
                "weather",
            ],
            string=["route", "route_code"],
            datetime=["crash_datetime", "report_datetime"],
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        """Two-month windows after a two-month gap; train keeps only the crashes reported before the window starts."""
        splits, _ = _reported_before_windows(df)
        return SplitPlan(splits=splits, df=df.drop(columns=["report_datetime"]))

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df  # the shipped frame has no report time; rebuild the cleaned frame with it
        frame = self._clean(raw.copy()).sort_values("crash_datetime", kind="stable").reset_index(drop=True)
        _, windows = _reported_before_windows(frame)

        # The 2022 crash dates, read as month/day throughout or repaired
        r22 = raw[raw["file"] == 2022]
        report = _parse_dates(r22["report_date"], 2022) + _parse_times(r22["report_time"])
        time = _parse_times(r22["crash_time"])
        month_day = _parse_dates(r22["crash_date"], 2022) + time
        repaired = _parse_dates(r22["crash_date"], 0) + time
        repair = pd.DataFrame(
            {
                "2022 crashes": [len(r22), len(r22)],
                "crash dates that differ from month/day": [0, int((repaired != month_day).sum())],
                "reported before the crash": [int((report < month_day).sum()), int((report < repaired).sum())],
            },
            index=pd.Index(
                ["month/day throughout", "day/month where day and month are both 12 or less (shipped)"],
                name="reading of the 2022 crash dates",
            ),
        )

        # Deaths by reporting delay: the delay follows the outcome
        delay = (frame["report_datetime"] - frame["crash_datetime"]).dt.days
        bins = pd.cut(
            delay,
            [-1, 1, 7, 30, 60, 120, 240, 2000],
            labels=["0-1", "2-7", "8-30", "31-60", "61-120", "121-240", "over 240"],
        )
        by_delay = frame.groupby(bins, observed=True)["deaths"].agg(
            crashes="size", share_with_a_death=lambda d: round(float((d > 0).mean()), 3), deaths_per_crash="mean"
        )
        by_delay.index.name = "days from crash to report"

        # The drunk-driving code by outcome on the highways, off and on the New Year and Songkran campaign days
        # (27 Dec-4 Jan, 10-18 Apr), when police test drivers for alcohol widely: the trace of the officer's reading
        day = frame["crash_datetime"].dt.month * 100 + frame["crash_datetime"].dt.day
        campaign = (day >= 1227) | (day <= 104) | day.between(410, 418)
        drunk = frame["presumed_cause"].isin(DRUNK_CODES)
        highways, fatal = frame["agency"] == HIGHWAYS, frame["deaths"] > 0
        trace = pd.DataFrame(
            [
                {
                    "coded drunk driving": int((rows & drunk).sum()),
                    "share with a death (drunk driving)": round(float(fatal[rows & drunk].mean()), 3),
                    "other crashes": int((rows & ~drunk).sum()),
                    "share with a death (others)": round(float(fatal[rows & ~drunk].mean()), 3),
                }
                for rows in (highways & ~campaign, highways & campaign)
            ],
            index=pd.Index(["off the campaign days", "on the campaign days"], name="highway crashes"),
        )
        return [
            Decision(
                "Each window trains on the crashes at least two months older that were reported before it starts",
                "A crash reaches the register weeks to months after it happens, fatal crashes sooner, so at a refit "
                "the recent crashes on record are fewer and more often fatal. Only crashes reported before the "
                "window starts train it, and a two-month gap leaves out the months with the lowest reported share.",
                windows,
            ),
            Decision(
                "The 2022 crash dates with day and month both 12 or less are read as day/month",
                "The 2022 file writes those dates day/month and the rest month/day. Read as month/day throughout, "
                "thousands of crashes are reported before they happen; the repaired reading leaves none, and it "
                "agrees with the Kaggle copy of 2023 on every crash both hold (curation_comments).",
                repair,
            ),
            Decision(
                "The report date is not a feature",
                "It is entered after the crash and its delay follows the outcome: crashes reported within a week "
                "had a death about twice as often as those reported after four months.",
                by_delay.round(3),
            ),
            Decision(
                "The officer's presumed cause and collision type stay (potential leak, kept on purpose)",
                "Both are entered in the record that holds the deaths. Off the campaign days a highway crash coded "
                "drunk driving has a death about twice as often as the rest, on them not, which fits an alcohol test "
                "made because someone died. Given the crash's hour, weekend, year, first vehicle, collision type, "
                "layout and vehicle count, the off-campaign odds ratio is 1.17 (95% CI 0.88-1.57), and blanking the "
                "code on the 530 crashes the trace locates loses no score (R^2 +0.001 to +0.003 over 3 seeds, 9 "
                "windows, untuned LightGBM; at most 0.0015 for an oracle). The column's gain sits on codes read at "
                "the scene (curation_comments).",
                trace,
            ),
        ]
