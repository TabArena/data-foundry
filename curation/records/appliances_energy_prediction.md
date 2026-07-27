---
unique_name: appliances_energy_prediction
name: Appliances Energy Prediction
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Forecasting)
collections:
- TabArena Reject
source_links:
- https://doi.org/10.24432/C5VC8G
- https://github.com/LuisM78/Appliances-energy-prediction-data
source_row: 266
type_adapter_id: curation-record-v1
---

## Comments

CC: "data from 10 mins for about 4.5 months, extra random variables"

CC (2026-07-27, Lennart): Confirmed **No — time-series forecasting**. The data has a **date column**
(10-min readings over ~4.5 months), so it is a temporal task. The original paper evaluates it with a
**leaking (random) split** — but that is the authors' choice, not a property of the task: a random split
on this temporal stream leaks future information into training. Papers can pick the wrong split, so the
prescribed evaluation protocol is **not authoritative** and must be checked against the task design.
Correctly excluded as forecasting rather than treated as in-scope temporal regression.

## Reference

Data driven prediction models of energy use of appliances in a low-energy house
By L. Candanedo, V. Feldheim, Dominique Deramaix. 2017

Published in Energy and Buildings, Volume 140
