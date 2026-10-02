---
unique_name: hotel_booking_demand
name: Hotel booking demand
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Other
year: '2019'
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

## Reference

Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. Data in brief, 22, 41-49.
