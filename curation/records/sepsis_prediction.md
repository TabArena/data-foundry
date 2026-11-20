---
unique_name: sepsis_prediction
name: SepsisPrediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Within Entity'
- 'Time: Lost'
- 'Target: Later'
- 'Entities: Recur'
- Panel Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: Kaggle
year: '2019'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/salikhussaini49/prediction-of-sepsis
notebook_path: datasets/beyond_iid/grouped/sepsis_prediction/sepsis_prediction_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/sepsis_prediction_1m/dataset.py
source_row: 689
type_adapter_id: curation-record-v1
---

## Comments

CC: "Highly imbalanced, high missing values, requires some feature preprocessing, unclear if patient duplicates; potential data leakage for unit 1 and unit 2 or group-based data; survival prediction task transformed into binary classification (creates some problems)"

https://physionet.org/content/challenge-2019/1.0.0/

CC (2026-10-01, Lennart): Leak audit: the data is fine; the scoring has to change (planned). Each row is one patient-hour with only that hour's measurements, and SepsisLabel is 1 from 6 hours before onset onward, so at every hour the task is "sepsis within the next 6 hours"; no row feature encodes the time left in the stay. The risk is in the evaluation: grouped splits put complete patient records into the test set, and septic records end shortly after onset, so a method that uses a patient's later rows (record length, last Hour/ICULOS) can read the outcome. Going forward, predictions must be causal per patient and scored with the PhysioNet 2019 utility per patient (already declared as the metric, with group_on = Patient_ID and group_time_on = Hour) rather than as independent rows. Patient_ID is group metadata and must not be used as a model feature. Documented in the v2 definition's curation comments.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source normalized_early_detection_utility — PhysioNet/CinC Challenge 2019 normalized utility score (Reyna et al. 2020, Early prediction of sepsis from clinical data: the PhysioNet/Computing in Cardiology Challenge 2019, Crit Care Med 48(2):210-217; https://physionet.org/content/challenge-2019/1.0.0/); inputs {"group": "Patient_ID", "order": "Hour"}.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

CC (2026-11-18, Andrej): time basis `UnseenGroup` in place of `ForcedGroupedFromTemporal` (Review issue 3, B; full-information split check; as dementia_prediction): the use case scores new ICU patients, the tree's panel leaf for new units. The split is unchanged (whole patients); patients admitted later stay untested.

## Review

**Outcome:** added as `sepsis_prediction_1m`. Full-information split check of 2026-11-18: the time basis tag disagreed with the split tree; decided below.

**Main points:** Tag the patient folds `UnseenGroup`, as dementia_prediction?

**Issues for Andrej:**

3. **Tag the patient folds `UnseenGroup`, as dementia_prediction?**

   * **Problem:**
     - The use case scores new ICU patients only, which the tree's panel branch gives as `UnseenGroup` (new units)[^s32u], and the tree names sepsis as that leaf's example.
     - The definition still carries `ForcedGroupedFromTemporal`, which no one chose under the tree; you moved dementia_prediction, the same leaf, to `UnseenGroup` on 2026-11-17[^ug_dem].
     - The folds are right either way: whole patients.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Grouped by patient, `ForcedGroupedFromTemporal` (implemented) | No change | | Not the tree's leaf |
     | B | The same folds, `UnseenGroup` | The Time basis line opens with `UnseenGroup` and names the later calendar as untested | The tree's leaf; as dementia | |

   * **Recommendation:** B. **Decision:** A or B?

   [^s32u]: **SPLIT-32** (Should): "does the use case aim at groups the data does not hold, rather than at a later period? ... the split groups by that unit ... That is `UnseenGroup`." The tree's panel leaf: "Only new units, met after the data (new patients, new customers) → Grouped · `UnseenGroup` (new units)".
   [^ug_dem]: dementia_prediction, the same panel leaf: "Option B: The same 3-fold CV over whole subjects, tagged UnseenGroup" (Andrej, 2026-11-17).

   **Andrej (2026-11-18, change):** Option B: The same folds, UnseenGroup.

   **Resolved (2026-11-18, Andrej):** B. `data_tags` names `UnseenGroup` in place of `ForcedGroupedFromTemporal`, and the `Time basis:` line opens with `UnseenGroup (Andrej, 2026-11-18; ForcedGroupedFromTemporal before)`: new ICU patients, whole patients held out; later admissions stay untested. The folds are unchanged.

## Reference

Kaggle / PhysioNet
