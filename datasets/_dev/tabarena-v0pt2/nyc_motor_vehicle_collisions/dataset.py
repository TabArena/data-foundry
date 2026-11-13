"""Whether a police-reported New York City crash injures or kills anyone, from its time, place and vehicles."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
)

# The eight injury and death counts: the target and its parts (LEAK-10).
OUTCOME_COUNTS = (
    "number_of_persons_injured",
    "number_of_persons_killed",
    "number_of_pedestrians_injured",
    "number_of_pedestrians_killed",
    "number_of_cyclist_injured",
    "number_of_cyclist_killed",
    "number_of_motorist_injured",
    "number_of_motorist_killed",
)
FACTORS = tuple(f"contributing_factor_vehicle_{i}" for i in range(1, 6))
VEHICLE_TYPES = (
    "vehicle_type_code1",
    "vehicle_type_code2",
    "vehicle_type_code_3",
    "vehicle_type_code_4",
    "vehicle_type_code_5",
)
STREETS = ("on_street_name", "cross_street_name", "off_street_name")
# The crash id and the portal's row metadata, all set or reset by the reload of 2026-10-29.
SOURCE_IDS = (":id", ":created_at", ":updated_at", "collision_id")
# NYPD stopped taking reports of crashes with property damage only on Monday 2020-04-06.
ERA_START = pd.Timestamp("2020-04-06")
# The snapshot's crashes run to 2026-11-03; November 2026 is not a complete month.
DATA_END = pd.Timestamp("2026-11-01")
# NYPD's vehicle type codes change in the week of 2026-05-04 ("Sedan" becomes "4 dr sedan", "Bike" "Bicyclist").
VEHICLE_CODE_CHANGE = pd.Timestamp("2026-05-04")

# The vehicle types of both coding eras on one scale (CLEAN-21): the first pattern that matches the upper-cased,
# trimmed value decides; anything else is "other". The data dictionary names the categories ATV, bicycle, car/suv,
# ebike, escooter, truck/bus, motorcycle and other; we keep taxi, bus, ambulance or fire and moped apart, as both
# eras code them, and put trucks, vans and pickups together, as the two lists draw the line between them differently.
VEHICLE_CATEGORIES = (
    (r"^UNKNOWN CAR$", "car"),
    (r"^UNKNOWN TRUCK$", "truck or van"),
    (r"^(?:UNK|UNKN|UNKNOWN|UNKNOWN VEHICLE|UNKOWN)$", "unknown"),
    # "Utility" of the new list is not checked against a body type, so it is masked, not guessed (force_2020).
    (r"^UTILITY$", "other"),
    (r"E[- ]?BIKE", "e-bike"),
    (r"E[- ]?SCOOTER|ELECTRIC S|STANDING SCOOTER|^SCOOTER$", "e-scooter"),
    (r"MOTOR ?SCOO|MOTORCYCLE|MOTORBIKE|DIRT ?BIKE|MINIBIKE|MINICYCLE", "motorcycle"),
    (r"MOPED", "moped"),
    (r"^BIKE$|BICYC|PEDICAB", "bicycle"),
    (r"AMBUL|^AMB|FIRE|FDNY|^EMS", "ambulance or fire"),
    (r"TAXI|^CAB$|LIMO|\bLIVERY\b", "taxi or limousine"),
    (r"BUS|OMNIBUS", "bus"),
    (
        r"REFRIGERAT|TRUCK|TRACTOR|TRAILER|DUMP|FLAT ?BED|FLAT RACK|GARBAGE|REFUSE|SANITATION|TOW|WRECKER|TANK|MIXER"
        r"|CHASSIS|DELIVERY|CARRY ?ALL|STAKE|ARMORED|BEVERAGE|SNOW ?PLOW|LIFT BOOM|MULTI-WHEELED|OPEN BODY"
        r"|^COM$|COMMERCIAL|USPS|BULK AGRICULTURE|PALLET|CONSTRUCTION|SWEEP|LUNCH WAGON|^DELV$"
        r"|PICK|^PK$|VAN|SPRINTER",
        "truck or van",
    ),
    (
        r"SEDAN|^2 ?DR|^4 ?DR|3-DOOR|CONVERTIBLE|STATION WAGON|SPORT UTILITY|^SUV$|^SUBN$|POLICE VEHICLE"
        r"|^UTIL$|SUBURBAN|PASSENGER|HATCH|COUPE",
        "car",
    ),
)
# Street names, written both ways over the years ("EAST 57 STREET", "E 57 ST"): the USPS abbreviations (CLEAN-21).
STREET_WORDS = {
    "STREET": "ST",
    "AVENUE": "AVE",
    "AV": "AVE",
    "ROAD": "RD",
    "BOULEVARD": "BLVD",
    "PLACE": "PL",
    "PARKWAY": "PKWY",
    "EXPRESSWAY": "EXPY",
    "DRIVE": "DR",
    "LANE": "LN",
    "COURT": "CT",
    "HIGHWAY": "HWY",
    "TERRACE": "TER",
    "BRIDGE": "BRG",
    "EAST": "E",
    "WEST": "W",
    "NORTH": "N",
    "SOUTH": "S",
}


def vehicle_category(values: pd.Series) -> pd.Series:
    """Map raw vehicle type codes of both coding eras onto one set of categories (missing stays missing)."""
    text = values.str.strip().str.upper()
    out = pd.Series(pd.NA, index=values.index, dtype="object")
    left = text.notna() & text.ne("")
    for pattern, category in VEHICLE_CATEGORIES:
        hit = left & text.str.contains(pattern, regex=True, na=False)
        out[hit] = category
        left &= ~hit
    out[left] = "other"
    return out


def normalise_street(values: pd.Series) -> pd.Series:
    """Upper case, single spaces, USPS abbreviations for street words; empty names become missing."""
    text = values.str.upper().str.replace(r"\s+", " ", regex=True).str.strip()
    words = re.compile(r"\b(" + "|".join(STREET_WORDS) + r")\b")
    text = text.str.replace(words, lambda m: STREET_WORDS[m.group(1)], regex=True)
    return text.mask(text.eq(""))


class NycMotorVehicleCollisions(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Was anyone injured or killed in this police-reported New York City crash?",
        use_case=(
            "For example, a city road-safety analyst estimates, for each police-reported crash, the chance that "
            "someone was hurt from its time, place and vehicles, to estimate expected injury crashes at each site "
            "and rank sites for safety work."
        ),
        row=(
            "One crash the NYPD reported between 6 April 2020, when police stopped taking reports of crashes with "
            "property damage only, and October 2026."
        ),
        predicted=(
            "Whether the police report counts at least one pedestrian, cyclist or vehicle occupant injured or killed "
            "(about a third of crashes in 2020, almost half in late 2026); reports can be amended later."
        ),
        known=(
            "The crash's date and hour, borough, ZIP code, coordinates, street names or address, and the kind of "
            "each of up to five vehicles involved."
        ),
        split=(
            "Three later three-month crash cohorts (February to October 2026) are each tested against all crashes "
            "from April 2020 up to one month before the cohort."
        ),
        changes=(
            "We keep crashes from 6 April 2020, drop the injury counts, the officers' contributing factors and the "
            "ids, floor the crash time to the hour, and put the vehicle types and street names of two coding eras "
            "on one scale."
        ),
        fit="approximate",
        fit_reason=(
            "The police count stands in for the injuries the analyst counts; crashes without injury are only those "
            "police still reported. Contributing factors are left out: officers fill them differently for injury "
            "crashes. Vehicle codes changed in May 2026 and are merged into coarser kinds. Kept: a blank vehicle "
            "type (1.5% of crashes, 81% with injury), which marks pedestrian and hit-and-run crashes."
        ),
    )

    unique_name = "nyc_motor_vehicle_collisions"
    year = "2026"  # the snapshot we pin; the register grows daily (PROV-9)
    domain = "social science"
    source = "GOV Website"
    source_url = "https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95"
    license = "See Terms of Use (NYC Open Data)"
    data_tags = ("Spatial",)
    download_description = r"""
        The crash table (dataset h9gi-nx95) through the portal's SoQL API, one CSV per crash month from January 2019
        (one year before the era, kept to show the 2020 break) to November 2026, into
        local-data-warehouse/nyc_motor_vehicle_collisions/crashes/crashes_<YYYY-MM>.csv:

        COLS=':id,:created_at,:updated_at,collision_id,crash_date,crash_time,borough,zip_code,latitude,longitude,on_street_name,cross_street_name,off_street_name,number_of_persons_injured,number_of_persons_killed,number_of_pedestrians_injured,number_of_pedestrians_killed,number_of_cyclist_injured,number_of_cyclist_killed,number_of_motorist_injured,number_of_motorist_killed,contributing_factor_vehicle_1,contributing_factor_vehicle_2,contributing_factor_vehicle_3,contributing_factor_vehicle_4,contributing_factor_vehicle_5,vehicle_type_code1,vehicle_type_code2,vehicle_type_code_3,vehicle_type_code_4,vehicle_type_code_5'
        mkdir -p local-data-warehouse/nyc_motor_vehicle_collisions/crashes
        for start in $(seq 0 94 | xargs -I{} date -d "2019-01-01 +{} month" +%Y-%m-%d); do
          end=$(date -d "$start +1 month" +%Y-%m-%d)
          curl -s -G "https://data.cityofnewyork.us/resource/h9gi-nx95.csv" --data-urlencode "\$select=$COLS" \
            --data-urlencode "\$where=crash_date >= '${start}T00:00:00' AND crash_date < '${end}T00:00:00'" \
            --data-urlencode '$order=collision_id' --data-urlencode '$limit=200000' \
            -o local-data-warehouse/nyc_motor_vehicle_collisions/crashes/crashes_${start:0:7}.csv
        done

        The portal often answers "Service unavailable": repeat a month until its file starts with the header ":id".
        The pinned snapshot was downloaded on 2026-11-09 (95 files, 883,059 rows, crashes to 2026-11-03, rows last
        updated 2026-11-06; sha256 of the files concatenated in name order
        0379bae2951a6a9684454c7675e601cb6aab8e6a28a773f66307c5890280e845). The portal amends and adds rows daily,
        and reloaded the whole table on 2026-10-29, so a later download need not reproduce these bytes.
    """
    bibtex = """
        @misc{nypd_motor_vehicle_collisions,
          author = {{New York City Police Department}},
          title = {Motor Vehicle Collisions - Crashes},
          year = {2026},
          howpublished = {\\url{https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95}},
          note = {NYC Open Data, dataset h9gi-nx95}
        }
    """
    curation_comments = """
        We start with NYPD's crash table on NYC Open Data (h9gi-nx95), downloaded by crash month through the SoQL API on 2026-11-09, January 2019 to November 2026.

        - Prediction point: a police-reported crash once its report is filed, before anyone reads its injury counts; a city road-safety analyst estimates from the crash's time, place and vehicles the chance that someone was hurt, to rank sites by expected injury crashes (the actor of chicago_traffic_crashes, Lennart, 2026-11-05). The source names no actor; the portal points to Vision Zero analysis.
        - History: crashes from Monday 2020-04-06, when NYPD stopped taking reports of crashes with property damage only (NYPD press release of 2020-04-03: such collisions "are not required to be reported to the police"), to October 2026 (SPLIT-6, SPLIT-20). From January 2019 to March 2020 19-23% of crashes had an injury, 25-36% in the months after the date; the crashes without injury after it are the ones police still attended (a person who feels unsafe, an owner who cannot be found). The first weeks are also the COVID-19 lockdown (826-1,579 crashes a week in April and May 2020 against 3,000-3,800 in February and early March). November 2026 is cut, as the snapshot ends on 2026-11-03.
        - The target is "Yes" when any of the eight counts (persons, pedestrians, cyclists, motorists, each injured or killed) is above 0: 47.6% "Yes" in the newest window, against 33.7% in 2020 (from April). The counts disagree in 14,370 of the 883,059 downloaded rows (persons injured is not the sum of its parts), so the target reads all eight; all eight leave as the target and its parts (LEAK-10). One row has no persons-injured count; its other counts decide.
        - The five contributing factors are dropped (LEAK-10 through LEAK-38's measured clause; chicago_traffic_crashes dropped its contributory causes as investigation information). Officers leave them unspecified far more often when nobody is hurt: in single-vehicle crashes factor 1 is "Unspecified" or "Does Not Apply" for 52.6% without injury against 29.9% with one (the decision table). On the three windows (untuned LightGBM, 2026-11-09) they lift ROC AUC from 0.737 to 0.805; flags saying only whether each factor is blank, unspecified or named reach 0.796. Most of that gain is not the officer's judgement but the number of parties: the count of filled factor slots alone reaches 0.783, 78% of the gain. A party count from the Vehicles table could come back in a later rebuild. Their coding also changes in April 2025: "Unspecified" gives way to "Does Not Apply", 60-64% of factor 1 from 2025Q3.
        - The vehicle types are put on one scale (CLEAN-21): from the week of 2026-05-04 NYPD writes them in another code list ("Sedan" becomes "4 dr sedan", "Bike" "Bicyclist", "Bus" "Bus (Omnibus)"; 48 and 44 distinct values in 2026Q3 and Q4 against 137 to 187 a quarter before). `vehicle_category` maps both lists and the free-text long tail onto 12 kinds (car, taxi or limousine, truck or van (pickups included), bus, ambulance or fire, motorcycle, moped, bicycle, e-bike, e-scooter, unknown, other), from the categories the data dictionary names, with taxis, buses, emergency vehicles and mopeds kept apart as both lists code them. "Police Vehicle" (new list only) counts as a car; "Utility" (989 vehicles of the new list, unchecked against a body type) goes to other, masked rather than guessed (force_2020). The taxi pattern matches LIVERY only as a word, so delivery vehicles stay trucks. Trucks, vans and pickups form one kind because the lists draw the line between them differently (box trucks are "Box Truck" in the old list and mostly "Van" in the new): together 8.5% of the vehicles of May-October 2025 and 9.8% of May-October 2026, while the codes the old list calls vans and pickups abbreviated "PK" are 1.0% against 3.0%. With the raw codes the window after the change scores ROC AUC 0.657 against 0.743 harmonised (0.708 against 0.738 over the three windows; untuned LightGBM, re-measured 2026-11-09 after the taxi and Utility fixes). "Unknown" is a vehicle of unknown kind. A blank slot usually means no further vehicle, but not always: 13.4% of crashes have a contributing factor in a slot whose vehicle type is blank.
        - Street names are upper-cased, spaces collapsed and street words written as USPS abbreviations ("EAST 57 STREET" and "E 57 ST" both become "E 57 ST"), as the portal writes them both ways. `off_street_name` holds an address (house number and street) when the crash is not at an intersection; it stays as text. The data dictionary's descriptions of `cross_street_name` and `off_street_name` are swapped on the portal page; the values follow the dictionary file.
        - The crash time is floored to the hour (LEAK-13), in `_clean` before the framework orders the rows by it, as chicago_traffic_crashes: 19.9% of crashes without injury are written at minute :00 against 12.3% with one, and the source minute lifts ROC AUC by 0.011 (0.737 to 0.748). Date and hour form one datetime.
        - Potential leak, kept on purpose (LEAK-6, a small optimism with a note): 1.5% of crashes (9,378) have no vehicle type in any slot, and 80.6% of them have an injury (40.0% overall). The blank marks a pedestrian or hit-and-run crash, a scene fact known when the report is filed: it is set in 13.7% of crashes where only pedestrians are hurt, against 0.19% where only motorists are and 0.48% of crashes without injury. In 39 of 40 such crashes sampled from 2025-2026 the Vehicles table holds a vehicle row with its type and make blank but often its pre-crash action, so a vehicle was there and its type was not entered. The blank alone scores ROC AUC 0.513 (leak probe 3); removing its signal costs 0.0005 ROC AUC. Kept as missing; a Person-table check of uninjured pedestrians in these crashes would confirm the mechanism.
        - Coordinates of 0 (7,273 rows in the era, the only values outside the city) are made missing: all of them came with the portal's backfill of 2026-11-06 (7,634 of its 7,855 rows), not crashes that failed to geocode. Borough and ZIP code stay as published, missing where the source left them: the borough is blank for 30-35% of crashes until 2024Q3 and for about 3% from 2025Q2 on, a geocoding change of 2025; a model sees that drift.
        - Selection: the MV-104AN report is required when someone is injured or killed or the damage is at least $1000, so the model learns the chance of an injury among reported crashes, not among all crashes; the rising injured share fits fewer reports without injury as much as more severe crashes.
        - Where the crash is written: crashes with only an address (`off_street_name`, no intersection; about 32% of test rows) are 30% injured, against 53% at an intersection. Both forms are on the report when it is filed, so this is signal the analyst has; whether it is a scene fact (driveways, parking lots) or how the report was taken, the table cannot tell.
        - Riders of e-scooters, e-bikes and mopeds are counted in persons injured but in neither the cyclist nor the motorist count (13,908 crashes from 2021 with persons injured and every part 0); the target reads all eight counts, so they count as injured.
        - Exact source copies (every field equal but the ids and the portal's row metadata) are removed, keeping the first: 229 rows. Crashes that coincide only after the drops and the hour floor stay (432 rows; 152 share their inputs with a row of the other label): distinct crash ids, and coarse inputs.
        - Dropped as identifiers or portal metadata: `collision_id` (a hash since the reload), `:id`, `:created_at` and `:updated_at` (all set by the reload of 2026-10-29). `location` repeats the coordinates and is not downloaded.
        - Not downloaded: the Vehicles (bm4k-52h4) and Person (f55k-p6yu) tables. Person holds each person's injury (the target); Vehicles adds per-vehicle details recorded on the same report (pre-crash action, damage, driver), starts in 2016 and would need its own fill checks; a later variant could add it.
        - The snapshot is the portal's reload of 2026-10-29 plus daily updates to 2026-11-06; the data is "preliminary and subject to change when the MV-104AN forms are amended". The reload set every row's update time, so how late amendments arrive cannot be measured; when new rows arrive can (the one-month gap in `splits_comment`).
        - Same task, another source (principles.md, Tensions; not a shared source, PROV-4 holds): chicago_traffic_crashes predicts the most severe of five police injury levels (KABCO) of a Chicago crash from 15 crash and road facts, from September 2017; this predicts any injury or death in a New York crash from 13 inputs (time, place, vehicle kinds), from April 2020, where crashes with property damage only enter only when police still attended them. Both enter (Lennart, 2026-11-08: neither is better data).
    """

    target = "anyone_injured_or_killed"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "No metric found: the NYC Open Data page and data dictionary, NYPD's collision pages and the NYPD "
            "MV-104AN form define a crash register, not a prediction task; no competition or paper defines one on "
            "this table (Kaggle notebooks only). RaX-Crash (arXiv 2512.07848) predicts severity on this table but reports accuracy, kappa, macro F1 and fatal recall and names no single criterion. ROC AUC on the binary any-injury target."
        )
    )
    temporal = Temporal(on="crash_datetime", splits=TemporalSplits(window=3, unit="months", n_windows=3, gap=1))
    splits_comment = """
        Three consecutive three-month windows of crash time, newest first: August-October, May-July and February-April 2026, each tested against all crashes from 2020-04-06 to one month before the window (an expanding train side, 560,000-603,000 crashes; no side is sampled, so no `_1m` version is needed). A quarterly refit, as chicago_traffic_crashes.
        The one-month gap rests on when rows arrive (SPLIT-10): the data is "preliminary and subject to change when the MV-104AN forms are amended", and rows added after the reload of 2026-10-29 arrive a median 3-5 days after the crash, the 99th percentile 22-48 days, so a refit at a window's start misses part of the last weeks and one month covers 99% of them. Gap 0 against 1 changes ROC AUC by 0.0005. Label amendments cannot be measured, as the reload reset every row's update time. A separate backfill on 2026-11-06 added 7,855 crashes from 2019 to 2026 (2.7% of 2026, 36% injured against 45% for the year) months to years late, beyond any gap.
        The windows fall after two coding changes: the contributing factors in April 2025 (dropped) and the vehicle types in May 2026 (harmonised). The May-July window starts with the new vehicle codes.
        Drift (SPLIT-20): the share of crashes with an injury rises from 30-36% (2020-2021) to 42-48% (2025-2026, by half-year), with a dip each January and February (to 35.5% in February 2026); the borough is filled for far more crashes from 2025.
        Places recur over time (a street, an intersection); this is not unseen-location evaluation.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        paths = sorted((raw_dir / "crashes").glob("crashes_*.csv"))
        return pd.concat([pd.read_csv(p, dtype="string") for p in paths], ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        day = pd.to_datetime(df["crash_date"], format="%Y-%m-%dT%H:%M:%S.%f")
        # 1. One era: from the day NYPD stopped taking property-damage-only reports, to the last complete month.
        df = df.loc[day.ge(ERA_START) & day.lt(DATA_END)].copy()
        # 2. Exact source copies: every field equal but the ids and the portal's row metadata; the first stays.
        df = df.drop_duplicates(subset=[c for c in df.columns if c not in SOURCE_IDS], keep="first")
        day = day.loc[df.index]
        # 3. The target: anyone injured or killed, by any of the eight counts (then dropped with them, LEAK-10).
        counts = df[list(OUTCOME_COUNTS)].apply(pd.to_numeric, errors="raise")
        assert counts.notna().any(axis=1).all()
        df[self.target] = counts.fillna(0).gt(0).any(axis=1).map({False: "No", True: "Yes"})
        # 4. The crash time, floored to the hour before the framework orders the rows by it (LEAK-13).
        time = pd.to_timedelta(df["crash_time"].str.strip() + ":00")
        df["crash_datetime"] = (day + time).dt.floor("h")
        # 5. Coordinates: 0 marks the rows of the backfill of 2026-11-06.
        for c in ("latitude", "longitude"):
            df[c] = pd.to_numeric(df[c], errors="raise").astype("float64")
            df.loc[df[c].eq(0), c] = float("nan")
        # 6. One scale for the vehicle types and the street names across the coding changes (CLEAN-21).
        for c in VEHICLE_TYPES:
            df[c] = vehicle_category(df[c])
        for c in STREETS:
            df[c] = normalise_street(df[c])
        df["borough"] = df["borough"].str.strip().str.upper()
        df["zip_code"] = df["zip_code"].str.strip()
        keep = ["crash_datetime", "borough", "zip_code", "latitude", "longitude", *STREETS, *VEHICLE_TYPES]
        return df[[*keep, self.target]]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["borough", "zip_code", *VEHICLE_TYPES],
            string=list(STREETS),
            datetime=["crash_datetime"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        day = pd.to_datetime(raw["crash_date"], format="%Y-%m-%dT%H:%M:%S.%f")
        hurt = raw[list(OUTCOME_COUNTS)].apply(pd.to_numeric).fillna(0).gt(0).any(axis=1)
        half = day.dt.year.astype(str) + "H" + (day.dt.month.gt(6) + 1).astype(str)
        half = half.where(~day.between("2020-01-01", "2020-04-05"), "2020-01-01 to 04-05")
        half = half.where(~day.between("2020-04-06", "2020-06-30"), "2020-04-06 to 06-30")
        era = pd.DataFrame({"crashes": hurt.groupby(half).size(), "with injury or death": hurt.groupby(half).sum()})
        era["share with injury"] = (era["with injury or death"] / era["crashes"]).round(3)

        # The same season in both code lists: May to October of 2025 (old list) and 2026 (new list).
        season = {
            "old list, 2025-05-04 to 10-31": day.ge("2025-05-04") & day.lt("2025-11-01"),
            "new list, 2026-05-04 to 10-31": day.ge(VEHICLE_CODE_CHANGE) & day.lt(DATA_END),
        }
        slots = {name: pd.concat([raw.loc[mask, c] for c in VEHICLE_TYPES]).dropna() for name, mask in season.items()}
        kinds = pd.DataFrame({name: vehicle_category(s).value_counts(normalize=True) for name, s in slots.items()})
        kinds = kinds.fillna(0).round(4)
        vehicle_new = slots["new list, 2026-05-04 to 10-31"].str.strip().value_counts()

        known = day.ge(ERA_START) & day.lt(DATA_END)
        n_vehicles = raw.loc[known, list(VEHICLE_TYPES)].notna().sum(axis=1).clip(upper=3)
        unspecified = raw.loc[known, "contributing_factor_vehicle_1"].isin(["Unspecified", "Does Not Apply"])
        factor = (
            pd.DataFrame(
                {"vehicles": n_vehicles, "injury": hurt[known].map({False: "No", True: "Yes"}), "u": unspecified}
            )
            .groupby(["vehicles", "injury"])["u"]
            .mean()
            .unstack("injury")
            .round(3)
        )
        factor.index = factor.index.map({0: "0", 1: "1", 2: "2", 3: "3 or more"})
        factor.columns = [f"factor 1 unspecified, injury {c}" for c in factor.columns]
        return [
            Decision(
                title="Keep crashes from 2020-04-06",
                why=(
                    "From that Monday NYPD no longer took reports of crashes with property damage only, so the "
                    "crashes without injury are another population after it (SPLIT-6, SPLIT-20)."
                ),
                evidence=era,
            ),
            Decision(
                title="Put the vehicle types of both code lists on one scale",
                why=(
                    "NYPD switched to another list of vehicle codes in the week of 2026-05-04; mapped to kinds, the "
                    "vehicles of the same season a year apart keep their shares (CLEAN-21). The new list's top codes: "
                    f"{', '.join(vehicle_new.head(6).index)}."
                ),
                evidence=kinds,
            ),
            Decision(
                title="Drop the contributing factors",
                why=(
                    "Officers leave factor 1 unspecified more often when nobody is hurt, within the same number of "
                    "vehicles (LEAK-38's measured clause, so LEAK-10); 'Does Not Apply' replaces 'Unspecified' from "
                    "April 2025 and both count here."
                ),
                evidence=factor,
            ),
        ]
