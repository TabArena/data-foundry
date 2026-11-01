---
unique_name: mic_duplicate
name: Myocardial infarction complications
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- New IID
collections:
- New (BeyondArena)
original_source: UCI
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C53P5M
source_row: 668
type_adapter_id: curation-record-v1
---

## Comments

Has multiple datasets / outcomes in one. Take one at most. Moreover, clearly describes which time points we could simulate with the data.

Hard to decide for one target. All of them have some merit. According to Dr. ChatGPT, it is better to model some of the Arrhythmias related cases and avoid the lethal outcome. Make judgement call based on data

**Assessment (AI, 2026-10-07):** Same data as `mic`, which ships in TabArena v0.1, BeyondArena and the v0.2 working copy (LET_IS at admission): the UCI 579 file behind doi 10.24432/C53P5M is byte-identical to `mic`'s `MI.data` (1,700 patients, outcome columns 113-124). A second outcome of the same patients is a duplicate (guidelines: a swapped outcome column), so it was not added; suggest `No` + `Duplicate` as `mic_duplicate`. If an arrhythmia target is preferred, switch `mic` instead: atrial fibrillation (FIBR_PREDS, 170 positives, 57 per test fold) reaches ROC AUC 0.71-0.72 at admission (10 x 3 CV) and does not depend on the ICU drug columns; ventricular fibrillation (71) rests on ICU lidocaine (AUC 0.74, 0.65 without), and SVT (20) has no signal.

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Open issue 1: duplicate of mic (byte-identical file); run did not add it). Same patients and file as mic, already shipped; at most a reason to switch mic's target, not a new dataset.

CC (2026-10-26, Lennart): "Yes rename and no": `No` + `Duplicate` of mic (same DOI, a byte-identical file), renamed from myocardial_infarction_complications to mic_duplicate (records.md, duplicates). Issue 2: mic keeps LET_IS at admission (as implemented).

**Assessment (AI, 2026-10-26):** the open issues of 2026-10-07 are settled and removed from this record; they said: the record is the same file as mic (UCI, DOI 10.24432/C53P5M) with another outcome column preferred, and mic's LET_IS at admission is a valid source-defined task.

## Reference

@article{golovenkin2020trajectories,
  title={Trajectories, bifurcations, and pseudo-time in large clinical datasets: applications to myocardial infarction and diabetes data},
  author={Golovenkin, Sergey E and Bac, Jonathan and Chervov, Alexander and Mirkes, Evgeny M and Orlova, Yuliya V and Barillot, Emmanuel and Gorban, Alexander N and Zinovyev, Andrei},
  journal={GigaScience},
  volume={9},
  number={11},
  pages={giaa128},
  year={2020},
  publisher={Oxford University Press}
}
