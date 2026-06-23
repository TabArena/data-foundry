---
unique_name: hotel_booking_demand
name: Hotel booking demand
checked_by:
- Andrej
data_foundry_status: 'Yes'
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
source_row: 732
type_adapter_id: curation-record-v1
---

# Hotel booking demand

## Comments

Data from two hotels - can likely be comncatenated.

Notes from the paper: 
"data point time for each observation was defined as the day prior to each booking׳s arrival"

"Data was extracted via TSQL queries executed directly in the hotels’ PMS database"

The authors even thought about leakage: "One of the most important properties in data for prediction models is not to promote leakage of future information [3]. In order to prevent this from happening, the timestamp of the target variable must occur after the input variables’ timestamp. Thus, instead of directly extracting variables from the bookings database table, when available, the variables’ values were extracted from the bookings change log, with a timestamp relative to the day prior to arrival date (for all the bookings created before their arrival date)"

"A word of caution is due for those not so familiar with hotel operations. In hotel industry it is quite common for customers to change their booking׳s attributes, like the number of persons, staying duration, or room type preferences, either at the time of their check-in or during their stay. It is also common for hotels not to know the correct nationality of the customer until the moment of check-in. Therefore, even though the capture of data took considered a timespan prior to arrival date, it is understandable that the distribution of some variables differ between non canceled and canceled bookings. Consequently, the use of these datasets may require this difference in distribution to be taken into account."
--> Might need to drop some features

The data would allow to predict no shows as a second target

The distributions are suspiciously clean, But the data source seems valid.

## Reference

Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. Data in brief, 22, 41-49.
