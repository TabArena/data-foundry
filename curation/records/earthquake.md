---
unique_name: earthquake
name: earthquake
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Time-series (Forecasting)
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '2023'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/alessandrolobello/the-ultimate-earthquake-dataset-from-1990-2023
- http://www.stern.nyu.edu/SOR/SmoothMeth
source_row: 803
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target  / Scientific Discovery`, SEL-3; `Time-series (Forecasting)`, SEL-10): a catalogue of every earthquake recorded 1990-2023 with no predictive target; the uploader offers it for "analyzing spatial and temporal distribution patterns" and to "forecast future seismic events".
- Source: Kaggle upload "All the Earthquakes Dataset : from 1990-2023" by alessandrolobello (Aug 2023, https://www.kaggle.com/datasets/alessandrolobello/the-ultimate-earthquake-dataset-from-1990-2023), "The data are from https://www.usgs.gov/" (the USGS ComCat catalogue is the first source, PROV-8). As published: one CSV of about 3 million events (494.8 MB), columns time, place, status, tsunami, significance, data_type, magnitudo, state, longitude, latitude, depth, date; no target named.
- Use case: none stated beyond research, public awareness and forecasting ("develop predictive models to forecast future seismic events more accurately"); predicting one catalogue column from the others (magnitude from depth and place, `significance`, which USGS computes from magnitude, felt reports and damage estimates) fits no decision; forecasting future events is SEL-10.
- Siblings and duplicates: `quake` (Simonoff 1996, 2,178 earthquakes 1964-1986, OpenML 550; `No`, Scientific Discovery: "Lennart: ... not a predictive task originally and not a real task either", which named this Kaggle upload as its "newer version"). Not a row duplicate of `quake` (other years), so the old `Duplicate` marker is dropped. The record's second link (stern.nyu.edu/SOR/SmoothMeth) is the book of `quake`, not of this upload. External collections: TabSTAR (as recorded; the target it used not checked).
- Metric: none found (Kaggle description).
- The human note on this record ("Unsure if a real task, or how it could be used. However, we can still take a look at it") leaves it open; `quake`'s verdict is the precedent with the same facts.
- Reject check (AI, 2026-10-22): stands. The Kaggle upload of the USGS catalogue names no target; its only stated uses are pattern analysis and forecasting ('develop predictive models to forecast future seismic events', https://www.kaggle.com/datasets/alessandrolobello/the-ultimate-earthquake-dataset-from-1990-2023). The precedent quake was rejected by Lennart on the same facts: 'not a predictive task originally and not a real task either'. A TabSTAR target, if there is one, would be a relabel under SEL-8 (not checked).

A Kaggle compilation of global earthquakes 1990-2023 (date, location, depth, magnitude). It has no well-defined supervised target: magnitude/occurrence prediction is a temporal forecasting / scientific-discovery problem rather than a fixed IID tabular task, and it is already tagged TabArena Reject / 2nd Tier. The record also notes it relates to OpenML d/550, suggesting overlap with existing data. Excluded as a forecasting / no-good-target scientific catalogue; a human need only confirm there is no extractable fixed classification/regression target before final rejection.

---

Unsure if a real task, or how it could be used. However, we can still take a look at it

Related/based on openml.org/d/550
