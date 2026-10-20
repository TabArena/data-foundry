# pkdd_15_taxi_trip_time_prediction_ii

**Outcome:** added as `pkdd_15_taxi_trip_time_prediction_ii_1m`. The travel time of a Porto taxi trip at its start,
from origin, destination, local start time, call type, stand and taxi (log target), temporal with three monthly test
windows (April to June 2014). The AI recommends shipping it; whether the destination may be a feature is open
(issue 1).

**Main points:** The destination is a feature (an ETA once the destination is known), although the source's task has
no destination.

**Record fields that disagree with the definition:**

- `domain`: record `Other`, definition `industry & manufacturing`.

**Record judgment:** valid with concerns. The competition's own Task II is a sequence task; the curator's framing (ETA
at the start of the trip) is a regression with a temporal split, in scope. The concern: the source says the
destination is not known to the dispatch system (issue 1).

**Issues for Lennart:**

1. **Framing: the destination as a feature.**
   - Question: keep the destination-known ETA, or ship the pickup-only task?
   - Evidence: in the source the destination is recorded at the end of the trip. The data page says "The last list item
     corresponds to the trip's destination". The challenge overview (geolink.pt, Wayback 2015) says "In most cases, taxi
     drivers operating through an electronic dispatch system do not indicate the final destination of the ride"; that is
     why Task I asks for it. Lam et al. 2015, Sec. 1: "busy taxi drivers do not report the final destination of the
     ride".
   - Your CC of 2026-09-21 rejected pickup-only for its weak signal (R^2 0.14). That reason predates task_probes.md rule
     2 (2026-10-06: a small but real signal is no reason to drop a task). Rule 6: "A better version the source itself
     defines ... replaces the current one". Pickup-only is the source's own question, when a busy taxi will be free.
   - Numbers on the shipped splits: R^2 0.118 / 0.113 / 0.150 without the destination, against 0.502 / 0.478 / 0.503
     with it. The signal is real on 3 of 3 windows.
   - Implemented: your framing.
   - If you switch: drop `end_lon` / `end_lat` and keep the filters. The folder stays `_1m` with a new checksum. Only
     one framing can ship, since they are the same data.
   - `nyc_taxi_trip_duration` differs: its source kept the dropoff coordinates as features on purpose.

2. **Two row filters beyond your list.**
   - (a) Trips under 60 s: 15,533 (0.9%), holding 21% of the variance of the log travel time. The share of trips that
     end within 100 m of their start falls from 70% at 15 s to 50% at 30 s, 40% at 45 s, 31% at 60 s and 7% at 120 s, so
     the 60-s cut is a choice on that slope. Two taxis record 3,352 of them (35% and 23% of their own trips).
   - (b) A start-to-end straight line faster than 120 km/h: 741 trips, 725 of them with a jump of over 1 km between two
     15-second GPS points.
   - Implemented: both dropped.
   - Alternative: keep them and drop only trips with < 2 points, as listed. `nyc_taxi_trip_duration` drops trips under
     30 s (its clock has 1-s resolution).

3. **Trips that end where they start (kept).**
   - 65,708 trips (4.0%) end within 500 m of their start and 23,712 (1.4%) within 100 m. Those within 100 m last a
     median 16.2 min, against 5.5 min for trips of 0.5-1 km: a meter left on or a round trip, with no destination a
     passenger would give.
   - The trips within 500 m hold 13.8% / 13.9% / 14.8% of the test variance (June / May / April). R^2 is 0.502 / 0.478 /
     0.503 with them and 0.552 / 0.528 / 0.554 without. That is noise, not a leak.
   - Implemented: kept, with an anomaly bullet.
   - Alternative: drop trips that end within 100 m of their start. That filter is on a feature, so a deployment could
     apply it. NYC kept its 0.4% of one-point trips.

4. **"Taxi as group" from the verdict.**
   - v2 refuses a task that is both grouped and temporal (`src/data_foundry/v2/dataset.py:1114`).
   - Implemented: temporal, with `taxi_id` as a categorical feature. 99.93% / 100% / 100% of the April / May / June
     trips are by taxis seen before (0-1 new taxi per month, 428-434 taxis active each month).
   - Alternative: a grouped split by taxi, which would test new drivers.
   - After the cleaning, taxi_id changes LightGBM R^2 by only -0.004 to +0.003. Its earlier strength came from a few
     taxis that record most of the sub-minute trips.

5. **ORIGIN_CALL dropped.**
   - After the row filters: 56,780 phone ids for 361,050 central trips, one id (2002) on 15.8%.
   - With the destination it changes R^2 by -0.001 to +0.002 as a LightGBM categorical; pickup-only it adds +0.002 to
     +0.005.
   - Alternative: keep it as a 57k-level categorical. A Kaggle write-up (topic 15019) found it "very helpful" for the
     partial-trajectory task.

6. **Window length.**
   - Implemented: 3 calendar months (horizon 1 month), because the challenge tested 1.5-6 months after its training
     year.
   - Alternative: 3 x 7 days, as in delivery_eta_1m, maps_router_eta_1m and nyc_taxi_trip_duration (31,699-34,810 trips
     per week here).

7. **Hour of day (pipeline choice).**
   - BeyondArena's `tabarena_default` preprocessing keeps the hour: it encodes datetimes with skrub's DatetimeEncoder
     (`tabarena/benchmark/preprocessing/date_feature_generators.py`).
   - Only the TabArena v0.1 `default` pipeline loses it, through AutoGluon's year/month/day/dayofweek
     (`autogluon/features/generators/datetime.py:27`). LightGBM R^2 is 0.484 / 0.453 / 0.463 with those parts against
     0.502 / 0.478 / 0.503 with the local hour.
   - Implemented: no extra column. Your call: which pipeline v0.2 runs.

8. **Label noise kept.**
   - 1.2% of the kept trips jump more than 1 km between two GPS points, a GPS error or missing points, so the (points -
     1) x 15 s label can be too short. Some trips also include a return with the meter on (Lam et al. 2015, Sec. 2).
   - Implemented: kept, since this is the challenge's own label definition.
   - Alternative: drop the 19,673 trips with a jump.

9. **Local time.**
   - TIMESTAMP is UTC: at both daylight-saving switches the weekday profile by UTC hour moves by one hour (correlation
     0.92 / 0.90 unshifted, 0.99 shifted).
   - Implemented: Europe/Lisbon wall-clock time without a time zone.
   - Alternative: keep UTC.

10. **Year.**
    - The two docstrings disagree. The v2 attribute (`src/data_foundry/v2/dataset.py:221`) says "Year the data was
      published"; the schema's `dataset_year` (`schema.py:192`) says "The year when the data was collected/created".
    - Implemented: `year = "2015"`, as in the record, the v2 docstring and the competition datasets of the working copy
      (kick 2011 for 2009-10 data, acquire_valued_shoppers_challenge 2014 for 2012-13, rossmann_store_sales 2015 for
      2013-15). The BibTeX follows UCI's own citation (2013).
    - Alternative: `year = "2013"`, UCI's year of creation.
