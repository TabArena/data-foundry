---
unique_name: aeolus_rebuilt
name: US flight delays with weather (Aeolus rebuilt from BTS and Meteostat)
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
original_source: GOV Website
year: '2026'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FGJ
- https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FLL
- https://dev.meteostat.net/data/timeseries/hourly
- https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv
v2_path: datasets/_dev/tabarena-v0pt2/aeolus_rebuilt_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Created on 2026-10-26 at Lennart's ask (aeolus, REVIEW issue 8): rebuild the Aeolus task from its origins, the BTS Reporting Carrier On-Time Performance table and Meteostat's hourly station weather, joined in UTC at the last reading before the scheduled departure, instead of the Aeolus release's weather join (local clock times read as UTC). A rebuild from other sources is a new dataset with its own record (PROV-11, PROV-14).

CC (2026-10-26, Lennart): "Can you rebuild this please, but keep it aeolus_correct or something? I assume we have all the information we need from the original sources, or is the data release from aeolus / the paper the only source of some information? if the paper state does not add much, we can build our better version as intended"

**Assessment (AI, 2026-10-26):** The Aeolus release and paper hold nothing this task needs that the origins lack. The Kaggle release has three parts: Flight_Tab (nine yearly CSVs: BTS flights with Meteostat temperature, precipitation and wind at both airports, the airports' coordinates and the authors' airport indexes), Flight_chain (27 PyTorch files of daily sequences) and Flight_network (3,234 daily DGL graphs, March 2024 included). All are built from BTS fields: the chains group by carrier, flight number and date (Sec. 3.2: "Dynamic grouping is then performed using (OP_CARRIER, OP_CARRIER_FL_NUM, DATE)"), not by aircraft as Sec. 1 says ("flights operated by the same tail number"), and the graphs link flights at the same airport at adjacent times (Sec. 3.3). The paper adds the task (delay over 15 minutes, AUC and ACC, App. B.2) and a split we do not follow. The origins give what the release lacks or damaged: the weather of the right hour (the release read it 3.5-11 h early), March 2024 (585,413 operated flights), the 192,954 flights of 43 airports the release dropped, tail numbers (the aircraft's previous flight), cancellations and diversions, and BTS's coordinates. Built as `aeolus_rebuilt_1m` (a `_1m` version, as the row budget requires) from the BTS on-time files, the BTS Master Coordinate table, NOAA's ISD station history and Meteostat: 13,708,650 operated flights of 2023-2024, aeolus_1m's three two-week windows, 34 features. With aeolus_1m's inputs the weather of the right hour adds 0.043-0.051 ROC AUC per window against 0.032-0.039 in aeolus_1m; the aircraft's previous flight adds 0.15-0.17, to 0.80-0.83 (untuned LightGBM, 1M training rows). Open for the curator: the aircraft-swap potential leak, cancelled flights as rows, the prediction point, and retiring aeolus_1m once this is accepted (PROV-6).

CC (2026-10-26, Lennart): issue 1: keep the operated flights only, "so we do not have these as rows in the data and could use the model as intended".

CC (2026-10-26, Lennart): issues 2 and 3 as implemented: the prediction point at the full hour before departure; the previous flight's columns kept with the note on aircraft swaps.

CC (2026-10-26, Lennart): issue 4: keep Meteostat's forecast-filled values, "remark this at least, this is good to know as a model-dependent outcome!"

CC (2026-10-26, Lennart): issue 6: "keep roc auc and label it as you see fit": the fallback (MET-5: the paper reports AUC and accuracy side by side).

CC (2026-10-26, Lennart): the record's year takes the definition's value (2026, the pinned snapshot).

**Assessment (AI, 2026-10-26):** applied: the remark on the model-filled weather in the notes, the metric relabelled as the fallback (same ROC AUC). No open issue is left, so the folder's REVIEW.md is removed; the review panel has not run (the curator's call of 2026-10-26).

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `O_COCO` (a partial order); `D_COCO` (a partial order); `INBOUND_STATUS` (a level outside the scale is a state of its own).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 columns with a state outside the scale ordered, the state placed by the rule.
