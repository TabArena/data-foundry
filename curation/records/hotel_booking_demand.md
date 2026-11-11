---
unique_name: hotel_booking_demand
name: Hotel booking demand
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Other
year: '2018'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.sciencedirect.com/science/article/pii/S2352340918315191#s0005
notebook_path: datasets/beyond_iid/temporal/hotel_booking_demand/hotel_booking_demand.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hotel_booking_demand/dataset.py
source_row: 732
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Split leak fixed: training rows with a future arrival were all cancelled.** The split kept "bookings that have arrival dates in the future, but were already canceled at the given prediction point" in training. At a prediction point, the only known future bookings are the cancelled ones, so these rows taught "arrival in the test window = cancelled": on the newest split 867 such rows (1.4% of training), 100% cancelled, against 12.5% cancelled in the test set (leak audit 2026-09-24; independent probe "Why we lose on hotel_booking_demand", 2026-08-20, gs://priorlabs-html-reports/hotel_booking_demand_probe_20260820/report.html, which shows every model over-predicting cancellations and in-context models hurt most). Fix: training uses only bookings arriving before the prediction point. Also dropped as recorded after the prediction point (Antonio et al. 2019, Data in Brief 22, Table 1): BookingChanges ("until the moment of check-in or cancellation"), AssignedRoomType (set by hotel operations) and RequiredCarParkingSpaces (> 0 in 6,470 bookings, none cancelled). Caveat from the data paper: every variable is a snapshot of "the day prior to each booking's arrival", later than our prediction point (up to three months before arrival). Result on the three newest splits: LightGBM AUC 0.81-0.83, log loss 0.32-0.36 (was about 1.7), mean prediction 0.20-0.24 vs true 0.125-0.14. The migrated split also crashed (outcome columns dropped before use); they are now dropped after splitting.

Data from two hotels - can likely be concatenated.

Notes from the paper: 
"data point time for each observation was defined as the day prior to each booking׳s arrival"

"Data was extracted via TSQL queries executed directly in the hotels' PMS database"

The authors even thought about leakage: "One of the most important properties in data for prediction models is not to promote leakage of future information [3]. In order to prevent this from happening, the timestamp of the target variable must occur after the input variables' timestamp. Thus, instead of directly extracting variables from the bookings database table, when available, the variables' values were extracted from the bookings change log, with a timestamp relative to the day prior to arrival date (for all the bookings created before their arrival date)"

"A word of caution is due for those not so familiar with hotel operations. In hotel industry it is quite common for customers to change their booking׳s attributes, like the number of persons, staying duration, or room type preferences, either at the time of their check-in or during their stay. It is also common for hotels not to know the correct nationality of the customer until the moment of check-in. Therefore, even though the capture of data took considered a timespan prior to arrival date, it is understandable that the distribution of some variables differ between non canceled and canceled bookings. Consequently, the use of these datasets may require this difference in distribution to be taken into account."
--> Might need to drop some features

The data would allow to predict no shows as a second target

The distributions are suspiciously clean, but the data source seems valid.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: IsRepeatedGuest.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The data paper publishes the data without a prediction task or metric; the authors' earlier cancellation-prediction papers used other (non-public) data and reported several metrics (accuracy, precision, AUC), none set as the task's metric.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `DepositType` (the README lists their levels); left unordered: `ArrivalDateMonth` (a partial order); `Meal` (a level outside the scale is a state of its own).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 calendar or compass cycles ordered; 1 columns with a state outside the scale ordered, the state placed by the rule; Meal's Undefined is SC (the paper), the meal plan ordered; the arrival month ordered.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (the data article of Antonio et al. 2019), shape +, risk 0 (the open issue is the choice of prediction dates).

CC (2026-11-11, Lennart): REVIEW.md issue 1, reply (a) to the answer of 2026-11-11 ("Reply (a): All ten dates"; he had asked "Why can we not extend it or roll back from the newest data to include 1 Jun in option (A) as well?"): the test uses the ten prediction dates 1 September 2016 to 1 June 2017, today's nine and 1 June 2017, the newest date whose three months of arrivals the data holds; SPLIT-14 as amended on 2026-11-11 admits the two oldest, signed off here: 1 October and 1 September 2016 train on 48.3% and 44.0% of the bookings (two windows under half, eight at or above it).

CC (2026-11-11, Lennart): the declared horizon (three months of arrivals, no gap, windows starting on the first of each month from 2017-06-01 back to 2016-09-01) is checked, as the source's system scores every open booking and sets no length, and three months hold 38% to 69% of the open bookings while letting the newest complete date reach June 2017 (REVIEW.md horizon, ok).

**Assessment (AI, 2026-11-11):** applied issue 1 (reply a): `_make_splits` lists the ten dates (1 June 2017 added; its rules unchanged). Counted with the split's own rules on the 81,418 bookings: test 6,511, 6,390, 6,015, 5,768, 4,578, 2,500, 2,474, 3,228, 4,314 and 4,596 (1 June 2017 back to 1 September 2016), train 64,524, 60,693, 57,112, 53,850, 50,982, 48,617, 45,946, 42,942, 39,297 and 35,860 (79.3%, 74.5%, 70.1%, 66.1%, 62.6%, 59.7%, 56.4%, 52.7%, 48.3% and 44.0%); 10.9% of the newest date's test bookings are cancelled (12.5% at 1 May 2017). `task_summary`, the notes and `splits_comment` name the ten dates, the latest prediction point (1 June 2017, arrivals to 31 August 2017), the two dates under half and the horizon's reason. `dataset check`: 0 errors, 0 warnings, with `splits_train_under_half` accepted on the CC line above.

## Reference

Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. Data in brief, 22, 41-49.
