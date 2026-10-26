---
unique_name: myocardial_infarction_complications
name: Myocardial infarction complications
checked_by:
- Lennart
suggestion: 'Yes'
priority: 2
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

**Open issues (AI, 2026-10-07):** not added; duplicate. The same file as `mic`.

1. **Duplicate of `mic`: mark the record `No` + `Duplicate`?** Evidence in the assessment above (same DOI,
   byte-identical file, a swapped outcome column of the same 1,700 patients). Implemented now: nothing; no folder.
   Alternative: ship a second folder with an arrhythmia target next to `mic`; the guidelines call that a duplicate,
   and no two folders of the working copy share their rows. The convention would rename the record to
   `mic_duplicate`.

2. **Which outcome should `mic` predict?** The record prefers an arrhythmia complication over the lethal outcome.
   The source ranks none of its 12 outcomes: the description (Golovenkin et al., Leicester PDF, p. 1) offers
   "prediction of complications based on patient information (i) at the time of admission and (ii) on the third day
   of the hospital period", and its bibliography has papers on both (p. 11, items 6 and 7: "Prediction of the
   occurrence of atrial fibrillation and ventricular fibrillation ..." and "Prediction of lethal outcome ...").
   Implemented now: `mic` keeps LET_IS at admission, a valid source-defined task with clear signal, unchanged since
   TabArena v0.1 (`task_probes.md` rule 6: a valid task stays). Alternative, if the arrhythmia framing is preferred:
   switch `mic` to atrial fibrillation (FIBR_PREDS, binary, ROC AUC; drop LET_IS with the other 10 outcomes), the
   only arrhythmia outcome with enough positives whose signal does not rest on an ICU treatment column. Ventricular
   fibrillation would need the ICU drug columns dropped first (lidocaine is the treatment of ventricular arrhythmias,
   and the column has no time stamp, although the source allows it at admission). Side note: `mic`'s comment "We use
   the categorical target as it summarizes the other possible targets" does not hold: 766 of the 935 patients with at
   least one of the 11 complications survived (LET_IS = 0), and 102 of the 271 deaths carry no complication flag.

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Open issue 1: duplicate of mic (byte-identical file); run did not add it). Same patients and file as mic, already shipped; at most a reason to switch mic's target, not a new dataset.

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
