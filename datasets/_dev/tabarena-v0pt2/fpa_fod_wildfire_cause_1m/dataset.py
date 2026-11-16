"""Curated dataset definition for `fpa_fod_wildfire_cause_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
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
    drop_columns,
)

MAP_SERVICE = "https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_FireOccurrenceCurrentEdition_01/MapServer/0"
"""The USFS map-service layer `Fire_FPA_FOD_7th_Fires` that serves the 7th edition (2,661,383 records)."""

N_RECORDS = 2_661_383
"""Records of the 7th edition ("Point and Vector Object Count: 2661383" in the layer's FGDC metadata)."""

PREPARED = "fpa_fod_7th_fires.parquet"

UNDETERMINED = "Missing data/not specified/undetermined"
"""The cause class of the fires whose cause was not determined: the unlabelled pool, not a class."""

OTHER = "Other causes"
"""The standard's residual class ("any wildfire that does not fit into the identified general or specific cause"),
since 2021 a recording convention of a few states' reports (the decision table): left out with the undetermined."""

LARGE_FIRE_SOURCES = ["IA-ICS209", "IA-MTBS"]
"""Records drawn only from the ICS-209 situation reports or the MTBS perimeters, which exist for fires that grew large:
4,038 and 220 records, whose cause is named only for 629 and 23 lightning fires and 2 power-line fires."""

OWNER_MISSING = "MISSING/NOT SPECIFIED"
"""The land owner's code for an owner not recorded (CLEAN-10)."""

TARGET_ENCODINGS = ["nwcg_cause_classification", "nwcg_cause_age_category"]
"""Other encodings of the target (LEAK-10): Human or Natural ("Natural" exactly where the target is), and "Minor" for
every fire of "Misuse of fire by a minor"."""

AFTER_DISCOVERY = [
    "cont_date",
    "cont_doy",
    "cont_time",
    "fire_size",
    "fire_size_class",
    "fire_name",
    "fire_code",
    "complex_name",
    "ics_209_plus_incident_join_id",
    "ics_209_plus_complex_join_id",
    "mtbs_id",
    "mtbs_fire_name",
]
"""Known only after discovery (LEAK-10): containment, the final perimeter and its size class, the incident's name and
cost code (given as the fire grows, sometimes after its cause), the complex it was managed under, and the ids and names
of the large-fire datasets (ICS-209 reports and MTBS perimeters exist only for fires that grew large)."""

IDENTIFIERS = ["objectid", "fod_id", "fpa_id", "local_fire_report_id", "local_incident_id", "globalid"]
"""Record ids (CLEAN-3): the database's, the source system's and the local report numbers."""

COPIES = ["fire_year", "discovery_doy", "nwcg_reporting_unit_name", "source_reporting_unit_name", "county", "fips_name"]
"""Other forms of kept columns (CLEAN-5): the year and day of year of the discovery date, the names of the two unit
codes, and the county name and number of the five-digit FIPS code."""


class FpaFodWildfireCause1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What started this US wildfire, judged from what is known when it is discovered?",
        use_case=(
            "For example, when a wildfire is reported, the responsible agency's fire-prevention staff estimate its "
            "likely cause from the first report, to decide whether to send a fire investigator (arson, equipment, "
            "power lines, railroads) and, for fires whose cause is never found, to attribute a probable cause when "
            "planning prevention."
        ),
        row=(
            "One US wildfire of 1992-2024 from the federal, state and local fire reports the Forest Service compiles "
            "(7th edition, 2.66 million fires), with a named cause: 1,879,544 fires."
        ),
        predicted=(
            "The general cause the fire report finally records, one of 11 named causes of the national standard "
            "(lightning, debris burning, arson, equipment, and so on)."
        ),
        known=(
            "The day and, for most fires, the hour of discovery; the point of origin, state and county; the owner of "
            "the land there; and the agency, unit and reporting system that filed the report."
        ),
        split=(
            "Each of the calendar years 2022, 2023 and 2024 is a test window (44,931 to 49,610 fires); training is a "
            "random million of all earlier fires from 1992 on, as for a model refit once a year."
        ),
        changes=(
            "We leave out the undetermined fires (15.0% of 2021's fires, 28.8% of 2023's) and those coded 'Other "
            "causes', a recording habit of a few states since 2021 and 25-35% of the labelled test fires, so the score "
            "covers about half of each year's fires; we drop what is known only later (containment, final size, the "
            "fire's name, large-fire report ids)."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs are known at discovery and the test years follow the training years, but the actor is ours, "
            "the undetermined fires the use case serves most are left out, the source holds no lightning or weather "
            "inputs, and the test years come from one interagency system (InFORM) while 92-97% of the training fires "
            "come from older systems."
        ),
    )

    # Dataset
    unique_name = "fpa_fod_wildfire_cause_1m"
    version_of = "fpa_fod_wildfire_cause"
    version_comment = """
        Every train side holds 1,738,296 to 1,832,837 fires, above the 1M-row budget, so the dataset ships only as this version (definitions.md, Lennart 2026-10-21). We sample per test window (v2 split protocol): each window keeps all of its 44,931 to 49,610 fires (under 500k), and its train side is a random 1M of all earlier fires, drawn in one random order for all windows so the train sides overlap; the frame keeps only the 1,141,248 fires a split uses. The sample is random rather than the latest fires, so the train sides cover all 30 to 32 earlier years.
    """
    year = "2026"  # the edition we pin (PROV-9: a source that grows by editions); the first edition is of 2013
    domain = "environmental science & climate"
    source = "GOV Website"
    source_url = "https://doi.org/10.2737/RDS-2013-0009.7"
    license = "Public Domain"  # US Government data, "can be used without additional permissions or fees"
    data_tags = ("Spatial",)
    download_description = """
        The 7th edition (Short 2026, https://doi.org/10.2737/RDS-2013-0009.7) ships as sqlite, gpkg, gdb and accdb files in the USFS Research Data Archive, which answered HTTP 403 to this machine on 2026-11-08 and 2026-11-09. We read the same table from the USFS map service that serves it (layer Fire_FPA_FOD_7th_Fires, 2,661,383 records), every attribute without the geometry, in 1,331 pages of 2,000 records by OBJECTID; `_prepare_raw_files` joins the pages into fpa_fod_7th_fires.parquet and checks the record count. The service serves the current edition, so the count check fails once it moves to an 8th.

        mkdir -p local-data-warehouse/fpa_fod_wildfire_cause/pages && cd local-data-warehouse/fpa_fod_wildfire_cause
        L=https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_FireOccurrenceCurrentEdition_01/MapServer/0
        curl -sS -o layer_metadata.xml "$L/metadata"
        for start in $(seq 1 2000 2661383); do
          curl -sS -G "$L/query" --data-urlencode "where=objectid>=$start AND objectid<$((start + 2000))" --data-urlencode "outFields=*" --data-urlencode "returnGeometry=false" --data-urlencode "orderByFields=objectid" --data-urlencode "f=json" | gzip > "pages/page_$(printf %08d $start).json.gz"
        done
    """
    bibtex = """
        @misc{short2026fpafod,
          author = {Short, Karen C.},
          title = {Spatial wildfire occurrence data for the United States, 1992-2024 [{FPA\\_FOD\\_20260615}]},
          year = {2026},
          edition = {7th},
          publisher = {Forest Service Research Data Archive},
          address = {Fort Collins, CO},
          doi = {10.2737/RDS-2013-0009.7},
          howpublished = {\\url{https://doi.org/10.2737/RDS-2013-0009.7}},
        }
    """
    curation_comments = """
        We start with the 7th edition of the Fire Program Analysis fire-occurrence database (FPA FOD, Short 2026; 2,661,383 fires of 1992-2024), every attribute of the USFS map-service layer that serves it.

        - The prediction point is the discovery of the fire: the model knows what the first fire report holds (date and hour, the point of origin, state, county and land owner, and the agency, unit and system that report it). The target is the general cause the closed report records, in the NWCG cause standard of August 2020, to which Short mapped the older systems' codes.
        - We leave out the 689,382 fires whose cause is "Missing data/not specified/undetermined" (25.9%): the pool the use case would score, not a class.
        - We leave out the 91,803 fires coded "Other causes", the standard's residual ("any wildfire that does not fit into the identified general or specific cause", BLM glossary). Until 2020 it holds under 1% of each year's fires; from 2021, when the interagency systems (IRWIN, then InFORM) replace the federal and state ones, it holds 18-28%, most of it in a few states (share of each state's fires in 2021-2024: Colorado 26-69%, Michigan 49-95%, Indiana 49-70%, Kansas 77-78% in 2021-2022 and 0-2% after): a recording convention of those states' reports, read off the state and the year (decision tables; LEAK-13). LEAK-25 as amended on 2026-11-02 (noaa_storm_events_damage) keeps such a class only when it is not read off the recording context, and that fails here (next sentence). Kept as a class, it would be 25-35% of the labelled fires of each test window, against 0.6% of the training years before 2021. On the three test years, an untuned LightGBM on the state and the date alone ranks the class with ROC AUC 0.77-0.80, about as well as on every input (0.78-0.82; one seed per year).
        - We drop the 654 named fires whose record comes only from the ICS-209 situation reports or the MTBS perimeters (source systems IA-ICS209, IA-MTBS): such a record exists because the fire grew large, and its cause is named for 652 lightning fires and 2 power-line fires out of 4,258 (LEAK-10, LEAK-13).
        - We drop two other encodings of the cause (LEAK-10): NWCG_CAUSE_CLASSIFICATION (Human or Natural, "Natural" exactly where the target is) and NWCG_CAUSE_AGE_CATEGORY ("Minor" for every fire of "Misuse of fire by a minor").
        - We drop what is known only after discovery (LEAK-10): the containment date, day and time, the final size and its class, the fire's name (it can spell the cause: 2,287 of the 2,512 names with "LIGHTNING" are Natural), the fire code for cost tracking, the complex, and the ICS-209 and MTBS ids and name, which exist only for fires that grew large.
        - We drop the record ids (FOD_ID, FPA_ID, OBJECTID, GLOBALID, the local report and incident numbers) and the copies of kept columns: the fire year and day of year (the date), the two unit names (their codes), and the county name and number (the five-digit FIPS code).
        - The discovery time, local "HHMM", becomes `discovery_hour`, the hour with the minutes as a fraction. It is missing for 31% of the records, by reporting system and state (federal systems 0.3%, nonfederal 43%, interagency 22%: IRWIN 68%, InFORM 10%, where Texas reports 63% without a time and most states none), and falls with the system change (30-60% in the 1990s, 4-16% since 2020). In the test years it differs by cause, from 2.8% (Natural) to 21.5% (Smoking) and 0% for firearms (human against natural ROC AUC 0.545, 0.592 within state). Its missingness is no shortcut to the cause: with the hour replaced by a missing-value flag, untuned LightGBM scores no better than without the column (log loss 1.456 against 1.438 in 2024, 1.478 against 1.428 in 2022, 1.512 against 1.502 in 2023).
        - The land owner "MISSING/NOT SPECIFIED" is set missing (CLEAN-10): 1,077,672 records, 60% of the nonfederal records and 1.4% of the federal ones, 37-64% of each year's fires before 2021 and about 0% after (at most 0.1% for any cause in the test years); two "Private" become "PRIVATE".
        - The point is the fire's point of origin (NAD 83), "at least as precise as a Public Land Survey System section"; its precision follows the reporting system (Florida's records hold 2 decimals), not the cause within a system (the number format alone: macro ROC AUC 0.509). The county is the five-digit FIPS code from the report (missing for 60% of federal records). In federal records its missingness differs by cause, from 13% (firearms) to 90% (misuse by a minor), 79% for arson and debris burning against 48-52% for natural, power-line and recreation fires, most likely by agency and region; in the test years it is missing for 0-7% of the fires and for no cause more than another. Kept as published, no missing-value flag.
        - The reporting fields stay (system type, system, NWCG agency and unit, source unit): the report is filed by them, so they are known at discovery (USE-6). They carry each system's recording conventions (the older systems of Georgia, Mississippi and South Carolina never code power lines, fireworks or firearms), and the test years are one system (InFORM): untuned LightGBM scores better without them in all three test years (log loss 1.403 against 1.432 in 2024, 1.490 against 1.615 in 2023, 1.378 against 1.433 in 2022; one seed, 300k training fires), but a logistic regression scores worse without them (2022: 1.4151 with all fields, 1.4491 without the two system fields, 1.4501 without all five; 200k training fires), so the untuned model's gain is its instability, not a proxy (open to the curator).
        - Note: `source_reporting_unit` is the source system's own unit code; 20 codes (111,013 records) stand for different units in different systems (numeric fire-department codes of Missouri and Colorado), which the state and the NWCG unit tell apart. Kept as published.
        - Note: the Idaho National Guard's training range (unit USIDIDNG) reports 710 fires since 2020, all "Firearms and explosives use", 561 of the 1,355 of that class in the test years: a property of the place, known at discovery, kept.
        - Note: the class shares drift (power lines and equipment rise since 2019, arson falls). The fires without a determined cause or with "Other causes" are 49.1%, 48.4% and 46.7% of the 2022, 2023 and 2024 records, no rise at the end that would mark causes still being investigated (LEAK-24). The undetermined share alone rises, 15.0% (2021), 22.2%, 28.8%, 28.7% (2024), as states such as Kansas stop coding "Other causes"; within 2024 it shows no fall-off at the end (by quarter 23.5%, 30.8%, 31.4%, 28.3%, Q4 below Q3), so no censoring signature. A second edition to compare against was not obtained.
        - Note: 22,320 kept fires (1.2%) share every input with another fire, mostly separate fires at one survey-section point on one day (a lightning storm, fires along a railroad), with different names; 597 such groups hold two causes. Kept (LEAK-18): copies share their date, so they never fall on both sides of a split.
        - Note: counts computed over all rows, test rows included, help a little: fires at the same point (+0.016 to +0.021 log loss) and fires of the same unit on the same day (+0.002 to +0.013), near the noise of 0.006-0.011 (task gamer, LightGBM). A participant uses past-only counts, and same-day counts only of the fires reported so far.
    """

    # Task
    target = "nwcg_general_cause"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "No source scores the cause with one metric. The FPA FOD papers (Short 2014, ESSD 6:1-27; Pourmohamad et "
            "al. 2024, ESSD 16:3045) define no prediction task; the Kaggle mirror of the 3rd edition "
            "(rtatman/188-million-us-wildfires) asks the question without a metric. Pourmohamad et al. 2025 (Earth's "
            "Future, doi:10.1029/2024EF005187, abstract and model record read) infer 12 causes in the western US and "
            "report several accuracies (overall above 70%, human against natural 93%, among human causes 55%), and a "
            "2026 BIO Web of Conferences paper reports cross-validated accuracy on four broad classes (abstract "
            "only): accuracies without a threshold or costs, several side by side (MET-5, MET-6). Fallback: "
            "multiclass log loss."
        )
    )

    splits_comment = """
        Each of the calendar years 2024, 2023 and 2022 (newest first) is a test window, and the train side is a random 1M of the fires discovered before it, from 1992 on, as for a model refit once a year after the season. A year covers every season, so no window is one atypical fire season. No gap: the cause is recorded in the fire report, closed after containment, and 10 to 15 training fires per window (0.001%) were contained only after the window began; when each cause was determined is not recorded. The reporting systems changed in 2020-2021 (curation notes): the test years are 99.9% interagency records (InFORM), the training sides 3% (2022) to 8% (2024). Recent history scores better: untuned LightGBM (300k sampled training fires) gives log loss 1.363 / 1.461 / 1.353 (2024 / 2023 / 2022) on the full history and 1.302 / 1.378 / 1.339 on the fires since 2016, and a regularized LightGBM gains 0.055 on average from the last 10 years only; the date is a feature and the recent years are on the train side, so a participant may weight them. A history from 2020 only would leave the 2022 window 88,503 training fires of its 229,751 (38.5%), and a later start (2005, 2010, 2015) is open to the curator.
    """
    temporal = Temporal(on="discovery_date", splits=TemporalSplits(window=1, unit="years", n_windows=3))
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (PREPARED,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        """Join the gzipped JSON pages of the map-service layer into one parquet file, every attribute as served."""
        import gzip
        import json

        frames = []
        for page in sorted((raw_dir / "pages").glob("page_*.json.gz")):
            body = json.loads(gzip.decompress(page.read_bytes()))
            frames.append(pd.DataFrame([f["attributes"] for f in body["features"]]))
        df = pd.concat(frames, ignore_index=True).sort_values("objectid", kind="stable").reset_index(drop=True)
        assert len(df) == N_RECORDS, len(df)
        assert df["objectid"].is_unique
        for col in ("discovery_date", "cont_date"):
            # Epoch milliseconds at 00:00 UTC of the date the record gives.
            df[col] = pd.to_datetime(df[col], unit="ms")
        df.to_parquet(raw_dir / PREPARED, index=False)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / PREPARED)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. Keep the fires with a determined cause; the undetermined ones are the pool the use case would score.
        df = df[~df[self.target].isin([UNDETERMINED, OTHER])]
        # 2. Records drawn only from the large-fire datasets have no discovery report, and carry a cause only when it
        #    was lightning (LEAK-10, LEAK-13).
        df = df[~df["source_system"].isin(LARGE_FIRE_SOURCES)]
        # 3. Drop the other encodings of the cause, the values known only after discovery, the ids and the copies.
        df = drop_columns(df, TARGET_ENCODINGS + AFTER_DISCOVERY + IDENTIFIERS + COPIES)
        # 4. The discovery time, local "HHMM" (every value is four digits, hours 00-23, minutes 00-59), as the hour of
        #    the day with the minutes as a fraction: a position on the day's cycle, a number (CLEAN-14).
        hhmm = df["discovery_time"]
        assert hhmm.dropna().str.fullmatch(r"([01]\d|2[0-3])[0-5]\d").all()
        df["discovery_hour"] = pd.to_numeric(hhmm.str.slice(0, 2)) + pd.to_numeric(hhmm.str.slice(2, 4)) / 60
        df = df.drop(columns=["discovery_time"])
        # 5. The owner not recorded is missing (CLEAN-10); two rows spell PRIVATE in lower case.
        df["owner_descr"] = df["owner_descr"].replace({OWNER_MISSING: np.nan, "Private": "PRIVATE"})
        return df

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        cause, year = raw[self.target], raw["fire_year"]
        by_year = pd.DataFrame(
            {
                "fires": year.value_counts().sort_index(kind="stable"),
                "undetermined": (cause == UNDETERMINED).groupby(year).mean().round(3),
                "Other causes": (cause == OTHER).groupby(year).mean().round(3),
                "interagency system (IRWIN, InFORM)": (raw["source_system_type"] == "INTERAGCY").groupby(year).mean(),
            }
        ).loc[lambda t: t.index >= 2012]
        by_year["interagency system (IRWIN, InFORM)"] = by_year["interagency system (IRWIN, InFORM)"].round(3)
        recent = raw[year >= 2021]
        by_state = (
            pd.DataFrame(
                {
                    "fires 2021-2024": recent.groupby("state").size(),
                    "Other causes": (recent[self.target] == OTHER).groupby(recent["state"]).sum(),
                }
            )
            .assign(share=lambda t: (t["Other causes"] / t["fires 2021-2024"]).round(3))
            .sort_values("Other causes", ascending=False, kind="stable")
            .head(8)
        )
        return [
            Decision(
                "'Other causes' is left out with the undetermined fires",
                "From 2021, when the records come from the interagency systems, 'Other causes' jumps from under 1% of "
                "the fires to 18-28%, concentrated in a few states whose reports it absorbs (Colorado, Michigan, "
                "Indiana, Kansas): a recording convention, not a cause (LEAK-13, LEAK-25).",
                by_year,
            ),
            Decision(
                "The states behind 'Other causes' since 2021",
                "A handful of states account for most of the class in 2021-2024, at shares no earlier year shows.",
                by_state,
            ),
        ]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "source_system_type",
                "source_system",
                "nwcg_reporting_agency",
                "nwcg_reporting_unit_id",
                "source_reporting_unit",
                "owner_descr",
                "state",
                "fips_code",
            ],
            datetime=["discovery_date"],
        )
